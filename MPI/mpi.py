from mpi4py import MPI

def main():
    # 1. Inisialisasi communicator
    comm = MPI.COMM_WORLD
    
    # 2. Mendapatkan rank dan jumlah proses
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        # Proses 0 mengirim data ke proses lain
        data = 100
        for i in range(1, size):
            comm.send(data, dest=i, tag=0)
            print(f"Proses 0 mengirim {data} ke proses {i}")
    else:
        # Proses lain menerima data dari proses 0
        data = comm.recv(source=0, tag=0)
        print(f"Proses {rank} menerima {data} dari proses 0")

    # 3. Finalisasi MPI
    MPI.Finalize()

if __name__ == "__main__":
    main()