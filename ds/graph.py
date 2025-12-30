"""
GRAF VERİ YAPISI VE DİJKSTRA ALGORİTMASI

Bu modül konumlar arasındaki bağlantıları ve en kısa yolları hesaplamak için kullanılır

harita temsilinde düğümler (semtler) ve kenarlar (yollar) bulunur
"""
import heapq  # min-heap kuyruğu için (öncelik kuyruğu uygulaması)

class Graph:
    # çift yönlü ağırlıklı graf sınıfı

    def __init__(self):
        # boş bir graf oluşturur, komşuluk listesi sözlüğü başlatılır

        self.adj = {}

    def kenar_ekle(self, u, v, w):
        """
        grafa çift yönlü kenar ekler
        
        args:
            u (str): ilk düğüm (örn: "Kadıköy")
            v (str): ikinci düğüm (örn: "Moda")
            w (int/float): kenar ağırlığı (mesafe, km cinsinden)
        
        işlem:
            1. eğer düğümler komşuluk listesinde yoksa ekler
            2. her iki yönde de kenar ekler (çift yönlü graf)
        """
        
        # eğer u düğümü komşuluk listesinde yoksa boş liste ile ekle

        if u not in self.adj:
            self.adj[u] = []
        
        # eğer v düğümü komşuluk listesinde yoksa boş liste ile ekle
        if v not in self.adj:
            self.adj[v] = []

        # udan vye kenar ekle  u → v, ağırlık w
        self.adj[u].append((v, w))

        # vden uya kenar ekle  v → u, ağırlık w
        self.adj[v].append((u, w))  # çift yönlü

    def dijkstra(self, start):

        """
        dijkstra algoritması ile başlangıç düğümünden tüm düğümlere olan en kısa mesafeleri hesaplar

            1. tüm mesafeleri sonsuz olarak başlat
            2. başlangıç düğümünün mesafesini 0 yap
            3. öncelik kuyruğu (min-heap) kullanarak en kısa mesafeye sahip düğümü işle
            4. her komşu için daha kısa yol bulunursa güncelle
        """
        
        # 1. ADIM: mesafeleri ve önceki düğümleri başlat
        # tüm düğümler için mesafeyi sonsuz yap
        mesafeler = {node: float("inf") for node in self.adj}

        # tüm düğümler için önceki düğümü None yap
        oncekiler = {node: None for node in self.adj}

        # başlangıç düğümünün mesafesini 0 yap
        mesafeler[start] = 0

        # 2. ADIM: öncelik kuyruğu oluştur (min-heap)
        # (mesafe düğüm) çiftlerini içeren heap
        kuyruk = [(0, start)] # (mesafe, düğüm)

        # 3. ADIM: kuyruk boşalana kadar döngü
        while kuyruk:
            # heapten en küçük mesafeye sahip düğümü al (min-heap özelliği)
            mevcut_mesafe, u = heapq.heappop(kuyruk)

            # eğer bu düğüm için daha kısa bir yol zaten bulunduysa atla (heapte eski girişler olabilir)
            if mevcut_mesafe > mesafeler[u]:
                continue    # bu düğüm zaten daha iyi işlendi

            # 4. ADIM: u düğümünün tüm komşularını kontrol et
            for v, w in self.adj[u]:    # v: komşu, w: kenar ağırlığı
                # u üzerinden v'ye giden yeni yolun uzunluğunu hesapla
                yol = mesafeler[u] + w

                # eğer yeni yol daha kısaysa güncelle
                if yol < mesafeler[v]:
                    mesafeler[v] = yol # mesafeyi güncelle
                    oncekiler[v] = u # vye udan geldiğimizi kaydet

                    # vyi yeni mesafe ile kuyruğa ekle
                    heapq.heappush(kuyruk, (yol, v))

        # 5. ADIM: sonuçları döndür
        return mesafeler, oncekiler

    def en_kisa_yol(self, oncekiler, target):
        """
        oncekiler sözlüğünü kullanarak başlangıçtan hedefe olan en kısa yolu oluşturur

            1. hedef düğümden başla
            2. oncekiler zincirini takip ederek geriye git
            3. listeyi ters çevirerek ileri yönlü yolu elde et
        """

        rota = []   # yolu saklamak için boş liste

        # hedef düğümden başlayarak geriye doğru git
        while target is not None:
            rota.append(target)     # mevcut düğümü rotaya ekle
            target = oncekiler[target]      #bir önceki düğüme geç
        
        # rota şu an tersten [hedef, ..., başlangıç]
        # rers çevirerek başlangıç -> hedef haline getir

        return rota[::-1]   # [::-1] slice ile listeyi ters çevir
