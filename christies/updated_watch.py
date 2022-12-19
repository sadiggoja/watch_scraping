from auctions import *

def parse_update():
    files =[file for file in os.listdir("updated_watches/")]
    watches=list()
    watch_urls=[url["0"] for url in pd.read_csv("updated_watch_urls.csv").to_dict("records")]

    for file in files:
        watch=dict()
        
        
        with open(f"updated_watches/{file}", encoding="utf8") as fp:
            soup=BeautifulSoup(fp, features="lxml")

        
        info=soup.find(class_="chr-lot-header__information")
        if(not info):
            logging.info("\n--------------------")
            logging.info(file)
            logging.info("empty slot")
            logging.info("--------------------\n")
            continue
            
        logging.info(file+"-----"+str(files.index(file)))
        watch["url"]=watch_urls[int(file.split(".")[0])]
        watch["title"]=info.find(class_="chr-lot-header__artist-name").text.strip()
        bid_details=info.find(class_="chr-lot-header__bid-details")    
        if(bid_details.find(class_="chr-lot-header__value-field")):
            watch['currency']=bid_details.find(class_="chr-lot-header__value-field").text.split(" ")[0]
            watch['realised_price']=bid_details.find(class_="chr-lot-header__value-field").text.split(" ")[1]

            est_pr = bid_details.find(class_="chr-lot-header__estimate-details").text.split("-")
            try:
                watch["high_estimate"] = est_pr[1].split(" ")[2]
                watch["low_estimate"] = est_pr[0].split(" ")[1]
            except:
                pass
        try:
            watch["auction_url"]=soup.find(class_="chr-breadcrumb__link").get("href")
            if(watch["auction_url"][:2]=='/s'):
                watch["auction_url"]="https://onlineonly.christies.com"+watch["auction_url"]
            

        except:
            pass
        
        watch['details']=soup.find(class_="chr-lot-header__title").text
        details=[det.strip() for det in watch['title'].split(",")]
        
        if(watch['details']):
            details+=[det.strip() for det in watch['details'].split(",")]
        
        try:
            additional_info=soup.find(class_="chr-accordion-item").contents[1]
            additional_info=additional_info.split("\n")
            if(len(additional_info)==1):
                additional_info=soup.find(class_="chr-accordion-item").contents[1].stripped_strings
            watch["description"]=" ".join(additional_info)
            details+=additional_info
        except:
            pass
        
        for d in details:
            try:
                watch['ref']=re.search("REF\. (\d+)", d).group(1)
            except:
                pass
            
            try:
                watch['ref']=re.search("REF (\d+)", d).group(1)
            except:
                pass
            
            try:
                watch['ref']=re.search("Ref\.(\d+)", d).group(1)
            except:
                pass
            
            try:
                watch['ref']=re.search("reference (\d+)", d).group(1)
            except:
                pass
            
            try:
                watch['ref']=re.search("ref: (\d+)", d).group(1)
            except:
                pass

            try:
                watch['year']=re.search("MANUFACTURED IN (\d+)", d).group(1)
            except:
                pass
            
            try:
                watch['year']=re.search("CIRCA: (\d+)", d).group(1)
            except:
                pass

            try:
                watch['year']=re.search("CIRCA (\d+)", d).group(1)
            except:
                pass

            try:
                watch['case_no']=d.split(re.search("CASE NO\. (\.?)", d).group(0))[1]        
            except:
                pass

            try:
                watch["brand"]=d.split(re.search("SIGNED (\.?)", d).group(0))[1]
            except:
                pass

            try:
                watch["model"]=d.split(re.search("(\.?) MODEL", d).group(0))[0]
            except:
                pass


            
            
            
        watches.append(watch)
    #     print("--------------------\n")

    pd.DataFrame(watches).to_csv("updated_christies_watches.csv", index=False)