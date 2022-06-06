'''Entry point for command line use of core library. Provides access to full GEE image 
extraction, export, and conversion to common file types.'''

import argparse

from core import extract_geotiff_from_gee
from util import convert_geotiff


def main():
    parser = argparse.ArgumentParser(
        prog='UtiliGEE GeoTIFF Fetcher', 
        description='''A utility for fetching GeoTIFF images from GEE. Specify a dataset, filtering
            options, and bands to export. All exports are saved to Google Drive. GEE authentication 
            required prior to running (follow CLI instructions). 
            '''     
    )
    parser.add_argument('--data', type=str, default='USDA/NAIP/DOQQ',
                         help='GEE dataset')
    parser.add_argument('--region', type=list, nargs='*', 
                         default=[-74.02065034469021, 40.7175360876491, -73.96855111678494, 40.69053317927286],
                         help='The minimum and maximum corners of the image\'s bounding rectangle. Four args \
                            expected: xmin, ymin, xmax, ymax.')
    parser.add_argument('--start', type=str, default='2017-01-01', 
                         help='Start date (yyyy-mm-dd).')
    parser.add_argument('--end', type=str, default='2018-12-31', 
                         help='End date (yyyy-mm-dd).')
    parser.add_argument('--bands', type=list, nargs='*', default=['R', 'G', 'B'],
                         help='Bands to be saved from the dataset.')
    parser.add_argument('--output_dir', default='UtiliGEE_Exports',
                         help='Output directory in Google Drive.')
    parser.add_argument('--desc', required=True,
                         help='Description of the file to be saved (i.e. file name root).')
    parser.add_argument('--mpp', type=int, default=30,
                         help='Meters per pixel. Smaller values yield higher resolution images.')
    parser.add_argument('--format', type=str, default='png',
                         help='Filetype to export to.')
    parser.add_argument('--min', type=int, default=None,
                         help='Minimum value of image data. Defaults to None. If None, inferred from image.')
    parser.add_argument('--max', type=int, default=None,
                         help='Maximum value of image data. Defaults to None. If None, inferred from image.')
    args = parser.parse_args()


    xmin, ymin, xmax, ymax = args.region
    dataset_name = args.data
    start_date = args.start
    end_date = args.end
    desc = args.desc
    mpp = args.mpp
    bands = args.bands
    output_dir = args.output_dir
    format = args.format
    min_value = args.min
    max_value = args.max

    print('Extracting GeoTIFF to Google Drive.')
    extract_geotiff_from_gee(dataset_name, bands, start_date, end_date, output_dir, desc, mpp, 
                         xmin, ymin, xmax, ymax)

    # TODO: 1
    # pull GeoTIFF image from Google Drive
    tmp_dir = 'raw'
    geotiff_local_path = f'{tmp_dir}/{desc}.tif'


    # convert GeoTIFF to specified format
    # TODO: 3   uncomment after the above and below TODO 1-2 are complete
    # convert_geotiff(geotiff_local_path, format, output_dir, min_value, max_value)


    # TODO:  2
    # upload final image to Google Drive? 


if __name__ == '__main__': 
    main()