python
path_to_webdriver = 'chromedriver'

proxy_list = []
with open("proxy.txt", "r", encoding="utf-8") as file:
    proxy_list = file.read().strip().split("\n")

with open("url.txt", "r", encoding="utf-8") as file:
    urls = file.read().strip().split("\n")

for website_url in urls:
    print(f"Opening URL: {website_url}")
    for proxy in proxy_list:
        print(f"Trying proxy: {proxy}")
        try:
            chrome_options = Options()
            chrome_options.add_argument(f"--proxy-server=http://{proxy}")

            driver = webdriver.Chrome(executable_path=path_to_webdriver, options=chrome_options)
            driver.get(website_url)

            error_element = driver.find_element(By.CSS_SELECTOR, 'div.icon.icon-generic')

            print("Good proxy")
            time.sleep(5)
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        except NoSuchElementException:
            print("Proxy is bad")
            driver.quit()
            continue

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            driver.quit()
            continue

        driver.quit()
        break  # Break out of the proxy loop if a successful proxy is found
