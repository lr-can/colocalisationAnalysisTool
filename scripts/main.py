import sys
import subprocess
import defenseFinder
import geNomad

subprocess.check_call(["bash","./activateVenv.sh"])
subprocess.check_call(["bash", "./checkOrInstall.sh"])
subprocess.check_call(["bash", "./defenseFinder.sh"])
genomad = geNomad.install_geNomad()
genomad_db = geNomad.download_geNomad_database()