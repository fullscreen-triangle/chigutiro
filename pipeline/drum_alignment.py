from scipy.signal import correlate
import numpy as np

def align_amen_break(song_y, song_sr, amen_y, amen_sr):
    min_len = min(len(song_y), len(amen_y))
    song_y, amen_y = song_y[:min_len], amen_y[:min_len]
    correlation = correlate(song_y, amen_y, mode="full")
    return np.argmax(correlation) - len(song_y)
