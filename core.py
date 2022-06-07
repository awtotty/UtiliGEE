'''Core library functions, including GEE extraction, image saving, conversion 
functions, etc.
'''


import time
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image
import ee

from util import trim_slash_from_path, extract_file_name_root
from masks_and_filters import maskS2clouds, filter_clouds


def extract_geotiff_from_gee(dataset_name: str, 
                             bands: list, 
                             start_date: str, 
                             end_date: str,
                             output_dir: str, 
                             desc: str, 
                             mpp: int, 
                             xmin: float, 
                             ymin: float, 
                             xmax: float, 
                             ymax: float,
                             filter: callable = None, 
                             mask: callable = None,
                            ) -> None: 
    # initializes the GEE instance
    ee.Initialize()

    geometry = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])

    dataset = ee.ImageCollection(dataset_name).filter(ee.Filter.date(start_date, end_date))

    # additional filtering and masking required based on dataset
    # if filter is None: 
    #     filter = filter_from_dataset_name(dataset_name)
    # if filter is not None: 
    #     dataset = dataset.filter(filter)

    if mask is None: 
        mask = mask_from_dataset_name(dataset_name)
    dataset = dataset.map(mask)

    # select bands and average for final image                 
    image = dataset.select(bands).mean();

    # export 
    output_dir = output_dir
    fname_root = desc
    # TODO: add key attrs to fname (default behavior)
    # if  attr: details_in_fname: 
    #   fname += #string with details
    task = ee.batch.Export.image.toDrive(**{
        'image': image, 
        'description': fname_root,
        'folder': output_dir,
        # smaller scale means better resolution
        'scale': mpp,  
        'region': geometry,
    })
    task.start()

    print('Working on export task (id: {}).'.format(task.id))
    while task.active(): 
        time.sleep(1)
    print(f'Export complete. File available in Drive at /{output_dir}/{fname_root}.tif')


def filter_from_dataset_name(dataset_name: str):
    # Sentinel-2 mask
    if 'S2' in dataset_name: 
        filter = filter_clouds
    # TODO: additional filters are needed based on specific dataset (see GEE web client for more)

    # default filter is identity
    else: 
        filter = None
    
    return filter


def mask_from_dataset_name(dataset_name: str):
    # Sentinel-2 mask
    if 'S2' in dataset_name: 
        mask = maskS2clouds
    # TODO: additional masks are needed based on specific dataset (see GEE web client for more)

    # default filter is identity
    else: 
        mask = lambda x: x 
    
    return mask 


def arr_from_geotiff(fname: str, 
                     r_channel: int = 1, 
                     g_channel: int = 2,
                     b_channel: int = 3,
                    ) -> Image: 
    """Converts a geotiff to an np.ndarray.
    
    Args: 
        fname (str): Filepath for the 
        r_channel (int): Channel of image data to assign to Red (1-indexed). Defaults to 1.
        g_channel (int): Channel of image data to assign to Green (1-indexed). Defaults to 2.
        b_channel (int): Channel of image data to assign to Blue (1-indexed). Defaults to 3.
    
    Returns a PIL.Image in rgb format.
    """

    # Read raster bands directly to Numpy arrays.
    if not fname.endswith('.tif'): 
        fname += '.tif'

    with rasterio.open(fname) as src:
        r = src.read(r_channel)
        g = src.read(g_channel)
        b = src.read(b_channel)

    img_arr = np.zeros((r.shape[0], r.shape[1], 3), dtype=np.uint8)
    img_arr[:,:,0] = r
    img_arr[:,:,1] = g
    img_arr[:,:,2] = b

    return Image.fromarray(img_arr)


def save_img(img_arr: np.ndarray,
             name: str,
             format: str = 'png', 
             output_dir: str = "out/", 
            ) -> None:
    """Saves an image np.ndarray in the specified format. 

    Args: 
        img_arr (np.ndarray): 
        name (str): Name of the image.  
        format (:obj: `str`, Optional): File type of output. Defaults to 'png'. 
        output_dir (:obj: `str`, Optional): Output directory. Defaults to 'out/'. 
            If the directory does not exist, it is created.  
    """

    output_dir = trim_slash_from_path(output_dir)
    fname = f"{output_dir}/{name}.{format}"

    # make sure output dir exists (create it if it doesn't)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    img_arr.save(fname)


def convert_geotiff(fname: str, 
                    format:str = 'png', 
                    output_dir: str = '/out',
                    min_value: int = None,   
                    max_value: int = None,
                   ):
    name = extract_file_name_root(fname)

    print(f'Converting GeoTIFF file {fname} to {format} file.')
    img_arr = arr_from_geotiff(fname)

    # TODO: 
    # project img arr data into rgb range [0, 256)
    # if min_value and max_value are None, infer their values from img_arr

    output_dir = trim_slash_from_path(output_dir) 
    print(f'Saving image to {output_dir}/{name}.{format}')
    save_img(img_arr=img_arr, name=name, format=format, output_dir=output_dir)


def batch_convert_geotiff(dir_name: str, 
                          format:str = 'png', 
                          output_dir: str = '/out',
                          min_value: int = None,   
                          max_value: int = None,
                         ):
    raise NotImplementedError()