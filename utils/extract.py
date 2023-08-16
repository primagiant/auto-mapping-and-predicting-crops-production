"""
this file is for converting the masking the tiff file with Geojson File
"""
import os
import fiona
import rasterio
from rasterio.mask import mask
from shapely.geometry import shape


""" the first input is the raster_path (the TIFF path)
the second input is the geojson_path (generate manual on Qgis and converted into GeoJson file byy Online source website)
the third input is the output folder where the extracted data will be stored """


def extract_data_from_polygon(raster_path, geojson_path, output_folder):
    # Open the raster file
    with rasterio.open(raster_path) as src:

        # Open the GeoJSON file
        with fiona.open(geojson_path, "r") as geojson:
            for feature in geojson:
                # Convert GeoJSON geometry to Shapely geometry
                geom = shape(feature["geometry"])

                # Perform the raster extraction using the mask() function
                out_image, out_transform = mask(src, [geom], crop=True)
                out_meta = src.meta.copy()

                # Update the metadata for the output raster
                out_meta.update(
                    {
                        "driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform,
                    }
                )

                # Save the extracted raster as a new GeoTIFF file
                out_path = os.path.join(
                    output_folder, f"extracted_{feature['id']}.tif")
                with rasterio.open(out_path, "w", **out_meta) as dest:
                    dest.write(out_image)


if __name__ == "__main__":

    raster_path = "./qgis/2020/jan/stack_bands.tif"
    geojson_path = './shapefile/geoJson/100_each_4326.geojson'
    output_folder = './output/rgb/crop/2020/all-100-poligon'

    # make folder if not exits
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with rasterio.open(raster_path) as src:
        print(f"Raster CRS : {src.crs}")
        raster_crs = src.crs

    with fiona.open(geojson_path, "r") as geojson:
        print(f"Geojson CRS : {geojson.crs}")
        geojson_crs = geojson.crs

    # check if the crs same
    if (raster_crs == geojson_crs):
        # extract the data
        extract_data_from_polygon(raster_path, geojson_path, output_folder)
    else:
        print('make sure the crs is same')
