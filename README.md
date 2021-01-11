# LoRa
Projet Tutoré

Rédaction un alghoritme robuste permétant d'évaluer la vitesse d'un  lien dans un  cas pratique

## objectif

voire  l'impacte de la  distance est des  différante modulation  sure ce débit  calculer

## état des lieux:
- Envoit de binaire hover Lora ✔
- Fiabilitée ✔
  - Detection des trame perdu ✔
  - Retransmition trame perdu ✔
  - Crash ✘ (Très Rare)
- Intégritée de la playload Recepteur ✔
  - Controlle d'intégritée ✔
  - Correction erreur ✘ (recherche si packet corrompu ou bug algo)
- Portage sur librairie ✘ (pour les benchmark)
  - Lancement transfère avec  paramètre ✔
  - Syncronisation des paramètre ✔ (théorique)
  - Output JSON ✘

## Objectif future
### Benchmark et Mesure
- Algorhitme de transfert! POSSIBLE
- estimation d'un débit minimal pour qu'une communication soit valide!

#### estimation du débit max en jouant sur les différant facteur:
- bruit/SNR ==> adaml pluto (brouillage)
- Distance/aténuation
- SF/facteur d'étalement
- CR/RaportCorectionErreur
- playload lenght

## plot
- plot des data dans un espace tridimentionel avec gnuplot
- faire des script pour expposer les différant résultat glannée
