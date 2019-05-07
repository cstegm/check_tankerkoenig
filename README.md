# check_tankerkoenig

This check uses the tankerkoenig.de API to check the prices of gas stations. 
1. You need to grab an API Key from: https://creativecommons.tankerkoenig.de/ for the --apikey parameter
2. You also need to retrieve the Stationid from the Finder-Tool https://creativecommons.tankerkoenig.de/TankstellenFinder/index.html for the --stationid parameter


Example:
```
./check_tankerkoenig_api.py --apikey <your api key> --stationid 51d4b671-a095-1aa0-e100-80009459e03a
```

Prerequisites:
```
CentOS 7
yum install python36 python36-requests
```
