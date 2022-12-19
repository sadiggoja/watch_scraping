from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

logging.basicConfig(level=logging.INFO, filename='antiquorum.log')

def signin(driver):
    wait = WebDriverWait(driver, 10)
    signin = wait.until(EC.element_to_be_clickable((By.ID, 'sign-in')))
    login="scrapertest2021@gmail.com"
    password="pythonselenium"
    signin.click()
    signin=wait.until(EC.element_to_be_clickable((By.NAME, 'button')))
    driver.find_element_by_id("user_email").send_keys(login)
    driver.find_element_by_id("user_password").send_keys(password)
    signin.click()
    time.sleep(1)
    logging.info("Signed in")
    return driver

def scroll_down(driver):
    try:
        total=int(driver.find_element_by_id("total_results").text)
    except:
        pass
    logging.info("Scrolling...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        
        try:    
            if len(driver.find_elements_by_class_name("shadow"))>total:
                break
        except:
            pass
    return driver


def load_page():
    
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r'geckodriver.exe')
    logging.info("Site is opening...")
    driver.get("https://catalog.antiquorum.swiss/")
    driver=signin(driver)

    time.sleep(5)
    driver=scroll_down(driver)
    page=driver.page_source
    driver.quit()
    return page


def parse_list(page, max):

    soup=BeautifulSoup(page, features="lxml")
    auctions=soup.find("div", {"id":"auctions"}).findAll("div", recursive=False)
    logging.info(f"{str(len(auctions))} auctions founded")
    auction_list=list()
    
    if(max==0):
        max=len(auctions)
    
    for i in range(max):
        auc=dict()
        subsections=auctions[i].findAll("div", recursive=False)[1].findAll("div", recursive=False)
        auc["auction_url"]=subsections[0].a.get("href")
        auc["auction_name"]=subsections[1].h5.text
        auc["auction_location"]=subsections[1].p.text
        auc["auction_date"]=subsections[1].find_all("p")[1].text
        try:
            auc["auction_sale"]=subsections[2].p.text.split(" : ")[1]
        except:
            auc["auction_sale"]=None
        
        auction_list.append(auc)

    return auction_list

def extract_auction_data(max):
    auctions = parse_list(load_page(), max)
    #special problematic cases
    # auctions.pop(55)
    # auctions.pop(169)
    # auctions.pop(183)

    
    df = pd.DataFrame(auctions)
    df.to_csv("auctions.csv", index=False)
    logging.info("Auctions are extracted to auctions.csv file")
    
