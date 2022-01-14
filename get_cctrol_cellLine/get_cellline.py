import argparse
import pandas as pd


def organize_df(df):
    '''receives a df
    and returns a df
    without SRX duplicates'''
    
    df1 = df.copy()
    df1 = df1.drop_duplicates(subset=['Experimental_ID'], keep='last').drop(columns=['Unnamed: 0'], axis=1)
 
    return df1
 
def filter_df_srx(df, srx):
    '''receives a list of srx
    of interest and a df with 
    metadata and returns a filtered
    df and input df'''
 
    df1 = organize_df(df)
    list_srx = [line.strip() for line in srx]
    df_filter = df1[df1['Experimental_ID'].isin(list_srx)]

    return df_filter


def filter_input(df):
    '''receives a list of srx   
    of interest and a df with 
    metadata and returns a filtered
    df and input df'''
    
    df1 = organize_df(df)
    df_input = df1[df1['Antigen'].str.contains('Input', case=False, na=False)]

    return df_input


def create_dict(df, col1, col2):
    '''receives a df and the col
    names to return a dict'''

    dict_ct = dict(zip(df[col1], df[col2]))

    if len(dict_ct) != len(df):
        print(f'Warning: the dict length {len(dict_ct)} and df length {len(df)} are different!')

    else:
        pass

    return dict_ct


def create_dict_ip_cctrol(dict1, dict2):
    """Receives two dicts and returns
    a new dict where the keys are SRX 
    (IPs), and the values are lists of 
    suggested inputs"""

    new_dict = {}
    for k,v in dict1.items():
        for k2,v2 in dict2.items():
            if v == v2:
                if k not in new_dict.keys():
                    new_dict[k] = [k2]
                else:
                    new_dict[k].append(k2)
                
        if k not in new_dict.keys():
            new_dict[k] = ['None']

    return new_dict


def create_df(dict1, dict2):
    """Receives two dicts (IPs
    and suggested cctrols) and 
    returns a df with two columns:
    SRX (IPs) and Corresponding_control
    """

    new_dict = create_dict_ip_cctrol(dict1, dict2) 
    list_srx = list(new_dict.keys())
    list_cctrl = list(new_dict.values())
    df_final = pd.DataFrame(list(zip(list_srx, list_cctrl)), columns=['SRX', 'Corresponding_control']) 
    df_final['Corresponding_control'] = df_final['Corresponding_control'].str.join(',') #converting list values to strings
    
    return df_final


def main():

    srx_f = open(args.file, 'r')
    df_CA = pd.read_csv(args.dataframe)
    df_filter = filter_df_srx(df_CA, srx_f)
    df_input = filter_input(df_CA)
    dict_srx = create_dict(df_filter, 'Experimental_ID', 'Cell_type') #IP
    dict_input = create_dict(df_input, 'Experimental_ID', 'Cell_type') #inputs
    df_final = create_df(dict_srx, dict_input)
    df_final.to_csv(args.out, index=False)
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="a script to select inputs related with the same cell line"
    )
    parser.add_argument('-f', '--file', action="store", help='list of SRX of interest', required=True)
    parser.add_argument('-d', '--dataframe', action="store", help='ChIP-Atlas metadata filtered by Homo sapiens', required=True)
    parser.add_argument('-o', '--out', action="store", help='Path to save the csv file', required=True)


    args = parser.parse_args()
    
    main()