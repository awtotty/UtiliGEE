import numpy as np
import rasterio
from PIL import Image


fname = 'small'

# Read raster bands directly to Numpy arrays.
#
with rasterio.open(f'raw/{fname}.tif') as src:
    r, g, b = src.read()
    print(src.width, src.height)
    print(src.crs)
    print(src.transform)
    print(src.count)
    print(src.indexes)

img_arr = np.zeros((r.shape[0], r.shape[1], 3), dtype=np.uint8)
img_arr[:,:,0] = r
img_arr[:,:,1] = g
img_arr[:,:,2] = b

im = Image.fromarray(img_arr)
im.save(f'out/{fname}.png')