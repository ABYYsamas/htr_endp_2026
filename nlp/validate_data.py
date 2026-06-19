import json
import os
import sys

def load_json(file_path):
    """Charge le fichier JSON."""
    if not os.path.exists(file_path):
        print(f"Erreur : Le fichier '{file_path}' n'existe pas.")
        return None
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except json.JSONDecodeError as e:
        print(f"Erreur de décodage JSON : {e}")
        return None

def validate_dataset(data):
    """Valide la structure du jeu de données."""
    if not isinstance(data, dict):
        print("Erreur de structure : Le fichier doit contenir un objet JSON (dictionnaire).")
        return False

    # 1. Validation des métadonnées
    if "metadata" not in data:
        print("Erreur de structure : Le champ 'metadata' est manquant.")
        return False
    
    metadata = data["metadata"]
    required_metadata = ["project", "corpus", "cer_global", "n_lines_total"]
    for key in required_metadata:
        if key not in metadata:
            print(f"Attention : La métadonnée '{key}' est manquante.")

    # 2. Validation des lignes
    if "lines" not in data:
        print("Erreur de structure : Le champ 'lines' est manquant.")
        return False
    
    lines = data["lines"]
    if not isinstance(lines, list):
        print("Erreur de structure : Le champ 'lines' doit être une liste.")
        return False

    print(f"Validation en cours de {len(lines)} lignes...")
    
    required_line_keys = {
        "line_id": str,
        "page": str,
        "content": str,
        "content_gt": str,
        "confidence": float,
        "polygon": list,
        "needs_review": bool
    }

    errors = 0
    for idx, line in enumerate(lines):
        line_id = line.get("line_id", f"index_{idx}")
        for key, expected_type in required_line_keys.items():
            if key not in line:
                print(f"Ligne {line_id} (index {idx}) : Le champ '{key}' est manquant.")
                errors += 1
            elif not isinstance(line[key], expected_type):
                # Cas spécial : les entiers peuvent être acceptés pour les flottants
                if expected_type == float and isinstance(line[key], int):
                    continue
                print(f"Ligne {line_id} (index {idx}) : Le champ '{key}' est de type {type(line[key])} au lieu de {expected_type}.")
                errors += 1

    if errors == 0:
        print("[OK] Validation reussie ! Aucune erreur de structure detectee.")
        return True
    else:
        print(f"[FAIL] Validation echouee : {errors} erreurs detectees.")
        return False

def generate_report(data):
    """Affiche des statistiques descriptives sur le jeu de données."""
    lines = data["lines"]
    total_lines = len(lines)
    
    confidences = [l["confidence"] for l in lines if "confidence" in l]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    needs_review_count = sum(1 for l in lines if l.get("needs_review") is True)
    
    languages = {}
    strata = {}
    pages = set()
    
    for l in lines:
        lang = l.get("language", "inconnu")
        languages[lang] = languages.get(lang, 0) + 1
        
        strat = l.get("stratum", "inconnu")
        strata[strat] = strata.get(strat, 0) + 1
        
        if "page" in l:
            pages.add(l["page"])

    print("\n" + "="*40)
    print("      RAPPORT STATISTIQUE DU CORPUS")
    print("="*40)
    print(f"Nombre de lignes chargées : {total_lines}")
    print(f"Nombre de pages uniques   : {len(pages)}")
    print(f"Confiance moyenne (HTR)   : {avg_confidence:.2%}")
    print(f"Lignes à réviser (needs_review) : {needs_review_count} ({needs_review_count/total_lines:.1%})")
    
    print("\nDistribution des langues :")
    for lang, count in languages.items():
        print(f"  - {lang} : {count} ({count/total_lines:.1%})")
        
    print("\nDistribution des époques (strata) :")
    for strat, count in strata.items():
        print(f"  - {strat} : {count} ({count/total_lines:.1%})")
    print("="*40)

def split_dataset(data, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Sépare le jeu de données en Train / Val / Test.
    Pour éviter la fuite de données (data leakage), on regroupe les lignes par PAGE.
    Ainsi, toutes les lignes d'une même page vont dans le même split.
    """
    lines = data["lines"]
    
    # 1. Regrouper les lignes par page
    pages_dict = {}
    for line in lines:
        page = line.get("page", "inconnue")
        if page not in pages_dict:
            pages_dict[page] = []
        pages_dict[page].append(line)
        
    # 2. Trier les pages pour assurer un découpage déterministe
    unique_pages = sorted(list(pages_dict.keys()))
    
    # Mélange reproductible
    import random
    random.seed(42)
    random.shuffle(unique_pages)
    
    n_pages = len(unique_pages)
    n_train = max(1, int(n_pages * train_ratio))
    n_val = max(1, int(n_pages * val_ratio))
    
    train_pages = unique_pages[:n_train]
    val_pages = unique_pages[n_train:n_train+n_val]
    test_pages = unique_pages[n_train+n_val:]
    
    train_lines = []
    val_lines = []
    test_lines = []
    
    for page in train_pages:
        train_lines.extend(pages_dict[page])
    for page in val_pages:
        val_lines.extend(pages_dict[page])
    for page in test_pages:
        test_lines.extend(pages_dict[page])
        
    print("\n" + "="*40)
    print("      DECOUPAGE TRAIN / VAL / TEST (Par Page)")
    print("="*40)
    print(f"Total pages : {n_pages} -> Train: {len(train_pages)}, Val: {len(val_pages)}, Test: {len(test_pages)}")
    print(f"Total lignes : {len(lines)}")
    print(f"  - Train : {len(train_lines)} lignes ({len(train_lines)/len(lines):.1%})")
    print(f"  - Val   : {len(val_lines)} lignes ({len(val_lines)/len(lines):.1%})")
    print(f"  - Test  : {len(test_lines)} lignes ({len(test_lines)/len(lines):.1%})")
    print("="*40)
    
    return {
        "train": train_lines,
        "val": val_lines,
        "test": test_lines
    }

if __name__ == "__main__":
    file_path = "dataset_nlp (1) (1).json"
    print(f"Chargement de {file_path}...")
    dataset = load_json(file_path)
    
    if dataset:
        is_valid = validate_dataset(dataset)
        if is_valid:
            generate_report(dataset)
            splits = split_dataset(dataset)
            
            # Optionnel : sauvegarder les splits sur le disque
            os.makedirs("data_split", exist_ok=True)
            for split_name, split_lines in splits.items():
                split_data = {
                    "metadata": {
                        "parent_project": dataset["metadata"].get("project"),
                        "split_name": split_name,
                        "n_lines": len(split_lines)
                    },
                    "lines": split_lines
                }
                out_path = f"data_split/{split_name}.json"
                with open(out_path, "w", encoding="utf-8") as out_f:
                    json.dump(split_data, out_f, indent=2, ensure_ascii=False)
                print(f"Sauvegardé : {out_path}")
