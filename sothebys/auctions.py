from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
import os
from lxml import etree
from io import StringIO
import unicodedata
import logging

logging.basicConfig(level=logging.INFO, filename='sothebys.log')

def scroll_down(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def sign_in_driver():
    options = Options()
    options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Sadig Goja\Documents\python\gamcap\geckodriver.exe')
    driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
    driver.get("https://www.sothebys.com/api/auth0login?lang=en&fromHeader=Y")
    wait = WebDriverWait(driver, 10)
    signin = wait.until(EC.visibility_of_element_located((By.ID, 'login-button-id')))
    login="scrapertest2021@gmail.com"
    password="Pyth0nselenium"
    driver.find_element_by_id("email").send_keys(login)
    driver.find_element_by_id("password").send_keys(password)
    signin.click()
    time.sleep(2)
    try:
        dialog_closer = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'DialogOverlay-close')))
        dialog_closer.click()
    except:
        pass

    logging.info("Signed in")
    
    return driver


def get_auctions():

    driver=sign_in_driver()

    driver.get("https://www.sothebys.com/en/results?from=&to=&f2=00000164-609a-d1db-a5e6-e9fffc050000&q=")

    scroll_down(driver)
    
    soup=BeautifulSoup(driver.page_source, features="lxml")
    items=soup.find_all(class_="SearchModule-results-item")

    auctions=list()
    for item in items:
        auction=dict()
        auction["auction_title"]=item.find(class_="Card-title").text
        auction["auction_url"]=item.a.get("href")
        auction["auction_date"]=item.find(class_="Card-details").text.split("|")[0].strip()
        auction["auction_location"]=item.find(class_="Card-details").text.split("|")[-1].strip()
        auctions.append(auction)
    
    driver.quit()
    return auctions







def get_urls_in_auction(driver):
    items=list()
    
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[2]/ul/li')))
    except:
        pass
    
    
    btns=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[2]/ul/li")
    if(btns):
        max_page=int(btns[-2].text)
        for i in range(max_page):
            try:
                wait = WebDriverWait(driver, 10)
                wait.until(EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div')))
            except:
                pass
            products=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div")
            items+=[
                prod.find_element_by_tag_name('a').get_attribute("href") 
                for prod in products
            ]

            btns=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[2]/ul/li")
            next_btn=btns[-1].find_element_by_tag_name("button")
            next_btn.click()
    else:
        products=driver.find_elements_by_xpath("/html/body/div[2]/div/div/div[4]/div/div[3]/div/div/div[2]/div[1]/div/div/div/div[3]/div/div[1]/div")
        if(products):
            items+=[
                prod.find_element_by_tag_name('a').get_attribute("href") 
                for prod in products
            ]
        else:
            if(driver.find_elements_by_class_name("AuctionsModule-results-item")):
                btns=driver.find_element_by_class_name("pagination").find_elements_by_xpath("a")
                if(btns):
                    max_page=int(driver.find_element_by_class_name("pagination").find_elements_by_tag_name("a")[-2].text)
                    for num in range(max_page):
                        try:
                            wait = WebDriverWait(driver, 20)
                            wait.until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[2]/div[2]/div/div[2]/a[6]")))
                        except:
                            pass
                        items+=[
                            item.find_element_by_tag_name("a").get_attribute("href") 
                            for item in driver.find_elements_by_class_name("AuctionsModule-results-item")
                        ]
                        btns=driver.find_element_by_class_name("pagination").find_elements_by_xpath("a")
                        next_btn=btns[-1]
                        next_btn.click()
                else:
                    items+=[
                        item.find_element_by_tag_name("a").get_attribute("href") 
                        for item in driver.find_elements_by_class_name("AuctionsModule-results-item")
                    ]
            else:
                logging.info("empty")
    
    return items


    