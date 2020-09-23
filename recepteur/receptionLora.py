from network import LoRa #pour etre en mode LoRa
import socket # pour lire les message recus
import time # pour la gestion des temps d'attente
import os

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, preamble=5, sf=8)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(True)

#fout =  open("imgOut.txt", "wb+")
print("démarage reception")

data=b''
compteur=0
while True:
    chunk=s.recv(128)
    print(chunk.read(1))
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
