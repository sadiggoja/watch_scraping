import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from math import ceil
import logging
from tqdm import tqdm

headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "tr-TR,tr;q=0.8,en-US;q=0.5,en;q=0.3",
           "Connection": "keep-alive",
           "Cookie": "ajs_user_id=null; ajs_group_id=null; ajs_anonymous_id=%22dbe14605-030f-4bf2-9552-6b3f597fe194%22; acceptedCookieUsage=true; _ALGOLIA=2d01cccb-6b6a-44fc-8fca-e5ba9c1da29b; JSESSIONID=EEDCF17C4BBEDF6DE6A066F9F7F2CFFD; renderid=rend01; parent_resource=http%253A%252F%252Fwww.sothebys.com%252Fen%252Fauctions%252Fecatalogue%252F2018%252F18028-contemporary-art-online%252Flot.18.html%253Flocale%253Den; ak_bmsc=461404C6F137D7DE48A9B1F24B480AEE17C0A3A9A53300007C8D7E5C82196D15~pl7rbxWlPspuCS9e5yqJEZat9z2W4fTZMYaVn+KoC6PbCyZWRfF4bZ+ce/5j70zWN/ndZWaY9p+rBP3Usp7cpTxtKmec/vIi6eQAxSRf0UpH+WjvP46MklKvDxm8GiJU+ys7HuPjXLRAOSGfFHo+fmJQzw3NKqMzja0bHknBk6jJxcJmilFnr81knIBnW32bXRy1dqaH7CUeWpl44re9of0t1j9vrE1+omb/bnxYy5EH8=; bm_sv=A43412B68ECAD4D66881FC34F964ABC2~XBneSfIfs+mSQqaTzIgkKaY6bSR2BigEewp78ueA3AnHTsxz9HpRR2tGByUFRwxoONW9jWt+s7rwqL+W+VS1NMFPB8BWPVjpVxgTwDtNiT1myV5BUEdIXJc2JrR6RZrQj4TtqccFA3v1W1yZFG4qfjdWT22fcl7CWvadwuKXEBU=; bm_mi=B4B4E3842ECCC728DDD2826BB77F97E3~ptcMxktl0CJRDlemuH/JMmF7K74CeSIN+p2KPeSwBlmmUvn2EViHE9FS03/FqPZxmvLXdVI8vPdoDizMTvqnTDXJA1xP6RKKVqlKCNMeiLFKzifBjUiee1OPX8FSIP1XwecFadr8taxcIPMhGej2XND+XJzzexblMwF4sJF60AA7UDf6V4Pj+P9aKGP1i/HLaj8z1qQ3pMTZeAMk1TPvhELBzUs8HtRJqlrSnYREUaI=",
           "DNT": "1", "Host": "www.sothebys.com", "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0"}


