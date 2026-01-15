import os
import csv

def list_files_to_csv(output_csv):
    root_directory = os.getcwd()
    filepaths = []

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            full_path = os.path.join(root, file)
            filepaths.append(full_path)

    with open(output_csv, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["filepath"])  # column A header
        for path in filepaths:
            writer.writerow([path])

if __name__ == "__main__":
    output_csv = "filepaths.csv"
    list_files_to_csv(output_csv)