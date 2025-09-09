import os
import shutil

from utils.constants import  PATH_TO_TRANSFORMS

# function to get all txt files from the input folder
def get_article(argument):
    # check if the user trying to pass more than 1 file address
    if not argument:
        print("Please pass only one file path as an argument.")
        exit(1)
    
    # make sure the file passed is a txt file
    if not argument.endswith(".txt"):
        print("Please pass a path of a .txt file")
        exit(1)
    
    # make sure the file exist
    if not os.path.exists(argument):
        print("Path does not exist! Please enter a valid .txt file path")
        exit(1)

    # remove the previous transform folder
    if os.path.exists(PATH_TO_TRANSFORMS):
        shutil.rmtree(PATH_TO_TRANSFORMS)

    # create a new transforms folder
    os.makedirs(PATH_TO_TRANSFORMS, exist_ok=True)

    # copy the input file into the transforms folder
    shutil.copy2(argument, PATH_TO_TRANSFORMS)
    print("File successfully copied into the transforms folder!")
