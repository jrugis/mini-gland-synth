#!/usr/bin/env bash
#SBATCH --time=00-00:20:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=1GB

echo $HOSTNAME
echo "task array id: $SLURM_ARRAY_TASK_ID"

# load environment modules
ml purge
ml Singularity/3.7.1

# directory associated with job array
job_dir=$( head -n $SLURM_ARRAY_TASK_ID dirs.txt | tail -1 )
echo $job_dir

cd $job_dir

# use blender module to create meshes
time singularity exec -B $PWD blender.sif python3 _mini_gland_striated_duct.py
