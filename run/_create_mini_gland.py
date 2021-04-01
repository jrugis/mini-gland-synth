# -*- coding: utf-8 -*-
#
# Wrapper script for creating parotid mini-gland meshes.
#
# J.rugis
# 30.03.2021
#
import os
import time

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

start = time.time()

#-----------------------------
# use blender module to create meshes
print("creating striated duct meshes...")
os.system("rm -f *.ply") # delete any existing mesh files
os.system("/usr/local/bin/python3.9 _mini_gland_striated_duct.py >/dev/null 2>&1")

#-----------------------------
# convert meshes to image stack (ply -> tiff)

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
