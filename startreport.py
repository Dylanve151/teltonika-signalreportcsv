#!/usr/bin/python

import subprocess
from datetime import datetime
import re
import csv
import time

TSstart = int(datetime.timestamp(datetime.now()))
CSVfilename = '/root/'+'signalreport_'+str(TSstart)+'.csv'
alines=0
TSvalue=0
CellStatus=''

with open(CSVfilename, 'w', encoding='UTF8', newline='') as CSVfile:
	CSVwriter = csv.writer(CSVfile)
	
	while alines < 2: 
		while TSvalue == int(datetime.timestamp(datetime.now())):
			time.sleep(0.1)
		
		## gsm active
		cmd = ['gsmctl', '-q']
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		o, e = proc.communicate()
		CellStatus = o.decode('ascii')
		
		## TS value
		TSvalue = int(datetime.timestamp(datetime.now()))
		
		if CellStatus != '':
			
			## gsm values
			cmd = ['gsmctl', '-CbfoqtK']
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			o, e = proc.communicate()
			LCIDvalue, pBANDvalue, PLMNvalue, CARRIERvalue, RSSIvalue, RSRPvalue, SINRvalue, RSRQvalue, TYPEvalue, *SERVINGvalues = o.decode('ascii').splitlines()
			
			## LCID values
			if 'ERROR' in LCIDvalue:
				LCIDvalue = 0
			else:
				LCIDvalue = int(LCIDvalue.strip(), 16)
			
			## primary band value
			pBANDvalue = pBANDvalue.strip()
			
			## PLMN value
			PLMNvalue = PLMNvalue.strip()
			
			## MCC + MNC
			MCCvalue, MNCvalue = re.findall('...?', PLMNvalue)
			
			## Carrier name
			CARRIERvalue = CARRIERvalue.strip()
			
			## signal values
			RSSIvalue = RSSIvalue.strip('RSSI: ').strip()
			SINRvalue = SINRvalue.strip('SINR: ').strip()
			RSRPvalue = RSRPvalue.strip('RSRP: ').strip()
			RSRQvalue = RSRQvalue.strip('RSRQ: ').strip()
			
			## network type value
			TYPEvalue = TYPEvalue.strip()
			
			## Serving value
			pSERVINGvalue, *oSERVINGvalues = SERVINGvalues
			pBEARINGvalue, pTDDvalue, *OTHERSERVvalues = pSERVINGvalue.split(' | ')
			pBEARINGvalue = pBEARINGvalue.strip('Access tech: ').strip()
			pTDDvalue = pTDDvalue.strip('TDD mode: ').strip()
			
			## GPS Values
			cmd = ['gpsctl', '-ixas']
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			o, e = proc.communicate()
			LAvalue, LOvalue, ATvalue, GPSSTATUSvalue = o.decode('ascii').splitlines()
			if int(GPSSTATUSvalue) == 0:
				LAvalue = None
				LOvalue = None
				ATvalue = None
			
			## bands info
			cmd = ['gsmctl', '-A', 'AT+QNWINFO']
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			o, e = proc.communicate()
			BANDINFOvalue = o.decode('ascii').replace('+QNWINFO: ','').replace('"','').strip()
			BANDINFOvalue1 = " | ".join(BANDINFOvalue.splitlines())
			
			## csv data
			CSVdata = {"lcid": LCIDvalue, "bearer": pBEARINGvalue, "band": pBANDvalue, "rssi": RSSIvalue, "sinr": SINRvalue, "rsrp": RSRPvalue, "rsrq": RSRQvalue, "plmn": PLMNvalue, "mnc": MNCvalue, "mcc": MCCvalue, "carrier_name": CARRIERvalue, "la": LAvalue, "lo": LOvalue, "at": ATvalue, "type": TYPEvalue, "bandinfo": BANDINFOvalue1,"ts": str(TSvalue)}
			
			if alines == 0:
				CSVwriter.writerows([CSVdata.keys()])
				alines = 1
			
			CSVwriter.writerows([CSVdata.values()])
			
			CSVfile.flush()
