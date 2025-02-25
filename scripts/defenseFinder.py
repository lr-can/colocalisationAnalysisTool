import subprocess
import sys
import site
import os
site.addsitedir('.venv')
import shutil

base_bin = os.path.join(os.getcwd(), '.venv/bin/')

# DefenseFinder installation
def install_defense_finder():
    try:
        import defense_finder
        print("mdmparis-defense-finder is already installed.")
    except ImportError:
        print("mdmparis-defense-finder not found. Installing...")
        subprocess.check_call(['pip', 'install', '--target', '.venv', 'mdmparis-defense-finder', 'numpy<2.1.0,>=1.26.0', 'markdown<3.4,>=3.2.1'])
        bin_dir = os.path.join('.venv', 'bin')
        for file_name in os.listdir(bin_dir):
            full_file_name = os.path.join(bin_dir, file_name)
            if os.path.isfile(full_file_name):
                shutil.copy(full_file_name, os.path.join('.venv', file_name))

def updateDF():
    try: 
        import defense_finder
        subprocess.check_call(['.venv/defense-finder', 'update'])
    except ImportError:
        print("defense-finder not found. Please check the installation.")
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
        sys.exit(1)