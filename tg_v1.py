# -*- coding: utf-8 -*-
"""
Created on Sat Jun 24 11:36:28 2023
Traffic Generator
@author: Dimka
"""
import requests
from random import randint
from bs4 import BeautifulSoup as bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
from os import path
from platform import system

#URL list
url_file = "urls.txt"
workDir = path.dirname(path.abspath(__file__))
drv_exec = '/chromedriiver' if system() == 'Linux' else '\chromedriver.exe' 
drv_exec = workDir + drv_exec

def get_urls(u_file):
    with open(u_file, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_links_from_page(url, n=1, with_download=False):
    headers = {'User-Agent': 
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/90.0.4430.85 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    if (r.status_code == 200) and (len(html)) > 0:
        bs = bs4(html, features='html.parser')
        hrefs = [href.get("href") for href in bs.find_all('a')]   
        rand_urls = []
        count = 0
        while count < n:
            rand_num = randint(0,len(hrefs))
            rand_href = hrefs[rand_num]
            if 'https' in rand_href:
                rand_urls.append(rand_href)
                count += 1
        if n == 1:
            return rand_urls[0]
        else:
            return rand_urls


def browser(url):
    options = Options()
    service = Service(executable_path = drv_exec)
    options.add_argument('--headless=new')
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get(url)
        print(driver.current_url, driver.title)
        #sleep(2)
    except BaseException as error:
        print(f'Error when accessng {url}')
    finally:
        driver.close()
    
 
    
    
def main():
    urls = get_urls(url_file)
    for url in urls:
        rand_urls = get_links_from_page(url,2)
        for url in rand_urls:
            browser(url)
        

        
  
if __name__== "__main__":
  main()
