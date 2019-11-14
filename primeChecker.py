import sys
from mpi4py import MPI

comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process

print("Proceso verificador ! ", rank, " con argumento ", sys.argv[1])

