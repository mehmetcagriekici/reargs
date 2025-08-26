import unittest
from utils.get_clusters import get_clusters
from utils.constants import SOFT_CLUSTER_KEY, HARD_CLUSTER_KEY

class TestsGetClusters(unittest.TestCase):
    # test if the function returns the elements with higher scores from a 2 dimentional array without any duplications
    def test_get_clusters_paragraph(self):
        sentences = [
    "The weather is lovely today.",
    "It's so sunny outside!",
    "He drove to the stadium.",
    "The new movie is awesome",
    "The cat sits outside",
    "A man is playing guitar",
    "The dog plays in the garden",
    "The new movie is so great",
    "A woman watches TV",
]
        self.assertDictEqual({f'{SOFT_CLUSTER_KEY}__(0, 1)': (0, 1), f'{HARD_CLUSTER_KEY}__(3, 7)': (3, 7)}, get_clusters(sentences, is_sentence_level=True) )
    
    def test_get_clusters_article(self):
        paragraphs = [
    # 0
    "Albert Einstein developed the theory of relativity in the early 20th century, which revolutionized our understanding of space, time, and gravity. His famous equation E=mc^2 established the relationship between mass and energy, influencing physics for generations.",
    
    # 1
    "The theory of relativity, introduced by Einstein, changed modern physics by reshaping how scientists view space and time. The relationship between mass and energy, expressed as E=mc^2, became one of the most recognized equations in history.",
    
    # 2
    "Marie Curie conducted pioneering research on radioactivity, becoming the first woman to win a Nobel Prize and the only person awarded Nobel Prizes in two different sciences. Her discoveries laid the groundwork for medical applications of radiation.",
    
    # 3
    "Curie’s work on radioactivity fundamentally altered both physics and chemistry. She was awarded Nobel Prizes in both fields, and her findings are still applied in modern medicine, particularly in cancer treatments involving radiation.",
    
    # 4
    "The history of art shows how culture evolves across centuries. From cave paintings to digital installations, artists have always sought to express human experiences and emotions in visual form."
]

        result = {
    f'{HARD_CLUSTER_KEY}__(0, 1)': (0, 1),   # Einstein paragraphs → near duplicates
    f'{SOFT_CLUSTER_KEY}__(2, 3)': (2, 3)    # Curie paragraphs → clearly related, not verbatim
    # Paragraph 4 is unrelated → no cluster
}
        
        self.assertDictEqual(get_clusters(paragraphs), result)



if __name__ == "__main__":
    unittest.main()
