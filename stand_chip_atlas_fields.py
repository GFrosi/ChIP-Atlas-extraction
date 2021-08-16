import pandas as pd
import sys
import csv
from tqdm import tqdm



def main():

    file = open(sys.argv[1], 'r') #experimentList.tab file from ChIP-Atlas git
    path = sys.argv[2] #path to save the experiment_List.tsv tab separated file
    big_list = []

    for line in tqdm(file):
        
        record = line.strip().split('\t')
        r1 = record[:9]
        r2 = record[9:]
        st = '###'.join(r2)
        r1.append(st)

        big_list.append(r1)


    with open(path, 'w') as out_file:
            
        col = ['Experimental_ID', 'Genome_assembly', 'Antigen_class', 'Antigen', 'Cell_type_class', 'Cell_type', 'Cell_type_description', 'Processing_logs', 'Title', 'Metadata']
        tsv_writer = csv.writer(out_file, delimiter='\t')
        tsv_writer.writerow(col)
        tsv_writer.writerows(big_list)


if __name__ == "__main__":

    main()