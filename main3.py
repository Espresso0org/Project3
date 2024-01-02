python
import urllib
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re

# Replace 'website_url' with the actual URL you want to visit
website_url = 'https://www.google.com/aclk?sa=l&ai=DChcSEwiKiNH5pr6DAxVxLtQBHU3DCSUYABAAGgJvYQ&ae=2&gclid=EAIaIQobChMIiojR-aa-gwMVcS7UAR1NwwklEAAYASAAEgLe1_D_BwE&sig=AOD64_1qVlEybeHyYSdBB2AuVn--FxTNzQ&q&adurl'

# Replace 'path_to_webdriver' with the actual path to your webdriver executable
path_to_webdriver = 'chromedriver'

proxy_list = []
with open("proxy.txt", "r", encoding="utf-8") as file:
    proxy_list = file.read().strip().split("\n")

for proxy in proxy_list:
    print(f"Trying proxy: {proxy}")
    try:
        chrome_options = Options()
        chrome_options.add_argument(f"--proxy-server=http://{proxy}")
        driver = webdriver.Chrome(executable_path=path_to_webdriver, options=chrome_options)
        driver.get(website_url)

        # Wait for 10 seconds
        time.sleep(10)

        # Check if the element 'div.icon.icon-generic' is present on the page
        error_element = driver.find_elements(By.CSS_SELECTOR, 'div.icon.icon-generic')
        if len(error_element) > 0:
            print(f"Connection unsuccessful using proxy: {proxy}")
            # Continue to the next proxy in case of failure
            continue

        # Do something on the website if needed

        # If the above operations were successful, break out of the loop
        break

    except Exception as e:
        print(f"Failed to connect using proxy: {proxy}")
        print(f"Error message: {str(e)}")
        # Continue to the next proxy in case of failure

    finally:
        # Quit the webdriver
        driver.quit()
