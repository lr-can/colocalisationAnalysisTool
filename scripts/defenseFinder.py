import subprocess
import sys
import site
site.addsitedir('.venv')

# DefenseFinder installation
def install_defense_finder():
    try:
        import defense_finder
        print("mdmparis-defense-finder is already installed.")
    except ImportError:
        print("mdmparis-defense-finder not found. Installing...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--target', '.venv', 'mdmparis-defense-finder'])
        import defense_finder
