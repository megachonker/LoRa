import machine
import os

machineA=b'\x80}:\xc2\xec\xf0'
machineB=b'\x80}:\xc3F`'


#Bande passante
# 2 = LoRa.BW_500KHZ
# 1 = LoRa.BW_250KHZ
# 0 = LoRa.BW_125KHZ
	#	Default  bandwidth  = 0


#Codding rate, Code  redondance ciclique  rapport
# 1 = LoRa.CODING_4_5
# 2 = LoRa.CODING_4_6
# 3 = LoRa.CODING_4_7
# 4 = LoRa.CODING_4_8
	#	Default	coding = 1

#Puissance d'émition en DBm
# tx_power  2 - 20
	#	Default  power=14

#SF  7-12     12 plus faible debit
	#	Default sf=7

#preamble nombre signe de  syncro
	#	Default  preamble=8


# coding=1
# bandwidth=0
# sf=7
# preamble=8
# buffersize=64
# power=14



coding=1
bandwidth=2
sf=7
preamble=8
buffersize=64
power=15

if machineA == machine.unique_id():
	import send
	#bandwidth=2, sf=7, buffersize=64, preamble=5, fichier='azer.txt'
	send.Send.__init__(bandwidth,sf,buffersize,preamble,"img.py",power,coding)


if machineB == machine.unique_id():
	import receptionLora
	receptionLora.Rcv.__init__(bandwidth,sf,buffersize,preamble,"azer.txt",power,coding)
