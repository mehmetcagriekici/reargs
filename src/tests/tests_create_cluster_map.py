import unittest
from utils.create_cluster_map import create_cluster_map

    # tests to control if the function correctly creates a map
class TestsCreateClusterMap(unittest.TestCase):
    def test_overlapping_clusters(self):
        sentences = ["s0", "s1", "s2"]
        clusters = {
            "soft_cluster__(0,1)": (0,1),
            "soft_cluster__(0,2)": (0,2),
            "soft_cluster__(1,2)": (1,2)
        }
        paragraph_id = "p_0"

        result = {
            "p_0__0": {
                "cluster_type": "soft_cluster",
                "cluster_sentences": ["s0", "s1", "s2"],
                "cluster_indexes": [0, 1, 2]
            }
        }

        self.assertDictEqual(result, create_cluster_map(sentences, clusters, paragraph_id))

    def test_different_types_overlapping(self):
        sentences = ["s0", "s1", "s2"]
        clusters = {
            "soft_cluster__(0,1)": (0,1),
            "hard_cluster__(0,2)": (0,2)
        }
        paragraph_id = "p_1"

        result = {
            "p_1__0": {
                "cluster_type": "soft_cluster",
                "cluster_sentences": ["s0", "s1"],
                "cluster_indexes": [0, 1],
                "sub_cluster--(0, 2)": {
                    "cluster_type": "hard_cluster",
                    "cluster_sentences": ["s0", "s2"],
                    "cluster_indexes": [0, 2]
                }
            }
        }

        self.assertDictEqual(result, create_cluster_map(sentences, clusters, paragraph_id))

    def test_chain_merging(self):
        sentences = ["s0", "s1", "s2"]
        clusters = {
            "soft_cluster__(0,1)": (0,1),
            "soft_cluster__(1,2)": (1,2)
        }
        paragraph_id = "p_2"

        result = {
            "p_2__0": {
                "cluster_type": "soft_cluster",
                "cluster_sentences": ["s0", "s1", "s2"],
                "cluster_indexes": [0, 1, 2]
            }
        }

        self.assertDictEqual(result, create_cluster_map(sentences, clusters, paragraph_id))

    def test_duplicate_pairs(self):
        sentences = ["s0", "s1"]
        clusters = {
            "hard_cluster__(0,1)": (0,1),
            "hard_cluster__(1,0)": (1,0)
        }
        paragraph_id = "p_3"

        result = {
            "p_3__0": {
                "cluster_type": "hard_cluster",
                "cluster_sentences": ["s0", "s1"],
                "cluster_indexes": [0, 1]
            }
        }
        
        self.assertDictEqual(result, create_cluster_map(sentences, clusters, paragraph_id))  

if __name__ == "__main__":
    unittest.main()