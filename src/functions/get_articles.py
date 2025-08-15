import os
import shutil

from utils.constants import PATH_TO_INPUTS, PATH_TO_TRANSFORMS

# function to get all txt files from the input folder
def get_articles():
    # get all the files inside the input folder
    files = os.listdir(PATH_TO_INPUTS)

    # remove the transforms folder
    shutil.rmtree(PATH_TO_TRANSFORMS)

    # create a new transforms folder
    os.makedirs(PATH_TO_TRANSFORMS, exist_ok=True)

    # copy all the files into the transforms folder
    for file in files:
        file_path = os.path.join(PATH_TO_INPUTS, file)
        # make sure it's a txt files
        if os.path.isfile(file_path) and file.endswith(".txt"):
            # copy the file into the transforms folder
            shutil.copy2(file_path, PATH_TO_TRANSFORMS)
            print(f"Copying {file} to {PATH_TO_TRANSFORMS}")
        else:
            print(f"Skipping {file} - Inputs must contain only .txt files.")