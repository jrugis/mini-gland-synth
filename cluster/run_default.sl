#!/usr/bin/env bash
#SBATCH --time=00-00:50:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=3GB

echo "hostname: $HOSTNAME"
echo "task array id: $SLURM_ARRAY_TASK_ID"

# load environment modules
ml purge 2> /dev/null
ml BlenderPy/.2.93.1-gimkl-2020a-Python-3.9.5

# activate the virtual environment
VENV_PATH=/nesi/project/nesi00119/mini-gland-synth-venv
source ${VENV_PATH}/bin/activate

# directory associated with job array
job_dir=$( head -n $SLURM_ARRAY_TASK_ID dirs.txt | tail -1 )
echo "job dir: $job_dir"
cd $job_dir

python3 _create_mini_gland.py
