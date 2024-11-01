class Trie:
    def __init__(self):
        self.root = _trieNode(None, None, None)

    def Insert(self, data):
        pass

    def Search(self, data):
        return True

    def Remove(self, data):
        pass

class _trieNode:
    def __init__(self, left, right, top):
        self.left = left
        self.right = right
        self.top = top

        self.value = None
        self.isLeaf = False

    def IsLeaf(self):
        return self.isLeaf

    def GetValue(self):
        return self.value

    def SetValue(self, value):
        self.value = value
        self.isLeaf = True