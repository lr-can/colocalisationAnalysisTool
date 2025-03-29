import json
import os
import sys
import argparse
import time
import zipfile

try:
    import requests
except ImportError:
    print("The 'requests' library is not installed. Installing it now...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

class bcolors:
    """
    Just a class to store colors for the terminal.
    """
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKGREY = '\033[90m'
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
        -j, --jobid (str): Job ID for the phaestest analysis.
    """

    parser = argparse.ArgumentParser(description="Run colocalisation analysis tool")
    parser.add_argument('-f', '--file', type=str, help='Input file to run colocalisation analysis on')
    parser.add_argument('-j', '--jobid', type=str, help='Job ID for the analysis')
    return parser.parse_args()

args = parse_arguments()

while True:
    response = requests.get(f"https://phastest.ca/phastest_api?acc={args.jobid}")
    data = response.json()
    
    if data['status'] != "Complete":
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{current_time} - {bcolors.WARNING}Job's status: {data['status']}{bcolors.ENDC}")
        time.sleep(60)  # Wait for 60 seconds before checking again
    else:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{current_time} - {bcolors.OKGREEN}Job's status: {data['status']}{bcolors.ENDC}")
        print(f"{bcolors.OKGREY}{str(data['summary'])[:1870]}{bcolors.ENDC}")
        file_name = os.path.splitext(args.file.split("/")[-1])[0]
        
        # Download the zip file
        zip_response = requests.get("https://" + data['zip'])
        zip_filename = f"./results/results_phastest/{file_name}.zip"
        
        with open(zip_filename, 'wb') as f:
            f.write(zip_response.content)
        
        # Unzip the file
        with zipfile.ZipFile(zip_filename, 'r') as zip_ref:

            zip_ref.extractall(f"./results/results_phastest/{file_name.split('.')[0]}/")
        
        print(f"{bcolors.OKGREEN}Results have been saved in results/results_phastest/{file_name}\n\n you can also view results at https://{data["url"]} {bcolors.ENDC}")
        
        break