import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd


def PhillipsParser(LotUrl):
    LotSource = urllib.request.urlopen(LotUrl)
    LotSoup = BeautifulSoup(LotSource, 'lxml')

    try:
        estimates = LotSoup.find("p", class_="lot-detail-header__estimate").text
        estimates = re.split("Estimate|\xa0", estimates)[1]
        estimates = re.split("(\$|\£|HK\$|-)", estimates)
        Currency = estimates[1]
        LowEstimate = float(estimates[2].replace(",", ""))
        HighEstimate = float(estimates[4].replace(",", ""))
    except:
        Currency = "N/A"
        LowEstimate = "N/A"
        HighEstimate = "N/A"

    try:
        realized = LotSoup.find("p", class_="lot-detail-header__sold").text
        RealizedPrice = re.split("(\$|\£|HK\$])", realized)[-1].replace(",", "")
    except:
        RealizedPrice = "N/A"

    if LotSoup.find("span", attrs={'class': None}) is None:
        ExecutionDate = "N/A"
        Medium = "N/A"
        Dimension = "N/A"
    else:
        LotInfo = []
        for span in LotSoup.find_all("span", attrs={'class': None}):
            LotInfo.append(span.text)

        try:
            ExecutionDate = re.findall("\d{4}", "".join(LotInfo))[1]
        except:
            ExecutionDate = "N/A"
            pass

        dm = re.compile("(\d{1,}.{0,1}\d{0,} x \d{1,}.{0,1}\d{0,} x \d{1,}.{0,1}\d{0,} (cm|mm)|\d{1,}.{0,1}\d{0,} "
                        "x \d{1,}.{0,1}\d{0,} (cm|mm)|\d{1,}.{0,1}\d{0,2} (cm|mm))")
        try:
            Dimension = list(filter(dm.search, LotInfo))[0]
            for iCounter in range(0, len(LotInfo)):
                if LotInfo[iCounter] == Dimension:
                    Medium = LotInfo[iCounter - 2]
        except:
            Dimension = "N/A"
            Medium = "N/A"
            pass

    try:
        Location = re.search("Hong Kong|Paris|London|Taipei|New York|Online",
                             LotSoup.find("meta", property="og:description")["content"]).group(0)
    except:
        Location = "N/A"

    try:
        Date = LotSoup.find("meta", property="og:description")["content"]
        Date = Date.replace("\xa0", " ")
        Date = re.findall("\d{1,} [a-zA-Z]{1,} \d{4}", Date)[0]
    except:
        Date = "N/A"

    try:
        Auction = LotSoup.find("div", class_="sale-title-banner").find("strong").text
    except:
        Auction = "N/A"

    if LotSoup.find("div", class_="lot-page-maker") is None:
        Artist = "N/A"
    else:
        Artist = LotSoup.find("div", class_="lot-page-maker")
        Artist = Artist.find("h1", class_="lot-page-maker__name").text.strip()

    try:
        Artwork = LotSoup.find("title").text.replace(" | Phillips", "")
    except:
        Artwork = "N/A"

    LotInfo = pd.DataFrame()
    LotInfo = LotInfo.assign(Auction=[Auction], Date=[Date], Location=[Location], Artist=[Artist],
                             ExecutionDate=[ExecutionDate], Artwork=[Artwork], Dimension=[Dimension], Medium=[Medium],
                             LowEstimate=[LowEstimate], HighEstimate=[HighEstimate], RealizedPrice=[RealizedPrice],
                             Currency=[Currency], Source=[LotUrl])
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    #     print(LotInfo)

    return(LotInfo)



