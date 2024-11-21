'''
import Circuit

c1 = Circuit.Circuit()

#Primary Inputs
c1.addVertex('gat1', 1)
c1.addVertex('gat2', 0)
c1.addVertex('gat3', 1)

c1.addVertex('gat4',

print(c1.numVertices)
c1.print()
'''
file = open('t6_24.ckt', 'r')

for line in file:
    if line[0] == '$':
        continue
    print(line, end='')

#for line in file:
#    print(line)