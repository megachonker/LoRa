# LoRa
Projet Tutoré

Rédaction un alghoritme robuste permétant d'évaluer la vitesse d'un  lien dans un  cas pratique

## objectif

voire  l'impacte de la  distance est des  différante modulation  sure ce débit  calculer

## état des lieux:
- Envoit de binaire hover Lora ✔
- Detection des trame perdu ✔ (avec le minimum de bande passante)
- Retransmition trame perdu ✔
- Intégritée de la playload Recepteur ✘
- Portage sur librairie ✘ (pour les benchmark) 
- Couche Verification/Correction Erreur ? (intégrée dans la pile lora)

## Objectif future
### Benchmark et Mesure
- Besoin de l'algorhitme de transfert! (not yet avaible)
- estimation d'un débit minimal pour qu'une communication soit valide!

#### estimation du débit max en jouant sur les différant facteur:
- bruit/SNR ==> adaml pluto (brouillage)
- Distance/aténuation
- SF/facteur d'étalement
- CR/RaportCorectionErreur
- playload lenght

## plot
plot des data dans un espace tridimentionel avec gnuplot
faire des script pour expposer les différant résultat glannée
