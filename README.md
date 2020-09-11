# Alma_Bacon_Analyse_Et_Synch
Injecte des PPN dans des notices de la CZ liées à des bouquets Bacon.
  - Prend en paramètre l'identifiant d'une collection électronique
  - Pour chaque bouquet, interroge le service Bacon id2Kbart avec tous les ISBN(s) ou ISSN(s) de la notice (e ou print) pour récupérer le PPN s'il existe
S'il y a PPN il créé une ligne dans un TSV avec le MMSID de la notice et le PPN
  - Dépose le fichier sur un FTP déclaré dans Alma
  - Déclenche un job de chargement qui copie la notice dans l'IZ et ajoute un PPN en 035.

## Pré-requis Alma
### Avoir configuré un ftp.

### Avoir configuré un profil de chargement 
![](Import Profile Details.png)

![](Import Profile Details2.png)