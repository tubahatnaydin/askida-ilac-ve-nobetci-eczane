"""
TRIE (PREFIX AĞACI) VERİ YAPISI
bu modül ilaç isimlerinde hızlı prefix araması yapmak için kullanılır
kullanıcı ilacın ilk harflerini girdiğinde o harflerle başlayan ilaçları önerir
"""

class TrieNode:     # Trie ağacının düğüm sınıfı

    def __init__(self):
        # yeni bir Trie düğümü oluşturur
        self.children = {}      # çocuk düğümler: {harf: TrieNode}
        self.kelime_sonu = False    # kelime burada bitiyor mu???

class Trie:     # Trie (prefix ağacı) sınıfı

    def __init__(self):
        # boş bir Trie ağacı oluşturur
        self.root = TrieNode()      # kök düğüm (boş string)

    def insert(self, word: str) -> None:
        """
        Trie ağacına yeni bir kelime ekler
        
            1. kök düğümden başla
            2. kelimenin her harfi için:
                --> harf çocuklarda yoksa yeni düğüm oluştur
                --> ilgili çocuk düğüme geç
            3. son harfte kelime_sonu bayrağını True yap
        """

        node = self.root    # kök düğümden başla

        # kelimenin her karakteri (harf) için
        for ch in word.lower():     # küçük harfe çevir

            # eğer bu harf mevcut düğümün çocuklarında yoksa
            if ch not in node.children:
                # yeni bir TrieNode oluştur ve çocuklara ekle
                node.children[ch] = TrieNode()

            # bir sonraki düğüme geç (bu harfe karşılık gelen düğüm)
            node = node.children[ch]
        
        # klimenin sonuna geldik bu düğümü "kelime sonu" olarak işaretle
        node.kelime_sonu = True

    def prefix_ara(self, prefix: str, limit: int = 5):
        """
        verilen prefix ile başlayan tüm kelimeleri bulur

            1. prefixin karakterlerini takip ederek ilgili düğüme git
            2. o düğümden DFS ile tüm kelimeleri topla
            3. limit sayısına ulaşınca dur
        """
        
        node = self.root    # kök düğümden başla

        # 1. ADIM: prefixi Trie'de takip et
        for ch in prefix.lower():   # küçük harfe çevir
            # eğer bu harf mevcut düğümün çocuklarında YOKSA
            if ch not in node.children:
                return []   # prefix ile başlayan kelime YOK
            
            # harf varsa ilgili çocuk düğüme geç
            node = node.children[ch]

        # 2. ADIM: bu noktada node prefixin bittiği düğüm
        # ÖR: prefix = "par" ise "par"ın 'r' düğümünde
        sonuclar = []   # bulunan kelimeleri sakla

        def dfs(suanki_node, yol_ch):
            """
            Depth-First Search (DFS) ile tüm kelimeleri bul
            
                1. eğer mevcut düğüm kelime sonu ise kelimeyi sonuçlara ekle
                2. tüm çocuk düğümlere recursive olarak git
                3. limit dolunca dur
            """
            
            # LIMIT KONTROLÜ: istenen sayıda kelime bulunduysa DUR
            if len(sonuclar) >= limit:
                return
            
            # 1. DURUM: bu düğüm bir KELİME SONU ise
            if suanki_node.kelime_sonu:
                # kelimeyi oluştur: prefix + yol_ch (harf listesi)
                sonuclar.append(prefix + "".join(yol_ch))   #sonuç listesine ekle

            # 2. DURUM: tüm çocuk düğümlere git (alfabetik sırada)
            # sorted() ile alfabetik sırala (kullanıcıya düzenli öneri sunmak için)
            for nxt in sorted(suanki_node.children.keys()):
                # recursive DFS: çocuk düğüme git harfi yola ekle
                dfs(suanki_node.children[nxt], yol_ch + [nxt])

        # 3. ADIM: DFS başlat (mevcut düğümden başla, boş yol listesi)
        dfs(node, [])

        # 4. ADIM: sonuçları döndür
        return sonuclar
