import os
import shutil

# function to get all txt files from the input folder
def get_articles():
    path_to_input_folder = "input"
    path_to_transforms = "transforms"
    
    # get all the files inside the input folder
    files = os.listdir(path_to_input_folder)

    # copy all the files into the transforms folder
    for file in files:
        file_path = os.path.join(path_to_input_folder, file)
        # make sure it's a txt files
        if os.path.isfile(file_path) and file.endswith(".txt"):
            # copy the file into the transforms folder
            shutil.copy2(file_path, path_to_transforms)
            print(f"Copying {file} to {path_to_transforms}")
        else:
            print(f"skipping current file {file}. File must be a .txt")