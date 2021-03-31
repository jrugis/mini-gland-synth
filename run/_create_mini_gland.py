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

print("creating striated duct meshes...")
os.system("rm -f *.ply") # delete any existing mesh files
os.system("python3 _mini_gland_striated_duct.py >/dev/null 2>&1")

end = time.time()
print(time.strftime("run time %H:%M:%S", time.gmtime(end-start)))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
