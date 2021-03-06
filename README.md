# Image Utility for Google Earth Engine (UtiliGEE)

UtiliGEE is a utility library for producing common image and video files from Google Earth Engine (GEE).  

## Getting Started
From the root directory run 

```conda env create -f env.yml```

Authenticate Google Earth Engine

(Mac/Linux)
```earthengine authenticate``

(WSL is not currently supported due to difficulties with authenticating gcloud in WSL; see TO-DO below)


## TO-DO: 
_This library is a work in progress. Please feel free to contribute._

- ~~build python utilities for downloading images from GEE~~
  - ~~allow specifiying lat/long bounding boxes only~~
- Find work around for WSL gcloud authentication and update readme with instructions
- build utility to apply library function to entire folder of raw files
- parallelize where possible
- create usage examples (good ones)
- add pip dependency install option (requirements.txt)
- ~~fix library branding~~
- documentation
- build module structure
