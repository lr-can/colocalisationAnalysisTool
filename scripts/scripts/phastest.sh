#!/bin/bash

file_=$1
filename=$(basename -- "$file_")

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

job_json_file=$(ls ./SubmissionJson/* | head -n 1)
job_id=$(jq -r '.job_id' "$job_json_file")
python3 ./scripts/phastest.py -f ./tmp/"${filename}" -j "$job_id"

echo -e "\e[32mPhasTest has finished running\e[0m"

rm -r ./tmp/
rm -r ./SubmissionJson/


echo "Removed the file in the tmp directory"