	
from __future__ import print_function

import argparse
import socket

from datetime import datetime
FILEOUT='outall.txt'
RESULTFILE="res.txt"
USERID=""
PASSWORD=''
YEAR = 2018
MONTH = 1
from ssh2.session import Session
from ssh2.sftp import LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR
def getNames(year,month):
	import datetime, calendar
	num_days = calendar.monthrange(year, month)[1]
	days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
	filelist=[]
	for item in days:
		#print(item)
		item1=str(item).replace("-","")
		filelist.append("custom_STL-"+item1+".01.009.CSV")
		#20180106
	#print filelist	
	return filelist
def main():
	print ('asdfasdf')
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(('reports.paypal.com', 22))
	s = Session()
	s.handshake(sock)
	s.userauth_password(USERID, PASSWORD)
	chan = s.open_session()
	print('connected')	
	sftp = s.sftp_init()
	print ('sftp done')
	now = datetime.now()
	outf= open(RESULTFILE,"w+")
	filelist=getNames(YEAR,MONTH)
	with open(FILEOUT, 'w+') as f:
		for fileName in filelist:		
			with sftp.open('/pptransfers/outgoing/'+fileName, LIBSSH2_FXF_READ, LIBSSH2_SFTP_S_IRUSR) as fh:
				print('sftp done')
				for size, data in fh:			
					f.write(data)
	f.close()	
	f=open(FILEOUT,'r')
	for row in f:
		if row.startswith("SB") or row.startswith('"SB') :
			outf.write(row)				
	outf.close()
	print("Finished file read in %s" % (datetime.now() - now,))
	f.close()
main()		
