#!/usr/bin/env python3

import geovista as gv
from geovista.pantry import ww3_global_smc
import geovista.theme  # noqa: F401


def main() -> None:
    # load the sample data
    sample = ww3_global_smc()

    # create the mesh from the sample data
    mesh = gv.Transform.from_unstructured(sample.lons, sample.lats, data=sample.data)

    # threshold the mesh of NaNs
    mesh = mesh.threshold()

    # plot the mesh
    plotter = gv.GeoPlotter()
    sargs = dict(title=f"{sample.name} / {sample.units}", shadow=True)
    plotter.add_mesh(mesh, scalar_bar_args=sargs)
    plotter.add_base_layer(texture=gv.natural_earth_hypsometric())
    plotter.add_coastlines()
    plotter.add_axes()
    plotter.add_text(
        "WW3 Spherical Multi-Cell (10m Coastlines)",
        position="upper_left",
        font_size=10,
        shadow=True,
    )
    plotter.show()


if __name__ == "__main__":
    main()
