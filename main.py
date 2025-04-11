# main.py - Main script to run the anime game bot

import handlers.browser_handler as browser_handler
import handlers.database_handler as database_handler
import handlers.game_logic as game_logic
import handlers.jikan_api as jikan_api
import time
import datetime # Added for timestamping and duration
import os       # Added for file path operations

GAME_URL = "https://www.higherorlowergame.com/anime/score/"
# MAX_ROUNDS = 10 # No longer needed, play until game over
ROUND_DELAY = 8 # Seconds to wait between rounds for page to update
RESULTS_FILE = "testsResults.txt"

def get_or_fetch_score(title: str) -> float | None:
    """Gets score from DB, fetches from API if not found, and saves if fetched."""
    if not title:
        print("Error: Received empty title.")
        return None

    # Check database first
    score = database_handler.get_score_from_db(title)
    if score is not None:
        print(f"DEBUG Main: Using score {score} for '{title}' from DB.")
        return score

    # If not in DB, fetch from Jikan API
    print(f"DEBUG Main: '{title}' not in DB, fetching from Jikan API...")
    score = jikan_api.get_anime_score(title)

    # If successfully fetched, save to DB for future use
    # Note: We save using the *original* title from the game, even if the
    # Jikan API found a score for a slightly different title string.
    # This ensures our DB is keyed by the exact titles encountered in the game.
    if score is not None:
        database_handler.save_score_to_db(title, score)
        print(f"Saved '{title}' with score {score} to DB.")
        return score
    else:
        print(f"Could not fetch score for '{title}' from API.")
        return None

def main():
    start_time = datetime.datetime.now() # Record start time
    print(f"Starting Anime Game Bot at {start_time.strftime('%Y-%m-%d %H:%M:%S')}...")
    database_handler.setup_database()
    driver = browser_handler.initialize_driver()

    if not driver:
        print("Failed to initialize browser. Exiting.")
        return

    high_score_session = 0
    rounds_played = 0

    try:
        browser_handler.navigate_to_url(driver, GAME_URL)
        time.sleep(2) # Wait a bit for page elements to potentially settle

        game_logic.click_play_button(driver)
        time.sleep(ROUND_DELAY) # Wait for the first round to load

        while True: # Loop indefinitely until game over
            rounds_played += 1
            print(f"\n--- Round {rounds_played} ---")

            # Check if game elements are still present (basic game over check)
            left_title_element = game_logic._find_element(driver, game_logic.By.XPATH, game_logic.LEFT_TITLE_XPATH)
            right_title_element = game_logic._find_element(driver, game_logic.By.XPATH, game_logic.RIGHT_TITLE_XPATH)
            if not left_title_element or not right_title_element:
                print("Game title elements not found. Assuming game over.")
                break # Exit the loop

            left_title, right_title = game_logic.get_anime_titles(driver)
            print(f"Left: {left_title} | Right: {right_title}")

            if not left_title or not right_title:
                print("Could not read titles. Attempting to wait and retry or stopping.")
                # You might want more robust handling here, e.g., wait longer, check score
                if game_logic.get_current_score(driver) is None and \
                   game_logic._find_element(driver, game_logic.By.XPATH, game_logic.PLAY_BUTTON_XPATH):
                   print("Titles missing and play button found. Assuming game over.")
                   break
                else:
                   print("Continuing after short delay, but titles were missing.")
                   time.sleep(ROUND_DELAY)
                   continue # Try next loop iteration

            left_score = get_or_fetch_score(left_title)
            right_score = get_or_fetch_score(right_title)

            if left_score is None or right_score is None:
                print("Could not determine scores for both titles.")
                print("Assuming game over due to missing score data.")
                break # Exit loop if scores can't be found

            print(f"Scores -> Left: {left_score}, Right: {right_score}")

            # Determine which has the higher score and click
            if right_score >= left_score:
                print("Choosing RIGHT")
                game_logic.make_choice(driver, 'right')
            else:
                print("Choosing LEFT")
                game_logic.make_choice(driver, 'left')

            print(f"Waiting {ROUND_DELAY} seconds for next round...")
            time.sleep(ROUND_DELAY)

            # Get and print the current score after the choice
            current_score = game_logic.get_current_score(driver)
            if current_score is not None:
                print(f"Current score: {current_score}")
                high_score_session = max(high_score_session, current_score)
                print(f"Highest score this session: {high_score_session}")
            else:
                print("Could not read current score. Checking for game over condition...")
                # Check if the play button reappeared, indicating game over
                time.sleep(1) # Short wait for elements to potentially update after score read fails
                if game_logic._find_element(driver, game_logic.By.XPATH, game_logic.PLAY_BUTTON_XPATH):
                    print("Play button detected after score read failure. Game over.")
                    break # Exit the loop
                else:
                    print("Score read failed, but play button not found. Potential issue or brief transition.")
                    # Decide whether to break or continue cautiously
                    # For now, let's break to be safe
                    print("Stopping due to score read failure.")
                    break

    except Exception as e:
        print(f"\nAn unexpected error occurred in the main loop: {e}")
    finally:
        end_time = datetime.datetime.now() # Record end time
        duration = end_time - start_time
        duration_str = str(duration).split('.')[0] # Format duration nicely (HH:MM:SS)

        final_rounds = rounds_played - 1 if rounds_played > 0 else 0
        print(f"\nGame finished after {final_rounds} successful choices.")
        print(f"Highest score achieved this session: {high_score_session}")
        print(f"Total runtime: {duration_str}")

        # Log results to file
        try:
            # Determine the next test number
            test_num = 1
            if os.path.exists(RESULTS_FILE):
                with open(RESULTS_FILE, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        if last_line.startswith("TEST"):
                            try:
                                test_num = int(last_line.split(':')[0].split(' ')[1]) + 1
                            except (IndexError, ValueError):
                                print(f"Warning: Could not parse last test number from '{RESULTS_FILE}'. Starting from 1.")
                                test_num = len(lines) + 1 # Fallback if parsing fails

            # Format the result string
            result_line = f"TEST {test_num}: played {final_rounds} rounds, highscore {high_score_session}, ran for {duration_str}\n"

            # Append to the file
            with open(RESULTS_FILE, 'a') as f:
                f.write(result_line)
            print(f"Results logged to {RESULTS_FILE}")

        except IOError as e:
            print(f"Error writing results to {RESULTS_FILE}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred during results logging: {e}")

        # Close browser gracefully
        print("\nClosing browser...")
        browser_handler.close_driver(driver)

    print("\nBot finished.")

if __name__ == "__main__":
    main() 