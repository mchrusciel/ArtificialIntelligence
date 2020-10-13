import sys
import random

 
class vertex():
    def __init_(name, edge):
        self.name = name
        self.edge = edge

    def __str__(self):
        return self.name 

    def __repr__(self):
        return str(self)



            
        
vertexCount = 0
vertices = []
keyClause = []
propositions = []
vertexList = []
edges=[]

def input1():
    with open(sys.argv[1],'r') as file:
        i = 0
        for line in file:
            if(i == 0):
                vertexCount = int(line)
            
            else:
                for elm in line:
                    if (elm not in vertices and elm != " " and elm != "\n"):
                        vertices.append(elm)
                edges.append(line.strip())

            i+=1
       
        vertices.sort()
        #print(vertices)
        #print(edges)
        for name in vertices:
            v = vertex()
            v.name = name
            vertexList.append(v)

            #


        


       # print(vertexList)
        
        j = 1


        for elm in vertices:
            for i in range(1,vertexCount+1):
                seq = str(j) + " " + elm + " " + str(i)
                keyClause.append(seq)
                j+=1

        #print(keyClause)

        for i in range(len(keyClause)):
            k=i
            bad = 0

            #print(str(keyClause[12].split(" ")[0]))
            while(k+vertexCount < len(keyClause)):
                j=k
                while((j+vertexCount)<len(keyClause)):
                    j+=vertexCount
                    prop = "-" + str(keyClause[k].split(" ")[0]) + " -" + str(keyClause[j].split(" ")[0])
                    # print(j)
                    if prop in propositions:
                        bad = 1
                        break
                    #print(prop)

                    propositions.append(prop)

                k+=vertexCount
                if(bad == 1):
                    break



            j = vertexCount+1      
            track = 0

        
        
        for i in range(len(vertices)):
            n = 0
            m= vertexCount*i
            for j in range(len(vertices)):
                sequence = ""
                
                if(vertices[i]!=vertices[j]):

                    sequence = vertices[i] + " " + vertices[j]
                   # print(sequence)
                    n=(vertexCount*j)+1
                   # print(n)
                    #print(sequence)
                    
                   # print(j)
                    #n+=j
                    #print(seq)
                if(sequence not in edges and len(sequence)> 1):

                    #print(n)
                    for k in range(0,vertexCount-1):
                        #print(i)
                        
                        prop = "-" + str(keyClause[m+k].split(" ")[0]) + " -" + str(keyClause[k+n].split(" ")[0])
                        propositions.append(prop)
                   # n+=1
                        #print(prop)
                

        frontEndFileOutput = open("FrontEndOutput.txt", 'w')

        topString = ""
        for i,elm in enumerate(keyClause):
            topString = topString + " " + (elm.split(" ")[0])
            if i%vertexCount == 0 and i > 0:
                topString = topString + "\n"

        topString = topString + "\n\n\n"
        midString = ""
        for elm in propositions:
            midString = midString + elm + "\n"

        midString = midString + "0\n"

        edgeString = ""
        for ed in keyClause:
            edgeString = edgeString + ed + "\n"

        frontEndFileOutput.write(topString)
        frontEndFileOutput.write(midString)
        frontEndFileOutput.write(edgeString)
        frontEndFileOutput.close()
        return
            
atomList= []
clauseList = []
clausesListEnd = []
def inputFromFront(input2):
    with open(input2,'r') as file:
        counter2 = 0
        counter = 0
        for line in file:
            if not line.strip():
                counter2 = 1
            if(counter2 == 1 and line.strip()):
                if counter == 1:
                    line2 = line.strip().split(" ")

                    clausesListEnd.append(line2[1])


           
                elif line[0] is not "0":
                    currList= line.strip().split(" ")
                    for elm in currList:
                        e = elm.replace("-", "")
                        if e not in atomList:
                            atomList.append(e)
                    clauseList.append(currList)
                else:
                    counter = 1

            for clauses in clauseList:
                for i in range(0, len(clauses)):
                    #print(clauses)
                    clauses[i] = int(clauses[i]) 

def handlePureLiteral(clauses):
    positionalArgs = []


    
    for c in clauses:
       
        for l in c:
            counter = 0
            neg = l*-1
            for c in clauses:
                if neg in c:
                    counter =1
                    break
            if counter is 0:
                positionalArgs.append(l)

                    #Negative is there - not pure literal
    #print(positionalArgs)
    return positionalArgs
def handleSingletion(clauses):
    positionalArgs = None
    #print(clauses)
    for a in clauses:
       # print(a)

        if(len(a) == 1):
            #print(a)
            positionalArgs = a[0]
            break
    #print(positionalArgs)
    return positionalArgs
    















MASTER = -1
stage = 1

