import pandas as pd
import sys
from tqdm import tqdm



def create_df_donor_id_count(df_ca):
    """Receives a df and retuns another
    df containing GSE, number of GSM and 
    number of donor_id"""

    big_list = get_rep(df_ca)
    df = pd.DataFrame(big_list, columns=['GSE', 'donor_id_count', 'gsm_count'])
    
    df_final = df_ca.merge(df, how='left', on='GSE')

    #saving dfs
    df.to_csv('C-A_rep_bio_C-A_2022_07_19.csv', index=False)
    df_final.to_csv('C-A_2021-2022_predictions_2022_07_19_rep_bio_gsm.csv', index=False)


def get_rep(df_ca):
    """Recieves a df containing a GSE
    column. Return a big list the number
    of bio replicates and GSM per GSE"""

    gse_list = sorted(list(set(df_ca['GSE'].dropna().astype(str))))
    print(f'Your df has {len(gse_list)} GSEs to be analyzed.')
   
    big_list = []


    for gse in tqdm(gse_list): #so far, so good
        list_info = []   #gse, how many gsm, how many donor_id 

        #creating dict to get how many gsm/donor_id per series
        df_test = df_ca[df_ca['GSE'].astype(str).str.contains(gse)]

        if len(df_test[df_test['donor_id'].astype(str).str.match('0')]) > 0:
            
            dict_test = dict([(gsm,[age,bio,cl,disease,health,sex]) for gsm,age,bio,cl,disease,health,sex in
            zip(df_test['GSM'] , df_test['age'].astype(str).str.lower(),
            df_test['biomaterial_type'].astype(str).str.lower(), df_test['cell_line'].astype(str).str.lower(),
            df_test['disease'].astype(str).str.lower(), df_test['donor_health_status'].astype(str).str.lower(),
            df_test['sex'].astype(str).str.lower())]) #order of metadata list
            
            list_values = dict_test.values() #len dict = number of gsm
            set_values = set(tuple(ele) for ele in list_values) #len set = number of donor_id
            
            #Append gse, number of bio_rep and number of GSM per series
            list_info.append(gse)
            list_info.append(len(set_values))
            list_info.append(len(list_values))

            big_list.append(list_info)


        else: #all GSMs have a donor_id info for this GSE

            df_grouped = df_test.groupby('GSE')['donor_id', 'GSM'].nunique().reset_index()
           
            list_info.append(gse)
            list_info.extend(df_grouped['donor_id'].tolist())
            list_info.extend(df_grouped['GSM'].tolist())

            big_list.append(list_info)
        

    return big_list



def main():

    print('Starting script...')

    df_ca = pd.read_csv(sys.argv[1]) #C-A csv file (e.g CA_hg38_Hs_GSM_GSE), 
    create_df_donor_id_count(df_ca)

    print('Dataframe saved!')



if __name__ == "__main__":

    main()
