from .Node import Node

import hashlib
import heapq
import string

class Encoder:
    def __init__(self, fileOrString:str, isFile:bool)->None:
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
        
    def hash(self, word:str)->str:
        return (hashlib.sha256(word.encode('utf-8'))).hexdigest()
    
    def makeTree(self):
        while len(self.nodeList) > 1:
            nodeL = heapq.heappop(self.nodeList)
            nodeR = heapq.heappop(self.nodeList)
            tempNode = Node(nodeL.freq+nodeR.freq, "Temp Node")
            tempNode.leftChild = nodeL
            tempNode.rightChild = nodeR
            tempNode.setWordHash(self.hash, newWord=f"{nodeL.hashValue}{nodeR.hashValue}")
            heapq.heappush(self.nodeList, tempNode)
        
    def makeNodes(self)->list[Node]:
        nodeList = []
        for word in self.fileDict.keys():
            tempNode = Node(self.fileDict[word], word)
            tempNode.setWordHash(self.hash)
            heapq.heappush(nodeList, tempNode)
        return nodeList
        
    def readString(self, sentence:str)->str:
        translator = str.maketrans('', '', string.punctuation)
        return (sentence).translate(translator)
    
    def readFile(self, filePath:str)->str:
        translator = str.maketrans('', '', string.punctuation)
        with open(filePath, 'r') as file:
            return (file.read()).translate(translator)
            
    def parseFreq(self, fileContent:str)->dict:
        freqDict: dict = {}
        data:list[str] = fileContent.split(" ")
        for word in data:
            if word in freqDict:
                freqDict[word] += 1
            else:
                freqDict[word] = 1
            
        return freqDict
        
    def printNodes(self)->None:
        for i in range(len(self.nodeList)):
            print(self.nodeList[i])

    def printTree(self, node:Node)->None:
        if node.leftChild == None and node.rightChild == None:
            print(node)
            return
        if node.leftChild != None:
            self.printTree(node.leftChild)
        print(node)
        if node.rightChild != None:
            self.printTree(node.rightChild)