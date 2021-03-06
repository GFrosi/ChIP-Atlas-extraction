import json
import pandas as pd
import sys
from tqdm import tqdm


def write_json(path, list_dset):
    """Write content to json path"""
    
    with open(path, 'w') as f:
        json.dump({"datasets":list_dset}, f)


def create_dict(df_ca, col_v):
    """Receives a df (C-A) and
    a col_name.Returns a dict
    using SRX col as keys and 
    col_v as value"""

    return dict(zip(df_ca['SRX'], df_ca[col_v]))

    
def get_keys(df_ca, merged_json, Sex, Cell_line, Biomaterial_type, Donor_health_status):


    dict_sex = create_dict(df_ca, Sex)
    dict_cell_line = create_dict(df_ca, Cell_line)
    dict_biomaterial = create_dict(df_ca, Biomaterial_type)
    dict_health = create_dict(df_ca, Donor_health_status)

    list_dset = []
    ca_js = json.load(merged_json)

    for dset in tqdm(ca_js['datasets']):
        
        if dset['md5sum'].split('-')[0] in dict_sex.keys(): # all dicts have the same length (keys from SRX col)
            dset['sex'] = str(dict_sex[dset['md5sum'].split('-')[0]]).lower()
            dset['cell_line'] = str(dict_cell_line[dset['md5sum'].split('-')[0]]).lower()
            dset['biomaterial_type'] = str(dict_biomaterial[dset['md5sum'].split('-')[0]]).lower()  
            dset['health_status'] = str(dict_health[dset['md5sum'].split('-')[0]]).lower()  
            list_dset.append(dset)
             
        else:
            dset['cell_line'] = ''
            dset['sex'] = ''
            dset['biomaterial_type'] = ''
            dset['health_status'] = ''
            list_dset.append(dset)
            
    return list_dset


def main():

    print('Starting...')
    df_ca = pd.read_csv(sys.argv[1]) #CA 59k_hs_GSM_GSE df (generated by filter_hs_antigen.py)
    merged_json = open(sys.argv[2]) #merged CA json 
    list_dset = get_keys(df_ca, merged_json, 'Sex', 'Cell_line', 'Biomaterial_type', 'Donor_health_status')
    print('Writing json...')
    write_json('merged_json_newmetadata.json', list_dset)
    print('Json saved!')    

if __name__ == "__main__":



    main()