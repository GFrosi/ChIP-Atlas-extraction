import pandas as pd
import sys
import argparse 




def read_tsv(file_name):
    '''Receives a tab separated 
    file and returns a dataframe'''

    df = pd.read_csv(file_name, sep= "\t")
    
    return(df)


def rename_col(df, col_ori, col_final):
    '''Receives a dataframe, and two columns 
    name (name to be replaced and desired name). 
    Returns a copy of the original dataframe with 
    the desired column name.'''
    
    df1 = df.copy()
    df1.rename(columns={col_ori: col_final}, inplace=True)

    return df1


def drop_replicates(df1):
    '''receives a df and 
    returns a df without
    duplicates'''

    df2 = df1.drop_duplicates(subset='SRX', keep="last")

    return df2


def merge_dfs(df_geo, df2):
    '''This function receives two dataframes 
    and returns a merged dataframe will all 
    rows (by left df)'''

    df_merged = df_geo.merge(df2,how='left', left_on='SRX', right_on='SRX')
    
    return df_merged


def select_cols(df_merge):
    '''receives a df and returns 
    a filterd df by columns'''


    col = ['Release-Date', 'Organism', 'Library_strategy', 'GPL',
       'GPL_title', 'GSE', 'GSE_title', 'GSM', 'GSM_title',
       'chip_antib_catalog', 'Target', 'Cell_line', 'Cell_type_x',
       'Source_cell', 'Target-interest', 'CL-target', 'Target-GEO',
       'Target-NGS-QC', 'Antigen','Address', 'SRX', 'SRR', 'SRR_Count'
       ]
    
    df_filt = df_merge[col]

    return(df_filt)


def save_df(df, path):
    '''Save df as csv file'''
    
    df.to_csv(path, index=False)


def main():
    
    df = read_tsv(args.file) #chipatlas
    df_geo = pd.read_csv(args.FILE) #geo from geo-metadata
    df1 = rename_col(df, "Experimental_ID", "SRX")
    df2 = drop_replicates(df1)
    df_merge = merge_dfs(df_geo, df2)
    df_filt = select_cols(df_merge)
    df_merge_renamed = rename_col(df_filt, "Antigen", "Target-ChiP-Atlas")
    # print(df_merge_renamed)
    save_df(df_merge_renamed, args.out)

    

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="a script to merge two dataframes keeping all rows"
    )

    parser.add_argument('-f', '--file', action="store", help='first csv file to be loaded. This file will be the major df to the merge command', required=True)
    parser.add_argument('-F', '--FILE', action="store", help='second csv file to be loaded and merged with the first one', required=True)
    parser.add_argument('-o', '--out', action="store", help='Path to save the merged csv file with the new columns', required=True)


    args = parser.parse_args()

    main()
