from auctions import *


def get_watch_list():
    driver=sign_in()
    watch_urls=list()
    time.sleep(10)
    logging.info("Getting urls:\n")
    for i in range(500):
        logging.info(f"page number:{str(i)}")
        wait = WebDriverWait(driver, 4)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chr-lot-tile-container')))
        except:
            try:
                icon=wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/main/div[2]/chr-search-results/section/div/chr-autocomplete-input/form/div/chr-button/button')))
                icon.click()
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'chr-lot-tile-container')))
            except:
                pass

        for attemp in range(5):
            try:
                watch_urls+=[
                    container.find_element_by_tag_name("a").get_attribute("href") 
                    for container in driver.find_elements_by_class_name("chr-lot-tile-container")
                ]
                break
            except:
                time.sleep(1)
                
        
        time.sleep(1)
        
        pagination=driver.find_elements_by_class_name('chr-page-pagination__list')[1]
        pagination.find_elements_by_tag_name("chr-button")[-1].click()
    
    driver.quit()
    pd.DataFrame(watch_urls).to_csv("watch_urls.csv", index=False)


def extract_pages():

    watch_urls=[url["0"] for url in pd.read_csv("watch_urls.csv").to_dict("records")]
    
    driver=sign_in()
    
    logging.info("Extracting pages:\n")
    for url in watch_urls:
    
        driver.get(url)
        wait = WebDriverWait(driver, 4)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chr-lot-header__information-column")))
        except:
            pass
        
        unique_name=str(watch_urls.index(url))
        
        with open(f"watches/{unique_name}.html", "w", encoding='utf-8') as f:
                f.write(driver.page_source)

        logging.info(f"html saved with name: {unique_name}\n\n")
