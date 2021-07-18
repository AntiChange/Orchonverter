# Orchonverter
**Note: Currently the project is too messy/complicated to install and is undergoing major changes to increase accuracy! Instructions for installation and running will be added when available, thank you for your patience.**

If you're someone without perfect pitch or relative pitch, music is pretty much impossible to transcribe into sheet music. Even for experienced and skilled transcribers, transcriptions are extremely tedious to create and take excessively large amounts of time. Thus, we created Orchonverter to quickly create a sheet music score of any musical work. Currently it is mainly geared towards orchestral or chamber music, but in the future we hope to implement different models for different genres of music.

Winner of the S21 Uwaterloo CSC x DSC Project Program!

## Authors
* [Nancy Shen](https://github.com/nancyluyishen) and [Chris Fang](https://github.com/AntiChange)


## About the Project
The project utilizes two different machine learning models; the first being a pre-trained Deep Convolutional Neural Network model trained with the Bach10 dataset, used as a melody separator responsible for generating separate audio files for each instrument/line. We then chunk each line and feed these lines into a pitch detection algorithm, which constructs each musical phrase note by note. 

Finally, we feed these phrases into a music engraver to create proper sheet music containing each part.

## License
This project is licensed under the terms of the MIT license.

## Link to model: (Reqruied in melody_separator\src\)
https://drive.google.com/file/d/1FeelPlTMdCidVh7PILsbDFA781I6elhx/view?usp=sharing

## Pitch Detection model training on Google Colab
https://colab.research.google.com/drive/1aQFJIys7IdlBCfkN1GjGNg5ktrrzr8WB?usp=sharing


## Project Architecture
Our project can be divided into 3 parts: 
- The first part is the melody separator, where it takes a multi-melody orchestral music into each individual instrument parts. Here we used a [pre-trained Deep Convolutional Neural Network model](https://github.com/MTG/DeepConvSep) trained with the [Bach10 dataset](https://interactiveaudiolab.github.io/).
- The second part is for pitch detection. Here we first convert each audio file into a spectrogram and then convert it into a list of frequencies. Then we trained the [single-note pitch detection model](https://colab.research.google.com/drive/1aQFJIys7IdlBCfkN1GjGNg5ktrrzr8WB?usp=sharing) with the [NSynth dataset](https://magenta.tensorflow.org/datasets/nsynth), by Logistic regression.
  - However, it did not achieve the accuracy as expected, therefore an alternative is to use a pre-trained pitch detection model [SPICE](https://www.tensorflow.org/hub/tutorials/spice) from Tensorflow.  
- The third part is to split the single-melody audio into multiple same-length chunks. So that each small chunk only has one pitch worth of audio, then we are able to get the pitch for every piece. Then we wrote an algorithm to put all chunk’s pitches together, and determine the note duration and rest based on the volume percentages.

## Installation and Running for the beta version
- Install [Lilypond](http://lilypond.org/download.html) for music engraving or transcription
- Currently we implemented some old libraries, therefore we host our application servers in both Python 2 and 3 environments. Running them in separate virtual environments is recommanded.
### Host server in Python 3 environemnt:
1. run the frontend server to upload the input wav file, then output a music sheet PDF file with all instrument parts separately.
```
pip install -r requirements.txt
python3 web.py
```
server will be hosted on: http://127.0.0.1:8080/

2. run the pitch detection and phrase construction server
```
cd SPICE
pip install -r requirements.txt
python3 server.py
```
server will be hosted on: http://127.0.0.1:5002/

### Host server in Python 2 environemnt:
3. run the melody separator server (in python2 environment) to convert multi-melody music into individual melodies
```
cd melody_separator/src
pip install -r requirements.txt
python app.py
```
server will be hosted on: http://127.0.0.1:8000/

### Server Structure
The 3 servers are in an onion strucutre. The order is: 1 > 2 > 3, from the outer most to the inner most.
<br />To run the application, go to http://127.0.0.1:8080/
