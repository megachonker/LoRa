from network import LoRa #pour etre en mode LoRa
import socket # pour lire les message recus
import time # pour la gestion des temps d'attente
import os #gestion de  fichier
import struct  #gestion des  structure  de  trame  sert  notament a  aranger des donnnée dans une suite de type  binaire
from struct import * ##verifier si ces utile
#on  importe un  librarie  qui  va permetre  de  trier  des tableaux de  turple
#librérie  ou j'ai  du  retirer des  fonction  de  python  3.7 pour l'adapter sur lopy 2.7
#de ce fait  je pourait la simplifier  au stricte minimum donc a voir  .....
from operator import itemgetter#, attrgetter
import hashlib

#on set la taille  du buffer ces a dire le  nombre  d'octée qu'on attend  pour fermer  le socket
buffersize=64
#on initialise lora Avec des parametre qu'on va vouloire jouer
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_500KHZ, preamble=5, sf=7)
#on initialise le  soket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

##ne pouvant avoir une résolution en  dessou de  la  seconde  sans passer  par des  tick ces mort
# ltime=int()
# def crono():
# 	global ltime
# 	b=time.time()
# 	out=b-ltime
# 	ltime=b
# 	return out

#fonction  permetant de vider  le buffer  qui peut poser  des soucis RArement mais  ça peut vite  être contrégniant dans le cas échéant
def purge():
	#purger les  sockete
	s.setblocking(False)
	purgetemp=s.recv(buffersize)
	while purgetemp!=b'':
		purgetemp=s.recv(buffersize)
	s.setblocking(True)


#declaration
startAt=0
nbtrame=0
indexManque=[]
indexRecieve=[]
stVarIndex=""
tVarIndex=""
playloadsize=0 #autodetect


def unboxing(rawtram):
	#on  autorise  la définition a avoire accèse au  meme variable que le main
	global indexRecieve
	global indexManque
	global startAt

	#on verifie si on peut umpack la trame
	try:			#"H"+str(buffersize-2)
		unpackted=unpack(stVarIndex+"s", rawtram)#on stoque la data qui est dans un  tuple dans une variable

		#pour le premier tour  on empege une division par zero
		totaltemp=time.time()-startAt
		if totaltemp == 0:
			totaltemp=1
		totaldata=(len(indexRecieve)+1)*int(playloadsize)

		print("del val",unpackted[0],"débit moyen: ",str(totaldata/totaltemp),"octée/s")

		#on vérifie si ces bien une trame  de data
		try:
			indexManque.remove(unpackted[0])
			indexRecieve.append(unpackted) #on archive le packet recus
		except ValueError:
			#debug value
			print("List des  packet a receptioner ",str(indexManque))
			print("liste des packet déja  receptioner", str(indexRecieve))
			print("valeur a  supprimer(1er):",unpackted)
			print("packet unpackted", str(unpackted))
			print("raw packet", str(rawtram))

		#lora.stats()

	except OSError as e:
		print("size  du  packet", str(len(unpackted)),"contenus: ", str(rawtram))


#définition d'une fonction d'aquitement
def sendACK(vara):
	s.settimeout(2)
	i=0
	while True:
		i+=1
		s.send(vara)
		print("attente ack...")
		try:
			retour=s.recv(buffersize)
			#print(retour)
			print("ack Reçus")
			break
		except OSError as socket :
			print("timeout try n° ",i)
	s.setblocking(True)
	return retour


def sendACKvrf(data, match):
	while True:
		if sendACK(data) == match.encode() :
			break
		else:
			print("Réponse inatentue/Malformed", str(sendACK(data)))
	return True

def writeTo(name):
	global indexRecieve
	#on essay suprime le fichier si il existe
	#flmee de  chercherune fonction  de  test  si  le fichier existe avant  de le suprimer
	name=str(name)
	try:
		#on  essaye  de le supprimer
		os.remove(name)
		print("fichier supprimer")
	except OSError as e:
		print("fichier inéxistant")

	#on  va  ouvrire  le fichiuer
	with open(name, 'w') as fout: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
		#on va  parser notre  tableaux de  tuple
		for truc in indexRecieve:
			#on  va selecioner  la  2eme valeur de  notre tuple  (les data)
			fout.write(truc[1])
			# on referme le fichier proprement
	fout.close()


print("Attente Trame Datalenght")
#purge le buffer au  cas ou
purge()
#pour définire nbtrame  on va  accepter que les  trame  étant sur 1 octée en Long
while True:
	try:
		nbtrame=unpack('L3s32s',s.recv(buffersize))
		if nbtrame[1]==b'OwO':
			checksum=nbtrame[2]
			nbtrame=nbtrame[0]
			break
	except Exception as e:
		print("nombretrame err : Trame Non  attendue",str(nbtrame))

print("nombre de trame", str(nbtrame))


