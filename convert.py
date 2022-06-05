'''Entry point for command line conversions of GeoTIFF files to common image types.'''


import argparse

from util import trim_slash_from_path, extract_file_name_root 
from core import arr_from_geotiff, save_img


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
