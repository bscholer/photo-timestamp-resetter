import os
import piexif
from datetime import datetime
import glob
from tqdm import tqdm

# Set the directory path to your folder containing JPEG images
directory_path = '/Volumes/SCANS/DCIM/100COACH'


def encode_exif_date(date_str):
    return date_str.encode('utf-8')  # Ensure the date is in the correct byte format


def update_capture_date(file_path):
    exif_date = datetime.now().strftime("%Y:%m:%d %H:%M:%S")
    encoded_date = encode_exif_date(exif_date)

    try:
        exif_dict = piexif.load(file_path)
        # Safely handle the problematic EXIF tag if present
        if 37500 in exif_dict['Exif']:
            del exif_dict['Exif'][37500]  # Remove problematic tag

        exif_dict['0th'][piexif.ImageIFD.DateTime] = encoded_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = encoded_date
        exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = encoded_date

        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, file_path)
        print(f"Updated EXIF capture date for {file_path}")
    except Exception as e:
        print(f"Error updating EXIF data for {file_path}: {e}")


for root, dirs, files in os.walk(directory_path):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg')) and not file.startswith('._'):
            file_path = os.path.join(root, file)
            update_capture_date(file_path)
        else:
            print(f"Skipping non-image or system file: {file}")