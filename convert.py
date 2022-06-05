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
    args = parser.parse_args()

    output_dir = trim_slash_from_path(args.o)
    fname = args.fname
    format = args.format

    convert_geotiff(fname, format, output_dir)


if __name__ == '__main__': 
    main()
