from importer import *

lats = [50, 10, 50]
lons = [-100, 160, 100]

r = gplates.get_paleo_coordinates(lats, lons, 100, model="PALEOMAP")
print(r)
