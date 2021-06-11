#!/usr/bin/env bash
#SBATCH --time=00-00:50:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=3GB

echo "hostname: $HOSTNAME"
echo "task array id: $SLURM_ARRAY_TASK_ID"

# load environment modules
ml purge 2> /dev/null
ml Singularity/3.7.1

# directory associated with job array
job_dir=$( head -n $SLURM_ARRAY_TASK_ID dirs.txt | tail -1 )
echo "job dir: $job_dir"
cd $job_dir

# use blender module to create meshes
BLENDER_IMG=/nesi/project/nesi00119/containers/blender_build_20210429.sif

echo "launching singularity container..."
singularity exec -B $PWD "$BLENDER_IMG" python3 _create_mini_gland.py
