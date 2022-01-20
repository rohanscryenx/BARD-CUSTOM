import k3d
import vtk
import ipywidgets as widgets
# from __future__ import print_function
# import sys

# if(len(sys.argv) != 3):
#   print('Usage: ', sys.argv[0], 'input.obj output.vtk')
#   sys.exit()

reader = vtk.vtkGLTFReader() 
reader.SetFileName('scene.glb')
reader.Update() 
mb = reader.GetOutput()

# plot = k3d.plot()

writer = vtk.vtkPolyDataWriter()
writer.SetFileName('output.vtk')
if vtk.VTK_MAJOR_VERSION <= 5:
    writer.SetInput(mb)
else:
    writer.SetInputData(mb)
writer.Write()

# plot += k3d.vtk_poly_data(poly_data)
# plot.display()