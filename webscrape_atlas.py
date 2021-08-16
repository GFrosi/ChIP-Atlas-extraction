import pandas as pd
import os
import sys
import urllib.request
import lxml.html as lh
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm 



def create_url_from_file(list_srx):

    '''This function receives a list of SRX and return a list of url for each one'''

    url_list = []
    root = "http://chip-atlas.org/view?id="
    
    for line in list_srx:

        line = line.strip()
        # url_path = os.path.join(root, line)
        url_path = root+line
        url_list.append(url_path)
    
    return(url_list)



def get_library(url_list):

    
    output = open('srx_library_atlas_test.txt', 'w')


    for adrs in tqdm(url_list):

        page = requests.get(adrs)
        sleep(2)
        data = page.text

        soup = BeautifulSoup(data, 'lxml')

        # info = soup.findAll('dl', attrs={'class':'dl-horizontal'}) 
        info = soup.findAll('dt')
    
        for ele in info:

            # if 'library_strategy' in ele.text.strip():
            if ele.text.strip() == 'library_strategy':
            # if ele.get_text() == 'library_strategy':

                # library = ele.find_next_sibling('dd')
                library = ele.findNext("dd")
                
                srx = adrs.split('=')[-1]

                to_write = srx+','+library.text+"\n"
                
                output.write(to_write)


def main():

    list_srx = open(sys.argv[1], 'r')
    url_list = create_url_from_file(list_srx)
    # print(url_list)
    get_library(url_list)




if __name__ == "__main__":



    main()