from machine import UART
import machine
import os

uart = UART(0, baudrate=115200)
os.dupterm(uart)

machineA=b'\x80}:\xc2\xec\xf0'
machineB=b'\x80}:\xc3F`'

if machineA == unique_id():
	machine.main('emeteur/send.py')

elif machineB == unique_id():
	machine.main('recepteur/receptionLora.py')