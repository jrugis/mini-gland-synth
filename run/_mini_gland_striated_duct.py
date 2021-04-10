# -*- coding: utf-8 -*-
#
# Sets up and runs a Blender animation to "grow" parotid gland cells around (and within) duct constraints.
#
# J.rugis
# 30.03.2021
#
import bpy
import bmesh
import math
import mathutils
import numpy as np
import os
import random
import sys
import time

#-------------------------------------------------------------------------------
# class (structure) definitions
#-------------------------------------------------------------------------------

class cPts: # duct segment end-point structure
  def __init__(self, position):
    self.position = position
    
class cDseg: # duct segment structure
  def __init__(self, idx_out, idx_in, ctype):
    self.idx_out = idx_out
    self.idx_in = idx_in
    self.ctype = ctype

#-------------------------------------------------------------------------------
# global constants
#-------------------------------------------------------------------------------

C_RADIUS = 2.3             # cell seed radius
C_SEEDS = 8               # cell seed target count
C_RETRIES = 80000          # cell seed creation retries
C_FRAMES = 5              # cell growing animation frame count

# duct segment end-points: position
PTS = (
  cPts(mathutils.Vector((0.0, 0.0, 0.0))), 
  cPts(mathutils.Vector((0.0, 0.0, 40.0)))
  )

# duct segment connectivity
#   - final duct out segment listed first
#   - "moving upstream" (high to low radius) ordering
DSEG = (
  cDseg(0, 1, "striated"))

# cell type dictionary
cell_types = {  
  "acinar"       : {"color":(1.000, 0.055, 0.060, 1.0), "pressure":1.8, "stiffness":0.20, "duct_radii":(0.35, 16.3)},
  "intercalated" : {"color":(1.000, 0.100, 0.120, 1.0), "pressure":1.2, "stiffness":0.11, "duct_radii":(0.8, 11.6)},
  "striated"     : {"color":(1.000, 0.200, 0.240, 1.0), "pressure":1.2, "stiffness":0.11, "duct_radii":(4.0, 23.8)}    
}

#-------------------------------------------------------------------------------
# global variables
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# function definitions
#-------------------------------------------------------------------------------

#---- create a duct segment given endpoints and radii
def create_seg(p1, p2, r1):
  d = (p2 - p1).length
  l = p1 + (p2 - p1) / 2.0
  r = (p2 - p1).to_track_quat('Z', 'X').to_euler()
  bpy.ops.mesh.primitive_cone_add(radius1 = r1, radius2 = r1, depth = d, location = l, rotation = r, end_fill_type = 'NGON')
  return

#---- create duct wall
def create_duct_wall(in_out):
  s = DSEG
  p1 = PTS[s.idx_out].position
  p2 = PTS[s.idx_in].position
  r1 = cell_types[s.ctype]['duct_radii'][in_out]

  # cylinder for non-acinar segments
  create_seg(p1, p2, r1)
  obj = bpy.context.object
  if in_out == 0:
    obj.name = "InnerWall"
  else:
    obj.name = "OuterWall"

  # remesh the duct object
  obj.select_set(True) # required by bpy.ops
  bpy.ops.object.modifier_add(type = 'REMESH')
  bpy.context.object.modifiers["Remesh"].mode = "SMOOTH"
  bpy.context.object.modifiers["Remesh"].octree_depth = 5
  bpy.ops.object.modifier_apply(modifier = "Remesh")

  # flip normals for outer duct wall
  if in_out == 1: 
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.flip_normals()
    bpy.ops.object.mode_set()
  bpy.ops.object.modifier_add(type = 'COLLISION')
  bpy.data.collections['Duct'].objects.link(bpy.context.object)
  bpy.context.collection.objects.unlink(bpy.context.object) # unlink from main collection
  return

#---- new cell too close to any of the existing cells?
def too_close(p, dist, cell_centers):
  if any((c-p).length < dist for c in cell_centers): return True
  return False

