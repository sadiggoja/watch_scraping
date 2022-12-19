from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup, NavigableString, Tag
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import requests
import os
import re
import logging

logging.basicConfig(level=logging.INFO, filename='christies.log')

def sign_in():

    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options ,executable_path=r'geckodriver.exe')
    driver.get("https://www.christies.com/departments/watches-wristwatches-60-1.aspx?pagesection=overview#overview")
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()
    except:
        pass
    time.sleep(2)
    signin = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/chr-header/header/div[1]/div/div/div/chr-button/button')))
    login="scrapertest2021@gmail.com"
    password="Pyth0nselenium"
    signin.click()
    driver.find_element_by_id("username").send_keys(login)
    driver.find_element_by_id("password").send_keys(password)
    signin=wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mb-1")))
    signin.click()
    time.sleep(8)

    search = wait.until(EC.element_to_be_clickable((By.ID, 'site-search')))
    time.sleep(1)
    search.send_keys("watches")
    search.send_keys(Keys.ENTER)

    time.sleep(6)
    icon=wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/chr-search-results/section/div/chr-autocomplete-input/form/div/chr-button/button')))
    icon.click()

    sold_lots = wait.until(EC.element_to_be_clickable((By.ID, 'tab-sold_lots')))
    sold_lots.click()

    filter_icon = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tabpanel-sold_lots"]/chr-search-lots-view/div/section/chr-lots-control-panel/div/div[1]/chr-drawer-toggle/chr-button/button/chr-icon')))
    filter_icon.click()

    cat_sect = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="filterDrawer"]/div/div[2]/div/chr-filter-block-lots/chr-filter-block/chr-accordion/div/chr-accordion-item[4]/div')))
    cat_sect.click()

    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sect_4"]/div/div/chr-checkbox[1]/label')))
    checkbox.click()

    close = wait.until(EC.element_to_be_clickable((By.ID, 'closeDrawer')))
    close.click()

    logging.info("Signed in")

    return driver


def scroll_down(driver):
    inf=driver.find_element_by_class_name("chr-page-nav__list-item").find_element_by_tag_name("a").text    
    n_prods=int(re.search(r'\((.*?)\)',inf).group(1))
    elements=driver.find_element_by_tag_name("chr-infinite-scroll").find_elements_by_xpath("div[1]/div")
    while len(elements) < n_prods:
        for i in range(12):
            driver.find_element_by_tag_name("body").send_keys(Keys.ARROW_DOWN)
        time.sleep(2)
        elements=driver.find_element_by_tag_name("chr-infinite-scroll").find_elements_by_xpath("div[1]/div")
    

def auctions_join():

    watches=pd.read_csv("christies_watches.csv").to_dict("records")
    auction_urls=list(set([wt["auction_url"] for wt in watches]))
    auction_list=list()
    for url in auction_urls:
        auction=dict()
        auction["auction_url"]=url
        response=requests.get(url)
        soup=BeautifulSoup(response.text,"html.parser")
        time.sleep(1)
        try:
            auction["auction_location"]=soup.find(class_="chr-auction-header__wrapper").text.strip()
            auction["auction_title"]=soup.find(class_="chr-auction-header__auction-title").text.strip()
            auction["auctio_date"]=soup.find(class_="chr-auction-header__auction-status").p.strong.text.strip()
        except:
            logging.info("\n")
            logging.info(url)
            logging.info(auction_urls.index(url))
            logging.info("\n")
        
        logging.info(auction_urls.index(url))
        
        auction_list.append(auction)

    auc_dict=dict()
    for auc in auction_list:
        auc_dict[auc["auction_url"]]=auc

    for w in watches:
        w.update(auc_dict[ w["auction_url"] ])

    pd.DataFrame(watches).to_csv("christies_watches.csv", index=False)
    

    