

## Prerequisites

- **Python 3.10:** Make sure you have Python 3.10 installed. You can download it from the [official Python website](https://www.python.org/downloads/).

- **Virtual Environment (venv):** Create a virtual environment to manage project dependencies.
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows, use venv\Scripts\activate
  ```

- **Install Dependencies:** Install project dependencies using `requirements.txt`.
  ```bash
  pip install -r requirements.txt
  ```

## Project Structure

- **`config.py`:** Configuration file containing constants and settings for the application.

- **`pipeline.py`:** Python script that handles scraping and processing

- **`main.py`:** Main Python script that orchestrates the scraping process.



- **Python Version:** 3.10


- **Dependencies:** Check `requirements.txt` for the list of Python packages used in this project.

## Usage

1. Ensure you have the required libraries installed: `requests`, `beautifulsoup4`, `pandas`, `loguru`.

2. Create a text file named `hotels.txt` with a list of hotel names and locations.

3. Run the script. It will scrape data for each hotel, save it as Feather files, and then merge and save as a CSV file.

```bash
python main.py
# economical_analysis
