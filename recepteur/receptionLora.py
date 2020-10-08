from network import LoRa #pour etre en mode LoRa
import socket # pour lire les message recus
import time # pour la gestion des temps d'attente
import os
import struct
from struct import *
#lib manquante
#import operator
#from operator import itemgetter#, attrgetter



buffersize=64
logtrames=[]

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, preamble=5, sf=8)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

def purge():
	#purger les  sockete
	s.setblocking(False)
	purgetemp=s.recv(buffersize)
	while purgetemp!=b'':
		purgetemp=s.recv(buffersize)
	s.setblocking(True)


indexRecieve=[]
indexManque=[]
def unboxing(rawtram):
	global indexRecieve
	global indexManque
	unpackted=unpack("H"+str(buffersize-2)+"s", rawtram)#on stoque la data qui est dans un  tuple dans une variable
	indexRecieve.append(unpackted)
	indexManque.remove(unpackted[0])
	print(unpackted[0])


#définition d'une fonction d'aquitement
def sendACK(vara):
	s.settimeout(2)
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
	s.setblocking(True)
	return retour

def sendACKvrf(data, match):
	while True:
		if sendACK(data) == match :
			break
		else:
			print("Réponse inatentue/Malformed")
	return True


print("Attente Trame Datalenght")
#purge le buffer au  cas ou
purge()
#pour définire nbtrame  on va  accepter que les  trame  étant sur 1 octée en Long
while True:
	try:
		nbtrame=unpack('H',s.recv(buffersize))[0]
		break
	except Exception as e:
		print("Trame Non  attendue")

print("size data reçus", str(nbtrame))

#génération d'un  tableaux qui contien toute les trame
for number in range(int(nbtrame)):
	indexManque.append(number)

print("envoit d'un  ackitement")

#Unboxing de la premierre trame de donnée qui fait office d'ackitment
unboxing(sendACK(str(nbtrame)))



print("démarage reception")


s.setblocking(True)
while True:
	while True:#trame!="STOP"
		#s.send(nombretrames)
		trame=s.recv(buffersize)
		if trame==b'STOP':
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

	while len(indexManque):
		i=0
		temp=b''
		while i<32 && len(indexManque):
			temp+=pack('H',indexManque[0])
			indexManque.pop(0)
			i+=1
		temp=struct.pack('H',i)+temp
		sendACKvrf(temp,"indexOK")#a la place de indexOk peut metre un ckecksum
	sendACKvrf(temp,"indexFIN")



	unboxing(sendACK()


	print("début de la rerectption")


print("récéption terminer:")
print("trie:")
indexRecieve.sort(key=itemgetter(0))#sor besoin lib ?
print(indexRecieve)
print("écriture en cour:")

with open('imgOut.txt', 'w') as fout: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
	for truc in indexRecieve:
		fout.write(truc[1]) # 3 saut à la ligne pour diferentier les data precedentes
		print("chunk écrit:\n",str(truc[1]))
fout.close() # on referme le fichier

print("transfer  terminer")
