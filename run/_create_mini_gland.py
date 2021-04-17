# -*- coding: utf-8 -*-
#
# Wrapper script for creating parotid mini-gland meshes.
#
# J.rugis
# 30.03.2021
#
import subprocess
import time

#-------------------------------------------------------------------------------
# function definitions
#-------------------------------------------------------------------------------
def sys_call(cmd):
  sp = subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
  if sp.returncode != 0:
    print("ERROR:", sp)
    exit()
  return

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

start = time.time()

#-----------------------------
# use blender module to create meshes
print("creating striated duct meshes...")
sys_call("rm -f Cell*.ply")
sys_call("python3.9 _mini_gland_striated_duct.py")

#-----------------------------
# convert meshes to image stack (ply -> tiff)
#print("converting meshes to tiff stack...")
#sys_call("python3.7 _ply2stack.py")
#sys_call("rm -f *.ply")

#-----------------------------
# process the image stack (tiff -> inr)

#-----------------------------
# convert image stack to conformal volumetric mesh (inr -> mesh)

#-----------------------------
# convert volumetric mesh format (mesh -> custom_ply) 

#-----------------------------

end = time.time()
print(time.strftime("run time %H:%M:%S", time.gmtime(end-start)))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
