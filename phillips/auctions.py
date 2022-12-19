from pages import *
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup, NavigableString, Tag
import re
import time
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from selenium.webdriver.common.keys import Keys
import logging

logging.basicConfig(level=logging.INFO, filename='phillips.log')

def signin():
    options = Options()
    options.headless = True
    # driver = webdriver.Firefox(options=options, executable_path=r'C:\Users\Sadig Goja\Documents\python\gamcap\geckodriver.exe')
    driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
    driver.get("https://www.phillips.com/auctions/past/filter/Departments%3DWatches/sort/oldest")
    wait = WebDriverWait(driver, 10)
    signin = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'phillips__nav__header__item__button--login')))
    login="scrapertest2021@gmail.com"
    password="Pyth0nselenium"
    signin.click()
    signin=wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-default')))
    driver.find_element_by_name("Username").send_keys(login)
    driver.find_element_by_name("Password").send_keys(password)
    signin.click()
    time.sleep(1)
    logging.info("Signed in")
    return driver

def scroll_down(driver):
    logging.info("Scrolling")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_auctions():
    
    driver=signin()
    
    scroll_down(driver)

    soup=BeautifulSoup(driver.page_source)
    auctions=list()
    for li in soup.find_all("li",{"class":"has-image"}):
        auc=dict()
        auc["url"]=li.a.get('href')
        auc["title"]=li.h2.text
        splitter=re.search("Auction(.+?)",li.p.text).group(0)
        auc["location"]=li.p.text.split(splitter)[0]
        auc["date"]=li.p.text.split(splitter)[1]
        auctions.append(auc)

    logging.info(f"{len(auctions)} auctions founded")
    driver.quit()
    return auctions

