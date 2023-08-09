import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

input_path = './qgis/tassled_cap_jan.tif'
output_path = './qgis/tassled_cap_jan_4326.tif'


with rasterio.open(input_path) as src:
    data = src.read()
    crs = src.crs
    transform = src.transform

# EPSG code for the target CRS
target_crs = 'EPSG:4326'

dst_crs = rasterio.crs.CRS.from_string(target_crs)
width, height = src.width, src.height
dst_transform, dst_width, dst_height = calculate_default_transform(
    crs, dst_crs, width, height, *src.bounds)


with rasterio.open(output_path, 'w', driver='GTiff', crs=dst_crs, transform=dst_transform, width=dst_width, height=dst_height, count=src.count, dtype=src.dtypes[0]) as dst:
    reproject(
        source=data,
        destination=rasterio.band(dst, 1),
        src_transform=transform,
        src_crs=crs,
        dst_transform=dst_transform,
        dst_crs=dst_crs,
        resampling=Resampling.nearest
    )
