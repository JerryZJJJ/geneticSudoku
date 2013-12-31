import re, os, sys
import random as r
import copy


class sudsol:
    block = None
    perm = None
    def __init__(self):
        self.block = [[-1 for j in range(9)] for i in range(9)]
        self.perm = [[1 for j in range(9)] for i in range(9)]
        ## everything is permanent until we load...

    def poke(self, x, y, v):
        if(x<9) & (y<9):
            self.block[x][y] = v 

    def grade(self):
        rowGrade = sum([len(set(i)) for i in self.block])
        #print rowGrade
        colGrade = 0
        for col in range(0, 9):
            #print "-",colGrade
            colGrade+=len(set([self.block[i][col] for i in range(0, 9)]))
            #print [self.block[i][col] for i in range(0, 9)]
        #print colGrade
        zoneGrade = 0
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                setSum = set()
                for x1 in range(0, 3):
                    for y1 in range(0, 3):
                        setSum.add(self.block[x+x1][y+y1])
                        #print "-",self.block[x+x1][y+y1]
                zoneGrade+=len(setSum)
                setSum = None
        #print zoneGrade
        return(colGrade+rowGrade+zoneGrade)

    def randomize(self):
        for i in range(0, 1000):
            self.poke(r.randint(0, 9), r.randint(0, 9), r.randint(1,9)) 

    def load(self, inStr):
        count = 0
        for k in inStr.split("\n"):
           # print k
            if(count>=9):
                break
            if(len(k.strip().split(" "))==9):
                self.block[count] = [int(r) for r in k.strip().split(" ")]
            else:
                raise Exception
            count+=1
        for x in range(9):
            for y in range(9):
                if(self.block[x][y]==-1):
                    self.perm[x][y] = 0
                    #if it's -1, it's a permanent

    def fliprand(self, numTimes):
        unks = []
        for x in range(0, 9):
            for y in range(0, 9):
                if(self.block[x][y]==-1):
                    unks.append([x,y])
        for i in range(0, numTimes):
            tgt = unks[r.randint(0, len(unks)-1)]
            self.block[tgt[0]][tgt[1]] = r.randint(1, 9)

    def mutate(self, numTimes):
        unks = []
        for x in range(0, 9):
            for y in range(0, 9):
                if(self.perm[x][y]==0):
                    unks.append([x,y])
        for i in range(0, numTimes):
            tgt = unks[r.randint(0, len(unks)-1)]
            self.block[tgt[0]][tgt[1]] = r.randint(1, 9)

    def randsolve(self):
        for x in range(9):
            for y in range(9):
                if(self.perm[x][y]==0):
                    self.block[x][y]=r.randint(1,9)

    def pprop(self):
        for i in self.block:
            for j in i:
                print str(j).rjust(3),
            print str(len(set(i)))


    def merge(self, another):
        for x in range(9):
            for y in range(9):
                if(self.perm!=1):
                    if(r.randint(0,1)==1):
                        self.block[x][y] = another.block[x][y]

if(__name__=="__main__"):
   # ss = sudsol()

    #ss.randomize()

    samp1 = '''-1 -1 3 -1 5 9 -1 8 6
-1 8 5 -1 1 -1 2 -1 4
-1 -1 -1 -1 -1 -1 5 7 -1
-1 4 1 -1 8 5 -1 -1 -1
-1 9 -1 3 -1 1 -1 4 -1
-1 -1 -1 4 6 -1 9 1 -1
-1 6 2 -1 -1 -1 -1 -1 -1
7 -1 8 -1 2 -1 6 3 -1 
9 1 -1 5 3 -1 7 -1 -1'''

    samp2 = '''7 1 -1 -1 -1 5 -1 8 -1
-1 -1 -1 3 -1 8 -1 -1 -1
4 -1 3 7 1 9 6 -1 5
6 7 5 9 -1 2 -1 -1 -1
-1 3 8 -1 5 -1 -1 9 6
-1 9 -1 -1 -1 6 2 5 3
8 2 -1 -1 9 3 -1 -1 -1
3 -1 -1 -1 8 7 -1 -1 -1
9 -1 7 -1 -1 1 -1 3 2'''
#    ss.load(samp1)
#    ss.fliprand(2)
    
    samp1 = samp2 
    solSet = []
    for k in range(0, 200):
        solSet.append([0, sudsol()])
    for t in solSet:
        t[1].load(samp1)
        t[1].randsolve()
        t[0] = t[1].grade()

    runs = 0
    numRuns = 1000

    high = 0
    while(runs < numRuns): 
        avgScore = float(sum([i[1].grade() for i in solSet]))/len(solSet)
        solSet.sort()
        print "Max: ",solSet[-1][0]," High: ",high
        if(solSet[-1][0]>high):
            high = solSet[-1][0]
        #solSet[-1][1].pprop()
        #print [j[0] for j in solSet]
        maxMerge = len(solSet)/3
        for i in range(0, maxMerge):
            solSet[i][1] = copy.deepcopy(solSet[r.randint(len(solSet)-maxMerge, len(solSet)-1)][1])
            solSet[i][1].merge(solSet[r.randint(len(solSet)-maxMerge, len(solSet)-1)][1])

        for i in range(0, len(solSet)):
            gGrade = solSet[i][1].grade()
            #print gGrade,
            #if(i>(len(solSet)-20)):
            #    pass
            if(gGrade<avgScore):
                solSet[i][1] = sudsol()
                solSet[i][1].load(samp1)
                solSet[i][1].randsolve()
            elif(gGrade>242):
                print solSet[i][1].block
            else:
                solSet[i][1].mutate(1)
            solSet[i][0] = solSet[i][1].grade()
        #print ""
        runs+=1
        ## if we assess it to be solved
        if(high==243):
            break

    solSet.sort()
    solSet[-1][1].pprop()

    '''
    for k in ss.block:
        for t in k:
            print str(t).rjust(3),
        print ""

    print ss.grade()
    '''
