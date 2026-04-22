from PIL import Image
import os

def tiff_to_jpeg_300dpi(input_folder, output_folder, target_dpi=300):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each file in the input folder
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)

        # Check if the file is a TIFF image
        if filename.lower().endswith(".tiff") or filename.lower().endswith(".tif"):

            # Open the TIFF image
            image = Image.open(input_path)

            # Get the original DPI from the TIFF metadata (default to 600 if not found)
            original_dpi = image.info.get("dpi", (600, 600))[0]

            # Calculate the scale factor based on original vs target DPI
            scale_factor = target_dpi / original_dpi

            # Resize the image based on the scale factor
            original_width, original_height = image.size
            new_width = int(original_width * scale_factor)
            new_height = int(original_height * scale_factor)
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)

            # Construct the output path with a .jpg extension
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".jpg")

            # Convert to RGB (required for JPEG) and save with target DPI metadata
            resized_image.convert("RGB").save(output_path, "JPEG", dpi=(target_dpi, target_dpi), quality=95)

            print(f"Converted {filename}:")
            print(f"  Format:     TIFF → JPEG")
            print(f"  DPI:        {int(original_dpi)} → {target_dpi}")
            print(f"  Dimensions: {original_width}x{original_height} → {new_width}x{new_height}")
            print(f"  Saved to:   {output_path}\n")

if __name__ == "__main__":
    # Update these paths to your folders
    input_folder = "W:\\SpcScanSpecial Collections\\Manuscript Collections - Scanned Material\\NashvillePrideCollection-MSS1126\\Binder 1"
    output_folder = "W:\\SpcScanSpecial Collections\\Manuscript Collections - Scanned Material\\NashvillePrideCollection-MSS1126\\Binder 1\\JPEG"

    tiff_to_jpeg_300dpi(input_folder, output_folder)