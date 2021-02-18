#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: <12.02.2021>
# @author: <Danil Zilov>
# @contact: <zilov.d@gmail.com>

import argparse
import os
import os.path
import shutil
from inspect import getsourcefile


def check_input_and_output(trim_in_file, trim_out_file, is_endcheck=False):
    # check for input_file
    check_in_file = os.path.exists(trim_in_file)
    if check_in_file:
        if os.path.getsize(trim_in_file) == 0:
            print(trim_in_file + " file is empty!")
            return False
    else:
        print(f"Cannot find {trim_in_file}, please check it.")
        return False
    # check for output_file, returns True if everything is okay
    check_out_file = os.path.exists(trim_out_file)
    if check_out_file:
        if os.path.getsize(trim_out_file) > 0:
            if not is_endcheck:  # if its a check for files before trimming
                answers = 0
                while answers < 5:
                    rerun = input("You've already done Trimming. Do you want to rerun? [y/n]: ")
                    if rerun == "y":
                        os.remove(trim_out_file)
                        return check_input_and_output(trim_in_file, trim_out_file)
                    elif rerun == "n":
                        return False
                    else:
                        answers += 1
                return False
            else:  # if its a check after trimming
                trim_out_dir = os.path.dirname(trim_out_file)
                return f"Trimmed files in {trim_out_dir}"
        else:
            answers = 0
            while answers < 5:
                rerun = input("Output files exists, but they are empty. Do you want to rerun? [y/n]: ")
                if rerun == "y":
                    os.remove(trim_out_file)
                    return check_input_and_output(trim_in_file, trim_out_file)
                elif rerun == "n":
                    return False
                else:
                    answers += 1
            return False
    else:
        return True


def unzip(file_to_unzip):
    if file_to_unzip.endswith(".tar.gz"):
        command = f"tar xfvz {file_to_unzip}"
        print(command)
        os.system(command)
        file_to_unzip = file_to_unzip.replace(".tar.gz", "")
    if file_to_unzip.endswith(".gz"):
        command = f"gzip -d {file_to_unzip}"
        print(command)
        os.system(command)
        file_to_unzip = file_to_unzip.replace(".gz", "")
    if file_to_unzip.endswith(".zip"):
        command = "unzip {file_to_unzip}"
        print(command)
        os.system(command)
        file_to_unzip = file_to_unzip.replace(".zip", "")
    return file_to_unzip


def prepare_in_file(file_path):
    """V2_trim needs specific pattern for input files, function renames input files
    by pattern to make it runnable

    Pattern is - file name must end with "_{1 or 2}.fasta", where {1 or 2} is read direction
    1 - forward read, 2 - reverse read."""

    file_name = os.path.basename(file_path)
    file_dir = os.path.dirname(file_path)
    if file_name.endswith("_1.fastq") or file_name.endswith("_2.fastq"):
        print(f"Prepare of {file_path} is done!")
        return file_path
    elif file_name.endswith(".gz") or file_name.endswith("tar.gz") or file_name.endswith(".zip"):
        print("Your reads are zipped, ples unzip it, or use -u argument to automate unzip before trimming")
        return False

    # define the pattern
    if "_R1" in file_name:
        in_pattern = "_R1"
        out_pattern = "_1.fastq"
    elif "_R2" in file_name:
        in_pattern = "_R2"
        out_pattern = "_2.fastq"
    else:
        print(file_path + " should have '_R1' or '_R2' to run v2trim")
        return False
    # rename by pattern
    while True:
        if file_path.endswith(out_pattern):
            print(f"Prepare of {file_path} is done!")
            break
        else:
            file_prefix = file_name.split(in_pattern)[0]  # prefix without _R1 or _R2
            new_file = os.path.join(file_dir, file_prefix + out_pattern)
            shutil.move(file_path, new_file)
            file_path = new_file
    return file_path


def v2trim_runner(v2trim_exe, trim_in_prefix, trim_out_prefix, threads, adapters_file, mode="fastq", param="0"):
    command = f"{v2trim_exe} {trim_in_prefix} {trim_out_prefix} {threads} {param} {mode} {adapters_file}"
    print(command)
    os.system(command)


