import rasterio
import joblib
import pandas as pd
import numpy as np

loaded_model = joblib.load('./model/model8.joblib')

list = []

with rasterio.open('./qgis/2020/jan/clipped.tif') as src:

    metadata = src.meta

    b2 = src.read(1)
    b3 = src.read(2)
    b4 = src.read(3)
    b5 = src.read(4)
    b6 = src.read(5)
    b7 = src.read(6)
    b8 = src.read(7)
    b11 = src.read(8)
    b12 = src.read(9)
    b8a = src.read(10)

    for row in range(b2.shape[0]):
        rows = []
        for col in range(b2.shape[1]):
            pixel = pd.DataFrame({
                'R': [b2[row][col]],
                'G': [b3[row][col]],
                'B': [b4[row][col]],
                'Vre1': [b5[row][col]],
                'Vre2': [b6[row][col]],
                'Vre3': [b7[row][col]],
                'Nir': [b8[row][col]],
                'Swir1': [b11[row][col]],
                'Swir2': [b12[row][col]],
                'NNir': [b8a[row][col]],
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
