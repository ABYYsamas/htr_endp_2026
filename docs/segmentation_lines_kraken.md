# Étape 2.3 — Segmentation des lignes de texte avec Kraken BLLA

Après l'échec de SAM (étape 2.2), on a testé Kraken BLLA pour segmenter les lignes de texte des pages e-NDP.

## Ce qu'on a fait

On a utilisé le module `kraken.blla.segment` sur deux pages du corpus, une de 1346 (XIVe) et une de 1501 (XVIe). Pour chaque page, on a comparé les lignes détectées par Kraken avec les lignes annotées manuellement dans les PAGE XML, en utilisant la même métrique IoU que pour SAM.

## Résultats

Les résultats sont bons : IoU moyen de 0,745 sur la page de 1346 et de 0,756 sur celle de 1501\. Kraken retrouve également le bon nombre de lignes — exactement 54 sur 54 pour la page XIVe, et 81 pour 73 annotées sur la page XVIe (légère sur-segmentation sur l'écriture plus serrée du XVIe siècle).

Par comparaison, SAM donnait un IoU de 0,05-0,09 sur les mêmes pages. L'amélioration est d'un facteur 8 à 15\.

## Pourquoi ça marche

Kraken BLLA est entraîné spécifiquement sur des pages de manuscrits historiques, contrairement à SAM qui est conçu pour des photos naturelles. Il sait qu'une page contient des lignes de texte horizontales et produit deux représentations complémentaires : la baseline (ligne d'écriture) et le boundary (polygone englobant la ligne).

On a eu quelques warnings de topologie sur certaines lignes dans les marges très denses, mais le pipeline ne plante pas — Kraken construit une boîte de secours et continue.

## Décision

On adopte Kraken BLLA pour la segmentation de lignes en production. Les polygones générés sont exportés en PAGE XML à l'étape 2.5 et servent d'entrée au fine-tuning de l'étape 3\.

## Référence

Kiessling, B. (2019). Kraken: A modular OCR system. Digital Humanities 2019\. [https://kraken.re](https://kraken.re)  
