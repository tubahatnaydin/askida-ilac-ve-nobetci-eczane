from ds.graph import Graph
from io_utils import load_graph
from ds.stack import Stack
from ds.sort_search import mergesort, binary_search
from ds.heap_pq import PriorityQueue
import time
from io_utils import load_drugs
from ds.trie import Trie

# ASKIDA İLAÇ VE NÖBETÇİ ECZANE SİSTEMİ
# Veri Yapıları ve Algoritmalar Projesi
# Kullanılanlar:
# Trie: ilaç adında prefix arama ve öneri
# PriorityQueue (Heap): hastaları öncelik puanına göre sıralama
# Stack: son bağışı geri alma (UNDO) -> LIFO
# MergeSort + Binary Search: teslim kayıtlarını TC’ye göre sırala/ara
# Graph + Dijkstra: en kısa yol ile nöbetçi eczane seçimi ve rota çıkarma
# JSON I/O: drugs.json ve graph.json üzerinden veri yükleme

kasa = 0

pq = PriorityQueue()
teslimler = []
undo_stack = Stack()

drug_map = load_drugs()

graph_data = load_graph()
graph = Graph()

for edge in graph_data["edges"]:
    graph.add_edge(edge["from"], edge["to"], edge["weight"])

trie = Trie()
for ilac_adi in drug_map.keys():
    trie.insert(ilac_adi)

print("Yüklenen ilaçlar:", list(drug_map.keys()))

