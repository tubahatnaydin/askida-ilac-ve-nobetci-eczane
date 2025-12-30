"""
GİRDİ/ÇIKTI İŞLEMLERİ MODÜLÜ
Bu modül projedeki JSON veri dosyalarını yüklemekten sorumludur
İlaç verileri ve grafik verilerini diskten okur python yapılarına dönüştürür
"""

import json
from pathlib import Path

# PROJE KÖK DİZİNİNİ BELİRLEME
# __file__ ile mevcut dosyanın yolunu alıp parent ile bir üst dizine çıkıyoruz
# böylece proje kök dizinini dinamik olarak buluyoruz
TEMEL_DIZIN = Path(__file__).resolve().parent

def ilaclari_yukle():
    """
    drugs.json dosyasından ilaç verilerini yükler.
    
    JSON formatındaki ilaç listesini okur her ilaç için sözlük oluşturur, ilaç ismini anahtar, diğer bilgileri değer olarak saklar
    
    """
    
    # data/drugs.json dosya yolunu oluştur
    ilac_yolu = TEMEL_DIZIN / "data" / "drugs.json"

    # UTF8 encoding ile JSON dosyasını aç ve oku
    with open(ilac_yolu, "r", encoding="utf-8") as dosya:
        # JSON içeriğini python listesine dönüştür
        ilac_listesi = json.load(dosya)

    # ilaç bilgilerini saklamak için boş sözlük oluştur
    ilac_sozlugu = {}

    # her ilaç için döngü başlat
    for ilac in ilac_listesi:
        # ilaç adını al
        ad = ilac["name"]
        
        # ilaç bilgilerini sözlüğe ekle
        # JSONdaki string fiyat ve kritikliği inte çevir
        # kategori bilgisi yoksa varsayılan "Bilinmiyor" kullan
        ilac_sozlugu[ad] = {
            "price": int(ilac["price"]),
            "criticality": int(ilac["criticality"]),
            "category": ilac.get("category", "Bilinmiyor")  
            # .get() ile güvenli erişim
        }

    # oluşturulan ilaç sözlüğünü döndür
    return ilac_sozlugu

def yukle_graph():
    """
    graph.json dosyasından grafik verilerini yükler
    
    graf yapısını (düğümler, kenarlar, eczaneler) içeren JSON dosyasını okur
    bu veriler harita ve konum bilgilerini içerir
    """
    
    # burada importları fonksiyon içinde yapıyoruz (yerel kapsamda)
    import json
    from pathlib import Path

    # TEMEL_DIZIN yeniden tanımla (fonksiyon içi kapsam)
    TEMEL_DIZIN = Path(__file__).resolve().parent
    
    # data/graph.json dosya yolunu oluştur
    graph_yolu = TEMEL_DIZIN / "data" / "graph.json"

    # JSON dosyasını aç ve direkt olarak python sözlüğüne dönüştürerek döndür
    with open(graph_yolu, "r", encoding="utf-8") as dosya:
        return json.load(dosya)  # otomatik olarak parse edilmiş sözlüğü döndür

import json
from pathlib import Path

TEMEL_DIZIN = Path(__file__).resolve().parent

def ilaclari_yukle():
    ilac_yolu = TEMEL_DIZIN / "data" / "drugs.json"

    with open(ilac_yolu, "r", encoding="utf-8") as dosya:
        # JSON dosyasını oku ve python listesine dönüştür
        ilac_listesi = json.load(dosya)

    ilac_sozlugu = {}

    for ilac in ilac_listesi:
        ad = ilac["name"]   # ilaç adını al
        ilac_sozlugu[ad] = {
            "price": int(ilac["price"]),"criticality":int(ilac["criticality"]),"category": ilac.get("category","Bilinmiyor")}
        # ilaç fiyatını inte çevir (JSONda string olabilir), ilaç kritiklik seviyesini inte çevir, kategori bilgisini al yoksa "Bilinmiyor" kullan

    return ilac_sozlugu

def yukle_graph():
    # graf verisini yüklemek için gerekli modülleri içe aktar
    import json
    from pathlib import Path

    # TEMEL_DIZINi bu fonksiyon için yeniden tanımla (yerel kapsamda olması için)
    TEMEL_DIZIN = Path(__file__).resolve().parent

    # graph.json dosyasının yolunu oluştur
    graph_yolu = TEMEL_DIZIN / "data" / "graph.json"

    # JSON dosyasını UTF8 encoding ile aç
    with open(graph_yolu, "r", encoding="utf-8") as dosya:
        # json.load() ile dosya içeriğini direkt olarak python sözlüğüne dönüştür ve döndür
        return json.load(dosya)
    
        # Dönen veri formatı:
        # {
        #   "nodes": ["Kadıköy", "Moda", ...],
        #   "edges": [{"from": "...", "to": "...", "weight": ...}, ...],
        #   "pharmacies": [{"name": "...", "location": "...", "stock": [...]}, ...]
        # }