import os
import shutil

from utils.constants import PATH_TO_OUTPUT

# function to create an output -prints to cli and creates a txt file- from output map
def write_output(output_map):
    # create a txt file inside the output folder

    # remove the previous output folder
    if os.path.exists(PATH_TO_OUTPUT):
        shutil.rmtree(PATH_TO_OUTPUT)

    # create a new output folder
    os.makedirs(PATH_TO_OUTPUT, exist_ok=True)

    # write the output file
    with open(os.path.join(PATH_TO_OUTPUT, "output.txt"), mode="w") as f:
        f.write(output_map)
        f.close()
    
    # print the putput map on the cli
    print(output_map)
