# function to create a map of similarities from sentences and clusters
def create_cluster_map(sentences, clusters, paragraph_id):
    # store the clusters with their corresponding sentences
    cluster_map = {}
    # to prevent duplicates create a cluster memo
    # append cluster indexes(curr/match: cluster_id).
    memo = {}

    # iterate over the clusters
    for cluster_key in clusters:
        # unpack the pair
        # curr -> current sentence index inside the paragraph
        # match -> similar sentence index inside the same paragraph
        (curr, match) = clusters[cluster_key]
        # get cluster type from the cluster key
        cluster_type = cluster_key.split("__")[0]
        # create a unique id for each cluster using curr
        cluster_id = memo.get(curr, f"{paragraph_id}__{curr}")
        # get the sentences that are matched
        cluster_sentences = [sentences[curr], sentences[match]]
        cluster_indexes = [curr, match]

        # handle already existing clusters  
        if curr in memo:
            # get the cluster inside the map and compare the types
            match_id = memo[curr]

            if cluster_type != cluster_map[match_id]["cluster_type"]:
                # create a sub cluster
                sub_cluster = create_cluster(cluster_type, cluster_sentences, cluster_indexes)
                # append sub cluster to the matching parent cluster's sub clusters arrray
                cluster_map[match_id]["sub_clusters"].append(sub_cluster)
            elif match not in memo:
                # add the match to the cluster sentences
                cluster_map[match_id]["cluster_sentences"].append(sentences[match])
                cluster_map[match_id]["cluster_indexes"].append(match)

            # add the match to memo with the cluster id - no need for sub cluster id
            memo[match] = match_id
            # move to the next iteration
            continue

        # initiate a cluster map element
        cluster_map[cluster_id] = create_cluster(
            cluster_type,
            cluster_sentences,
            cluster_indexes
        )

        # add match and curr to the memo saving the cluster id
        memo[match] = cluster_id
        memo[curr] = cluster_id
        
    # saved into similarities_paragraphs dict with the current paragraph id
    return cluster_map

# helper function to create a cluster
def create_cluster(cluster_type, cluster_sentences, cluster_indexes, sub_clusters=None):
    return dict(
            cluster_type=cluster_type,
            cluster_sentences=cluster_sentences,
            cluster_indexes=cluster_indexes,
            sub_clusters=sub_clusters if sub_clusters else []
        )
