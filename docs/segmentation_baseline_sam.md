# Étape 2.2 — Segmentation de structure de page : test avec SAM

Pour cette étape, on a testé le modèle SAM (Segment Anything, ViT-B) de Meta AI pour détecter automatiquement les zones logiques des pages e-NDP (blocs de texte, listes, dates, numérotation).

## Ce qu'on a fait

On a évalué SAM sur 4 pages du corpus, une par période : une page de 1346 (XIVe), une de 1401 (XVe début), une de 1450 (XVe fin), et une de 1501 (XVIe). Pour chaque page, on a comparé les masques générés par SAM avec les zones annotées dans les PAGE XML, en utilisant la métrique IoU (Intersection over Union).

La configuration utilisée est SAM ViT-B en mode `SamAutomaticMaskGenerator`, avec `points_per_side=16`, `pred_iou_thresh=0.86`, `stability_score_thresh=0.92` et un downscale de 4x pour réduire le temps de calcul. L'évaluateur IoU est implémenté dans `src/segmentation/evaluator.py`.

## Résultats

Les résultats sont mauvais : IoU moyen de 0,049 sur la page de 1346 et de 0,092 sur celle de 1501. En regardant les masques produits sur une page exemple, SAM génère un grand masque qui couvre presque toute la page, un masque sur la reliure du livre, et une série de petits masques sur des fragments graphiques sans lien avec la structure documentaire. Aucun masque ne correspond aux zones logiques annotées par les paléographes.

## Pourquoi ça ne marche pas

SAM est entraîné sur des photos naturelles (objets, animaux, scènes). Il segmente ce qui est visuellement saillant, pas ce qui est fonctionnellement significatif pour un document historique. Le parchemin médiéval ajoute des taches et des variations de couleur que SAM interprète comme des objets à segmenter, ce qui augmente le nombre de faux positifs.

## Décision

On abandonne SAM pour la segmentation de page et on passe à Kraken BLLA (étape 2.3), qui est conçu spécifiquement pour les manuscrits historiques. Le code SAM reste dans le repo pour garder une trace de la démarche.

## Référence

Kirillov, A., Mintun, E., Ravi, N., et al. (2023). Segment Anything. arXiv:2304.02643.
