"""
ANA PROGRAM 
bu dosya tüm sistemin koordinasyonunu sağlar
kullanıcı menüleri, iş akışları ve modül entegrasyonu burada yapılır

SİSTEM AKIŞI:
- kullanıcı ana menüden seçim yapar
- seçime göre alt menülere yönlendirilir
- işlemler gerçekleştirilir (bağış, talep, teslim, arama)
- program kullanıcı çıkış yapana kadar devam eder
"""

from ds.graph import Graph   # graf ve dijkstra algoritması - en kısa yol hesaplama
from io_yard import ilaclari_yukle, yukle_graph   # JSON veri yükleme fonksiyonları
from ds.yigin import Stack   # stack (undo) veri yapısı -  geri alma
from ds.sort_search import mergesort, binary_search   # sıralama ve arama
from ds.heap_oncelik_kuyrugu import PriorityQueue   # öncelik kuyruğu - acil durum sıralaması
import time   # zaman işlemleri için - kayıt zamanı ve bekleme süresi hesaplama
from ds.trie import Trie  # Trie (prefix ağacı) - ilaç öneri sistemi

kasa = 0
"""
KASA (FON): 
- bağışlardan gelen paralar burada birikir
- hastalara ilaç teslim edildikçe buradan düşülür
- her bağışta artar her teslimde azalır
"""

oncelik_kuyrugu = PriorityQueue()
"""
ÖNCELİK KUYRUĞU:
- bekleyen hastalar bu kuyrukta sıralanır
- öncelik puanına göre sıralama yapar (max-heap)
- öncelik puanı = (acil_mi * 100) + ilaç_kritikliği + bekleme_süresi
- acil durumlar, kritik ilaç ihtiyacı olanlar öne geçer
"""

teslim_kayitlari = []
"""
TESLİM KAYITLARI:
- her ilaç teslimi bu listeye kaydedilir
- her kayıt: [ad, tc, ilaç_adı, fiyat] formatında
- MergeSort ile TCye göre sıralanabilir
- BinarySearch ile TCye göre hızlı arama yapılabilir
"""

undo_yigin = Stack()
"""
UNDO YIĞINI (STACK):
- yapılan bağışlar LIFO ile saklanır
- son yapılan bağış ilk geri alınır
- her öğe: ("DONATION", miktar) formatında
- sadece bağış işlemleri için kullanılır
"""

# ilaç verilerini yükle - drugs.json
ilac_haritasi = ilaclari_yukle()

# graf verilerini yükle - graph.json
graf_verisi = yukle_graph()

"""
bu projede kenar terimi graf teorisinden geliyor 
iki semt arasındaki bağlantıyı yani yolu temsil ediyor

her kenarın üç özelliği var:
hangi semtten başladığı 
hangi semte gittiği  
aradaki mesafe (km cinsinden)

ÖR: kadıköyden modaya 2 km bir kenardır 
toplam 12 kenar var yani 12 farklı yol bağlantısı
"""

# graf nesnesi oluştur ve kenarları ekle
graph = Graph()

# graf verisindeki tüm kenarları graf nesnesine ekle
for kenar in graf_verisi["edges"]:
    graph.kenar_ekle(kenar["from"], kenar["to"], kenar["weight"])

# Trie (prefix ağacı) oluştur ve ilaç isimlerini ekle
trie = Trie()
"""
TRIE NESNESİ:
- prefix araması için kullanılır
- kullanıcı ilacın ilk harflerini girdiğinde öneri sunar
"""

# tüm ilaç isimlerini Trieye ekle
for ilac_adi in ilac_haritasi.keys():
    trie.insert(ilac_adi)