#---- create cells around a duct segment
def create_seg_cells(s):
  cell_centers = list()
  mat = bpy.data.materials.new(name="mat")
  mat.diffuse_color = cell_types[s.ctype]["color"]

  z1 = PTS[s.idx_out].position.z
  z2 = PTS[s.idx_in].position.z

  r1 = cell_types[s.ctype]['duct_radii'][1] - 2.5 * C_RADIUS# near outer wall
  for i in range(C_SEEDS): # try to create this number of random cell seeds
    create = False
    for j in range(C_RETRIES): # with many retries to help fill gaps in the seed distribution
      # a duct cell seed placement point
      a1 = random.uniform(0.0, 2.0 * math.pi)
      z = random.uniform(z1 + C_RADIUS, z2 - C_RADIUS) 
      p = mathutils.Vector((r1*math.sin(a1), r1*math.cos(a1), z))
      if len(cell_centers)==0 or not too_close(p, 3.0 * C_RADIUS, cell_centers): # accept only if not too close to other seeds
        create = True
        break
    if create:
      cell_centers.append(p)
      bpy.ops.object.duplicate()
      bpy.context.object.name = "Cell.001"    # duplicate names will auto increment
      bpy.context.object.data.materials[0] = mat #assign material to object
      bpy.context.object.location = p
      if s.ctype == "acinar": # an acinar cell seed placement point
        scale = random.uniform(0.90, 0.99)
      else:
        scale = 1.0
      bpy.context.object.scale = (scale, scale, scale)
      bpy.context.object.modifiers["Cloth"].settings.uniform_pressure_force = cell_types[s.ctype]["pressure"]
      bpy.context.object.modifiers["Cloth"].settings.compression_stiffness = cell_types[s.ctype]["stiffness"]
  return

#---- create cells around all of the duct segments
def create_cells():
  create_seg_cells(DSEG)
  return

#---- create prototype cell
def create_proto_cell():
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions = 5, radius = C_RADIUS, location = (0.0, 0.0, 0.0))
  mat = bpy.data.materials.new(name="mat")
  bpy.context.object.data.materials.append(mat) # add material to object
  bpy.ops.object.modifier_add(type = 'CLOTH')
  bpy.context.object.modifiers["Cloth"].settings.use_internal_springs = False
  bpy.context.object.modifiers["Cloth"].settings.use_pressure = True
  bpy.context.object.modifiers["Cloth"].settings.tension_stiffness = 0.02
  bpy.ops.object.modifier_add(type = 'COLLISION')
  bpy.data.collections["Cells"].objects.link(bpy.context.object)
  bpy.context.collection.objects.unlink(bpy.context.object) # unlink from main collection
  return

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

bpy.context.scene.gravity = (0,0,0) # turn gravity off

# create duct collection
bpy.context.scene.collection.children.link(bpy.data.collections.new(name = "Duct"))
create_duct_wall(0) # duct inner wall
create_duct_wall(1) # duct outer wall

# create cells collection
bpy.context.scene.collection.children.link(bpy.data.collections.new(name = "Cells"))
create_proto_cell()
create_cells() # duplicate prototype cell
bpy.data.objects.remove(bpy.data.objects['Icosphere']) # remove the prototype cell

# animate (to apply physics) 
bpy.context.scene.frame_current = 1
for frame in range(C_FRAMES):
  bpy.context.view_layer.update()
  bpy.context.scene.frame_current += 1

# save the cell meshes...
# ---- as individual standard ply files
for obj in bpy.data.collections["Duct"].all_objects: obj.select_set(False)
for obj in bpy.data.collections["Cells"].all_objects: obj.select_set(False)
for obj in bpy.data.collections["Cells"].all_objects:
  obj.select_set(True)
  bpy.ops.export_mesh.ply(filepath=obj.name.replace('.', '_') + ".ply",\
    use_normals=False, use_uv_coords=False, use_colors=False, use_selection=True)
  obj.select_set(False)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
