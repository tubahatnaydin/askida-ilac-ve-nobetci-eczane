"""
STACK (YIĞIN) VERİ YAPISI - LIFO (last in first out)
bu modül geri alma (undo) işlemleri için kullanılır
son yapılan bağışı ilk olarak geri almak için
"""

class Stack:
    """
    push(eleman): stacke öğe ekle
    pop(): stackten öğe çıkar
    peek(): üstteki öğeyi görüntüle (çıkarma)
    bos_mu(): stack boş mu kontrol et
    __len__(): stack boyutunu döndür
    """
      
    def __init__(self):
        # boş bir stack oluşturur
        self.elemanlar = []     # öğeleri saklamak için boş liste

    def push(self, eleman):
        """
        stackin üstüne yeni öğe ekler (push)
        listeye eleman ekler (sonuna)
        """
        self.elemanlar.append(eleman)   # liste sonuna ekle

    def pop(self):
        """
        stackin üstündeki öğeyi çıkarır ve döndürür (pop)
        listenin son elemanını çıkarır ve döndürür
        """
        # stack boş mu kontrol et
        if self.bos_mu():
            return None     # boşsa None döndür
        
        # listenin son elemanını çıkar ve döndür
        return self.elemanlar.pop()

    def peek(self): 
        # stackin üstündeki öğeyi görüntüler ama ÇIKARMAZ
        
        # stack boş mu kontrol et
        if self.bos_mu():
            return None     # boşsa None döndür
        
        # listenin son elemanını döndür (silmek yok)
        return self.elemanlar[-1]   # son elemana eriş

    def bos_mu(self):   # stackin boş olup olmadığını kontrol eder
        return len(self.elemanlar) == 0

    def __len__(self):
        """
        stackteki öğe sayısını döndürür
        len(stack_nesnesi) şeklinde kullanılabilir
        """
        return len(self.elemanlar)
    