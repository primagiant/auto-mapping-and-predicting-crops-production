import os
import fiona
import numpy as np
import tifffile
import csv


def generate_labels_classification(geojson_path):
    labels = {}
    with fiona.open(geojson_path, "r") as geojson:
        for feature in geojson:
            class_id = feature["properties"]["Classid"]
            labels[feature["id"]] = class_id
    return labels


def extract_mean_band(input_folder, output_folder, label_list):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    input_files = os.listdir(input_folder)

    # Header data
    header = ['Brightness', 'Greenness', 'Wetness', 'Label']

    # Write the header to the output CSV file
    output_csv_file = os.path.join(output_folder, "result_pixel.csv")
    with open(output_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    # Process each TIFF file in the input folder
    for i, filename in enumerate(input_files):
        if filename.endswith(".tif"):
            tiff_file_path = os.path.join(input_folder, filename)

            # Read the TIFF file
            tiff_data = tifffile.imread(tiff_file_path)

            # Extract band 1, 2, and 3
            red = tiff_data[:, :, 0]
            green = tiff_data[:, :, 1]
            blue = tiff_data[:, :, 2]

             # Extract label (optional bisa n+1 atau n tergantung dengan data label)
            label = label_list[f"{i+1}"]

            for j in range(red.shape[0]):
                for k in range(red[j].shape[0]):
                    if red[j][k] != 0 and green[j][k] != 0 and blue[j][k] != 0:
                        # Create a CSV row containing the mean values and label
                        csv_row = [red[j][k], green[j][k], blue[j][k], label]

                        # Write the CSV row to the output CSV file
                        output_csv_file = os.path.join(output_folder, "result_pixel.csv")
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
    geojson_path = './shapefile/geoJson/newGeojson.geojson'
    labels = generate_labels_classification(geojson_path)

    # print(labels)

    input_folder = "./output/rgb/crop/2020/jan-50-tc"
    output_folder = "./csv/rgb/2020/jan"
    extract_mean_band(input_folder, output_folder, labels)
