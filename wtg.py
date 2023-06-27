# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 11:36:28 2023
Web Traffic Generator
@author: Dimka
"""
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


requests.packages.urllib3.disable_warnings()


#URL list
workDir = path.dirname(path.abspath(__file__))
drvExec = f'{workDir}//drv/chromedriver' if system() == 'Linux' else f'{workDir}\drv\chromedriver.exe' 
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
        r = requests.get(url, headers=headers, verify=False)
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


def browser(url):
    options = Options()
    service = Service(executable_path = drvExec)
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        logging(f'Browsing {url}')
        driver.get(url)
    except BaseException:
        logging(f'[-] Error when accessng {url}')
    finally:
        driver.close()

    
def main():
    
    urls = get_urls_from_file()
    for url in urls:
        links = get_links_from_page(url,4)
        for link in links:
            browser(link)

    logging('Starting virus checking section')
    urls = get_urls_from_file(urlFile2)
    for url in urls:
        try:
            r = requests.get(url, allow_redirects=True)
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
