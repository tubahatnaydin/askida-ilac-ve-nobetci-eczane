import json
from pathlib import Path

TEMEL_DIZIN = Path(__file__).resolve().parent

def ilaclari_yukle():
    ilac_yolu = TEMEL_DIZIN / "data" / "drugs.json"

    with open(ilac_yolu, "r", encoding="utf-8") as dosya:
        ilac_listesi = json.load(dosya)

    ilac_sozlugu = {}

    for ilac in ilac_listesi:
        ad = ilac["name"]
        ilac_sozlugu[ad] = {
            "price": int(ilac["price"]),"criticality":int(ilac["criticality"]),"category": ilac.get("category","Bilinmiyor")}

    return ilac_sozlugu

def yukle_graph():
    import json
    from pathlib import Path

    TEMEL_DIZIN = Path(__file__).resolve().parent
    graph_yolu = TEMEL_DIZIN / "data" / "graph.json"

    with open(graph_yolu, "r", encoding="utf-8") as dosya:
        return json.load(dosya)
