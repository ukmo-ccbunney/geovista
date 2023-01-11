#!/usr/bin/env python3
"""
This example demonstrates how to create a mesh from 1-D latitude and longitude
(degrees) unstructured cell points and connectivity. The resulting mesh contains
triangular cells.

It uses a WAVEWATCH III (WW3) unstructured triangular mesh sea surface
wave significant height data located on mesh nodes/points.

Note that, a threshold is also applies to remove land NaN cells, and a
Natural Earth base layer is rendered along with Natural Earth coastlines.
As data is located on the mesh nodes/points, these values are interpolated
across the mesh faces/cells.

"""

import geovista as gv
from geovista.pantry import ww3_global_tri
import geovista.theme  # noqa: F401


def main() -> None:
    # load the sample data
    sample = ww3_global_tri()

    # create the mesh from the sample data
    mesh = gv.Transform.from_unstructured(
        sample.lons, sample.lats, connectivity=sample.connectivity, data=sample.data
    )

    # plot the mesh
    plotter = gv.GeoPlotter()
    sargs = dict(title=f"{sample.name} / {sample.units}", shadow=True)
    plotter.add_mesh(mesh, show_edges=True, scalar_bar_args=sargs)
    plotter.add_base_layer(texture=gv.natural_earth_hypsometric())
    plotter.add_coastlines()
    plotter.add_axes()
    plotter.view_xy(negative=True)
    plotter.add_text(
        "WW3 Triangular Mesh (10m Coastlines)",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.show()


if __name__ == "__main__":
    main()
