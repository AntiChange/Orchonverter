import requests
from flask import Flask, jsonify, request

import glob
from data_prep import main
from display import exportSheet

app = Flask(__name__)

@app.route("/", methods=["GET"])
def audio_to_note():
   
  response = requests.get(url="http://127.0.0.1:8000/", params=request.args)
  wavList = glob.glob("../melody_separator/src/output/*")
  all_pitches = []
  for wav_file in wavList:
    file_name = wav_file
    all_pitches.append(main(file_name))
    print("audio_to_note is done")
    
  exportSheet(all_pitches)
  return all_pitches

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)



