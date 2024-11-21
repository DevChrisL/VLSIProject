n = 5
i = 0
sum = 0
while i < n:
    sum += 2 ** i
    i += 1

print(bin(sum).replace("0b", ""))