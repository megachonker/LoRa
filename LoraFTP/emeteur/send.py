from network import LoRa #pour être en mode LoRa
import socket #pour envoyer des trames
import time # pour la gestion du timer
import struct
from struct import *
import os
import hashlib

buffersize=64 #taille  du  buffer  de récéption

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_500KHZ,preamble=5, sf=7)#définition dun truc
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora
f = open('img.py', 'rb')#on va ouvrire l'image qui port l'extention .py (pycom n'axepte pas  des fichier de format image)
s.setblocking(True)#on dit que l'écoute ou l'envoit bloque le socket
s.settimeout(2) #temps  a attendre avant de  considérer une trame  comme perdu


def purge():
	#purger les  sockete
	s.setblocking(False)
	purgetemp=s.recv(buffersize)
	while purgetemp!=b'':
		purgetemp=s.recv(buffersize)
	s.setblocking(True)



#définition d'une fonction d'aquitement
def sendACK(vara):
	i=0
	while True:
		i+=1
		s.send(vara)#LA ?
		print("attente ack...")
		try:
			retour=s.recv(buffersize)
			print("ack Reçus")
			break
		except OSError as socket :
			print("timeout try n° ",i)
	return retour

#initialisation de la map de donnée

dataMap=[]
f = open('img.py', 'rb')
azer=var=b''
while True:
	var=f.read(buffersize-2)
	if (var==b''):
		break

	#pour que la fin  du fichier soit fill avec des 0 pour un checksum correct
	ajouter=(buffersize-2)-len(var)
	if ajouter!=0:
		var+=ajouter*b'\x00'
	dataMap.append(var)
	azer+=var

#on va  hasher  datamap
m = hashlib.sha256()
m.update(azer)

# print("array contenant les data maper:")
# print(dataMap)

###initialisation d'un tableaux qui va lister tout les chunk de data
#indexToSend[0,1,2,3,4,5,6,7,8,9]
indexToSend=[]
for number in range(len(dataMap)):
	indexToSend.append(number)
print("tableaux d'envoit:")
print(indexToSend)

#send du nombre de trame
print("send demande de communiquation et annonce de ",str(len(dataMap))," trame a envoiller")

#on va  utiliser le smiller OwO  pour  taguer qu'on est bien  sur  une  trame qui  annonce la  longeur
#on  verrifie que la valeur envoilkler est bien la  valleur recus

##temporaire ?
purge()
s.settimeout(2)


if (int(sendACK(pack('H3s32s',len(dataMap),b'OwO',m.digest())))==len(dataMap)):
	print("Nombre de trame OK")
else:
	print("erreur de trame")

print("sucès début de transmition")
while len(indexToSend)!=0:
	chargement=len(indexToSend)
	for notrame in range(len(indexToSend)):
		#on map la trame en  utilisant un octée pour anoncer le nombre de tram est ensuite 63 suivant pour les data
		trame=pack("H"+str(buffersize-2)+"s",indexToSend[notrame], dataMap[indexToSend[notrame]])#buffersize = tl ?
		#j'envoit ma  trame
		s.send(trame)
		print("envoit trame num: "+str(notrame)+"/"+str(chargement)+" index data: "+ str(indexToSend[notrame]))#,"string pur",dataMap[indexToSend[notrame]])

	#truc a  dégager  #FAire refleciton     doit servier a
	missingTrame=sendACK("STOP")
	#on va optimiser la bande passante en transformant la liste en  suite de chifre

	#divise par 2  le  buffer car on  a  des short de  2  octée

	#reception des trame manquante
	print("detection des trame manquante")
	indexToSend=[]
	while True:
		#on indique que  l'on écoute sagement
		s.setblocking(True)
		#on enleve le time  out
		s.settimeout(None)
		#on attend une trame
		temp=s.recv(buffersize)
		s.settimeout(0.1)###########  Besoin de désincroniser pour que A ecoute et B parle
		#print("mssage des message",temp)########  ?
		if (temp == b'STOP'):
			print("attente destinataire ok....")
			sendACK("indexFIN")
			break
		#on va déduire le nombre de valeur a insere dans le tableaux par la longeur /2 car  coder sur 2 bite
		nbcase=int(len(temp)/2)
		for i in range(nbcase):##on déduit le nombre de numero en  fonction de la  size de  trame  attention si malformer !
			indexToSend.append(struct.unpack(str(nbcase)+'H',temp)[i])#  I n'a  pas a être la et on e st  sensermodifier les h
		print("envoit confirmation reception")
		sendACK("indexOKforNext")
	print("toute numero de  chunck a renvoiller recus:")
	print(indexToSend)


print("sortie!")
