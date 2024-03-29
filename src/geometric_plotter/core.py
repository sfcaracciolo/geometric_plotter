import matplotlib
import matplotlib.pyplot as plt 
import numpy as np
import geometric_tools
import sys 
import mpl_toolkits.mplot3d.art3d as art3d
import matplotlib as mpl
from typing import Tuple
class Plotter:

    def __init__(self, _2d=False, computed_zorder=False, **kwargs) -> None:
        try:
            if sys.argv[1] == '--save': Plotter.set_export() 
        except IndexError:
            # print('Showing plots ...')
            pass
        
        if _2d:
            self.figure2d(**kwargs)
        else:
            self.figure3d(computed_zorder, **kwargs)


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

    def figure2d(self, **kwargs):
        nrows = kwargs.pop('nrows', 1)
        ncols = kwargs.pop('ncols', 1)
        self.fig, self.axs = plt.subplots(nrows=nrows, ncols=ncols, **kwargs)

    def figure3d(self, computed_zorder, **kwargs):
        self.fig = plt.figure(**kwargs)

        self.ax = self.fig.add_subplot(
            projection='3d',
            computed_zorder=computed_zorder,
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
            # plt.savefig(path +'.eps', orientation = 'portrait', bbox_inches = 'tight')
            plt.savefig(path +'.pdf', orientation = 'portrait', bbox_inches = 'tight')
            # plt.savefig(path +'.png', dpi = 300, orientation = 'portrait', bbox_inches = 'tight')


    def camera(self, view, zoom):
        self.ax.view_init(*view)
        self.ax.set_box_aspect([ub - lb for lb, ub in (getattr(self.ax, f'get_{a}lim')() for a in 'xyz')], zoom=zoom)

    def add_trisurf(self, nodes, faces, vertex_values=None, translate=(0,0,0), colorbar=False, cmap='viridis', vmin=0, vmax=1, location='right', **kwargs):

        p = self.ax.plot_trisurf(
            nodes[:,0]-translate[0],
            nodes[:,1]-translate[1],
            nodes[:,2]-translate[2],
            triangles=faces,
            **kwargs
        )
        if vertex_values is not None:
            if vertex_values.ndim > 1:
                vertex_values = np.ravel(vertex_values)

            triangle_values = geometric_tools.interp_vertices_values_to_triangles(nodes, faces, vertex_values)
            norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
            cmap = plt.get_cmap(cmap)
            m = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
            if colorbar:
                cbar = self.fig.colorbar(m, ax=self.ax, location=location, extend='both')
                cbar.minorticks_on()
            fc = m.to_rgba(triangle_values) # fc = cmap(norm(triangle_values))
        else:
            fc = 'w'

        p.set_facecolors(fc)
        p.set_edgecolors('k')

        return p 

    @staticmethod
    def colorbar(cmap='viridis', vmin=0, vmax=1, **kwargs):
        p = Plotter(False, figsize=(2,5))
        cax = plt.axes([0.5, 0.1, 0.1, 0.9]) # left, bottom, width, height
        norm = matplotlib.colors.Normalize(vmin=vmin, vmax=vmax)
        cmap = plt.get_cmap(cmap)
        m = matplotlib.cm.ScalarMappable(cmap=cmap, norm=norm)
        cbar = p.fig.colorbar(m, cax=cax, **kwargs)
        cbar.minorticks_on()
        return p

    def add_scatter(self, nodes, translate=(0,0,0), texts=None, txt_kw={}, **kwargs):
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

        if texts is not None:
            x_offset = txt_kw.pop('x_offset', None)
            y_offset = txt_kw.pop('y_offset', None)
            z_offset = txt_kw.pop('z_offset', None)
            for i, (pt, t) in enumerate(zip(nodes, texts)):
                x, y, z = pt.tolist()
                if x_offset is not None: x -= x_offset[i]
                if y_offset is not None: y -= y_offset[i]
                if z_offset is not None: z -= z_offset[i]
                self.ax.text(x, y, z, t, **txt_kw)

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

    def add_patch(self, patch, **kwargs):
        self.ax.add_patch(patch)
        art3d.pathpatch_2d_to_3d(patch, **kwargs)

    def add_line(self, a, b, patch_kw, **kwargs):
        self.add_patch(mpl.patches.ConnectionPatch(a, b, 'data', **patch_kw),**kwargs)

    def add_circle(self, center, radius, patch_kw, **kwargs):
        self.add_patch(plt.Circle(center, radius=radius, **patch_kw),**kwargs)

    def bland_altman(self, ax, data1, data2, **kwargs):

        _diff = data1 - data2 # Difference between data1 and data2
        _sum = (data1 + data2)/2.
        ax.scatter(_sum, _diff, **kwargs)

        md = np.mean(_diff) # Mean of the difference
        sd = np.std(_diff, axis=0) # Standard deviation of the difference
        sup = md + 1.96*sd
        inf = md - 1.96*sd

        ax.axhline(md, color='gray', linestyle='--', linewidth=.5)
        ax.axhline(sup, color='gray', linestyle='--', linewidth=.5)
        ax.axhline(inf, color='gray', linestyle='--', linewidth=.5)
        ax.text(.1,.9,f'$\\mu = {md:.3f}$', transform=ax.transAxes)
        ax.text(.1,.8,f'$\\sigma = {sd:.3f}$', transform=ax.transAxes)

        _max = max(abs(sup), abs(inf))
        ax.set_ylim((-_max*3, _max*3))
    
    def pearson(self, ax, data1, data2, **kwargs):
        # ax.hist2d(data1, data2, bins=200) # , s=3, color='k')
        ax.scatter(data1, data2, **kwargs)
        X_plot = np.linspace(*ax.get_xlim(), 100)
        
        # Add correlation line
        m, b = np.polyfit(data1, data2, 1)
        rho = np.corrcoef(data1, data2)[0,1]
        ax.plot(X_plot, m*X_plot + b, '--', color='gray', linewidth=.5)
        ax.plot(X_plot, X_plot, '--', color='gray', linewidth=.5)
        ax.text(.1,.9,f'$\\rho = {rho:.3f}$', transform=ax.transAxes)
        ax.text(.1,.8,f'$m = {m:.3f}$', transform=ax.transAxes)