def sothebys_lot_parser(LotUrl):
    LotInfo = pd.DataFrame()
    try:
        LotResponse = requests.get(LotUrl, headers=headers)
        LotSoup = BeautifulSoup(LotResponse.text, 'html.parser')
    except:
        LotInfo = LotInfo.assign(Auction="N/A", Date="N/A", Location="N/A", Artist="N/A", ExecutionDate="N/A",
                                 Artwork="N/A", Dimension="N/A", Medium="N/A", LowEstimate="N/A", HighEstimate="N/A",
                                 RealizedPrice="N/A", Currency="N/A")
        return LotInfo

    LowEstimate = LotSoup.find("span", class_="range-from")
    if LowEstimate is None:
        LowEstimate = "N/A"
    else:
        LowEstimate = float(LowEstimate['data-range-from'])

    HighEstimate = LotSoup.find("span", class_="range-to")
    if HighEstimate is None:
        HighEstimate = "N/A"
    else:
        HighEstimate = float(HighEstimate['data-range-to'])

    RealizedPrice = LotSoup.find("span", class_="curr-convert")
    if RealizedPrice is None:
        RealizedPrice = "N/A"
    else:
        RealizedPrice = float(RealizedPrice['data-price'])

    Currency = LotSoup.find("div", class_="dropdown currency-dropdown inline")
    if Currency is None:
        Currency = "N/A"
    else:
        Currency = Currency['data-default-currency']

    Artist = LotSoup.find("div", class_="lotdetail-guarantee")
    if Artist is None:
        Artist = "N/A"
    else:
        Artist = Artist.text.split("(")[0].strip()

    Artwork = LotSoup.find("div", class_="lotdetail-subtitle")
    if Artwork is None:
        Artwork = "N/A"
    else:
        Artwork = Artwork.text

    Auction = LotSoup.find("span", class_="active")
    if Auction is None:
        Auction = "N/A"
    else:
        Auction = Auction.text

    Location = LotSoup.find("div", class_="location")
    if Location is None:
        Location = "N/A"
    else:
        Location = Location.text

    Date = LotSoup.find("time", class_="dtstart")
    try:
        Date = re.split("(\d{2} [a-zA-Z]{3,10} \d{4})", Date["datetime"])[1]
    except:
        Date = "N/A"
        pass

    MedExDim = LotSoup.find("div", class_="lotdetail-description-text")
    try:
        ExecutionDate = re.search("(\d{4})", MedExDim.text).group(0)
    except:
        ExecutionDate = "N/A"
        pass

        # Splits the lot detail bit into a list, finds dimensions by filtering with regex. Finds medium from dimensions positions in the list, medium is generally the one before medium.
    try:
        DimMed = re.split("<br\/{0,1}>", str(MedExDim))
        dm = re.compile("\d{0,}.{0,1}\d{0,}\ {0,1}(by){0,1}(x){0,1}\ {0,1}\d{1,}.{0,1}\d{0,}\ {0,1}(cm|mm)")
        Dimension = list(filter(dm.search, DimMed))[0]
        for iCounter in range(0, len(DimMed)):
            if DimMed[iCounter] == Dimension:
                Medium = DimMed[iCounter - 1]
                if Medium == "":
                    Medium = DimMed[iCounter - 2]
                Dimension = Dimension.split(";")[0]
                Medium = re.sub("<div class=\"lotdetail-description-text\">|<p>|</p>", "", Medium).strip()
    except:
        Dimension = "N/A"
        Medium = "N/A"
        pass

    LotInfo = LotInfo.assign(Auction=[Auction], Date=[Date], Location=[Location], Artist=[Artist],
                             ExecutionDate=[ExecutionDate], Artwork=[Artwork], Dimension=[Dimension], Medium=[Medium],
                             LowEstimate=[LowEstimate], HighEstimate=[HighEstimate], RealizedPrice=[RealizedPrice],
                             Currency=[Currency], Source=[LotUrl])
    return (LotInfo)


