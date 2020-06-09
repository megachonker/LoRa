import machine
from network import LoRa
import socket
import machine
import time
from L76GNSS import L76GNSS
from pytrack import Pytrack

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, tx_power=20, preamble=20, sf=12 )
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
py = Pytrack()
l76 = L76GNSS(py, timeout=30)

while (True):
    s.setblocking(False)
    data = s.recv(64)
    time.sleep(1)
    coord = l76.coordinates()
    txt=coord,lora.stats(),data
    print(txt)
