# -*- coding: utf-8 -*-
#
# Convert initial ply files to image stack.
#
# J.rugis
# 01.04.2021
#
import pyvista as pv
import numpy as np
from tifffile import imsave

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

# get a list of all the cell ply files


#-----------------------------
# get extents over all cells, create a positive octant translation vector
fname = "Cell_001.ply"
surface = pv.read(fname)
#print(surface.bounds)
bounds = surface.bounds
trans = [-1.0*surface.bounds[0]+PIXEL_SIZE/2.0, -1.0*surface.bounds[2]+PIXEL_SIZE/2.0, -1.0*surface.bounds[4]+PIXEL_SIZE/2.0]

#-----------------------------
# voxelize each cell and merge it into an image pixel array 

image = np.zeros((512,512,512), 'uint16') # create a blank image array

fname = "Cell_001.ply"
surface = pv.read(fname)
surface.translate(trans)
#print(surface.bounds)
#cpos = surface.plot(show_edges=True)

voxels = pv.voxelize(surface, density=PIXEL_SIZE)
#print(voxels.n_cells)
#print(voxels.cell_centers().points)
voxels.plot(color=True, show_edges=True)

centers = np.around(voxels.cell_centers().points / PIXEL_SIZE).astype(int)
#print(centers.shape)
#print(np.amin(centers, axis=0))
#print(np.amax(centers, axis=0))

for row in centers: image[tuple(row)] = 200
imsave('stack.tif', image) # save the image

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#plotter = pv.Plotter(off_screen=True)
#plotter.add_mesh(mesh)
#plotter.show(screenshot="myscreenshot.png")

#-------------------------------------------------------------------------------

###############################################################################
#cpos = [(7.656346967151718, -9.802071079151158, -11.021236183314311),
# (0.2224512272564101, -0.4594554282112895, 0.5549738359311297),
# (-0.6279216753504941, -0.7513057097368635, 0.20311105371647392)]

#surface.plot(cpos=cpos, opacity=0.75)


###############################################################################
# Create a voxel model of the bounding surface
#voxels = pv.voxelize(surface, density=surface.length/200)

#p = pv.Plotter()
#p.add_mesh(voxels, color=True, show_edges=True, opacity=0.5)
#p.add_mesh(surface, color="lightblue", opacity=0.5)
#p.show(cpos=cpos)

###############################################################################
# We could even add a scalar field to that new voxel model in case we
# wanted to create grids for modelling. In this case, let's add a scalar field
# for bone density noting:
#voxels["density"] = np.full(voxels.n_cells, 3.65) # g/cc
#voxels

###############################################################################
#voxels.plot(scalars="density", cpos=cpos)

###############################################################################
# A constant scalar field is kind of boring, so let's get a little fancier by
# added a scalar field that varies by the distance from the bounding surface.
#voxels.compute_implicit_distance(surface, inplace=True)
#voxels

###############################################################################
#contours = voxels.contour(6, scalars="implicit_distance")

#p = pv.Plotter()
#p.add_mesh(voxels, opacity=0.25, scalars="implicit_distance")
#p.add_mesh(contours, opacity=0.5, scalars="implicit_distance")
#p.show(cpos=cpos)
