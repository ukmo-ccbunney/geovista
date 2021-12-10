import netCDF4 as nc
import geovista as gv
import numpy as np

d = nc.Dataset('gbl.nc')
clons = d.variables['longitude'][:]
clats = d.variables['latitude'][:]
base_lon_size = d.base_lon_size
base_lat_size = d.base_lat_size
cx = d.variables['cx'][:]
cy = d.variables['cy'][:]

dlon = cx * base_lon_size
dlat = cy * base_lat_size

fac = 0.5
x1 = (clons - fac * dlon).reshape(-1, 1)
x2 = (clons + fac * dlon).reshape(-1, 1)
y1 = (clats - fac * dlat).reshape(-1, 1)
y2 = (clats + fac * dlat).reshape(-1, 1)

lons = np.hstack([x1, x2, x2, x1])
lats = np.hstack([y1, y1, y2, y2])


#calculate mesh
hs = d.variables['hs']
mesh = gv.Transform.from_unstructured(lons, lats, lons.shape, data=hs[0,:])

# calculate a subset of arrow vectors
# I've done this in a very noddy way! Basically I've calculated
# the arrow direction vector as the difference between two
# geodesic transforms: the cell centre and the cell centre + a scaled
# wind speed component!
# 'nth' is used to thin out the data a bit...
u = d.variables['uwnd']
v = d.variables['vwnd']
nth = 200
xyz = gv.geodesic.to_xyz(clons[::nth], clats[::nth])
xyz2 = gv.geodesic.to_xyz(clons[::nth] + u[0,::nth] * 0.25,
		clats[::nth] + v[0,nth] * 0.25)
arrow_dirs = xyz2 - xyz

# plot
plotter = gv.GeoBackgroundPlotter()
plotter.add_base_layer(color='darkgray')
plotter.add_mesh(mesh, show_edges=False)
plotter.add_arrows(xyz, arrow_dirs, mag=1, color='black')

