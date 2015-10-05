#!/usr/bin/env python
import os
#import io


mesh14 = open("test.vtk", "rb")
tri14 =  open("triangles.txt", "wb")
ver14 = open("vertices.txt", "wb")

#while mesh14:
flag_ver = 0
flag_tri = 0

lines = mesh14.readlines()
for line in lines:
	ar_line = line.split()

        if (flag_ver and ar_line[0] != 'CELLS'):
                ver14.write(line)

        if (flag_tri and len(ar_line) >= 4):
		line1 = ar_line[1] + ' ' + ar_line[2] + ' ' + ar_line[3] + ' ' + ar_line[4] + '\n'
                tri14.write(line1)

	if ar_line[0] == 'POINTS':
		#print line
		flag_ver = 1

	if ar_line[0] == 'CELLS':
		flag_tri = 1
		flag_ver = 0

	if ar_line[0] == 'CELL_TYPES':
		flag_tri = 0
		flag_ver = 0

ver14.close()
tri14.close()
mesh14.close()
