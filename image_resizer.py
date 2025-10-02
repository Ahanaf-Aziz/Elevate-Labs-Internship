import os
from PIL import Image

def resize_images(input_folder, output_folder, target_size=(800, 600), output_format='JPEG'):
    """
    Resize and convert all images in input_folder, save to output_folder.
    Args:
        input_folder (str): Path to the folder containing input images.
        output_folder (str): Path to the folder to save resized images.
        target_size (tuple): Target size as (width, height).
        output_format (str): Format to save images (e.g., 'JPEG', 'PNG').
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)
        if not os.path.isfile(file_path):
            continue

        try:
            with Image.open(file_path) as img:
                img = img.convert("RGB")  # Ensures compatibility
                img_resized = img.resize(target_size, Image.ANTIALIAS)
                base_name, _ = os.path.splitext(filename)
                output_file = os.path.join(output_folder, f"{base_name}.{output_format.lower()}")
                img_resized.save(output_file, output_format)
                print(f"Resized and saved: {output_file}")
        except Exception as e:
            print(f"Failed to process {filename}: {e}")

if __name__ == "__main__":
    # Example usage
    input_folder = "images"
    output_folder = "resized"
    target_size = (800, 600)  # Change as needed
    output_format = "JPEG"    # Change as needed

    resize_images(input_folder, output_folder, target_size, output_format)
