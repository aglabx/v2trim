#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: <12.02.2021>
#@author: <Danil Zilov>
#@contact: <zilov.d@gmail.com>

import sys
import argparse
import os
import os.path


def rename(fr, raw_fastq_1):
    if not os.path.exists(fr):
        command = "mv %s %s" % (raw_fastq_1, fr)
        print(command)
        os.system(command)
    assert os.path.exists(fr)

def unzip_n_prepare(file):
    file_name = file.split("/")[-1]
    if file.endswith("_1.fastq"):
        print("Prepare of %s is done!" % file)
        return file
    elif file.endswith("_2.fastq"):
        print("Prepare of %s is done!" % file)
        return file
    else:
        if file.endswith(".tar.gz"):
            command = "tar xfvz %s" % (file)
            print(command)
            os.system(command)
            file = file.replace(".tar.gz", "")
        if file.endswith(".gz"):
            command = "gzip -d %s" % (file)
            print(command)
            os.system(command)
            file = file.replace(".gz", "")
        if "_R1" in file_name:
            file_dir = "/".join(file.split("/")[:-1])
            new_file = file_dir + "/" + file_name.split("_R1")[0] + "_1.fastq"
            command = "mv %s %s" % (file, new_file)
            print(command)
            os.system(command)
            file = new_file
        if "_R2" in file_name:
            file_dir = "/".join(file.split("/")[:-1])
            new_file = file_dir + "/" + file_name.split("_R2")[0] + "_2.fastq"
            command = "mv %s %s" % (file, new_file)
            print(command)
            os.system(command)
            file = new_file
        return unzip_n_prepare(file)
    
def main():
    ''' Function description.
    '''
    EXECUTE_INDEX_BUILDING = False
    
    # Unzipping and preparing file
    
    #checking if files empty
    if os.path.getsize(fr) == 0:
        print(fr + " file is empty!")
        return True
    
    if rr:
        if os.path.getsize(rr) == 0:
            print(rr + " file is empty!")
            return True
        
    raw_fastq_1 = unzip_n_prepare(fr)
    if rr:
        raw_fastq_2 = unzip_n_prepare(rr)
    
    assert raw_fastq_1.endswith("_1.fastq")
    if rr:
        assert raw_fastq_2.endswith("_2.fastq")
    
    
    # Setting parameters
    trim_in_prefix = raw_fastq_1.replace("_1.fastq", "")
    if prefix:
        trim_out_prefix = output_path + "/" + prefix
    else:
        trim_out_prefix = output_path + "/" + raw_fastq_1.replace("_1.fastq", "").split("/")[-1]
    trim_out_file_1 = trim_out_prefix + ".trim_1.fastq"
    trim_out_file_2 = trim_out_prefix + ".trim_2.fastq"
    
    
    #Running v2trim

    command = "./V2_trim.exe %s %s %s %s %s %s" % (trim_in_prefix, trim_out_prefix, threads, "0", "fastq", adapters)
    check_file = os.path.exists(trim_out_file_1)
    if check_file == True:
        if os.path.getsize(trim_out_file_1) > 0:
            print("U've already done Trimming")
            rename(fr, raw_fastq_1)
            if rr:
                rename(rr, raw_fastq_2)
            pass
        else:
            print(command)
            os.system(command)
    else:
        print(command)
        os.system(command)
        
    assert os.path.getsize(trim_out_file_1) > 0
    if rr:
        assert os.path.getsize(trim_out_file_1) > 0
    
    print("\n\nPlease cite us https://github.com/aglabx/v2trim\n\n")
    print("DONE!")
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='v2trim fast and accurate Illumina adapters trimming')
    parser.add_argument('-1','--forward_reads', help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format', required=True)
    parser.add_argument('-2','--reverse_reads', help='Reverse reads file in fastq|fq|gz|tar.gz format', required=False, default="")
    parser.add_argument('-o','--outdir', help='Ouput folder (default = reads filder)', required=False, default= "")
    parser.add_argument('-p','--prefix', help='Output file prefix (default = prefix of original file)', required=False, default="")
    parser.add_argument('-t','--threads', help='Number of threads (default = 8)', required=False, default="8")
    parser.add_argument('-a','--adapters', help='File with adapters (default is /path/to/v2trim/data/illumina_ext.data)', required=False, default="./data/illumina_ext.data")
    
    args = vars(parser.parse_args())
    
    fr = os.path.abspath(args["forward_reads"])
    threads = args["threads"]
    adapters = os.path.abspath(args["adapters"])
    prefix = args["prefix"]
    
    if args["reverse_reads"]:
        rr = os.path.abspath(args["reverse_reads"])
    else: 
        rr = args["reverse_reads"]
        
    if not args["outdir"]:
        output_path = "/".join(fr.split("/")[:-1])
    else: 
        output_path = args["outdir"]
        

    main()