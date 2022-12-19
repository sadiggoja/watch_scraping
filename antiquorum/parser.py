from pages import *
from auctions import *

def parse_extract():

    print("Give number of auctions you want\n0(zero) for all\n")
    max=int(input())
    extract_auction_data(max)
    
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path=r"geckodriver.exe")
    
    watches=iter_pages(driver)

    driver.quit()

    df = pd.DataFrame(watches)
    df.to_csv("watches.csv", index=False)
    logging.info("Watches are extracted to watches.csv file")

def main():
    parse_extract()
    

if __name__=="__main__":
    main()