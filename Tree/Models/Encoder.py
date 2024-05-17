from .Node import Node

from .HashFunc import HashFunc
import heapq
import string

class Encoder:
    
    """
    Encoder Class that creates a tree and hashes each node
    """
    
    def __init__(self, fileOrString:str, isFile:bool)->None:
        
        """
        Encoder.Constructor
        """
        
        if isFile:    
            self.file_path = fileOrString
            self.fileContent = self.readFile(fileOrString)
        else:
            self.sentence = fileOrString
            self.fileContent = self.readString(self.sentence)
        self.fileDict = self.parseFreq(self.fileContent)
        self.nodeList = self.makeNodes()
        self.makeTree()
        self.printTree(self.nodeList[0])
        
    def getFinalHash(self)->str:
        
        """
        Encoder.getFinalHash
        """
        
        return self.nodeList[0].hashValue


    def hash(self, input_data:str, rounds=10)->str:
        
        """
        Encoder.hash
        """
        
        return HashFunc.custom_hash(input_data, rounds)

    def makeTree(self):
        
        """
        Encoder.makeTree
        """
                
        while len(self.nodeList) > 1:
            nodeL = heapq.heappop(self.nodeList)
            nodeR = heapq.heappop(self.nodeList)
            tempNode = Node(nodeL.freq+nodeR.freq, f"Temp Node")
            tempNode.leftChild = nodeL
            tempNode.rightChild = nodeR
            tempNode.setWordHash(self.hash, newWord=f"{nodeL.hashValue}{nodeR.hashValue}")
            heapq.heappush(self.nodeList, tempNode)
        

    def makeNodes(self)->list[Node]:
        
        """
        Encoder.makeNodes
        """        
        
        nodeList = []
        for word in self.fileDict.keys():
            tempNode = Node(self.fileDict[word], word)
            tempNode.setWordHash(self.hash)
            heapq.heappush(nodeList, tempNode)
        return nodeList
        

    def readString(self, sentence:str)->str:
        
        """
        Encoder.readString
        """
        
        translator = str.maketrans('', '', string.punctuation)
        return (sentence).translate(translator)
    

    def readFile(self, filePath:str)->str:
        
        """
        Encoder.readFile
        """
        
        translator = str.maketrans('', '', string.punctuation)
        with open(filePath, 'r') as file:
            return (file.read()).translate(translator)
            

    def parseFreq(self, fileContent:str)->dict:
        
        """
        Encoder.parseFreq
        """
        
        freqDict: dict = {}
        data:list[str] = fileContent.split(" ")
        for word in data:
            if word in freqDict:
                freqDict[word] += 1
            else:
                freqDict[word] = 1
            
        return freqDict
        

    def printNodes(self)->None:
        
        """
        Encoder.printNodes
        """
        
        for i in range(len(self.nodeList)):
            print(self.nodeList[i])


    def printTree(self, node:Node)->None:
        
        """
        Encoder.printTree
        """
        
        if node.leftChild == None and node.rightChild == None:
            print(node)
            return
        if node.leftChild != None:
            self.printTree(node.leftChild)
        print(node)
        if node.rightChild != None:
            self.printTree(node.rightChild)
            
            
    def getHashFunction(self):
        
        """
        Encoder.getHashFunction
        """
        
        return hash
    
    def getOriginalData(self)->str:
        
        """
        Encoder.getOriginalHash
        """
        
        return self.fileContent