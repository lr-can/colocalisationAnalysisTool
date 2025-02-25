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
        if shutil.which('hmmsearch') is None:
            print("hmmsearch not found. Installing...")
            subprocess.check_call(['wget', 'http://eddylab.org/software/hmmer/hmmer.tar.gz'])
            subprocess.check_call(['tar', 'zxf', 'hmmer.tar.gz'])
            os.chdir('hmmer-3.4')
            subprocess.check_call(['./configure', '--prefix', os.path.join(os.getcwd(), '.venv')])
            subprocess.check_call(['make'])
            subprocess.check_call(['make', 'check'])
            subprocess.check_call(['make', 'install'])
            os.chdir('easel')
            subprocess.check_call(['make', 'install'])
            os.chdir('../..')
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