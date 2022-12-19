from pages import *
from auctions import *
from watch import *



def parse_extract():

    print("Give number of auctions you want\n0(zero) for all\n")
    max=int(input())

    watch_url_list=get_watch_list(max)
    
    extract_pages(watch_url_list)

    watches=parse_watch(watch_url_list)
    
    pd.DataFrame(watches).to_csv("watches.csv", index=False)

def main():
    parse_extract()
    

if __name__=="__main__":
    main()