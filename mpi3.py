import sys
import numpy as np
import math
from mpi4py import MPI
import isPrimeScript

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size % 2 == 0 or ((size - 1) / 3) % 1 != 0:
    print('Error en numero de procesos.')

print('Numero de procesos: ', size)

print("Proceso verificador ! ", rank, " con argumento ", sys.argv[1])

if rank == 0:

    maxK = sys.argv[1]

    arraySize = int(math.ceil((maxK/float(size-1))/float(2)))
    for i in range(1, size):
        comm.Send([np.array([maxK, arraySize]), MPI.INT], dest=i)

    primes = [2]

    res = np.empty([arraySize, 2], np.int32)
    check = np.array([0])
    missing = size - 1

    while missing > 0:
        comm.Recv([res, MPI.INT], tag=1)

        missing = missing - 1
        for p in range(0, arraySize):
            if res[p][1] == 1 and res[p][0] != 0:
                primes.append(res[p])

else:
    data = np.array([0, 0])
    comm.Recv([data, MPI.INT], source=0)

    jump = (size-1)*2
    cur = (2 * rank) + 1
    c = 0

    pr = np.empty([data[1], 2], np.int32)
    while cur < data[0]:
        pr[c][0] = cur
        pr[c][1] = 1 if isPrimeScript.isPrime(cur) else 0
        c = c + 1
        cur = cur + jump

    comm.Send([pr, MPI.INT], dest=0, tag=1)
