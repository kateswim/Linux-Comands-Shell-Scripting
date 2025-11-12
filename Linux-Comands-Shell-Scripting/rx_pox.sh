#! /bin/bash

city=Surrey

curl -s "wttr.in/$city?T" --output weather_report

#To extract Current Temperature
obs_temp=$(grep -m 1 '°.' weather_report | grep -Eo -e '-?[[:digit:]].*')

echo "The current Temperature of $city: $obs_temp"

fc_temp=$(head -23 weather_report | tail -1 | grep '°.' | cut -d 'C' -f2 | grep -Eo -e '-?[[:digit:]].*')

echo "The forecasted temperature for noon tomorrow for $city : $fc_temp C"

#Assign Country and City to variable TZ
TZ='Canada/Surrey'

# Use command substitution to store the current day, month, and year in corresponding shell variables:
day=$(TZ='Canada/Surrey' date -u +%d) 
month=$(TZ='Canada/Surrey' date +%m)
year=$(TZ='Canada/Surrey' date +%Y)


record=$(echo -e "$year\t$month\t$day\t$obs_temp\t$fc_temp C")
echo -e "$record" >> rx_poc.log