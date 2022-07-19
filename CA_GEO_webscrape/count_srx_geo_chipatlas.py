import pandas as pd
import sys


def read_tsv(file_name):
    '''Receives a tab separated 
    file and returns a dataframe'''

    df = pd.read_csv(file_name, sep= "\t")
    
    return(df)


def set_list(geo, chip):
    '''Receives two dataframes 
    (from ChIP-Atlas and GEO) and 
    prints the information
    about the SRX for each one'''

    srx_geo = set(geo['SRX'].tolist())
    srx_chip = set(chip['Experimental_ID'].tolist())
    inters_chip_geo = srx_chip.intersection(srx_geo)

    print('Exploring total samples...')
    print('LEN srx geo:', len(srx_geo))
    print('LEN srx chip:', len(srx_chip))
    print('LEN intersection:', len(inters_chip_geo))
    print('Exploring total samples done!')


def filter_hs(chip, geo):
    '''Receives two dataframes 
    (from ChIP-Atlas and GEO) and 
    returns a filtered dataframe 
    for Homo sapiens and a list of 
    exclusive SRX from ChIP-Atlas'''

    df_chip_hs = chip[chip['Genome_assembly'].str.contains('hg')]
    hs_set = set(df_chip_hs['Experimental_ID'].tolist())
    srx_geo = set(geo['SRX'].tolist())
    inters_chip_geo = hs_set.intersection(srx_geo)
    excl_atlas = list(hs_set - srx_geo)

    print('Exploring Human Atlas samples...')
    print('LEN srx geo:', len(srx_geo))
    print('LEN srx chip:', len(hs_set))
    print('LEN intersection homo sapiens:', len(inters_chip_geo))
    print('Exploring Human Atlas samples done!')
    print('LEN intersection homo sapiens:', len(inters_chip_geo))
    print('Exclusive SRX Homo sapiens from Atlas:', len(excl_atlas))
    print('Returning atlas human dataframe')

    return df_chip_hs, excl_atlas


def write_list(excl_atlas):
    '''Receives a list and returns 
    a txt file'''

    with open('exclusive_atlas.txt', 'w') as output:
        output.write("\n".join(excl_atlas))

    output.close()


def main():

    geo = pd.read_csv(sys.argv[1]) #geo dataframe (exemple: histones of interest)
    chip = read_tsv(sys.argv[2]) #chip atlas dataframe separated by tab. Use first the stand_chip_atlas_fields.py
    # set_list(geo, chip) #to uncoment if you want to see the description of the whole ChIP-Atlas table
    df_chip_hs, excl_atlas = filter_hs(chip, geo)  
    # df_chip_hs.to_csv('chip_atlas_Homosapiens.csv', index=False) #To uncomment if you want save the file 
    write_list(excl_atlas)


if __name__ == "__main__":


    main()