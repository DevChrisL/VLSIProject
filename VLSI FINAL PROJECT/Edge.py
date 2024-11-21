class Edge:
    def __init__(self, label, initialV, destV) -> None:
        self.label = label #Name of Edge
        self.start = initialV #Staring gate
        self.end = destV #Destination gate
        self.faultList = [] #List of faults tied to this edge