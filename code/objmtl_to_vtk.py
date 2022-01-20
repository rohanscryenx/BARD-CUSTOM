import k3d
import vtk
import ipywidgets as widgets
# from __future__ import print_function
# import sys

# if(len(sys.argv) != 3):
#   print('Usage: ', sys.argv[0], 'input.obj output.vtk')
#   sys.exit()

reader = vtk.vtkOBJImporter() 
reader.SetFileName('Segmentation_1.obj')
reader.SetFileNameMTL('Segmentation_1.mtl') #Attribute not found
# reader.Update()

plot = k3d.plot()

writer = vtk.vtkPolyDataWriter()
writer.SetFileName('output.vtk')
if vtk.VTK_MAJOR_VERSION <= 5:
    writer.SetInput(reader)
else:
    writer.SetInputData(reader)
writer.Write()

plot += k3d.vtk_poly_data(poly_data)
plot.display()