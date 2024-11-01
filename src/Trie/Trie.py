# Tamanho do alfabeto utilizado (ASCII)
SIGMA_SIZE = 127

class Trie:
    def __init__(self):
        self.root = _trieNode(None)

    def Insert(self, key, value):
        pass

    def Search(self, key):
        pass

    def Remove(self, key):
        pass

    def __getitem__(self, key):
        return self.Search(key)

    def __setitem__(self, key, value):
        self.Insert(key, value)
        
class _trieNode:
    def __init__(self, previous, value = None):
        self.children = [None] * SIGMA_SIZE
        self.previous = previous

        self._value = value
        self._isLeaf = (value != None)

    def IsLeaf(self):
        return self.isLeaf

    def GetValue(self):
        return self.value

    def SetValue(self, value):
        self.value = value
        self.isLeaf = True