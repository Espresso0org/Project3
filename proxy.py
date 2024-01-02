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

stay = int(input("Enter time to stay on each page in minutes: "))
trynumb = input("Enter the number of tries per proxy: ")
user_agent_type = int(input("Enter 1 for mobile user agent or 2 for desktop user agent: "))

chrome_driver_path = "chromedriver"

chrome_options = Options()
if user_agent_type == 1:
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36")
if user_agent_type == 2:
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36")

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
driver.maximize_window()

root = "https://www.google.com/"
url = "https://google.com/search?q="

with open("keyword.txt", "r", encoding="utf-8") as file:
    query = file.read().strip()

query = urllib.parse.quote_plus(query)
link = url + query
driver.get(link)

wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tads"]/div[1]/div/div[1]/div/div[1]/a')))
headings = driver.find_elements_by_css_selector('div.v5yQqb.jqWpsc')

# Open the file in write mode and truncate it to remove existing content
with open("url.txt", "w", encoding="utf-8") as file:
    file.truncate()

    for heading in headings:
        title = heading.find_elements_by_tag_name('h3')
        element = heading.find_element_by_css_selector('a')
        data_rw = re.search(r'data-rw="([^"]+)"', element.get_attribute("outerHTML"))
        href = re.search(r'href="([^"]+)"', element.get_attribute("outerHTML"))

        if data_rw and href:
            data_rw_value = data_rw.group(1)
            href_value = href.group(1)

            data_rw_value = data_rw_value.replace("amp;", "")

            # Write the data_rw_value to the file
            file.write(data_rw_value + "\n")
            print("URLs grabbed successfully")

driver.quit()

# Replace 'path_to_webdriver' with the actual path to your webdriver executable
path_to_webdriver = 'chromedriver'

proxy_list = []
with open("proxy.txt", "r", encoding="utf-8") as file:
    proxy_list = file.read().strip().split("\n")

with open("url.txt", "r", encoding="utf-8") as file:
    urls = file.read().strip().split("\n")

for proxy in proxy_list:
    print(f"Trying proxy: {proxy}")
    try:
        chrome_options = Options()
        chrome_options.add_argument(f"--proxy-server=http://{proxy}")
        
        for website_url in urls:
            print(f"Opening URL: {website_url}")
            driver = webdriver.Chrome(executable_path=path_to_webdriver, options=chrome_options)
            driver.get(website_url)

            error_element = driver.find_elements(By.CSS_SELECTOR, 'div.icon.icon-generic')

            if len(error_element) > 0: 
                print("Proxy is bad")
                driver.quit()
                continue
            else:
                print("Good proxy")
                time.sleep(60*stay)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                for _ in range(trynumb):
                    # Do something on the website if needed
                    # ...
                    pass

            driver.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.quit()
        continue
