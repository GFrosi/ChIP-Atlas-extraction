import pandas as pd
import sys
import csv
from tqdm import tqdm



def main():

    file = open(sys.argv[1], 'r') #experimentList.tab file from ChIP-Atlas git
    path = sys.argv[2] #path to save the experiment_List.tsv tab separated file
    big_list = []
    extra_cols =  [0,0,0,0]
    for line in tqdm(file):
        
        record = line.strip().split('\t')
        r1 = record[:9]
        r2 = record[9:]
        st = '###'.join(r2)
        r1.append(st)
        r1 = r1 + extra_cols
        big_list.append(r1)

        for col in r2:
            if 'sex=' in col.lower():
                r1[10] = col.split('=')[1]
            elif 'cell_line=' in col.lower():
                r1[11] = col.split('=')[1]
            elif 'biomaterial_type=' in col.lower():
                r1[12] = col.split('=')[1]
            elif 'DONOR_HEALTH_STATUS=' in col.upper():
                r1[13] = col.split('=')[1]


    with open(path, 'w') as out_file:
            
        col = ['Experimental_ID', 'Genome_assembly', 'Antigen_class', 'Antigen', 
        'Cell_type_class', 'Cell_type', 'Cell_type_description', 'Processing_logs', 'Title', 'Metadata', 
        'Sex', 'Cell_line', 'Biomaterial_type', 'Donor_health_status']

        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(col)
        tsv_writer.writerows(big_list)


if __name__ == "__main__":

    main()