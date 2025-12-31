# Askıda İlaç ve Nöbetçi Eczane Sistemi

Bu proje, Veri Yapıları ve Algoritmalar dersi kapsamında geliştirilmiş bir uygulamadır.
Amaç: derste öğrenilen veri yapıları ve algoritmaları gerçek hayatta karşılığı olan bir problem üzerinde bilinçli şekilde kullanmaktır.

Proje iki ana problemi çözer:
1. Askıda ilaç bağışlarının adil ve öncelikli şekilde ihtiyaç sahiplerine ulaştırılması
2. Kullanıcının konumuna göre, istenen ilacı stokta bulunduran en yakın nöbetçi eczanenin bulunması

---

## Proje Özeti

### 1. Askıda İlaç Sistemi
- Kullanıcılar bağış yaparak askıda ilaç fonuna katkıda bulunur.
- İlaç talep eden hastalar, öncelik puanına göre sıraya alınır.
- Öncelik puanı; aciliyet durumu ve ilacın kritiklik seviyesine göre hesaplanır.
- Fon yeterli olduğunda, en öncelikli hastaya otomatik olarak ilaç teslim edilir.
- Yapılan bağışlar geri alınabilir (undo).

### 2. Nöbetçi Eczane Sorgulama
- Kullanıcı bulunduğu konumu girer.
- İstenen ilacı stokta bulunduran eczaneler filtrelenir.
- Konumlar arası mesafeler kullanılarak en kısa yol hesaplanır.
- Kullanıcıya en yakın uygun eczane ve izlenecek rota gösterilir.

---

## Kullanılan Veri Yapıları ve Algoritmalar

- **Priority Queue (Heap)** – Hasta taleplerini öncelik puanına göre sıralamak için
- **Stack (Yığın)** – Bağış işlemlerini geri alma (undo) mekanizması için
- **Trie (Prefix Ağacı)** – İlaç isimlerinde hızlı arama ve öneri sistemi için
- **Graph + Dijkstra Algoritması** – En kısa yol ve en yakın eczane hesaplaması için
- **MergeSort** – Teslim kayıtlarını TC'ye göre sıralamak için
- **Binary Search** – Teslim kayıtlarında hızlı arama yapmak için

---

## Proje Dosya Yapısı

```
.
├── main.py
├── io_yard.py
├── ds/
│   ├── graph.py
│   ├── heap_oncelik_kuyrugu.py
│   ├── trie.py
│   ├── yigin.py
│   ├── sort_search.py
├── data/
│   ├── drugs.json
│   ├── graph.json
└── README.md
```

---

## Nasıl Çalıştırılır?

```bash
python main.py
```

---

## Test Edilen Senaryolar

- Geçersiz TC kimlik numarası girişi
- Stokta olmayan ilaç araması
- Yetersiz bakiye ile teslim denemesi
- Geçersiz konum girişi

---

## Sonuç

Bu proje, veri yapıları ve algoritmaların gerçek hayatta karşılığı olan problemler üzerinde
nasıl etkin şekilde kullanılabileceğini göstermektedir.

---

**Hazırlayanlar:**  
| Tuba Hatun Aydın |
| Zeynep Sena Beyhan |
| Kanita Abazi |