#!/bin/bash
#SBATCH --job-name=two_tasks                     # create a short name for your job
#SBATCH --nodes=1                                # node count
#SBATCH --ntasks=2                               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1                        # cpu-cores per task (equal to $SLURM_CPUS_PER_TASK)
#SBATCH --mem=1G                                 # total cpu requested memory
#SBATCH --time=01:00:00                          # total run time limit (HH:MM:SS)

# This file was written by Rob Bierman


# set bash strict mode (http://redsymbol.net/articles/unofficial-bash-strict-mode/)
# -m is needed to use `fg` to foreground run1.py
set -euom pipefail

# create run1.py and run2.py that don't do much
printf "import time\nfor i in range(10):\n    print('py1',i,flush=True)\n    time.sleep(1)" > run1.py
printf "import time\nfor i in range(4) :\n    print('py2',i,flush=True)\n    time.sleep(1)" > run2.py

# start run1 in the background
python run1.py &

# wait for two seconds to give run1 a headstart
sleep 2

# start run2 in the background
python run2.py &

# bring run1 to the foreground so SLURM doesn't exit
# (when I didn't do this the job just stopped immediately)
# this outputs `python run1.py`
fg %1

# seems like the SLURM job will stop when the `python run1.py` finishes
# whether or not `python run2.py` finishes