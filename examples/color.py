from open3d.geometry import TriangleMesh
from src.geometric_plotter import Plotter
import numpy as np 
import pathlib 
import geometric_tools
filename = pathlib.Path(__file__).stem

mesh = TriangleMesh().create_cylinder(radius=1.0, height=2.0, resolution=20, split=4)
vertices, triangles = np.asarray(mesh.vertices), np.asarray(mesh.triangles)

# smooth functions
spherical = geometric_tools.cartesian_to_spherical_coords(mesh.vertices)
ρ, θ, φ = spherical[:,0], spherical[:,1], spherical[:,2]
f = np.cos(φ)*np.sin(θ)

p = Plotter(figsize=(5,5))
p.add_trisurf(vertices, triangles, alpha=1, vertex_values=f, vmin=f.min(), vmax=f.max(), colorbar=True)
p.camera(view=(25, -75, 0), zoom=1.)
p.save(folder='figs/', name=f'{filename}')


Plotter.show()