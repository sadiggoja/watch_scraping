from auctions import *


def get_watch_list(max):
    
    auctions=get_auctions()
    
    watch_list=list()

    if(max==0):
        max=len(auctions)

    for i in range(max):
        
        base="https://www.phillips.com/"
        response=requests.get(base+auctions[i]["url"])
        time.sleep(1.5)
        page=BeautifulSoup(response.text,"html.parser")
        for li in page.find_all("li", {"class": "lot single-cell"}):
            try:
                watch=dict()
                watch["auc_url"]=auctions[i]["url"]
                watch["auction"]=auctions[i]["title"]
                watch["auction_date"]=auctions[i]["date"]
                watch["auction_location"]=auctions[i]["location"]
                watch["url"]=li.a.get("href")
                watch_list.append(watch)
            except:
                logging.info(li.p.text+". is no available")

    return watch_list


def extract_pages(watch_list):

    driver=signin()
    for watch in watch_list:
        try:
            time.sleep(1)
            driver.get(watch["url"])
            unique_name="-".join(watch["url"].split("/")[-2:])
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'lot-page__lot__maker__name')))
            logging.info(element.text+" is downloaded")
            try:
                with open(f"watches/{unique_name}.html", "w", encoding='utf-8') as f:
                    f.write(driver.page_source)
            except:
                logging.info("---"+str(watch_list.index(watch))+"--- problem ocurred with saving")
                continue
            logging.info("---"+str(watch_list.index(watch))+"---")
            logging.info(f"html saved with name: {unique_name}\n\n")

        except:
            logging.info(watch["url"])
    driver.quit()