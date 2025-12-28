import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def load_drugs():
    drugs_path = BASE_DIR / "data" / "drugs.json"

    with open(drugs_path, "r", encoding="utf-8") as f:
        drugs_list = json.load(f)

    drug_map = {}
    for d in drugs_list:
        name = d["name"]
        drug_map[name] = {
            "price": int(d["price"]),"criticality":int(d["criticality"]),"category": d.get("category","Bilinmiyor")}

    return drug_map

def load_graph():
    import json
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent
    path = BASE_DIR / "data" / "graph.json"

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
