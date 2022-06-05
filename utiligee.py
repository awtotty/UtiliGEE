import argparse
import time

import ee


def main():
    parser = argparse.ArgumentParser(
        prog='UtiliGEE GeoTIFF Fetcher', 
        description='''A utility for fetching GeoTIFF images from GEE. Specify a dataset, filtering
            options, and bands to export. All exports are saved to Google Drive. GEE authentication 
            required prior to running (follow CLI instructions). 
            '''     
    )
    parser.add_argument('--data', default='USDA/NAIP/DOQQ',
                         help='GEE dataset')
    parser.add_argument('--region', nargs='*', 
                         default=[-74.02065034469021, 40.7175360876491, -73.96855111678494, 40.69053317927286],
                         help='The minimum and maximum corners of the image\'s bounding rectangle. Four args \
                            expected: xmin, ymin, xmax, ymax.')
    parser.add_argument('--start', default='2017-01-01', 
                         help='Start date.')
    parser.add_argument('--end', default='2018-12-31', 
                         help='End date.')
    parser.add_argument('--bands', nargs='*', default=['R', 'G', 'B'],
                         help='Bands to be saved from the dataset.')
    parser.add_argument('--output_dir', default='UtiliGEE_Exports',
                         help='Output directory in Google Drive.')
    parser.add_argument('--desc', required=True,
                         help='Description of the file to be saved (i.e. file name root).')
    parser.add_argument('--mpp', default=30,
                         help='Meters per pixel. Smaller values yield higher resolution images.')
    args = parser.parse_args()


    ee.Initialize()

    # region should be defined by user
    xmin, ymin, xmax, ymax = args.region
    geometry = ee.Geometry.Rectangle([xmin, ymin, xmax, ymax])

    # select dataset and filter
    dataset_name = args.data
    start_date = args.start
    end_date = args.end
    dataset = ee.ImageCollection(dataset_name) \
            .filter(ee.Filter.date(start_date, end_date));

    # select bands and geometry of final image                  
    bands = args.bands
    image = dataset.select(bands) \
                .mean();

    # export 
    output_dir = args.output_dir
    fname_root = args.desc
    task = ee.batch.Export.image.toDrive(**{
        'image': image, 
        'description': fname_root,
        'folder': output_dir,
        # smaller scale means better resolution
        'scale': args.mpp,  
        'region': geometry,
    })
    task.start()

    print('Working on export task (id: {}).'.format(task.id))
    while task.active(): 
        time.sleep(1)
    print(f'Export complete. File available in Drive at /{output_dir}/{fname_root}.tif')


if __name__ == '__main__': 
    main()