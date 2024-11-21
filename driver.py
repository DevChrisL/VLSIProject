#VLSI FINAL PROJECT, FALL 2022
#CHRISTOPHER LUEVANO , ANDREW SZYMANSKI, JESSE THOMPSON

import Circuit
import re #Regex used for parseNetlist
import random

c1 = Circuit.Circuit()

#Parses input NetList and makes a directed graph from it
def parseNetlist(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print('File not found.')
        return
    
    for line in file:
        if line[0] == '$' or not line.strip(): #Skip comments and blank lines
            continue
        if line.find('input') != -1: #Store inputs
            buffer = ''
            i = 0
            while line[i] != ' ' and line[i] != '\t':
                buffer += line[i]
                i += 1
            c1.addVertex(buffer)
        elif line.find('output') != -1: #Store outputs
            buffer = ''
            j = 0
            while line[j] != ' ' and line[j] != '\t':
                buffer += line[j]
                j += 1
            c1.addVertex(buffer, True)
        else:
            #Check if first gate listed is already a vertex:
                #If so, create an Edge from the two gates following TO this gate. Add the gate type to this gate
                #If not, create a new vertex with FALSE for PrimaryOutput, then perform above procedure
            words = re.findall(r'\w+', line) #Regex used to break the line into separate words
            if len(words) == 4:
                if c1.findVertex(words[2]) == -1:
                    c1.addVertex(words[2], False)
                if c1.findVertex(words[3]) == -1:
                    c1.addVertex(words[3], False)
                if c1.findVertex(words[0]) == -1:
                    if words[1].lower() == 'nand':
                        c1.addVertex(words[0], False)
                    elif words[1].lower() == 'nor':
                        c1.addVertex(words[0], False, 1)
                    elif words[1].lower() == 'and':
                        c1.addVertex(words[0], False, 2)
                    elif words[1].lower() == 'or':
                        c1.addVertex(words[0], False, 3)
                    c1.addEdge(words[2], words[0])
                    c1.addEdge(words[3], words[0])
                else:
                    if words[1].lower() == 'nand':
                        c1.changeGate(words[0], 0)
                    elif words[1].lower() == 'nor':
                        c1.changeGate(words[0], 1)
                    elif words[1].lower() == 'and':
                        c1.changeGate(words[0], 2)
                    elif words[1].lower() == 'or':
                        c1.changeGate(words[0], 3)
                    c1.addEdge(words[2], words[0])
                    c1.addEdge(words[3], words[0])
            else:
                if c1.findVertex(words[2]) == -1:
                    c1.addVertex(words[2], False)
                if c1.findVertex(words[0]) == -1:
                    c1.addVertex(words[0], False, 4)
                    c1.addEdge(words[2], words[0])
                else:
                    c1.changeGate(words[0], 4)
                    c1.addEdge(words[2], words[0])
    file.close()
    print('File successfully parsed!')

#This function sets up simulation. A fault can be placed on one of the input lines and, if propagated through to the primary output, will be displayed
    #Otherwise, this function simulates a circuit normally with a given input vector
def simulate(input:str, faults:dict):
    if len(faults) == 0:
        pis = c1.findPIs()
        for i, name in enumerate(pis):
            c1.changeValue(name, int(input[i]))
        out = c1.simulateCircuit()
    else:
        pis = c1.findPIs()
        for i, name in enumerate(pis):
            if name in faults.keys():
                c1.changeValue(name, faults[name])
            else:
                c1.changeValue(name, int(input[i]))
        out = c1.simulateCircuit()
    print('Output(s): ', end='')
    for val in out:
        if val == 2:
            print('D', end=' ')
        elif val == 3:
            print('D\'', end=' ')
        else:
            print(val)
    print('')

#D-Algorithm Setup Function
def dAlgorithm(fault:dict):
    c2 = Circuit.Circuit()
    c2 = c1
    dFrontier = []
    jFrontier = []

    c2.xInputs()
    key = list(fault.keys())
    fEdge = key[0]
    f = fault[fEdge]

    words = re.findall(r'\w+', fEdge)
    
    c2.changeValue(words[0], f)
    dFrontier.append(words[2])
    jFrontier.append(words[2])
    c2.processDAlg(dFrontier, jFrontier)
    return


            

#User Menu
def main():
    while 1:
        print('--------------------------------------------------------------')
        print("[0] Read the input net-list\n[1] Perform fault collapsing \n[2] List fault classes")
        print("[3] Simulate \n[4] Generate tests (D-Algorithm)\n[5] Generate tests (Boolean satisfiability)\n[6] Exit \n[7] TEST PRINT")
        print('--------------------------------------------------------------')

        option = int(input("Please enter an option from the menu: "))

        if option == 0:
            c1.clear()
            inputFile = input('Enter the name of the Netlist file: ')
            parseNetlist(inputFile)
        elif option == 1:
            if c1.empty():
                print('No Netlist detected. Use input 0 to parse a Netlist first.')
                continue
            c1.faultCollapse()
        elif option == 2:
            if c1.empty():
                print('No Netlist detected. Use input 0 to parse a Netlist first.')
                continue
            c1.printFaults()
        elif option == 3:
            faults = {}
            if c1.empty():
                print('No Netlist detected. Use input 0 to parse a Netlist first.')
                continue
            pis = c1.findPIs()
            choice = int(input('Enter a fault set? Type 1 for yes, 0 for no: '))
            while choice < 0 or choice > 1:
                choice = int(input('Incorrect option. Type 1 for yes, 0 for no: '))
            while choice == 1:
                print('Primary Inputs: ')
                for i, v in enumerate(pis):
                    print(str(i + 1) + ': ' + v)
                x = int(input('Enter the number corresponding to the input to fault: '))
                while x < 0 or x > len(pis):
                    x = int(input('Incorrect input. Enter the number corresponding to the input to fault: '))
                pi = pis[x - 1]
                y = int(input('Set this fault to s-a-_ (Enter 0 or 1): '))
                while y < 0 or y > 1:
                    y = int(input('Incorrect input. Set this fault to s-a-_ (Enter 0 or 1): '))
                if y == 1:
                    Dval = 3 #D'
                else:
                    Dval = 2 #D
                faults[pi] = Dval
                choice = int(input('Add another fault? Type 1 for yes, 0 for no: '))
                while choice < 0 or choice > 1:
                    choice = int(input('Incorrect option. Type 1 for yes, 0 for no: '))
            vector = input('Enter a test vector of size {} (If fault was added, that input vector will be D or D\' regardless of vector input): '.format(len(pis)))
            while len(vector) != len(pis):
                vector = input('Incorrect vector size. Please enter a test vector of size {}: '.format(len(pis)))
            simulate(vector, faults)
        elif option == 4: 
            if c1.empty():
                print('No Netlist detected. Use input 0 to parse a Netlist first.')
                continue
            faultDict = {}
            edgeList = c1.getEdges()
            for i, e in enumerate(edgeList):
                print(str(i) + ': ' + e)
            choice1 = int(input('Type the number corresponding to the line to fault: '))
            while choice1 < 0 or choice1 >= len(edgeList):
                choice1 = int(input('Incorrect input. Type the number corresponding to the line to fault: '))
            choice2 = input('Type D or D\' to apply this fault to the chosen line: ')
            while choice2 != 'D' and choice2 != 'D\'':
                choice2 = input('Incorrect input. Type D or D\' to apply this fault to the chosen line: ')
            
            faultDict[edgeList[choice1]] = choice2
            dAlgorithm(faultDict)
        elif option == 5:
            if c1.empty():
                print('No Netlist detected. Use input 0 to parse a Netlist first.')
                continue
            liSat = []
            liSat = c1.convertBool()
            count1 = 0
            count2 = 0
            x = 0
            sum = 0
            out = 0
            value1 = 0
            vector = ""
            vector1 = 0
            for i in range(len(liSat)-1):
                j = i + 1
                if(liSat[j] == liSat[i]) and (liSat[i] == 'True') and (liSat[j+1] != 'OR'):
                    count1 += 1
                if(liSat[j] == 'AND') or (liSat[j] == 'OR') or (liSat[j] == 'NAND') or (liSat[j] == 'NOR'):
                    count2 += 1
            pis = c1.findPIs()
            n = len(pis)
            if(count1 == count2):#binary 1's
                while x < n:
                    sum += 2 ** x
                    x += 1
                vector = bin(sum).replace("0b", "")
                pis = c1.findPIs()
                for i, name in enumerate(pis):
                    c1.changeValue(name, int(vector[i]))
                out = c1.simulateCircuit()
                for value1 in out:
                    if value1 == 1:
                        print("Output: ",value1)
                if(value1 == 0):
                    n = count1
                    while value1 != 1:
                        for k in enumerate(pis):
                            temp = str(random.randint(0,1))
                            vector += temp
                        vector1 = type(vector)
                        pis = c1.findPIs()
                        for i, name in enumerate(pis):
                            c1.changeValue(name, int(vector[i]))
                        out = c1.simulateCircuit()
                        for value1 in out:
                            if value1 == 1:
                                print("Output: ",value1)
                    print(vector)
                else:
                    print("Working test vector: ", bin(sum).replace("0b", ""))
            else:#binary 0 and 1's
                n = count1
                while value1 != 1:
                    for k in enumerate(pis):
                        temp = str(random.randint(0,1))
                        vector += temp
                    vector1 = type(vector)
                    pis = c1.findPIs()
                    for i, name in enumerate(pis):
                        c1.changeValue(name, int(vector[i]))
                    out = c1.simulateCircuit()
                    for value1 in out:
                        if value1 == 1:
                            print("Output: ",value1)
                print("Working test vector: ", vector)
        elif option == 6:
            return
        elif option == 7:
            c1.print()
        else:
            print("Incorrect option")
    

main()