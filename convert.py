import argparse
from pathlib import Path

import numpy as np
import rasterio
from PIL import Image


# TODO: allow for file paths to Google Drive files and local files
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


# TODO: allow output to be Google Drive paths 
def save_img(img_arr: np.ndarray,
             name: str,
             format: str = 'png', 
             output_dir: str = "out/", 
            ):
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


def trim_slash_from_path(path: str) -> str:
    """Utility function to remove ending slash from directory path."""
    if path.endswith('/'): 
        return path[0:-1]
    return path


def extract_file_name_root(path: str) -> str: 
    """Utility function to remove the parent directories and file extension
    from a file path.
    """
    name = path.split('/')[-1]
    return name[0:name.rindex('.')]


def main():
    parser = argparse.ArgumentParser(
        prog='UtiliGEE GeoTIFF Converter', 
        description='''A utility for converting GeoTIFF images exported from GEE to common
            image file types.
            '''     
    )
    parser.add_argument('-f', required=True,
                         help='File path to source GeoTIFF.')
    parser.add_argument('-o', default='out/',
                         help='Output directory.')
    parser.add_argument('--format', default='png',
                         help='Output image format.')
    args = parser.parse_args()

    output_dir = trim_slash_from_path(args.o)
    fname = args.f
    format = args.format

    name = extract_file_name_root(fname)

    print(f'Converting GeoTIFF file {fname} to {args.format} file.')
    img_arr = arr_from_geotiff(fname)

    print(f'Saving image to {output_dir}/{name}.{format}')
    save_img(img_arr=img_arr, name=name, format=format, output_dir=output_dir)


if __name__ == '__main__': 
    main()
