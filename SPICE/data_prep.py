from pydub import AudioSegment
from scipy.io import wavfile
import os

from model import main_model

def main (file_name):

  # Function that converts the user-created audio to the format that the model 
  # expects: bitrate 16kHz and only one channel (mono).

  EXPECTED_SAMPLE_RATE = 16000

  def convert_audio_for_model(user_file, output_file='converted_audio_file.wav'):
    audio = AudioSegment.from_file(user_file)
    audio = audio.set_frame_rate(EXPECTED_SAMPLE_RATE).set_channels(1)
    audio.export(output_file, format="wav")
    return output_file

    # Converting to the expected format for the model
  # in all the input 4 input method before, the uploaded file name is at
  # the variable uploaded_file_name
  # file_name = ""
  converted_audio_file = convert_audio_for_model(file_name)
  # converted_audio_file = convert_audio_for_model("09-Jesus_fast_violin.wav")


  # Loading audio samples from the wav file:
  sample_rate, audio_samples = wavfile.read(converted_audio_file, 'rb')

  # Show some basic information about the audio.
  duration = len(audio_samples)/sample_rate
  print(f'Sample rate: {sample_rate} Hz')
  print(f'Total duration: {duration:.2f}s')
  print(f'Size of the input: {len(audio_samples)}')

  # # Let's listen to the wav file.
  # Audio(audio_samples, rate=sample_rate)

  MAX_ABS_INT16 = 32768.0
  audio_samples = audio_samples / float(MAX_ABS_INT16)

  best_notes_and_rests = main_model(audio_samples, duration)
  #delete output file
  os.remove(file_name)
  return best_notes_and_rests