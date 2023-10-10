from importer import *

r = gplates.get_paleo_coastlines(100)
print(r)

r = gplates.get_paleo_coastlines(100, format="shapely")
print(r)
