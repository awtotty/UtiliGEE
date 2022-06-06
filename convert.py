'''Entry point for command line conversions of GeoTIFF files to common image types.'''


import argparse

from util import convert_geotiff, trim_slash_from_path 


def main():
    parser = argparse.ArgumentParser(
        prog='UtiliGEE GeoTIFF Converter', 
        description='''A utility for converting GeoTIFF images exported from GEE to common
            image file types.
            '''     
    )
    parser.add_argument('fname',
                         help='File path to source GeoTIFF.')
    parser.add_argument('-o', default='out/',
                         help='Output directory.')
    parser.add_argument('--format', default='png',
                         help='Output image format.')
    parser.add_argument('--min', type=int, default=None,
                         help='Minimum value of image data. Defaults to None. If None, inferred from image.')
    parser.add_argument('--max', type=int, default=None,
                         help='Maximum value of image data. Defaults to None. If None, inferred from image.')
    args = parser.parse_args()

    output_dir = trim_slash_from_path(args.o)
    fname = args.fname
    format = args.format
    min_value = args.min
    max_value = args.max

    convert_geotiff(fname, format, output_dir, min_value, max_value)


if __name__ == '__main__': 
    main()
