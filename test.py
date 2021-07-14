from mingus.extra.lilypond import *
from mingus.containers import Bar

def intToNote(midi_int):
    if midi_int % 12 == 0:
        return ("c", midi_int//12)
    elif midi_int%12 == 1:
        return ("cis", midi_int//12)
    elif midi_int%12 == 2:
        return ("d", midi_int//12)
    elif midi_int%12 == 3:
        return ("dis", midi_int//12)
    elif midi_int%12 == 4:
        return ("e", midi_int//12)
    elif midi_int%12 == 5:
        return ("f", midi_int//12)
    elif midi_int%12 == 6:
        return ("fis", midi_int//12)
    elif midi_int%12 == 7:
        return ("g", midi_int//12)
    elif midi_int%12 == 8:
        return ("gis", midi_int//12)
    elif midi_int%12 == 9:
        return ("a", midi_int//12)
    elif midi_int%12 == 10:
        return ("ais", midi_int//12)
    else:
        return ("b", midi_int//12)


testingDict = {'bassoon': [70, 70, 66, 70, 66, 66, 94, 69, 70, 70, 70, 70, 94, 78, 94, 70, 94, 70, 66, 70, 94, 66, 94, 69, 70, 70, 70, 70, 94, 78, 94, 70, 94, 94, 70, 70, 94, 94, 94, 51, 94, 94, 94, 70, 70, 94, 94, 94, 70, 70, 94, 70, 94, 51, 94, 94, 70], 'clarinet': [94, 94, 94, 94, 70, 70, 70, 47, 94, 94, 94, 94, 70, 70, 70, 94, 94, 94, 94, 94, 70, 70, 70, 47, 94, 94, 94, 94, 70, 70, 70, 94, 94, 70, 70, 94, 94, 59, 70, 70, 70, 70, 70, 94, 94, 94, 94, 49, 94, 94, 94, 59, 70, 70, 94, 94, 70], 'saxphone': [94, 70, 70, 70, 70, 70, 70, 70, 70, 70, 69, 94, 70, 94, 94, 94, 66, 70, 70, 70, 70, 70, 70, 94, 70, 70, 94, 94, 70, 94, 94, 70, 94, 70, 94, 70, 70, 94, 94, 94, 94, 70, 70, 94, 70, 94, 70, 94, 70, 70, 94, 94, 70, 94, 94, 70, 70], 'violin': [70, 70, 70, 70, 69, 70, 70, 
59, 70, 70, 70, 94, 70, 70, 70, 70, 70, 66, 70, 70, 69, 70, 70, 59, 70, 70, 70, 94, 70, 70, 70, 70, 70, 59, 70, 70, 70, 59, 70, 70, 70, 70, 69, 70, 94, 70, 70, 70, 70, 94, 70, 94, 70, 70, 70, 70, -1]}

lilyString = "{ \\time 4/4 \\key c \\major "

testingInstrument = 'bassoon'

for i in range(len(testingDict[testingInstrument])):
    lilyString += intToNote(testingDict[testingInstrument][i])[0]
    if intToNote(testingDict[testingInstrument][i])[1] > 4:
        for i in range(intToNote(testingDict[testingInstrument][i])[1] - 4):
            lilyString += "\'"
    elif intToNote(testingDict[testingInstrument][i])[1] < 4:
        for i in range(4 - intToNote(testingDict[testingInstrument][i])[1]):
            lilyString += ","
    lilyString += "8 "

lilyString += "}"

print(lilyString)

to_pdf(lilyString, "test.pdf")


# testString = "{ \\time 4/4 \\key c \\major c'4 e'5 g'4 b'4 }"
# print(testString)

# to_pdf(testString, "test.pdf")

# # % 12 = pitch
# # // 12 = octave
