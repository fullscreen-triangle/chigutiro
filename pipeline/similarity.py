import os
import networkx as nx
from sklearn.cluster import DBSCAN
import numpy as np
from rhythmic_analysis import compare_features

def load_graph(graph_file):
    if os.path.exists(graph_file):
        return nx.read_gpickle(graph_file)
    return nx.Graph()

def save_graph(graph, graph_file):
    nx.write_gpickle(graph, graph_file)

def update_similarity_graph(processed_tracks, graph_file):
    G = load_graph(graph_file)
    for track_a, features_a in processed_tracks.items():
        for track_b, features_b in processed_tracks.items():
            if track_a != track_b:
                distance = compare_features(features_a, features_b)
                G.add_edge(track_a, track_b, weight=distance)
    save_graph(G, graph_file)
    return G



def cluster_segments(processed_tracks, eps=1.5, min_samples=2):
    """
    Cluster segments using DBSCAN to identify potential VIPs/Dubplates.
    :param processed_tracks: Dictionary of processed track features
    :param eps: Maximum distance between samples for clustering
    :param min_samples: Minimum samples per cluster
    :return: Clusters and outliers
    """
    features = [list(track.values()) for track in processed_tracks.values()]
    feature_matrix = np.array(features)

    clustering = DBSCAN(eps=eps, min_samples=min_samples).fit(feature_matrix)
    labels = clustering.labels_

    clusters = {}
    for label, track in zip(labels, processed_tracks.keys()):
        if label not in clusters:
            clusters[label] = []
        clusters[label].append(track)
    return clusters
