#!/usr/bin/sh

python mesh14.py
python make_tri_ver.py
python driver.py
cat test.vtk point_data.txt > test14.vtk
cp test14.vtk /Users/new/vtkpython/bin
cd /Users/new/vtkpython/bin
vtkpython mesh_reader14.py
