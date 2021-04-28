#!/usr/bin/env bash
#SBATCH --time=00-00:30:00
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
BLENDER_IMG=/nesi/project/nesi00119/riom/blender.sif

echo "creating striated duct meshes..."
time singularity exec -B $PWD "$BLENDER_IMG" python3 _create_mini_gland.py
