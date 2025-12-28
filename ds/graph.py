import heapq

class Graph:
    def __init__(self):
        self.adj = {}

    def kenar_ekle(self, u, v, w):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append((v, w))
        self.adj[v].append((u, w))  # çift yönlü

    def dijkstra(self, start):
        mesafeler = {node: float("inf") for node in self.adj}
        oncekiler = {node: None for node in self.adj}

        mesafeler[start] = 0
        kuyruk = [(0, start)]

        while kuyruk:
            mevcut_mesafe, u = heapq.heappop(kuyruk)

            if mevcut_mesafe > mesafeler[u]:
                continue

            for v, w in self.adj[u]:
                yol = mesafeler[u] + w
                if yol < mesafeler[v]:
                    mesafeler[v] = yol
                    oncekiler[v] = u
                    heapq.heappush(kuyruk, (yol, v))

        return mesafeler, oncekiler

    def en_kisa_yol(self, oncekiler, target):
        rota = []
        while target is not None:
            rota.append(target)
            target = oncekiler[target]
        return rota[::-1]
