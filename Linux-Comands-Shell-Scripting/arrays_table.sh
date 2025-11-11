#!/bin/bash

csv_url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-LX0117EN-SkillsNetwork/labs/M3/L2/arrays_table.csv"
data_file="arrays_table.csv"

# Download the CSV file using wget (or curl as fallback)
if command -v wget >/dev/null 2>&1; then
    wget "$csv_url" -O "$data_file"
elif command -v curl >/dev/null 2>&1; then
    curl -L "$csv_url" -o "$data_file"
else
    echo "Error: Neither wget nor curl is available. Please install one of them."
    exit 1
fi

# parse table columns into 3 arrays
column_0=($(cut -d "," -f 1 "$data_file"))
column_1=($(cut -d "," -f 2 "$data_file"))
column_2=($(cut -d "," -f 3 "$data_file"))

# print first array
echo "Displaying the first column:"
echo "${column_0[@]}"

## Create a new array as the difference of columns 1 and 2
# initialize array with header
column_3=("column_3")
# get the number of lines in each column
nlines=$(wc -l < "$data_file")
echo "There are $nlines lines in the file"
# populate the array
for ((i=1; i<$nlines; i++)); do
  column_3[$i]=$((column_2[$i] - column_1[$i]))
done
echo "${column_3[@]}"

## Combine the new array with the csv file
# first write the new array to file
# initialize the file with a header
echo "${column_3[0]}" > column_3.txt

for ((i=1; i<nlines; i++)); do
  echo "${column_3[$i]}" >> column_3.txt
done
paste -d "," "$data_file" column_3.txt > report.csv