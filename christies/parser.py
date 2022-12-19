from pages import *
from auctions import *
from watch import *



def parse_extract():
    get_watch_list()
    extract_pages()
    parse_watch()
    auctions_join()

def main():
    parse_extract()
    

if __name__=="__main__":
    main()