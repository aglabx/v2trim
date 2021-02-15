#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: <12.02.2021>
# @author: <Danil Zilov>
# @contact: <zilov.d@gmail.com>

import argparse
import os
import os.path
from inspect import getsourcefile
from os.path import abspath


def check_input_and_output(trim_in_file, trim_out_file):
    # check for input_file
    check_in_file = os.path.exists(trim_in_file)
    if check_in_file:
        if os.path.getsize(trim_in_file) == 0:
            print(trim_in_file + " file is empty!")
            return False
    else:
        print("Cannot find %s, please check it." % trim_in_file)
        return False
    # check for output_file, returns True if everything is okay
    check_out_file = os.path.exists(trim_out_file)
    if check_out_file:
        if os.path.getsize(trim_out_file) > 0:
            rerun = input("U've already done Trimming. Do you want to rerun? [y/n]")
            if rerun == "y":
                remove_output = "rm %s" % trim_out_file
                os.system(remove_output)
                return check_input_and_output(trim_in_file, trim_out_file)
    else:
        return True


def unzip(file):
    if file.endswith(".tar.gz"):
        command = "tar xfvz %s" % file
        print(command)
        os.system(command)
        file = file.replace(".tar.gz", "")
    if file.endswith(".gz"):
        command = "gzip -d %s" % file
        print(command)
        os.system(command)
        file = file.replace(".gz", "")
    if file.endswith(".zip"):
        command = "unzip %s" % file
        print(command)
        os.system(command)
        file = file.replace(".zip", "")
    return file


def prepare(file):
    file_name = file.split("/")[-1]
    if file.endswith(".zip") or file.endswith(".gz") or file.endswith(".tar.gz"):
        return False
    elif file.endswith("_1.fastq"):
        print("Prepare of %s is done!" % file)
        return file
    elif file.endswith("_2.fastq"):
        print("Prepare of %s is done!" % file)
        return file
    else:
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
        return prepare(file)


def v2trim_runner(tool_dir, in_prefix, out_prefix, n_threads, path_to_adapters, mode="fastq", param="0"):
    command = "%s %s %s %s %s %s %s" % (tool_dir, in_prefix, out_prefix,
                                        n_threads, param, mode, path_to_adapters)
    print(command)
    os.system(command)


def rename(file1, file2):
    if not os.path.exists(file2):
        command = "mv %s %s" % (file1, file2)
        print(command)
        os.system(command)
    assert os.path.exists(file2)


def main_pe(forward_read, out_file_1, reverse_read, out_file_2,
            unzip_bool, in_prefix, out_prefix, n_threads, adapters_path):
    """Runs v2trim on pair-end reads"""
    # Check up inputs and outputs
    inputs = [forward_read, reverse_read]
    outputs = [out_file_1, out_file_2]
    for i in range(len(inputs)):
        check = check_input_and_output(inputs[i], outputs[i])
        if not check: 
            return "Input and output files check failed!"

    # Unzipping
    if unzip_bool:
        forward_read = unzip(forward_read)
        reverse_read = unzip(reverse_read)

    # Preparing file
    raw_fastq_1 = prepare(forward_read)
    raw_fastq_2 = prepare(reverse_read)

    if raw_fastq_1 is False or raw_fastq_2 is False:
        return "Please unzip your reads or use '-u' argument to unzip automatically"
    # Running v2trim
    v2trim_runner(v2trim_exe, in_prefix, out_prefix, n_threads, adapters_path)
    rename(raw_fastq_1, forward_read)
    rename(raw_fastq_2, reverse_read)
    
    print("\nOutput is in %s" % output_path)
    print("\n\nPlease cite us https://github.com/aglabx/v2trim\n\n")
    print("DONE!")


def main_se(single_read, out_file_1, unzip_bool, in_prefix, out_prefix, n_threads, adapters_path):
    """Runs v2trim on single-end reads"""
    # Check up inputs and outputs
    inputs = [single_read]
    outputs = [out_file_1]
    for i in range(len(inputs)):
        check = check_input_and_output(inputs[i], outputs[i])
        if not check: 
            return "Input and output files check failed!"

    # Unzipping
    if unzip_bool:
        single_read = unzip(single_read)

    # Preparing file
    raw_fastq_1 = prepare(single_read)

    # Running v2trim
    v2trim_runner(v2trim_exe, in_prefix, out_prefix, n_threads, adapters_path, mode="fastq_se")
    rename(raw_fastq_1, fr)
    
    print("\nOutput is in %s" % output_path)
    print("\n\nPlease cite us https://github.com/aglabx/v2trim\n\n")
    print("DONE!")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='v2trim fast and accurate Illumina adapters trimming')
    parser.add_argument('-1', '--forward_reads', help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format',
                        required=True)
    parser.add_argument('-2', '--reverse_reads', help='Reverse reads file in fastq|fq|gz|tar.gz format', required=False,
                        default=False)
    parser.add_argument('-o', '--outdir', help='Ouput folder (default = reads filder)', required=False, default=False)
    parser.add_argument('-p', '--prefix', help='Output file prefix (default = prefix of original file)', required=False,
                        default=False)
    parser.add_argument('-t', '--threads', help='Number of threads (default = 8)', required=False, default="8")
    parser.add_argument('-a', '--adapters',
                        help='File with adapters (default is /path/to/v2trim/data/illumina_ext.data)', required=False,
                        default="default")
    parser.add_argument('-u', '--unzip', action="store_true",
                        help='Will unzip your files before run (v2trim required unzipped reads)', required=False)

    args = vars(parser.parse_args())
    fr = os.path.abspath(args["forward_reads"])
    rr = args["reverse_reads"]
    threads = args["threads"]
    prefix = args["prefix"]
    unzip_files = args["unzip"]

    if not args["outdir"]:
        output_path = "/".join(fr.split("/")[:-1])
    else:
        output_path = os.path.abspath(args["outdir"])
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    v2trim_dir = "/".join(abspath(getsourcefile(lambda: 0)).split("/")[:-1])
    v2trim_exe = v2trim_dir + "/data/V2_trim.exe"

    if args["adapters"] == "default":
        adapters_file = v2trim_dir + "/data/illumina_ext.data"
    else:
        adapters_file = os.path.abspath(args["adapters"])

    reads_dir = "/".join(fr.split("/")[:-1])
    fr_name = fr.split("/")[-1]
    raw_fastq = reads_dir + "/" + fr_name.split("_R1")[0] + "_1.fastq"

    # set up output parameters
    trim_in_prefix = raw_fastq.replace("_1.fastq", "")
    if prefix:
        trim_out_prefix = output_path + "/" + prefix
    else:
        trim_out_prefix = output_path + "/" + raw_fastq.split("/")[-1].replace("_1.fastq", "")
    trim_out_file_1 = trim_out_prefix + ".trim_1.fastq"
    trim_out_file_2 = trim_out_prefix + ".trim_2.fastq"

    if rr:
        rr = os.path.abspath(rr)
        main_pe(fr, trim_out_file_1, rr, trim_out_file_2, unzip_files, trim_in_prefix, trim_out_prefix, threads, adapters_file)
    else:
        main_se(fr, trim_out_file_1, unzip_files, trim_in_prefix, trim_out_prefix, threads, adapters_file)
