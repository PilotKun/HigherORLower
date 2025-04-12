# Higher or Lower Anime Game Bot

## Description

This Python bot automatically plays the "Higher or Lower" game specifically for the Anime category on `https://www.higherorlowergame.com/anime/score/`.

It uses Selenium to interact with the web browser, fetches anime score data from the Jikan API (`api.jikan.moe`), caches scores locally in an SQLite database to minimize API calls, and employs fuzzy string matching to find the most accurate anime entry when dealing with potentially ambiguous titles returned by the game vs. the API. It also considers the type (TV, Movie, OVA, etc.) provided by the game to further refine the search.

## Features

*   **Automated Gameplay:** Opens the game website and automatically clicks "Higher" or "Lower" based on fetched scores.
*   **Jikan API Integration:** Fetches anime scores from the Jikan v4 API.
*   **Local Score Caching:** Stores fetched scores in a local SQLite database (`data/anime_scores.db`) to avoid redundant API calls and respect rate limits.
*   **Fuzzy Title Matching:** Uses `thefuzz` library to find the best match between the game's title and the API results, handling variations in naming (e.g., seasons, subtitles).
*   **Type Matching:** Uses the Type (TV/Movie) shown in the game to improve the accuracy of the API result selection.
*   **Session Statistics:** Tracks and logs the number of rounds played, the highest score achieved during the session, and the total runtime to `testsResults.txt`.
*   **Error Handling:** Includes basic error handling for browser interaction and API requests.

## Setup & Installation

1.  **Prerequisites:**
    *   Python 3.x installed.
    *   A compatible web browser (e.g., Chrome, Firefox) installed.
    *   The corresponding WebDriver for your browser (e.g., `chromedriver`, `geckodriver`).

2.  **Clone the Repository (if applicable):**
    ```bash
    git clone <your-repository-url>
    cd <repository-directory>
    ```

3.  **Install Dependencies:**
    *   It's highly recommended to use a virtual environment:
        ```bash
        python -m venv venv
        source venv/bin/activate # On Windows use `venv\Scripts\activate`
        ```
    *   Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **WebDriver Setup:**
    *   Download the WebDriver executable that matches your browser version.
    *   Place the WebDriver executable in the `drivers/` directory within the project folder (create the directory if it doesn't exist). The bot currently expects `chromedriver.exe` or `geckodriver.exe` in this location (see `handlers/browser_handler.py`). You might need to adjust the path in `browser_handler.py` if you place it elsewhere or use a different driver.

## Usage

1.  Ensure your WebDriver is correctly set up in the `drivers/` directory.
2.  Activate your virtual environment (if you created one).
3.  Run the main script from the root project directory:
    ```bash
    python main.py
    ```

The bot will open a browser window, navigate to the game, and start playing automatically. Progress and results will be printed to the console. Session results will be appended to `testsResults.txt`.

## Configuration

*   **`ROUND_DELAY`:** (in `main.py`) Sets the delay in seconds between rounds to allow the page to load. Default is 8 seconds.
*   **`DB_PATH`:** (in `handlers/database_handler.py`) Path to the SQLite database file. Default is `data/anime_scores.db`.
*   **`RESULTS_FILE`:** (in `main.py`) Path to the file where session results are logged. Default is `testsResults.txt`.
*   **`JIKAN_API_*` Constants:** (in `handlers/jikan_api.py`) Base URL, request delay, search limit, and similarity threshold for the Jikan API interaction.

## Project Structure

```
.
├── .gitignore
├── main.py                 # Main script to run the bot
├── requirements.txt        # Python dependencies
├── testsResults.txt        # Log file for test/run results
├── data/                   # Directory for data files
│   └── anime_scores.db     # SQLite database for caching scores (auto-generated)
├── drivers/                # Directory for WebDriver executables (add your driver here)
│   └── ...                 # (e.g., chromedriver.exe, geckodriver.exe)
├── handlers/               # Directory for modular handler scripts
│   ├── __init__.py
│   ├── browser_handler.py  # Handles Selenium browser setup and interaction
│   ├── database_handler.py # Handles SQLite database operations
│   ├── game_logic.py       # Handles game-specific element finding and actions
│   └── jikan_api.py        # Handles Jikan API communication and matching
└── venv/                   # Virtual environment (if used)
```

## Dependencies

*   `selenium`: For browser automation.
*   `requests`: For making HTTP requests to the Jikan API.
*   `thefuzz[speedup]`: For fuzzy string matching (requires `python-Levenshtein` for speedup).

See `requirements.txt` for specific versions. 