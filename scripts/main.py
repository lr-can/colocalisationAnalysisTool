import sys
import subprocess
import defenseFinder

subprocess.run(["./activateVenv.sh"], check=True)
defenseFinder.install_defense_finder()
