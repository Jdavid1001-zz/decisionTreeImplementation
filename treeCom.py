# -*- coding: utf-8 -*-
"""
Created on Fri May  1 14:23:09 2015

@author: Robert Parrillo, Michael Gofron, Juan David Dominguez
"""
import sys
import decisionTreeImpl as treeML
import pickle

fileName = ""
dataFile = ""
validateFile = ""
newValidateName = ""
newTreeName = ""
treeFile = ""
classifiedFileIn = ""
classifiedFileOut = ""
Prune = False
newTree = False
validate = False
doingTree = False
newValidate = False
newData = False
newTesting = False
newClassified = False 
validateData = []
data = []
tree = []

for x in xrange(len(sys.argv)):
    if sys.argv[x] == "nt":
        dataFile = sys.argv[x + 1]
        newTreeName = sys.argv[x + 2]
        newData = True
        doingTree = True
    if sys.argv[x] == "rt":
        treeFile = sys.argv[x + 1]
        doingTree = True
    if sys.argv[x] == "nv":
        validateFile = sys.argv[x + 1]
        newValidateName = sys.argv[x + 2]
        validate = True
        newValidate = True
    if sys.argv[x] == "rv":
        validateFile = sys.argv[x + 1]
        validate = True
    if sys.argv[x] == "tc":
        classifiedFileIn = sys.argv[x + 1]
        classifiedFileOut = sys.argv[x + 2]
        newClassified = True
    if sys.argv[x] == "p":
        Prune = True
        newTesting = True
    if sys.argv[x] == "np":
        newTesting = True
        continue

print "Begining"


if newData and doingTree:
    data = treeML.init(dataFile)
    tree = treeML.dTree(data)
    pickle.dump(tree, open(newTreeName, "wb") )
elif doingTree:
    tree = pickle.load(open(treeFile, "rb"))

if newValidate and validate:
    validateData = treeML.readData(validateFile)
    pickle.dump(validateData, open(newValidateName, "wb"))
elif validate:
    validateData = pickle.load(open(validateFile, "rb"))

if newClassified:
    if not tree:
        raise  Exception("Not Classifying since no tree specified")
    else:
        treeML.outputClassifiedTest(classifiedFileIn, classifiedFileOut, tree)



if Prune and newTesting and doingTree and validate:
    print 
    print "DNF Before Prune"
    treeML.DNF(tree)
    
    print
    print "Percent of correct validation classifications before Prune:"    
    print treeML.pCorrect(validateData, tree)

    treeML.prune(validateData, tree)        
    
    print
    print "DNF After Prune"
    treeML.DNF(tree)
    
    print
    print "Percent of correct validation classifications after Prune:"
    print treeML.pCorrect(validateData, tree)
elif newTesting and doingTree and validate:
    print
    print "DNF Without Prune"
    treeML.DNF(tree)
    
    print
    print "Percent of correct validation classifications without prune:"
    print treeML.pCorrect(validateData, tree)
