# htr-ndp-cursive-evolution-2026

Reconnaissance automatique de texte manuscrit (HTR) appliquée au corpus e-NDP (Notre-Dame de Paris, 1326–1504).


**Groupe**  : Valentine Bounmy, Aby Samassa, Fares Hafiane

## Question scientifique

Un modèle HTR entraîné sur la cursive notariale du XIVe siècle généralise-t-il à la cursive du XVe–XVIe siècle, malgré l'évolution paléographique de l'écriture sur deux siècles ?

## Résultats

| Condition | Split | CER | WER |
| :---- | :---- | :---- | :---- |
| Baseline (zéro fine-tuning) | val | 40,60 % | 88,24 % |
| Fine-tuning cremma-medieval | val | 17,26 % | — |
| Fine-tuning cremma-medieval | **test scellé** | **16,71 %** | **54,68 %** |
| Seuil de validation (brief) | — | \< 15 % | \< 25 % |

SHA-256 test set : `f31c7dd2fa21505bf16984c631bb52ec2718f062593845268154fb3238682d59`

---

## Structure du dépôt

.

├── src/

│   ├── preprocessing/

│   │   └── pipeline.py          \# Prétraitement images (CLAHE, Sauvola, deskew)

│   ├── segmentation/

│   │   ├── kraken\_wrapper.py    \# Segmentation BLLA

│   │   ├── sam\_wrapper.py       \# SAM ViT-B (testé, échec documenté)

│   │   └── evaluator.py         \# Calcul IoU

│   └── corpus/

│       ├── splitting.py         \# Découpage diachronique train/val/test

│       ├── parser.py            \# Parsing PAGE XML

│       └── page\_xml\_export.py   \# Export PAGE XML

├── scripts/

│   ├── build\_split.py           \# Génération du split \+ SHA-256

│   └── export\_page\_xml.py       \# Export des splits en PAGE XML

├── tests/                       \# Suite pytest

├── experiments/

│   └── journal.jsonl            \# Journal de toutes les expériences

├── dataset\_nlp/                 \# JSON livrable au Volet 2 NLP

├── notebooks/

│   ├── etape3\_kraken\_finetuning.ipynb   \# Fine-tuning Kraken (Google Colab)

│   └── etape4\_evaluation\_finale.ipynb  \# Évaluation test scellé (Google Colab)

├── CONVENTIONS\_TRANSCRIPTION.md

├── DATA\_SOURCES.md

├── MODEL\_CARD.md

├── requirements.txt

└── README.md

## Installation

git clone https://github.com/vbounmy/samassa-hafiane-bounmy-htr-manuscripts-md5

cd samassa-hafiane-bounmy-htr-manuscripts-md5

pip install \-r requirements.txt

**Environnement recommandé** : Python 3.12, GPU CUDA 12.x (Google Colab T4 ou équivalent).

## Reproduire les résultats

### 1\. Données

Télécharger le corpus e-NDP depuis Zenodo :

https://zenodo.org/records/7575693

Placer les fichiers dans la structure suivante :

data/

└── HTR\_Ground-Truth/

    ├── images/     \# fichiers JPG/JPEG

    └── page\_xml/   \# fichiers PAGE XML

### 2\. Générer le split diachronique

python scripts/build\_split.py \\

    \--corpus-root data/HTR\_Ground-Truth/page\_xml \\

    \--headers data/doc\_headers.txt \\

    \--output-dir data/processed/endp

Le fichier `data/processed/endp/stats.json` contiendra les SHA-256 des trois splits.

### 3\. Exporter les PAGE XML par split

python scripts/export\_page\_xml.py \\

    \--splits-dir data/processed/endp \\

    \--output-dir data/processed/page\_xml\_export

### 4\. Fine-tuning Kraken (Google Colab)

Ouvrir `notebooks/etape3_kraken_finetuning.ipynb` sur Google Colab avec GPU T4 activé et suivre les cellules dans l'ordre. Le modèle produit (`best_model.mlmodel`) sera sauvegardé sur Google Drive.

### 5\. Évaluation finale (Google Colab)

Ouvrir `notebooks/etape4_evaluation_finale.ipynb` sur Google Colab. Le split test est scellé — cette évaluation ne doit être réalisée qu'une seule fois.

### 6\. Lancer les tests

pytest tests/

---

## Organisation de l'équipe

| Membre | Rôle | Tâches principales |
| :---- | :---- | :---- |
| Valentine Bounmy | Responsable technique | Segmentation SAM et BLLA, évaluation IoU, pipeline étape 2 |
| Aby Samassa | Responsable expérimentation | Fine-tuning Kraken, notebooks Colab étapes 3 et 4, journal d'expériences |
| Fares Hafiane | Responsable documentation | Article scientifique, DATA\_SOURCES.md, CONVENTIONS\_TRANSCRIPTION.md, MODEL\_CARD.md |

---

## Corpus

**ANR e-NDP Ground Truth** — registres capitulaires de Notre-Dame de Paris (1326–1504).  
Licence : Creative Commons CC-BY 4.0  
DOI : [10.5281/zenodo.7575693](https://doi.org/10.5281/zenodo.7575693)  
Claustre, J., Smith, D., Torres Aguilar, S. et al. (2023).

## Licence

Code source : MIT  
Données : CC-BY 4.0 (hérité du corpus e-NDP)  
