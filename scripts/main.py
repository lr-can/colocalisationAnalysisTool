import sys
import subprocess
import defenseFinder
import geNomad

subprocess.check_call(["bash","./activateVenv.sh"])
defenseFinder.install_defense_finder()
defenseFinder.updateDF()
geNomad.install_geNomad()
geNomad.download_geNomad_database()