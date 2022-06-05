// select dataset and filter
var dataset = ee.ImageCollection('USDA/NAIP/DOQQ')
                  .filter(ee.Filter.date('2017-01-01', '2018-12-31'));

// select bands and geometry of final image                  
var trueColor = dataset.select(['R', 'G', 'B'])
  .mean();
  
  
// visualization on map below only
var trueColorVis = {
  min: 0.0,
  max: 255.0,
};
var region_center = geometry.centroid({'maxError': 1})
Map.centerObject(region_center, 10)
Map.addLayer(trueColor.clip(geometry), trueColorVis, 'True Color');


// export 
Export.image.toDrive({
  image: trueColor, 
  description: 'small',
  scale: 1, // smaller means better resolution
  region: geometry
})