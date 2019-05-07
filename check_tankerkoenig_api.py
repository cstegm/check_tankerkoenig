#!/usr/bin/env python3
import sys, argparse
import requests, json
import pprint

# define the program description
text = 'This program uses the Tankerkoenig API to check prices from gas-stations'

# initiate the parser with a description
parser = argparse.ArgumentParser(description = text)  
parser.add_argument("--apikey", help="specify the tankerkoenig api key. You can get the Key here: https://creativecommons.tankerkoenig.de/")
parser.add_argument("--stationid", help="specify the stationid. You can find the stations here: https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html")
args = parser.parse_args()  

if args.apikey and args.stationid:
    next
else:
    print("please specify apikey and station id")
    exit(1)

# API Dokumentation: https://creativecommons.tankerkoenig.de/?page=info
# Den key kann man hier beantragen: https://creativecommons.tankerkoenig.de/
tankerkoenig_api_key = args.apikey

# jet gesucht über: https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html man muss hier den marker an die richtige stelle ziehen, damit man in dem umkreis die tankstellen sieht,
tankerkoenig_tankstellen_id = args.stationid

# build detail url
tankerkoenig_detail_url = "https://creativecommons.tankerkoenig.de/json/detail.php?id=" + tankerkoenig_tankstellen_id + "&apikey=" + tankerkoenig_api_key

# build price url
tankerkoenig_price_url = "https://creativecommons.tankerkoenig.de/json/prices.php?ids=" + tankerkoenig_tankstellen_id + "&apikey=" + tankerkoenig_api_key




# Get Details of the gasstation:
r_detail = requests.get(tankerkoenig_detail_url)

# if no 200 exit
if r_detail.status_code != requests.codes.ok:
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
    print( "Exitcode:" + str(r_price.status_code))
    exit(3)
j_price = r_price.json()

# transform {"license": "CC BY 4.0 -  https://creativecommons.tankerkoenig.de", "ok": true, "prices": {"51d4b671-a095-1aa0-e100-80009459e03a": {"e5": 1.419, "diesel": 1.219, "status": "open", "e10": 1.379}}, "data": "MTS-K"}
# into {"e5": 1.419, "diesel": 1.219, "status": "open", "e10": 1.379}
prices = next(iter(j_price["prices"].values()))

metrics = ""
for price in prices.items():
    key = price[0]
    value = str(price[1])
    # filter out the status
    if key == "status":
        continue
    
    metrics = metrics + "'"+ key + "'=" + value + " "

if prices["status"] != "open":
    print( station_name + " is closed now")
else:
    print( station_name + " |" +  metrics)
exit(0)
