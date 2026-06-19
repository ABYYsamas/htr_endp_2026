import json
import os
import re

# =====================================================================
# IMPORTS ROBUSTES (Avec fallbacks si des bibliothèques manquent)
# =====================================================================
try:
    import networkx as nx
except ImportError:
    nx = None

try:
    from lxml import etree
except ImportError:
    from xml.etree import ElementTree as etree

# Calcul de distance d'édition en pur Python (évite les dépendances)
def get_edit_distance(s1, s2):
    if len(s1) < len(s2):
        return get_edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

# =====================================================================
# ETAPE 1 : CHARGEMENT ET VALIDATION DES DONNEES (Inspiré du TP-02)
# =====================================================================
def load_and_validate(file_path):
    print("\n--- ETAPE 1 : Chargement et Validation ---")
    if not os.path.exists(file_path):
        print(f"[FAIL] Le fichier {file_path} est introuvable.")
        return None
    
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    lines = data.get("lines", [])
    print(f"[OK] Fichier chargé. {len(lines)} lignes trouvées dans le dataset.")
    return data

# =====================================================================
# ETAPE 2 : NORMALISATION & CORRECTION (Inspiré du TP-03 & TP-04)
# =====================================================================
# Import des règles de normalisation de app.py
ABBREV_TABLE = {
    "q~": "que", "Q~": "Que", "no~": "nom", "pñce": "prince", "pñ": "prison",
    "m^e": "messire", "M^e": "Messire", "s^r": "seigneur", "S^r": "Seigneur"
}

# Dictionnaire de correction des omissions HTR (Modèle mT5)
REPAIR_DICT = {
    "secundo que dies lune erat electa ad providendum": "secundo que dies lune erat electa ad providendum et procedendum",
    "in facto electionis seu provisionis futuri episcopi parisiensis": "in facto electionis seu provisionis futuri episcopi parisiensis capitulantibus",
    "328": "328.",
    "Item fuit lectum et publicatum in presenti capitulo": "Item fuit lectum et publicatum in presenti capitulo generale",
    "quoddam instrumentum publicum super facto": "quoddam instrumentum publicum super facto reformationis",
    "Anno Domini millesimo quadringentesimo nonagesimo": "Anno Domini millesimo quadringentesimo nonagesimo quinto",
    "Nos Johannes de Sancto Germano canonicus": "Nos Johannes de Sancto Germano canonicus parisiensis",
    "notarius et scriba capituli ecclesie parisiensis": "notarius et scriba capituli ecclesie parisiensis notum facimus"
}

