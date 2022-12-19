import os
from auctions import *
from watch import watch

def iter_pages(driver):
    df=pd.read_csv("auctions.csv")
    auction_list=df.to_dict("records")
    logging.info("Iterating auction pages")
    driver.get("https://catalog.antiquorum.swiss")
    signin(driver)
    watches=list()
    for auc in auction_list:
        driver.get("https://catalog.antiquorum.swiss"+auc['auction_url'])
        logging.info(auc["auction_name"]+" is scrolling..")
        scroll_down(driver)
        save_html(driver.page_source, auc)

        watches+=watch(driver.page_source, auc)
    return watches
    

def save_html(page, auc):
    if not os.path.isdir("auctions"):
        os.makedirs("auctions")
    
    unique_name=auc['auction_location'].replace(" ", "")+auc['auction_date'].replace(" ", "").replace(":", "")
    
    with open(f"auctions/{unique_name}.html", "w", encoding='utf-8') as f:
        f.write(page)
    logging.info(f"html saved with name: {unique_name}")

