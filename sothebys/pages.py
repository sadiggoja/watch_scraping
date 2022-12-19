from auctions import *


def get_watch_urls(max):

    watches=list()
    auctions=get_auctions()
    if(max==0):
        max=len(auctions)
    driver=sign_in_driver()

    for i in range(max):
        
        driver.get(auctions[i]["auction_url"])
        
        try:
            auc_watches=get_urls_in_auction(driver)
        except:
            logging.info("___NOT COMPLETED___")
            logging.info(auctions[i]["auction_title"])
            logging.info(auctions.index(auctions[i]))
            logging.info("\n")
            continue
        
        logging.info(len(auc_watches))
        logging.info(auctions[i]["auction_title"])
        logging.info(auctions.index(auctions[i]))
        logging.info("\n")
        
        for w in auc_watches:
            temp=auctions[i].copy()
            temp["url"]=w
            watches.append(temp)

    pd.DataFrame(watches).to_csv("watch_url.csv", index=False,encoding='utf-8-sig')

    driver.quit()




def extract_pages():
    
    watches=pd.read_csv("watch_url.csv").to_dict("records")
    driver=sign_in_driver()
    for w in watches:
    
        driver.get(w["url"])
 
        time.sleep(2)
        unique_name=str(watches.index(w))
        try:
            with open(f"watches/{unique_name}.html", "w", encoding='utf-8') as f:
                    f.write(driver.page_source)
        except:
            logging.info(f"problem ocurred: {unique_name}\n\n")
            continue
        logging.info(f"html saved with name: {unique_name}\n\n")