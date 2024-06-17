import sys
import pandas as pd
import PyPDF2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def main(file_path, file_type):
    if file_type == 'csv':
        songs = read_songs_from_csv(file_path)
    elif file_type == 'pdf':
        songs = read_songs_from_pdf(file_path)
    elif file_type == 'log':
        songs = read_songs_from_log(file_path)
    else:
        print("Unsupported file type")
        return

    print(f"Read {len(songs)} songs from {file_path}")
    print(songs)  # Debug: print the list of songs

    if not songs:
        print("No songs found. Exiting.")
        return

    driver = setup_browser()
    try:
        search_and_queue_songs(driver, songs)
    finally:
        driver.quit()

if __name__ == "__main__":
    file_path = sys.argv[1]  # path to the input file
    file_type = sys.argv[2]  # type of the input file ('csv', 'pdf', 'log')
    try:
        main(file_path, file_type)
    except Exception as e:
        print(f"An error occurred: {e}")
