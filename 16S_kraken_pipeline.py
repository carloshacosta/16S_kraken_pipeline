#!\usr\bin\python3

import sys
import os
import shutil
import re

import argparse

#16S pipeline challenge --- quality check, trimming, assembly and OTU metagenomic identification with Kraken2.

parser = argparse.ArgumentParser(description='16S metagenomic identification pipeline', usage = '%(prog)s -reads [reads.fastq] -o [output_folder]', epilog="Version: 1.0 Developed by: Carlos H. A. Costa - email: carloscostaha@gmail.com")

#Mandatory options
requiredNamed = parser.add_argument_group('Mandatory arguments')
requiredNamed.add_argument('-r', '--reads', type = str, required = True, metavar = "", help = "FASTQ file containing all the raw reads")
requiredNamed.add_argument('-o', '--output_folder', type = str, required = False, metavar = "", help = "Output Folder Name")
requiredNamed.add_argument('-db', '--kraken_db', type = str, required = True, metavar = "", help = "Kraken2 database pre-built")


args = parser.parse_args()

#Controling the output folder creation for all analysis

if not args.output_folder:
    attempt = 1
    path = args.reads.split("/")
    path_partial = path[-1].split("_")
    folder = "_".join(path_partial[0:2])
    while os.path.exists(folder) and os.path.isdir(folder):
        folder = "_".join(path_partial[0:2])
        overwrite = input(f"Folder {folder} exists. Do you want overwrite it? (Y/N):\n")
        if overwrite in ["N", "n", "NO", "no", "No"]:
            folder = folder + "_" + str(attempt) #
            attempt += 1
        else:
            shutil.rmtree(folder)
            os.mkdir(folder)
            break
    else:
        os.mkdir(folder)

#Building all the subsequential subdirectories
print(f"--- Starting processing sample: {args.reads} ---\n")
subdir = ["fastqc_before", "fastqc_after", "trimmed_reads", "kraken_output"]
for dir in subdir:
    create = f"{folder}/{dir}"
    os.mkdir(create)

#Using FASTQC for all initial analysis
print("1)   Starting raw reads quality check - FASTQC")
fastqc = f"fastqc {args.reads} -q -o {folder}/fastqc_before"
os.system(fastqc)

#Running trimmomatic to filter all the reads using

print("2)   Starting triming step with TRIMMOMATIC")
#Trimommatic Adapter Path#
path = os.path.abspath(__file__)
script_path = path.split("/")
script_path_partial = "/".join(script_path[0:-1])
adapter = script_path_partial + "/trimmomatic_adapters/TruSeq3-SE.fa"

#Running trimmomatic 0.39 for SE reads
trimmomatic = f'trimmomatic SE -phred33 -quiet {args.reads} {folder}/trimmed_reads/output_trimmomatic.fastq ILLUMINACLIP:'+f'{adapter}'+':2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:20 HEADCROP:20 MINLEN:36 SLIDINGWINDOW:4:20 LEADING:3 TRAILING:3 HEADCROP:20 MINLEN:35'
os.system(trimmomatic)

#Re-running FASTQC for trimmed reads
print("3)   Starting trimmed reads quality check - FASTQC")
fastqc2 = f"fastqc {folder}/trimmed_reads/output_trimmomatic.fastq -q -o {folder}/fastqc_after"
os.system(fastqc2)

#Running metaphlan3 taxonomic profiler

print("4)   Starting OTU designation of reads - kraken2\n")

kraken = f'kraken2 {args.reads} --db {args.kraken_db} --use-names --use-mpa-style --report {folder}/kraken_output/{folder}_kraken_mpa.txt --output {folder}/kraken_output/{folder}_kraken.txt 2> /dev/null'

os.system(kraken)
#Writing a new subtable using KRAKEN2 MPA output

genus_table =  open(f'{folder}/kraken_output/{folder}_kraken_mpa_genus.txt', 'w')

header = f"#Kraken2\t{folder}\n"
genus_table.write(header)

with open(f'{folder}/kraken_output/{folder}_kraken_mpa.txt', 'r') as mpa:
    for n in mpa:
        if "g__" in n:
            genus_table.write(n)

genus_table.close()

exit()