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

        # Check if the target element 'div.icon.icon-generic' is present
        is_element_present = EC.presence_of_element_located((By.CSS_SELECTOR, "div.icon.icon-generic"))(driver)

        if is_element_present:
            print("Proxy failed: Target element is present.")
        else:
            print("Proxy successful: Target element not found.")
            break  # Break the loop if the proxy is successful

        # Quit the webdriver
        driver.quit()

    except:
        print(f"Proxy failed: {proxy}")
