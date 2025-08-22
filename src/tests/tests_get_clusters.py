import unittest
from utils.get_clusters import get_clusters
from utils.constants import SOFT_CLUSTER_KEY, HARD_CLUSTER_KEY

class TestsGetClusters(unittest.TestCase):
    # test if the function returns the elements with higher scores from a 2 dimentional array without any duplications
    def test_get_clusters(self):
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
        self.assertDictEqual({f'{SOFT_CLUSTER_KEY}__(0, 1)': (0, 1), f'{HARD_CLUSTER_KEY}__(3, 7)': (3, 7)}, get_clusters(sentences) )


if __name__ == "__main__":
    unittest.main()
