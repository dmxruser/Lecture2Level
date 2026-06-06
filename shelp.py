import librosa
import numpy as np
from moviepy import VideoFileClip


def convert(filename):
    # Converts MP4 to MP3 for processing
    output_filename = filename.replace(".mp4", ".mp3")
    clip = VideoFileClip(filename)
    if clip.audio is not None:
        clip.audio.write_audiofile(output_filename, codec='libmp3lame')
    else:
        raise ValueError("The uploaded MP4 file does not contain an audio track.")
    clip.close()
    return output_filename

import soundfile as sf

def speed_up(input_path, output_path, speed_factor):
    y, sr = librosa.load(input_path)
    y_fast = librosa.effects.time_stretch(y, rate=speed_factor)
    sf.write(output_path, y_fast, sr)
    return output_path


def load_song(filename):
    # Loads songs for ovbious reasons
    y, sr = librosa.load(filename)
    return y, sr
def calc_average(arr, smpl):
    # Calculates the average for checking a lot of things
    avg = np.average(np.abs(arr))
    return avg
def get_lenghts(arr, smpl, avg):
    lengths = [] # Total sec of each part
    threshold = 0.20 * avg # To use for checking if lenght is somewhat in average
    for i in range(0, len (arr), smpl):
        secvol = np.average(np.abs(arr[i:i+smpl])) # To save on costs and tmie
        if secvol > avg:
            lengths.append(3)
        elif (avg - threshold) <= secvol <= (avg + threshold):
            lengths.append(2)
        elif secvol < avg:
            lengths.append(2)
        else:
            lengths.append(2)
    return lengths