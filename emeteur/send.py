from network import LoRa #pour être en mode LoRa
import socket #pour envoyer des trames
import time # pour la gestion du timer
import struct
from struct import *
import os

buffersize=64 #taille  du  buffer  de récéption

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ,preamble=5, sf=8)#définition dun truc
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)#définition d'un socket réseaux de type lora
f = open('img.py', 'rb')#on va ouvrire l'image qui port l'extention .py (pycom n'axepte pas  des fichier de format image)
s.setblocking(True)
s.settimeout(2)
#définition d'une fonction d'aquitement
def sendACK(vara):
	i=0
	while True:
		i+=1
		s.send(str(vara))
		print("attente ack...")
		try:
			retour=s.recv(buffersize)
			print("ack Reçus")
			break
		except OSError as socket :
			print("timeout try n° ",i)
	return retour

#nbtrame=(os.path.getsize('img.py')//buffersize-1)+1#nombre de  trame a envoyer

#initialisation de la map de donnée

# totalChunk=(os.stat('img.py')[0]//(buffersize-1))+1
# for nbChunk in range(totalChunk):
# 	print("maping de du chunk n°",nbChunk)
# 	dataMap.append(f.read(buffersize-32))
# 	print(dataMap[nbChunk])


dataMap=[]
f = open('img.py', 'rb')
var=b'e'
while var!=b'':
	var=f.read(buffersize-1)
	dataMap.append(var)


# print("array contenant les data maper:")
# print(dataMap)

###initialisation d'un tableaux qui va lister tout les chunk de data
#indexToSend[0,1,2,3,4,5,6,7,8,9]
indexToSend=[]
for number in range(len(dataMap)):
	indexToSend.append(number)
print("initial index tableaux sending intialiser !")
print(indexToSend)
#send du nombre de trame
print("send demande de communiquation et annonce de ",str(len(dataMap))," trame a envoiller")

print(sendACK(len(dataMap)))#faire des rery avec des  ack

print("sucès début de transmition")
while len(indexToSend)!=0:
	for notrame in range(len(indexToSend)):
		#on map la trame en  utilisant un octée pour anoncer le nombre de tram est ensuite 63 suivant pour les data
		trame=pack("H"+str(buffersize-2)+"s",notrame, dataMap[indexToSend[notrame]])#buffersize = tl ?
		#f.read(buffersize-1))#on  concatène le no de trame est le numéro  de tram suivant + les  data
		s.send(trame) # envoie du message
		print("trame n°"+str(notrame))
	print("toute les trame on étée envoiler")
	print("envoit de trame de fin")
	missingTrame=sendACK("STOP")

	#reception des trame manquante
	indexToSend=s.recv(buffersize)
	print(type(indexToSend))
	print("Début retransmition !")


print("sortie!")
