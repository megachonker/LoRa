#!/usr/bin/env python
#on  importe un  librarie  qui  va permetre  de  trier  des tableaux de  turple
#lib ou j'ai  du  retirer des  fonction  de  python  3.7 pour l'adapter sur lopy 2.7
#de ce fait  je pourait la simplifier  au stricte minimum donc a voir  .....
from operator import itemgetter#, attrgetter
import gps				#permet d'utiliser le gps

from network import LoRa# pour etre en mode LoRa
import socket 			# gestion des socket de lora
import time 			# gestion temps Débit Crono etc
import os 				# gestion de  fichier
import hashlib			# permet  d'utiliser des  fonction de hashage
from sys import exit 	#permet de d'envoiler des  signal de sortie
import struct  			# gestion des  structure  de  trame  sert  notament a  aranger des donnnée dans une suite de type  binaire
from struct import * 	# IDK

from sys import exit


#
class Rcv:
	"""docstring for Send"""


	def __init__(bandwidth=0, sf=7, buffersize=64, preamble=8, fichier='azer.txt',power=14,coding=1,timeout=0.5,maxretry=10):

		# fichier='azer.txt'
		# buffersize=64
		#buffersize=64 #taille  du  buffer  de récéption
		# lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_500KHZ,preamble=5, sf=7)#définition dun truc
		lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=bandwidth,preamble=preamble, sf=sf,tx_power=power,coding_rate=coding)#définition dun truc
		s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora
		print(lora.stats())
		print("bandwidth="+str(bandwidth)+"preamble="+str(preamble)+"sf="+str(sf)+"tx_power="+str(power)+"coding_rate="+str(coding))
		print("bandtith"+str(lora.bandwidth())+"preamble"+str(lora.preamble())+"sf"+str(lora.sf())+"tx_power"+str(lora.tx_power())+"coding_rate"+str(lora.coding_rate()))

		# #ne pouvant avoir une résolution en  dessou de  la  seconde  sans passer  par des  tick ces mort
		# ltime=int()
		# def crono():
		# 	global ltime
		# 	b=time.time()
		# 	out=b-ltime
		# 	ltime=b
		# 	return out

		#fonction  permetant de vider  le buffer  qui peut poser  des soucis RArement mais  ça peut vite  être contrégniant dans le cas échéant
		def purge():
			#purger les  sockete
			s.setblocking(False)
			purgetemp=s.recv(buffersize)
			while purgetemp!=b'':
				purgetemp=s.recv(buffersize)
			s.setblocking(True)


		#declaration
		startAt=0
		nbtrame=0
		indexManque=[]
		indexRecieve=[]
		stVarIndex=""
		tVarIndex=""
		playloadsize=0 #autodetect

		arrayStat=[]


		def unboxing(rawtram):

			#on verifie si on peut umpack la trame
			try:			#"H"+str(buffersize-2)
				unpackted=unpack(stVarIndex+"s", rawtram)#on stoque la data qui est dans un  tuple dans une variable

			except ValueError:#OSError
				print("Unboxing: raw: "+str(rawtram))
			else:
				#pour le premier tour  on empege une division par zero
				totaltemp=time.time()-startAt
				if totaltemp == 0:
					totaltemp=1
				totaldata=(len(indexRecieve)+1)*int(playloadsize)

				# arrayStat.append((unpackted[0], (totaldata/totaltemp), time.time(), gps.coord,lora.stats()[1], lora.stats()[2]))
				print("Unboxing: chunk "+str(unpackted[0])+" Download: "+str((len(indexRecieve)+1)/nbtrame*100)+"% débit moyen: "+str(totaldata/totaltemp)+"octée/s "+"position: "+str(gps.coord)+" power reçus "+str(lora.stats()[1])+"dBm, SNR: "+str(lora.stats()[2])+"dB ",  end='')

				#pour  verifier si  un  packet DOUBLON OU est malformer  on verifi  que l'index  existe  bien
				if unpackted[0] in indexManque:
					#on vérifie si ces bien une trame  de data
					#try  plus nécésaire ?
					try:
						#on archive le packet recus
						indexRecieve.append(unpackted)
						#caclule en%  des trame perdu #####peut être  opti
						print("packet  perdu  "+str(lostpacket(unpackted[0]))+"%")
						#on  suprime  le  packet  de la  liste de  packet a  renvoiller
						indexManque.remove(unpackted[0])
					except ValueError:
						#debug value
						print("List des  packet a receptioner ",str(indexManque))
						# print("liste des packet déja  receptioner", str(indexRecieve))
						print("chunk  a  suprimer :",unpackted[0])
						print("packet unpackted", str(unpackted))
						print("raw packet", str(rawtram))
				else:
					#ajouter un compteur pour dire  q'uon a un packet  corrompu  pour les  packet  perdu !!
					print("Unboxing: BAD INDEX Duplicate Packet or Malformed  packet ?")

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
					time.sleep(0.1)
					if(i==maxretry):
						exit("connexion  perdu")
			#s.setblocking(True)
			return retour


		def sendACKvrf(data, match):
			while True:
				mydata=sendACK(data)
				if(type(match)==bytes):
					if mydata == match:
						break
					else:
						print("ACKvfr attendue :  ", match, "is byte  reçus", mydata)
				if(type(match)==str):
					if mydata == match.encode() :
						break
					else:
						print("ACKvfr attendue :  ", match.encode(), "  is str  reçus", mydata)
			return True

		#fonction qui  va  calculer  les   packet perdu
		def lostpacket(id):
			indexlost=indexManque.index(id)
			for a in range(len(indexRecieve)):
				if(indexRecieve[a][0]==id):
					indexadd=a
					break
			#trame perdu +  trame  reception  =  nombre trame  totale
			totaltramesend=indexadd+indexlost+1
			#raport  de perte
			return (indexlost+1)/totaltramesend*100

		def writeTo(name):
			# global indexRecieve #ABON ?
			#on essay suprime le fichier si il existe
			#flmee de  chercherune fonction  de  test  si  le fichier existe avant  de le suprimer
			name=str(name)
			try:
				#on  essaye  de le supprimer
				os.remove(name)
				print("fichier supprimer")
			except OSError as e:
				print("fichier inéxistant")

			#on  va  ouvrire  le fichiuer
			with open(name, 'w') as fout: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
				#on va  parser notre  tableaux de  tuple
				for truc in indexRecieve:
					#on  va selecioner  la  2eme valeur de  notre tuple  (les data)
					fout.write(truc[1])
					# on referme le fichier proprement
			fout.close()


		print("Attente Trame Datalenght")
		#purge le buffer au  cas ou
		purge()

		s.settimeout(10)##EXPERIMENTAL POUR PAS BLOQUER
		#pour définire nbtrame  on va  accepter que les  trame  étant sur 1 octée en Long
		varnul=0
		while True:
			try:
				nbtrame=unpack('L3s32s',s.recv(buffersize))
				if nbtrame[1]==b'OwO':
					checksum=nbtrame[2]
					nbtrame=nbtrame[0]
					break
			except Exception as e:
				print("INITIALISATION: nombretrame err : Trame Non  attendue",str(nbtrame))
				varnul+=1
				if(varnul==maxretry):
					exit("connexion  perdu")
		print("nombre de trame", str(nbtrame))

		s.settimeout(timeout)

		#on déduit le type de  variable a  utiliser en fonction du  nombre de trame total
		if nbtrame<256:
			tVarIndex="B"
			stVarIndex="B"+str(buffersize-1)
			playloadsize=str(buffersize-1)
		elif (nbtrame<65536):
			tVarIndex="H"
			stVarIndex="H"+str(buffersize-2)
			playloadsize=str(buffersize-1)
		else:
			tVarIndex="L"
			stVarIndex="L"+str(buffersize-4)
			playloadsize=str(buffersize-1)


		#génération d'un  tableaux qui contien toute les trame
		for number in range(int(nbtrame)):
			indexManque.append(number)


		print("envoit d'un  ackitement")
		#Unboxing de la premierre trame de donnée qui fait office d'ackitment
		purge()
		startAt=time.time()
		unboxing(sendACK(str(nbtrame)))


		print("démarage reception")
		startAt=time.time()
		#je  demande explicitement d'écouter j'usqua se que je  recois une trame
		s.setblocking(True)
		while True:

			#tant que l'éméteur veux envoiller des donnée
			while True:
				#je  reçois ma trame
				##experimentale
				s.settimeout(10)##
				trame=s.recv(buffersize)
				s.settimeout(timeout)##

				#quand l'éméteur  a fini ENvoit de  stop pour  passer a la partie suivante
				if trame==b'STOP':
					print("fin de flux reçus  !")
					#s.send("OK")
					break
				#sinon on traite la trame normalement
				else:
					#on va traiter la  trame  recus
					unboxing(trame)

			print("Packet perdu"+str(len(indexManque)/(len(indexRecieve)+len(indexManque))*100)+"%")

			#si il  n'y a plus de trame manquante
			if(len(indexManque)==0):
				print("plus de trame manquante.")
				#sendACK("STOP")
				#on va indiquer a l'éméteur que ces fini
				s.send("STOP")
				#on sort de toute mes boucle  affain  de  passer a  au  trie  des data
				break

			print("trame perdu/restant:")
			print(indexManque)


			#Envoit des trame a  retransmetre
			#+ ajout de la premierre trame reçus (data)

			#on copy explicitement le  précédant tableaux dans un  nouveaux
			indexManquetosend=indexManque.copy()

			time.sleep(0.250)

			#tant qu'il reste des trame dans la liste TEMPORAIRE des trame qui  manque
			while len(indexManquetosend):
				#vieux conmpeur
				i=0
				#on initialise ma future  trame en déclarant que ça serat du  binaire
				temp=b''

				#je  crée  une  trame  qui  sera  égale  a la taille  du buffer ou inferieure  tant qu'il  me   reste des valeur  a y metre
				##	  i<(buffersize/2) #mieux ? ###########################
				while i<32 and len(indexManquetosend):
					#je rajoute de nouveaux Idex de trame  manquante  a ma trame  éxistante
					temp+=pack('H',indexManquetosend[0])
					#je  suprime  la valeur  ajouter
					indexManquetosend.pop(0)
					i+=1
				#je  m'assurt  que l'éméteur a  bien recus la  trame  qu'il  a recus  est qu'il n'es pas  perdu  [utile quand je chercherer a débusquer les trame  malformer]
				sendACKvrf(temp,"indexOKforNext")#######a la place de indexOk peut metre un ckecksum
				print("INDEXE echangée  "+str(i)+" liste des chunck")
			#on envoit a  l'éméteur un  signial  indiquant qu'il n'y a plus  de  trame a  envoiller est on verifi qu'il  est bien sincro

			print("on STOP la l'émition")
			sendACKvrf("STOPliste","indexFIN")
			print("liste  trame manquante bien  réceptioner") ##  ligne 160  et  163 redondante ?
			print(indexManque)
			#on envoit une  trame  pour  trigguer l'éméteur pour qu'il  passe  en  mode émition  et on traite  la premierre valeur reçus
			###metre  un  time  out a  l'éméteur


			#on commence  la  reception qqd  on est  sur d'avoir  du  binaire
			tmpp=b'indexFIN'
			while tmpp==b'indexFIN':
				print(tmpp)#debug
				tmpp=sendACK("GO")
				print(tmpp)#debug
			unboxing(tmpp)

			print("début de la rerectption")
####

		print("récéption terminer:")

		purge()
		s.setblocking(False)
		s.send("FinTransmition")
		s.send("FinTransmition")
		s.send("FinTransmition")

		stopAt=time.time()

		print("trie:")
		#on va trier  en fonction  du  1er élémenet du tuple du tableaux
		indexRecieve.sort(key=itemgetter(0))
		#print(indexRecieve)

		datafile=b''
		for truc in indexRecieve:
			if (truc[1]==b''):
				break
			datafile+=truc[1]
		print("durée du transfer:",str(stopAt-startAt),"seconde débit moyen de", str(len(datafile)/(stopAt-startAt)),"octée/s")
		m = hashlib.sha256()
		m.update(datafile)

		print("################")
		if checksum==m.digest():
			print("Fichier intègre !")
		else:
			print("/!\ bad checksum ! /!\ ")
		print("################")

		print("Phase écriture:")

		writeTo(fichier)

		# print("durée du transfer:",str(stopAt-startAt),"débit moyen de", str(os.stat("imgOut.txt")[5]/(stopAt-startAt)))

		print("transfer  terminer")


		print(str(indexRecieve))
