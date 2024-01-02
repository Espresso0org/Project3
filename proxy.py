python
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Read proxy list from file
with open('proxy.txt', 'r') as file:
    proxies = file.read().splitlines()

# Function to check if a proxy is working
def check_proxy(proxy):
    try:
        response = requests.get('https://www.example.com', proxies={'http': proxy}, timeout=5)
        return response.status_code == 200
    except:
        return False

# Function to open URL with proxy using Selenium
def open_url_with_proxy(url, proxy):
    chrome_options = Options()
    chrome_options.add_argument('--proxy-server={}'.format(proxy))
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    # Check if the desired element is present
    if len(driver.find_elements_by_css_selector('div.icon.icon-generic')) > 0:
        driver.quit()
        return False
    else:
        return True

# Iterate through the proxy list
for proxy in proxies:
    if check_proxy(proxy):
        if open_url_with_proxy('https://www.example.com', proxy):
            print('Successfully opened URL with proxy:', proxy)
            break
        else:
            print('Failed to open URL with proxy:', proxy)
    else:
        print('Proxy not working:', proxy)
