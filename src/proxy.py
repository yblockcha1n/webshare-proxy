import requests
import random
import configparser
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.ini')
config.read(config_path)

API_KEY = config['API']['API_KEY']
BASE_URL = "https://proxy.webshare.io/api/v2"

def get_proxy_list():
    url = f"{BASE_URL}/proxy/list/"
    headers = {"Authorization": f"Token {API_KEY}"}
    params = {"mode": "direct"}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"エラー: {response.status_code}")
        print(f"レスポンス: {response.text}")
        return None

def use_proxy_with_selenium(proxy):
    print(f"使用するプロキシ: {proxy['proxy_address']}:{proxy['port']}")
    
    chrome_options = Options()
    chrome_options.add_argument(f'--proxy-server={proxy["proxy_address"]}:{proxy["port"]}')
    #chrome_options.add_argument('--headless')

    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get("https://httpbin.org/ip")
        wait = WebDriverWait(driver, 10)
        ip_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "pre")))
        ip_info = ip_element.text
        print(f"スクレイピング成功: {ip_info}")
    except Exception as e:
        print(f"スクレイピングエラー: {e}")
    finally:
        driver.quit()

def main():
    proxy_list = get_proxy_list()
    if proxy_list and 'results' in proxy_list:
        print(f"{len(proxy_list['results'])}個のプロキシが見つかりました")
        
        print("見つかったプロキシアドレス:")
        for proxy in proxy_list['results']:
            print(f"{proxy['proxy_address']}:{proxy['port']}")

        if proxy_list['results']:
            random_proxy = random.choice(proxy_list['results'])
            use_proxy_with_selenium(random_proxy)
        else:
            print("利用可能なプロキシがありません")
    else:
        print("プロキシリストの取得に失敗しました")

if __name__ == "__main__":
    main()