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
    def __init__(self, detailedReturn = False):
        self.root = _trieNode(None)
        self._nodeCount = 1
        self._depth = 1
        self.detailedReturn = detailedReturn  
        
    def GetDetailedReturn(self):
        return self.detailedReturn

    def Insert(self, key, value):
        if not key:
            raise ValueError("The key cannot be empty")
        
        if not isinstance(value, int):
            raise ValueError("The value must be an integer.")
        
        if value < 0:
            raise ValueError("The value cannot be negative.")
        
        detailedReturn = self.GetDetailedReturn()
        
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
            return (currentNode.GetSubstring(), currentNode.GetValue()) if not detailedReturn else (key, key, None, value)

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

                    extraReference  = childNode.children[SIGMA_SIZE]
                    oldChildren = childNode.children                    
                    childNode.SetSubstring(prefixMatch)
                    childNode.children = [None] * (SIGMA_SIZE + 1)

                    newChildExisting = _trieNode(childNode, suffixExisting, childNode.GetValue())
                    newChildExisting.children = oldChildren  
                    childNode.children[breakbitSubstring] = newChildExisting

                    if extraReference  is not None:
                        newChildExisting.children[SIGMA_SIZE] = extraReference 

                    newChildNode = _trieNode(childNode, suffixNew, value)
                    childNode.children[breakbitKey] = newChildNode
                    childNode.SetValue(None)

                    insertionDepth += 1
                    self._nodeCount += 2
                    self._depth = max(self._depth, insertionDepth)

                    return (key, value) if not detailedReturn else (key, suffixNew, suffixExisting, newChildNode.GetValue())

            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            if bit is not None and childNode.children[bit] is None and childNode.IsLeaf():
                newChildNode = _trieNode(currentNode, IS_WORD_FULL, childNode.GetValue())
                childNode.children[2] = newChildNode
                childNode.children[bit] = _trieNode(currentNode, key[i:], value)
                currentNode: _trieNode = childNode.children[bit]

                return (key, value) if not detailedReturn else (key, IS_WORD_FULL, currentNode.GetSubstring(), currentNode.GetValue())
            
            currentNode = childNode

        return (key, value) if not detailedReturn else (key, currentNode.GetSubstring(), None, value)

    def Search(self, key):
        if not key:
            raise ValueError("The key cannot be empty")
        
        detailedReturn = self.GetDetailedReturn()
        
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
                if i + j >= len(key) or key[i + j] != substring[j]:
                    return False
                
                searchkey += substring[j]
            
            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            if not currentNode.IsLeaf():
                currentNode = child
            else:
                return None

        if currentNode.children[SIGMA_SIZE] is None:
            suffix = currentNode.GetSubstring()
        else:
            currentNode = currentNode.children[2]
            suffix = currentNode.GetSubstring()
        
        return (searchkey, suffix) if detailedReturn else True

    def ContainsKey(self, key):
        return self.Search(key) != None

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
