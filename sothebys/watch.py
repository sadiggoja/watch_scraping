from auctions import *

properties=[
    "Dial", "Calibre", "Movement number", "Case", 
    "Case number", "Closure", "Dimensions",
    "Signed", "Box", "Papers", "Accessories",
    "Caliber", "Size"]

def parse_watch():
    
    watches=list()
    files =[file for file in os.listdir("watches/")]
    watch_urls=pd.read_csv("watch_url.csv").to_dict("records")
    htmlparser = etree.HTMLParser()
    for file in files:
        ind_watch=int(file.split('.')[0])
        watch=watch_urls[ind_watch].copy()
        
        with open(f"watches/{file}", encoding="utf8") as fp:
            soup=BeautifulSoup(fp, features="lxml")
        
        with open(f"watches/{file}", encoding="utf8") as fp:
            tree=etree.parse(fp, htmlparser)        
        
        logging.info(file+"-----"+str(files.index(file)))
        
        try:
            if(soup.find(class_="LotPage-productHead")):
                logging.info("class_type")
                watch=class_type(watch, soup)
            else:
                logging.info("xpath_type")
                watch=xpath_type(watch, soup, tree)
                pass
        except:
            logging.info("\n---------------------")
            logging.info("NOT COMPLETED")
            logging.info(watch["url"])
            logging.info("---------------------\n")
            continue
        
        watches.append(watch)

    pd.DataFrame(watches).to_csv("sothebys_watches.csv", index=False, encoding='utf-8-sig')



def class_type(watch, soup):
    info=soup.find(class_="LotPage-productInfo")
    try:
        watch["title"]=unicodedata.normalize("NFKD",info.find(class_="LotPage-productTitle").text.strip())
    except:
        pass
    
    est=info.find(class_="LotPage-estimatePrice")
    
    if(est):
        est=est.text.strip()
        watch["currency"]=est.split(" ")[-1]
        watch["low_estimate"]=est.split(" ")[-4]
        watch["high_estimate"]=est.split(" ")[-2]
    
    sold=soup.find(class_="LotPage-soldPrice")
    
    if(sold):
        sold=sold.text.strip()
        watch["currency"]=sold.split(" ")[-1]
        watch["realised_price"]=sold.split(" ")[0]
    
    description=""
    
    desc=soup.find(class_="LotPage-lotDescription") 
    if(desc):
        description+=unicodedata.normalize("NFKD",desc.text.strip())
    
    
    details=soup.find(class_="LotPage-lotDetails")
    if(details):
        for det in details.contents:
            try:
                description+=" "
                description+=unicodedata.normalize("NFKD",det.text.strip())
            except:
                pass
    
    
    watch['description']=description
    
    watch["year"]=desc_year(description)
    watch["reference"]=desc_ref(description)
    return watch

def xpath_type(watch, soup, tree):
    
    watch['title']=unicodedata.normalize("NFKD",soup.find("h1", {"data-cy":"lot-title"}).text)
    
    try:
        elem=tree.xpath('/html/body/div[2]/div/div/div[4]/div/div/div[3]/div[3]/div[1]/div[2]/div[2]/div[2]')    
        if(not elem):
            elem=tree.xpath("/html/body/div[2]/div/div/div[4]/div/div/div[3]/div[3]/div[1]/div[2]/div[3]/div[2]")
        
        est=" ".join([child.text for child in elem[0].getchildren()])
            
    except:
        logging.info("est problem")
        logging.info(watch['url'])
    
#     print(est)
        
    if(est):
        watch["currency"]=est.split(" ")[-1]
        watch["low_estimate"]=est.split(" ")[-4]
        watch["high_estimate"]=est.split(" ")[-2]
    
    try:
        sold_elem=tree.xpath("/html/body/div[2]/div/div/div[4]/div/div/div[3]/div[3]/div[1]/div[2]/div[4]/div[1]/div[1]")
        sold=" ".join([child.text for child in sold_elem[0].getchildren()])
    except:
        sold_elem=tree.xpath("/html/body/div[2]/div/div/div[4]/div/div/div[3]/div[3]/div[1]/div[2]/div[3]/div[1]/div[1]")
        sold=" ".join([child.text for child in sold_elem[0].getchildren()])

    if(sold):
        watch["realised_price"]=sold.split(" ")[-2]
#         print(watch["realised_price"])
        
        
        
    desc=soup.find("div",{"id":re.compile("collapsable-container-Description")}).find("div", recursive=False)    
    if(desc):   
        description=''

        for i in desc.find("div").find("div").contents:
            description+=" "
            description+=unicodedata.normalize("NFKD",i.text.strip())

        try:
            for i in desc.findAll("p"):
                data_prop=i.text.split(":")
                if(len(data_prop)>1):
                    prop=data_prop[0].encode('utf-8').decode('utf-8-sig').strip()
                    if(prop in properties):
                        watch[prop]=data_prop[1].strip()
        except:
            pass

                
        watch['description']=description
    else:
        pass
    
    watch["year"]=desc_year(description)
    watch["reference"]=desc_ref(description)
    
    return watch


def desc_year(description):
    try:
        return re.search("CIRCA (\d+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("Circa (\d+)", description).group(1)
    except:
        pass 
    
    try:
        return re.search("CIRCA: (\d+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("MADE IN (\d+)", description).group(1)
    except:
        pass
    
    try:
#         return re.search(".*([1-2][0-9]{3})", description).group(1)
        return re.search(".*(1[0-9][0-9][0-9]|20[0-2][0-9])", description).group(1)        
    except:
        pass
    
    try:
        return re.search("in (\d+)", description).group(1)
    except:
        pass
    

    
    return ""


def desc_ref(description):
    try:
        return re.search("REF (\S+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("Ref. (\S+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("REFERENCE (\S+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("Reference (\S+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("reference (\S+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("ref (\S+)", description).group(1)
    except:
        pass
    
    try:
        return re.search("ref. (\S+)", description).group(1)
    except:
        pass
    
    return ""