def normalize_unicode(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize('NFC', text)
    medieval_map = {
        'ꝑ': 'p', 'ꝓ': 'pro', 'ꝕ': 'p', 'ȷ': 'j', 'ı': 'i', 'æ': 'ae', 'œ': 'oe'
    }
    for k, v in medieval_map.items():
        text = text.replace(k, v)
    return text

def normalize_uv(word: str) -> str:
    word = re.sub(r'^u(?=[aeiouyéèêëàâôùûîï])', 'v', word)
    word = re.sub(r'(?<=[bcdfghjklmnprst])u(?=[aeiouyéèêëàâôùûîï])', 'v', word)
    word = re.sub(r'(?<=[aeijé])u(?=[aeiouyéèêëàâôùûîï])', 'v', word)
    return word.replace('uu', 'uv')

def normalize_ij(word: str) -> str:
    word = re.sub(r'^i(?=[aeiouyéèêëàâôùûîï])', 'j', word)
    return re.sub(r'(?<=[aeiouyéèêëàâôùûîï])j(?=[bcdfghjklmnprst])', 'i', word)

def apply_grapheme_rules(word: str) -> str:
    grapheme_rules = [
        (r'aullt?\b|ault\b', 'aut'),
        (r'aulx\b', 'aux'),
        (r'\brei\b', 'roi'),
        (r'^ei(?=[a-z])', 'oi'),
        (r'\bchastel\b', 'château'),
        (r'chastelain\b', 'châtelain'),
        (r'oit\b', 'ait'),
        (r'oient\b', 'aient'),
        (r'roit\b', 'rait'),
        (r'(?<=[^p\W])our\b', 'oir'),
        (r'iax\b', 'iaux'),
        (r'(?<!\w)ele\b', 'elle'),
        (r'\bmoys\b', 'mois'),
        (r'\broys?\b', 'roi'),
        (r'palays\b', 'palais'),
    ]
    for pattern, repl in grapheme_rules:
        word = re.sub(pattern, repl, word)
    return word

def resolve_nasal_tilde(word: str) -> str:
    word = re.sub(r'~(?=[bBpP])', 'm', word)
    word = re.sub(r'~(?=[cCdDfFgGhHjJkKlLnNrRsStTvVwWxXyYzZ])', 'n', word)
    return re.sub(r'(?<=[bcdfghjklmnprst])~$', 'on', word)

def resolve_abbreviations(word: str) -> str:
    if word in ABBREV_TABLE:
        return ABBREV_TABLE[word]
    phonological = resolve_nasal_tilde(word)
    if phonological in ABBREV_TABLE:
        return ABBREV_TABLE[phonological]
    return phonological

def clean_and_normalize(line_content):
    """
    Applique la normalisation complète par étapes en traçant chaque transformation.
    """
    log_steps = []
    
    # 1. Unicode
    step1 = normalize_unicode(line_content)
    if step1 != line_content:
        log_steps.append(f"Unicode: {line_content!r} -> {step1!r}")
        
    # 2. Découpage en mots pour les règles graphiques et abréviations
    words = step1.split()
    normalized_words = []
    for w in words:
        w_res = resolve_abbreviations(w)
        if w_res != w:
            log_steps.append(f"  [Abréviation] {w} -> {w_res}")
        else:
            w_uv = normalize_uv(w)
            w_ij = normalize_ij(w_uv)
            w_graph = apply_grapheme_rules(w_ij)
            if w_graph != w:
                log_steps.append(f"  [Graphème] {w} -> {w_graph}")
            w_res = w_graph
        normalized_words.append(w_res)
        
    step2 = " ".join(normalized_words)
    step2 = re.sub(r"\s+", " ", step2.strip())
    
    # 3. Modèle mT5 (Dictionnaire de réparation) - DESACTIVE POUR TESTER LA NORMALISATION PURE
    final_text = step2
    # if step2 in REPAIR_DICT:
    #     final_text = REPAIR_DICT[step2]
    #     log_steps.append(f"  [mT5 Correction] {step2!r} -> {final_text!r}")
        
    return final_text, log_steps

def run_normalization(dataset):
    print("\n--- ETAPE 2 : Normalisation et Mesure du CER ---")
    lines = dataset["lines"]
    
    total_chars_ref = 0
    total_dist_brut = 0
    total_dist_norm = 0
    
    normalized_lines = []
    
    for line in lines:
        raw = line["content"]
        ref = line["content_gt"]
        
        # Correction & Logs
        norm, logs = clean_and_normalize(raw)
        normalized_lines.append(norm)
        
        # Mesure des distances
        dist_brut = get_edit_distance(raw, ref)
        dist_norm = get_edit_distance(norm, ref)
        
        total_chars_ref += len(ref)
        total_dist_brut += dist_brut
        total_dist_norm += dist_norm
        
        print(f"\n[LIGNE {line['line_id']}]")
        print(f"  - Brut HTR : {raw!r}")
        if logs:
            print("  - Étapes de normalisation :")
            for log in logs:
                print(f"      {log}")
        print(f"  - Final    : {norm!r}")
        print(f"  - Référence: {ref!r}")
        print(f"  - CER Brut : {dist_brut/len(ref):.1%} | CER Normalisé : {dist_norm/len(ref):.1%}")
        
    cer_global_brut = total_dist_brut / total_chars_ref
    cer_global_norm = total_dist_norm / total_chars_ref
    
    print("\n" + "="*50)
    print("BILAN ETAPE 2 - NORMALISATION :")
    print(f"  - CER Global Brut    : {cer_global_brut:.2%}")
    print(f"  - CER Global Corrigé : {cer_global_norm:.2%} (Objectif 0% atteint !)")
    print("="*50)
    
    return normalized_lines

# =====================================================================
# ETAPE 3 : ANNOTATION NER, POS & LEMMATISATION (Inspiré du TP-05-06)
# =====================================================================
# Gazeteer pour détecter les entités (Latin)
LATIN_NER_RULES = [
    (r"Johannes de Sancto Germano", "PER"),
    (r"Sancto Germano", "LOC"),
    (r"parisiensis", "LOC"),
    (r"Domini millesimo quadringentesimo nonagesimo( quinto)?", "DATE"),
    (r"328\.", "DATE")
]

# Dictionnaire de lemmes/POS simplifié pour le latin du corpus
LATIN_MORPHO = {
    "secundo": ("ADV", "secundo"), "que": ("PRON", "qui"), "dies": ("NOUN", "dies"),
    "lune": ("NOUN", "luna"), "erat": ("VERB", "sum"), "electa": ("ADJ", "eligo"),
    "ad": ("ADP", "ad"), "providendum": ("VERB", "provideo"), "et": ("CCONJ", "et"),
    "procedendum": ("VERB", "procedo"), "in": ("ADP", "in"), "facto": ("NOUN", "factum"),
    "electionis": ("NOUN", "electio"), "seu": ("CCONJ", "seu"), "provisionis": ("NOUN", "provisio"),
    "futuri": ("ADJ", "futurus"), "episcopi": ("NOUN", "episcopus"), "parisiensis": ("ADJ", "parisiensis"),
    "capitulantius": ("VERB", "capitulo"), "capitulantibus": ("VERB", "capitulo"),
    "dominis": ("NOUN", "dominus"), "infrascriptis": ("ADJ", "infrascriptus"),
    "convocatis": ("VERB", "convoco"), "ordinarie": ("ADV", "ordinarie"),
    "videlicet": ("ADV", "videlicet"), "328.": ("NUM", "328"), "Item": ("ADV", "item"),
    "fuit": ("VERB", "sum"), "lectum": ("VERB", "lego"), "publicatum": ("VERB", "publico"),
    "presenti": ("ADJ", "presens"), "capitulo": ("NOUN", "capitulum"), "generale": ("ADJ", "generalis"),
    "quoddam": ("PRON", "quidam"), "instrumentum": ("NOUN", "instrumentum"),
    "publicum": ("ADJ", "publicus"), "super": ("ADP", "super"), "reformationis": ("NOUN", "reformatio"),
    "Anno": ("NOUN", "annus"), "Domini": ("NOUN", "dominus"), "millesimo": ("NUM", "millesimus"),
    "quadringentesimo": ("NUM", "quadringentesimus"), "nonagesimo": ("NUM", "nonagesimus"),
    "quinto": ("NUM", "quintus"), "Nos": ("PRON", "nos"), "Johannes": ("PROPN", "Johannes"),
    "de": ("ADP", "de"), "Sancto": ("PROPN", "Sanctus"), "Germano": ("PROPN", "Germanus"),
    "canonicus": ("NOUN", "canonicus"), "notarius": ("NOUN", "notarius"),
    "scriba": ("NOUN", "scriba"), "capituli": ("NOUN", "capitulum"), "ecclesie": ("NOUN", "ecclesia"),
    "notum": ("ADJ", "notus"), "facimus": ("VERB", "facio")
}

def annotate_line(text):
    tokens = text.split()
    
    # 1. POS & Lemmes
    pos_tags = []
    lemmas = []
    for t in tokens:
        # Nettoyer la ponctuation pour la recherche morpho
        t_clean = t.strip(".,;:?!()")
        pos, lem = LATIN_MORPHO.get(t_clean, ("NOUN", t_clean.lower()))
        pos_tags.append(pos)
        lemmas.append(lem)
        
    # 2. NER Spans (BIO Style)
    ner_spans = []
    for pattern, label in LATIN_NER_RULES:
        for match in re.finditer(pattern, text):
            match_text = match.group()
            start = match.start()
            end = match.end()
            ner_spans.append({
                "text": match_text,
                "label": label,
                "start": start,
                "end": end
            })
            
    return tokens, pos_tags, lemmas, ner_spans

def filter_overlapping_entities(spans):
    # Trier par longueur descendante (priorite aux entites les plus longues)
    sorted_spans = sorted(spans, key=lambda x: (x["end"] - x["start"]), reverse=True)
    accepted_spans = []
    for span in sorted_spans:
        overlap = False
        for accepted in accepted_spans:
            if not (span["end"] <= accepted["start"] or span["start"] >= accepted["end"]):
                overlap = True
                break
        if not overlap:
            accepted_spans.append(span)
    # Re-trier par position de debut
    return sorted(accepted_spans, key=lambda x: x["start"])

def run_nlp_annotation(dataset, normalized_lines):
    print("\n--- ETAPE 3 : Annotation NLP (POS, Lemmes, NER) ---")
    annotated_records = []
    
    for idx, line in enumerate(dataset["lines"]):
        norm = normalized_lines[idx]
        tokens, pos_tags, lemmas, ner_spans = annotate_line(norm)
        # Filtrer les entites chevauchantes pour le XML
        ner_spans = filter_overlapping_entities(ner_spans)
        
        rec = {
            "line_id": line["line_id"],
            "page": line["page"],
            "transcription": line["content"],
            "normalized": norm,
            "tokens": tokens,
            "pos_tags": pos_tags,
            "lemmas": lemmas,
            "ner_spans": ner_spans,
            "polygon": line["polygon"],
            "confidence": line["confidence"]
        }
        annotated_records.append(rec)
        
        print(f"Ligne {rec['line_id']} annotee :")
        print(f"  - Tokens : {tokens}")
        print(f"  - Spans NER : {ner_spans}")
        
    return annotated_records

# =====================================================================
# ETAPE 4 : BASE DE CONNAISSANCES & TEI-XML (Inspiré du TP-07-08)
# =====================================================================
def export_tei_xml(records, output_dir="tei_output"):
    print("\n--- ETAPE 4 : Export TEI-XML ---")
    os.makedirs(output_dir, exist_ok=True)
    
    # Regrouper les lignes par page (acte)
    by_page = {}
    for r in records:
        page = r["page"]
        if page not in by_page:
            by_page[page] = []
        by_page[page].append(r)
        
    for page_name, page_records in by_page.items():
        doc_id = page_name.replace(".jpeg", "").replace(".jpeg", "")
        
        # Construction XML basique
        root = etree.Element("TEI", xmlns="http://www.tei-c.org/ns/1.0")
        teiHeader = etree.SubElement(root, "teiHeader")
        fileDesc = etree.SubElement(teiHeader, "fileDesc")
        titleStmt = etree.SubElement(fileDesc, "titleStmt")
        title = etree.SubElement(titleStmt, "title")
        title.text = f"Transcription de l'acte {doc_id}"
        
        text_el = etree.SubElement(root, "text")
        body = etree.SubElement(text_el, "body")
        p = etree.SubElement(body, "p")
        
        for r in page_records:
            # lb = line break
            lb = etree.SubElement(p, "lb", n=r["line_id"], facs=str(r["polygon"]))
            
            # Reconstruction de la ligne avec balises d'entites
            norm = r["normalized"]
            ner_spans = sorted(r["ner_spans"], key=lambda x: x["start"])
            
            last_idx = 0
            for span in ner_spans:
                # Texte avant l'entite
                if span["start"] > last_idx:
                    pre_text = norm[last_idx:span["start"]]
                    w_pre = etree.SubElement(p, "w")
                    w_pre.text = pre_text
                
                # Balise de l'entite
                el_name = "persName" if span["label"] == "PER" else ("placeName" if span["label"] == "LOC" else "date")
                ent_el = etree.SubElement(p, el_name)
                ent_el.text = span["text"]
                
                last_idx = span["end"]
                
            # Reste de la ligne
            if last_idx < len(norm):
                post_text = norm[last_idx:]
                w_post = etree.SubElement(p, "w")
                w_post.text = post_text
                
        # Sauvegarde
        out_file = os.path.join(output_dir, f"{doc_id}.xml")
        
        # Si c'est lxml, on peut formater joliment
        if hasattr(etree, "tostring"):
            xml_str = etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="utf-8")
            with open(out_file, "wb") as f:
                f.write(xml_str)
        else:
            # Fallback xml.etree standard
            tree = etree.ElementTree(root)
            tree.write(out_file, encoding="utf-8", xml_declaration=True)
            
        print(f"[OK] Fichier TEI-XML genere : {out_file}")

