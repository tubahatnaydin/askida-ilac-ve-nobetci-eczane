import heapq

class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v, w):
        if u not in self.adj:
            self.adj[u] = []
        if v not in self.adj:
            self.adj[v] = []

        self.adj[u].append((v, w))
        self.adj[v].append((u, w))  # çift yönlü

    def dijkstra(self, start):
        dist = {node: float("inf") for node in self.adj}
        prev = {node: None for node in self.adj}

        dist[start] = 0
        pq = [(0, start)]

        while pq:
            cur_dist, u = heapq.heappop(pq)

            if cur_dist > dist[u]:
                continue

            for v, w in self.adj[u]:
                alt = dist[u] + w
                if alt < dist[v]:
                    dist[v] = alt
                    prev[v] = u
                    heapq.heappush(pq, (alt, v))

        return dist, prev

    def shortest_path(self, prev, target):
        path = []
        while target is not None:
            path.append(target)
            target = prev[target]
        return path[::-1]
