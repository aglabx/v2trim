# v2trim fast and accurate Illumina adapters trimming

The preparation of raw data for genome assembly has a high impact on the quality of the further analysis.
Usually, it includes a few steps:
* Raw reads QC
* Filtering of short reads
* Adapters Trimming 
* Optical/PCR duplicates trimming
* Prepared reads QC

There is a lot of tools for adapters trimming. Most of them are doing a great job, but takes a long time or requires many parameters to run. We created v2trim - an user-friendly tool for fast and accurate adapters trimming from raw Illumina sequence reads. It was tested on bacterial and human reads and shows better trimming time and quality of trimmed reads. Benchmark if available from this repository. V2trim is written on C++ and available from Conda.

## Installation
1. From Conda 
`conda install v2trim`
2. From github
`git clone https://github.com/aglabx/v2trim.git`

## Usage
All you need to run v2trim is forward and reverse raw sequence reads. For example you have two files: SRR519926_1.fastq and SRR519926_2.fastq.

To run v2trim enter:
```
./v2trim.exe SRR519926 SRR519926.v2trim 32 0 fastq illumina_ext.data
```
Where:
* **SRR519926** - prefix of input files, without _1.fastq/_2.fastq (may be with path /home/user/raw_reads/SRR519926).
* **SRR519926.v2trim** - output prefix, can be written with output path (for example: /home/user/v2trim_test/SRR519926.v2trim_output)
* **32** - threads 
* **fastq** - output format (<format: reads|fasta|fastq|fastq_se|fastq_raw>)
* **illumina_ext.data** - file with all Illumina adapters 

## Citation

## Copyright Notice

v2trim written by Aleksey Komissarov (ad3002@gmail.com)
Copyright (c) 2020 Aleksey Komissarov. 

This code is licensed under the same GNU General Public License v2
(or at your option, any later version).  See
http://www.gnu.org/licenses/gpl.html
