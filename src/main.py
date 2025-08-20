import sys

from functions.get_article import get_article
from functions.transform_article import transform_article

def main():    
    # get the article file
    get_article(sys.argv)
    # transform the file contents and write the output
    transform_article()
    
main()