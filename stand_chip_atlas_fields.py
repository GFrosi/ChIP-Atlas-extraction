import pandas as pd
import sys
import csv
import json
from tqdm import tqdm


def create_dict(df_new_col):
    """Receives a df containing 
    two cols: All_metadata_cols and 
    Category. Returns a dict where the
    first one is the key, and the second
    one is the value"""

    return dict(zip(df_new_col['All_metadata_cols'], df_new_col['Category']))
    

def set_cols(file):
    """Receives a file and
    returns a csv file containig
    all metadata keys stored in
    the metadata col"""

    list_new_col = []

    for line in file:
        record = line.strip().split('\t')
        r2 = record[9:]
        
        for col in r2:
            list_new_col.append(col.split('=')[0])
    
    list_uniq =  list(set(list_new_col))

    with open('list_unique_cols_CA.csv', 'w') as f:
        f.write("\n".join(list_uniq))
    
    

def main():

    file = open(sys.argv[1], 'r') #experimentList.tab file from ChIP-Atlas git
    df_new_cols = pd.read_csv(sys.argv[2]) #additional_categories_CA_2022.csv file (new columns)
    path = sys.argv[3] #path to save the experiment_List.tsv tab separated file
    
    #Fixed columns
    fixed_cols = ['Experimental_ID', 'Genome_assembly', 'Antigen_class', 'Antigen', 
        'Cell_type_class', 'Cell_type', 'Cell_type_description', 'Processing_logs', 'Title', 'Metadata']

    #creating dict to generate new columns
    dict_cols = create_dict(df_new_cols)

    #list of new columns
    list_new_cols = sorted(list(set(dict_cols.values()))) #set do not guarantee the order

    #list of all desired cols
    res_cols = fixed_cols + list_new_cols
    big_list = []
    extra_cols =  [0,0,0,0,0,0,0,0,0,0,0,0,0] # to change if the number of categories changes

    for line in tqdm(file):
        
        record = line.strip().split('\t')
        r1 = record[:9]
        r2 = record[9:]
        st = '###'.join(r2)
        r1.append(st)
        r1 = r1 + extra_cols #all columns
        big_list.append(r1)

        #updating extra columns
        for col in r2:

            typo = dict_cols.get(col.split('=')[0], '--') #return our desired category if exist in this sample
            
            if typo in list_new_cols:
                index_typo = res_cols.index(typo)
                r1[index_typo] = col.split('=')[1]
            else:
                continue
  
    with open(path, 'w') as out_file:
    
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(res_cols)
        tsv_writer.writerows(big_list)


if __name__ == "__main__":

    main()