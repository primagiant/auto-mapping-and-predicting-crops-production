import os
import fiona
import numpy as np
import tifffile
import csv


def generate_labels_classification(geojson_path):
    labels = {}
    with fiona.open(geojson_path, "r") as geojson:
        for feature in geojson:
            labels[feature["id"]] = [feature["properties"]["Classid"], feature["properties"]["Classtxt"]]
    return labels


def extract_mean_band(input_folder, output_folder, label_list, csv_name):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    input_files = os.listdir(input_folder)

    # Header data
    header = ['R', 'G', 'B', 'Vre1', 'Vre2', 'Vre3', 'Nir', 'Swir1', 'Swir2', 'NNir', 'Label_id', 'Label_txt']

    # Write the header to the output CSV file
    output_csv_file = os.path.join(output_folder, csv_name)
    with open(output_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    # Process each TIFF file in the input folder
    for i, filename in enumerate(input_files):
        if filename.endswith(".tif"):
            tiff_file_path = os.path.join(input_folder, filename)

            # Read the TIFF file
            tiff_data = tifffile.imread(tiff_file_path)

            # Extract band (reference sentinel 2 band)
            b2 = tiff_data[:, :, 0]
            b3 = tiff_data[:, :, 1]
            b4 = tiff_data[:, :, 2]
            b5 = tiff_data[:, :, 3]
            b6 = tiff_data[:, :, 4]
            b7 = tiff_data[:, :, 5]
            b8 = tiff_data[:, :, 6]
            b11 = tiff_data[:, :, 7]
            b12 = tiff_data[:, :, 8]
            b8a = tiff_data[:, :, 9]

             # Extract label (optional bisa n+1 atau n tergantung dengan data label)
            label = label_list[f"{i}"]

            for j in range(b2.shape[0]):
                for k in range(b2[j].shape[0]):
                        csv_row = [
                            b2[j][k], b3[j][k],
                            b4[j][k], b5[j][k],
                            b6[j][k], b7[j][k],
                            b8[j][k], b11[j][k],
                            b12[j][k], b8a[j][k],
                            label[0], label[1],
                        ]

                        # Write the CSV row to the output CSV file
                        output_csv_file = os.path.join(output_folder, csv_name)
                        with open(output_csv_file, mode='a', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(csv_row)

            print(f"{i} shapefile exported")


if __name__ == "__main__":

    """ Label Information
    0 = water
    1 = vegetation_type1 (no crops)
    2 = vegetation_type2 (with crops)
    3 = forest
    4 = building
    """
    geojson_path = './shapefile/geoJson/100_each_4326.geojson'
    labels = generate_labels_classification(geojson_path)

    input_folder = "./output/rgb/crop/2020/all-100-poligon"
    output_folder = "./csv/rgb/2020/jan"
    csv_name = "poligon-500-result.csv"
    extract_mean_band(input_folder, output_folder, labels, csv_name)
