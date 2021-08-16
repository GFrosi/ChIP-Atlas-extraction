#!/bin/bash
#SBATCH --time=00:20:00  
#SBATCH --account=
#SBATCH --cpus-per-task=24
#SBATCH --mem=31G
#SBATCH --mail-user=
#SBATCH --mail-type=FAIL
#SBATCH --job-name=chipatlas

module load python/3.7
virtualenv --no-download $SLURM_TMPDIR/env
source $SLURM_TMPDIR/env/bin/activate
pip install --no-index --upgrade pip

pip install --no-index -r requirements.txt

echo "Starting"

# python chip_atlas_parse.py -h 
python chip_atlas_parse.py -f experimentList_stand.tsv -F GEO_metadata_NGS_updated_08-21-inputfirst_mammouth.csv -o geo_ngs_chipatlas_input_first_08-21.tsv

echo "Done"
