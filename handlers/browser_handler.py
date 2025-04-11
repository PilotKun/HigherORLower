# browser_handler.py - Manages Selenium browser interactions

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# TODO: Specify path to Brave browser executable and ChromeDriver
BRAVE_PATH = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
CHROMEDRIVER_PATH = "C:\\Users\\DELL\\Coding\\HigherORLower\\drivers\\chromedriver.exe"

# TODO: Implement functions for initialization, navigation, element interaction, and closing

def initialize_driver():
    """Initializes and returns a Selenium WebDriver instance for Brave."""
    options = Options()
    options.binary_location = BRAVE_PATH
    # options.add_argument('--headless') # Uncomment to run without opening a browser window
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Suppress unnecessary logs

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("Browser initialized successfully.")
        return driver
    except Exception as e:
        print(f"Error initializing browser: {e}")
        # Consider more specific error handling or raising the exception
        return None

def navigate_to_url(driver, url: str):
    """Navigates the browser to the specified URL."""
    if driver:
        try:
            driver.get(url)
            print(f"Navigated to: {url}")
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
    else:
        print("Driver not initialized, cannot navigate.")

def close_driver(driver):
    """Closes the WebDriver instance."""
    if driver:
        try:
            driver.quit()
            print("Browser closed.")
        except Exception as e:
            print(f"Error closing browser: {e}") 