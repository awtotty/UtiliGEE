'''Dataset-specific filters and masks for producing visually appealing images.'''


import ee


def maskS2clouds(image: ee.Image): 
    '''A cloud filter primarily to be used with Sentinel-2 (S2) data. 
    source: https://code.earthengine.google.com/?scriptPath=Examples%3ADatasets%2FCOPERNICUS_S2_SR
    '''
    qa = image.select('QA60');

    # Bits 10 and 11 are clouds and cirrus, respectively.
    cloudBitMask = 1 << 10;
    cirrusBitMask = 1 << 11;

    # Both flags should be set to zero, indicating clear conditions.
    mask = qa.bitwiseAnd(cloudBitMask).eq(0) \
        .And(qa.bitwiseAnd(cirrusBitMask).eq(0));

    return image.updateMask(mask).divide(10000);


def filter_clouds(): 
    return ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)