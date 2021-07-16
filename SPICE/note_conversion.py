# from model import indices, pitch_outputs, confidence_outputs, output2hz
import math
import statistics
import music21

def main_note (indices, pitch_outputs, confidence_outputs, output2hz):
  pitch_outputs_and_rests = [
      output2hz(p) if c >= 0.8 else 0
      for i, p, c in zip(indices, pitch_outputs, confidence_outputs)
  ]
  # print(pitch_outputs_and_rests)

  A4 = 440
  C0 = A4 * pow(2, -4.75)
  note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

  def hz2offset(freq):
    # This measures the quantization error for a single note.
    if freq == 0:  # Rests always have zero error.
      return None
    # Quantized note.
    h = round(12 * math.log2(freq / C0))
    return 12 * math.log2(freq / C0) - h


  # The ideal offset is the mean quantization error for all the notes
  # (excluding rests):
  offsets = [hz2offset(p) for p in pitch_outputs_and_rests if p != 0]
  # print("offsets: ", offsets)

  ideal_offset = statistics.mean(offsets)
  # print("ideal offset: ", ideal_offset)

  def quantize_predictions(group, ideal_offset):
    # Group values are either 0, or a pitch in Hz.
    non_zero_values = [v for v in group if v != 0]
    zero_values_count = len(group) - len(non_zero_values)

    # Create a rest if 80% is silent, otherwise create a note.
    if zero_values_count > 0.7 * len(group):
      # Interpret as a rest. Count each dropped note as an error, weighted a bit
      # worse than a badly sung note (which would 'cost' 0.5).
      return 0.51 * len(non_zero_values), "Rest"
    else:
      # Interpret as note, estimating as mean of non-rest predictions.
      h = round(
          statistics.mean([
              12 * math.log2(freq / C0) - ideal_offset for freq in non_zero_values
          ]))
      octave = h // 12
      n = h % 12
      note = note_names[n] + str(octave)
      # Quantization error is the total difference from the quantized note.
      error = sum([
          abs(12 * math.log2(freq / C0) - ideal_offset - h)
          for freq in non_zero_values
      ])
      return error, note


  def get_quantization_and_error(pitch_outputs_and_rests, predictions_per_eighth,
                                prediction_start_offset, ideal_offset):
    # Apply the start offset - we can just add the offset as rests.
    pitch_outputs_and_rests = [0] * prediction_start_offset + \
                              pitch_outputs_and_rests
    # Collect the predictions for each note (or rest).
    groups = [
        pitch_outputs_and_rests[i:i + predictions_per_eighth]
        for i in range(0, len(pitch_outputs_and_rests), predictions_per_eighth)
    ]

    quantization_error = 0

    notes_and_rests = []
    for group in groups:
      error, note_or_rest = quantize_predictions(group, ideal_offset)
      quantization_error += error
      notes_and_rests.append(note_or_rest)

    return quantization_error, notes_and_rests


  best_error = float("inf")
  best_notes_and_rests = None
  best_predictions_per_note = None

  for predictions_per_note in range(20, 65, 1):
    for prediction_start_offset in range(predictions_per_note):

      error, notes_and_rests = get_quantization_and_error(
          pitch_outputs_and_rests, predictions_per_note,
          prediction_start_offset, ideal_offset)

      if error < best_error:      
        best_error = error
        best_notes_and_rests = notes_and_rests
        best_predictions_per_note = predictions_per_note

  # At this point, best_notes_and_rests contains the best quantization.
  # Since we don't need to have rests at the beginning, let's remove these:
  while best_notes_and_rests[0] == 'Rest':
    best_notes_and_rests = best_notes_and_rests[1:]
  # Also remove silence at the end.
  while best_notes_and_rests[-1] == 'Rest':
    best_notes_and_rests = best_notes_and_rests[:-1]


  # Creating the sheet music score.
  sc = music21.stream.Score()
  # Adjust the speed to match the actual singing.
  # bpm = 60 * 60 / best_predictions_per_note
  bpm = 120
  print ('bpm: ', bpm)
  a = music21.tempo.MetronomeMark(number=bpm)
  sc.insert(0,a)

  for snote in best_notes_and_rests:   
      d = 'eighth' 
      d_rest = 'half' 
      if snote == 'Rest':      
        sc.append(music21.note.Rest(type=d_rest))
      else:
        sc.append(music21.note.Note(snote, type=d))

  #@title [Run this] Helper function to use Open Sheet Music Display (JS code) to show a music score

  from IPython.core.display import display, HTML, Javascript
  import json, random

  def showScore(score):
      xml = open(score.write('musicxml')).read()
      showMusicXML(xml)
      
  def showMusicXML(xml):
      DIV_ID = "OSMD_div"
      display(HTML('<div id="'+DIV_ID+'">loading OpenSheetMusicDisplay</div>'))
      script = """
      var div_id = {{DIV_ID}};
      function loadOSMD() { 
          return new Promise(function(resolve, reject){
              if (window.opensheetmusicdisplay) {
                  return resolve(window.opensheetmusicdisplay)
              }
              // OSMD script has a 'define' call which conflicts with requirejs
              var _define = window.define // save the define object 
              window.define = undefined // now the loaded script will ignore requirejs
              var s = document.createElement( 'script' );
              s.setAttribute( 'src', "https://cdn.jsdelivr.net/npm/opensheetmusicdisplay@0.7.6/build/opensheetmusicdisplay.min.js" );
              //s.setAttribute( 'src', "/custom/opensheetmusicdisplay.js" );
              s.onload=function(){
                  window.define = _define
                  resolve(opensheetmusicdisplay);
              };
              document.body.appendChild( s ); // browser will try to load the new script tag
          }) 
      }
      loadOSMD().then((OSMD)=>{
          window.openSheetMusicDisplay = new OSMD.OpenSheetMusicDisplay(div_id, {
            drawingParameters: "compacttight"
          });
          openSheetMusicDisplay
              .load({{data}})
              .then(
                function() {
                  openSheetMusicDisplay.render();
                }
              );
      })
      """.replace('{{DIV_ID}}',DIV_ID).replace('{{data}}',json.dumps(xml))
      display(Javascript(script))
      return

  # rendering the music score
  showScore(sc)
  print(best_notes_and_rests)
  return best_notes_and_rests
