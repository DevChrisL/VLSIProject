import Circuit

def dInterceptOutput1(in1, in2): #AND
        if (in1 == 0) and (in2 == 0):
            outputVal = 0
        elif (in1 == 1) and (in2 == 1):
            outputVal = 1
        elif (in1 == x) and (in2 == x):
            outputVal = x
        elif (in1 == D) and (in2 == D):
            outputVal = D
        elif (in1 == Dbar) and (in2 == Dbar):
            outputVal = Dbar
        elif (in1 == 0) and (in2 == 1):
            outputVal = 0
        elif (in1 == 0) and (in2 == x):
            outputVal = 0
        elif (in1 == 0) and (in2 == D):
            outputVal = 0 
        elif (in1 == 0) and (in2 == Dbar):
            outputVal = 0 
        elif (in1 == 1) and (in2 == 0):
            outputVal = 0
        elif (in1 == 1) and (in2 == x):
            outputVal = x
        elif (in1 == 1) and (in2 == D):
            outputVal = D
        elif (in1 == 1) and (in2 == Dbar):
            outputVal = Dbar
        elif (in1 == x) and (in2 == 0):
            outputVal = 0
        elif (in1 == x) and (in2 == 1):
            outputVal = x
        elif (in1 == x) and (in2 == D):
            outputVal = x
        elif (in1 == x) and (in2 == Dbar):
            outputVal = x
        elif (in1 == D) and (in2 == 0):
            outputVal = D
        elif (in1 == D) and (in2 == 1):
            outputVal = D
        elif (in1 == D) and (in2 == x):
            outputVal = x
        elif (in1 == D) and (in2 == Dbar):
            outputVal = 0
        elif (in1 == Dbar) and (in2 == 0):
            outputVal = 0
        elif (in1 == Dbar) and (in2 == 1):
            outputVal = Dbar
        elif (in1 == Dbar) and (in2 == x):
            outputVal = x
        elif (in1 == Dbar) and (in2 == D):
            outputVal = 0

        return outputVal

def dInterceptOutput2(in1, in2): #OR
        if (in1 == 0) and (in2 == 0):
            outputVal = 0
        elif (in1 == 1) and (in2 == 1):
            outputVal = 1
        elif (in1 == x) and (in2 == x):
            outputVal = x
        elif (in1 == D) and (in2 == D):
            outputVal = D
        elif (in1 == Dbar) and (in2 == Dbar):
            outputVal = Dbar
        elif (in1 == 0) and (in2 == 1):
            outputVal = 1
        elif (in1 == 0) and (in2 == x):
            outputVal = x
        elif (in1 == 0) and (in2 == D):
            outputVal = D 
        elif (in1 == 0) and (in2 == Dbar):
            outputVal = Dbar 
        elif (in1 == 1) and (in2 == 0):
            outputVal = 1
        elif (in1 == 1) and (in2 == x):
            outputVal = 1
        elif (in1 == 1) and (in2 == D):
            outputVal = 1
        elif (in1 == 1) and (in2 == Dbar):
            outputVal = 1
        elif (in1 == x) and (in2 == 0):
            outputVal = x
        elif (in1 == x) and (in2 == 1):
            outputVal = 1
        elif (in1 == x) and (in2 == D):
            outputVal = x1
        elif (in1 == x) and (in2 == Dbar):
            outputVal = x
        elif (in1 == D) and (in2 == 0):
            outputVal = D
        elif (in1 == D) and (in2 == 1):
            outputVal = 1
        elif (in1 == D) and (in2 == x):
            outputVal = x
        elif (in1 == D) and (in2 == Dbar):
            outputVal = 1
        elif (in1 == Dbar) and (in2 == 0):
            outputVal = Dbar
        elif (in1 == Dbar) and (in2 == 1):
            outputVal = 1
        elif (in1 == Dbar) and (in2 == x):
            outputVal = x
        elif (in1 == Dbar) and (in2 == D):
            outputVal = 1

        return outputVal
        #convert to Dcube

#define d frontier and j frontier
def dFront():
    if(in1 == D) or (in1 == Dbar) or (in2 == D) or (in21 == Dbar):
        output = x

def jFront():
    if(output == 1) or (output == 0):
        in1 = in2 = x

#implemented psuedocode for d algorithm

def dAlgo(c):
    #if Imply_and_check() = FAILURE then return FAILURE     all values that can be uniquely determined by implication
                                                            #check for consistency and assign values
                                                            #maintain d frontier and j frontier
    if(out != fault):#fault not at primary output
        if(dFront == None):#d frontier equals null
            return 0
        while(dFront(gate) != None):#try all gates with d frontier
            dfront(gate)#pick random gate that has not been tried
            c = control(gate)#control value of gate 
            in1 = in2 = ~c #assign inputs as ~c for gate
            if(dAlgo == 1):
                return 1
        return 0
    
    elif(jFront == None):#error propagated through primary output
        return 1
    jFront(gate)
    c = control(gate)
    while(in1 != None) and (in2 != None):
        if(in1 == x):
            in1 = c
        elif(in2 == x):#input from j frontier
            in2 = c
        if(dAlgo == 1):
            return 1
        if(in1 == x):#reverse decision
            in1 = ~c
        elif(in2 == x):#input from j frontier
            in2 = ~c
    return 0
