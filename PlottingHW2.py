# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

regTree = [(69.34, 100), (78.97999999999999, 200), (64.47, 300), (80.22, 400), (67.14, 500), (80.73, 600), (65.08, 700), (57.93000000000001, 800), (68.56, 900), (80.11, 1000), (66.88, 1100), (80.34, 1200), (48.309999999999995, 1300), (65.09, 1400), (65.14, 1500), (48.08, 1600), (65.08, 1700), (70.03, 1800), (65.66, 1900), (48.35, 2000), (63.78, 2100), (80.11, 2200), (50.07, 2300), (66.06, 2400), (82.88, 2500), (70.02000000000001, 2600), (82.3, 2700), (61.99, 2800), (80.93, 2900), (59.089999999999996, 3000), (68.4, 3100), (65.03, 3200), (65.08, 3300), (69.67, 3400), (67.56, 3500), (48.28, 3600), (67.19000000000001, 3700), (68.46, 3800), (81.97, 3900), (70.35, 4000), (66.62, 4100), (68.85, 4200), (48.29, 4300), (68.60000000000001, 4400), (49.09, 4500), (77.84, 4600), (71.89999999999999, 4700), (63.78, 4800), (71.77, 4900), (65.08, 5000), (67.99, 5000), (48.26, 10000), (71.53, 15000), (69.97, 20000), (72.41, 25000), (63.78, 30000), (65.12, 35000), (63.85999999999999, 40000), (70.17999999999999, 45000), (73.83999999999999, 50000)]
pTree = [(63.78, 100), (78.97999999999999, 200), (63.78, 300), (80.22, 400), (67.14, 500), (82.11, 600), (65.08, 700), (60.89, 800), (70.03, 900), (81.13, 1000), (66.88, 1100), (81.36, 1200), (48.309999999999995, 1300), (63.78, 1400), (65.14, 1500), (48.08, 1600), (65.08, 1700), (70.03, 1800), (70.03, 1900), (48.35, 2000), (63.78, 2100), (81.13, 2200), (50.07, 2300), (66.06, 2400), (83.87, 2500), (70.03, 2600), (82.3, 2700), (65.66, 2800), (81.35, 2900), (60.86, 3000), (70.03, 3100), (65.03, 3200), (65.08, 3300), (63.99, 3400), (67.56, 3500), (48.28, 3600), (71.63000000000001, 3700), (72.82, 3800), (71.77, 3900), (70.35, 4000), (68.14, 4100), (71.89999999999999, 4200), (48.08, 4300), (70.03, 4400), (49.09, 4500), (78.01, 4600), (71.89999999999999, 4700), (63.78, 4800), (71.78, 4900), (65.08, 5000), (67.99, 5000), (48.26, 10000), (71.53, 15000), (69.97, 20000), (72.41, 25000), (63.78, 30000), (65.12, 35000), (63.85999999999999, 40000), (70.17999999999999, 45000), (73.83999999999999, 50000)]

yReg, xReg = zip(*regTree)
yPrune, xPrune = zip(*pTree)

xRegA = np.asarray(xReg)
yRegA = np.asarray(yReg)
yPrune = np.asarray(yPrune)

# red dashes, blue squares and green triangles
plt.plot(xRegA, yRegA, 'r--', xRegA, yPrune, 'bs')
plt.xlabel('Size Of Data')
plt.ylabel('Percent Correct')
plt.yticks(xrange(0, 110, 10))
plt.title('Learning Curve')
plt.show()

