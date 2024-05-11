import os
import piexif
from datetime import datetime
from PIL import Image
import glob
from tqdm import tqdm

# Set the directory path to your folder containing JPEG images
directory_path = '/Volumes/SCANS/DCIM/100COACH'
MIRROR_IMAGES = True


def encode_exif_date(date_str):
    return date_str.encode('utf-8')  # Ensure the date is in the correct byte format


def mirror_image(file_path):
    with Image.open(file_path) as img:
        mirrored_img = img.transpose(Image.FLIP_LEFT_RIGHT)
        mirrored_img.save(file_path)
        print(f"Mirrored image saved for {file_path}")


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


def prepend_random_string(file_paths):
    random_string = os.urandom(2).hex()
    for file_path in file_paths:
        new_file_path = os.path.join(os.path.dirname(file_path), f"{random_string}_{os.path.basename(file_path)}")
        os.rename(file_path, new_file_path)
        print(f"Renamed {file_path} to {new_file_path}")


def main():
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')) and not file.startswith('._'):
                file_path = os.path.join(root, file)
                update_capture_date(file_path)
                if MIRROR_IMAGES:
                    mirror_image(file_path)
                prepend_random_string([file_path])
            else:
                print(f"Skipping non-image or system file: {file}")


if __name__ == '__main__':
    main()