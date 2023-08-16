import rasterio
import joblib
import pandas as pd
import numpy as np

loaded_model = joblib.load('./model/model8.joblib')

list = []

with rasterio.open('./qgis/clipped_tc_jan_2.tif') as src:

    metadata = src.meta

    data_brightness = src.read(1)
    data_greenness = src.read(2)
    data_wetness = src.read(3)

    for row in range(data_brightness.shape[0]):
        rows = []
        for col in range(data_brightness.shape[1]):
            pixel = pd.DataFrame({
                'Brightness': [data_brightness[row][col]],
                'Greenness': [data_greenness[row][col]],
                'Wetness': [data_wetness[row][col]]
            })
            result = loaded_model.predict(pixel)
            rows.append(result[0])
        list.append(rows)
        print(f"complete appending row : {row}")
    print("comleted")

    new_array = np.array(list)

    output_tif_path = './output/lulc/_jan_2020.tif'

    metadata.update({
        'count': 1,
        'dtype': new_array.dtype.name
    })

    # Create the new GeoTIFF file and write the new array
    with rasterio.open(output_tif_path, 'w', **metadata) as dst:
        dst.write(new_array, 1)
