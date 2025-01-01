import librosa
import numpy as np
from rhythmic_analysis import calculate_metrics
from drum_alignment import align_amen_break

def detect_key(audio_file):
    """
    Detect the musical key of a song.
    """
    y, sr = librosa.load(audio_file, sr=None)
    y_harmonic, _ = librosa.effects.hpss(y)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    keys = [
        "C major", "C# major", "D major", "D# major", "E major", "F major",
        "F# major", "G major", "G# major", "A major", "A# major", "B major",
        "C minor", "C# minor", "D minor", "D# minor", "E minor", "F minor",
        "F# minor", "G minor", "G# minor", "A minor", "A# minor", "B minor",
    ]
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])
    profiles = np.vstack([np.roll(major_profile, i) for i in range(12)] +
                         [np.roll(minor_profile, i) for i in range(12)])

    correlation = np.dot(profiles, chroma_mean)
    best_key_index = np.argmax(correlation)
    return keys[best_key_index]

def extract_bassline(y, sr):
    """
    Extract bassline frequencies from the audio.
    """
    harmonic, _ = librosa.effects.hpss(y)
    bass = librosa.effects.percussive(harmonic, margin=2.0)
    return bass

def process_audio(file_path, amen_break_path):
    """
    Extract features, detect key, align Amen Break, and extract bassline.
    """
    y, sr = librosa.load(file_path, sr=None)
    amen_y, amen_sr = librosa.load(amen_break_path, sr=None)

    key = detect_key(file_path)
    alignments = align_amen_break(y, sr, amen_y, amen_sr)
    metrics = calculate_metrics(y, sr)
    bassline = extract_bassline(y, sr)

    return {
        **metrics,
        "key": key,
        "alignments": alignments,
        "bassline": bassline.tolist(),
    }
