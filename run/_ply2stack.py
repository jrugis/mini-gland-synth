# -*- coding: utf-8 -*-
#
# Convert initial ply files to image stack.
#
# J.rugis
# 01.04.2021
#
import pyvista as pv
import numpy as np
import tifffile as tif

#-------------------------------------------------------------------------------
# global constants
#-------------------------------------------------------------------------------

PIXEL_SIZE = 0.1

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
flist = ["Cell_001.ply"]

#-----------------------------
# get extents over all cells, create a positive octant translation vector
#-----------------------------

vmin = np.zeros((1,3))
vmax = np.zeros((1,3))
for fname in flist:
  surface = pv.read(fname)
## MORE HERE
  vmin = np.array(surface.bounds)[[0,2,4]]
  vmax = np.array(surface.bounds)[[1,3,5]]

vrange = vmax - vmin
trans = -1.0 * vmin + PIXEL_SIZE/2.0

#-----------------------------
# voxelize each cell and merge it into an image pixel array 
#-----------------------------

# create a blank image array (with edge padding)
image = np.zeros(tuple(np.around(vrange/PIXEL_SIZE).astype(int) + 2), 'uint16') 

# iterate through the cell files
for fname in flist:
  surface = pv.read(fname)
  surface.translate(trans)

  # voxelize the surface mesh
  voxels = pv.voxelize(surface, density=PIXEL_SIZE)

  # get voxel centers as indices into the image array
  centers = np.around(voxels.cell_centers().points / PIXEL_SIZE).astype(int)

  # color image pixels by cell number
  for row in centers: image[tuple(row)] = int(fname[-7:-4]) 

# save the image
tif.imsave('stack.tif', image)


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