#on déduit le type de  variable a  utiliser en fonction du  nombre de trame total
if nbtrame<256:
	tVarIndex="B"
	stVarIndex="B"+str(buffersize-1)
	playloadsize=str(buffersize-1)
elif (nbtrame<65536):
	tVarIndex="H"
	stVarIndex="H"+str(buffersize-2)
	playloadsize=str(buffersize-1)
else:
	tVarIndex="L"
	stVarIndex="L"+str(buffersize-4)
	playloadsize=str(buffersize-1)


#génération d'un  tableaux qui contien toute les trame
for number in range(int(nbtrame)):
	indexManque.append(number)


print("envoit d'un  ackitement")
#Unboxing de la premierre trame de donnée qui fait office d'ackitment
purge()
startAt=time.time()
unboxing(sendACK(str(nbtrame)))


print("démarage reception")
startAt=time.time()
#je  demande explicitement d'écouter j'usqua se que je  recois une trame
s.setblocking(True)
#tant qu'il  y a des trame  manquante
while True:
	#tant que l'éméteur veux envoiller des donnée
	while True:
		#je  reçois ma trame
		trame=s.recv(buffersize)
		#quand l'éméteur  a fini ENvoit de  stop pour  passer a la partie suivante
		if trame==b'STOP':
			print("fin de flux reçus  !")
			s.send("Ok")
			break
		#sinon on traite la trame normalement
		else:
			#on va traiter la  trame  recus
			unboxing(trame)
##j'aurait pus  inverser les if avec un != ?

	#si il  n'y a plus de trame manquante
	if(len(indexManque)==0):
		print("plus de trame manquante.")
		#sendACK("STOP")
		#on va indiquer a l'éméteur que ces fini
		s.send("STOP")
		#on sort de toute mes boucle  affain  de  passer a  au  trie  des data
		break

	print("trame perdu/restant:")
	print(indexManque)


	#Envoit des trame a  retransmetre
	#+ ajout de la premierre trame reçus (data)

	#on copy explicitement le  précédant tableaux dans un  nouveaux
	indexManquetosend=indexManque.copy()
	#tant qu'il reste des trame dans la liste TEMPORAIRE des trame qui  manque
	while len(indexManquetosend):
		#vieux conmpeur
		i=0
		#on initialise ma future  trame en déclarant que ça serat du  binaire
		temp=b''

		#je  crée  une  trame  qui  sera  égale  a la taille  du buffer ou inferieure  tant qu'il  me   reste des valeur  a y metre
		##	  i<(buffersize/2) #mieux ?
		while i<32 and len(indexManquetosend):
			#je rajoute de nouveaux Idex de trame  manquante  a ma trame  éxistante
			temp+=pack('H',indexManquetosend[0])
			#je  suprime  la valeur  ajouter
			indexManquetosend.pop(0)
			i+=1
		#je  m'assurt  que l'éméteur a  bien recus la  trame  qu'il  a recus  est qu'il n'es pas  perdu  [utile quand je chercherer a débusquer les trame  malformer]

		sendACKvrf(temp,"indexOKforNext")#######a la place de indexOk peut metre un ckecksum
		print("trame contenant les nb de trame bien récéptioner par le destinataire")
	#on envoit a  l'éméteur un  signial  indiquant qu'il n'y a plus  de  trame a  envoiller est on verifi qu'il  est bien sincro
	sendACKvrf("STOP","indexFIN")
	print("liste  trame manquante bien  réceptioner") ##  ligne 160  et  163 redondante ?
	print(indexManque)
	#on envoit une  trame  pour  trigguer l'éméteur pour qu'il  passe  en  mode émition  et on traite  la premierre valeur reçus
	###metre  un  time  out a  l'éméteur
	unboxing(sendACK("GO"))

	print("début de la rerectption")


print("récéption terminer:")
stopAt=time.time()

print("trie:")
#on va trier  en fonction  du  1er élémenet du tuple du tableaux
indexRecieve.sort(key=itemgetter(0))
#print(indexRecieve)

datafile=b''
for truc in indexRecieve:
	if (truc[1]==b''):
		break
	datafile+=truc[1]
print("durée du transfer:",str(stopAt-startAt),"débit moyen de", str(len(datafile)/(stopAt-startAt)),"octée/s")
m = hashlib.sha256()
m.update(datafile)

if checksum==m.digest():
	print("Fichier intègre !")
else:
	print("/!\ bad checksum ! /!\ ")


print("Phase écriture:")

writeTo("imgOut.txt")

# print("durée du transfer:",str(stopAt-startAt),"débit moyen de", str(os.stat("imgOut.txt")[5]/(stopAt-startAt)))

print("transfer  terminer")
purge()
s.setblocking(False)
s.send("STOP")
s.send("STOP")
s.send("STOP")
s.send("STOP")
