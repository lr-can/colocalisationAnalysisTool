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

end=$((SECONDS+600))
while [ $SECONDS -lt $end ]; do
    echo -e "\e[34mChecking job status...\e[0m"
    if ! bash phastest_api.sh --getresults --outDir ./results/results_phastest/$filename; then
        echo -e "\e[34mJob is still running...\e[0m"
    else
        echo -e "\e[34mJob has finished. Retrieving data from the server...\e[0m"
        break
    fi
    sleep 30
done

if [ $SECONDS -ge $end ]; then
    echo -e "\e[31mJob did not finish within 10 minutes.\e[0m"
    exit 1
fi

if ! bash phastest_api.sh --getresults --outDir ./results/results_phastest/$filename; then
    echo -e "\e[31mFailed to retrieve data from the server.\e[0m"
    exit 1
fi

echo -e "\e[32mPhasTest has finished running\e[0m"

rm -r ./tmp/

echo "Removed the file in the tmp directory"