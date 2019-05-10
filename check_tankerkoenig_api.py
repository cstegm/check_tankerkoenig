#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#######################################################################
#  Copyright (C) 2019 cstegm <cstegm's mail>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#######################################################################

# Date:
#  2017-12-21
#
# Author:
#  cstegm
#
# Repo:
#  https://github.com/cstegm/check_tankerkoenig
#
# Description:
#   Use Tankerkoenig API to extract provided fuel types.
#
# Advice:
#   1. YOU HAVE TO REQUEST AN OWN API-KEY!!!! https://creativecommons.tankerkoenig.de/
#   2. DO NOT CONFIGURE A CHECK INTERVAL UNDER 5 MIN
#
# Usage:
#   check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872
#
# Changelog:
#   2019-05-10 CW <doc@snowheaven.de> - added --table option - longoutput data as html table
#   2019-05-10 CW <doc@snowheaven.de> - moved prices into long output
#   2019-05-10 CW <doc@snowheaven.de> - added --offline option - demo data instead of requesting api
#   2019-05-10 CW <doc@snowheaven.de> - added --verbose option - more and more more output
#   2019-05-10 CW <doc@snowheaven.de> - usage of --crit_diesel without --warn_diesel is now possible
#   2019-05-10 CW <doc@snowheaven.de> - Fixed: no thresholds possible
#   2019-05-10 CW <doc@snowheaven.de> - Add thresholds to graphs
#   2019-05-09 CW <doc@snowheaven.de> - Show prices
#   2019-05-08 CW <doc@snowheaven.de> - Added threshold function
#
# ToDO:
#   - add more gas types
#   - be more dynamic


import sys

try:
    import argparse
    import requests
    import json
    from pprint import pprint

except ImportError as e:
    print("Missing python module: {}".format(e.message))
    sys.exit(255)


# Defaults
global exit_code
exit_code = 0

# define the program description
text = 'This program uses the Tankerkoenig API to check prices from gas-stations. Example: ./check_tankerkoenig_api.py --apikey <YOUR-API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872 --warn_diesel 1.22 --crit_diesel 1.20 --warn_e5 1.35 --crit_e5 1.30'

# initiate the parser with a description
parser = argparse.ArgumentParser(description = text)
parser.add_argument("--apikey",      help="specify the tankerkoenig api key. You can get the Key here: https://creativecommons.tankerkoenig.de/", required=True)
parser.add_argument("--stationid",   help="specify the stationid. You can find the stations here: https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html", required=True)
parser.add_argument("--verbose",     help="increase output verbosity", action="store_true")
parser.add_argument("--offline",     help="output demo data - no data is requested from api", action="store_true")
parser.add_argument("--table",       help="longoutput data as html table", action="store_true")

# Thresholds
parser.add_argument("--warn_diesel", help="define your optional warning threshold for diesel (use . in price!)")
parser.add_argument("--crit_diesel", help="define your optional critical threshold for diesel (use . in price!)")
parser.add_argument("--warn_e5",     help="define your optional warning threshold for super e5 (use . in price!)")
parser.add_argument("--crit_e5",     help="define your optional critical threshold for super e5 (use . in price!)")
parser.add_argument("--warn_e10",    help="define your optional warning threshold for super e10 (use . in price!)")
parser.add_argument("--crit_e10",    help="define your optional critical threshold for super e10 (use . in price!)")

args = parser.parse_args()

if args.offline:
    print ( "********************" )
    print ( "*** OFFLINE MODE ***" )
    print ( "********************" )

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


if args.verbose:
    print( "warnings:" )
    pprint (warnings)
    print( "criticals:" )
    pprint (criticals)
    print ( "--------" )


# Get Details of the gasstation:
if args.offline:
    r_detail = '{"ok":true,"license":"CC BY 4.0 -  https:\/\/creativecommons.tankerkoenig.de","data":"MTS-K","status":"open","station":{"id":"005056ba-7cb6-1ed2-bceb-90e59ad2cd35","name":"star Tankstelle","brand":"STAR","street":"Gelsdorfer Strasse","houseNumber":"2-4","postCode":53340,"place":"Meckenheim","openingTimes":[{"text":"Mo-Fr","start":"06:00:00","end":"22:00:00"},{"text":"Samstag","start":"07:00:00","end":"22:00:00"},{"text":"Sonntag, Feiertag","start":"08:00:00","end":"22:00:00"}],"overrides":[],"wholeDay":false,"isOpen":true,"e5":1.449,"e10":1.429,"diesel":1.249,"lat":50.61793,"lng":7.02484,"state":null}}'

    j_detail = json.loads(r_detail)

    if args.verbose:
        print ( j_detail)

else:
    r_detail = requests.get(tankerkoenig_detail_url)

    # if no 200 exit
    if r_detail.status_code != requests.codes.ok:
        if int(r_detail.status_code) == 503:
            print ( "Request interval is too small!" )
        else:
            print( "Exitcode:" + str(r_detail.status_code))
        exit(3)

    j_detail = r_detail.json()

