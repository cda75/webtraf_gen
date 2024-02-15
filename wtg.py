# -*- coding: utf-8 -*-

import requests, ssl
from random import randint
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from os import path
from platform import system
from datetime import datetime
from urllib.parse import urlparse, urljoin
from cgw import get_default_gw 
import chromedriver_autoinstaller as chromedriver

requests.packages.urllib3.disable_warnings()

#URL list
workDir = path.dirname(path.abspath(__file__))
#drvExec = f'{workDir}//drv/chromedriver' if system() == 'Linux' else f'{workDir}\drv\chromedriver.exe' 
certDir = f'{workDir}/certs/'
urlFile = f'{workDir}/url/web_urls.txt'
logFile = f'{workDir}/logs/access.log'
urlFile2 = f'{workDir}/url/virus_urls.txt'

def logging(log_text, title=False):
    time = datetime.today().strftime('%d.%m.%Y %H:%M')
    if title:
        log_text = f'{log_text}'
    else:
        log_text = f'{time}\t{log_text}\n'
    with open(logFile, 'a') as f:
        print(log_text)
        f.write(log_text)


def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_urls_from_file(uf=urlFile):
    with open(uf, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_links_from_page(url, n=1, with_download=False):
    logging(f'\nExtracting {n} links from {url}\n', True)
    headers = {'User-Agent': 
               'Mozilla/5.0 Chrome/90.0.4430.85'}
    try:
        r = requests.get(url, headers=headers, verify=f'{workDir}/certs')
        html = r.text
        if (r.status_code != 200) or (len(html) == 0):
            logging(f'[{r.status_code}] Error during connection to {url}')
            return []
        bs = bs4(html, features='html.parser')
        hrefs = [href.get("href") for href in bs.find_all('a')] 
        if len(hrefs) == 0:
            logging(f'[-] Can not find any links on the page {url}')
            return []
        good_urls = [href for href in hrefs if (href) and ('http' in href)]
        rand_urls = []
        for i in range(n):
            rand_num = randint(0, len(good_urls)-1)
            rand_urls.append(good_urls[rand_num])
        return rand_urls
    except requests.exceptions.RequestException:
        logging(f'Error during connection to {url}')
        return []


def browser(driver, url):
    try:
        logging(f'Browsing {url}')
        driver.get(url)
    except BaseException:
        logging(f'[-] Error when accessng {url}')

    
def main():
    chromedriver.install()
    options = Options()
    proxy = {}
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    if get_default_gw() == '10.10.100.252':
        options.add_argument('--proxy-server=10.10.0.8:8090')
        proxy = {'http': '10.10.0.8:8090', 'https': '10.10.0.8:8090'}
        print('Using UserGate as a proxy-server')
    drv = webdriver.Chrome(options=options)
 
    urls = get_urls_from_file()
    for url in urls:
        links = get_links_from_page(url, 7)
        for link in links:
            browser(drv, link)
    drv.close()

    if get_default_gw() == '10.10.100.252':
        proxy = {'http': '10.10.0.8:8090', 'https': '10.10.0.8:8090'}
    else:
        proxy = {}
    logging('\nStarting virus checking section')
    urls = get_urls_from_file(urlFile2)
    for url in urls:
        try:
            r = requests.get(url, allow_redirects=True, proxies=proxy, verify=f'{workDir}/certs')
            f_name = url[:5]
            try:
                with open(f'{workDir}/tmp/{f_name}', 'wb') as f:
                    logging(f'Downloading file from {url}')
                    f.write(r.content)
            except AttributeError:
                logging('[-] Ошибка сохранения файла...')
        except BaseException:
            print('Error accessing file for download')


        
  
if __name__== "__main__":
  main()
