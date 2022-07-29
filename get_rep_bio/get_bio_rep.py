import pandas as pd
import sys
from tqdm import tqdm


def create_df_donor_id_count(df_ca):
    """Receives a df and retuns another
    df containing GSE, number of GSM and 
    number of donor_id"""

    big_list = get_biorep_nodonor(df_ca)
    df = pd.DataFrame(big_list, columns=['GSE', 'donor_id_count_categ_comb_hist', 'gsm_count_categ_comb_hist'])

    df.to_csv('C-A_donorid_notnull_categ_combination_histone.csv', index=False)


def get_biorep_nodonor(df_ca):
    """Receives a df and returns a list of list
    containing the GSE, number of GSM and number
    of donor_id based in a combination of metadata
    for each sample per GSE"""

    df_d_id = df_ca[~df_ca['donor_id'].astype(str).str.match('0')] #just getting the samples with a donor id to compare the results using metadata combination strategy
    gse_list = sorted(list(set(df_d_id['GSE'].dropna().astype(str))))
    # print(len(gse_list))
    big_list = []
    
    for gse in tqdm(gse_list): #so far, so good
        list_info = []   #gse, how many gsm, how many donor_id 
        # print(gse)

        #creating dict to get how many gsm/donor_id per series
        df_test = df_d_id[df_d_id['GSE'].astype(str).str.contains(gse)]
        # print(df_test)
        # sys.exit()
        dict_test = dict([(gsm,[age,bio,cl,disease,health,sex]) for gsm,age,bio,cl,disease,health,sex in
        zip(df_test['GSM'] , df_test['age'].astype(str).str.lower(),
        df_test['biomaterial_type'].astype(str).str.lower(), df_test['cell_line'].astype(str).str.lower(),
        df_test['disease'].astype(str).str.lower(), df_test['donor_health_status'].astype(str).str.lower(),
        df_test['sex'].astype(str).str.lower())]) #order of metadata list

        list_values = dict_test.values() #len dict = number of gsm
        set_values = set(tuple(ele) for ele in list_values) #len set = number of donor_id

        list_info.append(gse)
        list_info.append(len(set_values))
        list_info.append(len(list_values))

        big_list.append(list_info)
    
    return big_list
  

def group_donor_id(df_ca):

    df_donorid_notnul = df_ca[~df_ca['donor_id'].astype(str).str.match('0')]
    df_grouped = df_donorid_notnul.groupby('GSE')['donor_id', 'GSM'].nunique()
    print(df_grouped.nunique())
    # df_grouped.to_csv('C-A_donorid_notnull_histone.csv')


def main():

    print('Starting script...')
    df_ca = pd.read_csv(sys.argv[1]) #C-A csv file (e.g CA_hg38_Hs_GSM_GSE)
    # group_donor_id(df_ca)
    create_df_donor_id_count(df_ca)
    print('Dataframe saved!')



if __name__ == "__main__":

    main()

