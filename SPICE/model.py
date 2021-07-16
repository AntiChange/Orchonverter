import tensorflow as tf
import tensorflow_hub as hub

from data_prep import audio_samples

# Loading the SPICE model is easy:
model = hub.load("https://tfhub.dev/google/spice/2")

# We now feed the audio to the SPICE tf.hub model to obtain pitch and uncertainty outputs as tensors.
model_output = model.signatures["serving_default"](tf.constant(audio_samples, tf.float32))

pitch_outputs = model_output["pitch"]
uncertainty_outputs = model_output["uncertainty"]

# 'Uncertainty' basically means the inverse of confidence.
confidence_outputs = 1.0 - uncertainty_outputs

# fig, ax = plt.subplots()
# fig.set_size_inches(20, 10)
# plt.plot(pitch_outputs, label='pitch')
# plt.plot(confidence_outputs, label='confidence')
# plt.legend(loc="lower right")
# plt.show()

confidence_outputs = list(confidence_outputs)
pitch_outputs = [ float(x) for x in pitch_outputs]

indices = range(len (pitch_outputs))
confident_pitch_outputs = [ (i,p)  
  for i, p, c in zip(indices, pitch_outputs, confidence_outputs) if  c >= 0.8  ]
confident_pitch_outputs_x, confident_pitch_outputs_y = zip(*confident_pitch_outputs)
 
# fig, ax = plt.subplots()
# fig.set_size_inches(20, 10)
# ax.set_ylim([0, 1])
# plt.scatter(confident_pitch_outputs_x, confident_pitch_outputs_y, )
# plt.scatter(confident_pitch_outputs_x, confident_pitch_outputs_y, c="r")

# plt.show()

def output2hz(pitch_output):
  # Constants taken from https://tfhub.dev/google/spice/2
  PT_OFFSET = 25.58
  PT_SLOPE = 63.07
  FMIN = 10.0;
  BINS_PER_OCTAVE = 12.0;
  cqt_bin = pitch_output * PT_SLOPE + PT_OFFSET;
  return FMIN * 2.0 ** (1.0 * cqt_bin / BINS_PER_OCTAVE)
    
confident_pitch_values_hz = [ output2hz(p) for p in confident_pitch_outputs_y ]
print(confident_pitch_values_hz)
print(len(confident_pitch_values_hz))

