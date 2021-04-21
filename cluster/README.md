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

Make sure to have Python loaded (could be put in .bash_profile):
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
submit the job:
```
python run_sim.py my_run_xxxx.sl
```
and monitor progress using:
```
squeue -u your_nesi_login
```