import urllib
from bs4 import BeautifulSoup
import re
import pandas as pd
from tqdm import tqdm
import logging


def christies_lot_parser(loturl):
    source = urllib.request.urlopen(loturl)
    soup = BeautifulSoup(source, 'lxml')

    try:
        RealizedPrice = soup.find("p", id="main_center_0_lblPriceRealizedPrimary").text.replace(",", "").split(" ")
        Currency = RealizedPrice[0]
        RealizedPrice = float(RealizedPrice[1])
    except:
        RealizedPrice = "N/A"
        Currency = "N/A"
        pass
    try:
        Estimates = soup.find("span", id="main_center_0_lblPriceEstimatedPrimary").text.replace(",", "").split(" ")
        LowEstimate = float(Estimates[1])
        HighEstimate = float(Estimates[4])
    except:
        LowEstimate = "N/A"
        HighEstimate = "N/A"
        pass

    try:
        Artwork = soup.find("h2", id="main_center_0_lblLotSecondaryTitle").text.strip()
    except:
        Artwork = "N/A"
        pass

    try:
        Artist = soup.find("span", id="main_center_0_lblLotPrimaryTitle").text.split("(")[0].strip()
    except:
        Artist = "N/A"
        pass

    try:
        Auction = soup.find("div", id="main_center_0_lblSaleTitle").text
    except:
        Auction = "N/A"
        pass

    try:
        Date = soup.find("p", id="main_center_0_lblSaleDate").text
    except:
        Date = "N/A"
        pass

    try:
        Location = soup.find("p", id="main_center_0_lblSaleLocation").text
    except:
        Location = "N/A"
        pass

    try:
        MedExecDim = re.split("\r|\n", soup.find("span", id="main_center_0_lblLotDescription").text)
        try:
            ExecutionDate = "N/A"
            for k in MedExecDim[1:]:
                ExecutionDate = re.search("\d{4}", k)
                if ExecutionDate is not None:
                    ExecutionDate = ExecutionDate.group(0)
                    break
                else:
                    ExecutionDate = "N/A"
        except:
            ExecutionDate = "N/A"
            pass

        try:
            for iCounter in range(0, len(MedExecDim)):
                Dimension = re.search(
                    "\d{0,}.{0,1}\d{0,}\ {0,1}(by){0,1}(x){0,1}\ {0,1}\d{1,}.{0,1}\d{0,}\ {0,1}(cm|mm)",
                    MedExecDim[iCounter])
                if Dimension is not None:
                    Dimension = Dimension.group(0).replace("(", "")
                    Medium = MedExecDim[iCounter - 2]
                    break
                else:
                    Dimension = "N/A"
                    Medium = "N/A"
        except:
            Dimension = "N/A"
            Medium = "N/A"
            pass
    except:
        ExecutionDate = "N/A"
        Dimension = "N/A"
        Medium = "N/A"
        pass

    LotInfo = pd.DataFrame()
    LotInfo = LotInfo.assign(Auction=[Auction], Date=[Date], Location=[Location], Artist=[Artist],
                             ExecutionDate=[ExecutionDate], Artwork=[Artwork], Dimension=[Dimension], Medium=[Medium],
                             LowEstimate=[LowEstimate], HighEstimate=[HighEstimate], RealizedPrice=[RealizedPrice],
                             Currency=[Currency])
    return LotInfo


