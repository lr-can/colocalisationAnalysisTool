#!/bin/bash

file_=$1
threads=$2

filename=$(basename -- "$file_")
filename="${filename%%.*}"

# Initialize conda
eval "$(conda shell.bash hook)" > /dev/null 2>&1
conda init > /dev/null 2>&1

if conda env list | grep -q 'genomad'; then
  echo "Activating existing conda environment 'genomad'"
fi

conda activate genomad

if [ ! -d "genomad_db" ]; then
  echo -e "\e[36mDirectory 'genomad_db' does not exist. Creating directory and downloading database.\e[0m"
  if ! genomad download-database .; then
    echo -e "\e[33mFailed to download database using genomad. Attempting to download from Zenodo.\e[0m"
    mkdir -p genomad_db

    echo -e "\e[36mDownloading 'genomad_db_v1.9.tar.gz' from Zenodo...\e[0m"
    wget -O genomad_db_v1.9.tar.gz "https://zenodo.org/records/14886553/files/genomad_db_v1.9.tar.gz?download=1"
    if [ $? -ne 0 ]; then
      echo -e "\e[31mFailed to download 'genomad_db_v1.9.tar.gz'. Exiting.\e[0m"
      exit 1
    fi
    echo -e "\e[36mExtracting 'genomad_db_v1.9.tar.gz'...\e[0m"
    tar -xzf genomad_db_v1.9.tar.gz -C genomad_db --strip-components=1
    rm genomad_db_v1.9.tar.gz

    echo -e "\e[36mDownloading 'genomad_hmm_v1.9.tar.gz' from Zenodo...\e[0m"
    wget -O genomad_hmm_v1.9.tar.gz "https://zenodo.org/records/14886553/files/genomad_hmm_v1.9.tar.gz?download=1"
    if [ $? -ne 0 ]; then
      echo -e "\e[31mFailed to download 'genomad_hmm_v1.9.tar.gz'. Exiting.\e[0m"
      exit 1
    fi
    echo -e "\e[36mExtracting 'genomad_hmm_v1.9.tar.gz'...\e[0m"
    tar -xzf genomad_hmm_v1.9.tar.gz -C genomad_db
    rm genomad_hmm_v1.9.tar.gz

    echo -e "\e[36mDownloading 'genomad_metadata_v1.9.tsv.gz' from Zenodo...\e[0m"
    wget -O genomad_metadata_v1.9.tsv.gz "https://zenodo.org/records/14886553/files/genomad_metadata_v1.9.tsv.gz?download=1"
    if [ $? -ne 0 ]; then
      echo -e "\e[31mFailed to download 'genomad_metadata_v1.9.tsv.gz'. Exiting.\e[0m"
      exit 1
    fi
    echo -e "\e[36mExtracting 'genomad_metadata_v1.9.tsv.gz'...\e[0m"
    gunzip -f genomad_metadata_v1.9.tsv.gz

    echo -e "\e[36mDownloading 'genomad_msa_v1.9.tar.gz' from Zenodo...\e[0m"
    wget -O genomad_msa_v1.9.tar.gz "https://zenodo.org/records/14886553/files/genomad_msa_v1.9.tar.gz?download=1"
    if [ $? -ne 0 ]; then
      echo -e "\e[31mFailed to download 'genomad_msa_v1.9.tar.gz'. Exiting.\e[0m"
      exit 1
    fi
    echo -e "\e[36mExtracting 'genomad_msa_v1.9.tar.gz'...\e[0m"
    tar -xzf genomad_msa_v1.9.tar.gz -C genomad_db
    rm genomad_msa_v1.9.tar.gz
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
