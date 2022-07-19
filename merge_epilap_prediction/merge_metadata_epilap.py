import pandas as pd
import sys
import glob
from functools import reduce
from datetime import datetime


def histones_ca_2022_pred(df_ca_hist):
    """Receives a df generated
    by filter_hs script (Histone_CA). 
    Returns a Histone_CA merged with 
    all epilap predicted csv files. 
    The csv files should in the same
    directory of this script"""
    
    date = datetime.now().strftime("%Y_%m_%d")
    list_df = [df_ca_hist]

    for df in glob.glob("*.csv"):
        name = df.split('_')[-1].split('.')[0] #getting the model type (sex, bio, assay...)
        name_df = 'df'+name
        df_1 = pd.read_csv(df)
        name_df = create_srx_col(df_1) #generating sample columns to merge dfs
        list_df.append(name_df)
    
    #merging all dfs
    df_merge = reduce(lambda left,rigth: pd.merge(left,rigth, on='Sample',how='left'), list_df)
    
    #saving df
    df_merge.to_csv('Histone_CA_2021-2022_predictions_'+date+'.csv', index=False)


def create_srx_col(df):
    """Return a df containing 
    sample column"""

    df['Sample'] = df['md5sum'].str.split('-').str[0]

    return df


def main():

    df_ca_hist = pd.read_csv(sys.argv[1]) #Histone_CA_2021-2022_06-07.csv (generated by filter_hs.py)
    histones_ca_2022_pred(df_ca_hist)


if __name__ == "__main__":

    main()