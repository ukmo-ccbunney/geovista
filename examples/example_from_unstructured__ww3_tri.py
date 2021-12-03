#!/usr/bin/env python
# Test for triangular FE grid from WAVEWATCH III.
# Values are defined on the node points of the triangular mesh.

import netCDF4 as nc
import geovista as gv

# Path on MetOffice linux system:
d = nc.Dataset('/home/h06/frey/ww3.201809_hs.nc')
lon = d.variables['longitude'][:]
lat = d.variables['latitude'][:]
tri = d.variables['tri'][:]

hs = d.variables['hs']

xverts = lon[tri-1]
yverts = lat[tri-1]

# I have to "clean" mesh to remove duplicate points,
# otherwise the number of points does not match the
# size of the data arrays. I can't seem to add the
# data array in the calls though regarsless of whether
# clean is True or False...
mesh=gv.Transform.from_unstructured(xverts, yverts, xverts.shape, name='tri', clean=True)

# Setting point data as scalars here works...
# but the values are clearly not in the right place...
mesh.point_data.set_scalars(hs[0,:])

plotter = gv.GeoBackgroundPlotter()
plotter.add_mesh(mesh, show_edges=True)

plotter.show()


## show points in matplotlib how it should look
import matplotlib.pyplot as plt
plt.scatter(lon,lat,c=hs[7,:],s=10)
plt.show()

#####
## For reference: NC dump of input file (trimmer to pertinent bits):

netcdf ww3.201809_hs {
dimensions:
	node = 16160 ;
	element = 30559 ;
	time = UNLIMITED ; // (17 currently)
	noel = 3 ;
variables:
	float longitude(node) ;
		longitude:units = "degree_east" ;
		longitude:standard_name = "longitude" ;
	float latitude(node) ;
		latitude:units = "degree_north" ;
		latitude:standard_name = "latitude" ;
	double time(time) ;
		time:standard_name = "time" ;
		time:units = "days since 1990-01-01T00:00:00" ;
		time:calendar = "standard" ;
	int tri(element, noel) ;

	float hs(time, node) ;
		hs:standard_name = "sea_surface_wave_significant_height" ;

}
