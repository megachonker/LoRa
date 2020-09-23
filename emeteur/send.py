from network import LoRa #pour être en mode LoRa
import socket #pour envoyer des trames
import time # pour la gestion du timer
import struct

buffersize=128

print('start Sending')

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ,preamble=5, sf=8)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(True)
#i=0 #i permet d’identifier le numero de trame et donc les trame perdu
f = open('img.py', 'rb')

compteur=0

msg=b''

while True:
	compteur+=1
	msg=bytes([compteur])
	msg+=f.read(buffersize-1)
	print(compteur)#,msg) # visulisation de celui-ci si on est branché à un PC
	if msg == b'':
		s.send("STOP") # envoie du message
		break
	s.send(msg) # envoie du message
	#msg=str(i)+"abcdefghijklmnopqrstuvwxyz0123456789" #chaine à envoyer
	#i+=1
	#time.sleep(0.1) # temps d’attente
print("sortie!")
