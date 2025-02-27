import sys
import subprocess
import argparse
import os


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run colocalisation analysis tool")
    parser.add_argument('-f', '--file', type=str, help='Input file to run colocalisation analysis on')
    parser.add_argument('-d', '--directory', type=str, help='Input directory if you want to run on multiple files')
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use for geNomad')
    return parser.parse_args()

args = parse_arguments()


files = []
if args.file and args.directory:
    print("Error: You can't use -f and -d at the same time.")
    sys.exit(1)

if args.directory:
    for filename in os.listdir(args.directory):
        filepath = os.path.join(args.directory, filename)
        if os.path.islink(filepath):
            filepath = os.path.realpath(filepath)
        if ".fa" in filename or ".fasta" in filename:
            files.append(filepath)
elif args.file:
    if os.path.islink(args.file):
        args.file = os.path.realpath(args.file)
    files.append(args.file)

for file_ in files:
    subprocess.check_call(["bash", "./defenseFinder.sh", '-f', file_])
    subprocess.check_call(["bash", "./geNomad.sh"], '-f', file_, '-t', args.threads)

#genomad = geNomad.install_geNomad()
#genomad_db = geNomad.download_geNomad_database()