import os
import shutil

from utils.constants import  PATH_TO_TRANSFORMS

# function to get all txt files from the input folder
def get_article(arguments):
    # check if the user trying to pass more than 1 file address
    if len(arguments) != 2:
        print("Please pass only one file path as an argument.")
        exit(1)
    
    # make sure the file passed is a txt file
    if not arguments[1].endswith(".txt"):
        print("Please pass a path of a .txt file")
        exit(1)
    
    # make sure the file exist
    if not os.path.exists(arguments[1]):
        print("Path does not exist! Please enter a valid .txt file path")
        exit(1)

    # remove the previous transform folder
    shutil.rmtree(PATH_TO_TRANSFORMS)

    # create a new transforms folder
    os.makedirs(PATH_TO_TRANSFORMS, exist_ok=True)

    # copy the input file into the transforms folder
    shutil.copy2(arguments[1], PATH_TO_TRANSFORMS)
    print("File successfully passed into the transforms folder!")