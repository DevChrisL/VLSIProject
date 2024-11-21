#when a circuit is read by program all wires should be initalized with s-a-0 and s-a-1 faults
#so these functions collapse the faults
def equivalentCollapse(in1, in2, self.gate):
     #either for loop in here or when calling
     #if loop in here we pass graph
    RemovefaultList1 = []
    if(self.gate == 0):#nand
        RemovefaultList1.append("s-a-0")#remove from inputs
    elif(self.gate == 1):#nor
        RemovefaultList1.append("s-a-1")
    elif(self.gate == 2):#and
        RemovefaultList1.append("s-a-0")
    elif(self.gate == 3):#or
        RemovefaultList1.append("s-a-1")
    else:#not?
        RemovefaultList1.append("s-a-1")

    return RemovefaultList1#prob good as array of strings since fault classes need to be displayed

def dominantCollapse(in1, in2, self.gate):#for loop here too probably
    RemovefaultList2 = []
    if(self.gate == 0):#nand
        RemovefaultList2.append("s-a-0")#input fault collapsed
        RemovefaultList2.append("s-a-0")#output fault collapsed
    elif(self.gate == 1):#nor
        RemovefaultList2.append("s-a-1")#input fault collapsed
        RemovefaultList2.append("s-a-1")#output fault collapsed
    elif(self.gate == 2):#and
        RemovefaultList2.append("s-a-0")#input fault collapsed
        RemovefaultList2.append("s-a-1")#output fault collapsed
    elif(self.gate == 3):#or
        RemovefaultList2.append("s-a-1")#input fault collapsed
        RemovefaultList2.append("s-a-0")#output fault collapsed
    else:#not?
        RemovefaultList2.append("s-a-1")#not sure about inverter

    return RemovefaultList2