"""
import numpy as np
import matplotlib.pyplot as plt



mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# the histogram of the data
n, bins, patches = plt.hist(x, 50, normed=1, facecolor='g', alpha=0.75)


plt.xlabel('Smarts')
plt.ylabel('Probability')
plt.title('Histogram of IQ')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.show()
"""
"""
import HW2349 as treeML
import pickle


dataFile = "btrain.csv"
validateData = pickle.load(open("validationset", "rb"))
data = treeML.init(dataFile)
intervals = 10
lenD = len(data)
init = lenD/intervals



treePercent = [(67.99, 1), (48.26, 2), (71.53, 3), (69.97, 4), (72.41, 5), (63.78, 6), (65.12, 7), (63.85999999999999, 8), (70.17999999999999, 9), (73.83999999999999, 10)]
pruneTreePercent = [(67.99, 1), (48.26, 2), (71.53, 3), (69.97, 4), (72.41, 5), (63.78, 6), (65.12, 7), (63.85999999999999, 8), (70.17999999999999, 9), (73.83999999999999, 10)]

ntreePercent = []
npruneTreePercent = []

newInputData = []
newInputDataPrune = []
for i in xrange(len(treePercent)):
    tp = treePercent[i]
    ptp = pruneTreePercent[i]
    x = tp[0]
    y = tp[1] * 5000
    newInputData.append((x,y))
    xp = ptp[0]
    yp = ptp[0] * 5000
    newInputDataPrune.append((x,y))

for x in range(100, 5100, 100):
    print x
    tree = treeML.dTree(data[:x])
    ntreePercent.append((treeML.pCorrect(validateData, tree), x))
    treeML.prune(validateData, tree)
    npruneTreePercent.append((treeML.pCorrect(validateData, tree), x))

newDataTree = ntreePercent + newInputData
newDataPruneTree = npruneTreePercent + newInputDataPrune

print newDataTree
print newDataPruneTree
"""

"""
    tree = treeML.dTree(data[:x])
    ntreePercent.append((treeML.pCorrect(validateData, tree), x))
    treeML.prune(validateData, tree)
    npruneTreePercent.append((treeML.pCorrect(validateData, tree), x))
"""
    



""""
for i in range(1, 11):
    s = ("tree_%s" %str(i))
    ps = ("prune_tree_%s" %str(i))
    tree = pickle.load(open(s, "rb"))
    pTree = pickle.load(open(ps, "rb"))
    print "Doing treee", i
    treeML.DNF(tree)
    print "Doing Prune treee", i
    treeML.DNF(pTree)


"""


"""
treePercent = []
pruneTreePercent = []
validateData = pickle.load(open("validationset", "rb"))
for i in range(1, 11):
    s = ("tree_%s" %str(i))
    ps = ("prune_tree_%s" %str(i))
    tree = pickle.load(open(s, "rb"))
    pTree = pickle.load(open(ps, "rb"))
    treePercent.append((treeML.pCorrect(validateData, tree), i))
    pruneTreePercent.append((treeML.pCorrect(validateData, tree), i))

print pruneTreePercent
print treePercent

print len(pruneTreePercent)
print len(treePercent)

pickle.dump(treePercent, open("Tree_Percent_Correct", "wb"))
pickle.dump(pruneTreePercent, open("Prune_Tree_Percent_Correct", "wb"))

"""

"""
dataFile = "btrain.csv"
validateData = pickle.load(open("validationset", "rb"))
data = treeML.init(dataFile)
intervals = 10
lenD = len(data)
init = lenD/intervals


i = 1
treePercent = []
pruneTreePercent = []


for x in range(init, lenD + init, init):
    s = ("tree_%s" %str(i))
    ps = ("prune_tree_%s" %str(i))
    print "Doing", s
    tree = treeML.dTree(data[:x])
    pickle.dump(tree, open(s, "wb") )
    treePercent.append((treeML.pCorrect(validateData, tree), x))
    print "Doing", ps    
    treeML.prune(validateData, tree)
    pruneTreePercent.append((treeML.pCorrect(validateData, tree), x))
    pickle.dump(tree, open(ps, "wb"))
    i += 1
    
pickle.dump(treePercent, open("Tree Percent Correct", "wb"))
pickle.dump(pruneTreePercent, open("Tree Percent Correct", "wb"))"""