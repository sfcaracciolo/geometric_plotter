import matplotlib
import matplotlib.pyplot as plt 
import geometric_tools

class Plotter:

    def __init__(self, **kwargs) -> None:
        self.figure(**kwargs)

    @staticmethod
    def set_export():
        if matplotlib.get_backend() != 'pgf':
            matplotlib.use('pgf')
            plt.rcParams.update(
                {
                    "font.family": "serif",
                    "text.usetex": True,
                    "pgf.rcfonts": False,
                    "pgf.texsystem": 'lualatex', # default is xetex
                    "pgf.preamble": "\n".join([
                        r'\usepackage[T1]{fontenc}',
                        # r"\usepackage{mathpazo}"
                        ]),
                    "font.size": 10,
                    "axes.titlesize": 10,
                    "axes.titlesize": 10,
                    "xtick.labelsize": 8,
                    "ytick.labelsize": 8,
                    "lines.linewidth": 1
                }
            )


    def figure(self, **kwargs):
        self.fig = plt.figure(**kwargs)

        self.ax = self.fig.add_subplot(
            projection='3d',
            computed_zorder=True,
        )
        self.ax.axis('off')
     
    @staticmethod
    def show():
        if matplotlib.get_backend() != 'pgf':
            plt.show()

    @staticmethod
    def save(folder, name):
        if matplotlib.get_backend() == 'pgf':
            path = folder + name
            plt.savefig(path +'.eps', dpi = 300, orientation = 'portrait', bbox_inches = 'tight')
            plt.savefig(path +'.pdf', dpi = 300, orientation = 'portrait', bbox_inches = 'tight')
            plt.savefig(path +'.png', dpi = 300, orientation = 'portrait', bbox_inches = 'tight')


    def camera(self, view, zoom):
        self.ax.view_init(*view)
        self.ax.set_box_aspect([ub - lb for lb, ub in (getattr(self.ax, f'get_{a}lim')() for a in 'xyz')], zoom=zoom)

    def add_trisurf(self, nodes, faces, vertex_values=None, translate=(0,0,0), colorbar=False, cmap='viridis', vmin=0, vmax=1, **kwargs):

        p = self.ax.plot_trisurf(
            nodes[:,0]-translate[0],
            nodes[:,1]-translate[1],
            nodes[:,2]-translate[2],
            triangles=faces,
            **kwargs
        )
        if vertex_values is not None:
            triangle_values = geometric_tools.interp_vertices_values_to_triangles(nodes, faces, vertex_values)
            norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
            cmap = plt.get_cmap(cmap)
            m = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
            fc = m.to_rgba(triangle_values) # fc = cmap(norm(triangle_values))
            if colorbar:
                cbar = self.fig.colorbar(m, ax=self.ax, location='right', extend='both')
                cbar.minorticks_on()
        else:
            fc = 'w'

        p.set_facecolors(fc)
        p.set_edgecolors('k')

        return p 

    def add_scatter(self, nodes, translate=(0,0,0), **kwargs):
        # s is markersize
        p = self.ax.scatter(
            nodes[:,0]-translate[0],
            nodes[:,1]-translate[1],
            nodes[:,2]-translate[2],
            marker='.',
            linewidths = 0,
            edgecolors = 'none',
            **kwargs,
        )

        return p
    
    def add_quiver(self, nodes, arrows, translate=(0,0,0), **kwargs):

        p = self.ax.quiver(
            nodes[:,0]-translate[0],
            nodes[:,1]-translate[1],
            nodes[:,2]-translate[2],
            arrows[:,0],
            arrows[:,1],
            arrows[:,2],
            **kwargs
        )

        return p

    def add_normals(self, nodes, faces, **kwargs):
        normals = geometric_tools.compute_triangle_normals(nodes, faces)
        centers = geometric_tools.compute_triangle_barycenters(nodes, faces)
        return self.add_quiver(centers, normals, **kwargs)