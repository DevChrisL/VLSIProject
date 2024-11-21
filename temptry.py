from z3 import *
import driver
a = Bool('a')
b = Bool('b')
count - int("0")

for v in reversed(self.vList):#first check for last gate with has output for circuit
    if(v.getGate() == 'AND'):
        f1 = And(a,b)
    if(v.getGate() == 'OR'):
        f1 = Or(a,b)
    if(v.getGate() == 'NAND'):
        f1 = Not(And(a,b))
    if(v.getGate() == 'NOR'):
        f1 = Not(Or(a,b))
    if(v.getGate() == 'NOT'):
        f1 = Not(a)
    for e in v.adjList:
    s = Solver()
    s.add(f1)
    while s.check() == sat:#check for satisfability, also, all possible inputs to achieve 1
        m = s.model()
        v_a = m.evaluate(a, model_completion=True)#initial gates
        v_b = m.evaluate(b, model_completion=True)
        if(v.getGate() == 'AND'):
            bc = And(a != v_a, b != v_b)#add other gates
        if(v.getGate() == 'OR'):
            bc = Or(a != v_a, b != v_b)#add other gates
        if(v.getGate() == 'NAND'):
            bc = Not(And(a != v_a, b != v_b))#add other gates
        if(v.getGate() == 'NOR'):
            bc = Not(Or(a != v_a, b != v_b))#add other gates
            
        s.add(bc)

    if(str(v_a) == 'True') and (str(v_b) == 'False'):#test inputs return 1
        print("10", int(count), "\n")
        count+=1
    elif(str(v_a) == 'False') and (str(v_b) == 'False'):#test inputs return 1
        print("00", int(count), "\n")
        count+=1
    elif(str(v_a) == 'True') and (str(v_b) == 'True'):#test inputs return 1
        print("11", int(count), "\n")
        count+=1
    elif(str(v_a) == 'False') and (str(v_b) == 'True'):#test inputs return 1
        print("01", int(count), "\n")
        count+=1


        
    #if
        #print("possible inputs to output 1:")
        #print("a := " + str(v_a))
       # print("b := " + str(v_b))

        #bc = Or(a != v_a, b != v_b)#add other gates
       # s.add(bc)

      #  vit = iter(v)
       #         lit = iter(letters)            
     #           if(temp == e.end):
      #              if(v.getGate() == 'AND'):
    #                   z3(And(letters, lit))
    #            if not v.PI:
    #                print(v.label + ', ' + v.getGate() + '->', end=' ')
    #            else:
    #                print(v.label + '->', end=' ')
    #            for e in v.adjList:
    #                print(e.end + ', ', end='')
    #            print('\n')