from open3d.geometry import TriangleMesh
from src.geometric_plotter import Plotter
import numpy as np 
import pathlib 
filename = pathlib.Path(__file__).stem

mesh = TriangleMesh().create_cylinder(radius=1.0, height=2.0, resolution=20, split=4)
vertices, triangles = np.asarray(mesh.vertices), np.asarray(mesh.triangles)

Plotter.set_export()

p = Plotter(True, figsize=(5,5))
p.add_trisurf(vertices, triangles, alpha=1)
p.add_trisurf(vertices, triangles, alpha=.5, translate=(0,-3,0))
p.camera(view=(25, 0, 0), zoom=1.)
p.save(folder='figs/', name=f'trisurf')

p = Plotter(False, figsize=(5,5))
p.add_trisurf(vertices, triangles, alpha=.8)
p.add_scatter(vertices, color='k', s=100, alpha=1)
p.camera(view=(25, 0, 0), zoom=1.)
p.save(folder='figs/', name=f'scatter')

p = Plotter(False, figsize=(5,5))
p.add_trisurf(vertices, triangles, alpha=.8)
p.add_normals(vertices, triangles, color='k', length=.4, alpha=1)
p.camera(view=(25, -45, 0), zoom=1.)
p.save(folder='figs/', name=f'normals')

Plotter.show()