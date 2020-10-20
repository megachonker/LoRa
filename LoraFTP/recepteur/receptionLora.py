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

#on set la taille  du buffer ces a dire le  nombre  d'octée qu'on attend  pour fermer  le socket
buffersize=64

#on initialise lora Avec des parametre qu'on va vouloire jouer
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868, bandwidth=LoRa.BW_250KHZ, preamble=5, sf=8)
#on initialise le  soket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)


#fonction  permetant de vider  le buffer  qui peut poser  des soucis RArement mais  ça peut vite  être contrégniant dans le cas échéant
def purge():
	#purger les  sockete
	s.setblocking(False)
	purgetemp=s.recv(buffersize)
	while purgetemp!=b'':
		purgetemp=s.recv(buffersize)
	s.setblocking(True)

#on  initialise  les tableaux pour  que les définition  puisse correctement les  utilisé
indexRecieve=[]
indexManque=[]
compteurerr=0
#declaration
nbtrame=0
def unboxing(rawtram):
	#on  autorise  la définition a avoire accèse au  meme variable que le main
	global indexRecieve
	global indexManque
	global compteurerr
	#chercher si la trame a unboxer est malformer
		#faire fonction qui check  la trame
	unpackted=unpack("H"+str(buffersize-2)+"s", rawtram)#on stoque la data qui est dans un  tuple dans une variable
	if(unpackted[0]<nbtrame):
		#print("trame depacked", unpackted)
		print("del val",unpackted[0],"/",str(nbtrame))#,"erreur estimer",str(len(indexRecieve)-compteurerr))
		#on
		indexRecieve.append(unpackted) #on archive le packet recus
		#print("indexremovebefort ",str(indexManque))
		indexManque.remove(unpackted[0])
		#print("indexremove after ",str(indexManque))

	else:
		print("malformer", unpackted)


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


print("Attente Trame Datalenght")
#purge le buffer au  cas ou
purge()
#pour définire nbtrame  on va  accepter que les  trame  étant sur 1 octée en Long
while True:
	try:
		nbtrame=unpack('H3s',s.recv(buffersize))
		if nbtrame[1]==b'OwO':
			nbtrame=nbtrame[0]
			break
	except Exception as e:
		print("Trame Non  attendue")

print("nombre de trame", str(nbtrame))
#génération d'un  tableaux qui contien toute les trame
for number in range(int(nbtrame)):
	indexManque.append(number)


print("envoit d'un  ackitement")
#Unboxing de la premierre trame de donnée qui fait office d'ackitment
purge()
unboxing(sendACK(str(nbtrame)))


print("démarage reception")

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
print("trie:")
#on va trier  en fonction  du  1er élémenet du tuple du tableaux
indexRecieve.sort(key=itemgetter(0))
print(indexRecieve)
print("écriture en cour:")

#on essay suprime le fichier si il existe
#flmee de  chercherune fonction  de  test  si  le fichier existe avant  de le suprimer
try:
	#on  essaye  de le supprimer
	os.remove("imgOut.txt")
	print("fichier supprimer")
except OSError as e:
	print("fichier inéxistant")

#on  va  ouvrire  le fichiuer
with open('imgOut.txt', 'w') as fout: #création de du fichier data.txt sur le module si il n'est pas present, ou sinon on l'ouvre en mode ajout de data.
	#on va  parser notre  tableaux de  tuple
	for truc in indexRecieve:
		#on  va selecioner  la  2eme valeur de  notre tuple  (les data)
		fout.write(truc[1])
fout.close() # on referme le fichier

print("transfer  terminer")
s.send("STOP")
s.send("STOP")
s.send("STOP")
s.send("STOP")
