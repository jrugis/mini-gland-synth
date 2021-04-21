import os
import subprocess
import time
import shutil
from pathlib import Path

# TODO add input parsing for slurm script
slurm = "/nesi/project/nesi00119/riom/mini-gland-synth/cluster/run_default.sl"

# TODO add input for parameters
n_sims = 20

# create the parameters sweep
sims = list(range(n_sims))

# create the top level results directory
repo_dir = Path(__file__).absolute().parent.parent
print("repo dir:", repo_dir)

assert "project" in repo_dir.parts, "Repository should be on project filesystem"

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

        # copy some files into parameter directory
        shutil.copy(run_dir / "_create_mini_gland.py", param_dir)
        shutil.copy(run_dir / "_mini_gland_striated_duct.py", param_dir)

# copy the SLURM script and submit it as array job
shutil.copy(slurm, results_dir / "run.sl")
os.chdir(results_dir)

cmd = "sbatch --array=1-" + str(len(sims)) + " run.sl"
print(cmd)
job_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
