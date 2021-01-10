import machine
import os
import time
#pour gestion  des  message
from network import LoRa #pour être en mode LoRa
import socket #pour envoyer des trames
#pour  les  signial  de sortie
from sys import exit

import pycom
##Juste pour pouvoire  mieux dormire la  nuit et pas  avoire des   sapin de  noel  en   continue  !
pycom.heartbeat(False)

machineA=b'\x80}:\xc2\xec\xf0'
machineB=b'\x80}:\xc3F`'

#DOIT etre equivalent a la passe
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=0,preamble=10, sf=12,tx_power=20,coding_rate=1)#définition dun truc
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora

##initialisation pour  que  ça  run  mais ces  par  défaut  nbormalent
coding=1
bandwidth=1
sf=7
preamble=8
buffersize=64
power=15
timeout=0.5
maxretry=10



def sendACK(vara):
	s.settimeout(2)
	i=0
	while True:
		i+=1
		s.send(vara)
		print("Main ACK Envoit: "+str(vara))
		try:
			retour=s.recv(buffersize)
			break
		except OSError as socket :
			print("Main ACK timeout n° ",i)
			##30 ok
			if(i==5):
				exit("main connexion  perdu")
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
		except SystemExit as e:
			#on  abolis d'exeption
			print("exeption "+str(e))


		# #attend j'usqua un  message ||durré d'un transfer au pire
		# #on attend j'usqua 30 second une rep concluante
		# s.settimeout(30)
		# #on verifie que ça soit pas une interférance
		# avar=""
		# while avar!= b'tla?':
		# 	print("en  attante  de trame")
		# 	#si timed out  l'erreur remonte j'usqaux main benchmark
		# 	avar=s.recv(64)
		# 	print(avar)
		# #si l'on recois le bon  message on va dire au  module  oposer  que nous somme  la
		# 	#30 foit
		# for a in range(10):
		# 	print("jesuisal")
		# 	s.send("jesuisla")
		# #Puisque nous avon s  reçus un  des 30 message  nous parton du  principe que nous avonc 50% de chance si ces le dernier message  que l'on avais  reus que l'autre reçois
		# 	#si on a reçus un des 30 message ça marche dansles 2 sens
		# #on   part du principe qu'il en a reçus au moin UN !
		# print("la  reception ces  bien  derouler")


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

Dcoding=1
Dbandwidth=1
Dsf=7
Dpreamble=8
Dbuffersize=64
Dpower=15

timeout=0.5
maxretry=10


#si  desincro  ces  la  mort !
def benchmark():
	for power in range(Dpower,2,-1):
		print("power: "+str(power), end=', ')
		for preamble in range(Dpreamble,0,-1):
			print("preamble: "+str(preamble), end=', ')
			for coding in range(Dcoding,4):
				print("coding: "+str(coding), end=', ')
				for buffersize in range(Dbuffersize,256,8):
					print("buffersize: "+str(buffersize), end=', ')
					for bandwidth in range(Dbandwidth,3):
						print("bandwidth: "+str(bandwidth), end=', ')
						for sf in range(Dsf,6,-1):
							print("sf: "+str(sf), end='\n')
							print("on  lance une  run ?")
							run()

while True:
	try:
		print("on  veux benchmark ?")
		benchmark()
	#pour  la partie  reception
	except OSError as socket:
		print("Main plus de connection "+str(socket))
	#pour la partie  emeteur
	except SystemExit as error:
		print("main  plus  de nonnexion"+str(error))
