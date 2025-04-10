import sys
import subprocess
import argparse
import os
from datetime import datetime

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
    parser.add_argument('-p', '--phastest', action='store_true', help='Include phastest in the analysis')

    return parser.parse_args()

args = parse_arguments()


files = []
if args.file and args.directory:
    print("Error: You can't use -f and -d at the same time.")
    sys.exit(1)

if args.directory:
    for filename in os.listdir(args.directory):
        filepath = os.path.join(args.directory, filename)
        if os.path.isfile(filepath) and ((".fa" in filename) or (".fasta" in filename) or (".fna" in filename)):
            files.append(filepath)
elif args.file:
    if os.path.isfile(args.file):
        files.append(args.file)

if not args.threads:
    args.threads = 1

print(f"""{bcolors.OKCYAN} Welcome to the colocalisation analysis tool! 
This tool has been developed by a group of Master's students from the Claude Bernard Lyon 1 University, under the supervision of COLUZZI, Charles, and PLANTADY, Clarisse.
{bcolors.ENDC}""")
print(r"""
                   ╫╫
     ╫╫          ╫╫╫╫╫╫          ╫╫
     ╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫╫
     ╫╫          ///////         ╫╫
     ╫╫      ///////////////     ╫╫
     ╫╫    %%%%         0000000  ╫╫
     ╫╫   %%%%    @00//   00000  ╫╫
     ╫╫   %%%%    @@@00   000000 ╫╫                   ╔══════════════════════════════════╗
   ╡╡╫╫  %%%%%%          %%%%%%% ╫╫╞╞                 ║   Colocalization Analysis Tool   ║
 ╡╡╡╡╫╫  @@@@@@      %%%%%%%%%%% ╫╫╞╞╞╞               ║ DefenseFinder, Genomad, Phastest ║
   ╡╡╫╫  @@@@    %%%%%%%%%%%%%%  ╫╫╞╞                 ║ Master's degree in bioinformatics║
     ╫╫   @@   @@@%%%%%%%%%%%%   ╫╫                   ║ University Claude Bernard Lyon 1 ║
     ╫╫       @@@@@@@@@%%%%%%    ╫╫                   ╚══════════════════════════════════╝
     ╫╫        @@@@@@@@@@        ╫╫
     ╫╫╫╫╫╫╫╫╫╫          ╫╫╫╫╫╫╫╫╫╫
     ╫╫      ╫╫╫╫╫   ╫╫╫╫╫╫      ╫╫
                ╫╫╫╫╫╫╫╫
                   ╫╫
      """)
print(f"{bcolors.BOLD} Running colocalisation analysis for {len(files)} file{"s" if len(files) > 1 else ""} {bcolors.ENDC}")
print(f"{bcolors.OKCYAN} Initializing result file and creating the result dir {bcolors.ENDC}")
current_date = datetime.now().strftime("%Y-%m-%d")
current_time = datetime.now().strftime("%H:%M:%S")
subprocess.check_call(["bash", "./scripts/createReport.sh", f"{current_date}_{current_time}"])

for file_ in files:
    print(f"{bcolors.OKBLUE} Running colocalisation analysis on {file_} {bcolors.ENDC}")
    print(f"{bcolors.OKCYAN} Checking file {bcolors.ENDC}")
    subprocess.check_call(["bash", "./scripts/checkFile.sh", file_])
    print(f"{bcolors.OKCYAN} Running defenseFinder.sh {bcolors.ENDC}")
    subprocess.check_call(["bash", "./scripts/defenseFinder.sh", file_])
    print(f"{bcolors.OKCYAN} Running geNomad.sh {bcolors.ENDC}")
    subprocess.check_call(["bash", "./scripts/geNomad.sh", file_, str(args.threads)])
    if args.phastest:
        print(f"{bcolors.OKCYAN} Running phastest.sh {bcolors.ENDC}")
        subprocess.check_call(["bash", "./scripts/phastest.sh", file_])
        print(f"{bcolors.OKGREEN} Phastest finished for {file_} {bcolors.ENDC}")
    print(f"{bcolors.OKGREEN} All analyses finished for {file_} {bcolors.ENDC}")

    print(f"{bcolors.OKCYAN} Merging results for {file_} {bcolors.ENDC}")

    result_finder = "./results/result_Finder/"
    result_genomad = "./results/results_genomad/"
    result_phastest = "./results/results_phastest/" if args.phastest else ""
    file_name = os.path.basename(file_).split(".")[0]

    subprocess.check_call(['bash' , './scripts/merge.sh', result_finder, result_genomad, file_name, result_phastest, f"{current_date}_{current_time}"])
    print(f"{bcolors.OKGREEN} Results merged for {file_} {bcolors.ENDC}")

from scripts.createReport import endReport
endReport(f"{current_date}_{current_time}")
os.remove("./merged_res.csv")
print(f"{bcolors.OKGREEN} All jobs finished! {bcolors.ENDC}")


#genomad = geNomad.install_geNomad()
#genomad_db = geNomad.download_geNomad_database()