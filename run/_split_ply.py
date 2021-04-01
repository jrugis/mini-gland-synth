# -*- coding: utf-8 -*-
#
# Split apical, basolateral and basal regions out from a custom mini-gland mesh.
#
# J.rugis
# 31.03.2021
#
import glob
import os

#-------------------------------------------------------------------------------
# function definitions
#-------------------------------------------------------------------------------

#---- split a custom ply file by face type
def split_file(fname):
  fi = open(fname, 'r')

  # get the vertex and face counts
  for ln in fi:
    token = ln.split()
    if token[0]=="element" and token[1]=="vertex":
      vertex_count = int(token[2])
    if token[0]=="element" and token[1]=="face":
      face_count = int(token[2])
      break

  # skip to end of header
  for ln in fi:
    if ln.split()[0]=="end_header":
      break

  # skip over vertices
  for i in range(vertex_count):
    fi.readline()
  
  # count the number of apical, basolateral and basal faces
  names = ["AP", "BL", "BS"]
  counts = [0,0,0]
  for i in range(face_count):
    type = int(fi.readline().split()[3])
    counts[type] += 1

  # write out new split ply files
  for type in range(len(names)):
    file = open(names[type] + '-' + fname.split('-')[1], 'w')  # create output file 
    file.write("ply\n") # write output file header
    file.write("format ascii 1.0\n")
    file.write("element vertex " + str(vertex_count) + "\n")
    file.write("property float x\n")
    file.write("property float y\n")
    file.write("property float z\n")
    file.write("element face " + str(counts[type]) + "\n")
    file.write("property list uchar uint vertex_indices\n")
    file.write("end_header\n")
  
    # seek to end of input file header
    fi.seek(0)    # start at begining of input file
    for ln in fi: # skip lines
      if ln.split()[0]=="end_header":
        break

    # copy out all of the vertices (overkill, but avoids reindexing)
    for i in range(vertex_count):
      file.write(fi.readline())
  
    # get and write out a subset of faces
    for i in range(face_count):
      token = fi.readline().split()
      if token[3]==str(type):
        file.write("3 " + token[0] + " " + token[1] + " " + token[2] + "\n")

    file.close() # close the output file
  fi.close() # close the input file
  return  

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
#  MAIN PROGRAM
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# delete any existing split files
os.system("rm -f AP*.ply")
os.system("rm -f BL*.ply")
os.system("rm -f BS*.ply")

# split all of the custom ply files
flist = glob.glob("PL-Cell_*.ply")
for f in flist:
  split_file(f)

#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