def DP(atoms, clauses, TruthVals):
    
    global MASTER  
    global stage
    MASTER+=1
    check = False
    check2 = True
    masterCheck = True
   


    while(masterCheck):
        x = handlePureLiteral(clauses)
        y = handleSingletion(clauses)
        #print(y)
        #print(clauses)
        masterCheck = False

        if(len(clauses) is 0):
           # print("b;lyat")

           # print("Hello")
            for i in range(len(TruthVals)):
                if TruthVals[i] is None:
                    TruthVals[i] = True
            return TruthVals
        elif any(a for a in clauses) is False:
            #print("sdadasda")

           # print("Suh")
            return None

        elif(len(x) > 0):
            masterCheck = True
            #print("Pure Literal")
            o = 0
            #print(x[0])
            TruthVals = obviousAssign(x[0], TruthVals)
            while(o < len(clauses)):
                if x[0] in clauses[o] or -1*x[0] in clauses[o]:
                    #clauses[o] = []
                    del clauses[o]
                    o-=1
                o+=1
            


        elif(y is not None):
            masterCheck = True
            #print("Singleton")
            #print(y)
            TruthVals = obviousAssign(y, TruthVals)
            clauses = propagate(str(abs(y)), clauses, TruthVals)
            #print(TruthVals)
            #print(clauses)

       # print(TruthVals)

    #print(clauses)
    #print()
        

   # print(clauses)
    #print(TruthVals)
    #HARD CASES
    ##ClauseCopy = clauses.copy()
    TruthValsCopy = TruthVals.copy()

   # print("After While Loop")
   # print(clauses)
    
    #print(TruthValsCopy)
    

    index = None
    for i in range(len(TruthVals)):

        if(TruthVals[i] is None):
            index = i
            TruthVals[i] = True
            break
   # print(stage)
    clauses2 = [x[:] for x in clauses]
    

    #print(clauses2)
    stage+=1
   
    
    #print(clauses2)
    clauses2 = propagate(atomList[index], clauses2,  TruthVals)
   # print(ClauseCopy)
    #print("This is clauses2")
    #print(clauses2)
    #HERE
    #print("beforesuh")
    TruthVals2 = DP(atomList, clauses2, TruthVals)
   # if TruthVals2 is None:
       # print("Hello Ther!")
   # print(ClauseCopy)
   # print(clauses2)
   # print(clauses)
   # print("aftersuh")
    if TruthVals2 is not None:
        return TruthVals2

    elif TruthVals2 is None:
       # print("HEHEHEEH")
       # print(TruthVals)
        #print(TruthValsCopy)
        TruthVals = TruthValsCopy.copy()
        
        
        TruthVals[index] = False
       # print(TruthVals)
       # clauses = clauses.copy()

        #print(index)
        clauses2 = propagate(atomList[index], clauses, TruthVals)
       # print(int(atomList[index])* -1)
        #print(atomList.index(atomList[index]))
        #print(clauses2)
        #MASTER+=1

        return (DP(atomList, clauses2, TruthVals))


def propagate(A, S, V):
   # print(A)
   # print(V)
    #print(atomList)
    #print(S)
   # print(atomList.index(A))
    #print(V)
    o = 0
    while ( o < len(S)):
        #print(S[o])
        #print(int(A)*-1)
       # print(V[atomList.index(A)])

        
        if((int(A) in S[o] and V[atomList.index(A)] is True) or (int(A)*-1 in S[o] and V[atomList.index(A)] is False )):
            print("SHOULD BE HERE")
            #print(p)
            #c = []
            del S[o]
            o-=1
            #print(c)
            #print(S)
        elif(int(A) in S[o] and V[atomList.index(A)] is False):
            S[o].remove(int(A))
        elif(int(A)*-1 in S[o] and V[atomList.index(A)] is True):
            S[o].remove(int(A)*-1)
        o+=1
   # print(S)
    #print("HEHEHE")
    return S

def obviousAssign(L, V):
   # print(V)
    #print(L*-1)
   # print(L)
   # print(type(L))
    if L > 0:
        V[L-1] = True
    elif int(L)<0:
        V[(L*-1)-1] = False
    #print(V)
    #print(V)
    return V
#input1()


input1()
filename = "FrontEndOutput.txt"
inputFromFront(filename)





TruthVals = [None] * len(atomList)
#print(TruthVals)
atomListCopy = atomList.copy()
a = DP(atomList, clauseList, TruthVals)
#print(a)
#print(a)



dpOutput = open("DPOutput.txt", 'w')

for i,c in enumerate(a):

    p1 = ""
    x = i+1
    if c is False:
        p1 = "F"
    elif c is True:
        p1 = "T"
    string = str(x) + " " + p1 + "\n"

    dpOutput.write(string)
dpOutput.write("0\n")

for i,atoms in enumerate(clausesListEnd):
    #print(ato)
    string = str(i+1) + " " + atoms + "\n"
    dpOutput.write(string)








    


