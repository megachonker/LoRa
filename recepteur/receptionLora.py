from network import LoRa #pour etre en mode LoRa
import socket # pour lire les message recus
import time # pour la gestion des temps d'attente
import os
import struct
from struct import *
from operator import itemgetter#, attrgetter


buffersize=64
logtrames=[]

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, preamble=5, sf=8)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setblocking(True)
#s.settimeout(2)

def unboxing(rawtram)
	global indexRecieve indexManque
	unpackted=unpack("B"+str(buffersize-1)+"s", rawtram)#on stoque la data qui est dans un  tuple dans une variable
	indexRecieve.append(unpackted)
	indexManque.remove(unpackted[0])
	print(unpackted)


#définition d'une fonction d'aquitement
def sendACK(var):
	s.setblocking(False)
	retour=s.recv(buffersize)
	i=0
	while len(retour)<0:
		i+=1
		#temps attente random ?
		print("essait d'envoit n° ",i)
		s.send(var)
		print("attente ack...")
		retour=s.recv(buffersize)
	print("ack Reçus")
	s.setblocking(True)
	return retour


nbtrame=s.recv(buffersize)
print("size data reçus")
indexRecieve=[]
indexManque=[]
for number in range(nbtrame):
	indexManque.append(number)

print("envoit d'un  ackitement")

#Unboxing de la premierre trame de donnée qui fait office d'ackitment
unboxing(sendACK("nombre de trame "+str(nbtrame)))


print("démarage reception")

while True:
	while True:#trame!="STOP"
		#s.send(nombretrames)
		trame=s.recv(buffersize)
		if trame=="STOP":
			print("fin de flux reçus  !")
			break
		else:
			unboxing(trame)
	if(len(indexManque)==0):
		print("plus de trame manquante.")
		break
	 print("trame perdu/restant:")
	print(indexManque)
	#Envoit des trame a  retransmetre
	#+ ajout de la premierre trame reçus (data)
	unboxing(sendACK(indexManque))
	print("début de la rerectption")


print("récéption terminer:")
print("trie:")
indexRecieve.sort(key=itemgetter(0))
print(indexRecieve)
print("écriture en cour:")

with open('imgOut.txt', 'w') as fout: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
	for truc in indexRecieve:
		fout.write(truc[1]) # 3 saut à la ligne pour diferentier les data precedentes
		print("chunk écrit:\n",str(truc[1]))
fout.close() # on referme le fichier

print("transfer  terminer")
