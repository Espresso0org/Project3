
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Set the path to the ChromeDriver executable
chrome_driver_path = "path/to/chromedriver"

chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Mobile Safari/537.36")

# Create a new instance of ChromeDriver
driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)

# Maximize the browser window
driver.maximize_window()

# Navigate to Google.com
driver.get("https://www.google.com")

# Find the search input field
search_input = driver.find_element(By.NAME, "q")

# Enter the keyword you want to search
keyword = "your keyword"
search_input.send_keys(keyword)

# Press Enter to perform the search
search_input.send_keys(Keys.ENTER)

# Wait until the search results are loaded
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.ID, "search")))

# Find all the search result elements
search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")

# Iterate over the search results and extract the data between href=" and data-ae=
for search_result in search_results:
    # Get the outer HTML of the search result element
    outer_html = search_result.get_attribute("outerHTML")

    # Extract the data between href=" and data-ae=
    start_index = outer_html.find('href="') + len('href="')
    end_index = outer_html.find('data-ae=', start_index)
    extracted_data = outer_html[start_index:end_index]

    # Print the extracted data
    print(extracted_data)

# Close the browser
driver.quit()

input("Press Enter to exit...")
)





