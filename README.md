# 16S Kraken Pipeline


## About this pipeline
___

This pipeline was written in Python (>=-3.8) uses Kraken2 to search and caracterize OTUs using 16S genes, at genus level, in single read data. 

*Developed by Carlos Henrique Aguiar Costa (carloscostaha@gmail.com)*

## Strategy

Single-end (SE) reads are initially processed with trimmomatic using FASTQC generating quality check reports before and after triming. Then, Remaining reads are processed with Kraken2 and reports in kraken tabular format and metaphlan2 (mpa) format generated.


## Dependencies 

All the below dependecies must be installed in PATH variable of the system. Meeting the specific versions as described below

* trimmomatic (0.38)
* fastqc (0.11.9)

**Note** that KRAKEN2 must be locally installed and set in PATH variable.

* kraken2 (2.3.4.1) --- Please see: [Kraken2 documentation](https://github.com/DerrickWood/kraken2)


## Installation

The installation of ALLMT can be done by cloning the repo inside the destination folder

```
  git clone https://github.com/carloshacosta/16S_kraken_pipeline
  cd /16S_kraken_pipeline
  chmod +x 16S_challenge.py
```
### Installing Dependecies

```
  conda env create -f env/packages.yml
  pip install -r requirements.txt
  conda activate 16S_challenge
```
**Note** Once kraken2 must be installed in the path variable, you must install some of the available database to run analysis. In the exampĺe below we used rdp (Ribosomal Database Project) database

```
kraken2-build --db <kraken2_db_dir> --special rdp

```

## Usage

Once you have the database from `kraken2-build`.

```  
python3  16S_challenge.py --reads <reads.fastq> --kraken_db <kraken2_db_dir>
```

### Merging tables ###

Using the script `combine_mpa.py` from [Jennifer Lu](https://github.com/jenniferlu717) you can merge all the mpa_tables into one unique table.

``` 
python3 combine_mpa.py -i <all_folders>/kraken*/*_genus.txt -o <merged_table.tsv>
``` 


