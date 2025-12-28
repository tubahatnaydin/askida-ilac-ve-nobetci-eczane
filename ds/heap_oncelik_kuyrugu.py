import heapq
import time

class PriorityQueue:

    # max-heap davranışı için önceliği negatif basarak heapq (min-heap) kullanır
    # eşit önceliklerde FIFO gibi davranması için zaman damgası eklendi

    def __init__(self):
        self._yigin = []

    def push(self, istek: dict) -> None:
        # heapq min-heap olduğu için en yüksek önceliği üste almak adına eksi kullanıyoruz
        # priority kullanıyoruz
        heapq.heappush(self._yigin, (-istek["oncelik"], time.time(), istek))

    def pop(self):
        if not self._yigin:
            return None
        return heapq.heappop(self._yigin)[2]

    def peek(self):
        if not self._yigin:
            return None
        return self._yigin[0][2]

    def bos_mu(self) -> bool:
        return len(self._yigin) == 0

    def __len__(self) -> int:
        return len(self._yigin)
    
