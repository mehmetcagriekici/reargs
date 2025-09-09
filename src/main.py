import argparse

from functions.get_article import get_article
from functions.transform_article import transform_article

def main():
    # create a parser for command line arguments
    parser = argparse.ArgumentParser(
            prog="ReArgs",
            description="Find semantic similarities inside a text")
    # define the path argument
    parser.add_argument("--path", required=True)
    # get the passed args
    args = parser.parse_args()
    # get the article file and pass the path args
    get_article(args.path)
    # transform the file contents and write the output
    transform_article()
    
if __name__ == "__main__":
    main()
