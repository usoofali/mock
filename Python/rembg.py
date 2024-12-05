import rembg
import numpy as np
from PIL import Image
import os

def remove_background(file_path):
    """Remove the background from an image file."""
    with Image.open(file_path) as img:
        
        # Convert image to numpy array
        print("Processing started.....")
        img_array = np.array(img)
        print("Processing.....1")
        # Remove the background using rembg
        output_array = rembg.remove(img_array)
        print("Processing started.....2")
        # Create a PIL Image from the output array
        output_image = Image.fromarray(output_array)
        print("Processed.....")
        
        # Define new file path for the image with removed background
        new_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
        print("Saving.........")
        # Save the output image
        output_image.save(new_file_path, format='JPG')
        print("Image saved")
        return new_file_path

def process_images(folder_path):
    """Process all image files in a specified folder to remove their backgrounds."""
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            try:
                new_file_path = remove_background(file_path)
                print(f"Processed: {new_file_path}")
            except Exception as e:
                print(f"Could not process {filename}: {e}")

folder_path = 'photos'
process_images(folder_path)
print("Processing complete.")
