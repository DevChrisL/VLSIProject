from multipledispatch import dispatch #For overloaded functions
from z3 import *
import Vertex
import Edge
import random


class Circuit:
    def __init__(self) -> None:
        self.numVertices = 0 #Number of gates (including PIs) in the circuit
        self.numPIs = 0 #Number of PIs, specifically
        self.vList = [] #List of gates
    
    #Returns true of circuit is empty, false otherwise
    def empty(self) -> bool:
        if self.numVertices == 0:
            return True
        else:
            return False

    #Clears the circuit of all vertices and edges
    def clear(self) -> None:
        while not self.empty():
            self.removeVertex(self.vList[0].label)

    #Primary Input Vertex
    @dispatch(str)
    def addVertex(self, name) -> None:
        if name == '':
            return
        newV = Vertex.Vertex(name, 0, False, True)
        self.vList.append(newV)
        self.numPIs += 1
        self.numVertices += 1

    #Secondary Gate Vertex (Not PI) w/ Default NAND Gate
    @dispatch(str, bool)
    def addVertex(self, name, primaryOut) -> None:
        if name == '':
            return
        newV = Vertex.Vertex(name, 0, primaryOut)
        self.vList.append(newV)
        self.numVertices += 1

    #Secondary Gate Vertex (Not PI) w/ Gate Value
    @dispatch(str, bool, int)
    def addVertex(self, name, primaryOut, gate) -> None:
        if name == '':
            return
        newV = Vertex.Vertex(name, gate, primaryOut)
        self.vList.append(newV)
        self.numVertices += 1

    #This function finds the vertex (gate) given a label and returns the index if found, -1 otherwise
    def findVertex(self, name) -> int:
        for i, v in enumerate(self.vList):
            if v.label == name:
                return i
        return -1

    #This function removes a vertex with label name
    def removeVertex(self, name) -> None:
        index = self.findVertex(name)
        if index == -1:
            print('Vertex not found')
            return
        targetV = self.vList[index]

        #Remove edges connected to this vertex
        for v in self.vList:
            for e in v.adjList:
                if e.end == name:
                    self.removeEdge(e.start, name)
    
        #Remove edges connected from this vertex
        targetV.adjList.clear()
        del self.vList[index]
        self.numVertices -= 1
    
    #Adds an edge between two vertices (gates), directional (start -> end)
    def addEdge(self, startLab, endLab) -> None:
        index = self.findVertex(startLab)
        if index == -1:
            print('Vertex ' + startLab + ' not found')
            return
        startV = self.vList[index]

        newEdge = Edge.Edge(startLab + ' to ' + endLab, startLab, endLab)
        if startV.PI:
            newEdge.faultList.append('s-a-0')
            newEdge.faultList.append('s-a-1')
        startV.adjList.append(newEdge)

    #Removes edge between two vertices
    def removeEdge(self, startLab, endLab) -> None:
        index = self.findVertex(startLab)
        if index == -1:
            print('Vertex ' + startLab + ' not found')
            return
        startV = self.vList[index]

        for i, edg in enumerate(startV.adjList):
            if edg.end == endLab:
                break
        
        del startV.adjList[i]

    #Manually changes the output value of a given vertex
    def changeValue(self, name, value) -> None:
        index = self.findVertex(name)
        if index == -1:
            print('Vertex ' + name + ' not found')
            return
        targetV = self.vList[index]
        
        targetV.outputVal = value

    #Manually changes the gate-type of a given vertex
    def changeGate(self, name, value) -> None:
        index = self.findVertex(name)
        if index == -1:
            print('Vertex ' + name + ' not found')
            return
        targetV = self.vList[index]
        
        targetV.gate = value
    
    #USED FOR D-ALG: Sets all vertex (gate) outputs to don't care: x
    def xInputs(self) -> None:
        for v in self.vList:
            self.changeValue(v.label, 'x')

    #Returns a list of Primary Input vertices
    def findPIs(self) -> list:
        pi = []
        for v in self.vList:
            if v.PI:
                pi.append(v.label)
        return pi

    #Returns a list of all edges
    def getEdges(self) -> list:
        edges = []
        for v in self.vList:
            for e in v.adjList:
                edges.append(e.label)
        return edges

    #FOR TESTING: Prints the directed graph in text format
    def print(self) -> None:
        for v in self.vList:
            if not v.PI:
                print(v.label + ', ' + v.getGate() + '->', end=' ')
            else:
                print(v.label + '->', end=' ')
            for e in v.adjList:
                print(e.end + ', ', end='')
            print('\n')

    #Prints a primary output's value
    def printOutput(self) -> None:
        for v in self.vList:
            if v.PO == True:
                print(v.outputValue)

    #This function performs fault collapsing: any two PIs connected to a gate will remove the equivalent
        #s-a-0 or s-a-1 fault
    def faultCollapse(self) -> None:
        before = 0
        endLabels = []
        dupList = []
        nullList = []

        for v in self.vList:
            if v.PI:
                for e in v.adjList:
                    if e.end not in nullList:
                        nullList.append(e.end)
                    else:
                        dupList.append(e.end)
        if len(dupList) != 0:
            for x in dupList:
                endLabels.append(x)

        for i, v in enumerate(self.vList):
            if v.PI:
                for e in v.adjList:
                    before += len(e.faultList)
                    u = self.vList[i + 1]
                    if u.PI:
                        for f in u.adjList:
                            if e.end == f.end:
                                if e.end not in endLabels:
                                    endLabels.append(e.end)
        
        print('Faults before collapsing: {}'.format(before))
        print(endLabels)
        after = before

        for v in self.vList:
            if v.PI:
                if len(endLabels) == 0:
                    continue
                for e in v.adjList:
                    if e.end != endLabels[0]:
                        continue
                    else:
                        nextV = self.vList[self.findVertex(endLabels.pop(0))]
                        if nextV.gate == 0:
                            e.faultList.pop(0) #Remove s-a-0
                            after -= 1
                        elif nextV.gate == 1:
                            e.faultList.pop(1) #Remove s-a-1
                            after -= 1
                        elif nextV.gate == 2:
                            e.faultList.pop(0) #Remove s-a-0
                            after -= 1
                        elif nextV.gate == 3:
                            e.faultList.pop(1) #Remove s-a-1
                            after -= 1
                        break
        
        print('Faults after collapsing: {}'.format(after))

    #This function prints the faults stored on an each edge of the PIs
    def printFaults(self) -> None:
        for v in self.vList:
            if v.PI:
                for e in v.adjList:
                    print(e.label + ': ', end='')
                    for fault in e.faultList:
                        print(fault + ' ', end='')
                    print('')    

    #This function simulates a circuit using values in1 and in2 stored in each vertex and provides an output value
    #This function uses 2 for D and 3 for D'.
    def simulateCircuit(self) -> list:
        verticies = []
        outputs = []
        for v in self.vList:
            if v.PI:
                for e in v.adjList:
                    nextV = self.vList[self.findVertex(e.end)]
                    if nextV.in1 == -1:
                        nextV.in1 = v.outputVal
                        #print('Updated ' + nextV.label + ' in1 with value ' + strng(nextV.in1))
                    else:
                        nextV.in2 = v.outputVal
                        #print('Updated ' + nextV.label + ' in2 with value ' + strng(nextV.in2))
                    if not (nextV in verticies):
                        verticies.append(nextV)

        
        while len(verticies) != 0:
            v = verticies.pop(0)
            if v.gate == 4:
                if v.in1 == -1:
                    verticies.append(v)
                    continue
            else:
                if v.in1 == -1:
                    verticies.append(v)
                    continue   
                if v.in2 == -1: 
                    verticies.append(v)
                    continue  
            
            if v.gate == 0: #NAND
                if v.in1 > 1 or v.in2 > 1: #If one of the inputs is D or D'
                    if v.in1 == 2:
                        if v.in2 == 0:
                            v.outputVal = 1
                        elif v.in2 == 1:
                            v.outputVal = 3
                        elif v.in2 == 2:
                            v.outputVal = 3
                        else:
                            v.outputVal = 1
                    elif v.in1 == 3:
                        if v.in2 == 0:
                            v.outputVal = 1
                        elif v.in2 == 1:
                            v.outputVal = 2
                        elif v.in2 == 2:
                            v.outputVal = 1
                        else:
                            v.outputVal = 2
                    elif v.in2 == 2:
                        if v.in1 == 0:
                            v.outputVal = 1
                        elif v.in1 == 1:
                            v.outputVal = 3
                        elif v.in1 == 2:
                            v.outputVal = 3
                        else:
                            v.outputVal = 1
                    elif v.in2 == 3:
                        if v.in1 == 0:
                            v.outputVal = 1
                        elif v.in1 == 1:
                            v.outputVal = 2
                        elif v.in1 == 2:
                            v.outputVal = 1
                        else:
                            v.outputVal = 2
                else:
                    temp = v.in1 & v.in2
                    if temp == 0:
                        v.outputVal = 1
                    else:
                        v.outputVal = 0
            elif v.gate == 1: #NOR
                if v.in1 > 1 or v.in2 > 1:
                    if v.in1 == 2:
                        if v.in2 == 0:
                            v.outputVal = 3
                        elif v.in2 == 1:
                            v.outputVal = 0
                        elif v.in2 == 2:
                            v.outputVal = 3
                        else:
                            v.outputVal = 0
                    elif v.in1 == 3:
                        if v.in2 == 0:
                            v.outputVal = 2
                        elif v.in2 == 1:
                            v.outputVal = 0
                        elif v.in2 == 2:
                            v.outputVal = 0
                        else:
                            v.outputVal = 2
                    elif v.in2 == 2:
                        if v.in1 == 0:
                            v.outputVal = 3
                        elif v.in1 == 1:
                            v.outputVal = 0
                        elif v.in1 == 2:
                            v.outputVal = 3
                        else:
                            v.outputVal = 0
                    elif v.in2 == 3:
                        if v.in1 == 0:
                            v.outputVal = 2
                        elif v.in1 == 1:
                            v.outputVal = 0
                        elif v.in1 == 2:
                            v.outputVal = 0
                        else:
                            v.outputVal = 2
                else:
                    temp = v.in1 | v.in2
                    if temp == 0:
                        v.outputVal = 1
                    else:
                        v.outputVal = 0
            elif v.gate == 2: #AND
                if v.in1 > 1 or v.in2 > 1:
                    if v.in1 == 2:
                        if v.in2 == 0:
                            v.outputVal = 0
                        elif v.in2 == 1:
                            v.outputVal = 2
                        elif v.in2 == 2:
                            v.outputVal = 2
                        else:
                            v.outputVal = 0
                    elif v.in1 == 3:
                        if v.in2 == 0:
                            v.outputVal = 0
                        elif v.in2 == 1:
                            v.outputVal = 3
                        elif v.in2 == 2:
                            v.outputVal = 0
                        else:
                            v.outputVal = 3
                    elif v.in2 == 2:
                        if v.in1 == 0:
                            v.outputVal = 0
                        elif v.in1 == 1:
                            v.outputVal = 2
                        elif v.in1 == 2:
                            v.outputVal = 2
                        else:
                            v.outputVal = 0
                    elif v.in2 == 3:
                        if v.in1 == 0:
                            v.outputVal = 0
                        elif v.in1 == 1:
                            v.outputVal = 3
                        elif v.in1 == 2:
                            v.outputVal = 0
                        else:
                            v.outputVal = 3
                else:
                    v.outputVal = v.in1 & v.in2
            elif v.gate == 3: #OR
                if v.in1 > 1 or v.in2 > 1:
                    if v.in1 == 2:
                        if v.in2 == 0:
                            v.outputVal = 2
                        elif v.in2 == 1:
                            v.outputVal = 1
                        elif v.in2 == 2:
                            v.outputVal = 2
                        else:
                            v.outputVal = 1
                    elif v.in1 == 3:
                        if v.in2 == 0:
                            v.outputVal = 3
                        elif v.in2 == 1:
                            v.outputVal = 1
                        elif v.in2 == 2:
                            v.outputVal = 1
                        else:
                            v.outputVal = 3
                    elif v.in2 == 2:
                        if v.in1 == 0:
                            v.outputVal = 2
                        elif v.in1 == 1:
                            v.outputVal = 1
                        elif v.in1 == 2:
                            v.outputVal = 2
                        else:
                            v.outputVal = 1
                    elif v.in2 == 3:
                        if v.in1 == 0:
                            v.outputVal = 3
                        elif v.in1 == 1:
                            v.outputVal = 1
                        elif v.in1 == 2:
                            v.outputVal = 1
                        else:
                            v.outputVal = 3
                else:
                    v.outputVal = v.in1 | v.in2
            elif v.gate == 4: #NOT
                if v.in1 == 0:
                    v.outputVal = 1
                elif v.in1 == 1:
                    v.outputVal = 0
                elif v.in1 == 2:
                    v.outputVal = 3
                else:
                    v.outputVal = 2
    
            for e in v.adjList:
                nextV = self.vList[self.findVertex(e.end)]
                if nextV.in1 == -1:
                    nextV.in1 = v.outputVal
                    #print('Updated ' + nextV.label + ' in1 with value ' + str(nextV.in1))
                else:
                    nextV.in2 = v.outputVal
                    #print('Updated ' + nextV.label + ' in2 with value ' + str(nextV.in2))
                if not (nextV in verticies):
                    verticies.append(nextV)

        for v in self.vList:
            if v.PO:
                outputs.append(v.outputVal)
        
        return outputs

    def convertBool(self)-> None:
        a = Bool('a')
        b = Bool('b')
        count = 0
        li = []
        gateAmount = 0

        for v in reversed(self.vList):#first check for last gate with has output for circuit
            #going in reverse to find an input vector
            if(v.getGate() == 'AND'):
                f1 = And(a,b)
                gateAmount += 1
            elif(v.getGate() == 'OR'):
                f1 = Or(a,b)
                gateAmount += 1
            elif(v.getGate() == 'NAND'):
                f1 = Not(And(a,b))
                gateAmount += 1
            elif(v.getGate() == 'NOR'):
                f1 = Not(Or(a,b))
                gateAmount += 1
            elif(v.getGate() == 'NOT'):
                f1 = Not(a)
                li.append(str(v_a))
                li.append(str(v.getGate()))
            if not v.PI:
                s = Solver()
                s.add(f1)
                if(v.getGate() == 'AND'):
                    while s.check() == sat:#check for satisfiability, all possible inputs to achieve 1
                        m = s.model()
                        v_a = m.evaluate(a, model_completion=True)#initial gates
                        v_b = m.evaluate(b, model_completion=True)
                        li.append(str(v_a))
                        li.append(str(v_b))
                        bc = And(a != v_a, b != v_b)#add other gates
                        s.add(bc)
                    li.append(str(v.getGate()))
                elif(v.getGate() == 'OR'):
                    while s.check() == sat:#check for satisfiability, all possible inputs to achieve 1
                        m = s.model()
                        v_a = m.evaluate(a, model_completion=True)#initial gates
                        v_b = m.evaluate(b, model_completion=True)
                        li.append(str(v_a))
                        li.append(str(v_b))
                        bc = Or(a != v_a, b != v_b)#add other gates
                        s.add(bc)
                    li.append(str(v.getGate()))
                elif(v.getGate() == 'NAND'):
                    tried = 0
                    while s.check() == sat:#check for satisfiability, all possible inputs to achieve 1
                        m = s.model()
                        v_a = m.evaluate(a, model_completion=True)#initial gates
                        v_b = m.evaluate(b, model_completion=True)
                        li.append(str(v_a))
                        li.append(str(v_b))
                        if tried == 1:
                            bc = Or(a != v_a, b != v_b)#in order to get all possible inputs to output for NAND an OR was used
                        else:
                            bc = Or(a != v_b, b != v_a)
                        s.add(bc)
                        if tried == 2:#to stop infinite running code
                            break
                        tried += 1
                    li.append(str(v.getGate()))
                elif(v.getGate() == 'NOR'):
                    while s.check() == sat:#check for satisfiability, all possible inputs to achieve 1
                        m = s.model()
                        v_a = m.evaluate(a, model_completion=True)#initial gates
                        v_b = m.evaluate(b, model_completion=True)
                        li.append(str(v_a))
                        li.append(str(v_b))
                        bc = Not(Or(a != v_a, b != v_b))#add other gates
                        s.add(bc)
                        break
                    li.append(str(v.getGate()))

        #this is needed to fix the way gates were inputted
        li.insert(0, li.pop())#removes last from end of list to put at beginning. this should be the last gate which should output 1 for satisfaibility
        count = 0
        for x in reversed(li):
            if(x == 'AND') or (x == 'OR') or (x == 'NAND') or (x == 'NOR') or (x == 'NOT'):
                break
            else:
                count += 1
        while count != 0:
            li.insert(0, li.pop())
            count -= 1
        print("Possible assignments per gate:\n", li)

        return li

                
    #NEEDS to be FINISHED
    def processDAlg(self, dFrontier, jFrontier):
        insertJ = []
        count = 0
        g = ""
        if (dFrontier == None): 
            return 0
        #propagate fault to PO
        for v in self.vList:
            for e in v.adjList:
                if v.label[len(v.label)-1] == e.faultList:
                    while count != len(dFrontier): 
                        g = dFrontier[count] 
                        jFrontier.append(g)#recursion
                        result = self.processDAlg(dFrontier, jFrontier) 
                        count += 1 
                    if result == 1:
                        return 1 
                    return 0 

        if jFrontier == None: 
            return 1

        for i in range(len(jFrontier)-1):
            if(jFrontier[i] != None):
                g = jFrontier[i] 
        while (g or None) != g:
            j = g
            for j in range(len(jFrontier)-1):
                insertJ.append(jFrontier[j])
            result = self.processDAlg(dFrontier, jFrontier) 
            if result == 1:
                return 1
            else:
                j = O 

        return 0
