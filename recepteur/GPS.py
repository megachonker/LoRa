import machine # pour pouvoir géré des fichier
import pycom # pour le gestion du module pycom (dans notre cas la led)
import socket # pour lire les message recus
import time # pour la gestion des temps d'attente
from network import LoRa #pour etre en mode LoRa
from L76GNSS import L76GNSS # pour le module gps
from pytrack import Pytrack # shield du modul gps

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, preamble=20, sf=12 ) #configuration initiale
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
py = Pytrack() # initialisation du shield
l76 = L76GNSS(py, timeout=1) # initialisation GPS

pycom.heartbeat(False) # on stop les pulsations indiquant que le module est allumé
pycom.rgbled(0x7f0000) # on initialise la led en rouge

with open('data.txt', 'a') as datafile: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
    datafile.write("\n\n\n") # 3 saut à la ligne pour diferentier les data precedentes
datafile.close() # on referme le fichier

while (True):
    s.setblocking(False) # module en position d'écoute
    data = s.recv(64) # data avec un buffer de 64
    time.sleep(4) # patienter 2 sec pour que les data arrive
    coord = l76.coordinates() #récupération des coordoné GPS
    if coord == (None,None) and data == b'':
        pycom.rgbled(0x7f0000) # rouge => - Coordoné ; - data

    if coord != (None,None) and data == b'':
        pycom.rgbled(0x0000ff) # bleu   => + Coordoné ; - data

    if coord == (None,None) and data != b'':
        pycom.rgbled(0xffff00) # jaune  => - Coordoné ; + data

    if coord != (None,None) and data != b'':
        pycom.rgbled(0x007f00) # vert   => + Coordoné ; + data

    txt=coord,lora.stats(),data
    with open('data.txt', 'a') as datafile:
        tx=str(txt)+"\n" #on note les coordonées GPS, les statistique du module et les data recu
        datafile.write(tx)
    datafile.close()
    print(txt) # lorsque l'on est brancher au pc, on observe les data mis dans le fipy
