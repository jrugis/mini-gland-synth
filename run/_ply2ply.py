# -*- coding: utf-8 -*-
#
# Combine initial ply files into single custom ply file.
#
# J.rugis
# 17.04.2021
#
import glob as gb
import pyvista as pv
import numpy as np
from typing import NamedTuple

#-------------------------------------------------------------------------------
# global constants
#-------------------------------------------------------------------------------

OUT = "mini_gland.ply"
DUCT_IN = "mini_gland_duct.ply"

#-------------------------------------------------------------------------------
# class definitions
#-------------------------------------------------------------------------------

# duct segment structure
class sDSeg(NamedTuple): 
    node_in: int
    node_out: int
    inner_diameter: float
    outer_diameter: float
    duct_type: int

#-------------------------------------------------------------------------------
# function definitions
#-------------------------------------------------------------------------------

# get face type (apical, basal, basolateral) based on distance from duct center line
# NOTE: for now, duct needs to be centered on z-axis (simplifies calculations!)
def get_ftype(verts, id, od): # face vertices, duct inner diameter, duct outer diamter
  c = np.mean(verts, axis=0)
  d = np.sqrt(c[0]**2 + c[1]**2)
  if((d - id/2.0) < 1.0): return(0)    # apical
  elif((od/2.0 - d) < 1.0): return(2)  # basal
  else : return(1)                     # basolateral

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

#------------------------------------------------
# get cell ply files sorted list and summary data
#------------------------------------------------
flist = sorted(gb.glob("Cell*.ply", recursive=False))
ncells = len(flist)          # total number of cells
tnverts = 0                  # total number of vertices
tnfaces = 0                  # total number of faces
cell_dsegs = []              # duct segment for each cell
for fname in flist:
  cell_dsegs.append(int(fname.split('.')[-2].split('_')[-1]))
  mesh = pv.read(fname)
  tnverts += mesh.n_points
  tnfaces += mesh.n_faces

#------------------------------------------------
# get duct data from the duct ply file
#------------------------------------------------
dfile = open(DUCT_IN, "r")
for ln in dfile:
  if ln.startswith("element duct_node"): break
ndnodes = int(ln.split()[-1])       # number of duct nodes
for ln in dfile:
  if ln.startswith("element duct_segment"): break
ndsegs = int(ln.split()[-1])        # number of duct segments
for ln in dfile:
  if ln.startswith("end_header"): break
dnodes = []
for i in range(ndnodes):            # duct node data
  ln = dfile.readline()
  dnodes.append([float(s) for s in ln.split()])
dsegs = []                          # duct segment data
for i in range(ndsegs):
  ln = dfile.readline().split()
  dsegs.append(sDSeg(int(ln[0]), int(ln[1]), float(ln[2]), float(ln[3]), int(ln[4])))
dfile.close()

#------------------------------------------------
# write out a single consilidated custom ply file
#------------------------------------------------
pfile = open(OUT, "w")

# ---write out the file header
pfile.write("ply\n")
pfile.write("format ascii 1.0\n")
pfile.write("comment Mini-Gland mesh format 1.0\n")
pfile.write("element vertex " + str(tnverts) + "\n")
pfile.write("property float x\n")
pfile.write("property float y\n")
pfile.write("property float z\n")
pfile.write("element face " + str(tnfaces) + "\n")
pfile.write("property int v1\n")
pfile.write("property int v2\n")
pfile.write("property int v3\n")
pfile.write("property int face_type\n")
pfile.write("element tetrahedron 0\n")
pfile.write("property int v1\n")
pfile.write("property int v2\n")
pfile.write("property int v3\n")
pfile.write("property int v4\n")
pfile.write("element cell " + str(ncells) + "\n")
pfile.write("property list int int face_index\n")
pfile.write("property list int int tetrahedron_index\n")
pfile.write("element duct_node " + str(ndnodes) + "\n")
pfile.write("property float x\n")
pfile.write("property float y\n")
pfile.write("property float z\n")
pfile.write("element duct_segment " + str(ndsegs) + "\n")
pfile.write("property int vertex_in\n")
pfile.write("property int vertex_out\n")
pfile.write("property float inner_diameter\n")
pfile.write("property float outer_diameter\n")
pfile.write("property int duct_type\n")
pfile.write("property list int int cell_index\n")
pfile.write("end_header\n")

# --- write out the vertex data (all cells)
for fname in flist:
  mesh = pv.read(fname)
  for p in mesh.points:
    pfile.write("{:.2f} {:.2f} {:.2f}\n".format(*p))

# --- write out oriented face data (all cells)
pi_offset = 0  # point index offset
for i, fname in enumerate(flist):
  mesh = pv.read(fname)
  for pi in mesh.faces.reshape((-1,4))[:, 1:]:  # three indices per row
    # -- vertex indices
    pfile.write("{:d} {:d} {:d} ".format(*(pi+pi_offset)))
    # -- face type (from cell duct segments)
    d = dsegs[cell_dsegs[i]]
    pfile.write(str(get_ftype(mesh.points[pi], d.inner_diameter, d.outer_diameter)) + "\n")
  pi_offset += mesh.n_points

# ---write out oriented tetrahedron data (all cells)
# NOTE: no tets for now

# --- write out the cell data
fi_offset = 0  # face index offset
for fname in flist:
  # --- output the number faces in this cell
  pfile.write(str(mesh.n_faces) + " ")
  # -- output the face indices for this cell
  for i in range(mesh.n_faces):
    pfile.write(str(i + fi_offset) + " ") # the face indices increment over all the cells
  # --- output the number of tetrahedrons in this cell
  pfile.write("0")
  pfile.write("\n")
  fi_offset += mesh.n_faces 

# --- write out the duct node data
for n in dnodes:
  pfile.write("{:.2f} {:.2f} {:.2f}\n".format(*n))

# --- write out the duct segment data
for i, s in enumerate(dsegs):
  pfile.write("{:d} {:d} {:.2f} {:.2f} {:d} ".format(s.node_in, s.node_out, s.inner_diameter, s.outer_diameter, s.duct_type))
  icells = np.where(np.array(cell_dsegs) == i)
  pfile.write(str(len(icells[0])))
  for ic in icells[0]:
    pfile.write(" " + str(ic)) # the cell indices for this segment
  pfile.write("\n")

# --- done
pfile.close()

#------------------------------------------------

