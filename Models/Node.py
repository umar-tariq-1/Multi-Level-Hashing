class Node:
    def __init__ (self, frequency:int, word:str)->None:
        self.freq = frequency
        self.word = word
        self.leftChild = None
        self.rightChild = None
        self.hashValue = ""

    def setWordHash(self, hashFunction, newWord = '')->None:
        self.hashValue = hashFunction(newWord if newWord != '' else self.word)

    def setNodeRight(self, rightChild)->None:
        self.rightChild = rightChild
    def setNodeLeft(self, leftChild)->None:
        self.leftChild = leftChild
        
    def __str__(self) -> tuple[str]:
        return f"({self.word}, {self.freq}, {self.hashValue})"
    def __repr__(self) -> tuple[str]:
        return f"({self.word}, {self.freq}, {self.hashValue})"
    
    def __lt__(self, node2)->bool:
        return self.freq < node2.freq