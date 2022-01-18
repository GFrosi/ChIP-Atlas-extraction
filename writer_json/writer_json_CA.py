import pandas as pd
import argparse


def read_csv(path):
    """load csv file"""
    
    df = pd.read_csv(path)
    
    return(df)


def read_df_header(file_srx):
    """Receives a list of samples (SRX)
    and returns a df with two columns
    (SRX and srx)"""
    
    df = pd.read_csv(file_srx, names=['SRX'], sep='\t')
    df['srx'] = df['SRX'].str.split("-").str[0]
        
    return df


def filter_genome_assembly(df):
    """Receives a df and returns a df
    containing samples of hg38 assembly"""
    
    df1 = df.copy()
    df_hg38 = df1[df1['Genome_assembly'].str.contains('hg38')]
    
    return df_hg38


def create_df_samples(df_srx, df_hg38):
    """Receives two dfs (hg38 and SRX)
    and returns a df containing the 
    desireded samples"""
    
    srx_list = df_srx['srx'].to_list()
    df_filter = df_hg38[df_hg38['Experimental_ID'].isin(srx_list)]
    df_filter = df_filter.astype(str)
    
    return df_filter


def create_dict(df_srx):
    """receives a df and return a dict.
    The key is the SRX and the value is
    srx"""
    
    dict_srx_epig = df_srx.set_index('SRX').to_dict()['srx']
    
    return dict_srx_epig


def print_json(df_result, dict_srx_epig):
    """Receives a filtered df and a dictionary.
    It will print a json file containing the
    metadata."""
    
    print('{"datasets": \n\t[')
    df_len = len(df_result)
    ctn = 0
    
    for index, row in df_result.iterrows(): 
        for key, val in dict_srx_epig.items(): #added to access the keys
            if row['Experimental_ID'] == val:
                fn = key
                target = row['Antigen'].lower()
                cell_type = '""'
                track_type = fn.split('-')[-1]
                if isinstance(row['Cell_type'], str):
                    cell_type = row['Cell_type']
                
                print(f'\t\t{{ "md5sum":"{fn}", "track_type":"{track_type}", "cell_type": "{cell_type}", "assay": "{target}"}}', end="")
                ctn += 1
                if ctn < df_len:
                    print(",")

    print("\n\t]\n}")


def main():

    df_CA = read_csv(args.metadata)
    df_srx = read_df_header(args.srx)
    df_hg38 = filter_genome_assembly(df_CA)
    df_result = create_df_samples(df_srx, df_hg38)
    dict_srx_epig = create_dict(df_srx)
    print_json(df_result, dict_srx_epig)



if __name__ == "__main__":


    parser = argparse.ArgumentParser(
        description="A scrip to print a json file for EpiLaP/epiGeEC from the ChIP-Atlas metadata information"
    )

    parser.add_argument('-m', '--metadata', action="store",
                        help="path to ChIP-Atlas metadata file (csv)",
                        required=True
    )
    
    parser.add_argument('-s', '--srx', action="store",
                        help="path to SRX txt file",
                        required=True
    )



    
    args = parser.parse_args()
    main()