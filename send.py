from network import LoRa
import socket
import time

print('start')

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, preamble=20, sf=12)
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
s.setblocking(True)
i=0

while True:
    msg=str(i)+"abcdefghijklmnopqrstuvwxyz0123456789"
    s.send(msg)
    print(msg)
    i+=1
    time.sleep(1)
