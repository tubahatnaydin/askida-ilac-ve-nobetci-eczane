"""
SIRALAMA VE ARAMA ALGORİTMALARI
bu modül teslim kayıtlarını sıralamak ve aramak için kullanılır
MergeSort ve BinarySearch algoritmalarını içerir
"""

def mergesort(liste, key_index):
    """
    MergeSort algoritması ile listeyi sıralar

        1. liste 1 elemanlı veya boşsa döndür (temel durum)
        2. listeyi ortadan ikiye böl
        3. her iki yarıyı recursive olarak sırala
        4. iki sıralı yarıyı birleştir (merge)
    """
    
    # TEMEL DURUM: liste zaten sıralı kabul edilir

    if len(liste) <= 1:
        return liste
    
    # 1. ADIM: lsteyi ortadan ikiye böl
    mid = len(liste) // 2

    # 2. ADIM: sol ve sağ yarıları recursive olarak sırala
    sol = mergesort(liste[:mid], key_index)     # 0dan mide kadar
    sag = mergesort(liste[mid:], key_index)     # midten sona kadar

    # 3. ADIM: iki sıralı listeyi birleştir
    return merge(sol, sag, key_index)

def merge(sol, sag, key_index):
    """
    iki sıralı listeyi birleştirir (merge işlemi)

        iki listenin başındaki öğeleri karşılaştırır, küçük olanı sonuç listesine ekler
    """
    
    sonuc = []      # birleştirilmiş listeyi sakla
    i = j = 0       # sol ve sağ listeler için pointerlar

    # 1. ADIM: iki listenin de öğeleri varken karşılaştır
    while i < len(sol) and j < len(sag):

        # key_index'e göre karşılaştır
        if sol[i][key_index] <= sag[j][key_index]:

            # sol listedeki daha küçük veya eşit
            sonuc.append(sol[i])    # soldan ekle
            i += 1      # sol pointerı ilerlet
        else:
            # sağ listedeki daha küçük
            sonuc.append(sag[j])    # sağdan ekle
            j += 1     # sağ pointerı ilerlet

    # 2. ADIM: kalan öğeleri ekle (bir liste boşaldığında)

    # sol listede kalan öğeler varsa hepsini ekle
    sonuc.extend(sol[i:])

    # sağ listede kalan öğeler varsa hepsini ekle
    sonuc.extend(sag[j:])
    return sonuc

def binary_search(sorted_list, tc, tc_index=1):
    """
    binary Search algoritması ile sıralı listede TCye göre arama yapar
    
        1. listenin ortasındaki öğeyi kontrol et
        2. eşitse bulundu
        3. küçükse sağ yarıyı atla
        4. büyükse sol yarıyı atla
        5. bulunamazsa None döndür
    """
    
    # arama aralığını başlat: tüm liste
    alt = 0
    ust = len(sorted_list) - 1

    # arama aralğı boşalana kadar döngü
    while alt <= ust:
        mid = (alt + ust) // 2      # orta noktayı hesapla

        # 1. DURUM: TC BULUNDU
        if sorted_list[mid][tc_index] == tc:
            return sorted_list[mid]     # kaydı döndür
        
        # 2. DURUM: aranan TC daha BÜYÜK (sayısal olarak)
        elif sorted_list[mid][tc_index] < tc: 
            alt = mid + 1       # sağ yarıya odaklan

        # 3. DURUM: aranan TC daha KÜÇÜK
        else:
            ust = mid - 1   # sol yarıya odaklan
    
    # TC bulunamadı
    return None
