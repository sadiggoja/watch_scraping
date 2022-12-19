from auctions import *
import re
def watch(page, auc):
    soup=BeautifulSoup(page, features="lxml")
    products=soup.find("div",{"id":"products"}).find_all(recursive=False)
    products = [tag for tag in products if tag.name != "script" ]
    
    watches_list=list()
    for i in range(0,len(products)):
        watch=dict()
        watch["auction_date"]=auc["auction_date"]
        watch['auction_location']=auc['auction_location']
        watch['auction_name']=auc['auction_name']
        watch['auction_url']=auc['auction_url']
        try:
            if (products[i].get("class")[0] !="row"):
                desc=products[i].find(class_="N_lots_description col")
                watch["title"]=desc.a.text.strip().replace("\n"," ")
                watch["url"]=desc.a.get("href")

                try:
                    est=products[i].find(class_="N_lots_estimations col").find("p")
                    watch['currency']=est.text.strip().replace(" -\t","").split(" ")[0]
                    watch['low_estimate']=est.text.strip().replace(" -\t","").split(" ")[1]
                    watch['high_estimate']=est.text.strip().replace(" -\t","").split(" ")[2]
                except:
                    watch['currency']=None
                    watch['low_estimate']=None
                    watch['high_estimate']=None

                try:
                    watch['realised_price']=products[i+1].p.text.strip().split(" ")[2]
                except:
                    watch['realised_price']=None

                try:
                    watch["description"]=" ".join([div.text.strip().replace("\n"," ") for div in desc.find_all("div")])
                    if(not (watch["description"])):
                        watch["description"]=" ".join([txt.replace("\n", " ") for txt in desc.text.split("\n \n\n\t\t\t\t\t\t")[1:]]).strip()
                except:
                    watch["description"]=None
                
                

                try:
                    properties = products[i].find(class_="pt-2 shadow-sm p-2").findAll("p")
                    for prop in properties:
                        prop=prop.text.split("\u2003")
                        watch[prop[0]]=prop[1]
                    try:
                        watch["Year"]= re.search(r"(\d{4})",watch["Year"]).group(1)
                    except:
                        pass
                except:
                    pass

                watches_list.append(watch)
            else:
                continue
        except:
            logging.info(str(int((i+2)/2))+". lot withdrawn")
        
        
    logging.info(str(len(watches_list))+" watches done")
    return watches_list