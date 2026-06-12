# MODEL\_CARD.md

**Modèle** : endp-kraken-finetuned  
**Version** : 1.0  
**Projet** : htr-ndp-cursive-evolution-2026  
**Groupe**  : Valentine Bounmy, Aby Samassa, Fares Hafiane 

## Description

Modèle de reconnaissance automatique de texte manuscrit (HTR) fine-tuné depuis cremma-medieval sur le corpus e-NDP (Notre-Dame de Paris, 1326–1504). Il est conçu pour transcrire la cursive notariale médiévale latine des registres capitulaires du chapitre de Notre-Dame de Paris.

## Performances

Évaluation réalisée sur le test set scellé (folios 17–20, approximativement XVe–XVIe siècle). Cette évaluation a été réalisée une seule fois, conformément au protocole du brief.

| Métrique | Baseline (zéro fine-tuning) | Modèle fine-tuné |
| :---- | :---- | :---- |
| CER (test scellé) | 40,60 % | **16,71 %** |
| WER (test scellé) | 88,24 % | 54,68 % |
| Accuracy caractères | 59,40 % | 83,29 % |
| Accuracy mots | 11,76 % | 45,32 % |

Seuil de validation du brief : CER \< 15 % — Seuil d'excellence : CER \< 8 %

## Données d'entraînement

- **Corpus** : ANR e-NDP Ground Truth (Claustre et al., 2023\)  
- **Licence** : Creative Commons CC-BY 4.0  
- **DOI** : 10.5281/zenodo.7575693  
- **Volume utilisé** : 24 fichiers PAGE XML (folios 1–12, XIVe siècle)  
- **Langue** : Latin médiéval (≥ 98 %), français (≤ 2 %)  
- **Convention** : Semi-diplomatique, abréviations résolues  
- **SHA-256 train** : voir `experiments/journal.jsonl`  
- **SHA-256 test** : `f31c7dd2fa21505bf16984c631bb52ec2718f062593845268154fb3238682d59`

## Modèle de base

- **Nom** : cremma-medieval\_best.mlmodel  
- **Source** : Zenodo 10.5281/zenodo.7234166  
- **Auteurs** : Pinche et al. (2022)  
- **Licence** : CC-BY 4.0

---

## Hyperparamètres d'entraînement

| Paramètre | Valeur |
| :---- | :---- |
| Framework | Kraken 7.0.2 |
| Architecture | LSTM bidirectionnel \+ CTC |
| Epochs | 21 (early stopping, patience 10\) |
| Batch size | 4 |
| Learning rate | 1e-4 |
| Normalisation | NFD |
| Resize codec | union |
| GPU | Tesla T4 (Google Colab) |
| Seed | 42 |

---

## Utilisation

### Installation

pip install kraken==7.0.2

### Transcription d'une image

from PIL import Image

from kraken import blla, rpred

from kraken.lib import models

model \= models.load\_any("best\_model.mlmodel")

with Image.open("page.jpg") as img:

    img.load()

    seg \= blla.segment(img)

    lines \= list(rpred.rpred(model, img, seg, bidi\_reordering=True))

for line in lines:

    print(line.prediction)

### Format d'entrée

- Images JPG ou TIFF de pages de manuscrits médiévaux  
- Résolution recommandée : 300 dpi minimum  
- Le modèle est optimisé pour la cursive notariale latine du XIVe–XVIe siècle

### Format de sortie

Transcription en texte Unicode, convention semi-diplomatique (abréviations résolues, distinction u/v et i/j appliquée).

---

## Limitations

**Corpus d'entraînement réduit** : le modèle a été entraîné sur seulement 24 documents (folios 1–12 du corpus e-NDP), soit une fraction du corpus complet (512 pages, 34 231 lignes). Cela explique le CER de 16,71 %, supérieur au seuil de validation de 15 %.

**Biais diachronique** : les données d'entraînement couvrent principalement le XIVe siècle. La généralisation aux cursives du XVe–XVIe siècle est partielle, comme en témoigne l'analyse des erreurs (confusions i/u, n/m fréquentes).

**Langue** : le modèle est optimisé pour le latin médiéval. Ses performances sur d'autres langues (ancien français, occitan) ne sont pas garanties.

**Abréviations résiduelles** : quelques caractères MUFI (ꝓ, ⁊) subsistent dans les transcriptions malgré la convention semi-diplomatique du corpus, issus d'inconsistances d'annotation.

## Biais de représentation

Le corpus e-NDP couvre exclusivement les registres capitulaires de Notre-Dame de Paris. Les types documentaires (actes notariaux, chartes, livres de comptes), les régions dialectales autres que l'Île-de-France, et les écritures gothiques non cursives sont absents. Le modèle ne doit pas être utilisé sur ces types de documents sans évaluation préalable.

## Citation

@misc{bounmy\_samassa\_hafiane\_2026,

  author \= {Bounmy, Valentine and Samassa, Aby and Hafiane, Fares},

  title  \= {endp-kraken-finetuned: HTR model for medieval cursive (e-NDP corpus)},

  year   \= {2026},

  note   \= {Projet MD5, Master Data/IA, HETIC. 

            Fine-tuned from cremma-medieval on ANR e-NDP Ground Truth.}

}

## Références

Claustre, J., Smith, D., Torres Aguilar, S. et al. (2023). The e-NDP project. Zenodo. [https://doi.org/10.5281/zenodo.7575693](https://doi.org/10.5281/zenodo.7575693)

Pinche, A. et al. (2022). CREMMA Medieval. Zenodo. [https://doi.org/10.5281/zenodo.7234166](https://doi.org/10.5281/zenodo.7234166)

Kiessling, B. et al. (2019). BADAM: A public dataset for baseline detection in Arabic-script manuscripts. HIP@ICDAR 2019\.  
