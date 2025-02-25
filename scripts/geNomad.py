import subprocess
import sys
import site
import os
site.addsitedir('.venv')

# DefenseFinder installation
def install_geNomad():
    if not os.path.exists('.venv/genomad'):
        try:
            import genomad
            print("genomad is already installed.")
        except ImportError:
            print("genomad not found. Installing...")
            print("Installing non-python dependencies:")
            if not os.path.exists('.venv/bin/mmseqs'):
                MMseq2_install()
            if not os.path.exists('.venv/aragorn'):
                aragorn()
            print("Non-python dependencies have been installed.")
            print("Installing genomad")

            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--target', '.venv', 'genomad'])
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'genomad'])
            print("genomad has been installed.")

def download_geNomad_database():
    if not os.path.exists('genomad_db'):
        print("Downloading genomad database")
        try:
            import genomad
            subprocess.check_call(['genomad', 'download-database','.'])
            print("genomad database has been downloaded.")
        except ImportError:
            print("genomad not found. Please check the installation.")
            sys.exit(1)
    else:
        print("genomad database already exists.")
    

def MMseq2_install():
    print("Installing MMseq2...")
    subprocess.check_call(['wget', 'https://mmseqs.com/latest/mmseqs-linux-avx2.tar.gz'])
    os.makedirs('.venv/bin/mmseqs', exist_ok=True)
    subprocess.check_call(['tar', 'xvfz', 'mmseqs-linux-avx2.tar.gz', '--strip-components=1', '-C', '.venv/bin/mmseqs'])
    subprocess.check_call(['rm', 'mmseqs-linux-avx2.tar.gz'])
    os.environ['PATH'] = os.path.join(os.getcwd(), '.venv/bin') + ':' + os.environ['PATH']
    print("MMseq2 has been installed and added to PATH")

def aragorn():
    print("Downloading ARAGORN")
    subprocess.check_call(['wget', 'https://www.trna.se/ARAGORN/Downloads/aragorn1.2.41.c'])
    subprocess.check_call(['gcc', '-o', '.venv/aragorn', 'aragorn1.2.41.c'])
    subprocess.check_call(['rm', 'aragorn1.2.41.c'])
    os.environ['PATH'] = os.path.join(os.getcwd(), '.venv') + ':' + os.environ['PATH']
    print("ARAGORN has been downloaded, compiled, and added to PATH")
