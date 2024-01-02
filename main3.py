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

stay = int(input("Enter time to stay on each page by minutes: "))
trynumb = int(input("Enter the number of tries per proxy: "))
user_agent_type = int(input("Enter 1 for mobile user agent, or 2 for desktop user agent: "))

chrome_driver_path = "chromedriver"

chrome_options = Options()
if user_agent_type == 1:
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36"
    )
if user_agent_type == 2:
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    )

proxy_list = []
with open("proxy.txt", "r", encoding="utf-8") as file:
    proxy_list = file.read().strip().split("\n")

driver = None

for proxy in proxy_list:
    print(f"Trying proxy: {proxy}")
    try:
        chrome_options.add_argument(f"--proxy-server=http://{proxy}")
        driver = webdriver.Chrome(
            executable_path=chrome_driver_path, options=chrome_options
        )
        driver.maximize_window()

        root = "https://www.google.com/"
        url = "https://google.com/search?q="

        with open("keyword.txt", "r", encoding="utf-8") as file:
            query = file.read().strip()

        query = urllib.parse.quote_plus(query)
        link = url + query
        driver.get(link)

        wait = WebDriverWait(driver, 15)
        wait.until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//*[@id="tads"]/div[1]/div/div[1]/div/div[1]/a')
            )
        )
        headings = driver.find_elements_by_css_selector('div.v5yQqb.jqWpsc')

        for _ in range(trynumb):
            for heading in headings:
                title = heading.find_elements_by_tag_name('h3')
                element = heading.find_element_by_css_selector('a')
                data_rw = re.search(
                    r'data-rw="([^"]+)"', element.get_attribute("outerHTML")
                )
                href = re.search(
                    r'href="([^"]+)"', element.get_attribute("outerHTML")
                )

                if data_rw and href:
                    data_rw_value = data_rw.group(1)
                    href_value = href.group(1)

                    data_rw_value = data_rw_value.replace("amp;", "")

                    print(data_rw_value)

                    # Open the URL
                    driver.execute_script(
                        '''window.open("{}","_blank");'''.format(href_value)
                    )
                    driver.switch_to.window(driver.window_handles[-1])

                    # Scroll to the end of the webpage
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);"
                    )

                    # Wait for a minute
                    time.sleep(60 * stay)

                    # Close the current tab and switch to the next URL
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        # Proxy worked, exit the loop
        break

    except:
        print("Proxy connection failed. Retrying with the next proxy...")

    finally:
        if driver is not None:
            driver.quit()

if driver:
    driver.quit()

print("Finished browsing with proxies.")
