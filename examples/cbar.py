from src.geometric_plotter import Plotter
import pathlib 
filename = pathlib.Path(__file__).stem

p = Plotter.colorbar(cmap='turbo',vmin=-1, vmax=2, extend='both')
p.save(folder='figs/', name=f'{filename}')


Plotter.show()