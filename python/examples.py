import random
import time
import argparse


def identity(x):
    return x


if __name__ == "__main__":
    # Set up argument parser
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-mpi", action="store_true", help="Use MPI to parallelize")
    argparser.add_argument("-parmap", action="store_true", help="Use parmap to parallelize")
    argparser.add_argument("-n", type=int, default=None, help="Number of cores for parmap")

    # Parse arguments
    args = argparser.parse_args()
    if args.mpi and args.parmap:
        raise ValueError("Cannot use both MPI and parmap")
    if not args.mpi and not args.parmap:
        try:
            from mpi4py import MPI
            if MPI.COMM_WORLD.Get_size() > 1:
                args.mpi = True
        except ImportError:
            pass
        if not args.mpi:
            args.parmap = True

    # use MPI to parallelize
    if args.mpi:
        from mpi4py import MPI
        try:
            from mpimap import mpimap
        except ImportError:
            raise ImportError("Cannot import mpimap. Make sure it is in the PYTHONPATH.")

        comm = MPI.COMM_WORLD
        my_rank = comm.Get_rank()

        def func(x):
            t = random.random()
            print("Rank {:02d} sleeping for {:.3f} on task {:02d}".format(my_rank, t, x))
            time.sleep(random.random())
            return identity(x)

        print("Rank", my_rank, "starting")
        out = mpimap(func, range(4 * comm.Get_size()), keep_results=True)
        if my_rank == 0:
            print("\nOutcome:")
            print(out)

    # use parmap to parallelize
    if args.parmap:
        import multiprocessing as mp
        try:
            from parmap import parmap
        except ImportError:
            raise ImportError("Cannot import parmap. Make sure it is in the PYTHONPATH.")

        if args.n is None:
            args.n = mp.cpu_count()

        out = parmap(identity, range(4 * args.n), nprocs=args.n)
        print("\nOutcome:")
        print(out)
