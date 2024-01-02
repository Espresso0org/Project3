python
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
                time.sleep(5)
                # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                for _ in range(5):
                    print(f"Opening URL: {website_url} (Attempt {_ + 1} of 5)")
                    time.sleep(5)
                    driver.quit()
                    driver = webdriver.Chrome(executable_path=path_to_webdriver, options=chrome_options)
                    driver.get(website_url)
                
            driver.quit()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.quit()
        continue
