import os
import piexif
from datetime import datetime
import glob
from tqdm import tqdm

# Set the directory path to your folder containing JPEG images
directory_path = '/Volumes/SCANS/DCIM/100COACH'

# Supported image formats for EXIF data manipulation with piexif
supported_formats = ['.jpg', '.jpeg', '.JPG', '.JPEG']


# Function to update the EXIF capture date
def update_capture_date(file_path):
    # Format the current datetime to EXIF date format
    exif_date = datetime.now().strftime("%Y:%m:%d %H:%M:%S")

    # Try to load existing EXIF data, if any
    try:
        exif_dict = piexif.load(file_path)
    except Exception as e:
        print(f"Error loading EXIF data for {file_path}: {e}")
        return

    # Update the EXIF capture date in both the '0th' and 'Exif' groups
    exif_dict['0th'][piexif.ImageIFD.DateTime] = exif_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = exif_date
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = exif_date

    # Generate the new EXIF bytes
    exif_bytes = piexif.dump(exif_dict)

    # Write the new EXIF data back to the image
    try:
        piexif.insert(exif_bytes, file_path)
        print(f"Updated EXIF capture date for {file_path}")
    except Exception as e:
        print(f"Error updating EXIF data for {file_path}: {e}")


# Loop through all files in the directory and update their capture date if supported
for root, dirs, files in os.walk(directory_path):
    for file in files:
        if any(file.endswith(ext) for ext in supported_formats):
            update_capture_date(os.path.join(root, file))