while(True):

    print("\nANA MENÜ\n")

    print("1 - Askıda İlaç Sistemi")
    print("2 - Nöbetçi Eczane Sorgulama")
    print("3 - Çıkış\n")

    secim = input("Seçiminizi tuşlayınız: ")

    if secim == "1":
        
        print("\nAskıda İlaç menüsüne girildi.\n")

        while(True):

            print("1 - Bağış yap")
            print("2 - Askıda ilaç sırasına gir")
            print("3 - Son teslimleri gör")
            print("4 - Bekleyen hasta sayısı")
            print("5 - Son bağışı geri al")
            print("6 - Geri dön\n")

            secim2 = input("Lütfen seçiminizi tuşlayınız: ")

            if secim2 == "1":

                print("\nBağış seçildi\n")
                print("Bu işlem ihtiyaç sahipleri için askı fonuna bakiye ekler.")
                print("Fon yeterliyse sistem sıradaki hastaya ilaç temin eder.\n")

                miktar = int(input("Bağış miktarını TL cinsinden giriniz: "))
                kasa = kasa + miktar

                undo_stack.push(("DONATION", miktar)) 
                # bir bağış yapıldı, miktarı stacke'e attık. LIFO (en son bağış en üstte)

                print("\nBağış işleminiz başarıyla gerçekleştirildi.")
                print("\nKasadaki toplam para: {} TL'dir\n".format(kasa))
                
                if len(pq) == 0:
                    print("Sırada bekleyen yok\n")
                
                else:
                    teslim_sayisi = 0
                    MAX_TESLIM = 5
                    
                    # Bağış sonrası otomatik teslim akışı:
                    # Kasadaki para yeterse en öncelikli hastaya teslim yapılır
                    # Maksimum 5 teslim (kota)
                    # Para yetmezse durur

                    while len(pq) > 0 and (teslim_sayisi < MAX_TESLIM):
                        hasta = pq.peek() # en öncelikli kişi
                        wait_minutes = int((time.time() - hasta["created_at"]) // 60)

                        # Not: Heap içinde elemanın prioritysini değiştirmek heap düzenini bozabilir
                        # Bu yüzden burada priority güncellemesi yapılmıyor

                        # hasta["priority"] = (100 * hasta["is_emergency"] + wait_minutes + drug_map[hasta["ilac"]]["criticality"])

                        hangi_ilac = hasta["ilac"]
                        fiyat = drug_map[hangi_ilac]["price"]

                        if kasa >= fiyat:
                            teslim_edilen = pq.pop() # ilk kişiyi sıradan çıkart
                            kasa = kasa - fiyat

                            teslimler.append([teslim_edilen["ad"], teslim_edilen["tc"], teslim_edilen["ilac"],fiyat]) 
                            #'teslim kaydı [ad, tc, ilaç, fiyat]

                            print("Teslim yapıldı ->",teslim_edilen["ad"],"-", teslim_edilen["ilac"])
                            teslim_sayisi = teslim_sayisi + 1
                    
                        else:
                            break
                    
                    if teslim_sayisi == MAX_TESLIM:
                        print("\nTeslim kotası doldu (5/5). Kalanlar bir sonraki bağışı bekliyor\n")
                     
                    if teslim_sayisi == 0:
                        print("\nKasadaki bakiye yetersiz. Sıradaki ilacın fiyatı:",fiyat,"TL'dir\n")
                    
                    else:
                        print("\nToplam teslim sayısı:",teslim_sayisi)
                        print("\nKalan kasa:",kasa,"TL'dir\n")

            elif secim2 == "2":

                print("\nİlaç sırasına girme seçildi\n")

                ad_soyad = input("Ad soyad giriniz: ")
                
                while True:
                    tc = input("TC giriniz (11 hane): ").strip()

                    if not tc.isdigit():
                        print("Hata: T.C. Kimlik Numarası sadece rakamlardan oluşmalıdır")
                        continue

                    if len(tc) != 11:
                        print("Hata: TC 11 haneli olmalıdır")
                        continue

                    break

                acil = input("\nAciliyet olarak önceliğiniz var mı? (E/H)")

                acil = acil.strip().upper()
                is_emergency = 1 if acil == "E" else 0

                
                print("\nMevcut ilaçlar:\n")

                for ilac_adi, info in drug_map.items():
                    print(ilac_adi,"-",info["category"],"-","(",info["price"],"TL )")

                prefix = input("\nAramak istediğiniz ilacın baştan en az bir harfini giriniz: ").strip()

                oneriler = trie.starts_with(prefix, limit=5)

                if not oneriler:
                    print("\nBu harfle başlayan ilaç yok.")
                    continue

                print("\nÖneriler:")
                
                for i, ad_ilac in enumerate(oneriler, start=1):
                    print(i, "-", ad_ilac)

                sec = input("\nSeçmek için numara yaz (iptal için Enter): ").strip()
                
                if sec == "":
                    continue

                sec_no = int(sec)
                
                if sec_no < 1 or sec_no > len(oneriler):
                    print("\nHatalı seçim.")
                    continue

                hangi_ilac = oneriler[sec_no - 1]

                # büyük/küçük harf fark etmesin diye
                secim_norm = hangi_ilac.strip().lower()
                
                for gerçek_isim in drug_map.keys():
                    
                    if gerçek_isim.lower() == secim_norm:
                        hangi_ilac = gerçek_isim
                        break


                print("\nSeçilen ilaç:", hangi_ilac)
                
                created_at = time.time()
                wait_minutes = 0

                # Öncelik puanı:
                # Acil ise +100
                # İlaç kritiklik puanı eklenir (drugs.json)
                # Not: wait_minutes burada 0 tutuldu

                priority = 100 * is_emergency + wait_minutes + drug_map[hangi_ilac]["criticality"]

                request = {"ad": ad_soyad,"tc": tc,"ilac": hangi_ilac,"is_emergency": is_emergency,"created_at": created_at,"priority": priority}

                pq.push(request)

                print("\nSıraya eklendiniz")
                print("\nÖncelik puanınız:", priority)
                print("\nBekleyen kişi sayısı:", len(pq), "\n")

            elif secim2 == "3":
                
                # Teslim kayıtları (teslimler):
                # Liste yapısı: [ad, tc, ilac, fiyat]
                # Mergesort ile TCye göre sıralıyoruz
                # Binarysearch ile TCye göre hızlı arama yapıyoruz

                print("\nSon teslimler seçildi\n")
                
                print("SON TESLİMLER\n")

                if len(teslimler) == 0:
                    print("Henüz teslim gerçekleşmedi\n")
                
                else:
                    print("1 - Normal Listele")
                    print("2 - TC'ye göre sırala (MergeSort)")
                    print("3 - TC ile teslim ara (Binary Search)\n")

                    alt = input("Seçiminizi tuşlayınız:")

                    if alt == "1":
                        for t in teslimler:
                            print("\nAd Soyad:",t[0],"TC:",t[1],"İlaç:",t[2],"Fiyat:",t[3],"TL")
                    
                    elif alt == "2":
                        sirali = mergesort(teslimler, key_index=1)
                        for t in sirali:
                            print("\nAd Soyad:",t[0],"TC:",t[1],"İlaç:",t[2],"Fiyat:",t[3],"TL")
                    
                    elif alt == "3":
                        tc_ara = input("\nTC giriniz:")
                        sirali = mergesort(teslimler, key_index=1)
                        sonuc = binary_search(sirali, tc_ara)

                        if sonuc:
                            print("\nBULUNDU →", sonuc)
                        else:
                            print("\nBu TC ile teslim bulunamadı")

                    else:
                        print("\nGeçersiz seçim\n")

            elif secim2 == "4":

                print("\nBEKLEYEN HASTA DURUMU\n")
                print("Bekleyen kişi sayısı:",len(pq))
                print()
            
            elif secim2 == "5":
                if len(undo_stack) == 0:
                    print("\nGeri alınacak işlem yok\n")
                
                else:
                    son_islem = undo_stack.pop()

                    if son_islem[0] == "DONATION":
                        miktar = son_islem[1]
                        kasa = kasa - miktar
                        
                        if kasa < 0:
                            kasa = 0
                        
                        print("\nSon bağış geri alındı")
                        print("\nGeri alınan miktar:", miktar, "TL")
                        print("\nGüncel kasa:", kasa, "TL\n")
                        # son bağış ilk geri alınır (LIFO)
                        # stack gerçek senaryo

            elif secim2 == "6":
                break
            
            else:
                print("\nGeçersiz seçim!\n")

    elif secim == "2":
        # Nöbetçi eczane sorgulama:
        # 1 - Kullanıcı konumunu al
        # 2 - Dijkstra ile tüm düğümlere en kısa mesafeleri hesapla
        # 3 - İstenen ilacı stokta bulunduran eczaneler arasından en yakını seç
        # 4 - shortest_path ile rota çıkar

        print("\nNöbetçi Eczane menüsüne girildi.\n")
        print("NÖBETÇİ ECZANE (EN KISA YOL)\n")

        print("Mevcut konumlar:")
        for n in graph_data["nodes"]:
            print("-", n)
        
        start = input("\nBulunduğunuz konumu giriniz: ").strip()

        def normalize_tr(text): 
            return text.strip().lower().replace("ı", "i")
        
        start_norm = normalize_tr(start)

        start_norm = normalize_tr(start)

        matched_start = None

        for node in graph.adj.keys():
            if normalize_tr(node) == start_norm:
                matched_start = node
                break
        
        if matched_start is None:
            print("Geçersiz konum.")
            continue

        start = matched_start

        dist, prev = graph.dijkstra(start)

        en_yakin = None
        min_mesafe = float("inf")

        print("\nMevcut ilaçlar:")
        mevcut_ilaclar = set()

        for eczane in graph_data["pharmacies"]:
            for ilac in eczane["stock"]:
                mevcut_ilaclar.add(ilac)
        
        for ilac in sorted(mevcut_ilaclar):
            print("-", ilac)

        prefix = input("\nAradığınız ilacın ilk harflerini giriniz: ").strip()

        oneriler = trie.starts_with(prefix, limit=5)

        if not oneriler:
            print("\nBu harflerle başlayan bir ilaç bulunamadı.\n")
            continue
        
        print("\nÖnerilen ilaçlar:")

        for i, ilac in enumerate(oneriler, start=1):
            print(f"{i} - {ilac}")
        
        sec = input("\nSeçiminizi numara ile yapınız (iptal için Enter): ").strip()

        if sec == "":
            continue

        if not sec.isdigit():
            print("\nLütfen sadece numara giriniz.\n")
            continue

        sec_no = int(sec)

        if sec_no < 1 or sec_no > len(oneriler):
            print("\nGeçersiz seçim.\n")
            continue

        istenen_ilac = oneriler[sec_no - 1]
        print("\nSeçilen ilaç:", istenen_ilac)

        istenen_norm = normalize_tr(istenen_ilac)

        for eczane in graph_data["pharmacies"]:
            stok_norm = [normalize_tr(i) for i in eczane["stock"]]

            if istenen_norm not in stok_norm:
                continue

            loc = eczane["location"]

            if dist[loc] < min_mesafe:
                min_mesafe = dist[loc]
                en_yakin = eczane

        if en_yakin is None:
            print("\nBu ilacı stokta bulunduran nöbetçi eczane yok.\n")
            continue

        yol = graph.shortest_path(prev, en_yakin["location"])

        print("\nEn yakın nöbetçi eczane:", en_yakin["name"])
        print("\nStokta bulunan ilaçlar:",", ".join(en_yakin["stock"]))
        print("\nToplam mesafe:", min_mesafe, "km")
        print("Önerilen güzergah:", " -> ".join(yol), "\n")

    elif secim == "3":
        print("Program sonlanıyor...")
        break
    else:
        print("\nGeçersiz tuşlama yaptınız! Tekrar deneyiniz.")
