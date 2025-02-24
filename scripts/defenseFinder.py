import subprocess
import sys
import site
import os
site.addsitedir('.venv')

# DefenseFinder installation
def install_defense_finder():
    try:
        import defense_finder
        print("mdmparis-defense-finder is already installed.")
    except ImportError:
        print("mdmparis-defense-finder not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade','--target', '.venv', 'mdmparis-defense-finder'])
        venv_path = os.path.join(os.getcwd(), 'scripts', '.venv', 'defense_finder_cli', 'main.py')
        os.symlink(venv_path, '/usr/local/bin/defense-finder')
        os.chmod('/usr/local/bin/defense-finder', 0o755)
        import defense_finder

def updateDF():
    try: 
        import defense_finder
        subprocess.check_call(['defense-finder', 'update'])
    except ImportError:
        print("defense-finder not found. Please check the installation.")
        subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
        sys.exit(1)