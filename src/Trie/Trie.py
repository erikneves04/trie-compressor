SIGMA_SIZE = 3
IS_WORD_FULL = "$"

class _trieNode:
    def __init__(self, previous, substring="", value=None):
        self.children = [None] * SIGMA_SIZE
        self.substring = substring
        self.previous = previous
        self._value = value
        self._isLeaf = (value is not None)

    def IsLeaf(self):
        return self._isLeaf

    def GetValue(self):
        return self._value

    def SetValue(self, value):
        self._value = value
        self._isLeaf = True if value is not None else False

    def SetSubstring(self, value):
        self.substring = value
        self._isLeaf = False if value is None else True

    def GetSubstring(self):
        return self.substring

class Trie:
    def __init__(self):
        self.root = _trieNode(None)
        self._nodeCount = 1
        self._depth = 1

    def Insert(self, key, value):
        if not key:
            raise ValueError("A chave não pode ser vazia")
        
        if not isinstance(value, int) or value <= 0:
            raise ValueError("O valor deve ser um inteiro maior que zero")
        
        currentNode = self.root
        insertionDepth = 0
        
        i = 0
        bit = int(key[i])

        if currentNode.children[bit] is None:
            currentNode.children[bit] = _trieNode(currentNode, key, value)
            currentNode = currentNode.children[bit]
            insertionDepth += 1
            self._nodeCount += 1
            self._depth = max(self._depth, insertionDepth)
            return (key, key, None)

        while i < len(key):
            childNode = currentNode.children[bit]
            substring = childNode.GetSubstring()
            lenSubstring = len(substring)

            for j in range(lenSubstring):
                if i + j >= len(key) or key[i + j] != substring[j]:
                    prefixMatch = substring[:j]
                    suffixExisting = substring[j:]
                    suffixNew = key[i+j:]
                    
                    breakbitKey = int(key[i + j])
                    breakbitSubstring = 0 if breakbitKey == 1 else 1
                    
                    oldChildren = childNode.children
                    childNode.SetSubstring(prefixMatch)
                    childNode.children = [None] * SIGMA_SIZE
                    
                    newChildExisting = _trieNode(childNode, suffixExisting, childNode.GetValue())
                    newChildExisting.children = oldChildren  
                    childNode.children[breakbitSubstring] = newChildExisting
                    
                    childNode.children[breakbitKey] = _trieNode(childNode, suffixNew, value)
                    childNode.SetValue(None)
                    
                    insertionDepth += 1
                    self._nodeCount += 2
                    self._depth = max(self._depth, insertionDepth)
                    
                    return (key, suffixNew, suffixExisting)

            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            if bit is not None and childNode.children[bit] is None and childNode.IsLeaf():
                childNode.children[2] = _trieNode(currentNode, IS_WORD_FULL, childNode.GetValue())
                childNode.children[bit] = _trieNode(currentNode, key[:i], value)
                currentNode = childNode
                currentNode.SetValue(None)
                
                return (key, IS_WORD_FULL, key[i:])
            
            currentNode = childNode

        return (key, currentNode.GetSubstring(), None)

    def Search(self, key):
        if not key:
            raise ValueError("A chave não pode ser vazia")
        
        currentNode = self.root

        i = 0
        bit = int(key[i])
        if currentNode.children[bit] is None:
            return None

        while i < len(key):
            child = currentNode.children[bit]
            prefix = ""
            substring = child.substring
            lenSubstring = len(substring)
            prefix += substring

            for j in range(lenSubstring):
                if i + j >= len(key) or key[i + j] != substring[j]:
                    breakbit = int(key[i + j])
                    
                    if currentNode.children[breakbit] is None:
                        return None
                    else:
                        child = currentNode.children[breakbit]

            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            currentNode = child

        result = currentNode.GetValue() if currentNode.IsLeaf() else None
        sufix = currentNode.GetSubstring()
        return (prefix, sufix, result)

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
