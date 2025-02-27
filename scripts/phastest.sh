#!/bin/bash

file_=$1
filename=$(basename -- "$file_")

echo "Copying the file to the tmp directory"

mkdir -p ./tmp/
cp "$file_" ./tmp/
gunzip -c ./tmp/"$filename" > ./tmp/"$filename.fna"
mv ./tmp/"$filename" ./tmp/"$filename.fna"

bash phastest_api.sh --submitjob --inputDir ./tmp/

echo -e "\e[34mJob submitted, waiting 5 min before retrieving data from the server\e[0m"
sleep 300
echo -e "\e[34mRetrieving data from the server...\e[0m"
bash phastest_api.sh --getresults --outDir ./results/results_phastest/$filename --cleanup
echo -e "\e[32mPhasTest has finished running\e[0m"

rm -r ./tmp/

echo "Removed the file in the tmp directory"