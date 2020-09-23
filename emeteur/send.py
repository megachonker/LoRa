from network import LoRa #pour être en mode LoRa
import socket #pour envoyer des trames
import time # pour la gestion du timer
import struct
from struct import *
import os

buffersize=64

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ,preamble=5, sf=8)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.settimeout(2)
#i=0 #i permet d’identifier le numero de trame et donc les trame perdu
f = open('img.py', 'rb')
msg=b''
nbtrame=(os.path.getsize('img.py')//buffersize-1)+1#nombre de  trame a envoyer

ntn=2# Next trame number
tn=1 #tram number
tl=64#trame lenght

print('sending negosciation')

#send du nombre de trame
s.send(nbtrame)#faire des rery avec des  ack
if  s.recv(buffersize)==nbtrame:

	echo("début de transmition")

	for notrame in range(nbtrame):
		trame=pack("B"+str(tl-1)+"s",notrame, f.read(buffersize-1))#on  concatène le no de trame est le numéro  de tram suivant + les  data
		s.send(trame) # envoie du message
		print("trame"+str(notrame)+"envoiller")

#Déclart l'arret en attente de réponse
trame=s.recv(buffersize)
while trame=='':
    s.send("STOP")
    trame=s.recv(buffersize)
if trame==b'oKay':
	print("start séquance de retrouvaille")
print("sortie!")
