import pandas as pd
import sys
from tqdm import tqdm
from datetime import datetime



def get_histones(df_merge, df_pred, col_target, col_gse):
    """Receives two dfs (merged - merge_hg38_chip_GEO and 
    df_pred from EpiLaP script), and two col names. Returns
    a df containing samples related to histones of interest
    and inputs"""

    list_hist = ['H3K4me3','H3K4me1','H3K9me3','H3K36me3','H3K27ac','H3K27me3', 'H3K9ac']
    df_hist = df_merge[df_merge[col_target].str.contains('|'.join(list_hist), case=False, na=False)]
    # print(len(df_hist))
    list_gse_hist = list(set(df_hist[col_gse].tolist()))
    df_gse = df_merge[df_merge[col_gse].isin(list_gse_hist)]
    df_input = df_gse[df_gse[col_target].str.contains('Input|WCE|Igg', case=False, na=False)]#change just for input. Map function including list of inputs
    # print(len(df_input))
    set_input = set(df_input[col_target].tolist())
    # print(set_input)
    df_hist_input = pd.concat([df_hist, df_input]) #concatenating hist+inputs
    print(len(df_hist_input),'\n')

    df_hist_input.rename(columns={'Experimental_ID':'Sample'}, inplace=True)
    
    return df_hist_input.merge(df_pred[['Sample', 'Predicted_assay', 'Max_value']], how='left', on='Sample')

    

def merge_hg38_chip_GEO(df_hg38_chip, df_geo, df_gsm_extracted):
    """Receives three dfs, C-A, GEO and a df 
    generated by get_gsm_srx.py. Returns a df
    containing the C-A cols and SRX, GSM and 
    GSE from geo df and mapped GSM from the
    third df"""

    #merging df CA and GEO - get SRX and GSM
    df_merged = df_hg38_chip.merge(df_geo[['SRX', 'GSM', 'GSE']], how='left', left_on='Experimental_ID', right_on='SRX').drop_duplicates(subset=['Experimental_ID'], keep='first')

    #map GSM from CA request using srx - file generated by get_gsm_srx.py (output: write_out/test_0_2021.txt)
    dict_gsm = dict(zip(df_gsm_extracted['SRX'], df_gsm_extracted['GSM'])) #9686
    df_merged['GSM'] = df_merged['Experimental_ID'].map(dict_gsm).fillna(df_merged['GSM'])

    return df_merged
   

def hg38_chipseq(df):
    """Receives a df and returns 
    a df containing hg38 ChIP-Seq
    samples"""

    df_hg38 = get_hg38(df)

    return df_hg38[~df_hg38['Antigen_class'].str.contains('ATAC-Seq|Bisulfite-Seq|DNase-seq', case=False, na=False)]

 
def get_hg38(df):
    """Receives a df (C-A)
    and returns samples related
    to hg38"""
    
    return df[df['Genome_assembly'].str.contains('hg38', case=False, na=False)]


def main():

    print('Starting script...')
    df_ca = pd.read_csv(sys.argv[1], sep='\t') #load experimentList_stand_2022.tsv
    df_geo = pd.read_csv(sys.argv[2]) #load GEO 79k csv file
    df_gsm_extracted = pd.read_csv(sys.argv[3], names=['SRX', 'GSM']) #load write_out/test_0_2021.txt (ChIP-Atlas folder HPC)
    df_pred = pd.read_csv(sys.argv[4]) #test_predict_max_complete.csv (project folder - C-A-EpiLaP total)
    
    date = datetime.now().strftime("%Y_%m_%d")
 
    #Generating dfs of interest
    df_hg38_chip = hg38_chipseq(df_ca) #59805 - Ok
    print('Saving CA_hg38_2022_filter_antigenclass.csv file...')
    df_hg38_chip.to_csv('CA_hg38_2022_filter_antigenclass_'+ date + '.csv', index=False) #path to save the filtered C-A hs ChIP-Seq
    print('Saving C-A_hg38_Hs_GSM_GSE_2022_antigenclass...')
    df_merge = merge_hg38_chip_GEO(df_hg38_chip, df_geo, df_gsm_extracted)
    df_merge.to_csv('CA_hg38_Hs_GSM_GSE_2022_antigenclass_'+ date + '.csv', index=False)
    df_histone_pred = get_histones(df_merge, df_pred, 'Antigen', 'GSE')
    print('Saving Histone_CA_2021-2022_06-07.csv...')
    df_histone_pred.to_csv('Histone_CA_'+ date + '.csv', index=False)
    print('All dfs of interest were saved!')

    




if __name__ == "__main__":



    main()