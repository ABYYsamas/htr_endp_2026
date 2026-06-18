# Étape 2.5 — Export des polygones en PAGE XML

## Ce qu'on a fait

Après avoir généré le split train/val/test à l'étape 2.4, on a exporté les géométries de lignes (polygones et baselines) en fichiers PAGE XML, un par page. C'est le format standard attendu par Kraken pour l'entraînement HTR à l'étape 3\.

## Structure des fichiers produits

data/processed/page\_xml\_export/

├── train/    fichiers \*.xml

├── val/      fichiers \*.xml

└── test/     fichiers \*.xml  ← scellé, ne pas ouvrir

Les polygones exportés viennent du ground truth e-NDP (annotations manuelles des paléographes), qui sont plus précis que ceux générés automatiquement par Kraken BLLA. Chaque fichier XML contient pour chaque ligne son polygone, sa baseline, son identifiant et son texte transcrit.

## Comment reproduire

python scripts/export\_page\_xml.py \\

    \--splits-dir data/processed/endp \\

    \--output-dir data/processed/page\_xml\_export

## Implémentation

- `src/corpus/page_xml_export.py` — module qui génère le PAGE XML  
- `scripts/export_page_xml.py` — script en ligne de commande  
- `tests/test_page_xml_export.py` — tests unitaires

## Référence

PRImA Research Lab. PAGE XML Format 2019-07-15. [http://www.primaresearch.org/tools/PAGELibraries](http://www.primaresearch.org/tools/PAGELibraries)  
