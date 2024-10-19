# network-traffic-monitoring

This script checks the upload and download traffic and saves the data in a portgres db

cron scheduling every minute:

``` bash
crontab -e

* * * * * /usr/bin/python3 /path/to/super/awesome/script/network_traffic.py
```
