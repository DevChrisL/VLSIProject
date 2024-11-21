def calculateOutput(self, gate, in1, in2) -> int: 
        if (gate == 0):
            outputVal = ~(in1 & in2)
        elif (gate == 1):
            outputVal = ~(in1 | in2)
        elif (gate == 2):
            outputVal = in1 & in2
        else:
            outputVal = in1 | in2

        return outputVal