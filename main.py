import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_on_google():
    # Get user input for search term
    search_terms = input("Enter the search term: ").split()

    # Get user input for time to stay on each website
    stay_time = int(input("Enter the time to stay on each website (in minutes): "))

    # Get user input for user agent type
    user_agent_type = int(input("Enter 1 for mobile user agent, or 2 for desktop user agent: "))

    # Create Chrome options and set the User-Agent based on the user input
    chrome_options = Options()
    if user_agent_type == 1:
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36")
    elif user_agent_type == 2:
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")

    # Set the path to the ChromeDriver executable
    chromedriver_path = '/path/to/chromedriver'  # Replace with the actual path to chromedriver

    # Create a new instance of the Chrome driver with the specified path and options
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)

    # Open Google Chrome
    driver.get("https://www.google.com/")

    # Find the search input element and enter the search terms
    search_input = driver.find_element_by_name("q")
    search_input.send_keys(" ".join(search_terms))

    # Press Enter to perform the search
    search_input.send_keys(Keys.RETURN)

    # Wait for the search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))

    # Find the sponsored links
    sponsored_links = driver.find_elements(By.CSS_SELECTOR, "div[data-hveid]")

    # Iterate over each sponsored link
    for link in sponsored_links:
        # Click on the sponsored link
        link.click()

        # Wait for the website to load
        time.sleep(5)  # Adjust the sleep time as needed

        # Scroll down to the end of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Adjust the sleep time as needed

        # Stay on the website for the specified time
        time.sleep(stay_time * 60)  # Convert minutes to seconds

        # Go back to the search results page
        driver.back()

        # Wait for the search results to load again
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.g")))

    # Rest of the code...

# Example usage:
search_on_google()

