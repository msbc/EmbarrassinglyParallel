from mpi4py import MPI
import numpy as np

_null = randNum = np.zeros(1)


class MPIMap:
    def __init__(self, func, iterable, comm=None, keep_results=True, mpi_init=False):
        if mpi_init:
            MPI.Init()
        self.comm = comm if comm is not None else MPI.COMM_WORLD
        self.func = func
        self.iterable = iterable
        self.ntasks = len(iterable)
        self.size = self.comm.Get_size()
        self.rank = self.comm.Get_rank()
        self.waiting = np.ones(self.ntasks, dtype=bool)
        self.mine = np.zeros(self.ntasks, dtype=bool)
        self.result = [None] * self.ntasks if keep_results else None
        self.keep_results = keep_results
        self._wait = 0

    def __call__(self):
        # Sync up
        self.comm.barrier()
        # Distribute initial tasks
        task = self.rank
        # Loop over tasks
        while task < self.ntasks:
            if self.comm.Iprobe(source=MPI.ANY_SOURCE, tag=task + self._wait):
                self.comm.Irecv(_null, source=MPI.ANY_SOURCE, tag=task + self._wait)
                self.waiting[task] = False
            else:
                self.mine[task] = True
                self.waiting[task] = False
                # tell other ranks I'm working on this task
                for i in range(self.size):
                    if i != self.rank:
                        self.comm.Isend(_null, dest=i, tag=task + self._wait)
                # Do the work
                out = self.func(self.iterable[task])
                if self.keep_results:
                    self.result[task] = out
            # find next task
            while not self.waiting[task]:
                task += 1
                if task >= self.ntasks:
                    break
                if self.comm.Iprobe(source=MPI.ANY_SOURCE, tag=task + self._wait):
                    self.comm.Irecv(_null, source=MPI.ANY_SOURCE, tag=task + self._wait)
                    self.waiting[task] = False
        # Sync up
        self.comm.barrier()
        if not self.keep_results:
            return
        owners = np.ones(self.ntasks, dtype=int) * -1
        owners[self.mine] = self.rank
        out = np.empty_like(owners)
        self.comm.Allreduce([owners, MPI.INT], [out, MPI.INT], op=MPI.MAX)
        for i in range(self.ntasks):
            self.result[i] = self.comm.bcast(self.result[i], root=out[i])
        return self.result


def mpimap(func, iterable, comm=None, keep_results=True):
    return MPIMap(func, iterable, comm=comm, keep_results=keep_results)()
