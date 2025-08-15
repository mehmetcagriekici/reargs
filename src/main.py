# imports
from functions.get_articles import get_articles
from functions.transform_articles import transform_articles
from functions.write_articles import write_articles

def main():
    # get all the txt files from the input folder
    get_articles()
    # transform the file contents
    transform_articles()
    # write the new files into the output folder
    write_articles()
    

main()