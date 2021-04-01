from pyvista import examples
from pyvista import demos
# list all examples
print(dir(examples))
# list all demos
print(dir(demos))


#---- find distance from point P to line segment AB
def dist(A, B, P):
  if (A == P) or (B == P):
    return 0

  v1 = (P - A).copy()
  v1.normalize()
  v2 = (B - A).copy()
  v2.normalize()
  if(np.arccos(v1.dot(v2)) > math.pi / 2.0):
    v1 = (P - A).copy()
    return(v1.length)

  v1 = (P - B).copy()
  v1.normalize()
  v2 = (A - B).copy()
  v2.normalize()
  if(np.arccos(v1.dot(v2)) > math.pi / 2.0):
    v1 = (P - B).copy()
    return(v1.length)

  ints = mathutils.geometry.intersect_point_line(P, A, B)
  v1 = (ints[0] - P).copy()
  return(v1.length)
  #return abs(  dot(A - B, P[::-1]) + det([A, B]) )    /      norm(A - B)


#---- combine mesh objects using boolean union modifier
def combine(prev):
  bpy.ops.object.modifier_add(type = 'BOOLEAN')
  bpy.context.object.modifiers["Boolean"].operation = "UNION"
  bpy.context.object.modifiers["Boolean"].object = prev
  bpy.context.object.modifiers["Boolean"].double_threshold = 0.0
  bpy.ops.object.modifier_apply(modifier = "Boolean")
  current = bpy.context.object
  # delete previous object
  bpy.ops.object.select_all(action = 'DESELECT')
  prev.select_set(True) # required by bpy.ops
  bpy.ops.object.delete()
  return(current)

#-------------------------------------------------------------------------------
# DEBUG: run interactive interpreter
#-------------------------------------------------------------------------------

import__('code').interact(local=dict(globals(), **locals()))

# ---- as individual custom ply files        *** TEMPORARY: WILL BE REMOVED LATER ***
for obj in bpy.data.collections["Cells"].all_objects:
  write_ply(obj.name)

#---- find distance from point P to line segment AB        *** TEMPORARY: WILL BE REMOVED LATER ***
def dist(A, B, P):
  if (A == P) or (B == P):
    return 0

  v1 = (P - A).copy()
  v1.normalize()
  v2 = (B - A).copy()
  v2.normalize()
  if(np.arccos(v1.dot(v2)) > math.pi / 2.0):
    v1 = (P - A).copy()
    return(v1.length)

  v1 = (P - B).copy()
  v1.normalize()
  v2 = (A - B).copy()
  v2.normalize()
  if(np.arccos(v1.dot(v2)) > math.pi / 2.0):
    v1 = (P - B).copy()
    return(v1.length)

  ints = mathutils.geometry.intersect_point_line(P, A, B)
  v1 = (ints[0] - P).copy()
  return(v1.length)

#---- write cell mesh out to a custom ply file       *** TEMPORARY: WILL BE REMOVED LATER ***
def write_ply(cname):

  # apply modifiers to the cell mesh
  bpy.context.view_layer.objects.active = bpy.context.scene.objects[cname]
  obj = bpy.context.object.evaluated_get(bpy.context.evaluated_depsgraph_get())

  # write the file
  with open("PL-" + cname.replace('.', '_') + ".ply", "w") as file:
    # write out the file header
    file.write("ply\n")
    #file.write("format binary_little_endian 1.0\n")
    file.write("format ascii 1.0\n")
    file.write("comment Mini-Gland mesh format 1.0\n")
    file.write("element vertex " + str(len(obj.data.vertices)) + "\n")
    file.write("property float x\n")
    file.write("property float y\n")
    file.write("property float z\n")
    file.write("element face " + str(len(obj.data.polygons)) + "\n")
    file.write("property int v1\n")
    file.write("property int v2\n")
    file.write("property int v3\n")
    file.write("property int face_type\n")
    file.write("end_header\n")

    # write out the vertex data
    for v in obj.data.vertices:
      p = v.co + obj.location
      file.write("{:.2f} ".format(p.x) + "{:.2f} ".format(p.y) + "{:.2f}\n".format(p.z))

    # write out the face data
    for poly in obj.data.polygons:
      tri_c = mathutils.Vector([0,0,0]) # surface triangle center
      # write out vertex indices
      for loop_index in range(poly.loop_start, poly.loop_start + poly.loop_total):
        pi = obj.data.loops[loop_index].vertex_index
        file.write(str(pi) + " ")
        tri_c += obj.data.vertices[pi].co + obj.location
      tri_c /= 3.0                      # use surface triangle center for distance calculations
      # write out face type
      d = dist(PTS[DSEG.idx_in].position, PTS[DSEG.idx_out].position, tri_c) # distance from duct center line
      da = d - cell_types[DSEG.ctype]['duct_radii'][0]                     # distance from duct inner limit
      db = cell_types[DSEG.ctype]['duct_radii'][1] - d                     # distance from duct outer limit
      if(da < 1.0): file.write(str(0))     # apical
      elif(db < 1.0): file.write(str(2))   # basal
      else : file.write(str(1))            # basolateral
      file.write("\n")
  return
