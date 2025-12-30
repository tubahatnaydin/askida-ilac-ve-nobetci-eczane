"""
ÖNCELİK KUYRUĞU  -  MAX-HEAP DAVRANIŞI
Bu modül hasta taleplerini öncelik puanına göre sıralamak için kullanılır
pythonun heapq (min-heap) modülünü kullanarak max-heap davranışı simüle eder
"""

import heapq    # min-heap implementasyonu için
import time     # FIFO davranışı için zaman damgası eklemek amacıyla

class PriorityQueue:
    """
     ax-heap davranışı gösteren öncelik kuyruğu
    
    pythonun heapq modülü min-heaptir, max-heap elde etmek için:
    1. öncelik değerlerini negatif yaparız (-priority)
    2. böylece en yüksek öncelik en küçük negatif sayı olur
    3. heapq.min-heap'i bu sayede max-heap gibi kullanırız
    
    ayrıca aynı önceliğe sahip öğeler için FIFO davranışı sağlamak amacıyla
    zaman damgası (timestamp) eklenmiştir
    """

    def __init__(self):
        """
        boş bir öncelik kuyruğu oluşturur
        
        self._yigin: heapq ile yönetilen liste
                     her öğe: (-öncelik, zaman_damgası, veri) üçlüsüdür
        """

        self._yigin = []    # heapq ile yönetilecek liste

    def push(self, istek: dict) -> None:
        """
        kuyruğa yeni bir hasta talebi ekler
        
            1. önceliği negatif yap (max-heap için)
            2. zaman damgası ekle (FIFO için)
            3. heapq.heappush ile min-heap'e ekle
        """
        
        # mxx-heap davranışı için önceliği negatif yapıyoruz
        # heapq min-heap olduğundan en büyük öncelik en küçük negatif sayı olur
        # zaman damgası ekleyerek aynı öncelikte FIFO davranışı sağlıyoruz

        heapq.heappush(self._yigin, (-istek["oncelik"], time.time(), istek) 
        # (-öncelik, zaman, veri) 
        )

    def pop(self):
        """
        kuyruktan en yüksek öncelikli öğeyi çıkarır ve döndürür

            1. heapq.heappop ile en küçük (-öncelik) değerini al
            2. üçüncü elemanı döndür
        """

        # kuyruk boşsa None döndür
        if not self._yigin:
            return None
        
        # heapten en küçük (-öncelik) değerini çıkar
        # [2] ile sadece istek verisini döndür (öncelik ve zamanı at)
        return heapq.heappop(self._yigin)[2]

    def peek(self):
        
        # kuyruğun en üstündeki öğeyi görüntüler ama çıkarmaz
        
        # kuyruk boşsa None döndür
        if not self._yigin:
            return None
        
        # heapin ilk elemanının [2] indexini döndür 
        return self._yigin[0][2]

    def bos_mu(self) -> bool:
        # kuyruğun boş olup olmadığını kontrol eder

        return len(self._yigin) == 0

    def __len__(self) -> int:
        # kuyruktaki öğe sayısını döndürür

        return len(self._yigin)
    