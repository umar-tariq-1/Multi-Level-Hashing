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
        # self.printTree(self.nodeList[0])
        

    def create_hex(self, data:str)->str:
        data_bytes = bytes(data, 'utf-8')
        hex_result = []
        for i in range(0, len(data_bytes), 16):
            chunk = data_bytes[i:i+16]
            hex_result.append(chunk.hex())
        last_chunk = hex_result[-1]
        last_chunk = last_chunk.ljust(32, 'f')
        hex_result[-1] = last_chunk
        if len(hex_result) == 1:
            xor_result = int(hex_result[0], 16) ^ int(data_bytes.hex(), 16)
        else:
            xor_result = int(hex_result[0], 16)
            for i in range(1, len(hex_result)):
                xor_result ^= int(hex_result[i], 16)
        final_hex = hex(xor_result)[2:].zfill(32)
        return final_hex


    def round_function(self, data:str, key:str)->str:
        hash_input = data + key
        hash_output = self.create_hex(hash_input)
        truncated_hash_output=hash_output
        return truncated_hash_output


    def hash(self, input_data:str, rounds=10)->str:
        if len(input_data) % 2 != 0:
            input_data += '\0'  # Pad with null character if needed
        compressed_input=self.create_hex(input_data)
        half_length = len(compressed_input) // 2
        left_part = compressed_input[:half_length]
        right_part = compressed_input[half_length:]

        left_binary = ''.join(format(ord(char), '08b') for char in left_part)
        right_binary = ''.join(format(ord(char), '08b') for char in right_part)

        for _ in range(rounds):
            original_right = right_binary

            round_output = self.round_function(right_binary, left_binary)

            right_binary = '{0:0{1}b}'.format(int(round_output, 16) ^ int(left_binary, 2), len(right_binary))

            left_binary = '{0:0{1}b}'.format(int(left_binary, 2) ^ int(original_right, 2), len(left_binary))

        output_hash = left_binary + right_binary

        return '{0:0{1}x}'.format(int(output_hash, 2), len(output_hash) // 4)


    def getHashFunction(self):
        return hash


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
            
    def getOriginalData(self)->str:
        return self.fileContent

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


    def getFinalHash(self)->str:
        return (self.nodeList[0].hashValue)