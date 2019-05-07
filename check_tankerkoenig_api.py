#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Date:
#  2017-12-21
#
# Author:
#  cstegm
#
# Description:
#   Use Tankerkoenig API to extract provided fuel types.
#
# Usage:
#   check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872
#
# Changelog:
#   2019-05-08 CW <doc@snowheaven.de> - Added threshold function
#
# ToDO:
#   - add more gas types
#   - be more dynamic


import sys

try:
    import argparse
    import requests, json
    from pprint import pprint

except ImportError as e:
    print("Missing python module: {}".format(e.message))
    sys.exit(255)


# Defaults
exit_code = 0

# define the program description
text = 'This program uses the Tankerkoenig API to check prices from gas-stations'

# initiate the parser with a description
parser = argparse.ArgumentParser(description = text)
parser.add_argument("--apikey", help="specify the tankerkoenig api key. You can get the Key here: https://creativecommons.tankerkoenig.de/")
parser.add_argument("--stationid", help="specify the stationid. You can find the stations here: https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html")

# Thresholds
parser.add_argument("--warn_diesel", help="define your optional warning threshold for diesel")
parser.add_argument("--crit_diesel", help="define your optional critical threshold for diesel")
parser.add_argument("--warn_e5", help="define your optional warning threshold for super e5")
parser.add_argument("--crit_e5", help="define your optional critical threshold for super e5")
parser.add_argument("--warn_e10", help="define your optional warning threshold for super e10")
parser.add_argument("--crit_e10", help="define your optional critical threshold for super e10")

args = parser.parse_args()

if args.apikey and args.stationid:
    next
else:
    print("please specify apikey and station id")
    exit(1)

# API Documentation: https://creativecommons.tankerkoenig.de/?page=info
# Get your API key from here: https://creativecommons.tankerkoenig.de/
tankerkoenig_api_key = args.apikey

# Get the gas station ID from here: https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html
# 1. search for the station
# 2. click on the name
# 3. note the resulting id
tankerkoenig_tankstellen_id = args.stationid

# build detail url
tankerkoenig_detail_url = "https://creativecommons.tankerkoenig.de/json/detail.php?id=" + tankerkoenig_tankstellen_id + "&apikey=" + tankerkoenig_api_key

# build price url
tankerkoenig_price_url = "https://creativecommons.tankerkoenig.de/json/prices.php?ids=" + tankerkoenig_tankstellen_id + "&apikey=" + tankerkoenig_api_key

# Build threshold dicts
warnings = {'diesel'         : args.warn_diesel,
            'e5'             : args.warn_e5,
            'e10'            : args.warn_e10,
           }

criticals = {'diesel'        : args.crit_diesel,
             'e5'            : args.crit_e5,
             'e10'           : args.crit_e10,
            }


#print( "warnings:" )
#pprint (warnings)
#print( "criticals:" )
#pprint (criticals)


# Get Details of the gasstation:
r_detail = requests.get(tankerkoenig_detail_url)

# if no 200 exit
if r_detail.status_code != requests.codes.ok:
    if int(r_detail.status_code) == 503:
        print ( "Request interval is too small!" )
    else:
        print( "Exitcode:" + str(r_detail.status_code))
    exit(3)
j_detail = r_detail.json()

station_name = j_detail["station"]["name"]
service_name = "Station_" + station_name.replace(" ","_")
#print(service_name)

# Get the Prices:
r_price = requests.get(tankerkoenig_price_url)

# if no 200 exit
if r_price.status_code != requests.codes.ok:
    if int(r_price.status_code) == 503:
        print ( "Request interval is too small!" )
    else:
        print( "Exitcode:" + str(r_price.status_code))
    exit(3)
j_price = r_price.json()

# transform {"license": "CC BY 4.0 -  https://creativecommons.tankerkoenig.de", "ok": true, "prices": {"51d4b671-a095-1aa0-e100-80009459e03a": {"e5": 1.419, "diesel": 1.219, "status": "open", "e10": 1.379}}, "data": "MTS-K"}
# into {"e5": 1.419, "diesel": 1.219, "status": "open", "e10": 1.379}
prices = next(iter(j_price["prices"].values()))

metrics = ""
hits = 0
for price in prices.items():
    key   = price[0]
    value = str(price[1])
    # filter out the status
    if key == "status":
        continue

    # Process thresholds
    threshold_text = ""

    #print ( "KEY          : %s" % (key) )
    #print ( "VALUE(str)   : %s" % (value) )
    #print ( "WARN         : %s: %s" % (key, warnings.get(key)) )
    #print ( "CRIT         : %s: %s" % (key, criticals.get(key)) )
    #print ( "type warnings.get(key)  : %s" % type(warnings.get(key)) )
    #print ( "type criticals.get(key) : %s" % type(criticals.get(key)) )
    #print( "--------" )

    if (criticals.get(key) is not None) and (warnings.get(key) is not None):
        if float(value) < float(criticals.get(key)):
            threshold_text = "%s is cheaper than %s Euro!" % (key.title(), criticals.get(key))
            exit_code = 2
            hits = hits + 1
        elif float(value) < float(warnings.get(key)):
            threshold_text = "%s is cheaper than %s Euro!" % (key.title(), warnings.get(key))
            exit_code = 1
            hits = hits + 1
        else:
            threshold_text = ""
            exit_code = 0
    else:
        threshold_text = ""

    #print ( "threshold_text : %s" % threshold_text )

    # Build perfdata output
    metrics = metrics + "'"+ key + "'=" + value + " "


# Generate output
# If more than one threshold hits
if hits > 1:
    fill = " and "
    threshold_sum = threshold_sum + fill + threshold_text
else:
    threshold_sum = threshold_text

output_text = " " + "(" + threshold_sum + ")"


if prices["status"] != "open":
    print( station_name + " is closed now" )
else:
    if exit_code != 0:
        print( station_name + output_text + "|" +  metrics )
    else:
        print( station_name + "|" +  metrics )


exit(exit_code)
