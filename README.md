# EmbarrassinglyParallel

The purpose of this project is to demonstrate different ways to parallelize a simple tasks that require no communication between the parallel processes, i.e. embarrassingly parallel tasks.

## Slurm

The `slurm` directory contains a simple example of how to submit a job to a SLURM managed cluster to perform an embarrassingly parallel task.

- `slurm/job_array.sbatch` is a SLURM script that submits a job array to the cluster to parallelize tasks.
- `slurm/two_process_example.sbatch` is a SLURM script that submits a singular job to the cluster to parallelize tasks using two cores. This file also allows for one task to be started first.

## Python

The `python` directory contains a simple example of how to parallelize a task using the `multiprocessing` and `mpi4py` modules in Python, and does not require a SLURM managed cluster.

- `python/examples.py` is a Python script shows how the below two files can be used to parallelize code.
- `python/parmap.py` is a Python script that demonstrates how to parallelize a task using the `multiprocessing` module, and has a `parmap` function that is similar to the `map` function in Python which can be easily imported into other codes. This script is designed to be run on a single node or a local environment.
- `python/mpimap.py` is a Python script that demonstrates how to parallelize a task using the `mpi4py` module. This script is designed to be run using the `mpirun` command (e.g. `mpirun python examples.py`), and can be used to parallelize a task across multiple nodes.