def sothebys_online_lot_parser(LotUrl):
    LotInfo = pd.DataFrame()

    try:
        LotResponse = requests.get(LotUrl, headers=headers)
        LotSoup = BeautifulSoup(LotResponse.text, 'lxml')
        source = LotSoup.contents[1]
    except:
        LotInfo = LotInfo.assign(Auction="N/A", Date="N/A", Location="N/A", Artist="N/A", ExecutionDate="N/A",
                                 Artwork="N/A", Dimension="N/A", Medium="N/A", LowEstimate="N/A", HighEstimate="N/A",
                                 RealizedPrice="N/A", Currency="N/A")
        return LotInfo

    try:
        high_low_estimates = source.find_all("p", class_="css-1g8ar3q")
        high_low_estimates = high_low_estimates[0].string
        high_low_estimates = re.split("Estimate: | | - ", high_low_estimates)
        low_estimate = high_low_estimates[1].replace(",", "")
        low_estimate = float(low_estimate)
        high_estimate = high_low_estimates[3].replace(",", "")
        high_estimate = float(high_estimate)
    except:
        low_estimate = "N/A"
        high_estimate = "N/A"

    try:
        realized_price = source.find_all("span", class_="css-15o7tlo")
        realized_price = realized_price[0].string.replace(",", "")
        realized_price = float(realized_price)
    except:
        realized_price = "N/A"

    try:
        currency = source.find_all("span", class_="css-wfxyp0")
        currency = currency[0].string
    except:
        currency = "N/A"

    try:
        date = source.find_all("span", class_="css-13r9ds1")
        date = date[0].string.split(" | ")[0]
    except:
        date = "N/A"

    try:
        info = source.find_all("script", type="application/ld+json")
        info = eval(info[0].contents[0])[0]
    except:
        Artist = "N/A"
        Artwork = "N/A"
        Auction = "N/A"
        Dimension = "N/A"
        ExecutionDate = "N/A"
        Medium = "N/A"

    try:
        title = info["mainEntity"]["offers"]["itemOffered"][0]["name"]
        try:
            Artist = title.split(" | ")[0]
        except:
            Artist = "N/A"
        try:
            Artwork = title.split(" | ")[1]
        except:
            Artwork = "N/A"
    except:
        Artist = "N/A"
        Artwork = "N/A"

    try:
        description = info["mainEntity"]["offers"]["itemOffered"][0]["description"]

        dm = re.compile("\d{0,}.{0,1}\d{0,}\ {0,1}(by){0,1}(x){0,1}\ {0,1}\d{1,}.{0,1}\d{0,}\ {0,1}(cm|mm)")
        Dimension = re.search(dm, description)[0]
        ExecutionDate = re.findall("\d{4}", description)[1]
        Medium = re.split("[a-zA-Z]{1,}:" + f"|{ExecutionDate}|{Dimension}", description)[1]
    except:
        Dimension = "N/A"
        ExecutionDate = "N/A"
        Medium = "N/A"

    try:
        Auction = info["breadcrumb"]["itemListElement"][0]["item"]["name"]
    except:
        Auction = "N/A"

    Location = "Online"

    LotInfo = LotInfo.assign(Auction=[Auction], Date=[date], Location=[Location], Artist=[Artist],
                             ExecutionDate=[ExecutionDate], Artwork=[Artwork], Dimension=[Dimension], Medium=[Medium],
                             LowEstimate=[low_estimate], HighEstimate=[high_estimate], RealizedPrice=[realized_price],
                             Currency=[currency], Source=[LotUrl])
    return (LotInfo)


