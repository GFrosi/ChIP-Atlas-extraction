import pandas as pd
import argparse
import sys
import os
import urllib.request
# import lxml.html as lh
from bs4 import BeautifulSoup
import requests
from time import sleep
from tqdm import tqdm
from retry import retry
from utils.loggerinitializer import *
from distutils.dir_util import mkpath
import csv


mkpath(os.getcwd() + "/logs/")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
initialize_logger(os.getcwd() + "/logs/", logger)



def get_isnull_gsm(df):
    """
    Receives a df including
    columns containing the GSM IDs
    and SRX info. It returns a list
    of SRX for samples without GSM
    info.
    """

    df_gsm_null = df[df['GSM'].isnull()]
    list_srx_null = df_gsm_null['Experimental_ID'].tolist()
    
    return list_srx_null

@retry(TimeoutError, tries=5, delay=3)
def wbs_gsm_gep(df, n, path):
    """
    Receives a df with all metadata
    columns, an integer (default 0)
    to be used to slice a list of 
    SRX and a path for the output
    dir which will store the txt files
    with the SRX and GSM IDs recovered
    by the requests. Returns two lists
    containing the SRX and  extracted GSM
    respectively.
    """

    list_srx_null = get_isnull_gsm(df)
    # list_srx_null = ['DRX000546','SRX6944741','DRX000550']
    list_gsm = []
    root = 'https://www.ncbi.nlm.nih.gov/sra/?term='
    path = os.path.join(os.getcwd(), 'write_out')


    #opening a file in case of the script broke
    myfile = open(os.path.join(path,'test_'+str(n)+'.txt'), 'w')
    writer = csv.writer(myfile, delimiter=',')

    print('Starting requests...')
    for index,i in enumerate(tqdm((list_srx_null[n:]))):
  
        try:
            url = root+i
            page = requests.get(url)
            data = page.text
            soup = BeautifulSoup(data, 'lxml')
            info = soup.find_all('title')
            sleep(4)

            for t in info:
                if 'GSM' in t.get_text():
                    list_gsm.append(t.get_text().split(':')[0])
                    writer.writerow((i,t.get_text().split(':')[0]))

                else:
                    list_gsm.append('----')
                    writer.writerow((i,'----'))

        except ConnectionAbortedError as cae:
            print(f"Error {cae}. You shold restart the program adding the argument --num={index}, srx:{i}. Also, you should use the argument --concat True")
            logger.error("Connection Aborted Error. You shold restart the program adding the argument --num=" + str(index) + "Also, you should use the argument --concat True")
            sys.exit(1)
        
        except ConnectionRefusedError as cre:
            print(f"Error {cre}. Index:{index}, srx: {i}. You maybe was added to a blacklist. Try to run the script adding --num={index}. Also, you should use the argument --concat True" )
            logger.error("Connection Refused Error. You maybe was added to a blacklist. Try to run the script adding --num=" + str(index) + "Also, you should use the argument --concat True")
            sys.exit(1)
    
    print("Requests finished!")

    return list_srx_null, list_gsm


def map_gsm(list_srx_null, list_gsm, df):
    """
    Receives two lists containig the SRX
    and extracted GSM to be mapped into
    df GSM column and the complete metadata 
    df. It will return a complete df including
    the mapped extracted GSM 
    """

    dict_gsm = {x:v for x,v in zip(list_srx_null, list_gsm)}
    df_final = df.copy()
    df_final['GSM'] = df_final['Experimental_ID'].map(dict_gsm).fillna(df_final['GSM'])

    return df_final


def concat_txt(path):
    """
    Receives a path for the
    dir containig txt files
    with SRX and extracted GSM
    information. Returns a complete
    metadata df with the mapped
    extracted GSM.
    """

    files = [os.path.join(path, fname) for fname in os.listdir(path)]

    #concat
    df_test = pd.concat(
    pd.read_csv(os.path.join(path, fname), sep=',', header=None, names=['SRX', 'GSM'])
    for fname in os.listdir(path))

    list_srx_c = df_test['SRX'].tolist()
    list_gsm_c = df_test['GSM'].tolist()

    return list_srx_c, list_gsm_c


def main():

    logger.info("Starting program!")

    df_ca = pd.read_csv(args.df) #df containing at least GSM and SRX (Experimental_ID) columns 

    if args.concat:
        logger.info("Running concat function to generate the final df")
        list_srx_c, list_gsm_c = concat_txt(args.write_out) #generate list of srx and gsm, and call df_final function
        df_final = map_gsm(list_srx_c, list_gsm_c, df_ca)
        df_final.to_csv(args.output, index=False)
        logger.info("Final dataframe generated via concat function saved successfully!")
        print('Final dataframe generated via concat function saved successfully!')
        sys.exit()

    logger.info("Requests running...")
    list_test, list_gsm = wbs_gsm_gep(df_ca, args.num, args.write_out)
    logger.info("Requests finished!")
    df_final = map_gsm(list_test, list_gsm, df_ca)
    df_final.to_csv(args.output, index=False)
    logger.info("Final dataframe generated without connection problems saved successfully!")
    print('Final dataframe generated without connection problems saved successfully!')

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description = 'A script to recover the GSM IDs related with the SRX IDs.'
    )

    parser.add_argument('-d', '--df', action='store',
                        help='The absolute path to the csv file with the metadata information containing at least the GSM and SRX columns',
                        required=True)
    
    parser.add_argument('-n', '--num', action='store',
                        help='The index number from the list of SRX if necessary to run the script again starting by a specific SRX',
                        type=int, default=0, required=False)
    
    parser.add_argument('-c', '--concat',
                        help='The absolute path to the txt files generated in the previous run to be concatenated and mapped into a final df',
                        type=bool, default=False, required=False)

    parser.add_argument('-w', '--write_out', action='store',
                        help='The absolute path to save the txt file if needed',
                        required=True)
    parser.add_argument('-o', '--output', action='store',
                        help='The absolute path to save the final df',
                        required=True)


    args = parser.parse_args()

    main()
