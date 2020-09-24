from network import LoRa #pour etre en mode LoRa
import socket # pour lire les message recus
import time # pour la gestion des temps d'attente
import os
import struct
from struct import *

buffersize=64
logtrames=[]

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, preamble=5, sf=8)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

s.setblocking(True)
#s.settimeout(2)

#définition d'une fonction d'aquitement
def sendACK(var):
	s.setblocking(False)
	retour=s.recv(buffersize)
	i=0
	while len(retour)<0:
		i+=1
		print("essait d'envoit n° ",i)
		s.send(var)
		print("attente ack...")
		retour=s.recv(buffersize)
	print("ack Reçus")
    s.setblocking(True)
	return retour


nbtrame=s.recv(buffersize)
s.send("nombre de trame "+str(nbtrame))

indexRecieve=[]
print("démarage reception")


while True:#trame!="STOP"
    s.send(nombretrames)
    trame=s.recv(buffersize)
    if trame=="STOP":
        print("fin de flux reçus  !")
        break
    else:
        unpackted=unpack("B"+str(buffersize-1)+"s", trame)#on stoque la data qui est dans un  tuple dans une variable
        #if(indexRecieve.index(unpackted))
        indexRecieve.append(unpackted)
        print(unpackted)


logtrames.append(trame)
#for notrame in range(nbtrame-1):
s.setblocking(True)
while True:
    trame=s.recv(buffersize)
    if trame=b'STOP':
        s.send('oKay')
        break
    logtrames.append(trame)

unpack("B"+str(buffersize-1)+"s", trames)#on  concatène le no de trame est le numéro  de tram suivant + les  data


data=b''
compteur=0
while True:
    chunk=s.recv(128)
    print(chunk[1])
    if(len(chunk)>0):
        compteur+=1
        print(compteur)
        if chunk==b'STOP':
            break
        data+=chunk

with open('imgOut.txt', 'w') as fout: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
    fout.write(data) # 3 saut à la ligne pour diferentier les data precedentes
fout.close() # on referme le fichier


#fout.write(data)
print("transfer  terminer")
