import os
import re
import subprocess
import time

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# TODO add input parsing for slurm script
slurm = "/nesi/project/nesi00119/riom/mini-gland-synth/cluster/run_default.sl"

# TODO add input for parameters
n_sims = 20

# create the parameters sweep
sims = list(range(n_sims))

# create the top level results directory
run_dir = os.getcwd()
run_dir = re.sub("^/scale_wlg_persistent/filesets", "/nesi", run_dir)

assert "project" in run_dir, "Run directory should be on project filesystem"

results_dir = run_dir.replace("project", "nobackup", 1)
results_dir += "/results/" + time.strftime("%y%m%d_%H%M%S")

print("result dir:", results_dir)
os.system("mkdir -p " + results_dir)
os.chdir(results_dir)

# setup parameter sweep directories
with open("dirs.txt", "w") as f1:  # create parameters directory list file
  for s in sims:
    # create parameter directory
    parm_dir = results_dir + f"/simulation-{s:04}"
    os.mkdir(parm_dir)
    os.chdir(parm_dir)
    f1.write(parm_dir + "\n")

    # copy some files into parameter directory
    os.system("cp " + run_dir + "/../run/_create_mini_gland.py .")
    os.system("cp " + run_dir + "/../run/_mini_gland_striated_duct.py .")
    os.system("cp " + slurm + " ../run.sl")  # TODO put this out of the loop?
    os.chdir("..")

# submit slurm script for an array job
cmd = "sbatch --array=1-" + str(len(sims)) + " run.sl"
print(cmd)
job_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
