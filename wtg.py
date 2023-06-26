# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 11:36:28 2023
Web Traffic Generator
@author: Dimka
"""
import requests
from random import randint
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from os import path
from platform import system
from datetime import datetime


#URL list
workDir = path.dirname(path.abspath(__file__))
drvExec = f'{workDir}/chromedriver' if system() == 'Linux' else f'{workDir}\chromedriver.exe' 
urlFile = f'{workDir}/web_urls.txt'
logFile = f'{workDir}/access.log'
urlFile2 = f'{workDir}/virus_urls.txt'

def logging(log_text, title=False):
    time = datetime.today().strftime('%d.%m.%Y %H:%M')
    if title:
        log_text = f'{log_text}'
    else:
        log_text = f'{time}\t{log_text}'
    with open(logFile, 'a') as f:
        print(log_text)
        f.write(log_text)


def get_urls_from_file(uf=urlFile):
    with open(uf, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_links_from_page(url, n=1, with_download=False):
    logging(f'Extracting {n} links from {url}', True)
    headers = {'User-Agent': 
               'Mozilla/5.0 Chrome/90.0.4430.85'}
    try:
        r = requests.get(url, headers=headers)
        html = r.text
        if (r.status_code == 200) and (len(html)) > 0:
            bs = bs4(html, features='html.parser')
            hrefs = [href.get("href") for href in bs.find_all('a')] 
            if len(hrefs) == 0:
                logging(f'[{r.status_code}] Error extracting links from {url}')
                return []
            rand_urls = []
            count = 0
            while (count < n) and (len(hrefs) > n):
                rand_num = randint(0, len(hrefs)-1)
                rand_href = hrefs[rand_num]
                if rand_href and ('http' in rand_href):
                    rand_urls.append(rand_href)
                    count += 1
                    logging(rand_href)
            return rand_urls
        else:
            logging(f'[{r.status_code}]:[{len(html)}] Error accessing {url}')
            return []
    except requests.exceptions.RequestException as e:
        print(e)
        logging(f'Error during connection to {url}')


def browser(url):
    options = Options()
    service = Service(executable_path = drvExec)
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
    except BaseException:
        logging(f'[-] Error when accessng {url}')
    finally:
        driver.close()

    
def main():
    
    urls = get_urls_from_file()
    for url in urls:
        links = get_links_from_page(url,5)
        for link in links:
            browser(link)
    logging('Finished ....\n') 

    urls = get_urls_from_file(urlFile2)
    for url in urls:
        r = requests.get(url, allow_redirects=True)
        logging(f'Downloading: {url}')
        f_name = url[:5]
        try:
            with open(f'{workDir}/tmp/{f_name}', 'wb') as f:
                f.write(r.content)
        except AttributeError:
            logging('[-] Ошибка сохранения файла...')


        
  
if __name__== "__main__":
  main()
