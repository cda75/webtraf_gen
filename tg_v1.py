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
from time import sleep

#URL list
url_file = "urls.txt"

def get_urls(u_file):
    with open(u_file, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]


def get_links_from_page(url, n=1, with_download=False):
    headers = {'User-Agent': 
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/90.0.4430.85 Safari/537.36'}
    r = requests.get(url, headers=headers)
    html = r.text
    #print(url, r.status_code, len(html))
    if (r.status_code == 200) and (len(html)) > 0:
        bs = bs4(html, features='html.parser')
        hrefs = [href.get("href") for href in bs.find_all('a')]   
        rand_urls = []
        count = 0
        while count < n:
            rand_href = hrefs[randint(0,len(hrefs))]
            if 'https' in rand_href:
                rand_urls.append(rand_href)
                count += 1
        if n == 1:
            return rand_urls[0]
        else:
            return rand_urls


def browser(url):
    options = Options()
    options.add_argument('--headless=new')
    driver = webdriver.Chrome('./chromedriver', options=options)
    try:
        driver.get(url)
        print(driver.current_url, driver.title)
        sleep(2)
    except BaseException as error:
        print(f'Error when accessng {url}')
        print(error)
    finally:
        driver.close()
    
 
    
    
def main():
    urls = get_urls(url_file)
    for url in urls:
        rand_urls = get_links_from_page(url,2)
        for rand_url in rand_urls:
            browser(rand_url)
        

        
  
if __name__== "__main__":
  main()