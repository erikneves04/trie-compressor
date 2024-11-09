# Tamanho do alfabeto utilizado (ASCII)
SIGMA_SIZE = 127 # Avaliar se está correto, pode ser alterado em breve para 2 (alfabeto binário)

class Trie:
    def __init__(self):
        self.root = _trieNode(None)
        self._nodeCount = 0
        self._depth = 1

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

    def GetNodeCount(self):
        return self._nodeCount
    
    def GetDepth(self):
        return self._depth
        
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