import requests
from flask import Flask, jsonify, request

import glob
from data_prep import main

app = Flask(__name__)

# @app.route("/hi_world", methods=["POST"])
# def hi_world():
#      a = request.json.get("a")
#      b = request.json.get("b")
#      paras = {"a":a, "b":b}
#     #  response = requests.post(url="http://0.0.0.0:5000/",data=paras)
#     #  print(response)
#      return None

@app.route("/", methods=["GET"])
def hi_world():
    #  a = request.json.get("a")
    #  b = request.json.get("b")
    #  paras = {"a":a, "b":b}
    # response = requests.get(url="http://127.0.0.1:8000/")
    
    wavList = glob.glob("../melody_separator/src/output/*")
    all_pitches = []
    for wav_file in wavList:
      file_name = wav_file
      print(file_name)
      all_pitches.append(main(file_name))
    return all_pitches

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5002,debug=True)



