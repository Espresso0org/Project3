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

        # Wait for the URL to load completely
        #WebDriverWait(driver, 10).until(EC.url_to_be(website_url))

        # Check if the div with class 'icon icon-generic' is present
        error_element = driver.find_elements(By.CSS_SELECTOR, 'div.icon.icon-generic')
        
    if len(error_element) > 0: 
        print("Proxy is bad")
        # Use the next proxy on the proxy list
        continue

    else:
        print("Good proxy")
        # Stay on the website for 10 seconds
        time.sleep(10)
        # Scroll to the end of the website
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Repeat the process 10 times with the good proxy
        for _ in range(10):
            # Do something on the website if needed
            # ...
            pass

    finally:
        # Quit the webdriver
        driver.quit()
