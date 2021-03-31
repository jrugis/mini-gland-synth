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

