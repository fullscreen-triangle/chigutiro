import numpy as np
import librosa
import json
import pandas as pd
import os

def calculate_metrics(y, sr):
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    inter_beat_intervals = np.diff(beat_times)
    return {
        "tempo": tempo,
        "avg_interval": np.mean(inter_beat_intervals),
        "std_interval": np.std(inter_beat_intervals),
    }

def compare_features(features_a, features_b):
    return np.linalg.norm(np.array(features_a["tempo"]) - np.array(features_b["tempo"]))



def save_combined_results(processed_tracks, output_path="database/metrics.json"):
    """
    Save all processed tracks' features and metrics to a combined JSON and optionally a CSV file.
    :param processed_tracks: Dictionary containing features and metrics for each segment.
    :param output_path: Path to save the combined results JSON file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Save as JSON
    with open(output_path, "w") as f:
        json.dump(processed_tracks, f, indent=4)

    # Optionally save as CSV
    csv_output_path = output_path.replace(".json", ".csv")
    track_data = []
    for track, features in processed_tracks.items():
        flattened_features = {"track": track}
        for key, value in features.items():
            # Flatten lists (e.g., bassline) by summarizing (e.g., mean, std) or truncating
            if isinstance(value, list):
                flattened_features[f"{key}_mean"] = sum(value) / len(value) if value else 0
                flattened_features[f"{key}_std"] = pd.Series(value).std() if len(value) > 1 else 0
            else:
                flattened_features[key] = value
        track_data.append(flattened_features)

    df = pd.DataFrame(track_data)
    df.to_csv(csv_output_path, index=False)

    print(f"Combined results saved as JSON: {output_path}")
    print(f"Combined results saved as CSV: {csv_output_path}")
