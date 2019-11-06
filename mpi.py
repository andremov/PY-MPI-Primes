import numpy as np
import math
from mpi4py import MPI
import time
import isPrimeScript

start_time = time.time()

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

arr = [0]
res = []
data = np.array([0,0])
c = 0
if rank == 0:

    print('Digite K')
    k = int(input())
    k = (k/2)
    maxn = math.ceil(float(k)/(size-1))

    print('son', k, 'numeros')
    print('son ', size, ' procesos')
    print('son ', size-1, ' procesos esclavos')
    print('son ', maxn, ' numeros por proceso')

    arr = [2]
    curn = 3
    proc = 1
    while k > 0:
        arr.append(curn)
        curn = curn + 2
        k = k - 1

        if len(arr) >= maxn:
            print(arr)
            comm.Send([np.array([arr]), MPI.INT], dest=proc, tag=1)
            proc = proc + 1
            arr = []

    if k == 0 & len(arr) != 0:
        print(arr)
        comm.Send([np.array([arr]), MPI.INT], dest=proc, tag=1)
        proc = proc + 1
        arr = []


    for proc in range(1, size):
        comm.Recv([data, MPI.INT], source=proc, tag=2)
        res.append(data[1])

    end_time = time.time()

    print('primos >', res)
    print('tiempo de exec > ', end_time-start_time)
else:
    comm.Recv([data, MPI.INT], source=0, tag=1)



#    max = len(data[0])
 #   r = []
  #  for i in range(0, max):
   #     r.append(isPrimeScript.isPrime(data[0][i]))

    #comm.Send([np.array([data[0], r]), MPI.INT], dest=0, tag=2)

