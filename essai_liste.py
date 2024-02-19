class UnionFind:
    def __init__(self, elements):
        self.liste = elements

    def find(self, element):
        return self.liste.index(element)

    def union(self, element1, element2):
        indice1 = self.liste.index(element1)
        indice2 = self.liste.index(element2)
        if indice1<indice2:
            

    def number_of_classes(self):
        return len(self.liste)
