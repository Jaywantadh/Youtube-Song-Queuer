import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
import threading
import sys
import time
import pandas as pd
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageTk


def read_songs_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df['songs'].tolist()

def read_songs_from_pdf(file_path):
    song_list = []
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfFileReader(file)
        for page_num in range(reader.numPages):
            page = reader.getPage(page_num)
            text = page.extractText()
            songs = text.split('\n')
            song_list.extend(songs)
    return song_list

def read_songs_from_log(file_path):
    with open(file_path, 'r') as file:
        songs = file.readlines()
    return [song.strip() for song in songs]

def setup_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def search_and_queue_songs(driver, song_list):
    driver.get("https://www.youtube.com")

    for song in song_list:
        try:
            # Search for the song
            search_box = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            search_box.clear()
            search_box.send_keys(song)
            search_box.send_keys(Keys.RETURN)

            # Wait for search results to load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "(//button[@aria-label='Action menu'])[1]"))
            )

            # Click the three-dot menu of the first video in the search results
            first_video_menu = driver.find_element(By.XPATH, "(//button[@aria-label='Action menu'])[1]")
            first_video_menu.click()

            # Wait for the menu to become interactive
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//yt-formatted-string[text()='Add to queue']"))
            )

            # Add the song to the queue
            add_to_queue = driver.find_element(By.XPATH, "//yt-formatted-string[text()='Add to queue']")
            add_to_queue.click()

            

        except Exception as e:
            print(f"Failed to add {song} to queue: {e}")

def start_playback(driver):
    try:
        play_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ytp-play-button') and @aria-label='Play']"))
        )
        play_button.click()
    except Exception as e:
        print(f"Failed to start playback: {e}")

def wait_for_queue_to_finish(driver):
    try:
        # Wait until the queue has been exhausted
        while True:
            # Check if there's a "Next" button that indicates the presence of more songs
            next_button = driver.find_elements(By.XPATH, "//a[@aria-label='Next']")
            if not next_button:
                break
            time.sleep(30)  # Check every 30 seconds
    except Exception as e:
        print(f"Error while waiting for the queue to finish: {e}")


def process_file(file_path):
    if file_path.endswith('.csv'):
        songs = read_songs_from_csv(file_path)
    elif file_path.endswith('.pdf'):
        songs = read_songs_from_pdf(file_path)
    elif file_path.endswith('.log'):
        songs = read_songs_from_log(file_path)
    else:
        messagebox.showerror("No songs found","No songs were found in selected file")

    print(f"Read {len(songs)} songs form {file_path}")
    print(songs)

    driver = setup_browser()
    
    try:
        search_and_queue_songs(driver, songs)
        start_playback(driver)
        wait_for_queue_to_finish(driver)
    finally:
        driver.quit()

def handle_file_selection(event=None):
    file_path = filedialog.askopenfilename()

    if file_path:
        threading.Thread(target=process_file, args=(file_path,)).start()

def drop(event):
    file_path = event.data
    threading.Thread(target=process_file, args=(file_path,)).start()


def main():
    root = TkinterDnD.Tk()
    root.title("YouTube Song Queuer")

    label = tk.Label(root, text= "Drag and drop file here or click 'Import file'")
    label.pack(pady=20)

    drag_drop_image = Image.open("drag-and-drop.png")  # Make sure to have this image in the same directory
    drag_drop_image = drag_drop_image.resize((300, 200), Image.LANCZOS)
    drag_drop_image = ImageTk.PhotoImage(drag_drop_image)

    frame = tk.Frame(root, width=400, height=200, bg='gray')
    frame.pack(pady=20)
    frame.drop_target_register(DND_FILES)
    frame.dnd_bind('<<Drop>>', drop)

    image_label = tk.Label(frame, image=drag_drop_image)
    image_label.image = drag_drop_image  # Keep a reference to avoid garbage collection
    image_label.pack()

    import_button = tk.Button(root, text="Import File", command= handle_file_selection)
    import_button.pack(pady= 20)

    root.geometry('500x400')
    root.mainloop()
    
    print("Thanks for using this application!")
    

if __name__ == "__main__":
    main()
