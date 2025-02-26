import sys
import subprocess
import defenseFinder
import geNomad

subprocess.check_call(["bash","./activateVenv.sh"])
conda_path = subprocess.run(["which", "conda"], capture_output=True, text=True).stdout.strip()
if not conda_path:
    print("Conda has just been installed, please restart your terminal")
    sys.exit(1)
subprocess.check_call(["bash", "./checkOrInstall.sh"])
subprocess.check_call(["bash", "./defenseFinder.sh"])
#genomad = geNomad.install_geNomad()
#genomad_db = geNomad.download_geNomad_database()
subprocess.check_call(["bash", "./geNomad.sh"])