import sys

from functions.get_article import get_article
from functions.transform_article import transform_article
from functions.write_article import write_article

def main():    
    # get the article file
    get_article(sys.argv)
    # transform the file contents
    transform_article()
    # write the new file into the output folder
    write_article()
    
main()