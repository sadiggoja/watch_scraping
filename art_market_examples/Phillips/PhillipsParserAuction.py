import urllib
from bs4 import BeautifulSoup
import pandas as pd
from PhillipsParser import PhillipsParser
from tqdm import tqdm

result = pd.DataFrame()

# auctionList = ["https://www.phillips.com/auctions/auction/UK030319","https://www.phillips.com/auctions/auction/UK010419","https://www.phillips.com/auctions/auction/UK010519","https://www.phillips.com/auctions/auction/NY010319","https://www.phillips.com/auctions/auction/HK010119","https://www.phillips.com/auctions/auction/HK010219","https://www.phillips.com/auctions/auction/NY010419","https://www.phillips.com/auctions/auction/NY010519"]
auctionList = ["https://www.phillips.com/auctions/auction/UK090319",
               "https://www.phillips.com/auctions/auction/UK010819",
               "https://www.phillips.com/auctions/auction/NY000719",
               "https://www.phillips.com/auctions/auction/HK010419",
               "https://www.phillips.com/auctions/auction/HK010319",
               "https://www.phillips.com/auctions/auction/NY010719",
               "https://www.phillips.com/auctions/auction/NY010919",
               "https://www.phillips.com/auctions/auction/NY010819",
               "https://www.phillips.com/auctions/auction/NY000619",
               "https://www.phillips.com/auctions/auction/HK090219",
               "https://www.phillips.com/auctions/auction/UK010719",
               "https://www.phillips.com/auctions/auction/UK010619",
               "https://www.phillips.com/auctions/auction/NY010619",
               "https://www.phillips.com/auctions/auction/UK090119",
               "https://www.phillips.com/auctions/auction/NY000419",
               "https://www.phillips.com/auctions/auction/UK010519",
               "https://www.phillips.com/auctions/auction/UK010419",
               "https://www.phillips.com/auctions/auction/HK010119",
               "https://www.phillips.com/auctions/auction/HK010219",
               "https://www.phillips.com/auctions/auction/NY010319",
               "https://www.phillips.com/auctions/auction/NY010419",
               "https://www.phillips.com/auctions/auction/NY010519",
               "https://www.phillips.com/auctions/auction/NY000219",
               "https://www.phillips.com/auctions/auction/UK010319",
               "https://www.phillips.com/auctions/auction/UK010219",
               "https://www.phillips.com/auctions/auction/UK010119",
               "https://www.phillips.com/auctions/auction/NY010119",
               "https://www.phillips.com/auctions/auction/NY000119"]

for url in tqdm(auctionList):
    auctionUrl = url
    # Parse lot links from auction site.
    source = urllib.request.urlopen(auctionUrl)
    soup = BeautifulSoup(source, 'lxml')
    LotList = []
    for options in soup.find_all("option"):
        LotList.append(options.attrs["value"])
    LotList = LotList[:len(LotList) - 4]

    # Parse the lots.
    for i in tqdm(range(0, len(LotList))):
        result = result.append(PhillipsParser(LotList[i]), sort=True)
        # print(len(result))

    result["Category"] = "20th Century and Contemporary Art"
    result["AuctionHouse"] = "Phillips"

    # Replace strings that disturb csvs.
    result = result.replace(";", "", regex=True)
    result = result.replace(",", "", regex=True)
    result = result.replace("\"", "", regex=True)
    result = result.replace("\n", "", regex=True)
    result.to_excel("2019_PhillipsContemporary.xlsx", encoding="utf-8-sig", index=False)
