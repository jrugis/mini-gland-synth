# -*- coding: utf-8 -*-
#
# Wrapper script to create parotid mini-gland.
#
# Usage:
#  navigate to folder containing this file, then
#  python3 create_mini_gland.py
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

print("creating striated duct...")
os.system("python3 mini_gland_striated_duct.py >/dev/null 2>&1")

end = time.time()
print(time.strftime("run time %H:%M:%S", time.gmtime(end-start)))

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
