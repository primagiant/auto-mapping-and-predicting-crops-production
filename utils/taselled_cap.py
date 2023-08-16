from utils.index.vegetation_index import brightness_sentinel_2_tasseled_cap, greeness_sentinel_2_tasseled_cap, wetness_sentinel_2_tasseled_cap
import rasterio
import numpy as np
import os

input_path = "./qgis/6_band_jan.tif"

# make folder if not exits
output_folder = f"./output/index/tc/2020"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

with rasterio.open(input_path, 'r', dtype='float32') as src:
    blue = src.read(1)
    green = src.read(2)
    red = src.read(3)
    nir = src.read(4)
    swir1 = src.read(5)
    swir2 = src.read(6)

    wetness = wetness_sentinel_2_tasseled_cap(
        blue, green, red, nir, swir1, swir2)

    output_file = os.path.join(output_folder, "wetness_jan.tif")

    profile = src.profile
    profile.update(dtype=rasterio.float32, count=1)

    with rasterio.open(output_file, 'w', **profile) as dst:
        dst.write(wetness, 1)

    print(f"File saved to {output_file}")
