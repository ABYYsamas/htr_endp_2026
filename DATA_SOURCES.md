# DATA\_SOURCES.md

Ce document recense le jeu de données utilisé pour entraîner et évaluer le pipeline HTR du projet. 

## Choix du corpus

**Notre question scientifique est la suivante : un modèle HTR entraîné sur la cursive notariale du XIVe siècle généralise-t-il à la cursive du XVe-XVIe siècle, malgré l'évolution paléographique de l'écriture sur deux siècles ?**

Pour y répondre, nous avons choisi de travailler sur un seul corpus mono-source dont la profondeur temporelle (1326-1504) permet précisément d'étudier cette évolution. Ce choix de profondeur sur largeur est cohérent avec les recommandations actuelles en humanités numériques (Torres Aguilar, TRIDIS, 2025), qui valorisent la cohérence et la qualité des annotations sur le volume brut.

## Corpus retenu : ANR e-NDP Ground Truth

Le corpus e-NDP est une vérité terrain HTR issue du projet ANR e-NDP (Notre-Dame de Paris et son cloître), édition numérique collaborative des registres capitulaires de la cathédrale Notre-Dame de Paris. Il est porté par le LaMOP (Université Paris 1 Panthéon-Sorbonne) sous la direction de Julie Claustre et Darwin Smith, en partenariat avec les Archives nationales, la Bibliothèque nationale de France, l'École nationale des chartes et la Bibliothèque Mazarine.

Il rassemble 512 pages représentatives des 26 registres médiévaux du chapitre, conservés aux Archives nationales sous les cotes AN LL 105-128. Les transcriptions ont été réalisées entre 2021 et 2022 par 12 paléographes et historiens, en deux tours de relecture, via l'interface eScriptorium.

Les principales caractéristiques du corpus sont les suivantes. La période couverte est 1326-1504, soit du XIVe au XVIe siècle. La langue principale est le latin médiéval (au moins 98 %), le français représentant au plus 2 %. La famille d'écriture est la cursive médiévale tardive. Les documents sont des registres administratifs (délibérations capitulaires). Le volume total est de 34 231 lignes pour 3 320 407 caractères sur 512 pages, avec 18 mains principales identifiées. La convention de transcription est semi-diplomatique avec abréviations résolues. Le format de livraison est PAGE XML accompagné de fichiers JPG/JPEG. Le corpus est disponible sur Zenodo sous le DOI 10.5281/zenodo.7575693, pour une taille d'archive de 913,8 Mo. Le code des modèles HTR associés est accessible sur [https://github.com/chartes/e-NDP\_HTR](https://github.com/chartes/e-NDP_HTR).

## Justification du choix du latin médiéval

Le brief impose un périmètre XIe-XVIIe siècle, vieux/moyen français. L'inclusion d'e-NDP, dont le contenu est majoritairement latin, se justifie par le recentrage paléographique de notre projet. Notre axe de recherche porte sur l'évolution de l'écriture cursive en tant que forme graphique, et non sur la langue sous-jacente. Le latin médiéval écrit en France et l'ancien français partagent la même tradition graphique (cursives, ligatures, systèmes d'abréviation), et un modèle HTR opère sur les formes visuelles des glyphes indépendamment du contenu lexical. Cette approche est cohérente avec les pratiques actuelles en HTR médiévale (Torres Aguilar, 2025 ; Pinche et al., 2023).

## Conformité licencielle

Le corpus e-NDP est diffusé sous licence Creative Commons Attribution 4.0 International (CC-BY 4.0). Cette licence autorise la redistribution, la modification et l'usage commercial des données, sous réserve de mentionner correctement les auteurs originaux. Le présent projet respecte cette obligation par la citation ci-dessous et par le fichier MODEL\_CARD.md du dépôt. Aucune source protégée par le droit d'auteur ou diffusée sous licence restrictive n'a été utilisée.

## Attribution

Toute publication issue du présent projet doit mentionner explicitement l'équipe e-NDP (Julie Claustre, Darwin Smith et l'ensemble des contributeurs du LaMOP, Université Paris 1 Panthéon-Sorbonne), financée par l'ANR sous le projet ANR-20-CE27-0012, ainsi que l'écosystème HTR-United (Chagué, Clérice, Chiffoleau, 2021\) comme infrastructure ayant permis la mise à disposition de la ressource.

## Citation académique

Claustre, J., Smith, D., Torres Aguilar, S., Bretthauer, I., Brochard, P., Canteaut, O., Cottereau, E., Delivré, F., Denglos, M., Jolivet, V., Julerot, V., Kouamé, T., Lusset, E., Massoni, A., Nadiras, S., Perreaux, N., Regazzi, H., & Treglia, M. (2023). The e-NDP project: collaborative digital edition of the Chapter registers of Notre-Dame of Paris (1326-1504). Ground-truth for handwriting text recognition (HTR) on late medieval manuscripts (Version 1.0) \[Dataset\]. Zenodo. [https://doi.org/10.5281/zenodo.7575693](https://doi.org/10.5281/zenodo.7575693)  
