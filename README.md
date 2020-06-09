# LoRa
Projet Tutoré

## A uploader sur Fipy Emmeteur:
send.py et le boot.py qui le lance

## A uploader sur Fipy recepteur:
boot.py -> lance GPS.py
GPS.py -> permet d'obtenir les coordoné et des statistique sur le message recu

## Sur le PC
Traitement LoRa -> permet de convertir en fichier gpx les resultats du type :

`((<latitude>, <longitude>), (rx_timestamp=0, rssi=-4, snr=0.0, sfrx=0, sftx=0, tx_trials=0, tx_power=20, tx_time_on_air=0, tx_counter=0, tx_frequency=0), b'<message>') `



