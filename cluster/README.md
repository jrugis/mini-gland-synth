# Synthesize a parotid mini-gland on Mahuika

Clone this repository in your folder on Mahuika:
```
cd /nesi/project/nesi00119/your_name
git clone https://github.com/jrugis/mini-gland-synth.git
```

Update the code to the latest version:
```
cd mini-gland-synth
git pull
```
or
```
cd mini-gland-synth
git fetch origin
git reset --hard origin/master
```


## Prerequisites

If Python 3 is not loaded, you can do it as follows (could be put in .bash_profile):
```
ml Python/3.8.2-gimkl-2020a
```


## Run

Adapt the SLURM script to your needs:
```
cd mini-gland-synth/cluster
cp run_default.sl my_run_xxxx.sl
nano my_run_xxxx.sl
```
and the parameters file:
```
cp ../run/params.ini my_params_xxxx.ini
nano my_params_xxxx.ini
```
submit the job:
```
python run_sim.py my_run_xxxx.sl my_params_xxxx.ini
```
and monitor progress using:
```
squeue -u your_nesi_login
```


## Build the Singularity image

The Singularity image has to be built on a computer where you have admin rights, as root access is needed.

Install [Singularity](https://sylabs.io/singularity/) then create the container using:
```
sudo singularity build blender.sif blender
```
This will download and compile Blender and all its dependencies to create a Python module.

Once it is finished, you should obtain a `blender.sif` file that you can upload on NeSI.

Don't forget to update the path to this image in your sbatch scripts.

*Note: at the time of writing (2021/04/29), building the image take 1h20min on a 8 cores / 2GHz laptop.*
