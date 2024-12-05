from PIL import Image
import os

def get_image_size(file_path):
    """Get the size of a file in bytes."""
    return os.path.getsize(file_path)

def resize_and_pad_image(img, size):
    """Resize and pad image to fit within specified size."""
    # Resize image while maintaining aspect ratio
    img.thumbnail(size, Image.LANCZOS)
    
    # Create a new image with the desired size and a white background
    new_img = Image.new('RGB', size, (255, 255, 255))
    
    # Calculate position to paste the resized image
    left = (size[0] - img.width) // 2
    top = (size[1] - img.height) // 2
    
    new_img.paste(img, (left, top))
    return new_img

def resize_image(file_path, target_size, min_size, max_size):
    """Resize image to fit within target size while keeping file size between min_size and max_size."""
    with Image.open(file_path) as img:
        # Resize image to the target size
        
        img.thumbnail(target_size, Image.LANCZOS)
        
        # Create a temporary path to save the resized image
        temp_path = file_path.rsplit('.', 1)[0] + '_temp.jpg'
        img.save(temp_path, format='JPEG', optimize=True, quality=85)  # Save as JPG with initial quality
        
        # Adjust dimensions if the file size is outside the desired range
        while True:
            current_size = get_image_size(temp_path)
            if min_size <= current_size <= max_size:
                with Image.open(temp_path) as img:
                    img = resize_and_pad_image(img, (700, 800))
                    img.save(temp_path, format='JPEG', optimize=True, quality=85)
                break
            
            with Image.open(temp_path) as img:
                # Adjust dimensions proportionally
                width, height = img.size
                if current_size > max_size:
                    new_size = (int(width * 0.9), int(height * 0.9))
                else:
                    new_size = (int(width * 1.1), int(height * 1.1))
                
                # Apply new size
                img = img.resize(new_size, Image.LANCZOS)
                img.save(temp_path, format='JPEG', optimize=True, quality=85)
        
        # Replace the original file with the resized JPG image
        new_file_path = file_path.rsplit('.', 1)[0] + '.jpg'
        os.replace(temp_path, new_file_path)
        return new_file_path

def process_images(folder_path):
    """Process all image files in a specified folder."""
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    min_size = 100 * 1024  # Minimum file size in bytes (100 KB)
    max_size = 150 * 1024  # Maximum file size in bytes (150 KB)
    target_size = (1024, 768)  # Initial size for resizing
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        if os.path.isfile(file_path):
            try:
                new_file_path = resize_image(file_path, target_size, min_size, max_size)
                print(f"Processed: {new_file_path}")
            except Exception as e:
                print(f"Could not process {filename}: {e}")

folder_path = 'resize'
process_images(folder_path)
print("Processing complete.")
