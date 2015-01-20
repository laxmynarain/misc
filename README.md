# misc
## Part 1:

For brevity the thought process is described as a series of steps.

1. An external library Geopy is used to get coordinates from a physical address.
2. urllib and json modules are used to get data and read json.
3. datetime and time modules are used to make epoch time conversions
3. For ease of use a Quake class is created to hold quake information.
4. Haversine formula is used to calculate distance between two points on the earth's surface.

1. To account for possibilities of two quakes with the same magnitude, an array of such quake objects is used as the "result" object. In this code it is called "quakelist".
2. The order of evaluation of quake criteria is as follows
   2.1 Quake happened less than a week ago
   2.2 Distance is less than 100 miles
3. The flow control of the program is as follows:
   If quake < week:
      if quake_distance <= 100 miles:
         if current_magnitude == highest magnitude so far:
            append new quake object to list
         elif curr_magnitude > highest magnitude so far:
            empty the quake list and populate with new quake object

_____________________________________________________________________________________________________________________

## Part 2:

jq is a lightweight commandline JSON processor.
We can use a combination of jq, curl and a few other unix utilities to get the desired result.

A sample code would look like this. (Although this solution is not nearly complete, it gives an idea of how some loose scripting could accomplish the desired end result.

"""

\#! /bin/bash

curl 'http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson' > eq.json
NUMOFLINES=$(wc -l < eq.json)
highmag=0

for i in `seq 1 $NUMOFLINES`; do
   # The line nelow can be used if we want to get more information out of the json object
   # cat eq.json | jq '.features['$i'].properties | {mag, time, place}'
    mag=$(cat eq.json | jq '.features['$i'].properties.mag')
    if [ "$mag" > "$highmag" ]; then
        echo $mag
        highmag=$mag
    fi
done
echo "______"
echo $highmag

"""
_____________________________________________________________________________________________________________________

## Part 3:

There are many standard tools to convert JSON to CSV. 
However if we have a JSON file and an outline file. We can use ordered dictionaries in python to process the data rows. This would eventually transform into the rows of a CSV file.
