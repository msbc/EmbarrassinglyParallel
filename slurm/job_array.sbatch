#!/bin/bash
#SBATCH --job-name=job_array     # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes per job
#SBATCH --cpus-per-task=1        # cpu-cores per task per job (equal to $SLURM_CPUS_PER_TASK)
#SBATCH --time=00:01:00          # total run time limit (HH:MM:SS) per job
#SBATCH --output=slurm-%A.%a.out # stdout file
#SBATCH --error=slurm-%A.%a.err  # stderr file
#SBATCH --array=0-4              # job array with index values 0, 1, 2, 3, 4

echo "My SLURM_ARRAY_JOB_ID is $SLURM_ARRAY_JOB_ID."
echo "My SLURM_ARRAY_TASK_ID is $SLURM_ARRAY_TASK_ID"
echo "Executing on the machine:" $(hostname)

# run the python script with the task id as an argument
python square.py $SLURM_ARRAY_TASK_ID

# create a file based on the task id
if [ $SLURM_ARRAY_TASK_ID -eq 2 ]; then
    echo "echo Task 2 is special" > my_script_${SLURM_ARRAY_TASK_ID}.sh
fi

# run a script based on the task id
SCRIPT=my_script_${SLURM_ARRAY_TASK_ID}.sh
if [-f $SCRIPT]; then
    echo "Running $SCRIPT"
    bash $SCRIPT
else
    echo "No script $SCRIPT"
fi

# do something different based on the task id
case $SLURM_ARRAY_TASK_ID in
    0) echo "First task done";;
    1) echo "Second task done";;
    2) echo "Third task done";;
    3) echo "Fourth task done";;
    4) echo "Fifth task done";;
    *) echo "Task not recognized";;
esac
