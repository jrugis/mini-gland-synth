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

Note that you can specify the number of simulations using the `-n` or `--n-sims` options of `run_sim.py`.
For example, to run 2 simulations, use:
```
python run_sim.py -n 2 my_run_xxxx.sl my_params_xxxx.ini
```

Default values for the options of `run_sim.py` can be obtained using `-h` or `--help`:
```
python run_sim.py -h
```


## Build the Python virtual environment

The virtual environment is shared between users of the project and need to be
created only once:
```
module purge
module load BlenderPy/.2.93.1-gimkl-2020a-Python-3.9.5
VENV_PATH="/nesi/project/nesi00119/mini-gland-synth-venv"
python3 -m venv --system-site-packages "$VENV_PATH"
source "${VENV_PATH}/bin/activate"
pip install pyvista tifffile
deactivate
```