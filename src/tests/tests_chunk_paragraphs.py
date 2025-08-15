import unittest
from utils.chunk_paragraphs import chunk_paragraphs

class TestsChunkParagraphs(unittest.TestCase):
    # test if the fucntion separates an article into paragraphs correctly
    def test_chunk_paragraphs(self):
        article ="""This is an article about nothing. This sentence is not a new paragraph.
This is a new line but not a new paragraph.
This one and all above should be in the same array element.

This is another paragraph. And this is the rest of the new paragraph.
This is a new line in the new paragraph.
And all above including this one should be the second element of the paragraphs array.

And let's go for a third paragraph because why not. We may need it or not. I am telling you writing tests are not something you should leave to last. Write tests and tests after each dot."""
        result = [
"""This is an article about nothing. This sentence is not a new paragraph.
This is a new line but not a new paragraph.
This one and all above should be in the same array element."""
             ,
"""This is another paragraph. And this is the rest of the new paragraph.
This is a new line in the new paragraph.
And all above including this one should be the second element of the paragraphs array."""
            , 
"""And let's go for a third paragraph because why not. We may need it or not. I am telling you writing tests are not something you should leave to last. Write tests and tests after each dot."""
        ]

        self.assertListEqual(chunk_paragraphs(article), result)

if __name__ == "__main__":
    unittest.main()