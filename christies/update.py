from auctions import *
from pages import *
from updated_watch import *

def sort_by_date(driver):
    time.sleep(2)
    wait = WebDriverWait(driver, 10)
    sorter = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/chr-search-results/chr-loader-next/div/div[1]/div/chr-search-tab-bar/div[2]/div/chr-search-lots-view/div/section/chr-lots-control-panel/div/div[2]/div/chr-select/div/chr-button/button')))
    sorter.click()
    opt = wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/main/div[2]/chr-search-results/chr-loader-next/div/div[1]/div/chr-search-tab-bar/div[2]/div/chr-search-lots-view/div/section/chr-lots-control-panel/div/div[2]/div/chr-select/div/div/ul/li[2]')))
    opt.click()
    
    logging.info("Sorted")
    return driver


def get_update_watch_list():
    driver=sort_by_date(sign_in())

    all_titles=list(pd.read_csv("christies_watches.csv")["title"])

    watch_urls=list()
    time.sleep(10)

    for i in range(1):

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
        
        news=list()

        for container in driver.find_elements_by_class_name("chr-lot-tile-container"):
            new=dict()
            new["title"]=container.find_element_by_class_name("chr-lot-tile__primary-title").text
            new["url"]=container.find_element_by_tag_name("a").get_attribute("href")
            news.append(new)        
        
        for new in news:
            if(new["title"] not in all_titles):
                watch_urls.append(new["url"])
        
        time.sleep(1)
        
        pagination=driver.find_elements_by_class_name('chr-page-pagination__list')[1]
        pagination.find_elements_by_tag_name("chr-button")[-1].click()
    

    driver.quit()
    pd.DataFrame(watch_urls).to_csv("updated_watch_urls.csv", index=False)


def extract_updated_pages():

    watch_urls=[url["0"] for url in pd.read_csv("updated_watch_urls.csv").to_dict("records")]
    
    driver=sign_in()
    
    
    for url in watch_urls:
    
        driver.get(url)
        wait = WebDriverWait(driver, 4)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "chr-lot-header__information-column")))
        except:
            pass
        
        unique_name=str(watch_urls.index(url))
        
        with open(f"updated_watches/{unique_name}.html", "w", encoding='utf-8') as f:
                f.write(driver.page_source)

        logging.info(f"html saved with name: {unique_name}\n\n")
    
    driver.quit()


def main():
    get_update_watch_list()
    logging.info("urls updated\n")
    logging.info("extracting part...\n")
    extract_updated_pages()
    parse_update()


if __name__=="__main__":
    main()