from vegetation_index import psri_index
from osgeo import gdal
import numpy as np
import zipfile
import os


# adjust with band data filename
target_band = ["B04_10m.jp2", "B08_10m.jp2"]
print(target_band)

zip_folder_path = "./data/2020"
files = os.listdir(zip_folder_path)

# make folder if not exits
output_folder = f"./index/psri/2020"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# shp file
shp_file = './shp/poly_paddy_13.5768_101.717.shp'

for path in files:
    zip_file_path = f'{zip_folder_path}/{path}'
    file_inside_zip = []

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        for file_name in zip_file.namelist():
            for target_fl in target_band:
                if file_name.endswith(target_fl):
                    file_inside_zip.append(file_name)

    # config to accesing the zip
    gdal.VSICurlClearCache()
    gdal.PushErrorHandler('CPLQuietErrorHandler')
    gdal.SetConfigOption('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', 'jp2')
    gdal.SetConfigOption('CPL_VSIL_CURL_ALLOWED_EXTENSIONS', 'jp2')

    # Open Using Gdal (adjust it with target_band)
    b8 = gdal.Open('/vsizip/' + zip_file_path + '/' + file_inside_zip[0])
    b4 = gdal.Open('/vsizip/' + zip_file_path + '/' + file_inside_zip[1])

    geoTransform = b4.GetGeoTransform()
    geoProjection = b4.GetProjection()

    nir = b8.GetRasterBand(1).ReadAsArray().astype(np.float32)
    red = b4.GetRasterBand(1).ReadAsArray().astype(np.float32)

    psri = psri_index(red, nir)

    # Save ram
    b4 = None
    b8 = None
    nir = None
    red = None

    # save psri
    driver = gdal.GetDriverByName('GTiff')
    output_path = f'{output_folder}/{path.split(".")[0]}.tif'
    cols, rows = psri.shape

    lon_start = geoTransform[0]
    lat_start = geoTransform[3]
    pixel_width = geoTransform[1]
    pixel_height = geoTransform[5]

    lon_values = np.arange(lon_start, lon_start +
                           cols * pixel_width, pixel_width)
    lat_values = np.arange(lat_start, lat_start + rows *
                           pixel_height, pixel_height)

    output_dataset = driver.Create(
        output_path, cols, rows, 1, gdal.GDT_Float32)
    output_dataset.GetRasterBand(1).WriteArray(psri)

    output_dataset.SetGeoTransform(geoTransform)
    output_dataset.SetProjection(geoProjection)

    metadata = {
        'Latitude': ' '.join(map(str, lat_values)),
        'Longitude': ' '.join(map(str, lon_values))
    }

    output_dataset.SetMetadata(metadata)

    print(f"Extract {path} : Completed")
