import pandas as pd
import numpy as np
import sys




def main():

    df = pd.read_csv(sys.argv[1]) #file from gdrive including all donor_id combination

    df_filter = df.dropna(subset=['GSE', 'donor_id_unique']).drop_duplicates(subset=['GSE'], keep='first') #float
    # print(df_filter.dtypes)
    df_filter['donor_id_vs_allcombined'] = np.where((df_filter['donor_id_unique'] == df_filter['donor_id_count_categ_comb']), 'True',
    np.where((df_filter['donor_id_unique'] < df_filter['donor_id_count_categ_comb']), 'False Positive', 'False Negative'))

    df_filter['donor_id_vs_no_tissue'] = np.where((df_filter['donor_id_unique'] == df_filter['donor_id_count_categ_comb_ct']), 'True',
    np.where((df_filter['donor_id_unique'] < df_filter['donor_id_count_categ_comb_ct']), 'False Positive', 'False Negative'))

    df_filter['donor_id_vs_no_tissue_no_ct'] = np.where((df_filter['donor_id_unique'] == df_filter['donor_id_count_categ_comb_notissue_ct']), 'True',
    np.where((df_filter['donor_id_unique'] < df_filter['donor_id_count_categ_comb_notissue_ct']), 'False Positive', 'False Negative'))


    df_filter.to_csv('Comparison_donor_id_to_plot.csv', index=False)

if __name__ == '__main__':



    main()