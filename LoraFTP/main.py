import machine
import os

machineA=b'\x80}:\xc2\xec\xf0'
machineB=b'\x80}:\xc3F`'

#Start gps thread

#test=[test3, test2, test3]
#while test not empty
while test:
	
	#set param from test
	#pop this test from test

	#run test on both machine
	if machineA == unique_id():

		#send setting on send.py 
		machine.main('emeteur/send.py')
		print("lol")

	elif machineB == unique_id():
		machine.main('recepteur/receptionLora.py')