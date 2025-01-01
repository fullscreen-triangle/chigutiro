import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def visualize_mix_signature(graph, metrics, output_path):
    pos = nx.spring_layout(graph, seed=42)
    node_colors = [
        "red" if metrics[node].get("vip_likelihood", False) else "blue"
        for node in graph.nodes
    ]
    nx.draw(
        graph, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=10
    )
    plt.savefig(output_path)
    plt.close()



def plot_heatmap(metrics, times, output_path="results/mix_heatmap.png"):
    """
    Plot a heatmap of metrics over time.
    :param metrics: Dictionary of metrics with time as keys
    :param times: List of time intervals
    :param output_path: Path to save the heatmap
    """
    metric_names = list(metrics.keys())
    data = np.array([metrics[metric] for metric in metric_names])

    plt.figure(figsize=(12, 6))
    plt.imshow(data, aspect="auto", cmap="viridis", origin="lower")
    plt.colorbar(label="Metric Value")
    plt.xticks(ticks=np.arange(len(times)), labels=[f"{t:.2f}s" for t in times], rotation=45)
    plt.yticks(ticks=np.arange(len(metric_names)), labels=metric_names)
    plt.xlabel("Time")
    plt.ylabel("Metrics")
    plt.title("Mix Metrics Heatmap")
    plt.savefig(output_path)
    plt.close()
    print(f"Heatmap saved at {output_path}")

def plot_bassline(bassline, sr, output_path="results/bassline.png"):
    """
    Plot the extracted bassline.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(bassline)
    plt.title("Bassline Frequencies")
    plt.xlabel("Time")
    plt.ylabel("Amplitude")
    plt.savefig(output_path)
    plt.close()