#!/usr/bin/env bash
#SBATCH --time=00-00:20:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=1GB
#SBATCH --output slurm_logs/%A-%a-%x.out
#SBATCH --error slurm_logs/%A-%a-%x.err
#SBATCH --array=1-10

# load environment modules
ml purge
ml Singularity/3.7.1

time singularity exec -B $PWD blender.sif python3 _mini_gland_striated_duct.py