def sothebys_parser(category):
    sothebys_categories = {
        "Contemporary Art": "00000164-609a-d1db-a5e6-e9fffdf80000&f2=00000164-609a-d1db-a5e6-e9fffd2c0000&f2=00000164"
                            "-609b-d1db-a5e6-e9ff01230000&f2=00000164-609a-d1db-a5e6-e9fff6760000",
        "Asian Art": "00000164-609a-d1db-a5e6-e9ffff270000&f2=00000164-609b-d1db-a5e6-e9ff04fc0000&f2=00000164-609a"
                     "-d1db-a5e6-e9fff8ca0000",
        "Impressionist and Modern Art": "00000164-609b-d1db-a5e6-e9ff08ab0000&f2=00000164-609b-d1db-a5e6-e9ff02b50000"
                                        "&f2=00000164-609a-d1db-a5e6-e9fff6150000",
        "All Contemporary": "00000164-609a-d1db-a5e6-e9fffdf80000&f2=00000164-609a-d1db-a5e6-e9fffd2c0000&f2=00000164"
                            "-609b-d1db-a5e6-e9ff01230000&f2=00000164-609a-d1db-a5e6-e9fff6760000&f2=00000164-609b"
                            "-d1db-a5e6-e9ff04fc0000 "
    }

    year_start = 2019
    year_end = 2019
    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                        filename='sothebys_parser.log', level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    logging.info(f"Parsing {category} between {year_start} - {year_end}.")

    quarters = ["1546300800000", "1554076800000", "1561939200000", "1569888000000", "1577836800000"]
    YearQuarter = ["2019Q1", "2019Q2", "2019Q3", "2019Q4"]

    # quarters = [1136073600000, 1143849600000, 1151712000000, 1159660800000, 1167609600000, 1175385600000, 1183248000000, 1191196800000, 1199145600000, 1207008000000, 1214870400000, 1222819200000, 1230768000000, 1238544000000, 1246406400000, 1254355200000, 1262304000000, 1270080000000, 1277942400000, 1285891200000, 1293840000000, 1301616000000, 1309478400000, 1317427200000, 1325376000000, 1333238400000, 1341100800000, 1349049600000, 1356998400000, 1364774400000, 1372636800000, 1380585600000, 1388534400000, 1396310400000, 1404172800000, 1412121600000, 1420070400000, 1427846400000, 1435708800000, 1443657600000, 1451606400000, 1459468800000, 1467331200000, 1475280000000, 1483228800000, 1491004800000, 1498867200000, 1506816000000, 1514764800000, 1522540800000, 1530403200000, 1538352000000, 1546300800000, 1554076800000]
    # YearQuarter = ["2006Q1", "2006Q2", "2006Q3", "2006Q4", "2007Q1", "2007Q2", "2007Q3", "2007Q4", "2008Q1", "2008Q2", "2008Q3", "2008Q4", "2009Q1", "2009Q2", "2009Q3", "2009Q4", "2010Q1", "2010Q2", "2010Q3", "2010Q4", "2011Q1", "2011Q2", "2011Q3", "2011Q4", "2012Q1", "2012Q2", "2012Q3", "2012Q4", "2013Q1", "2013Q2", "2013Q3", "2013Q4", "2014Q1", "2014Q2", "2014Q3", "2014Q4", "2015Q1", "2015Q2", "2015Q3", "2015Q4", "2016Q1", "2016Q2", "2016Q3", "2016Q4", "2017Q1", "2017Q2", "2017Q3", "2017Q4", "2018Q1", "2018Q2", "2018Q3", "2018Q4", "2019Q1"]

    # quarters = ["1569888000000", "1577836800000"]
    # YearQuarter = ["2019Q4"]

    for quarterCounter in tqdm(range(0, len(quarters) - 1)):
        logging.info(f"Started parsing {YearQuarter[quarterCounter]} for {category}")
        url = "https://www.sothebys.com/en/buy/lot-archive?q=&f2=" + sothebys_categories[category] + "&f1=" + \
              str(quarters[quarterCounter]) + "-" + str(quarters[quarterCounter + 1])
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        SearchResults = soup.find("div", class_="SearchModule-count").text.replace(",", "").split(" ")[1]

        logging.info(f"Found {SearchResults} lots for {category} at {YearQuarter[quarterCounter]}")
        NumberOfPages = ceil(int(SearchResults) / 15)

        result = pd.DataFrame()
        for pageCounter in tqdm(range(1, NumberOfPages + 1)):
            nextPage = url + "&p=" + str(pageCounter)

            nextPageResponse = requests.get(nextPage, headers=headers)
            NextPageSoup = BeautifulSoup(nextPageResponse.text, 'html.parser')
            lot_list = NextPageSoup.find_all("div", class_="Card-media")
            lot_list = [lot.contents[1]["href"].replace("https", "http") for lot in lot_list]
            for lot_url in tqdm(lot_list):
                logging.info(lot_url)
                lot_df = sothebys_lot_parser(lot_url)
                na_count = sum(lot_df.unstack().str.count("N/A"))
                if na_count > 5:
                    lot_df = sothebys_online_lot_parser(lot_url.replace("http", "https"))
                result = result.append(lot_df)

                # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                #     print(result)

        result["Category"] = category
        result["AuctionHouse"] = "Sothebys"
        result = result.replace(";", "", regex=True)
        result = result.replace(",", "", regex=True)
        result.to_excel(YearQuarter[quarterCounter] + "Sothebys" + category + ".xlsx", encoding="utf-8-sig",
                        index=False)
        logging.info(f"Finished parsing {YearQuarter[quarterCounter]} for {category}.")

# LotUrl = "https://www.sothebys.com/en/buy/auction/2019/contemporary-art-online/cb8d1573-359d-4c48-913d-aa757dd1d8a9?locale=en"
# lot_url ="https://www.sothebys.com/en/buy/auction/2019/contemporary-art-online/40f1e48f-8ac9-4e41-91b4-ff1773adf368"
# url = "https://www.sothebys.com/en/buy/auction/2019/the-hoarder-sale/bas-van-den-hurk-beatrix-kiddo-1"
# df = sothebys_online_lot_parser(url)
# df_o = sothebys_lot_parser(url)
# na_count = sum(df_o.unstack().str.count("N/A"))