if args.verbose:
    print( "r_detail:" )
    pprint ( r_detail )
    print ( "--------" )

station_name = j_detail["station"]["name"]
service_name = "Station_" + station_name.replace(" ","_")

if args.verbose:
    print( "station_name : " + station_name )
    print( "service_name : " + service_name )
    print( "status       : " + j_detail["status"] )


# Get the Prices:
if args.offline:
    r_price = '{"ok":true,"license":"CC BY 4.0 -  https:\/\/creativecommons.tankerkoenig.de","data":"MTS-K","prices":{"404b23d9-3446-4b68-ab7e-3fdced82c872":{"status":"open","e5":1.429,"e10":1.419,"diesel":1.199}}}'

    j_price = json.loads(r_price)

    if args.verbose:
        print ( j_price)

else:
    r_price = requests.get(tankerkoenig_price_url)

    # if no 200 exit
    if r_price.status_code != requests.codes.ok:
        if int(r_price.status_code) == 503:
            print ( "Request interval is too small!" )
        else:
            print( "Exitcode:" + str(r_price.status_code))
        exit(3)

    j_price = r_price.json()

if args.verbose:
    print( "r_price:" )
    pprint ( r_price )
    print ( "--------" )


# transform {"license": "CC BY 4.0 -  https://creativecommons.tankerkoenig.de", "ok": true, "prices": {"51d4b671-a095-1aa0-e100-80009459e03a": {"e5": 1.419, "diesel": 1.219, "status": "open", "e10": 1.379}}, "data": "MTS-K"}
# into {"e5": 1.419, "diesel": 1.219, "status": "open", "e10": 1.379}
prices = next(iter(j_price["prices"].values()))

threshold_text = ""
output_prices = ""
metrics       = ""
warn          = ""
crit          = ""
hits          = 0

for price in prices.items():
    key   = price[0]
    value = str(price[1])
    # filter out the status
    if key == "status":
        continue

    if args.verbose:
        print ( "KEY          : %s" % (key) )
        print ( "VALUE(str)   : %s" % (value) )
        print ( "WARN         : %s: %s" % (key, warnings.get(key)) )
        print ( "CRIT         : %s: %s" % (key, criticals.get(key)) )
        print ( "type warnings.get(key)  : %s" % type(warnings.get(key)) )
        print ( "type criticals.get(key) : %s" % type(criticals.get(key)) )
        print ( "--------" )

    # Process thresholds
    #if (criticals.get(key) is not None) and (warnings.get(key) is not None):
    if (criticals.get(key) is not None) or (warnings.get(key) is not None):
        warn = str(warnings.get(key))
        crit = str(criticals.get(key))

        if args.verbose:
            print ( "- WARN         : %s: %s" % (key, warnings.get(key)) )
            print ( "- CRIT         : %s: %s" % (key, criticals.get(key)) )
            print ( "- type warnings.get(key)  : %s" % type(warnings.get(key)) )
            print ( "- type criticals.get(key) : %s" % type(criticals.get(key)) )
            print ( "--------" )


        if float(criticals.get(key)) is not None:
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

    if args.verbose:
        print ( "threshold_text : %s" % threshold_text )

        print ( "-- WARN         : %s: %s" % (key, warnings.get(key)) )
        print ( "-- CRIT         : %s: %s" % (key, criticals.get(key)) )
        print ( "-- type warnings.get(key)  : %s" % type(warnings.get(key)) )
        print ( "-- type criticals.get(key) : %s" % type(criticals.get(key)) )
        print ( "--------" )

    # Build perfdata output ('e5'=1.429 'e10'=1.419 'diesel'=1.199)
    metrics = metrics + "'"+ key + "'=" + value + ";" + warn + ";" + crit + ";0;2.5 "

    # Build prices output
    if args.table:
        output_prices = output_prices + "<tr><td>" + key.title() + "</td><td>" + value + " Euro</td><td>" + warn + "</td><td>" + crit + "</td></tr>"
    else:
        output_prices = output_prices + key.title() + "\t: " + value + " Euro\n"

    if args.verbose:
        print ( "output_prices : %s" % output_prices )

# Build html table
if args.table:
    output_prices = "<table border=1><tr><th>Type</th><th>Price</th><th>Warning</th><th>Critical</th></tr>" + output_prices + "</table>"

# Generate output
# If more than one threshold hits
if hits > 1:
    fill = " and "
    threshold_output = threshold_output + fill + threshold_text
else:
    threshold_output = threshold_text

if prices["status"] != "open":
    print( station_name + " is closed now" )
else:
    if exit_code != 0:
        print( station_name + " - " + threshold_output + "\n" + output_prices + "|" +  metrics )
    else:
        print( station_name + "\n" + output_prices + "|" +  metrics )


exit(exit_code)
