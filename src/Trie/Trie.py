SIGMA_SIZE = 2
IS_WORD_FULL = "$"

class _trieNode:
    def __init__(self, previous, substring="", value=None):
        self.children = [None] * (SIGMA_SIZE + 1)
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

    def Insert(self, key, value, detailed_return=False):
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
            return (currentNode.GetSubstring(), currentNode.GetValue()) if not detailed_return else (key, key, None, value)

        while i < len(key):
            childNode = currentNode.children[bit]
            substring = childNode.GetSubstring()
            lenSubstring = len(substring)

            for j in range(lenSubstring):
                if i + j >= len(key) or key[i + j] != substring[j]:
                    prefixMatch = substring[:j]
                    suffixExisting = substring[j:]
                    suffixNew = key[i + j:]

                    breakbitKey = int(key[i + j])
                    breakbitSubstring = 0 if breakbitKey == 1 else 1

                    child_2_reference = childNode.children[2]
                    oldChildren = childNode.children                    
                    childNode.SetSubstring(prefixMatch)
                    childNode.children = [None] * SIGMA_SIZE

                    newChildExisting = _trieNode(childNode, suffixExisting, childNode.GetValue())
                    newChildExisting.children = oldChildren  
                    childNode.children[breakbitSubstring] = newChildExisting

                    if child_2_reference is not None:
                        newChildExisting.children[2] = child_2_reference

                    newChildNode = _trieNode(childNode, suffixNew, value)
                    childNode.children[breakbitKey] = newChildNode
                    childNode.SetValue(None)

                    insertionDepth += 1
                    self._nodeCount += 2
                    self._depth = max(self._depth, insertionDepth)

                    return (key, value) if not detailed_return else (key, suffixNew, suffixExisting, newChildNode.GetValue())

            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            if bit is not None and childNode.children[bit] is None and childNode.IsLeaf():
                newChildNode = _trieNode(currentNode, IS_WORD_FULL, childNode.GetValue())
                childNode.children[2] = newChildNode
                childNode.children[bit] = _trieNode(currentNode, key[i:], value)
                currentNode: _trieNode = childNode.children[bit]

                return (key, value) if not detailed_return else (key, IS_WORD_FULL, currentNode.GetSubstring(), currentNode.GetValue())
            
            currentNode = childNode

        return (key, value) if not detailed_return else (key, currentNode.GetSubstring(), None, value)


    def Search(self, key, detailed_return=False):
        if not key:
            raise ValueError("A chave não pode ser vazia")
        
        currentNode = self.root
        i = 0
        bit = int(key[i])
        if currentNode.children[bit] is None:
            return False

        searchkey = ""
        while i < len(key):
            child = currentNode.children[bit]

            if child is None:
                return False
            
            substring = child.GetSubstring()
            lenSubstring = len(substring)

            for j in range(lenSubstring):
                if i + j >= len(key):
                    return (searchkey, substring) if detailed_return else True
                    
                if key[i + j] != substring[j]:
                    return False
                
                searchkey += substring[j]
            
            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            if not currentNode.IsLeaf():
                currentNode = child
            else:
                return None

        if currentNode.children[2] is None:
            suffix = currentNode.GetSubstring()
        else:
            currentNode = currentNode.children[2]
            suffix = currentNode.GetSubstring()
        
        return (searchkey, suffix) if detailed_return else True

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
