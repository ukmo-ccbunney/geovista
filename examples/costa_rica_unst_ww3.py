#!/usr/bin/env python
# Test for triangular FE grid from WAVEWATCH III.
# Domain is high resolution grid around Puerto Limon harbour, Costa Rica.
# Values are defined on the node points of the triangular mesh.

import netCDF4 as nc
import geovista as gv

# Path on MetOffice linux system:
d = nc.Dataset('/net/home/h06/frey/src/geovista/examples/tp2.6_ww3.201008_hs.nc')
lons = d.variables['longitude'][:]
lats = d.variables['latitude'][:]
tri = d.variables['tri'][:]

# Data is sig. wv. ht
fld = d.variables['hs']
itime = 0

mesh=gv.Transform.from_unstructured(lons, lats, tri - 1, name='tri', data=fld[itime,:])


plotter = gv.GeoBackgroundPlotter()
plotter.add_base_layer(color='darkgreen')
plotter.add_mesh(mesh, cmap="jet", show_edges=True,clim=[0,4]) # I know Jet is bad, but I like it :o)
plotter.add_coastlines(resolution='10m')

# This next bit is my super hacky way of focussing on the
# region of interest. I'm probabvly doing it all wrong, but
# it is a result of nosing around avaialbe the GeoVista / pyVista 
# functions and general trial and error!!
# Please advise if there is a better way of doing this!!! :-)
cam = plotter.camera    # this seems to reset the view, so I'm probably not suppose to do this?
plotter.fly_to(gv.geodesic.to_xyz(-83.021624, 9.985544))
cam.azimuth=-130  ## needed this when I was using plotter.fly_to
cam.zoom(2**13) # Double the zoom, 13 times...

# The above "works", but results in a lot of visual oddities on the plot.
# Possible something to do with the base layer (See note2) or the view angle?
# In fact, if you zoom out, the base layer definitely looks .... odd.....

####plotter.set_position(gv.geodesic.to_xyz(-83.011624, 9.986444))
# see Note1 below.


def fld_update_callback():
    global itime
    global mesh
    global fld

    itime = (itime + 1) % min(fld.shape[0],24) # it's a bit boring after 24 timesteps!
    name = mesh.active_scalars_name
    mesh[name] = fld[itime].data

plotter.add_callback(fld_update_callback, interval=300)

plotter.show()

#
# Note1: "set_position" seems a more logical choice than fly_to, but then
# I can't seem to programmatically set a sensible zoom value (at
# least not by my trial and error attemps!!!)
#
#
# Note2: Turning off the base later doesn't remove the weird visual
# oddities, but it does make the interactive globe much more responsive
# on my VDI instance...tohught I would mention that...
