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