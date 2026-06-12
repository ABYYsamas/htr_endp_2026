# CONVENTIONS\_TRANSCRIPTION.md

**Projet** : htr-ndp-cursive-evolution-2026

## Niveau de transcription

Le corpus e-NDP adopte une convention semi-diplomatique. Elle maintient la graphie originale du manuscrit tout en appliquant un ensemble ciblé de régularisations : résolution des abréviations, distinction u/v et i/j, capitalisation des entités nommées.

## Abréviations

Toutes les abréviations sont résolues par les annotateurs. Les suspensions, contractions et signes conventionnels sont développés dans leur forme complète. Par exemple, dñi devient domini, ⁊ devient et, et ꝓ devient pro.

## Distinction u/v et i/j

Le corpus distingue u (voyelle) de v (consonne), et i (voyelle) de j (consonne). Ainsi unus s'écrit avec u, vir avec v, ipse avec i, et Johannes avec j.

## Casse

Les capitales originales du notaire sont préservées. Les entités nommées (personnes, lieux, institutions) sont systématiquement capitalisées par les annotateurs.

## Ponctuation

La ponctuation manuscrite est conservée telle quelle. Aucun signe de ponctuation moderne n'est ajouté.

## Corrections et biffures

Les passages biffés ou corrigés par le notaire sont encadrés par le marqueur $. Dans notre pipeline, les lignes contenant ce marqueur sont automatiquement signalées comme `needs_review = true` dans le JSON de sortie.

## Espaces

Les espaces ne sont pas homogènes dans le corpus. Certaines transcriptions reproduisent l'espacement du manuscrit, d'autres utilisent des espaces lexicaux. Nous n'avons pas cherché à normaliser ce point, ce qui explique en partie le WER élevé observé sur nos résultats.

## Référence

Claustre, J., Smith, D., Torres Aguilar, S. et al. (2023). The e-NDP project. Zenodo. [https://doi.org/10.5281/zenodo.7575693](https://doi.org/10.5281/zenodo.7575693)  
