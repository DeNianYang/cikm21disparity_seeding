import numpy as np

from bokeh.models import ColumnDataSource, Plot, LinearAxis, Grid
from bokeh.models.markers import Circle
from bokeh.io import curdoc, show
from bokeh.io import export_svgs



N = 9
x = np.linspace(-2, 2, N)
y = x**2
sizes = np.linspace(10, 20, N)

source = ColumnDataSource(dict(x=x, y=y, sizes=sizes))

plot = Plot(
    title=None, plot_width=300, plot_height=300,
    min_border=0, toolbar_location=None)

glyph = Circle(x="x", y="y", size="sizes", line_color="yellow", fill_color="yellow", line_width=3)
plot.add_glyph(source, glyph)


curdoc().add_root(plot)

plot.output_backend = "svg"
export_svgs(plot, filename="circle/plot_yellow.svg")