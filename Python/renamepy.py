import os

def rename_files(source_folder, destination_folder):
    """Renames all files in the source folder to the destination folder."""

    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)
        name = filename.split("_")
        destination_path = os.path.join(destination_folder, name[0])
        os.rename(source_path, destination_path)

if __name__ == "__main__":
    source_folder = "1232"
    destination_folder = "assets"

    rename_files(source_folder, destination_folder)