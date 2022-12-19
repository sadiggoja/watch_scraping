from pages import *
from auctions import *
from watch import *



def parse_extract():
    
    print("Give number of auctions you want\n0(zero) for all\n")
    max=int(input())

    get_watch_urls(max)
    extract_pages()
    parse_watch()

def main():
    parse_extract()
    

if __name__=="__main__":
    main()