import numpy as np
from mpi4py import MPI
import isPrimeScript

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()


c = 0

if rank == 0:

    pkg = np.array([4])
    comm.Send([pkg, MPI.INT], dest=1, tag=1)

    data = np.array([0])
    comm.Recv([data, MPI.INT], source=1, tag=2)

    print('primos >', data)

else:
    data = np.array([0])
    comm.Recv([data, MPI.INT], source=0, tag=1)

    number = data[0]

    res = np.array([1 if isPrimeScript.isPrime(number) else 0])
    comm.Send([res, MPI.INT], dest=0, tag=2)
