#!/usr/bin/env python

# This example demonstrates the conversion of point data to cell data.
# The conversion is necessary because we want to threshold data based
# on cell scalar values.

import vtk

#from vtk.util.misc import vtkGetDataRoot
#VTK_DATA_ROOT = vtkGetDataRoot()

# Read some data with point data attributes. The data is from a
# plastic blow molding process (e.g., to make plastic bottles) and
# consists of two logical components: a mold and a parison. The
# parison is the hot plastic that is being molded, and the mold is
# clamped around the parison to form its shape.
reader = vtk.vtkUnstructuredGridReader()
reader.SetFileName("test14.vtk")
#reader.SetScalarsName("thickness9")
#reader.SetVectorsName("displacement9")

ds2do = vtk.vtkDataSetToDataObjectFilter()
ds2do.SetInputConnection(reader.GetOutputPort())

write = vtk.vtkDataObjectWriter()
write.SetInputConnection(ds2do.GetOutputPort())
write.SetFileName("UGridField.vtk")
write.Write()

# Read the field and convert to unstructured grid.
dor = vtk.vtkDataObjectReader()
dor.SetFileName("UGridField.vtk")

do2ds = vtk.vtkDataObjectToDataSetFilter()
do2ds.SetInputConnection(dor.GetOutputPort())
do2ds.SetDataSetTypeToUnstructuredGrid()
do2ds.SetPointComponent(0, "Points", 0)
do2ds.SetPointComponent(1, "Points", 1)
do2ds.SetPointComponent(2, "Points", 2)
do2ds.SetCellTypeComponent("CellTypes", 0)
do2ds.SetCellConnectivityComponent("Cells", 0)
do2ds.Update()


fd2ad = vtk.vtkFieldDataToAttributeDataFilter()
fd2ad.SetInputData(do2ds.GetUnstructuredGridOutput())
fd2ad.SetInputFieldToDataObjectField()
fd2ad.SetOutputAttributeDataToPointData()
#fd2ad.SetVectorComponent(0, "displacement9", 0)
#fd2ad.SetVectorComponent(1, "displacement9", 1)
#fd2ad.SetVectorComponent(2, "displacement9", 2)
#fd2ad.SetScalarComponent(0, "thickness9", 0)
fd2ad.Update()



# Convert the point data to cell data. The point data is passed
# through the filter so it can be warped. The vtkThresholdFilter then
# thresholds based on cell scalar values and extracts a portion of the
# parison whose cell scalar values lie between 0.25 and 0.75.
p2c = vtk.vtkPointDataToCellData()
p2c.SetInputConnection(reader.GetOutputPort())
p2c.PassPointDataOn()

#print p2c

warp = vtk.vtkWarpVector()
warp.SetInputConnection(p2c.GetOutputPort())

#print warp

thresh = vtk.vtkThreshold()
thresh.SetInputConnection(warp.GetOutputPort())
thresh.ThresholdBetween(0.25, 0.75)
thresh.SetInputArrayToProcess(1, 0, 0, 0, "thickness9")
#thresh.SetAttributeModeToUseCellData()

#print thresh

# This is used to extract the mold from the parison.
connect = vtk.vtkConnectivityFilter()
connect.SetInputConnection(thresh.GetOutputPort())
connect.SetExtractionModeToSpecifiedRegions()
connect.AddSpecifiedRegion(0)
connect.AddSpecifiedRegion(1)

#print connect

moldMapper = vtk.vtkDataSetMapper()
moldMapper.SetInputConnection(reader.GetOutputPort())
moldMapper.ScalarVisibilityOff()
moldActor = vtk.vtkActor()
moldActor.SetMapper(moldMapper)
moldActor.GetProperty().SetColor(.2, .2, .2)
moldActor.GetProperty().SetRepresentationToWireframe()

#print moldActor

# The threshold filter has been used to extract the parison.
connect2 = vtk.vtkConnectivityFilter()
connect2.SetInputConnection(thresh.GetOutputPort())

#print connect2

parison = vtk.vtkGeometryFilter()
parison.SetInputConnection(connect2.GetOutputPort())

#print parison

normals2 = vtk.vtkPolyDataNormals()
normals2.SetInputConnection(parison.GetOutputPort())
normals2.SetFeatureAngle(60)

#print normals2

lut = vtk.vtkLookupTable()
lut.SetHueRange(0.0, 0.66667)

#print lut

parisonMapper = vtk.vtkPolyDataMapper()
parisonMapper.SetInputConnection(normals2.GetOutputPort())
parisonMapper.SetLookupTable(lut)
parisonMapper.SetScalarRange(0.12, 1.0)

#print parisonMapper

parisonActor = vtk.vtkActor()
parisonActor.SetMapper(parisonMapper)

#print parisonActor

# We generate some contour lines on the parison.
cf = vtk.vtkContourFilter()
cf.SetInputConnection(connect2.GetOutputPort())
cf.SetValue(0, .5)
contourMapper = vtk.vtkPolyDataMapper()
contourMapper.SetInputConnection(cf.GetOutputPort())
contours = vtk.vtkActor()
contours.SetMapper(contourMapper)

# Create graphics stuff
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Add the actors to the renderer, set the background and size
ren.AddActor(moldActor)
ren.AddActor(parisonActor)
ren.AddActor(contours)

ren.ResetCamera()
ren.GetActiveCamera().Azimuth(60)
ren.GetActiveCamera().Roll(-90)
ren.GetActiveCamera().Dolly(2)
ren.ResetCameraClippingRange()

ren.SetBackground(1, 1, 1)
renWin.SetSize(750, 400)

iren.Initialize()
renWin.Render()
iren.Start()
