import pandas as pd
import sys


def read_tsv(file_n):
    '''Receivs a file
    separated by tab 
    and return a df'''

    df = pd.read_csv(file_n, sep='\t')

    return df


def get_list_srx(df_histone):
    '''Receives a df and returns
     a list'''

    srx_list = df_histone['SRX'].tolist()

    return srx_list

    
def get_hg19_hg38(file_n_chip, list_srx):
    '''receives a file (ChIP-Atlas separated
    by tab) and a list. Returns two lists with
    yes or no (one for each assembly)'''

    file_assemble = open(file_n_chip, 'r')
    list_hg19 = []
    list_hg38 = []
    dict_exp_table = {}

    for line in file_assemble:
        record = line.split('\t')
        dict_exp_table[record[0]+"_"+record[1]] = 1


    for ele in list_srx:
        if dict_exp_table.get(ele +"_"+"hg19") is not None:
            list_hg19.append('yes')
            
        if dict_exp_table.get(ele +"_"+"hg38") is not None:
            list_hg38.append('yes')
            
        else:
            list_hg19.append('NA')
            list_hg38.append('NA')
        
    
    return list_hg19, list_hg38
   

def add_cols(df_histone, list_hg19, list_hg38):
    '''Receives a df and two lists. Returns a 
    df with the new two columns'''
    
    df_final = df_histone.copy()
    df_final['ChIP_hg19'] = list_hg19
    df_final['ChIP_hg38'] = list_hg38

    return df_final


def main():


    file_n_chip = (sys.argv[1]) #path to the ChiP-Atlas file (experimentList_stand.tsv)
    file_n_geo = sys.argv[2] #path to the GEO metadata table (e.g GEodiff_nodiff_2021_merged_histones_EpiLaP.tsv)
    df_histone = read_tsv(file_n_geo)
    list_srx = get_list_srx(df_histone)
    list_hg19, list_hg38 = get_hg19_hg38(file_n_chip, list_srx)
    df_final = add_cols(df_histone, list_hg19, list_hg38)
    df_final.to_csv(sys.argv[3]) #path to the output file



    



if __name__ == "__main__":



    main()