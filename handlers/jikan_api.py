# jikan_api.py - Handles interaction with the Jikan API

import requests
import time
import json # Added for parsing JSON response

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"
# Jikan API limits: 3 requests/second, 60 requests/minute
REQUEST_DELAY = 0.5 # Seconds to wait between requests

# TODO: Implement function to search anime and get score
# TODO: Add error handling and respect rate limits

def get_anime_score(title: str) -> float | None:
    """Fetches the score for a given anime title from the Jikan API.

    Searches for the title and returns the score of the first result.
    Note: This relies on the first result from the Jikan search being the correct
    match for the game's title. Discrepancies in naming (e.g., season numbers,
    subtitles) between the game and the API database can lead to incorrect matches.

    Args:
        title: The anime title to search for.

    Returns:
        The score as a float if found, otherwise None.
    """
    search_url = f"{JIKAN_API_BASE_URL}/anime"
    params = {"q": title, "limit": 1} # Search for the title, limit to 1 result

    try:
        # Wait briefly before making the request
        time.sleep(REQUEST_DELAY)

        response = requests.get(search_url, params=params)
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        if data and data.get("data"):
            first_result = data["data"][0]
            score = first_result.get("score")
            retrieved_title = first_result.get("title", "N/A")
            if score is not None:
                print(f"Jikan API: Found score {score} for title '{retrieved_title}' (searched for '{title}')")
                return float(score)
            else:
                print(f"Jikan API: Score not found for title '{retrieved_title}'.")
                return None
        else:
            print(f"Jikan API: No results found for title '{title}'.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Jikan API: Error during request for '{title}': {e}")
        return None
    except json.JSONDecodeError:
        print(f"Jikan API: Error decoding JSON response for '{title}'.")
        return None
    except IndexError:
        print(f"Jikan API: Unexpected response structure (IndexError) for '{title}'.")
        return None
    except Exception as e:
        print(f"Jikan API: An unexpected error occurred for '{title}': {e}")
        return None

# Example usage (for testing)
if __name__ == '__main__':
    test_title = "Naruto"
    score = get_anime_score(test_title)
    if score:
        print(f"Test: Score for {test_title} is {score}")
    else:
        print(f"Test: Could not retrieve score for {test_title}")

    test_title_nonexistent = "DefinitelyNotAnAnime12345"
    score = get_anime_score(test_title_nonexistent)
    if score:
        print(f"Test: Score for {test_title_nonexistent} is {score}")
    else:
        print(f"Test: Could not retrieve score for {test_title_nonexistent}") 