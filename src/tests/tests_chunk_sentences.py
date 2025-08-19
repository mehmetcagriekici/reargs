import unittest
from utils.chunk_sentences import chunk_sentences

class TestsChunkSentences(unittest.TestCase):
    # test if the function separates a paragraph into sentences correctly
    def test_chunk_sentences(self):
        paragraph="""This is a paragraph.
This is a new line inside the paragraph, and a new sentence...
And who would knew? We can't... But I am telling you: Get this, you are writing unittests.
And this is the end of the paragraph."""       
        result = [
            """This is a paragraph.""", 
            """This is a new line inside the paragraph, and a new sentence...""",
            """And who would knew?""",
            """We can't...""",
            """But I am telling you: Get this, you are writing unittests.""",
            """And this is the end of the paragraph."""
        ]

        self.assertListEqual(chunk_sentences(paragraph), result)

if __name__ == "__main__":
    unittest.main()