def christies_online_lot_parser(loturl):
    source = urllib.request.urlopen(loturl)
    soup = BeautifulSoup(source, 'lxml')

    try:
        RealizedPrice = float(soup.find("meta", property="product:price:amount")["content"]) * 1.25
    except:
        RealizedPrice = "N/A"
        pass

    try:
        Currency = soup.find("meta", property="product:price:currency")["content"]
    except:
        Currency = "N/A"
        pass

    try:
        Estimates = soup.find("div", class_="estimated row").text.replace("\n", "").strip().replace(",", "").split(" ")
        LowEstimate = float(Estimates[2])
        HighEstimate = float(Estimates[5])
    except:
        LowEstimate = "N/A"
        HighEstimate = "N/A"
        pass

    try:
        Artwork = soup.find("meta", property="product:brand")["content"]
    except:
        Artwork = "N/A"
        pass

    try:
        Artist = soup.find("meta", property="og:title")["content"].split("(")[0].strip()
    except:
        Artist = "N/A"
        pass

    try:
        Auction = soup.find("div", class_="col-xs-12 nopadl nopadr title").text.replace("\n", "").strip()
    except:
        Auction = "N/A"
        pass

    try:
        Date = soup.find("span", class_="col-xs-12 col-md-9 nopad").text
    except:
        Date = "N/A"
        pass

    Location = "Online"

    try:
        # MedExecDim = re.split("\r|\n",soup.find("span",id="main_center_0_lblLotDescription").text)
        MedExecDim = str(soup.find("div", class_="lot-notes-row")).split("<br/>")
        try:
            ExecutionDate = "N/A"
            for k in MedExecDim[1:]:
                ExecutionDate = re.search("\d{4}", k)
                if ExecutionDate is not None:
                    ExecutionDate = ExecutionDate.group(0)
                    break
                else:
                    ExecutionDate = "N/A"
        except:
            ExecutionDate = "N/A"
            pass

        try:
            for iCounter in range(0, len(MedExecDim)):
                Dimension = re.search(
                    "(\d{1,}.{0,1}\d{0,} x \d{1,}.{0,1}\d{0,} x \d{1,}.{0,1}\d{0,}\ {0,1}(cm|mm)|\d{1,}.{0,1}\d{0,} x \d{1,}.{0,1}\d{0,}\ {0,1}(cm|mm)|\d{1,}.{0,1}\d{0,2}\ {0,1}(cm|mm))",
                    MedExecDim[iCounter])
                if Dimension is not None:
                    Dimension = Dimension.group(0).replace("(", "")
                    Medium = MedExecDim[iCounter - 1]
                    break
                else:
                    Dimension = "N/A"
                    Medium = "N/A"
        except:
            Dimension = "N/A"
            Medium = "N/A"
            pass
    except:
        ExecutionDate = "N/A"
        Dimension = "N/A"
        Medium = "N/A"
        pass

    LotInfo = pd.DataFrame()
    LotInfo = LotInfo.assign(Auction=[Auction], Date=[Date], Location=[Location], Artist=[Artist],
                             ExecutionDate=[ExecutionDate], Artwork=[Artwork], Dimension=[Dimension], Medium=[Medium],
                             LowEstimate=[LowEstimate], HighEstimate=[HighEstimate], RealizedPrice=[RealizedPrice],
                             Currency=[Currency])
    return LotInfo



def christies_parser(category, year_start, year_end):
    christies_categories = {"Impressionist and Modern": "29|100|99",
                            "Post War Contemporary": "74",
                            "Asian Contemporary": "94|92",
                            "All Contemporary": "98|94|92|74"
                            }

    logging.basicConfig(filename='christies_parser.log', level=logging.INFO)
    logging.info(f"Parsing {category} between {year_start} - {year_end}.")

    for year in range(year_start, year_end + 1):
        for quarter in range(1, 5):
            result = pd.DataFrame()
            for month in range((quarter * 3) - 2, (quarter * 3) + 1):
                logging.info(f"Started parsing {month}/{year}.")
                try:
                    url = 'https://www.christies.com/Results/?' + "&did=" + christies_categories[
                        category] + "&year=" + str(year) + "&month=" + str(month)
                    logging.info(url)
                    source = urllib.request.urlopen(url)
                    soup = BeautifulSoup(source, 'lxml')

                    # Finds the saleid of the auctions in the javascript part of the html.
                    script = soup.find_all("script")
                    sale_ids = re.findall("\"sale_id\"\:\"[0-9]{0,}\"", script[11].string)
                    sale_ids = [re.sub("\"sale_id\"\:|\"", "", sale_id) for sale_id in sale_ids]
                except:
                    logging.warning(f"Could not find auction on {month}/{year}")
                    continue

                number_of_auctions = len(sale_ids)
                logging.info(f"Found {number_of_auctions} auctions at {month}/{year}.")

                for auction in tqdm(range(0, number_of_auctions), desc="Auctions"):
                    # Generates the url for items sold at the auction for given saleid.
                    LotListUrl = "https://www.christies.com/AjaxPages/SaleLanding/DisplayLotList.aspx?pg=all&intsaleid=" \
                                 + sale_ids[auction]

                    # Parses the list of lots for direct urls to lots and uses Christiesparser function to parse lot details.
                    LotSoup = BeautifulSoup(urllib.request.urlopen(LotListUrl), 'lxml')
                    auction_lots = LotSoup.find_all("li",
                                                    class_="col-xs-6 col-sm-6 col-md-6 col-lg-4 filter--lots-wrapper--items")
                    lot_links = [lot_link.find("a")["href"] for lot_link in auction_lots]
                    logging.info(f"Found {len(lot_links)} lots for the auction {sale_ids[auction]} at {month}/{year}.")

                    for lot_link in tqdm(lot_links, desc="Lots"):
                        if not re.findall("online", lot_links[0]):
                            result = result.append(christies_lot_parser(lot_link))
                        else:
                            result = result.append(christies_online_lot_parser(lot_link))

                        # with pd.option_context('display.max_rows', None, 'display.max_columns', None):
                        #    print(result)

                    logging.info(f"Finished {month}/{year}.")

            # Saves the result data frame to excel.
            result = result.replace(";", "", regex=True).replace(",", "", regex=True). \
                replace("\"", "", regex=True).replace("\n", "", regex=True)
            result["Category"] = category
            result["AuctionHouse"] = "Christies"
            result.to_excel(str(year) + "Q" + str(quarter) + "Christies" + category + ".xlsx", encoding="utf-8-sig",
                            index=False)
