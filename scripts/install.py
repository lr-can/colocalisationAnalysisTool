import subprocess
import sys
import os

subprocess.check_call(["bash","./scripts/activateVenv.sh"])
conda_path = subprocess.run(["which", "conda"], capture_output=True, text=True).stdout.strip()
if not conda_path:
    print("Conda has just been installed, please restart your terminal")
    sys.exit(1)
subprocess.check_call(["bash", "./scripts/checkOrInstall.sh"])