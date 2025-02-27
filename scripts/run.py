import sys
import subprocess
import argparse
import os

class bcolors:
    """
    Just a class to store colors for the terminal.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def parse_arguments():
    """
    Parses command-line arguments for the colocalisation analysis tool.
    Returns:
        argparse.Namespace: Parsed command-line arguments.
    Arguments:
        -f, --file (str): Input file to run colocalisation analysis on.
        -d, --directory (str): Input directory if you want to run on multiple files.
        -t, --threads (int): Number of threads to use for geNomad.
    """

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

if not args.threads:
    args.threads = 4

print(f"""{bcolors.OKCYAN} Welcome to the colocalisation analysis tool! 
This tool has been developed by a group of Master's students from the Claude Bernard Lyon 1 University, under the supervision of COLUZZI, Charles, and PLANTADY, Clarisse.
{bcolors.ENDC}""")
print(f"{bcolors.BOLD} Running colocalisation analysis for {len(files)} file{"s" if len(files) > 1 else ""} {bcolors.ENDC}")
for file_ in files:
    print(f"{bcolors.OKBLUE} Running colocalisation analysis on {file_} {bcolors.ENDC}")
    print(f"{bcolors.OKCYAN} Running defenseFinder.sh {bcolors.ENDC}")
    subprocess.check_call(["bash", "./defenseFinder.sh", file_])
    print(f"{bcolors.OKCYAN} Running geNomad.sh {bcolors.ENDC}")
    subprocess.check_call(["bash", "./geNomad.sh", file_, str(args.threads)])
    print(f"{bcolors.OKGREEN} Colocalisation analysis finished for {file_} {bcolors.ENDC}")

#genomad = geNomad.install_geNomad()
#genomad_db = geNomad.download_geNomad_database()