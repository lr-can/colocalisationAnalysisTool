#!/bin/bash

file_=$1
filename=$(basename -- "$file_")
extractfilename="${filename%%.*}"

echo $extractfilename

if [ -d "./results/results_phastest/$extractfilename" ]; then
    echo -e "\e[31mWARNING : Output directory already exists for $filename, skipping Phastest step.\e[0m"
    exit 0
fi

 # Detect Python interpreter
if command -v python &>/dev/null; then
    PYTHON_BIN=python
elif command -v python3 &>/dev/null; then
    PYTHON_BIN=python3
else
    echo "❌ No Python interpreter found. Please install Python 3 and try again."
    exit 1
fi

echo "Copying the file to the tmp directory"

mkdir -p ./tmp/
cp "$file_" ./tmp/
gunzip ./tmp/"$filename"

for f in ./tmp/*; do
    mv -- "$f" "${f%.gz}.fna"
done

bash phastest_api.sh --submitjob --inputDir ./tmp/

echo -e "\e[34mJob submitted.\e[0m"

echo -e "\e[34mWaiting for the job to finish...\e[0m"

mkdir -p ./results/results_phastest/

job_json_file=$(ls ./SubmissionJson/* | head -n 1)
job_id=$(jq -r '.job_id' "$job_json_file")
$PYTHON_BIN ./scripts/phastest.py -f ./tmp/"${filename}" -j "$job_id"

echo -e "\e[32mPhasTest has finished running\e[0m"

rm -r ./tmp/
rm -r ./SubmissionJson/


echo "Removed the file in the tmp directory"