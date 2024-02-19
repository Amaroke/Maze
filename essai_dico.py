class UnionFind:
    def __init__(self, elements):
        self.dictionnaire = {}
        for element in elements:
            self.dictionnaire[element] = hash(element)

    def find(self, element):
        return self.dictionnaire[element]

    def find_friends(self, element):
        friends = []
        hash_elem = hash(element)
        for cle, valeur in self.dictionnaire.items():
            if valeur == hash_elem:
                friends.append(cle)
        return friends

    def little_union(self, hash_element1, elements):
        for element in elements:
            self.dictionnaire[element] = hash_element1

    def union(self, element1, element2):
        hashage_elem_1 = self.dictionnaire[element1]
        hashage_elem_2 = self.dictionnaire[element2]
        assert hashage_elem_2 != hashage_elem_1, "Les deux sont déjà unis."
        if hashage_elem_1 < hashage_elem_2:
            self.little_union(hashage_elem_1, self.find_friends(element2))
        else:
            self.dictionnaire[element1] = hashage_elem_2

    def number_of_classes(self):
        compteur = 0
        deja_vu = []
        for value in self.dictionnaire.values():
            if value not in deja_vu:
                compteur += 1
                deja_vu.append(value)
        return compteur

    def __repr__(self):
        return str(self.dictionnaire)


def test():
    """test all the methods"""

    elems = [1, 2, 3, 4]
    union_find = UnionFind(elems)

    assert union_find.number_of_classes() == 4

    union_find.union(1, 3)
    union_find.union(2, 4)

    assert union_find.find(1) == union_find.find(3)
    assert union_find.find(2) == union_find.find(4)
    assert union_find.find(1) != union_find.find(2)
    assert union_find.find(1) != union_find.find(4)

    assert union_find.number_of_classes() == 2

    union_find.union(3, 2)

    assert union_find.number_of_classes() == 1


if __name__ == "__main__":
    test()
