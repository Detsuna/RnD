class Node() : 
    def __init__(self, parent=None, selfInParent=None) : 
        self.hasValue = False
        self.value = None
        self.children = None
        self.parent = parent
        self.selfInParent = selfInParent

    @property
    def Key(self) : 
        node = self
        key = []
        while node.selfInParent is not None : 
            key.append(node.selfInParent)
            node = node.parent
        key = reversed(key)
        return key

    def _Representation(self) : 
        here = {}
        if self.hasValue : 
            here["value"] = self.value
        for i, child in enumerate(self.children) : 
            if child is None : pass
            else : here[str(i)] = child._Representation()
        #info = inspect.stack(0)[0]
        return here

    def __repr__(self) : return str(self._Representation())

class NodeIterator() :
    def __init__(self, node) : 
        self.node = node
        found = False
        while not found : 
            children = [child for child in self.node.children if child is not None]
            if any(children) :
                self.node = children[0]
            elif self.node.hasValue is False : raise StopIteration('empty tree')
            else : found = True
    def __iter__(self) : return self
    def __next__(self) : 
        if self.node is None : raise StopIteration
        r = self.node

        found = False
        down = False
        while not found : 
            if self.node.parent is None :
                if self.node is r or not self.node.hasValue: self.node = None
                found = True
            elif down is False : 
                n = None
                for i in range(self.node.selfInParent + 1, len(self.node.children)) : 
                    n = self.node.parent.children[i]
                    if n is not None : break
                if n is None :
                    self.node = self.node.parent
                    if self.node.hasValue : found = True
                else : 
                    self.node = n
                    down = True
            else : 
                children = [child for child in self.node.children if child is not None]
                if any(children) : self.node = children[0]
                else : found = True
        return r
        

class Tree(Node) : 
    def __init__(self, *a, **k) : 
        super().__init__(*a, **k)
        self.count = 0
    def __iter__(self) : return NodeIterator(self)
        
    def _Find(self, key = [], withCreate=False) : 
        node = self
        for seg in reversed(key) : 
            if node.children[seg] is not None : node = node.children[seg]
            elif withCreate is True : 
                node.children[seg] = Node(parent=node, selfInParent=seg)
                node.children[seg].children = [None] * len(self.children)
                node = node.children[seg]
            else : 
                node = None
                break
        return node
    def __getitem__(self, key) : 
        node = self._Find(key)
        if node is None or node.hasValue is False : self.__missing__(key)
        return node.value
    def __setitem__(self, key, value) : 
        node = self._Find(key, withCreate=True)
        node.hasValue = True                
        node.value = value
        self.count = self.count + 1
    def __delitem__(self, key) : 
        node = self._Find(key)
        if node is not None and node.hasValue is True : self.count = self.count -1
        node.hasValue = False
        node.value = None

        parent = None
        while not any([True for child in node.children if child is not None]) : 
            if node.parent is not None :
                parent = node.parent
                parent.children[node.selfInParent] = None                
                node.parent = None
                node.selfInParent = None
                node = parent

    def __missing__(self, key) : raise KeyError(key)
    def __contains__(self, key) : 
        try :
            self.__getitem__(key)
            return True
        except KeyError as e : return False

class ByteTree(Tree) : 
    def __init__(self, *a, **k) : 
        super().__init__(*a, **k)
        self.children = [None] * 256
    def _Find(self, key, withCreate=False) : 
        if not isinstance(key, (bytes, bytearray)) : raise TypeError(f'expected bytes-like object, not {type(key).__name__}')
        return super()._Find(key=key, withCreate=withCreate)

class StringTree(ByteTree) : 
    def _Find(self, key, withCreate=False) : 
        if not isinstance(key, str) : raise TypeError(f'expected string, not {type(key).__name__}')
        return super()._Find(key=bytearray(key, 'UTF-8'), withCreate=withCreate)

class MetricTree(Tree) : 
    def __init__(self, *a, **k) : 
        super().__init__(*a, **k)
        self.children = [None] * 10
    def _Find(self, key, withCreate=False) : 
        if not isinstance(key, (int)) : raise TypeError()
        converted = [int(i) for i in str(key)]
        return super()._Find(key=converted, withCreate=withCreate)


class Page() : pass

class Cover(Page) : pass


class Table() : pass


class Connection() :
    def __init__(self, file) : 
        self.file = file
        self.handle = None
    def Open(self) : 
        if self.handle is None : 
            self.handle = open(self.file)
    def Close() : pass
    def __enter__(self):
        self.Open()
        return self      
    def __exit__(self, exc_type, exc_value, exc_traceback) : 
        self.Close()

class Transaction() : pass

class Command() : pass # CRUD/SIUD, create table

