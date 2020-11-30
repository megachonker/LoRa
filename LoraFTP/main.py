import machine
import os

machineA=b'\x80}:\xc2\xec\xf0'
machineB=b'\x80}:\xc3F`'

#Start gps thread

#test=[test3, test2, test3]
#while test not empty
# while test:

#set param from test
#pop this test from test



#tx_power
#coding_rate
# coding_rate=[]
    # LoRa.CODING_4_5
    # LoRa.CODING_4_6
    # LoRa.CODING_4_7
    # LoRa.CODING_4_8
#run test on both machine

	##consigne du de la passe

# 2 = LoRa.BW_500KHZ
# 1 = LoRa.BW_250KHZ
# 0 = LoRa.BW_125KHZ



bandwidth=1
sf=8
preamble=5
buffersize=64
# tx_power  2 - 20
power=15

if machineA == machine.unique_id():
	import send
	#bandwidth=2, sf=7, buffersize=64, preamble=5, fichier='azer.txt'
	send.Send.__init__(bandwidth,sf,buffersize,preamble,"img.py",power)



if machineB == machine.unique_id():
	import receptionLora
	receptionLora.Rcv.__init__(bandwidth,sf,buffersize,preamble,"azer.txt",power)
