# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 16:10:54 2015

@author: Robert Parrillo, Juan David Dominguez, Michael Gofron
"""
import csv
import random
import math
import itertools
from copy import deepcopy

sampleSize = 100
sampleSizeProp = float(4)/3
dataInputs = 50000
totalAttributes = 13
klimit = 5
lenData = 0
prePruneThresh = 0.0003
gainThresh = 0.005
lenData = 0
numericTypes = ["numeric","numeric","nominal","numeric","numeric",
"numeric","nominal","nominal","numeric","numeric","nominal",
"numeric","numeric","binary"]
listName = ['winpercent', ' oppwinpercent', ' weather', ' temperature', ' numinjured',
' oppnuminjured', ' startingpitcher', ' oppstartingpitcher',
' dayssincegame', ' oppdayssincegame', ' homeaway', ' rundifferential', ' opprundifferential', ' winner']
listOfPaths = []

def init(fileName):
    """Takes in a data file name that has the exact same format as that
    in the hw and modifies it so that we can use it to create a tree"""
    global lenData, listName, totalAttributes
    data = []
    with open(fileName, 'rb') as f:
        reader = csv.reader(f)
        data = list(reader)
    listName = data.pop(0) #First row has name of attributes
    totalAttributes = len(listName) - 1 #Last row tells classification and is not an attribute
    fillAll(data) #Modify to our format
    lenData = len(data)
    return data

def readData(fileWithData):
    """Takes in a data file name that has the exact same format as that
    in the hw and modifies is so that we can work with it. However, it
    does not ready the information to make a tree. Therefore, this is used
    mainly for validation set"""
    with open(fileWithData, 'rb') as f:
        reader = csv.reader(f)
        newData = list(reader)
    newData.pop(0) #Since same format as tree, we can disregard
    fillAll(newData) #Modify to our
    return newData

def num(s):
    """Takes a string, s, then returns an integer or a float of that number"""
    try:
        return int(s)
    except ValueError:
        return float(s)

def getLogicalAvg(total, divisor, pos):
    """Using the logic of our hw, we hardcoded whether something was a float
    or an integer."""
    if divisor == 0:
        divisor = 1
    if pos == 0 or pos == 1 or pos == 3:
        return float(total)/divisor
    if pos == 2:
        x = round(float(total)/divisor)
        if x < 1 and x > -1:
            return int(abs(x))
        else:
            return int(x)
    else:
        return int(round(float(total)/divisor))

def average(pos, inData):
    """Find the average for a certain attribute in our data. """
    total=0.0
    divisor=0.0
    for m in inData:
        if (m[pos]!='?'): #Skip if "?" - unknown value for that attribute
            total += num(m[pos])
            divisor +=1
    finalAvg = getLogicalAvg(total,divisor,pos)
    return finalAvg
    
def fill(inData, avg, pos):
    """Fill in the attribute, denoted by pos, with the average, avg, in
    the data"""
    for m in inData:
         if (m[pos]=='?'):
             m[pos]=avg
         else:
             m[pos]=num(m[pos])

def fillAll(inData):
    """Take in data with unknown values denoeted by ? and return a filled
    in list"""
    for x in xrange(0, len(inData[0])):
        a=average(x, inData)
        fill(inData, a, x)
        

def countClass(listOfTuples, Class):
    """Takes in a list of tuples and a classification. Then returns the
    number of tuples that meet that classification"""
    count = 0
    for x in listOfTuples:
        if x[1] == Class:
            count += 1
    return float(count)

def entropyOfSplit(inlist):
    """Takes in a list of tuples that have the (value, class) then it calculates
    the entropy of the binary split.."""
    total = len(inlist)
    if total == 0:#There is no split meaning no information gain
        raise ValueError("inList equals 0")        
        return 1
    if total == 1: #One object means that it was perfectly split
        return 0
    pOfWin = countClass(inlist, 1)/total
    pOfLose = countClass(inlist, 0)/total
    
    if pOfWin == 0: #If split iwth an empty list on one side
        return -(pOfLose)*math.log(pOfLose, 2)
    elif pOfLose == 0: #If split iwth an empty list on one side
        return -(pOfWin)*math.log(pOfWin, 2)
    else:
        return -(pOfWin)*math.log(pOfWin, 2) - (pOfLose)*math.log(pOfLose, 2)

def getEntropy(attribPos,datalist):
    return { "numeric" : getContEntropy(attribPos,datalist),
                "nominal" : getNomEntropy(attribPos,datalist)
    }[numericTypes[attribPos]]

def findEntropyOfSplit(goingLeft,goingRight):
    leftSplit = entropyOfSplit(goingLeft)
    rightSplit = entropyOfSplit(goingRight)
    noSplit = goingLeft + goingRight
    entropyAfter = float(len(goingLeft))/len(noSplit)*leftSplit + float(len(goingRight))/len(noSplit)*rightSplit
    return entropyAfter

def getNomAllSplitsEntropy(k, numk, inList, pos):
    minEntropy = float("inf")
    minLeft = []
    minRight = []
    for val in k:
        goingLeft = []
        goingRight = []
        for result in inList:
            if result[pos] == val:
                goingLeft.append((result[pos], result[totalAttributes]))
            else:
                goingRight.append((result[pos], result[totalAttributes]))
        entropyAfter = findEntropyOfSplit(goingLeft,goingRight)
        if entropyAfter < minEntropy:
            minEntropy = entropyAfter
            minLeft = [val]
            minRight = [x for x in k if x != val]  
    return checkSplits(minEntropy,minLeft,minRight)

def checkSplits(minEntropy,minLeft,minRight):
    if not minLeft or not minRight:
        return (float("inf"), [], [])
    return (minEntropy, minLeft, minRight)

def getNomEntropy(attribPos, datalist):
    """Takes in attribPos, possition of the attribute, and datalist,
    a list of data. Returns a tuple of (entropy, the values of the attributes
    to split on the left  and the values of the attributes to split on the
    right)."""
    listOfAttribute = [el[attribPos] for el in datalist ] #Geting all values of the attribute
    k = list(set(listOfAttribute)) #Using set to have only possible values of the attribute
    numk = len(k)
    if numk <= klimit:
        binEntropy = getNomBinEntropy(k, numk, datalist, attribPos)
        return binEntropy # (entropy, list of values of Attributes left, list of values of Attributes right)
    else:
        nomEntropySplit = getNomAllSplitsEntropy(k, numk, datalist, attribPos)
        return nomEntropySplit # (entropy, list of values of Attributes left, list of values of Attributes right)
        
def getNomBinEntropy(k, numk, dataList, pos):
    if not (k or dataList):
        raise ValueError("K or dataList is empty")
    leftPermutation, rightPermutation = getPermutationsList(k,numk)
    minLeft = []
    minRight = []
    minEntropy = float("inf")
    if len(leftPermutation) != len(rightPermutation):
        raise ValueError("leftPermutation and rightPermutation are not equal in length")
    while leftPermutation:
        templ = leftPermutation.pop()
        tempr = rightPermutation.pop()
        goingLeft = []
        goingRight = []
        for val in templ:
            for result in dataList:
                if result[pos] == val:
                    goingLeft.append((result[pos], result[totalAttributes]))
        for val in tempr:
            for result in dataList:
                if result[pos] == val:
                    goingRight.append((result[pos], result[totalAttributes]))
        
        entropyAfter = findEntropyOfSplit(goingLeft,goingRight)
        if entropyAfter < minEntropy:
            minEntropy = entropyAfter
            minLeft = templ
            minRight = tempr
    return checkSplits(minEntropy,minLeft,minRight)
        
def getPermutationsList(k,numk):
    lst = list(itertools.product([0, 1], repeat=numk))
    
    lst.pop(0)
    lst.pop()
    
    stop = 2**(numk-1) - 1
    left = []
    r = []
    count = 0
    for x in lst:
        if count == stop:
            break
        templ = []
        tempr = []
        for y in xrange(numk):
            if x[y] == 1:
                templ.append(k[y])
            else:
                tempr.append(k[y])
        left.append(templ)
        r.append(tempr)
        count += 1
    return (left,r)

def getContEntropy(attribPos,inList):
    randomInts = makeSample(inList)
    size = len(randomInts)
    xPos = 0
    minEntropy = float("inf")
    randomValTuple = []
    for x in xrange(0,size):#changed from samplesize cause slpitting changes length to <10000
        randomValTuple.append((randomInts[x][attribPos], randomInts[x][totalAttributes]))
    randomValTuple.sort()
    for x in xrange(0, size - 2):
        if (randomValTuple[x][0]!=randomValTuple[x+1][0]):
            goingLeft = randomValTuple[0:x+1]
            goingRight = randomValTuple[x+1:size + 1]
            entropyAfter = findEntropyOfSplit(goingLeft,goingRight)
            if entropyAfter < minEntropy:
                xPos = x
                minEntropy = entropyAfter
    return minEntropy, randomValTuple[xPos][0]
    
def findBestEntropy(datalist):
    if not datalist:
        ValueError("Datalist is empty")
    bestEntropy = (float("inf"), [])
    count=0
    for i in range(0,totalAttributes-1):
        entropyNow = getEntropy(i,datalist)

        if (entropyNow[0] < bestEntropy[0]):
            count = i
            bestEntropy = entropyNow
    if bestEntropy[0] == float("inf"):
        ValueError("Best entropy inf")
    return bestEntropy, count
        
    

def makeSample(inlist):
    """Takes in inlist, a list, and returns a list of randomly selected elements
    from inlist. If inlist is smaller than a proportion to sampleSize, return
    sampleSize"""
    if not inlist:
        raise ValueError('Empty Data List Passed to makeSample')
    if (len(inlist) < sampleSizeProp * sampleSize):
        return inlist
    else:
        return random.sample(inlist, sampleSize)
        
        
# Returns two split lists of big list
def contSeperate(datalist,pos, num):
    firstList=[]
    secondList=[]
    for m in range(0,len(datalist)-1):
        if (datalist[m][pos] <= num):        
            firstList.append(datalist[m])
        else:
            secondList.append(datalist[m])
    return firstList,secondList
        
def nomSeperate(datalist, pos, permList):
    firstList = []
    secondList = []
    for ex in range(0,len(datalist)-1):
        if (datalist[ex][pos] in permList):        
            firstList.append(datalist[ex])
        else:
            secondList.append(datalist[ex])
    return firstList,secondList
    
    
def countSplit(split):
    oneCount = 0
    zeroCount = 0
    for x in range(0,len(split)-1):
        element = split[x]
        outcome = element[len(element)-1]
        if float(outcome) == 1.0:
            oneCount += 1
        else:
            zeroCount += 1
    totalCount = oneCount + zeroCount
    return (float(zeroCount)/float(totalCount)),(float(oneCount)/float(totalCount))
    
def prePrune(dataList):
    currLen = len(dataList)
    percent = float(currLen)/lenData
    if percent > prePruneThresh:
        return True
    else:
        return False
        

class BinaryTree():
    def __init__(self, datalist):
        self.left = None
        self.right = None
        entropyResult = findBestEntropy(datalist)
        self.pos=entropyResult[1]#position of best attribute to split on
        self.entropy=entropyResult[0][0]#the entropy itself
        if (len(entropyResult[0])==2):
            if numericTypes[self.pos] != "numeric":
                ValueError("Not numeric treated as numeric")
            self.splitType = 0 #0 means numeric
            self.num = entropyResult[0][1]
            self.nomList=[]
        else:
            if numericTypes[self.pos] != "nominal":
                ValueError("Not nominal treated as nominal")
            self.splitType = 1 #1 means nominal
            self.nomList = entropyResult[0][1]
            self.num = None
    def getLeftChild(self):
        return self.left
    def getRightChild(self):
        return self.right
    #def setNodeValue(self,value):
        #self.rootid = value
    def getNodeEntropy(self):
        return self.entropy
    def getNodePos(self):
        return self.pos
    def getNodeNum(self):
        return self.num
    def getNodeNomList(self):
        return self.nomList
    def getNodeType(self): #0 means numeric, #1 means nominal  
        return self.splitType
    def insertRight(self, tree):#got rid of newNode, now it stuffs a new tree in
        if self.right == None:
            self.right = tree
        else:
            #tree = BinaryTree(datalist)
            tree.right = self.right
            self.right = tree

    def insertLeft(self, tree):#got rid of newNode, now it stuffs a new tree in

        if self.left == None:
            self.left = tree
        else:
            #tree = BinaryTree(datalist)
            tree.left = self.left
            self.left = tree
            
def getVal(tree):
    if (tree.getNodeType()==0):
        return str(tree.getNodeNum())
    else:
        return str(tree.getNodeNomList())

def DNFPath(node, path):
    global listOfPaths
    AND = " AND "
    if isinstance(node, ClassifyNode):
        if node.getBinary():
            p = AND.join(path)
            p = p[6:] # Remove the AND from previous statement
            listOfPaths.append(p)
        else:
            pass # Not adding path if zero
    elif isinstance(node, BinaryTree):
        lChild = node.getLeftChild()
        rChild = node.getRightChild()
        sLeft = pathString(node, " <= ")
        sRight = pathString(node, " > ")
        lPath = path + [sLeft]
        DNFPath(lChild, lPath)
        rPath = path + [sRight]
        path.append(sRight)
        DNFPath(rChild, rPath)
    return

def DNF(tree):
    global listOfPaths
    OR = " OR "
    DNFPath(tree, [""])
    lPath = OR.join(listOfPaths)
    listOfPaths = []
    print lPath
    return

# <= == being in set,  > == not being in set
def pathString(parent, parentPath):
    if parent.getNodeType() and parentPath == " <= ":
        return str("Is in " + getVal(parent) + " " + listName[parent.getNodePos()] + " ")
    elif parent.getNodeType() and parentPath == " > ":
        return str("Is not in " + getVal(parent) + " " + listName[parent.getNodePos()] + " ")
    return str(parentPath + getVal(parent) + " " + listName[parent.getNodePos()] + " ")
 
 
def seeClassOfList(inList):
    classification = []
    for x in inList:
        classification.append(x[totalAttributes])
    classification.sort()
    print classification

class ClassifyNode:#the leaves of the decision tree
    def __init__(self, datalist):
        total=0
        for x in datalist:
            if(x[totalAttributes] == 1):
                total += 1
        pWin = float(total)/len(datalist) * 100
        if pWin > 50:
            self.binary = 1
        else:
            self.binary = 0
    def getBinary(self):
        return self.binary

#this generates the tree recursively, gain could be information gain or depth, i did depth for now
#also gain could be a finite number and subtract 1 on recursive calls, gain=depth
def decisionTree(datalist, pEntropy):#pass gain=infinity, it will be entropy gain. when too small stops tree
    if (datalist and prePrune(datalist)):#1-tree.getNodeEntropy()=gain
        tree = BinaryTree(datalist)
        newEntropy = tree.getNodeEntropy()
        gain = pEntropy - newEntropy
        if gain > gainThresh:
            if (tree.getNodeType()==0):#numeric
                local = contSeperate(datalist, tree.getNodePos(), tree.getNodeNum())
                tree.insertRight(decisionTree(local[1],newEntropy))#1 means win so if we end after a right branch its a win
                tree.insertLeft(decisionTree(local[0],newEntropy))
            else:#nominal
                local=nomSeperate(datalist, tree.getNodePos(), tree.getNodeNomList())
                tree.insertRight(decisionTree(local[1], gain))
                tree.insertLeft(decisionTree(local[0], gain))
            return tree
        else:
            return ClassifyNode(datalist)
    elif not datalist:
        return ClassifyNode([[0] * 14])
    else:
        return ClassifyNode(datalist)

def dTree(datalist):
    return decisionTree(datalist, 1)

#classifies an example
def classify(example,tree):
    if isinstance(tree, BinaryTree):
        if (tree.getNodeType()==0):
            if (tree.getNodeNum()>example[tree.getNodePos()]):
                return classify(example,tree.getLeftChild())
            else:
                return classify(example,tree.getRightChild())
        else:
            if (example[tree.getNodePos()] in tree.getNodeNomList()):
                return classify(example,tree.getLeftChild())
            else:
                return classify(example,tree.getRightChild())
    else:
        return tree.getBinary()

def countLeaf(tree, x): # x is either 1 or 0 for win or loss
    if isinstance(tree, BinaryTree):
        return countLeaf(tree.getLeftChild(), x) + countLeaf(tree.getRightChild(), x)
    else:
        if(tree.getBinary()==x):
            return 1
        else:
            return 0
            
def mostCommon(tree):
    if (countLeaf(tree, 0)>countLeaf(tree, 1)):
        return 0
    else:
        return 1
        
def replaceR(tree):
    fakeEx=[0]*(totalAttributes+1)
    fakeEx[totalAttributes]=mostCommon(tree.getRightChild())
    tree.insertRight(ClassifyNode([fakeEx]))
    

def replaceL(tree):
    fakeEx=[0]*(totalAttributes+1)
    fakeEx[totalAttributes]=mostCommon(tree.getLeftChild())
    tree.insertLeft(ClassifyNode([fakeEx]))
    
def prune(valid, tree):
    if isinstance(tree, BinaryTree):
        prune(valid, tree.getLeftChild())
        prune(valid, tree.getRightChild())
        prunedTree = deepcopy(tree)
        replaceR(prunedTree)
        if (testTrain(valid,prunedTree)>=testTrain(valid, tree)):
            tree.insertRight(prunedTree.getRightChild())
        prunedTree=deepcopy(tree)
        replaceL(prunedTree)
        if (testTrain(valid, prunedTree)>=testTrain(valid, tree)):
            tree.insertLeft(prunedTree.getLeftChild())
            
def testTrain(valid, tree):
    total=0
    for ex in valid:
        if ex[13]==classify(ex,tree):
            total+=1
    return total
        
def pCorrect(vdata, tree):
    totalCorrect = testTrain(vdata, tree)
    total = len(vdata)
    return (float(totalCorrect)/total) * 100
        
def outputClassifiedTest(inTestFile,outTestFile,tree):
    outputClassifyFile(inTestFile,outTestFile, tree)

def outputClassifyFile(inData,outData,tree):
    fin = readData(inData)
    with open(outData,"wb") as fout:
        writer=csv.writer(fout)
        for row in fin:
            writer.writerow(guessLastVal(row,tree)) 

# take in tree and dataset then  output one or zero in last column
def guessLastVal(wRow, tree):
    binVal = classify(wRow, tree)
    wRow[-1] = binVal 
    return wRow


        
def assertNoTuple(inlist):
    for x in inlist:
        assert not isinstance(x, tuple)
def assertNot1(inLT):
    assert not (len(inLT) == 1)
def assertNoRep(inPos, inList):
    x = inList[0][inPos]
    allTheSame = True
    for i in inList:
        if not x == i[inPos]:
            allTheSame = False
    if allTheSame:
        print inList
        print inPos
        raise ValueError("All the Same")