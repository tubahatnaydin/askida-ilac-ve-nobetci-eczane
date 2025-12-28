class Stack:
    def __init__(self):
        self.elemanlar = []

    def push(self, eleman):
        self.elemanlar.append(eleman)

    def pop(self):
        if self.bos_mu():
            return None
        return self.elemanlar.pop()

    def peek(self):
        if self.bos_mu():
            return None
        return self.elemanlar[-1]

    def bos_mu(self):
        return len(self.elemanlar) == 0

    def __len__(self):
        return len(self.elemanlar)
