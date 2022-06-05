'''Various utility functions for cleaning file paths and managing files locally
and on Google Drive. 
'''


import numpy as np
from pathlib import Path

from core import arr_from_geotiff


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


def download_file_from_drive(path: str, output_path: str = None): 
    fname = extract_file_name_root(path)

    if output_path is None: 
        output_path = f'raw/{fname}'
    
    raise NotImplementedError


# TODO: allow output to be Google Drive paths 
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


def convert_geotiff(fname: str, format:str = 'png', output_dir: str = '/out'):
    name = extract_file_name_root(fname)

    print(f'Converting GeoTIFF file {fname} to {format} file.')
    img_arr = arr_from_geotiff(fname)

    output_dir = trim_slash_from_path(output_dir) 
    print(f'Saving image to {output_dir}/{name}.{format}')
    save_img(img_arr=img_arr, name=name, format=format, output_dir=output_dir)
