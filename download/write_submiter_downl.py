import argparse
import sys
import os


def get_files(path_files): #maybe improve to split the big list here, and create a dir to save them
    '''Receives a path with 
    the SRX lists and returns
    a list of file names'''

    list_files = os.listdir(path_files)

    return list_files


def write_sh(path_files, path_out):
    '''Receives a path to the SRX 
    files and the path to the .sh
    outputs. It will write the .sh
    files containing the wget for each
    SRX.'''

    list_files = get_files(path_files)  
    
    for list_srx in list_files:
        file = open(os.path.join(path_files,list_srx), 'r')
        out_name = list_srx + '.sh'
        output = open(os.path.join(path_out,out_name), 'w') 
        command_line = """#!/bin/bash

#SBATCH --time=4-00:00:00
#SBATCH --account=def-jacquesp
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --mail-user=frog2901@usherbrooke.ca
#SBATCH --mail-type=FAIL
#SBATCH --output=%j-%x.slurm
#SBATCH --job-name=""" + out_name + "\n\n"
        
        to_write = command_line

        for line in file:
            line = line.strip()
            srx_bw = line+".bw"
            path_wget = os.path.join("dbarchive.biosciencedbc.jp/kyushu-u/hg38/eachData/bw",srx_bw)
        
            command_wget = "wget " + path_wget + "\n"
            to_write += command_wget

        output.write(to_write)

        output.close()


def main():

    path_files = args.path
    path_out = args.out
    write_sh(path_files,path_out)




if __name__ == "__main__":

    
    parser = argparse.ArgumentParser(

            description = "A tool to write .sh files using SRX list from a specific path to download each sample using wget"

    )
 
    parser.add_argument('-p', '--path', action="store",

                        help='Absolute path to the SRX lists (.txt)',
                        required=True
    )

    parser.add_argument('-o', '--out', action="store",

                        help='Absolute path to .sh outputs',
                        required=True
    )

    args = parser.parse_args()
    main()
