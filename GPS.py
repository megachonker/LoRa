import machine
import pycom
import socket
import time
from network import LoRa
from L76GNSS import L76GNSS
from pytrack import Pytrack

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, tx_power=20, preamble=20, sf=12 )
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
py = Pytrack()
l76 = L76GNSS(py, timeout=30)

pycom.heartbeat(False)
pycom.rgbled(0x7f0000) # red
i==0
with open('data.txt', 'a') as datafile:
    txt="\n\n\n"
    datafile.write(txt)
datafile.close()

while (True):
    s.setblocking(False)
    data = s.recv(64)
    time.sleep(2)
    coord = l76.coordinates()
    if coord == (None,None) and data == b'':
        pycom.rgbled(0x7f0000) # rouge => - Coordoné ; - data 

    if coord != (None,None) and data == b'':
        pycom.rgbled(0x0000ff)# bleu   => + Coordoné ; - data 

    if coord == (None,None) and data != b'':
        pycom.rgbled(0xffff00)# jaune  => - Coordoné ; + data 

    if coord != (None,None) and data != b'':
        pycom.rgbled(0x007f00)# vert   => + Coordoné ; + data 

    txt=coord,lora.stats(),data
    with open('data.txt', 'a') as datafile:
        tx=str(txt)+"\n"
        datafile.write(tx)
    datafile.close()
    print(txt)
