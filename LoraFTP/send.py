#!/usr/bin/env python
#script permettant de transferer  un fichier

from network import LoRa #pour être en mode LoRa
import socket #pour envoyer des trames
import time # pour la gestion du timer
import struct
from struct import *
import os
import hashlib
from sys import exit

class Send:
	"""docstring for Send"""
	def MABITE():
		print("HE  FUCKING   HUGE")
	def __init__(self,bandwidth=0, sf=7, buffersize=64, preamble=8, fichier='img.py',power=14,coding=1,timeout=0.5,maxretry=10):
		#super(Send, self).__init__()
		#self.arg = arg

		#buffersize=64 #taille  du  buffer  de récéption
		# lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_500KHZ,preamble=5, sf=7)#définition dun truc
		lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=bandwidth,preamble=preamble, sf=sf,tx_power=power,coding_rate=coding)#définition dun truc
		print(lora.stats())
		print("bandwidth="+str(bandwidth)+"preamble="+str(preamble)+"sf="+str(sf)+"tx_power="+str(power)+"coding_rate="+str(coding))
		print("bandtith"+str(lora.bandwidth())+"preamble"+str(lora.preamble())+"sf"+str(lora.sf())+"tx_power"+str(lora.tx_power())+"coding_rate"+str(lora.coding_rate()))

		s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora
		f = open(fichier, 'rb')#on va ouvrire l'image qui port l'extention .py (pycom n'axepte pas  des fichier de format image)

		s.setblocking(True)#on dit que l'écoute ou l'envoit bloque le socket
		s.settimeout(timeout) #temps  a attendre avant de  considérer une trame  comme perdu ==> DOIT ETRE BC  PLUS COURT ! ! ! ! ! quelque  MS


		#purger les  sockete
		def purge():
			s.setblocking(False)
			purgetemp=s.recv(buffersize)
			while purgetemp!=b'':
				purgetemp=s.recv(buffersize)
			s.setblocking(True)

		#définition d'une fonction d'aquitement
		def sendACK(vara):
			s.settimeout(timeout)
			i=0
			while True:
				i+=1
				s.send(vara)
				print("ACK Envoit: "+str(vara))
				try:
					retour=s.recv(buffersize)
					#print("ack Reçus")
					break
				except OSError as socket :
					print("ACK timeout n° ",i)
					if(i==maxretry):
						exit("connexion  perdu")
			return retour

		def sendACKvrf(data, match):
			while True:
				mydata=sendACK(data)
				if(type(match)==bytes):
					#print("ACKvfr type  = bytes")
					if mydata == match:
						#print("ACKvfr break")
						break
					else:
						print("ACKvfr attendue :  ", match, " type byte reçus", mydata)
				if(type(match)==str):
					#print("ACKvfr type  = str")
					if mydata == match.encode() :
						#print("ACKvfr break")
						break
					else:
						print("ACKvfr attendue :  ", match.encode(), " type str reçus", mydata)
			return True

		#on va  utiliser la  trame  rentrée   est  la décomposer  est ajouter  les  numero
		def AddToIndexToSend(temp):
			#on va déduire le nombre de valeur a insere dans le tableaux par la longeur /2 car  coder sur 2 bite
			nbcase=int(len(temp)/2)
			#on parse  toute  les valeur reçus   de la  trame
			for i in range(nbcase):##on déduit le nombre de numero en  fonction de la  size de  trame  attention si malformer !
				#on  verrifie   si  la   valeur  existe  bien...
				pointeur=struct.unpack(str(nbcase)+'H',temp)[i]
				if(len(dataMap) >= pointeur):
					#on ajoute  la case  parser a un tableaux  principale
					indexToSend.append(pointeur)#  I n'a  pas a être la et on e st  sensermodifier les h
			#on affiche  la geule de la  trame entierre
			print("trame a renvoiller récéptioner :",indexToSend)
			#return True


		#initialisation de la map de donnée
		dataMap=[]
		f = open(fichier, 'rb')
		stringToHash=var=b''
		sizefile=os.stat(fichier)[6]

		#on déduit le type de  variable a  utiliser en fonction du  nombre de trame total
		if sizefile/(buffersize-1)<256:
			tVarIndex="B" #a  enlever qqd ça marhce
			stVarIndex="B"+str(buffersize-1)
			sVarIndex=1
		elif sizefile/(buffersize-2) < 65536:
			tVarIndex="H"
			stVarIndex="H"+str(buffersize-2)
			sVarIndex=2
		else:
			tVarIndex="L"
			stVarIndex="L"+str(buffersize-4)
			sVarIndex=4

		lenDatamap=os.stat(fichier)[6]//(buffersize-sVarIndex)+1


		#on génère notre dataMap
		while True:
			var=f.read(buffersize-sVarIndex)
			if (var==b''):
				break

			#pour que la fin  du fichier soit fill avec des 0 pour un checksum correct
			ajouter=(buffersize-sVarIndex)-len(var)
			if ajouter!=0:
				var+=ajouter*b'\x00'

			dataMap.append(var)
			stringToHash+=var

		if (len(dataMap)!=lenDatamap):
			print("Erreur  taille  datamap")
			print("len(dataMap)",str(len(dataMap)))
			print("lenDatamap",str(lenDatamap))


		#on va  hasher  datamap
		m = hashlib.sha256()
		m.update(stringToHash)



		# print("array contenant les data maper:")

		###initialisation d'un tableaux qui va lister tout les chunk de data
		#indexToSend[0,1,2,3,4,5,6,7,8,9]
		indexToSend=[]
		for number in range(lenDatamap):
			indexToSend.append(number)

		#send du nombre de trame
		print("send demande de communiquation et annonce de ",str(lenDatamap)," trame a envoiller")

		#on va  utiliser le smiller OwO  pour  taguer qu'on est bien  sur  une  trame qui  annonce la  longeur
		#on  verrifie que la valeur envoilkler est bien la  valleur recus

		purge() ##verifier si utile ?

					##pack('H3s32s'
				#utiliser  un  sendACKvrf ??
		if (int(sendACK(pack('L3s32s',lenDatamap,b'OwO',m.digest())))==lenDatamap):
			print("Nombre de trame OK")
		else:
			print("erreur de trame")

		print("sucès début de transmition")
		while len(indexToSend)!=0:
			chargement=len(indexToSend)
			for notrame in range(len(indexToSend)):
				#on map la trame en  utilisant un octée pour anoncer le nombre de tram est ensuite 63 suivant pour les data
				trame=pack(stVarIndex+"s",indexToSend[notrame], dataMap[indexToSend[notrame]])#buffersize = tl ?
				#j'envoit ma  trame
				s.send(trame)
				print("envoit trame num: "+str(notrame)+"/"+str(chargement)+" index data: "+ str(indexToSend[notrame]))#,"string pur",dataMap[indexToSend[notrame]])

			#on  flush  la  variable  qui stoque  la  précédante  session  d'index a  send
			indexToSend=[]
			#on verifi qu'il y a encore  des data
			indextrame=sendACK("STOP")
			if (indextrame == b'FinTransmition'):
				break

			#reception des trame manquante
			print("detection des trame manquante")

			while True:
				#on  va  décomposer la  trame est l'ajouter  a  la  bd
				AddToIndexToSend(indextrame)
				indextrame = sendACK("indexOKforNext")


				#avec un prochaine opti  doit plus exister
				if (indextrame == b'FinTransmition'):
					break



				#indextrame=s.recv(buffersize)
				# s.settimeout(timeout)###########  Besoin de désincroniser pour que A ecoute et B parle
				print("INFO TrameListe reçus",indextrame)# # DEBUGage

				if (indextrame == b'STOPliste'):
					print("Attente confirmation du  de stop  d'envoit trame")
					sendACKvrf("indexFIN","GO")
					print("SINKRO")
					break

		print("toute numero de  chunck a renvoiller recus:")
		print(indexToSend)
		print("sortie!")
