import os
import shutil

from utils.constants import PATH_TO_INPUTS, PATH_TO_TRANSFORMS

# function to get all txt files from the input folder
def get_articles():
    # to check if there are duplicate file names
    memo = {}

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
            # check if the file path already exist
            if file_path in memo:
                # skip and inform user
                print(f"{file} already exists, skipping to the next file... There must not be any duplicates in the inputs folder!")
            else:
                # add the file_path into the memo
                memo[file_path] = file_path
                # copy the file into the transforms folder
                shutil.copy2(file_path, PATH_TO_TRANSFORMS)
                print(f"Copying {file} to {PATH_TO_TRANSFORMS}")
        else:
            print(f"Skipping {file} - Inputs must contain only .txt files.")
    print("All .txt files successfully copied into the transforms folder.")