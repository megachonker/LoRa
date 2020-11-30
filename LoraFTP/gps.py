import machine # pour pouvoir géré des fichier
import pycom # pour le gestion du module pycom (dans notre cas la led)
import time # pour la gestion des temps d'attente
from L76GNSS import L76GNSS # pour le module gps
from pytrack import Pytrack # shield du modul gps
import _thread

py = Pytrack() # initialisation du shield
l76 = L76GNSS(py, timeout=5) # initialisation GPS
time.sleep(2) # pour  pas brusquer
coord=()

def listenGPS():
    while True:
        global  coord
        coord = l76.coordinates() #récupération des coordoné GPS#random.randrange(1000)#

_thread.start_new_thread(listenGPS,())
