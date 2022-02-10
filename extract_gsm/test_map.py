import pandas as pd
import sys




def map_gsm(df, file_txt):
    """
    Receives two lists containig the SRX
    and extracted GSM to be mapped into
    df GSM column and the complete metadata 
    df. It will return a complete df including
    the mapped extracted GSM 
    """
    df_gsm_null = df[df['GSM'].isnull()]
    list_srx_null = df_gsm_null['Experimental_ID'].tolist()

    

    dict_gsm = {x:v for x,v in zip(list_srx_null, list_gsm)}
    df_final = df.copy()
    df_final['GSM'] = df_final['Experimental_ID'].map(dict_gsm).fillna(df_final['GSM'])


    df_final.nunique()

    print('checking GSM')
    
    
    # return df_final


def main():
    
    df = pd.read_csv(sys.argv[1])
    file_txt = open(sys.argv[2], 'r')



if __name__ == "__main__":

    

    main()