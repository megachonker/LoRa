#!/usr/bin/env python
import machine 			#pour avoir les ID et de l'aléatoir
import os 				# IDK
import time 			# IDK
from network import LoRa#pour géré le module lora
import socket 			#pour envoyer des trames
from sys import exit 	#Gestion des signial
import pycom			#Pour Mieux dormire la nuit DIsable Blink  !
pycom.heartbeat(False)

machineA=b'\x80}:\xc2\xec\xf0'
machineB=b'\x80}:\xc3F`'

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=1,preamble=10, sf=12,tx_power=20,coding_rate=1)#définition dun truc
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora

##déclaration  pour que les  fonction fonctionne
coding=1
bandwidth=1
sf=7
preamble=8
buffersize=64
power=15
timeout=0.5
maxretry=15

#purger les  sockete
def purge():
	import socket# WTFFF   ? ? ? ? ??  ?  ?? ? *w*
	global s, lora #  why not   UwU
	#on Redéfinie le lora a chaque  foit  pour  écraser la dernierre  fonction
	lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=1,preamble=10, sf=12,tx_power=20,coding_rate=1)#définition dun truc
	s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type
	#on  va purge  en  vidant
	s.setblocking(False)
	purgetemp=s.recv(buffersize)
	while purgetemp!=b'':
		purgetemp=s.recv(buffersize)
	s.setblocking(True)

#fonction Permétant d'envoiller un  message est  de  retourner le message  reçus
def sendACK(vara):
	i=0
	while True:
		s.settimeout(0.5)#int(str(machine.rng())[:4])/2000
		i+=1
		s.send(vara)
		print("Main ACK Envoit: "+str(vara), end='')
		#time.sleep(int(str(machine.rng())[:3])/1000)
		try:
			retour=s.recv(buffersize)
			print(" =>"+str(retour))
			break
		except OSError as socket :
			print(" => timeout n° ",i)
			##30 ok
			# if(i==5):
			# 	exit("main connexion  perdu")
	return retour

def sendACKvrf(data, match):
	while True:
		supertruc=sendACK(data)
		if(type(match)==bytes):
			if supertruc == match:
				print("match byte")
				break
			else:
				print("ACKvfr attendue :  ", match, "byte reçus", supertruc)
		if(type(match)==str):
			if supertruc == match.encode() :
				print("match string")
				break
			else:
				print("ACKvfr attendue :  ", match.encode(), "str reçus", supertruc)
	return True

def run():
	lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=1,preamble=10, sf=12,tx_power=20,coding_rate=1)#définition dun truc
	s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora

	print("fc run")
	if machineA == machine.unique_id():
		import send
		sendACKvrf("tla?","jesuisla")
		print("MES parametre:")
		print("sf="+str(sf)+" bandwidth="+str(bandwidth)+" buffersize="+str(buffersize)+" coding_rate="+str(coding)+" preamble="+str(preamble)+" tx_power="+str(power))
		print("éméteur lancement transfer")
		try:
			send.Send(bandwidth,sf,buffersize,preamble,"img.py",power,coding,timeout,maxretry)
			# send.Send.MABITE()
		except SystemExit as e:
			print("exeption "+str(e))

	if machineB == machine.unique_id():
		import receptionLora


		while s.recv(buffersize) != b'tla?':
			pass
		#critique  ?
		s.send("jesuisla")
		s.send("jesuisla")
		print("message  envoiller !")

		print("MES parametre:")
		print("sf="+str(sf)+" bandwidth="+str(bandwidth)+" buffersize="+str(buffersize)+" coding_rate="+str(coding)+" preamble="+str(preamble)+" tx_power="+str(power))
		print("éméteur lancement transfer")

		try:
			#on l'ance le programe de reception
			receptionLora.Rcv.__init__(bandwidth,sf,buffersize,preamble,"azer.txt",power,coding,timeout,maxretry)

		#si on  a  une exeption exit  (fait par trop  de retry )
		except SystemExit as detaille:
			print("Exeption Exit "+str(detaille))

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

#Puissance d'émition en DBm
# tx_power  2 - 20

#preamble nombre signe de  syncro
#[8]
#0-infinit

# coding=1
# bandwidth=0
# sf=7
# preamble=8
# buffersize=64
# power=14

Dcoding=1
Dbandwidth=1
Dsf=7
Dpreamble=8
Dbuffersize=64
Dpower=15

timeout=0.5
maxretry=10

#implémentée les  tableaux  pour  l'interface  graphique
#	   choisie
#		 |  max
#		 |   |	step
#		 |	 |	 |
#buffer=[64,257,64]


#si  desincro  ces  la  mort !
#test toute  les  possibilitée
def benchmark():
	for power in range(Dpower,2,-1):
		for preamble in range(Dpreamble,0,-1):
			for coding in range(Dcoding,5):
				for buffersize in range(Dbuffersize,257,64):#256
					for bandwidth in range(Dbandwidth,3):
						for sf in range(Dsf,6,-1):
							#displayParam("Main")
							purge()
							run()


#REAL MAIN :
while True:
	print("Lancement du benchmark")
	try:
		benchmark()
	#pour  la partie  reception
	except OSError as socket:
		print("Main plus de connection "+str(socket))
	#pour la partie  emeteur
	except SystemExit as error:
		print("main  plus  de nonnexion"+str(error))
