class Vertex:
    def __init__(self, label, gateType, primaryOut=False, primaryIn=False, output=0) -> None:
        self.label = label #Name of Vertex (gate)
        self.adjList = [] #List of edges tied to this gate
        self.gate = gateType #0 = NAND, 1 = NOR, 2 = AND, 3 = OR, 4 = NOT
        self.PO = primaryOut #Is this a PO?
        self.PI = primaryIn #Is this a PI?
        self.outputVal = output #Value to be put onto the next line (edge) connecting to the next gate (vertex)
        self.in1 = -1 #Input val 1
        self.in2 = -1 #Input val 2

    def getGate(self) -> str:
        if (self.gate == 0):
            return 'NAND'
        elif (self.gate == 1):
            return 'NOR'
        elif (self.gate == 2):
            return 'AND'
        elif (self.gate == 3):
            return 'OR'
        else:
            return 'NOT'