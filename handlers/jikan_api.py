# jikan_api.py - Handles interaction with the Jikan API

import requests
import time
import json # Added for parsing JSON response
from thefuzz import process, fuzz # Import for fuzzy matching

JIKAN_API_BASE_URL = "https://api.jikan.moe/v4"
# Jikan API limits: 3 requests/second, 60 requests/minute
REQUEST_DELAY = 0.5 # Seconds to wait between requests
SEARCH_LIMIT = 10 # Number of search results to fetch from API
SIMILARITY_THRESHOLD = 75 # Minimum similarity score (0-100) to consider a match

# TODO: Implement function to search anime and get score
# TODO: Add error handling and respect rate limits

def get_anime_score(title: str, expected_type: str | None = None) -> float | None:
    """Fetches the score for a given anime title from the Jikan API.

    Searches for the title, fetches multiple results, and selects the best match
    based on title similarity and optionally, the expected anime type (TV, Movie, etc.).

    Args:
        title: The anime title to search for (from the game).
        expected_type: The expected type (e.g., "TV", "MOVIE") from the game, if available.

    Returns:
        The score as a float if a suitable match is found, otherwise None.
    """
    search_url = f"{JIKAN_API_BASE_URL}/anime"
    params = {"q": title, "limit": SEARCH_LIMIT} # Fetch multiple results

    print(f"Jikan API: Searching for '{title}' (Expected type: {expected_type or 'Any'})...")

    try:
        time.sleep(REQUEST_DELAY)
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data or not data.get("data"):
            print(f"Jikan API: No results found for title '{title}'.")
            return None

        results = data["data"]
        print(f"Jikan API: Received {len(results)} results for '{title}'.")

        candidates = []
        for result in results:
            api_title = result.get("title")
            api_score = result.get("score")
            api_type = result.get("type") # e.g., "TV", "Movie", "OVA"

            if not api_title or api_score is None:
                continue # Skip results without a title or score

            # Calculate title similarity
            similarity = fuzz.ratio(title.lower(), api_title.lower())

            # Basic type matching (convert game type if needed, API types are usually uppercase)
            type_match = False
            if expected_type:
                if api_type and api_type.upper() == expected_type.upper():
                    type_match = True
            else:
                type_match = True # No expected type, so any type is okay initially

            # Store candidate info: (api_score, similarity, type_match_bonus, api_title)
            # We'll use this tuple for sorting later.
            # Add a bonus score for matching type to prioritize them.
            type_bonus = 100 if type_match else 0 # Add significant bonus for type match

            if similarity >= SIMILARITY_THRESHOLD:
                candidates.append({
                    "score": float(api_score),
                    "similarity": similarity,
                    "type_match": type_match,
                    "api_title": api_title,
                    "api_type": api_type
                })
                # print(f"  - Candidate: '{api_title}' (Type: {api_type}, Score: {api_score}, Sim: {similarity}, TypeMatch: {type_match})")


        if not candidates:
            print(f"Jikan API: No results for '{title}' met the similarity threshold ({SIMILARITY_THRESHOLD}).")
            return None

        # Sort candidates: Prioritize type match, then highest similarity
        # If types match, higher similarity is better.
        # If types don't match, we still consider them but rank them lower.
        candidates.sort(key=lambda x: (x["type_match"], x["similarity"]), reverse=True)

        best_match = candidates[0]

        print(f"Jikan API: Best match for '{title}' (Expected: {expected_type or 'Any'}) -> '{best_match['api_title']}' (Type: {best_match['api_type']}, Score: {best_match['score']}, Similarity: {best_match['similarity']})")
        return best_match["score"]


    except requests.exceptions.RequestException as e:
        print(f"Jikan API: Error during request for '{title}': {e}")
        return None
    except json.JSONDecodeError:
        print(f"Jikan API: Error decoding JSON response for '{title}'.")
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