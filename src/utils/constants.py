PATH_TO_TRANSFORMS = "transforms"
PATH_TO_OUTPUT = "output"

SOFT_CLUSTER_KEY = "soft_cluster"
HARD_CLUSTER_KEY = "hard_cluster"

# prev cluster sentence
# |
# |
# |
# current cluster sentence
CLUSTER_BODY_SKELETON = "\n|\n|\n|\n"

# cluster title
#      _s     |
#             cluster body...
CLUSTER_NODE_SKELETON = lambda _s: f"\n{_s}|\n"

MAX_SENTENCE_LENGTH = 40