# htr-ndp-cursive-evolution-2026

Reconnaissance automatique de texte manuscrit (HTR) appliquée au corpus e-NDP (Notre-Dame de Paris, 1326–1504).

**Module** : Vision par ordinateur — Master Data/IA, HETIC 2026  
**Groupe A** : Valentine Bounmy, Aby Samassa, Fares Hafiane

---

## Notebooks

| Étape   | Description        | Lancer sur Colab                                                                                                                                                                                  |
| ------- | ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Étape 3 | Fine-tuning Kraken | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ABYYsamas/htr_endp_2026/blob/main/notebooks/etape3_kraken_finetuning.ipynb) |
| Étape 4 | Évaluation finale  | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ABYYsamas/htr_endp_2026/blob/main/notebooks/etape4_evaluation_finale.ipynb) |

---

## Question scientifique

Un modèle HTR entraîné sur la cursive notariale du XIVe siècle généralise-t-il à la cursive du XVe–XVIe siècle, malgré l'évolution paléographique de l'écriture sur deux siècles ?

---

## Résultats

| Condition                   | Split           | CER         | WER         |
| --------------------------- | --------------- | ----------- | ----------- |
| Baseline (zéro fine-tuning) | val             | 40,60 %     | 88,24 %     |
| Fine-tuning cremma-medieval | val             | 17,26 %     | —           |
| Fine-tuning cremma-medieval | **test scellé** | **16,71 %** | **54,68 %** |
| Seuil de validation (brief) | —               | < 15 %      | < 25 %      |

SHA-256 test set : `f31c7dd2fa21505bf16984c631bb52ec2718f062593845268154fb3238682d59`

---

## Structure du dépôt

```
.
├── src/
│   ├── preprocessing/
│   │   └── pipeline.py               # Prétraitement images (CLAHE, Sauvola, deskew)
│   ├── segmentation/
│   │   ├── kraken_wrapper.py         # Segmentation BLLA
│   │   ├── sam_wrapper.py            # SAM ViT-B (testé, échec documenté)
│   │   └── evaluator.py             # Calcul IoU
│   └── corpus/
│       ├── splitting.py             # Découpage diachronique train/val/test
│       ├── parser.py                # Parsing PAGE XML
│       └── page_xml_export.py       # Export PAGE XML
├── scripts/
│   ├── build_split.py               # Génération du split + SHA-256
│   ├── export_page_xml.py           # Export des splits en PAGE XML
│   ├── evaluate_kraken_lines.py     # Évaluation segmentation Kraken
│   └── evaluate_sam_baseline.py     # Évaluation baseline SAM
├── tests/                           # Suite pytest (37 tests)
├── experiments/
│   └── journal.jsonl                # Journal de toutes les expériences
├── dataset_nlp/
│   └── dataset_nlp.json             # JSON livrable au Volet 2 NLP
├── notebooks/
│   ├── etape3_kraken_finetuning.ipynb
│   └── etape4_evaluation_finale.ipynb
├── docs/
│   ├── segmentation_baseline_sam.md
│   ├── segmentation_lines_kraken.md
│   └── export_page_xml.md
├── paper/
│   └── article_htr_endp.docx
├── CONVENTIONS_TRANSCRIPTION.md
├── DATA_SOURCES.md
├── MODEL_CARD.md
├── requirements.txt
└── README.md
```

---

## Installation

```bash
git clone https://github.com/ABYYsamas/htr_endp_2026.git
cd htr_endp_2026
pip install -r requirements.txt
```

**Environnement recommandé** : Python 3.12, GPU CUDA 12.x (Google Colab T4 ou équivalent).

---

## Reproduire les résultats

### 1. Données

Télécharger le corpus e-NDP depuis Zenodo :

```
https://zenodo.org/records/7575693
```

Placer les fichiers dans la structure suivante :

```
data/
└── HTR_Ground-Truth/
    ├── images/      # fichiers JPG/JPEG
    └── page_xml/    # fichiers PAGE XML
```

Le fichier `doc_headers.txt` s'extrait du zip Zenodo (dossier `No_Sketch_Engine/endp/vertical/source`).

### 2. Générer le split diachronique

```bash
python scripts/build_split.py \
    --corpus-root data/HTR_Ground-Truth/page_xml \
    --headers data/doc_headers.txt \
    --output-dir data/processed/endp
```

### 3. Exporter les PAGE XML par split

```bash
python scripts/export_page_xml.py \
    --splits-dir data/processed/endp \
    --output-dir data/processed/page_xml_export
```

### 4. Fine-tuning Kraken (Google Colab)

Cliquer sur le badge Colab étape 3 ci-dessus, activer GPU T4, lancer les cellules dans l'ordre. Le notebook télécharge automatiquement cremma-medieval depuis Zenodo (https://zenodo.org/records/7234166).

### 5. Évaluation finale (Google Colab)

Cliquer sur le badge Colab étape 4. Le split test est scellé — évaluation réalisée une seule fois.

### 6. Lancer les tests

```bash
pytest tests/
```

---

## Organisation de l'équipe

| Membre           | Rôle                        | Tâches principales                                                                 |
| ---------------- | --------------------------- | ---------------------------------------------------------------------------------- |
| Valentine Bounmy | Responsable technique       | Segmentation SAM et BLLA, évaluation IoU, pipeline étape 2                         |
| Aby Samassa      | Responsable expérimentation | Fine-tuning Kraken, notebooks Colab étapes 3 et 4, journal d'expériences           |
| Fares Hafiane    | Responsable documentation   | Article scientifique, DATA_SOURCES.md, CONVENTIONS_TRANSCRIPTION.md, MODEL_CARD.md |

---

## Corpus

**ANR e-NDP Ground Truth** — registres capitulaires de Notre-Dame de Paris (1326–1504).  
Licence : Creative Commons CC-BY 4.0  
DOI : [10.5281/zenodo.7575693](https://doi.org/10.5281/zenodo.7575693)  
Claustre, J., Smith, D., Torres Aguilar, S. et al. (2023).

---

## Licence

Code source : MIT  
Données : CC-BY 4.0 (hérité du corpus e-NDP)
