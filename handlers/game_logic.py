# game_logic.py - Contains the core game playing logic

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time # Import time for delays if needed later

# XPaths provided by user (Note: Absolute XPaths can be brittle)
PLAY_BUTTON_XPATH = '//*[@id="start-game-anime-all"]'
LEFT_TITLE_XPATH = "/html/body/section[2]/div[1]/button[2]/section/h2"
RIGHT_TITLE_XPATH = "/html/body/section[2]/div[2]/button[1]/section/h2"
LEFT_TYPE_XPATH = "/html/body/section[2]/div[1]/button[2]/section/h4"
RIGHT_TYPE_XPATH = "/html/body/section[2]/div[2]/button[1]/section/h4"
LEFT_CHOICE_XPATH = "/html/body/section[2]/div[1]/button[2]"
RIGHT_CHOICE_XPATH = "/html/body/section[2]/div[2]/button[1]"
SCORE_DISPLAY_XPATH = "/html/body/section[2]/div[4]" # Contains "Score: X High score: Y"

WAIT_TIMEOUT = 10 # Increased timeout for better reliability

def _find_element(driver: WebDriver, by: str, value: str) -> WebElement | None:
    """Helper function to find an element with explicit wait."""
    try:
        element = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((by, value))
        )
        # Optional: Add wait for visibility/interactability if needed
        # element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        #    EC.element_to_be_clickable((by, value))
        #)
        return element
    except TimeoutException:
        print(f"Error: Element not found or timed out ({by}={value})")
        return None
    except Exception as e:
        print(f"Error finding element ({by}={value}): {e}")
        return None

def click_play_button(driver: WebDriver):
    """Clicks the initial play button to start the game."""
    print("Attempting to click the play button...")
    play_button = _find_element(driver, By.XPATH, PLAY_BUTTON_XPATH)
    if play_button:
        try:
            play_button.click()
            print("Play button clicked.")
            # Add a small delay for the game state to update after clicking play
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.presence_of_element_located((By.XPATH, LEFT_TITLE_XPATH))
            )
            print("Game elements loaded after play.")
        except Exception as e:
            print(f"Error clicking play button: {e}")
    else:
        print("Play button not found.")


def get_anime_titles(driver: WebDriver) -> tuple[str | None, str | None, str | None, str | None]:
    """Gets the text of the left/right anime titles and their types (e.g., TV, Movie)."""
    left_title_element = _find_element(driver, By.XPATH, LEFT_TITLE_XPATH)
    right_title_element = _find_element(driver, By.XPATH, RIGHT_TITLE_XPATH)
    left_type_element = _find_element(driver, By.XPATH, LEFT_TYPE_XPATH)
    right_type_element = _find_element(driver, By.XPATH, RIGHT_TYPE_XPATH)

    left_title = left_title_element.text.strip() if left_title_element else None
    right_title = right_title_element.text.strip() if right_title_element else None
    left_type = left_type_element.text.strip().upper() if left_type_element and left_type_element.text else None
    right_type = right_type_element.text.strip().upper() if right_type_element and right_type_element.text else None

    if not left_title or not right_title:
        print(f"Warning: Could not retrieve one or both titles (Left: {left_title}, Right: {right_title})")
    if not left_type or not right_type:
        print(f"Warning: Could not retrieve one or both types (Left Type: {left_type}, Right Type: {right_type})")

    return left_title, left_type, right_title, right_type

def get_current_score(driver: WebDriver) -> int | None:
    """Gets the current score from the score display element."""
    score_element = _find_element(driver, By.XPATH, SCORE_DISPLAY_XPATH)
    if score_element:
        try:
            # Example text: "Score: 5 High score: 14"
            # We need to parse out the current score.
            score_text = score_element.text
            score_part = score_text.split("High score:")[0] # Get the "Score: X" part
            score_value = int(score_part.replace("Score:", "").strip())
            return score_value
        except (ValueError, IndexError, AttributeError) as e:
            print(f"Error parsing score from text '{score_element.text}': {e}")
            return None
        except Exception as e:
            print(f"Unexpected error getting score: {e}")
            return None
    else:
        print("Score display element not found.")
        return None

def make_choice(driver: WebDriver, choice: str):
    """Clicks the button corresponding to the chosen anime ('left' or 'right')."""
    xpath = LEFT_CHOICE_XPATH if choice == "left" else RIGHT_CHOICE_XPATH
    button_element = _find_element(driver, By.XPATH, xpath)

    if button_element:
        try:
            print(f"Clicking {choice} choice.")
            # Scroll into view if necessary, although clicking often handles this
            # driver.execute_script("arguments[0].scrollIntoView(true);", button_element)
            # time.sleep(0.2) # Small delay before click if needed
            button_element.click()
        except Exception as e:
            print(f"Error clicking {choice} choice ({xpath}): {e}")
    else:
        print(f"{choice.capitalize()} choice button not found.")

# TODO: Implement game state reading, decision making, and action execution
pass 