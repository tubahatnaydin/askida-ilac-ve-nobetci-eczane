class TrieNode:
    def __init__(self):
        self.children = {}
        self.kelime_sonu = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word.lower():
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.kelime_sonu = True

    def prefix_ara(self, prefix: str, limit: int = 5):
        
        # prefix'e göre en fazla -liimt- tane öneri döndürür
        
        node = self.root
        for ch in prefix.lower():
            if ch not in node.children:
                return []
            node = node.children[ch]

        sonuclar = []

        def dfs(suanki_node, yol_ch):
            if len(sonuclar) >= limit:
                return
            if suanki_node.kelime_sonu:
                sonuclar.append(prefix + "".join(yol_ch))
            for nxt in sorted(suanki_node.children.keys()):
                dfs(suanki_node.children[nxt], yol_ch + [nxt])

        dfs(node, [])
        return sonuclar
