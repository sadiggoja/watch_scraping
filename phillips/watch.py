from pages import *
import re
from auctions import *

def parse_watch(watch_list):
    watches=list()
    # missed=list()
    for w in watch_list:
    # for miss in missed:
        # watch=miss.copy()
        watch=w.copy()
        unique_name="-".join(watch["url"].split("/")[-2:])
        with open("watches/"+unique_name+".html", encoding="utf8") as fp:
            soup=BeautifulSoup(fp, features="lxml")
        try:
            
            try:
                for span in soup.find("ul", {"class":"lot-page__details__list"}).li.find_all("span"):
                    watch[span.strong.text.replace(":", "")]=span.find("text").text.strip()
            except:
                pass
            
            try:
                watch["Description"]=soup.find(class_="lot-page__lot__title").text.split(watch['Reference No'])[1]
            except:
                watch["Description"]=soup.find(class_="lot-page__lot__title").text.strip()
            
            try:
                price_text=soup.find(class_="lot-page__lot__sold").text.split(" ")[-1]
                watch["currency"]=re.search(r'(\D*)[\d\,\.]+(\D*)',price_text).group(1)
                watch["realised_price"]=price_text.split(watch["currency"])[1]
            except:
                pass
            
            try:
                watch["Year"]= re.search(r"(\d{4})",watch["Year"]).group(1)
            except:
                pass
            
            try:
                
                est=soup.find(class_="lot-page__lot__estimate")
                
                if(est.find("span")):
                    text = ''
                    for child in est:
                        if isinstance(child, NavigableString):
                            text += str(child).strip()
                        elif isinstance(child, Tag):
                            if child.name != 'br':
                                text += child.text.strip()
                            else:
                                text += '\n'


                    try:
                        result = text.strip().split('\n')[1].replace("•", "").split(watch["currency"])[1].split("-")
                        watch["low_estimate"]=result[0]   
                    except:
                        result = text.strip().split('\n')[1].replace("•", "").split("-")
                        watch["currency"]=re.search(r'(\D*)[\d\,\.]+(\D*)',result[0]).group(1)
                        watch["low_estimate"]=result[0].replace(watch["currency"],"")
                        
                    watch["high_estimate"]=result[1].strip()

                else:
    #                 print(est.text)

                    try:
                        price=re.search("In Excess of (\D*)(\d+)", est.text).group(1)
                        price=est.text.split(price)[1]
                        
                        try:
                            watch["low_estimate"]=price.split(" ")[0]
            #             print(price.split(re.search(r"^(\D*)(\d+)(\D*)$",price).group(1)))
                        except:
                            watch["low_estimate"]=price
            #             print("\n"+watch["low_estimate"]+"\n")
                        
                        watch["high_estimate"]=None
                    except:
                        text = ''
                        for child in est:
                            if isinstance(child, NavigableString):
                                text += str(child).strip()
                            elif isinstance(child, Tag):
                                if child.name != 'br':
                                    text += child.text.strip()
                                else:
                                    text += '\n'
                        
                        try:
                            result = text.strip().split('\n')[1].replace("•", "").split(watch["currency"])[1].split("-")
                            watch["low_estimate"]=result[0]
                        except:
                            result = text.strip().split('\n')[1].replace("•", "").split("-")
                            watch["currency"]=re.search(r'(\D*)[\d\,\.]+(\D*)',result[0]).group(1)
                            watch["low_estimate"]=result[0].replace(watch["currency"],"")
                        
                        watch["high_estimate"]=result[1].strip()
            except:
                watch["high_estimate"]=None
                watch["low_estimate"]=None
        except:
            logging.info("\n")
            logging.info(watch["url"])
    #         missed.append(watch_list.index(w))
            logging.info(unique_name+" not completed\n")
            continue
    # #     --------------------------
    #     if(watch_list.index(w)%50==0):
    #         print(watch_list.index(w))
    # #     --------------------------
        # print(missed.index(miss))
        watches.append(watch)

    return watches