print("Yüklenen ilaçlar:", list(ilac_haritasi.keys()))

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

                # undo stacke kaydet (geri alma için)
                undo_yigin.push(("DONATION", miktar)) 
                # bir bağış yapıldı, miktarı stacke attık -  LIFO (en son bağış en üstte)

                print("\nBağış işleminiz başarıyla gerçekleştirildi.")
                print("\nKasadaki toplam para: {} TL'dir\n".format(kasa))
                
                if len(oncelik_kuyrugu) == 0:
                    print("Sırada bekleyen yok\n")
                
                else:
                    teslim_sayisi = 0
                    MAX_TESLIM = 5
                    
                    # bağış sonrası otomatik teslim akışı:
                    # kasadaki para yeterse en öncelikli hastaya teslim yapılır
                    # maks 5 teslim (kota)
                    # para yetmezse durur

                    while len(oncelik_kuyrugu) > 0 and (teslim_sayisi < MAX_TESLIM):
                        hasta = oncelik_kuyrugu.peek() # en öncelikli kişi
                        bekleme_dakika = int((time.time() - hasta["kayit_zamani"]) // 60)   # bekleme süresini hesapla(dk)

                        hangi_ilac = hasta["ilac"]
                        fiyat = ilac_haritasi[hangi_ilac]["price"]

                        if kasa >= fiyat:
                            teslim_edilen = oncelik_kuyrugu.pop() # ilk kişiyi sıradan çıkart
                            kasa = kasa - fiyat

                            teslim_kayitlari.append([teslim_edilen["ad"], teslim_edilen["tc"], teslim_edilen["ilac"],fiyat]) 
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

                    if not tc.isdigit():    # sadece rakam kontrolü
                        print("Hata: T.C. Kimlik Numarası sadece rakamlardan oluşmalıdır")
                        continue

                    if len(tc) != 11:   # uzunluk kontrolü
                        print("Hata: TC 11 haneli olmalıdır")
                        continue

                    break

                acil = input("\nAciliyet olarak önceliğiniz var mı? (E/H)")

                acil = acil.strip().upper()
                acil_mi = 1 if acil == "E" else 0
                """
                ACİL DURUM:
                E: Evet -> acil_mi = 1 -> 100 puan
                H: Hayır -> acil_mi = 0 -> 0 puan
                """
                
                print("\nMevcut ilaçlar:\n")

                for ilac_adi, info in ilac_haritasi.items():
                    print(ilac_adi,"-",info["category"],"-","(",info["price"],"TL )")

                # Trie ile ilaç önerisi
                prefix = input("\nAramak istediğiniz ilacın baştan en az bir harfini giriniz: ").strip()

                oneriler = trie.prefix_ara(prefix, limit=5)

                if not oneriler:
                    print("\nBu harfle başlayan ilaç yok.")
                    continue    # menüye geri dön

                print("\nÖneriler:")
                
                for i, ad_ilac in enumerate(oneriler, start=1):
                    print(i, "-", ad_ilac)

                sec = input("\nSeçmek için numara yaz (iptal için Enter): ").strip()
                
                if sec == "":
                    continue    # iptal

                sec_no = int(sec)
                
                if sec_no < 1 or sec_no > len(oneriler):
                    print("\nHatalı seçim.")
                    continue

                hangi_ilac = oneriler[sec_no - 1]

                # büyük/küçük harf fark etmesin diye
                secim_norm = hangi_ilac.strip().lower()
                
                for gerçek_isim in ilac_haritasi.keys():
                    
                    if gerçek_isim.lower() == secim_norm:
                        hangi_ilac = gerçek_isim
                        break


                print("\nSeçilen ilaç:", hangi_ilac)
                
                # öncelik puanı hesapla
                kayit_zamani = time.time()
                bekleme_dakika = 0  # yeni kayıtta bekleme süresi 0

                # öncelik puanı
                # acil ise +100
                # ilaç kritiklik puanı eklenir (drugs.json)
                # not -> bekleme_dakika burada 0 tutuldu

                oncelik_puani = 100 * acil_mi + bekleme_dakika + ilac_haritasi[hangi_ilac]["criticality"]

                istek = {"ad": ad_soyad,"tc": tc,"ilac": hangi_ilac,"acil_mi": acil_mi,"kayit_zamani": kayit_zamani,"oncelik": oncelik_puani}

                oncelik_kuyrugu.push(istek)

                print("\nSıraya eklendiniz")
                print("\nÖncelik puanınız:", oncelik_puani)
                print("\nBekleyen kişi sayısı:", len(oncelik_kuyrugu), "\n")

            elif secim2 == "3":
                
                # tslim kayıtları
                # liste yapısı: [ad, tc, ilac, fiyat]
                # mergesort ile TCye göre sıralıyoruz
                # binarysearch ile TCye göre hızlı arama yapıyoruz

                print("\nSon teslimler seçildi\n")
                
                print("SON TESLİMLER\n")

                if len(teslim_kayitlari) == 0:
                    print("Henüz teslim gerçekleşmedi\n")
                
                else:
                    print("1 - Normal Listele")
                    print("2 - TC'ye göre sırala")
                    print("3 - TC ile teslim ara\n")

                    alt = input("Seçiminizi tuşlayınız:")

                    if alt == "1":    # normal listele
                        for t in teslim_kayitlari:
                            print("\nAd Soyad:",t[0],"TC:",t[1],"İlaç:",t[2],"Fiyat:",t[3],"TL\n")
                    
                    elif alt == "2": # mergesort ile TCye göre sırala
                        sirali = mergesort(teslim_kayitlari, key_index=1)
                        for t in sirali:
                            print("\nAd Soyad:",t[0],"TC:",t[1],"İlaç:",t[2],"Fiyat:",t[3],"TL\n")
                    
                    # TC ile ara (binary search)
                    elif alt == "3":
                        tc_ara = input("\nTC giriniz:")
                        
                        # önce sırala
                        sirali = mergesort(teslim_kayitlari, key_index=1)

                        # binarysearch ile ara
                        sonuc = binary_search(sirali, tc_ara)

                        if sonuc:
                            print("\nBULUNDU →", sonuc)
                        else:
                            print("\nBu TC ile teslim bulunamadı")

                    else:
                        print("\nGeçersiz seçim\n")

            elif secim2 == "4":

                print("\nBEKLEYEN HASTA DURUMU\n")
                print("Bekleyen kişi sayısı:",len(oncelik_kuyrugu))
                print()
            
            elif secim2 == "5":
                """
                GERİ ALMA (UNDO) İŞLEMİ:
                - undo stackten son işlemi al
                - eğer bağış ise, kasadan çıkar
                - kasayı negatif olmaması için kontrol et
                - kullanıcıya bilgi ver
                """

                if len(undo_yigin) == 0:
                    print("\nGeri alınacak işlem yok\n")
                
                else:
                    # stackten son işlemi al - LIFO
                    son_islem = undo_yigin.pop()

                    if son_islem[0] == "DONATION":
                        miktar = son_islem[1]
                        kasa = kasa - miktar
                        
                        # kasa negatif olmamalı
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
        # nöbetçi eczane sorgulama
        # kullanıcı konumunu al
        # dijkstra ile tüm düğümlere en kısa mesafeleri hesapla
        # istenen ilacı stokta bulunduran eczaneler arasından en yakını seç

        print("\nNöbetçi Eczane menüsüne girildi.\n")
        print("NÖBETÇİ ECZANE (EN KISA YOL)\n")

        print("Mevcut konumlar:")
        for n in graf_verisi["nodes"]:
            print("-", n)
        
        baslangic = input("\nBulunduğunuz konumu giriniz: ").strip()

        def normalize_tr(text): 
            return text.strip().lower().replace("ı", "i")

        baslangic_norm = normalize_tr(baslangic)

        # graf düğümleri arasında eşleşen konumu bul
        eslesen_baslangic = None

        for node in graph.adj.keys():
            if normalize_tr(node) == baslangic_norm:
                eslesen_baslangic = node
                break
        
        if eslesen_baslangic is None:
            print("\nGeçersiz konum.")
            continue    # ana menü

        baslangic = eslesen_baslangic

        # dijkstra ile en kısa yolları hesapla
        mesafe, onceki = graph.dijkstra(baslangic)

        en_yakin_eczane = None
        min_mesafe = float("inf")

        print("\nMevcut ilaçlar:")
        mevcut_ilaclar = set()

        for eczane in graf_verisi["pharmacies"]:
            for ilac in eczane["stock"]:
                mevcut_ilaclar.add(ilac)
        
        for ilac in sorted(mevcut_ilaclar):
            print("-", ilac)

        # Trie ile ilaç önerisi
        prefix = input("\nAradığınız ilacın ilk harflerini giriniz: ").strip()

        oneriler = trie.prefix_ara(prefix, limit=5)

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

        for eczane in graf_verisi["pharmacies"]:
            stok_norm = [normalize_tr(i) for i in eczane["stock"]]

            if istenen_norm not in stok_norm:
                continue

            konum = eczane["location"]

            if mesafe[konum] < min_mesafe:
                min_mesafe = mesafe[konum]
                en_yakin_eczane = eczane

        if en_yakin_eczane is None:
            print("\nBu ilacı stokta bulunduran nöbetçi eczane yok.\n")
            continue

        yol = graph.en_kisa_yol(onceki, en_yakin_eczane["location"])

        print("\nEn yakın nöbetçi eczane:", en_yakin_eczane["name"])
        print("\nStokta bulunan ilaçlar:",", ".join(en_yakin_eczane["stock"]))
        print("\nToplam mesafe:", min_mesafe, "km")
        print("Önerilen güzergah:", " -> ".join(yol), "\n")

    elif secim == "3":
        print("Program sonlanıyor...")
        break
    else:
        print("\nGeçersiz tuşlama yaptınız! Tekrar deneyiniz.")
