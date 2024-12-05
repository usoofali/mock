import os
from data import names
def get_names(fullname):
    # Split the full name into parts
    names = fullname.split()

    # Check the number of names
    if len(names) == 2:
        firstname = names[0]
        lastname = names[1]
    elif len(names) == 3:
        firstname = " ".join(names[:2])  # Join the first two names
        lastname = names[2]
    else:
        raise ValueError("The name should contain either two or three parts.")

    return firstname, lastname

def main():
    passport_folder = 'Passport'
    signature_folder = 'Signature'
    output_folder = 'ID_Cards'
    os.makedirs(output_folder, exist_ok=True)
    
    photo_coords = (269, 439, 594, 861)     # Coordinates (left, top, right, bottom) for photo
    signature_coords = (357,1245, 590, 1291) # Coordinates (left, top, right, bottom) for signature
    name_coords = (230, 901, 767,961)     # Coordinates (left, top, right, bottom) for name
    adm_coords = (262, 1075, 729,1138)     # Coordinates (left, top, right, bottom) for adm
    dept_coords = (232,990, 767,1044)     # Coordinates (left, top, right, bottom) for department
    phone_coords = (268,1170, 720,1229)     # Coordinates (left, top, right, bottom) for department
    count = 0
    sql = "INSERT INTO `users` (`username`, `password`, `fullname`) VALUES\n"

    for photo_file in os.listdir(passport_folder):
        count += 1
        if photo_file.endswith(('.jpeg', '.jpg', '.png')):
            name_department = os.path.splitext(photo_file)[0]
            photo_path = os.path.join(passport_folder, photo_file)
            name, adm, bg, department, phone, email = name_department.split('_')
            dept, year, sn, phone = name.split('.')
            adm = dept + "/" + year + "/" + sn + "/" + phone
            std = names[adm]
            name = std[0]
            phone = std[1]
            output_path = os.path.join(output_folder, f'{name_department}_id_card.jpeg')
            fname, lname = get_names(name)
            
            sql += f"('{adm}', '{sn}', '{name}'),\n"
    print(sql)
                
if __name__ == '__main__':
    main()
