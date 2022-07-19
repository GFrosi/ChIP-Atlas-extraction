#!/bin/bash
#SBATCH --time=24:00:00  
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

python stand_chip_atlas_fields.py experimentList.tab experimentList_stand.tsv

echo "Done"
