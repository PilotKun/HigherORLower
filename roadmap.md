# Anime Game Roadmap

1.  **Project Setup:**
    *   Create a project directory.
    *   Set up a Python virtual environment.
    *   Initialize a `requirements.txt` file for dependencies.
    *   Create the main script file (e.g., `main.py`) and potentially separate modules for different functionalities (e.g., `browser_handler.py`, `database_handler.py`, `jikan_api.py`, `game_logic.py`).

2.  **Browser Automation Setup:**
    *   Install Selenium and the appropriate WebDriver for Brave (ChromeDriver).
    *   Implement functions to:
        *   Initialize the Brave browser instance using Selenium.
        *   Navigate to the specified game URL.
        *   Close the browser gracefully.

3.  **Game Element Interaction:**
    *   Inspect the game's web page structure (HTML/CSS) to find stable selectors (like IDs, classes, or XPath) for:
        *   The elements displaying the two anime titles.
        *   The "Higher" and "Lower" buttons (or equivalent choice elements).
        *   The score display element.
    *   Implement functions using Selenium to:
        *   Extract the text content of the anime title elements.
        *   Click the choice buttons.
        *   Read the current score.

4.  **Database Implementation:**
    *   Choose a database: SQLite is a good choice as it's built into Python (`sqlite3`) and stores the database in a single file, making it simple to manage for this scope.
    *   Design the database schema: A simple table like `anime_scores` with columns `title` (TEXT, PRIMARY KEY) and `score` (REAL or FLOAT).
    *   Implement functions to:
        *   Connect to the SQLite database (create it if it doesn't exist).
        *   Query the database for a score given an anime title.
        *   Insert a new anime title and score into the database.
        *   Ensure data persistence (saving changes).

5.  **Jikan API Integration:**
    *   Install the `requests` library.
    *   Find the relevant Jikan API endpoint (likely the search endpoint: `https://api.jikan.moe/v4/anime`).
    *   Implement a function to:
        *   Take an anime title as input.
        *   Make a GET request to the Jikan API search endpoint.
        *   Parse the JSON response to find the most relevant match and extract its score (`score` field).
        *   Handle potential errors (e.g., anime not found, API rate limits, network issues). *Respect Jikan's rate limits.*

6.  **Core Game Logic:**
    *   Implement the main loop that orchestrates the game playing:
        *   Start the browser and navigate to the game.
        *   In a loop:
            *   Read the two anime titles from the page.
            *   For each title:
                *   Check the local database.
                *   If not found, call the Jikan API function to get the score.
                *   If found via API, store the title and score in the database.
            *   Compare the scores obtained for both titles.
            *   Click the "Higher" or "Lower" button based on the comparison.
            *   (Optional) Add a short delay to mimic human interaction and avoid overwhelming the game server or API.
            *   Read the updated score.
            *   Check for game over conditions or decide when to stop.

7.  **Error Handling and Refinement:**
    *   Add `try...except` blocks for robustness (e.g., network errors, elements not found on the page, API errors).
    *   Implement proper waits (e.g., `WebDriverWait`) in Selenium to ensure elements are loaded before interacting with them, rather than fixed `time.sleep()` calls.
    *   Handle edge cases (e.g., ties in scores, slight variations in titles between the game and MAL/Jikan).

## Tech Stack

*   **Language:** Python 3.x
*   **Browser Automation:** Selenium (`selenium` library)
*   **Web Driver:** ChromeDriver (compatible with Brave)
*   **Database:** SQLite (`sqlite3` standard library module)
*   **HTTP Requests:** `requests` library (for Jikan API)
*   **API:** Jikan API (v4)