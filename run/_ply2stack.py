# -*- coding: utf-8 -*-
#
# Convert initial ply files to image stack.
#
# J.rugis
# 01.04.2021
#
import glob as gb
import pyvista as pv
import numpy as np
import tifffile as tif

#-------------------------------------------------------------------------------
# global constants
#-------------------------------------------------------------------------------

PIXEL_SIZE = 0.4

#-------------------------------------------------------------------------------
# function definitions
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#-----------------------------
# get a list of all the cell ply files
#-----------------------------
flist = sorted(gb.glob("Cell_???.ply", recursive=False))

#-----------------------------
# get extents over all cells, create a positive octant translation vector
#-----------------------------
vmin = np.full(3, 1000.0)   # lower bound coordinates
vmax = np.full(3, -1000.0)  # upper ...
for fname in flist:
  surface = pv.read(fname)
  vmin = np.amin(np.array([vmin, np.array(surface.bounds)[[0,2,4]]]), axis=0)
  vmax = np.amax(np.array([vmax, np.array(surface.bounds)[[1,3,5]]]), axis=0)
vrange = vmax - vmin           # extents vector
trans = -vmin + PIXEL_SIZE/2.0 # translation vector

#-----------------------------
# voxelize each cell and merge it into an image pixel array 
#-----------------------------

# create a blank image array sized by the extents vector (plus edge padding)
image = np.zeros(tuple(np.around(vrange/PIXEL_SIZE).astype(int) + 3), 'uint16') 

# iterate through the cell files
for fname in flist:
  print(fname)
  surface = pv.read(fname)
  surface.translate(trans) # translate to positive quadrant

  # voxelize the surface mesh
  voxels = pv.voxelize(surface, density=PIXEL_SIZE)

  # get voxel centers mapped to indices into the image array
  centers = np.around(voxels.cell_centers().points / PIXEL_SIZE).astype(int)

  # color the image pixels for this cell by cell number
  for row in centers: image[tuple(row)] = 200 + int(fname[-7:-4]) 

# save the image
tif.imsave('stack.tif', np.swapaxes(image, 0, 2))

#voxels.plot(color=True, show_edges=True)


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#print(surface.bounds)
#surface.plot(show_edges=True)

#print(voxels.n_cells)
#print(voxels.cell_centers().points)
#voxels.plot(color=True, show_edges=True)

#print(centers.shape)
#print(np.amin(centers, axis=0))
#print(np.amax(centers, axis=0))

