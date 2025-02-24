import sys
import subprocess
import defenseFinder
import geNomad

subprocess.run(["./activateVenv.sh"], check=True)
defenseFinder.install_defense_finder()
defenseFinder.updateDF()
geNomad.install_geNomad()
geNomad.download_geNomad_database()