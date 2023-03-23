import pandas as pd
import sys
import json


##Maybe create a uuid key

def create_json(df_ca,out_json):

    df_ca_filter = filter_cols(df_ca)
    json_ca = df_ca_filter.to_dict(orient='records')

    with open(out_json, 'w') as f:
        json.dump({'datasets':json_ca}, f)


def filter_cols(df_ca):

    cols = ['Sample', 'Genome_assembly', 'Antigen_class', 'Antigen',
       'Cell_type_class', 'Cell_type', 'Cell_type_description',
       'Processing_logs', 'Title', 'Metadata', 'age', 'biomaterial_type',
       'cell_line', 'disease', 'disease_ontology_uri', 'donor_health_status',
       'donor_health_status_ontology_uri', 'donor_id',
       'origin_sample_ontology_uri', 'sample_ontology_uri', 'sex', 'sra',
       'tissue_type', 'SRX', 'GSM', 'GSE']

    df_ca_filter = df_ca.loc[:,cols] #good 

    df_ca_filter.rename(columns={'Sample':'md5sum'}, inplace=True) #no duplicates
    df_ca_filter.loc[:,'track_type'] = 'raw' #good
    df_ca_filter['assay_epiclass'] = df_ca_filter.loc[:,'Antigen'].str.lower().replace('input control', 'input')
    df_ca_filter['uuid'] = df_ca_filter.loc[:,'md5sum']
    
    df_ca_filter = df_ca_filter.fillna('')
    df_ca_filter = df_ca_filter.replace('----', '')

    return df_ca_filter


def filter_ca_other_targets(df_ca, to_filter):


    list_filter = to_filter['SRX_filter'].tolist()
    df_ca_filter = df_ca[df_ca['Experimental_ID'].isin(list_filter)]
    df_ca_filter.rename(columns={'Experimental_ID':'Sample', 'SRX_GEO':'SRX'}, inplace=True)
    df_ca_filter.reset_index(drop=True, inplace=True)
    
    return df_ca_filter
    


def main():

    print('Starting...')
    df_ca = pd.read_csv(sys.argv[1], low_memory=False) #path to Histone_CA file (If samples from C-A big table, rename Experimental_ID by Sample; SRX_GEO by SRX)
    out_json = sys.argv[2] #json file name
    create_json(df_ca,out_json)
    print('json saved!')
    
#################################################################
                #special case - filter C-A table
#################################################################    
    # to_filter = pd.read_csv(sys.argv[2], names=['SRX_filter']) #list additional samples
    # df_ca_filter = filter_ca_other_targets(df_ca, to_filter)
    # out_json = sys.argv[3] #json file name
    # create_json(df_ca_filter,out_json)
    # print('json saved!')



if __name__ == '__main__':


    main()


