python
import requests

def check_proxy(proxy):
    try:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        response = requests.get('http://www.example.com', proxies=proxies, timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False

def main():
    with open('proxy.txt', 'r') as file:
        proxies = file.read().splitlines()

    for proxy in proxies:
        if check_proxy(proxy):
            print(f"Proxy {proxy} is working.")
        else:
            print(f"Proxy {proxy} is not working.")

if __name__ == '__main__':
    main()
