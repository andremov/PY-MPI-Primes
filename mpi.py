import numpy as np
import math
from mpi4py import MPI
import time

start_time = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

arr = [0]
data = np.array([0,0])
c = 0
if rank == 0:

    print('Digite K')
    k = int(input())
    enum = math.ceil(k/(size-1))
    print('e ',enum)
    
    encargado = 1
    missing = k-1
    for x in range(2, k):
        comm.Send([np.array([x,min(enum, missing)]), MPI.INT], dest=encargado, tag=encargado)
        
        if x%enum == 0:
            missing = missing - enum
            encargado = encargado + 1

    encargado = 1
    for n in range(2,k):
        comm.Recv([data, MPI.INT], source=encargado, tag=n)
        arr.append(data[1])
        c = c + data[0]

        encargado = encargado + 1

        if encargado%size == 0:
            encargado = 1

    end_time = time.time()

    print('validaciones >', arr)
    print('primos >', c)
    print('tiempo de exec > ', end_time-start_time)
else:
    cur = 0
    maxN = 1
    while cur < maxN:
        comm.Recv([data, MPI.INT], source=0, tag=rank)

        p = data[0]
        cur = cur + 1
        maxN = data[1]

        esPrimo = 1
        val = 0
        for n in range(2,math.ceil(p/2)+1):
            val = val + 1
            if p%n == 0:
                esPrimo = 0
                break

        data[0] = esPrimo
        data[1] = val
        comm.Send([data, MPI.INT], dest=0, tag=p)