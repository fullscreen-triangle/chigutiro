import numpy as np
# Monkey-patch NumPy for compatibility with madmom
np.float = float
np.int = int

import os
import json
from audio_processing import process_audio
from mix_analysis import segment_mix, extract_segments
from similarity import update_similarity_graph, cluster_segments
from visualization import visualize_mix_signature, plot_heatmap, plot_bassline
from rhythmic_analysis import save_combined_results

def analyze_mix(mix_file, amen_break_file, db_dir="database", output_dir="results"):
    """
    Analyze a mix to identify VIPs and Dubplates, extract bassline and key features, and visualize results.
    """
    os.makedirs(db_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Step 1: Segment the mix
    print("Segmenting mix...")
    segments = segment_mix(mix_file)
    segment_dir = extract_segments(mix_file, segments)

    # Step 2: Process each segment
    print("Processing segments...")
    processed_tracks = {}
    for segment_file in os.listdir(segment_dir):
        segment_path = os.path.join(segment_dir, segment_file)
        features = process_audio(segment_path, amen_break_file)
        if features:
            processed_tracks[segment_path] = features

    # Step 3: Update and save the similarity graph
    print("Updating similarity graph...")
    graph_file = os.path.join(db_dir, "similarities.gpickle")
    similarity_graph = update_similarity_graph(processed_tracks, graph_file)

    # Step 4: Save combined metrics and visualizations
    print("Saving results...")
    metrics_file = os.path.join(db_dir, "metrics.json")
    save_combined_results(processed_tracks, metrics_file)

    print("Generating heatmap...")
    times = [0.0] + segments
    plot_heatmap(
        {k: [f[k] for f in processed_tracks.values()] for k in processed_tracks[next(iter(processed_tracks))]},
        times,
        os.path.join(output_dir, "mix_heatmap.png"),
    )

    print("Generating bassline plots...")
    for segment_file, features in processed_tracks.items():
        bassline_output = os.path.join(output_dir, "{}_bassline.png".format(os.path.basename(segment_file)))
        plot_bassline(features["bassline"], features.get("sr", 22050), bassline_output)

    print("Clustering segments...")
    clusters = cluster_segments(processed_tracks)
    print("Clusters: {}".format(clusters))

    print("Visualizing mix signature...")
    visualize_mix_signature(similarity_graph, processed_tracks, os.path.join(output_dir, "mix_signature.png"))

    print("Analysis complete.")
    return metrics_file, graph_file
