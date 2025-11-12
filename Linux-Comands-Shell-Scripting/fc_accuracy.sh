#! /bin/bash

yesterday_fc=$(tail -2 rx_poc.log | head -1 | cut -d ' ' -f5 | grep -oE '^[0-9]+')
today_temp=$(tail -1 rx_poc.log | cut -d ' ' -f4 | grep -oE '^[0-9]+')

# Check if we got valid numbers
if [ -z "$yesterday_fc" ] || [ -z "$today_temp" ]; then
    echo "Error: Could not extract temperature values from rx_poc.log"
    exit 1
fi

accuracy=$(($yesterday_fc-$today_temp))

echo "accuracy is $accuracy"

if [ $accuracy -ge -1 ] && [ $accuracy -le 1 ]
then
    accuracy_range=excellent
elif [ $accuracy -ge -2 ] && [ $accuracy -le 2 ]
then
    accuracy_range=good
elif [ $accuracy -ge -3 ] && [ $accuracy -le 3 ]
then
    accuracy_range=fair
else
    accuracy_range=poor
fi

echo "Forecast accuracy is $accuracy_range"

row=$(tail -1 rx_poc.log)
year=$(echo $row | cut -d ' ' -f1)
month=$(echo $row | cut -d ' ' -f2)
day=$(echo $row | cut -d ' ' -f3)
echo -e "$year\t$month\t$day\t$today_temp\t$yesterday_fc\t$accuracy\t$accuracy_range" >> historical_fc_accuracy.tsv