# Tamanho do alfabeto utilizado (ASCII)

SIGMA_SIZE = 2   
class _trieNode:
    def __init__(self, previous, substring="", value = None):
        self.children = [None] * SIGMA_SIZE   
        self.substring = substring
        self.previous = previous 
        
        self._value = value
        self._isLeaf = (value != None)

    def IsLeaf(self):
        return self._isLeaf

    def GetValue(self):
        return self._value

    def SetValue(self, value):
        self._value = value
        self._isLeaf = True if value is not None else False
        
    def SetSubstring(self, value):
        self.substring = value
        self._isLeaf = False
        
    def GetSubstring(self):
        return self.substring
    
class Trie:
    def __init__(self):
        self.root = _trieNode(None)
        self._nodeCount = 1
        self._depth = 1

    def Insert(self, key, value):
        currentNode = self.root
        
        i = 0
        bit = int(key[i])
        if currentNode.children[bit] is None:
            currentNode.children[bit] = _trieNode(currentNode, key, value)
            self._nodeCount += 1
            self._depth = max(self._depth, len(key) - i + 1)
            return (True, currentNode.GetSubstring(), key)              
        
        while i < len(key):                 
            child: _trieNode = currentNode.children[bit]
            substring = child.GetSubstring()
            lenSubstring = len(substring)
            
            for j in range(lenSubstring):
                prefixCurrentNode = ""
                sufixCurrentNode = ""
                sufixNewNode = ""
                
                # Se diferir, entro no if e faço as alterações                
                if i + j >= len(key) or key[i + j] != substring[j]:
                    # Prefixo acumulado até agora no nó atual
                    prefixCurrentNode += substring[:j]
                    
                    #Sufixo que sobrou no nó atual
                    sufixCurrentNode += substring[j:]
                    
                    #Sufixo do que sobrou da chave
                    sufixNewNode += key[i+j:]
                    
                    #Bit da chave que diferiu
                    breakbitKey = int(key[i + j])
                    breakbitSubstring = 0 if breakbitKey == 1 else 1
                    
    
                    currentNode.SetSubstring(prefixCurrentNode)
                    currentNode.children[breakbitKey] = _trieNode(currentNode, sufixNewNode, value)
                    currentNode.children[breakbitSubstring] = _trieNode(currentNode, sufixCurrentNode, currentNode.GetValue())
                    self._nodeCount += 1
                    self._depth += 1 
                    return (True, currentNode.GetSubstring(), key)             
                        
            i += lenSubstring
            bit = int(key[i]) if i < len(key) else None
            currentNode = child  
            if currentNode[bit] is None:
                currentNode.SetSubstring(substring + key[i:])
        
        return (True, currentNode.GetSubstring(), key)                
        

    def Search(self, key):
        currentNode = self.root
        
        i = 0
        bit = int(key[i])
        if currentNode.children[bit] is None:
                return None
            
        while i < len(key):                 
            child = currentNode.children[bit]
            substring = child.substring
            lenSubstring = len(substring)
            
            for j in range(lenSubstring):
                if i + j >= len(key) or key[i + j] != substring[j]:
                    breakbit = int(key[i + j])
                    
                    if currentNode.children[breakbit] is None:
                        return None  
                    
                    else:
                        child = currentNode.children[breakbit]
            
            i += lenSubstring
            bit = int(key[i])
            currentNode = child                       
        
        return currentNode.GetValue() if currentNode.IsLeaf() else None          
    
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
