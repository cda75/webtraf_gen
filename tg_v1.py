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
import re

#URL list
workDir = path.dirname(path.abspath(__file__))
drvExec = f'{workDir}/chromedriver' if system() == 'Linux' else f'{workDir}\chromedriver.exe' 
urlFile = f'{workDir}/urls.txt'
logFile = f'{workDir}/tg.log'
urlFile2 = f'{workDir}/download_urls.txt'

def logging(log_text):
    time = datetime.today().strftime('%d.%m.%Y %H:%M')
    with open(logFile, 'a') as f:
        f.write(f'{time}\t{log_text}\n')


def get_urls_from_file(uf=urlFile):
    logging('Starting new round...')
    with open(uf, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_links_from_page(url, n=1, with_download=False):
    headers = {'User-Agent': 
               'Mozilla/5.0 Chrome/90.0.4430.85'}
    r = requests.get(url, headers=headers)
    html = r.text
    if (r.status_code == 200) and (len(html)) > 0:
        bs = bs4(html, features='html.parser')
        hrefs = [href.get("href") for href in bs.find_all('a')] 
        rand_urls = []
        count = 0
        while (count < n) and (len(hrefs) > n):
            rand_num = randint(0,len(hrefs)-1)
            rand_href = hrefs[rand_num]
            try:
                if 'http' in rand_href:
                    rand_urls.append(rand_href)
                    count += 1
                    logging(rand_href)
            except BaseException():
                print('Error retriving random links from page', url)
        return rand_urls


def browser(url):
    options = Options()
    service = Service(executable_path = drvExec)
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        print(driver.current_url, driver.title)
    except BaseException:
        print(f'Error when accessng {url}')
    finally:
        driver.close()

'''    
def is_downloadable(url):
    h = requests.head(url, allow_redirects=True)
    header = h.headers
    content_type = header.get('content-type')
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True 


def get_filename_from_url(content):
    if not content:
        return None
    fname = re.findall('filename=(.+)', content)
    if len(fname) == 0:
        return None
    return fname[0]
'''
    
def main():
    '''
    urls = get_urls_from_file()
    for url in urls:
        links = get_links_from_page(url)
        for link in links:
            browser(link)
    logging('Finished ....\n') 
    '''
    urls = get_urls_from_file(urlFile2)
    for url in urls:
        r = requests.get(url, allow_redirects=True)
        print(f'Downloading: {url}')
        f_name = url[:5]
        try:
            with open(f'{workDir}/tmp/{f_name}', 'wb') as f:
                f.write(r.content)
        except AttributeError:
            print('[-] Ошибка сохранения файла...')
            
            
            

        
  
if __name__== "__main__":
  main()
