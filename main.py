from pydub.utils import make_chunks
from pydub import AudioSegment
import pydub
from pathlib import Path
import glob
import pickle
import zipfile
import os
import json
import random
import itertools as it

import numpy as np
import pandas as pd

from scipy import signal
from scipy.io import wavfile

import sklearn as sk
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from scipy import stats

import matplotlib.pyplot as plt

# Constant parameters for model
REMOVE_BEGIN = 0.0
REMOVE_END = 0.0
FILTER_INTENSITY = 0


# Function to obtain spectrogram from wav file
def get_spectrogram(file_name, remove_begin=0, remove_end=0, filter_intensity=0):
    """
    Provide spectrogram associated to a WAV file
    To focus only on relevant information:
    - optionally removes begin and end of WAV file (ratio between 0 and 1)
    - optionally removes time buckets whose frequency intensities are all under a given threshold (absolute)
    """

    # Reading WAV file
    sample_rate, samples = wavfile.read(file_name)

    # Removing begin and end of samples since they may not be relevant
    length = len(samples)

    if remove_begin > 0:

        samples_to_remove = int(length * remove_begin)
        samples = samples[samples_to_remove:]

    if remove_end > 0:

        samples_to_remove = int(length * remove_end)
        samples = samples[:-samples_to_remove]

    # Computing spectogram
    frequencies, times, spectrogram = signal.spectrogram(
        samples, fs=sample_rate, nperseg=1024)

    # Getting max intensity for each time bucket
    max_intensity = np.amax(spectrogram, axis=0)

    # Filtering on max intensity
    selections = np.array(max_intensity > filter_intensity)

    return frequencies, times[selections], spectrogram[:, selections], max_intensity[selections], sample_rate, samples

# Function to display spectrogram


def display_spectrogram(frequencies, times, spectrogram, sample_rate, samples):
    """
    Display spectrogram
    """

    fig, axs = plt.subplots(1, 3, figsize=(20, 5))

    # Plotting frequencies for a given time
    axs[0].plot(frequencies, spectrogram[:, 50])
    axs[0].set_ylabel('Intensity')
    axs[0].set_xlabel('Frequency [Hz]')
    axs[0].set_title("Frequencies at arbitrary given time")

    # Plotting spectrogram (method 1)
    axs[1].pcolormesh(times, frequencies, 10*np.log10(spectrogram))
    axs[1].set_ylabel('Frequency [Hz]')
    axs[1].set_xlabel('Time [sec]')
    axs[1].set_title("Spectrogram (method 1)")

    # Plotting spectogram (method 2)
    axs[2].specgram(samples, Fs=sample_rate, NFFT=25,
                    noverlap=5, detrend='mean', mode='psd')
    axs[2].set_ylabel('Frequency [Hz]')
    axs[2].set_xlabel('Time [sec]')
    axs[2].set_title("Spectrogram (method 2)")

    plt.show()


def prepare_data(file_name, samples, labels):

    # Getting spectrogram
    # Frequencies are frequency buckets
    # Times are time buckets
    # Intensities are intensities for each (frequency bucket, time bucket) couple
    # Max intensities are max intensities for each time bucket
    frequencies, times, intensities, max_intensities, _, _ = get_spectrogram(
        file_name,
        remove_begin=REMOVE_BEGIN,
        remove_end=REMOVE_END,
        filter_intensity=FILTER_INTENSITY)

    # Transposing spectrogram, to switch from frequencies x times to times x frequencies
    intensities = intensities.transpose()

    # Concatenating all time buckets in samples and labels sets
    # A time bucket is a list of 129 frequencies like [2.93450565e+01 5.87889600e+03 1.26233027e+04 2.72070879e+04 ... ]
    for time_bucket in intensities:

        samples.append(time_bucket)

        if labels is not None:

            # Pitch comes from metadata
            labels.append(value['pitch'])


# Loading Modal and Sclaer
model_name = './saved-model/valid_pitch_detection_model.pkl'
scaler_filename = './saved-model/valid_pitch_detection_scaler.pkl'

loaded_model = pickle.load(open(model_name, 'rb'))
loaded_scaler = pickle.load(open(scaler_filename, 'rb'))

samples_prediction = []

# # Preprocessing
# prepare_data('./Testing wav files/bass_synthetic_009-078-127.wav', samples_prediction, None)
# samples_prediction_scaled = loaded_scaler.transform(samples_prediction)
# samples_prediction_scaled = np.asarray(samples_prediction_scaled)

# # Prediction
# result = loaded_model.predict(samples_prediction_scaled)

# print(result)


# Beats per minute
BPM = 120

# Notes per beat
NPB = 8

# For example, let us work with 32nd notes
chunk_length_ms = float(60000 / BPM / NPB)

wavList = glob.glob("./SeparatedParts/*")
print(wavList)

instrumentDict = {}

os.makedirs("instruments")

for wav_file in wavList:
    current_audio = AudioSegment.from_file(wav_file, "wav")
    chunks = make_chunks(current_audio, chunk_length_ms)

    new_dir_name = wav_file.split("/")[-1]
    instrumentName_wav = new_dir_name.split("_")[-1]
    instrumentName = instrumentName_wav.split(".")[0]

    os.makedirs("instruments/" + instrumentName)

    instrumentDict[instrumentName] = []

    for i, chunk in enumerate(chunks):
        chunk_name = "chunk{0}.wav".format(i)
        file_path = "instruments/" + instrumentName + "/" + chunk_name
        print("exporting", chunk_name)
        chunk.export(file_path, format="wav")

instruments = glob.glob("./instruments/*")

for line in instruments:
    currentInstrument = line.split("/")[-1]
    currentInstrument = currentInstrument[12:]

    path = line + "/*"
    fileList = glob.glob(path)  # List of all wav files
    count = 0
    filePath = line + "/chunk" + str(count) + ".wav"

    filePath.replace("\\", "/")

    # replace with while(coumt < 7) for testing purposes Path(filePath)
    while (os.path.exists(filePath)):
        print(filePath)
        try:
            # Use pitch detection on every chunk
            samples_prediction = []

            # Preprocessing
            prepare_data(filePath, samples_prediction, None)
            samples_prediction_scaled = loaded_scaler.transform(
                samples_prediction)
            samples_prediction_scaled = np.asarray(samples_prediction_scaled)

            # Prediction
            result = loaded_model.predict(samples_prediction_scaled).tolist()

            mode = max(set(result), key=result.count)
            instrumentDict[currentInstrument].append(mode)

        except ValueError:
            instrumentDict[currentInstrument].append(-1)

        count += 1
        filePath = line + "/chunk" + str(count) + ".wav"

print(instrumentDict)
