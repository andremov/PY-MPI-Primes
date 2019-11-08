import numpy as np
import math
from mpi4py import MPI
import time
import isPrimeScript

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

arr = []
res = []
c = 0

if rank == 0:

    kjump = 100000

    print('Digite W en cientos de miles')
    kmax = int(input())
    kmax = kmax

    for ik in range(1, kmax+1):
        curk = ik * kjump

        for ix in range(1, size):
            curk = ik * kjump

            start_time = time.time()

            maxn = (curk - 2) / float(2)
            maxn = math.ceil(maxn) + 1
            maxn = math.ceil(maxn / ix)

            arr = [2]
            all = [2]
            k = 1
            proc = 1

            while (2*k)+1 <= curk:
                arr.append((2*k)+1)
                all.append((2*k)+1)
                k = k + 1

                if len(arr) >= maxn:
                    for i in range(0, len(arr)):
                        print('sent', arr[i])
                        req = comm.Send([np.array([arr[i], len(arr)]), MPI.INT], dest=proc, tag=i+1)

                    proc = proc + 1
                    arr = []

            if len(arr) != 0:
                for i in range(0, len(arr)):
                    print('sent', arr[i])
                    comm.Send([np.array([arr[i], len(arr)]), MPI.INT], dest=proc, tag=i+1)

                proc = proc + 1
                arr = []

            data = np.array([0])
            for n in range(0, len(all)):
                print('waiting for', all[n])
                comm.Recv([data, MPI.INT], tag=all[n])
                print('received', all[n])
                if data[0] == 1:
                    #print(all[n], ' si es primo, o eso me dicen')
                    res.append(all[n])

            end_time = time.time()

            print('primos >', res)
            print('primos >', np.sum(res))
            print('tiempo de exec > ', end_time-start_time)
            comm.Bcast([np.array([1]), MPI.INT], root=0, tag=0)

    print('done')
    comm.Bcast([np.array([0]), MPI.INT], root=0, tag=0)
else:
    data = np.array([0,0])
    i = 1
    while True:
        comm.Recv([data, MPI.INT], source=0, tag=i)

        i = i + 1

        if i == data[1]:
            i = 0

        if data[0] == 0 and i == 0:
            break

        comm.Send(
            [np.array(1 if isPrimeScript.isPrime(data[0]) else 0), MPI.INT],
            dest=0,
            tag=data[0]
        )
