#!/usr/bin/env python
#script permettant de transferer  un fichier

from network import LoRa#pour être en mode LoRa
import socket 			#pour envoyer des trames
import time 			# pour la gestion du timer
import struct			#permet d'utiliser  une  structure sur  du  binaire
from struct import *	# IDK
import os 				#  IDK
import hashlib			#fait des hash
from sys import exit 	#sortie  personaliser

class Send:

	def __init__(self,bandwidth=0, sf=7, buffersize=64, preamble=8, fichier='img.py',power=14,coding=1,timeout=0.5,maxretry=10):

		lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=bandwidth,preamble=preamble, sf=sf,tx_power=power,coding_rate=coding)#définition dun truc
		#print("bandwidth="+str(bandwidth)+"preamble="+str(preamble)+"sf="+str(sf)+"tx_power="+str(power)+"coding_rate="+str(coding))
		print("PARAMETRE EMETEUR")
		print("bandtith"+str(lora.bandwidth())+"preamble"+str(lora.preamble())+"sf"+str(lora.sf())+"tx_power"+str(lora.tx_power())+"coding_rate"+str(lora.coding_rate()))

		s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora
		f = open(fichier, 'rb')#on va ouvrire l'image qui port l'extention .py (pycom n'axepte pas  des fichier de format image)

		s.setblocking(True)#on dit que l'écoute ou l'envoit bloque le socket
		s.settimeout(timeout) #trouver un opotimal


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
				print("ACK Envoit: "+str(vara), end='')
				try:
					retour=s.recv(buffersize)
					print(" =>"+str(retour))
					return retour
				except OSError as socket :
					print(" => timeout n° ",i)
					time.sleep(0.1)# UTILE ?
					if(i==maxretry):
						exit("connexion  perdu")

		def sendACKvrf(data, match):
			while True:
				mydata=sendACK(data)
				if(type(match)==bytes):
					if mydata == match:
						break
					else:
						print("ACKvfr attendue :  ", match, " type byte reçus", mydata)
				if(type(match)==str):
					if mydata == match.encode() :
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

		def resizevar(nbtrame):
			global tvar,tVarType,playloadsize,stVarIndex
			if nbtrame<256:
				tvar=1
				tVarType="B"
				playloadsize=str(buffersize-tvar)
				stVarIndex=tVarType+playloadsize
			elif (nbtrame<65536):
				tvar=2
				tVarType="H"
				playloadsize=str(buffersize-tvar)
				stVarIndex=tVarType+playloadsize
			else:
				tvar=4
				tVarType="L"
				playloadsize=str(buffersize-tvar)
				stVarIndex=tVarType+playloadsize

		#initialisation de la map de donnée
		indexToSend=[]
		def datamapinit():
			nonlocal indexToSend
			global dataMap
			dataMap=[]
			stringToHash=var=b''
			#on  ouvre le fichier
			f = open(fichier, 'rb')
			#la  taille  du fichier a  envoiller
			sizefile=os.stat(fichier)[6]
			#on déduit le type de  variable a  utiliser en fonction du  nombre de trame total
			resizevar(sizefile/(buffersize-1))
			#déduit la  taille  de n otre tableaux
			global lenDatamap
			lenDatamap=sizefile//(buffersize-tvar)+1
			#on génère notre dataMap
			while True:
				var=f.read(buffersize-tvar)
				if (var==b''):
					break

				#pour que la fin  du fichier soit fill avec des 0 pour un checksum correct
				ajouter=(buffersize-tvar)-len(var)
				if ajouter!=0:
					var+=ajouter*b'\x00'

				dataMap.append(var)
				stringToHash+=var

			if (len(dataMap)!=lenDatamap):
				print("Erreur  taille  datamap")
				print("len(dataMap)",str(len(dataMap)))
				print("lenDatamap",str(lenDatamap))

			#on va  hasher  datamap
			global mhashed
			mhashed = hashlib.sha256()
			mhashed.update(stringToHash)

			###initialisation d'un tableaux qui va lister tout les chunk de data
			#indexToSend[0,1,2,3,4,5,6,7,8,9]
			#global indexToSend
			indexToSend=[]
			for number in range(lenDatamap):
				indexToSend.append(number)

		#MAIN
		purge()
		datamapinit()
		print("send demande de communiquation et annonce de ",str(lenDatamap)," trame a envoiller")
		#send du nombre de trame
		#on va  utiliser le smiller OwO  pour  taguer qu'on est bien  sur  une  trame qui  annonce la  longeur
		#on  verrifie que la valeur envoilkler est bien la  valleur recus
			# sendACKvrf(pack('L3s32s',lenDatamap,b'OwO',m.digest()),str(lenDatamap))
		sendACKvrf(pack('L3s32s',lenDatamap,b'OwO',mhashed.digest()),str(lenDatamap))

		# if (str(sendACK(pack('L3s32s',lenDatamap,b'OwO',mhashed.digest())))==str(lenDatamap)):
		# 	pass
		# else:
		# 	print("erreur de trame")

		print("début de transmition")
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
				print("debug  idex"+str(indextrame))
				indextrame = sendACK("indexOKforNext")


				#avec un prochaine opti  doit plus exister
				if (indextrame == b'FinTransmition'):
					break

				#indextrame=s.recv(buffersize)
				#print("INFO TrameListe reçus",indextrame)# # DEBUGage

				if (indextrame == b'STOPliste'):
					#print("Attente confirmation du  de stop  d'envoit trame")
					sendACKvrf("indexFIN","GO")
					#print("SINKRO")
					break

		print("Upload terminer !")
		
