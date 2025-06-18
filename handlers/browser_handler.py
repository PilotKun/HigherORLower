# browser_handler.py - Manages Selenium browser interactions

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

# TODO: Specify path to Brave browser executable and ChromeDriver
BRAVE_PATH = "/usr/bin/brave-browser"
CHROMEDRIVER_PATH = "/usr/bin/chromedriver"  # Linux chromedriver path

# TODO: Implement functions for initialization, navigation, element interaction, and closing

def initialize_driver():
    """Initializes and returns a Selenium WebDriver instance for Brave."""
    options = Options()
    options.binary_location = BRAVE_PATH
    
    # Disable proxy and add connection options
    options.add_argument('--no-proxy-server')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--disable-web-security')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--start-maximized")
    options.add_experimental_option('excludeSwitches', ['enable-logging']) # Suppress unnecessary logs

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)

    try:
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)  # Set page load timeout to 30 seconds
        print("Browser initialized successfully.")
        return driver
    except Exception as e:
        print(f"Error initializing browser: {e}")
        return None

def navigate_to_url(driver, url: str):
    """Navigates the browser to the specified URL."""
    if driver:
        try:
            driver.set_page_load_timeout(30)  # Set timeout for this navigation
            driver.get(url)
            print(f"Navigated to: {url}")
        except Exception as e:
            print(f"Error navigating to {url}: {e}")
            # Try refreshing the page once if navigation fails
            try:
                print("Attempting to refresh the page...")
                driver.refresh()
                print("Page refreshed successfully.")
            except Exception as refresh_error:
                print(f"Failed to refresh page: {refresh_error}")
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