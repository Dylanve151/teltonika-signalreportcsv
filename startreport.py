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

with open(CSVfilename, 'w', encoding='UTF8', newline='') as CSVfile:
	CSVwriter = csv.writer(CSVfile)
	
	while alines < 99: 
		while TSvalue == int(datetime.timestamp(datetime.now())):
			time.sleep(0.1)
		
		## gsm data
		CellData = ''
		cmd = ['gsmctl', '-CbfoqtK']
		proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		o, e = proc.communicate()
		CellData = o.decode('ascii').splitlines()
		
		## TS value
		TSvalue = int(datetime.timestamp(datetime.now()))
		
		if len(CellData) > 9:
			
			## gsm values
			LCIDvalue, pBANDvalue, PLMNvalue, CARRIERvalue, RSSIvalue, RSRPvalue, SINRvalue, RSRQvalue, TYPEvalue, *SERVINGvalues = CellData
			
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
			GPSvalues = ''
			cmd = ['gpsctl', '-ixas']
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			o, e = proc.communicate()
			GPSvalues = o.decode('ascii').splitlines()
			if len(GPSvalues) > 3:
				LAvalue, LOvalue, ATvalue, GPSSTATUSvalue = GPSvalues
				if int(GPSSTATUSvalue) == 0:
					LAvalue = None
					LOvalue = None
					ATvalue = None
			else:
					LAvalue = None
					LOvalue = None
					ATvalue = None
					GPSSTATUSvalue = None
			
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
