import sys
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser

def apriori(data, minSup, minConf):

    def getDataList(data): #get the whole list of transactions
        dataList = list()
        itemSet = set()
        for record in data:
            element = frozenset(record)
            dataList.append(element)
            for item in element:
                itemSet.add(frozenset([item]))
        return itemSet, dataList
    
    def setJoin(itemSet, length): #join set function 
        return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])
    
    def getSup(item): #returns the support of the item
        return float(freqSet[item])/len(dataList)

    def subsets(dS): #returns the subsets of the given set
        return chain(*[combinations(dS, i + 1) for i, j in enumerate(dS)])
    
    def supportTest(itemSet, dL, minSup, freqSet): #returns sets above support
        retSet = set()
        tempSet = defaultdict(int)

        for item in itemSet:
                for data in dL:
                        if item.issubset(data):
                                freqSet[item] += 1
                                tempSet[item] += 1

        for item, count in tempSet.items():
                support = float(count)/len(dL)
                if support >= minSup:
                        retSet.add(item)
        return retSet
    
    itemSet, dataList = getDataList(data)

    freqSet = defaultdict(int)
    baseSupSet = dict() #contains all sets above support

    cSet = supportTest(itemSet,dataList,minSup,freqSet)
    lSet = cSet
    
    k = 2
    while(lSet != set([])):
        baseSupSet[k-1] = lSet
        lSet = setJoin(lSet, k)
        cSet = supportTest(lSet,dataList,minSup,freqSet)
        lSet = cSet
        k = k + 1
    
    finalItemSets = []
    for k, value in baseSupSet.items(): #compiles a list of all the sets above support
        finalItemSets.extend([(tuple(item), getSup(item))
                           for item in value])

    finalAccRules = []
    for k, value in baseSupSet.items()[1:]: #compile a list of all the rules above confidence
        for item in value:
            subSets = map(frozenset, [x for x in subsets(item)])
            for element in subSets:
                remain = item.difference(element)
                if len(remain) > 0:
                    conf = getSup(item)/getSup(element)
                    if conf >= minConf:
                        finalAccRules.append(((tuple(element), tuple(remain)), conf))
    return finalItemSets, finalAccRules

def getData(fN, dL, pO): #grabs data from a given file and returns a generator
        data = open(fN, 'rU')
        firstLine = True   #counter for first line
        colNames = [] #data column names
        for line in data:
                line = line.strip().rstrip(dL) #strip of trailing characters
                lineset = line.split(dL) #split data by given character
                if pO == '1': #non unique columns
                    for i in range(len(lineset)):
                        lineset[i] = lineset[i].strip('"')
                elif pO == '2': #unique columns with no name
                    for i in range(len(lineset)):
                        lineset[i] ="col"+str(i)+": "+lineset[i].strip('"')
                elif pO == '3': #unique columns with first line as the name
                    if firstLine == True:
                        firstLine = False
                        colNames = lineset
                        for i in range(len(colNames)):
                            colNames[i] = colNames[i].strip('"')
                    else:
                        for i in range(len(lineset)):
                            lineset[i] =colNames[i]+": "+lineset[i].strip('"')
                else:
                    pO = pO.strip().rstrip(dL)
                    colNames=pO.split(dL)
                    for i in range(len(lineset)):
                        lineset[i] =colNames[i]+": "+lineset[i].strip('"')
                dataset = frozenset(lineset)
                yield dataset   #return a generator to save memory

def printr(aS, rS): #print all the sets and rules with a given format
    print "\n------------------ ITEMS ------------------"
    print "Item: item set, support"
    for item, sup in aS:
        print "Item: %s , %.3f" % (str(item), sup)
    print "\n------------------ RULES ------------------"
    print "Rule: rule set, confidence"
    for rule, conf in rS:
        pre, post = rule
        print "Rule: %s ==> %s , %.3f" % (str(pre), str(post), conf)
    print "\n------------------- END -------------------"

if __name__ == "__main__":
    #runs this if it is run from a script
    op = OptionParser()
    op.add_option('-f', '--inputFile',dest='input',help='data file',default=None)
    op.add_option('-s', '--minSup',dest='minS',help='minimum support value',default=0.25,type='float')
    op.add_option('-c', '--minConf',dest='minC',help='minimum confidence value',default=0.8,type='float')   
    op.add_option('-d', '--deLimiter',dest='dL',help='the splitting character',default=',',type='string')  
    op.add_option('-p', '--parseOptions',dest='pOpt',help='parsing options, refer to readme file',default='1',type='string')
    #different run options for the algorithm
                         
    (opt, args) = op.parse_args()

    inFile = None
    if opt.input is not None:
            inFile = getData(opt.input,opt.dL,opt.pOpt)
    else:
            print "Please specify a valid data file with the option -f 'filename'\n"
            sys.exit()

    acc_sets, rule_sets = apriori(inFile, opt.minS, opt.minC)
    printr(acc_sets, rule_sets)