import librosa
import os
import numpy as np

def segment_mix(audio_file):
    y, sr = librosa.load(audio_file, sr=None)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    frames = librosa.frames_to_time(np.arange(len(onset_env)), sr=sr)
    segments = [0.0] + list(frames[np.diff(onset_env) > 0.05]) + [frames[-1]]
    return segments

def extract_segments(audio_file, segments, output_dir="segments"):
    y, sr = librosa.load(audio_file, sr=None)
    os.makedirs(output_dir, exist_ok=True)
    for i, (start, end) in enumerate(zip(segments[:-1], segments[1:])):
        segment_file = os.path.join(output_dir, f"segment_{i + 1}.wav")
        librosa.output.write_wav(segment_file, y[int(start * sr):int(end * sr)], sr)
    return output_dir
