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

# CheckMK

CheckMK usage:
```
cd /opt/omd/sites/<YOUR_SITE>/local/lib/nagios/plugins/
git clone git@github.com:cstegm/check_tankerkoenig.git
```

Create a Classical active and passive Monitoring check in WATO:
```
Service description: TK-D-freie_Ahnefeldstr
Command line: 	     check_tankerkoenig/check_tankerkoenig_api.py --apikey <YOUR API-KEY> --stationid 404b23d9-3446-4b68-ab7e-3fdced82c872
Performance data:    process performance data
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

