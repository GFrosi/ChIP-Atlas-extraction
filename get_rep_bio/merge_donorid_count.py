import pandas as pd
import sys




def main():

    df_ca_gsm_gse = pd.read_csv(sys.argv[1]) #csv generated by filter_hs_antigen mammouth (CA_hg38_Hs_GSM_GSE_2022_antigenclass_2022_07_19.csv)
    df_donorid = pd.read_csv(sys.argv[2]) #csv generated by get_bio_rep

    df_merge = df_ca_gsm_gse.merge(df_donorid, how='left', on='GSE')
    
    df_merge.to_csv('../2022_newmetadata/C-A_hg38_Hs_GSM_GSE_2022_antigenclass_2022_07_19_donor_id_combined.csv', index=False)

if __name__ == "__main__":

    main()