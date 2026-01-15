import os
import csv

def rename_files_from_csv(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            old_path = row.get("filepath")
            new_base_name = row.get("new_name")

            if not old_path or not new_base_name:
                continue

            if not os.path.exists(old_path):
                print(f"SKIP (not found): {old_path}")
                continue

            directory = os.path.dirname(old_path)
            _, extension = os.path.splitext(old_path)

            new_path = os.path.join(directory, new_base_name + extension)

            if os.path.exists(new_path):
                print(f"SKIP (already exists): {new_path}")
                continue

            os.rename(old_path, new_path)
            print(f"RENAMED: {old_path} -> {new_path}")

if __name__ == "__main__":
    csv_file = "filepaths.csv"
    rename_files_from_csv(csv_file)