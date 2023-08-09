from vegetation_index import ndvi_index
import rasterio
import numpy as np
import zipfile
import os


# adjust with band data filename
target_band = ["B04_10m.jp2", "B08_10m.jp2"]

zip_folder_path = "./data/2020"
files = os.listdir(zip_folder_path)

# make folder if not exits
output_folder = f"./output/index/ndvi/2020"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for path in files:
    zip_file_path = f'{zip_folder_path}/{path}'
    file_inside_zip = []

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            for target_fl in target_band:
                if file_name.endswith(target_fl):
                    file_inside_zip.append(file_name)

    # Open Using Rasterio (adjust it with target_band)
    with rasterio.open(f'/vsizip/{zip_file_path}/{file_inside_zip[0]}') as b8:
        with rasterio.open(f'/vsizip/{zip_file_path}/{file_inside_zip[1]}') as b4:
            geoTransform = b4.transform
            geoProjection = b4.crs.to_wkt()

            nir = b8.read(1).astype(np.float32)
            red = b4.read(1).astype(np.float32)

            ndvi = ndvi_index(red, nir)

            # Save ram
            nir = None
            red = None

            # save ndvi
            output_path = f'{output_folder}/{path.split(".")[0]}.tif'
            cols, rows = ndvi.shape

            lon_start = geoTransform[2]
            lat_start = geoTransform[5]
            pixel_width = geoTransform[0]
            pixel_height = geoTransform[4]

            lon_values = np.arange(
                lon_start, lon_start + cols * pixel_width, pixel_width)
            lat_values = np.arange(
                lat_start, lat_start + rows * pixel_height, pixel_height)

            with rasterio.open(
                output_path,
                'w',
                driver='GTiff',
                height=rows,
                width=cols,
                count=1,
                dtype=np.float32,
                crs=geoProjection,
                transform=geoTransform,
            ) as output_dataset:
                output_dataset.write(ndvi, 1)

                metadata = {
                    'Latitude': ' '.join(map(str, lat_values)),
                    'Longitude': ' '.join(map(str, lon_values))
                }

                output_dataset.update_tags(**metadata)

            print(f"Extract {path} : Completed")