def main_pe(settings):
    """Runs v2trim on pair-end reads"""
    # Check up inputs and outputs
    stg = settings
    inputs = [stg["fr"], stg["rr"]]
    outputs = [stg["trim_out_file_1"], stg["trim_out_file_2"]]
    for i in range(len(inputs)):
        check = check_input_and_output(inputs[i], outputs[i])
        if not check:
            return "Input and output files check failed!"

    forward_read = stg["fr"]
    reverse_read = stg["rr"]

    # Unzipping
    if stg["is_to_unzip"]:
        forward_read = unzip(forward_read)
        reverse_read = unzip(reverse_read)

    # Preparing file
    raw_fastq_1 = prepare_in_file(forward_read)
    raw_fastq_2 = prepare_in_file(reverse_read)

    if raw_fastq_1 is False or raw_fastq_2 is False:
        return "Please unzip your reads or use '-u' argument to unzip automatically"

    # Running v2trim
    v2trim_runner(stg["v2trim_exe"], stg["trim_in_prefix"], stg["trim_out_prefix"],
                  stg["threads"], stg["adapters_file"])

    shutil.move(raw_fastq_1, forward_read)
    shutil.move(raw_fastq_2, reverse_read)

    is_endcheck = True

    check_input_and_output(forward_read, trim_out_file_1, is_endcheck=is_endcheck)
    check_input_and_output(reverse_read, trim_out_file_2, is_endcheck=is_endcheck)
    return "Done!"


def main_se(settings):
    """Runs v2trim on single-end reads"""
    # Check up inputs and outputs
    stg = settings
    inputs = [stg["fr"]]
    outputs = [stg["trim_out_file_1"]]
    for i in range(len(inputs)):
        check = check_input_and_output(inputs[i], outputs[i])
        if not check:
            return "Input and output files check failed!"

    forward_read = stg["fr"]

    # Unzipping
    if stg["is_to_unzip"]:
        forward_read = unzip(stg["fr"])

    # Preparing file
    raw_fastq_1 = prepare_in_file(forward_read)

    # Running v2trim
    v2trim_runner(stg["v2trim_exe"], stg["trim_in_prefix"], stg["trim_out_prefix"],
                  stg["threads"], stg["adapters_file"], mode="fastq_se")
    shutil.move(raw_fastq_1, forward_read)

    is_endcheck = True

    check_input_and_output(forward_read, trim_out_file_1, is_endcheck=is_endcheck)
    return "Done!"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='v2trim fast and accurate Illumina adapters trimming')
    parser.add_argument('-1', '--forward_reads', help='Forward reads file (or single-end) in fastq|fq|gz|tar.gz format',
                        required=True)
    parser.add_argument('-2', '--reverse_reads', help='Reverse reads file in fastq|fq|gz|tar.gz format', required=False,
                        default=False)
    parser.add_argument('-o', '--outdir', help='Ouput folder (default = reads folder)', required=False, default=False)
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
    is_to_unzip = args["unzip"]

    if not args["outdir"]:
        output_path = "/".join(fr.split("/")[:-1])
    else:
        output_path = os.path.abspath(args["outdir"])
        if not os.path.exists(output_path):
            os.mkdir(output_path)

    execution_folder = os.path.abspath(getsourcefile(lambda: 0))  # define where the wrapper is executing
    one_folder_down = "/".join(execution_folder.split("/")[:-2])  # prefolder of execution_folder
    v2trim_folder_generator = os.walk(one_folder_down)

    for directory, subdirs, files in v2trim_folder_generator:
        for file in files:
            if "V2_trim.exe" in file:
                v2trim_exe = os.path.join(directory, file)  # define path to V2_trim.exe
            if "illumina_ext.data" in file:
                adapters_file = os.path.join(directory, file)  # define path to V2_trim.exe

    if args["adapters"] != "default":
        adapters_file = os.path.abspath(args["adapters"])

    reads_dir = os.path.dirname(fr)
    fr_name = os.path.basename(fr)
    fr_prefix = fr_name.split("_R1")[0]
    raw_fastq = os.path.join(reads_dir, fr_prefix + "_1.fastq")

    # set up output parameters
    trim_in_prefix = raw_fastq.replace("_1.fastq", "")
    if prefix:
        trim_out_prefix = os.path.join(output_path, prefix)
    else:
        trim_out_prefix = os.path.join(output_path, fr_prefix)
    trim_out_file_1 = trim_out_prefix + ".trim_1.fastq"
    trim_out_file_2 = trim_out_prefix + ".trim_2.fastq"

    settings = {
        "fr": fr,
        "rr": rr,
        "trim_in_prefix": trim_in_prefix,
        "trim_out_prefix": trim_out_prefix,
        "trim_out_file_1": trim_out_file_1,
        "trim_out_file_2": trim_out_file_2,
        "is_to_unzip": is_to_unzip,
        "threads": threads,
        "adapters_file": adapters_file,
        "v2trim_exe": v2trim_exe,
    }

    if rr:
        settings["rr"] = os.path.abspath(rr)
        main_pe(settings)
    else:
        main_se(settings)
    print("\nThanks for using v2trim!\n")
    print("Please cite us https://github.com/aglabx/v2trim\n")