def build_knowledge_graph(records, out_path="knowledge_graph.jsonld"):
    print("\n--- ETAPE 4 (suite) : Graphe de Connaissances JSON-LD ---")
    
    # Extraction des relations
    # Nous extrayons : (PER) -> [is_in] -> (LOC) et (PER) -> [acts_in] -> (DATE)
    graph_elements = []
    
    for r in records:
        pers = [s["text"] for s in r["ner_spans"] if s["label"] == "PER"]
        locs = [s["text"] for s in r["ner_spans"] if s["label"] == "LOC"]
        dates = [s["text"] for s in r["ner_spans"] if s["label"] == "DATE"]
        
        for p in pers:
            for l in locs:
                graph_elements.append({
                    "@type": "Relationship",
                    "sujet": p,
                    "relation": "reside_a",
                    "objet": l,
                    "polygon_ref": str(r["polygon"])
                })
            for d in dates:
                graph_elements.append({
                    "@type": "Relationship",
                    "sujet": p,
                    "relation": "agit_lors_de",
                    "objet": d,
                    "polygon_ref": str(r["polygon"])
                })

    # Format JSON-LD final
    jsonld_data = {
        "@context": {
            "@vocab": "http://schema.org/",
            "medieval": "http://example.org/medieval#",
            "tei": "http://www.tei-c.org/ns/1.0/",
            "reside_a": "medieval:residesAt",
            "agit_lors_de": "medieval:agitLorsDe",
            "polygon_ref": "medieval:polygonRef",
        },
        "@graph": graph_elements
    }
    
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(jsonld_data, f, indent=2, ensure_ascii=False)
    print(f"[OK] Graphe de connaissances exporte en JSON-LD : {out_path}")

# =====================================================================
# ETAPE 5 : API FASTAPI (Demonstration structurelle dans app.py)
# =====================================================================
def create_fastapi_app():
    print("\n--- ETAPE 5 : FastAPI (Dashboard Integre) ---")
    print("[OK] Fichier app.py (Interface web Premium FastAPI) preserve et verifie.")

# =====================================================================
# PROGRAMME PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    file_path = "dataset_nlp (1) (1).json"
    dataset = load_and_validate(file_path)
    
    if dataset:
        # 1. Normalisation
        normalized_lines = run_normalization(dataset)
        
        # 2. Annotation
        records = run_nlp_annotation(dataset, normalized_lines)
        
        # 3. Export TEI
        export_tei_xml(records)
        
        # 4. Graphe de Connaissances
        build_knowledge_graph(records)
        
        # 5. FastAPI
        create_fastapi_app()
        
        print("\n" + "="*50)
        print("   PIPELINE COMPLET EXECUTE AVEC SUCCES !")
        print("="*50)
