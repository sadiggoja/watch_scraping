import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd
import json
from PhillipsParser import PhillipsParser

url = "https://www.phillips.com/auctions/past"
Source = urllib.request.urlopen(url)
soup = BeautifulSoup(Source, 'lxml')

# Loads json from the website that contains all the data about auctions.
javs = soup.find("script", type="text/javascript").text.split(",")
# Filter json for month and year.
auctionDate = [k for k in javs if "Date" in k]
auctionYearList = []
auctionMonthList = []
for date2 in auctionDate:
    try:
        date2 = re.search("(\d{4})(\d{2})(\d{2})", date2)
        auctionYearList.append(date2.group(1))
        auctionMonthList.append(date2.group(2).replace("0", ""))
    except:
        continue
# Filter json for departments.
auctionsDepartments = [k for k in javs if "Department" in k]
DepartmentList = []
for Department in auctionsDepartments:
    DepartmentList.append(re.sub('(\"|\'|:|Department|u0026|\\\)', '', Department))
# Filter json for links.
auctionLinks = [k for k in javs if "Permalink" in k]
LinkList = []
for Auction in auctionLinks:
    LinkList.append(re.sub('(\"|\'|:|Permalink)', '', Auction))

auctions = pd.DataFrame()
# Combine filtered data into data frame.
auctions = auctions.assign(Year=auctionYearList, Month=auctionMonthList, Department=DepartmentList, Link=LinkList)
Contemporary = auctions[auctions.Department == "20TH CENTURY  CONTEMPORARY ART"]

for year in range(2019, 2020):
    result = pd.DataFrame()
    for month in range(1, 4):
        for Link in Contemporary[(Contemporary.Year == str(year)) & (Contemporary.Month == str(month))].Link:
            auctionUrl = "https://www.phillips.com" + Link
            # Parse lot links from auction site.
            source = urllib.request.urlopen(auctionUrl)
            soup = BeautifulSoup(source, 'lxml')
            LotList = []
            for options in soup.find_all("option"):
                LotList.append(options.attrs["value"])
            LotList = LotList[:len(LotList) - 4]

            # Parse the lots.
            for i in range(0, len(LotList)):
                result = result.append(PhillipsParser(LotList[i]), sort=True)
                print(len(result))
    print(str(year) + "_q1_phillips")
    result["Category"] = "20th Century and Contemporary Art"
    result["AuctionHouse"] = "Phillips"
    # Replace strings that disturb csvs.
    result = result.replace(";", "", regex=True)
    result = result.replace(",", "", regex=True)
    result = result.replace("\"", "", regex=True)
    result = result.replace("\n", "", regex=True)
    result.to_excel(str(year) + "Q1PhillipsContemporary.xlsx", encoding="utf-8-sig", index=False)
