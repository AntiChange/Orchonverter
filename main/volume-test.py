from pydub import AudioSegment
chunk = AudioSegment.from_file("instruments/violin/chunk36.wav", "wav")
print(chunk.rms)
print(chunk[50:200].rms)
print(chunk[100:200].rms)

#21 - 2 - 5.25
#7 - 752
#37 - 14
#36 - 657

#cutting the start and end
#standard: 300