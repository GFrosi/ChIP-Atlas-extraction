# ChIP-Atlas-extraction
A script to extract the ChIP-Atlas metadata and compare with GEO metadata (ChIP-Seq and Human metadata)

# Requiremets

```python > 3.0``` and ```create a env with requirements.txt```

## stand_chip_atlas_fields.py

### Usage

```
Stand experimentList.tab to tab separated file
python stand_chip_atlas_fields.py experimentList.tab experimentList.tsv
```

## chip_atlas_parse.py

### Usage

```
Merge dataframes

usage: chip_atlas_parse.py [-h] -f FILE -F FILE -o OUT

a script to merge two dataframes keeping all rows

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  first csv file to be loaded. This file will be the
                        major df to the merge command
  -F FILE, --FILE FILE  second csv file to be loaded and merged with the first
                        one
  -o OUT, --out OUT     Path to save the merged csv file with the new columns
```

## count_srx_geo_chipatlas.py

### Usage

```
Get exclusive ChIP-Atlas SRX

python count_srx_geo_chipatlas.py geo_metadata.csv experimentList.tsv
```


## get_hg19_hg38.py

### Usage

```
Check if each sample has a bigwig for each assembly (hg38 and hg19). These information it will be added into new columns in the final dataframe.

python get_hg19_hg38.py experimentList_stand.tsv GEodiff_nodiff_2021_merged_histones_EpiLaP.tsv output.tsv
```