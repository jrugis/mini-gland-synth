import os
import sys
import subprocess
import time
import shutil
import argparse
from pathlib import Path

# get input from the command line
parser = argparse.ArgumentParser(
    description="Generate a set of meshes.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument("slurm_script", type=Path, help="SLURM script to use")
parser.add_argument("params_file", type=Path, help="parameters as a .ini file")
parser.add_argument(
    "-n", "--n-sims", type=int, default=20, help="number of simulations"
)
args = parser.parse_args()

if not args.slurm_script.is_file():
    print(f"File '{args.slurm_script}' not found.")
    sys.exit(1)

# create the parameters sweep
sims = list(range(args.n_sims))

# create the top level results directory
repo_dir = Path(__file__).absolute().parent.parent
print("repo dir:", repo_dir)

project_root = "/scale_wlg_persistent/filesets/project"
if not str(repo_dir).startswith(project_root):
    print("Repository should be on project filesystem.")
    sys.exit(1)

results_dir = Path("/scale_wlg_nobackup/filesets/nobackup", *repo_dir.parts[4:])
results_dir = results_dir / "results" / time.strftime("%y%m%d_%H%M%S")

print("result dir:", results_dir)
results_dir.mkdir(parents=True, exist_ok=True)

# setup parameter sweep directories and save the list in a file
with (results_dir / "dirs.txt").open("w") as f1:
    run_dir = repo_dir / "run"
    for s in sims:
        # create parameter directory
        param_dir = results_dir / f"simulation-{s:04}"
        param_dir.mkdir(parents=True, exist_ok=True)
        f1.write(str(param_dir) + "\n")

        # copy the parameters file
        shutil.copy(args.params_file, param_dir / "params.ini")

        # copy some files into parameter directory
        shutil.copy(run_dir / "_create_mini_gland.py", param_dir)
        shutil.copy(run_dir / "_mini_gland_striated_duct.py", param_dir)
        shutil.copy(run_dir / "_ply2ply.py", param_dir)
        shutil.copy(run_dir / "mini_gland_duct.ply", param_dir)

# copy the SLURM script and submit it as array job
shutil.copy(args.slurm_script, results_dir / "run.sl")
os.chdir(results_dir)

cmd = "sbatch --array=1-" + str(len(sims)) + " run.sl"
print(cmd)
job_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
