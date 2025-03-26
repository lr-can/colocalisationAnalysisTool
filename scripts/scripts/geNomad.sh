#!/bin/bash

file_=$1
threads=$2

filename=$(basename -- "$file_")
filename="${filename%%.*}"

# Initialize conda
eval "$(conda shell.bash hook)"

if conda env list | grep -q 'genomad'; then
  echo "Activating existing conda environment 'genomad'"
fi

conda activate genomad

if [ ! -d "genomad_db" ]; then
  echo "Directory 'genomad_db' does not exist. Creating directory and downloading database."
  if ! genomad download-database .; then
    echo -e "\e[33mFailed to download database using genomad. Attempting to download from Zenodo.\e[0m"
    echo 
    mkdir -p genomad_db
    echo -e "\e[36mDownloading database from Zenodo...\e[0m"
    wget -O genomad_db_files.zip "https://zenodo.org/api/records/14886553/files-archive"
    if [ $? -ne 0 ]; then
      echo -e "\e[31mFailed to download database from Zenodo. Exiting.\e[0m"
      exit 1
    fi
    echo -e "\e[36mUnzipping downloaded database...\e[0m"
    unzip genomad_db_files.zip -d genomad_db
    echo -e "\e[36mExtracting tar.gz files...\e[0m"
    find genomad_db -name "*.tar.gz" -exec tar -xzf {} -C genomad_db --strip-components=1 \; -exec rm {} \;
    echo -e "\e[36mCleaning up temporary files...\e[0m"
    rm genomad_db_files.zip
    echo -e "\e[36mDatabase setup complete.\e[0m"
    fi
    else
    echo -e "\e[36mDirectory 'genomad_db' already exists. Skipping database download.\e[0m"
    fi


echo "Genomad is installed and ready to use."

if [ -d "./results/results_genomad/$filename" ]; then
  echo -e "\e[31mWARNING : Output directory already exists for $filename, skipping Genomad step.\e[0m"
  conda deactivate
  exit 0
fi
mkdir -p ./results/results_genomad/$filename
genomad end-to-end --threads "$threads" "$file_" "./results/results_genomad/$filename" genomad_db


conda deactivate
