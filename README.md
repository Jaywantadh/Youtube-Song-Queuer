# YouTube Song Queue Automator

This project is an automation script that reads song names from a file (CSV, PDF, or log) and creates a queue of these songs on YouTube. The script uses Python and Selenium for web automation.

## Features

- Reads song names from CSV, PDF, or log files.
- Searches for each song on YouTube.
- Adds the first search result to the YouTube queue.

## Requirements

- Python 3.7+
- `selenium` library
- `pandas` library
- `PyPDF2` library
- Google Chrome browser
- ChromeDriver

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/YouTube-Song-Queue-Automator.git
    cd YouTube-Song-Queue-Automator
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Download ChromeDriver:**

    Make sure to download the ChromeDriver version that matches your installed version of Chrome. You can download ChromeDriver from [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). Place the downloaded `chromedriver` executable in your project directory or add it to your system PATH.

## Usage

1. **Prepare your input file:**

    Ensure you have a CSV, PDF, or log file with the list of song names. For a CSV file, make sure the column with song names is titled `song`.

2. **Run the script:**

    ```bash
    python youtube_queue.py path_to_your_file file_type
    ```

    - `path_to_your_file`: Path to your input file.
    - `file_type`: Type of your input file (`csv`, `pdf`, or `log`).

    For example, if you have a CSV file named `songs.csv`:

    ```bash
    python youtube_queue.py songs.csv csv
    ```

## Example

Here is an example of how your CSV file (`songs.csv`) might look:

song
Shape of You by Ed Sheeran
Blinding Lights by The Weeknd
Uptown Funk by Mark Ronson ft. Bruno Mars
Contributing
This project is still in development and we welcome contributions from the community. Here are some ways you can help:

##Fix bugs and issues.
Improve the script to handle edge cases.
Add support for more file formats.
Optimize the Selenium interactions.
Improve error handling and logging.
Please feel free to fork this repository and submit pull requests.

##License
This project is licensed under the MIT License - see the LICENSE file for details.

##Acknowledgements
This project uses the selenium library for web automation.
Thanks to the open-source community for their contributions and support.
If you have any questions or need further assistance, please feel free to open an issue on the GitHub repository.



This `README.md` file provides a comprehensive overview of the project, including installation instructions, usage examples, and contribution guidelines. Feel free to customize it further based on your specific needs and preferences.






