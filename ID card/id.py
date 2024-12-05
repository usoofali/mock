import os
from PIL import Image, ImageDraw, ImageFont
import warnings

# Ignore DeprecationWarning for the PIL textsize method
warnings.filterwarnings("ignore", category=DeprecationWarning)

def get_font_size(draw, text, max_width, max_height, initial_font_size=34, font_path="arial.ttf"):
    font_size = initial_font_size
    font = ImageFont.truetype(font_path, font_size)
    while True:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        if text_width <= max_width and text_height <= max_height:
            return font
        font_size -= 1
        font = ImageFont.truetype(font_path, font_size)

def resize_image_to_fit(image, target_coords):
    target_width = target_coords[2] - target_coords[0]
    target_height = target_coords[3] - target_coords[1]
    image.thumbnail((target_width, target_height), Image.LANCZOS)
    
    # Create a blank image with white background
    new_image = Image.new("RGB", (target_width, target_height), (255, 255, 255))
    # Calculate the position to paste the resized image to center it
    paste_x = (target_width - image.width) // 2
    paste_y = (target_height - image.height) // 2
    new_image.paste(image, (paste_x, paste_y))
    
    return new_image

def create_identity_card(photo_path, signature_path, name, adm, department, phone, photo_coords, signature_coords, name_coords, adm_coords, dept_coords, phone_coords, output_path):
    template = Image.open('identity_card.jpg')
    photo = Image.open(photo_path)
    signature = Image.open(signature_path)
    
    resized_photo = resize_image_to_fit(photo, photo_coords)
    resized_signature = resize_image_to_fit(signature, signature_coords)

     # Ensure the template and images are in the same mode
    if template.mode != resized_photo.mode:
        resized_photo = resized_photo.convert(template.mode)
    if template.mode != resized_signature.mode:
        resized_signature = resized_signature.convert(template.mode)

    template.paste(resized_photo, (photo_coords[0], photo_coords[1]))
    template.paste(resized_signature, signature_coords)
    
    draw = ImageDraw.Draw(template)
    font_path = os.path.join("font", "ARIAL.TTF") # Adjust the path to the font file if necessary
    
    # Calculate and adjust font size for name
    name_font = get_font_size(draw, name, name_coords[2] - name_coords[0], name_coords[3] - name_coords[1], font_path=font_path)
    name_width, name_height = draw.textsize(name, font=name_font)
    name_x = name_coords[0] + (name_coords[2] - name_coords[0] - name_width) // 2
    name_y = name_coords[1] + (name_coords[3] - name_coords[1] - name_height) // 2
    draw.text((name_x, name_y), name, fill="black", font=name_font)
    
    # Calculate and adjust font size for adm
    adm_font = get_font_size(draw, adm, adm_coords[2] - adm_coords[0], adm_coords[3] - adm_coords[1], font_path=font_path)
    adm_width, adm_height = draw.textsize(adm, font=adm_font)
    adm_x = adm_coords[0] + (adm_coords[2] - adm_coords[0] - adm_width) // 2
    adm_y = adm_coords[1] + (adm_coords[3] - adm_coords[1] - adm_height) // 2
    draw.text((adm_x, adm_y), adm, fill="black", font=adm_font)

    # Calculate and adjust font size for department
    dept_font = get_font_size(draw, department, dept_coords[2] - dept_coords[0], dept_coords[3] - dept_coords[1], font_path=font_path)
    dept_width, dept_height = draw.textsize(department, font=dept_font)
    dept_x = dept_coords[0] + (dept_coords[2] - dept_coords[0] - dept_width) // 2
    dept_y = dept_coords[1] + (dept_coords[3] - dept_coords[1] - dept_height) // 2
    draw.text((dept_x, dept_y), department, fill="black", font=dept_font)

    # Calculate and adjust font size for phone
    phone_font = get_font_size(draw, phone, phone_coords[2] - phone_coords[0], phone_coords[3] - phone_coords[1], font_path=font_path)
    phone_width, phone_height = draw.textsize(phone, font=phone_font)
    phone_x = phone_coords[0] + (phone_coords[2] - phone_coords[0] - phone_width) // 2
    phone_y = phone_coords[1] + (phone_coords[3] - phone_coords[1] - phone_height) // 2
    draw.text((phone_x, phone_y), phone, fill="black", font=phone_font)
    
    template.save(output_path)

def main():
    passport_folder = 'Passport'
    signature_folder = 'Signature'
    output_folder = 'ID_Cards'
    os.makedirs(output_folder, exist_ok=True)
    
    photo_coords = (193, 330, 440, 658)     # Coordinates (left, top, right, bottom) for photo
    signature_coords = (200, 883, 570, 960) # Coordinates (left, top, right, bottom) for signature
    name_coords = (188, 666, 583, 716)     # Coordinates (left, top, right, bottom) for name
    adm_coords = (195, 807, 576, 856)     # Coordinates (left, top, right, bottom) for adm
    dept_coords = (188, 740, 583, 789)     # Coordinates (left, top, right, bottom) for department
    phone_coords = (450, 940, 603, 970)     # Coordinates (left, top, right, bottom) for department
    count = 0
    for photo_file in os.listdir(passport_folder):
        count += 1
        if photo_file.endswith(('.jpeg', '.jpg', '.png')):
            name_department = os.path.splitext(photo_file)[0]
            photo_path = os.path.join(passport_folder, photo_file)
            signature_path = os.path.join(signature_folder, photo_file)
            
            if os.path.exists(signature_path):
                name, adm, department = name_department.split('_')
                dept, year, sn, phone = adm.split('.')
                adm = dept + "/" + year + "/" + sn
                output_path = os.path.join(output_folder, f'{name_department}_id_card.jpeg')
                create_identity_card(photo_path, signature_path, name, adm, department, phone, photo_coords, signature_coords, name_coords, adm_coords, dept_coords, phone_coords,output_path)
                print(f'{count}. Created ID card for {name} in {department}')
            else:
                print(f'Signature file for {name_department} not found')

if __name__ == '__main__':
    main()
