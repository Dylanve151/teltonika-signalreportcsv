# teltonika-signalreportcsv

Requires python package to be installed.

logs lcid, bearer, band, rssi, sinr, rsrp, rsrq, plmn, mnc, mcc, carrier_name, la, lo, at, type, bandinfo, ts in a convenient CSV file

For /etc/rc.local
```
python startreport.py >> /var/log/startreport.log
```
