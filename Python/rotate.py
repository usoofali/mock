import os
from PIL import Image

# Specify the folder path containing the images
folder_path = "rotates"

# Loop through each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith((".jpg", ".jpeg", ".png", ".bmp", ".tiff")):  # Check for valid image file types
        # Construct full file path
        file_path = os.path.join(folder_path, filename)
        
        # Open the image
        with Image.open(file_path) as img:
            # Rotate the image by 90 degrees
            rotated_img = img.rotate(90, expand=True)
            
            # Save the rotated image (overwrite the original or save with a new name)
            rotated_img.save(file_path)  # You can add a prefix/suffix to filename if you don't want to overwrite
            print(f"Rotated and saved {filename}")
