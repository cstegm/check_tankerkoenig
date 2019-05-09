# check_tankerkoenig

This check uses the tankerkoenig.de API to check the prices of gas stations. 
1. You need to grab an API Key from: https://creativecommons.tankerkoenig.de/ for the --apikey parameter
2. You also need to retrieve the Stationid from the Finder-Tool https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html for the --stationid parameter


Help:
```
./check_tankerkoenig_api.py --help

```

Example:
```
./check_tankerkoenig_api.py --apikey <your api key> --stationid 51d4b671-a095-1aa0-e100-80009459e03a

or

./check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872 --warn_diesel 1.22 --crit_diesel 1.20 --warn_e5 1.35 --crit_e5 1.30

TSB Tankstellenbetriebs-GmbH ( e5:1.429 e10:1.419 diesel:1.199 ) Diesel is cheaper than 1.20 Euro!!!!|'e5'=1.429;1.35;1.30;0;2.5'e10'=1.419;1.35;1.30;0;2.5'diesel'=1.199;1.22;1.20;0;2.5
```

Prerequisites:
```
CentOS 7
yum install python36 python36-requests
```

# CheckMK

CheckMK usage:
```
cd /opt/omd/sites/<YOUR_SITE>/local/lib/nagios/plugins/
git clone git@github.com:cstegm/check_tankerkoenig.git
```

Create a "Classical active and passive Monitoring" check in WATO -> Host & Service Parameters -> Active checks (HTTP, TCP, etc.) :
```
Service description: TK-D-freie_Ahnefeldstr
Command line: 	     check_tankerkoenig/check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872
Performance data:    process performance data
```

You can use and combine thresholds for different gas types and define a maximum wait time for a result.
```
Service description: 	TK-D-freie_Ahnefeldstr
Command line: 		git/check_tankerkoenig/check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872 --warn_diesel 1.25 --crit_diesel 1.20 --warn_e5 1.35 --crit_e5 1.30
Performance data: 		process performance data
Check freshness: 	
Expected update interval: 				5 minutes
State in case of absent updates: 			UNKNOWN
Plugin output in case of absent updates: 	Check result did not arrive in time
```

Check interval:
```--apikey <YOUR API-KEY>
Use a minimal check interval of 5 min. If you use a shorter interval your API key could be blocked.
```
# CheckMK mrpe
Another Option is to use the check_mk_agent and mrpe. Add the following Line to /etc/check_mk/mrpe.cfg:
```
Tanke_JET (interval=300) /your/path/to/check_tankerkoenig/check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 51d4b671-a095-1aa0-e100-80009459e03a
```

Changelog
- 2019-05-10 CW <doc@snowheaven.de> - Add thresholds to graphs
- 2019-05-09 CW <doc@snowheaven.de> - Show prices
- 2019-05-08 CW <doc@snowheaven.de> - Added threshold function
