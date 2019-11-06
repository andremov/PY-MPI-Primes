import numpy as np
import math
import time

start_time = time.time()

print('Digite K')
k = int(input())

arr = [0]
val = 0
c = 0

for p in range(2, k):
    c = c + 1

    for n in range(2, int(math.ceil(p/2)+1)):
        val = val + 1
        if p%n == 0:
            c = c - 1
            break

    arr.append(val)
    val = 0


end_time = time.time()

print('validaciones >', arr)
print('primos >', c)
print('tiempo de exec > ', end_time-start_time)