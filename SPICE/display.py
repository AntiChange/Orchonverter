from mingus.extra.lilypond import *
from mingus.containers import Bar


def lilypondConversion(noteString):
    newNote = noteString[0]
    newNote = newNote.lower()

    if noteString[1] == "#":
        sharpAddOn = "is"
        octaveIndex = 2
    
    else:
        sharpAddOn = ""
        octaveIndex = 1
    
    octaveString = ""
    if int(noteString[octaveIndex]) > 3:
        for i in range(int(noteString[octaveIndex]) - 3):
            octaveString += "\'"

    elif int(noteString[octaveIndex]) < 3:
        for i in range(3 -int(noteString[octaveIndex])):
            octaveString += ","

    return newNote + sharpAddOn + octaveString


def exportSheet(inputList):
    newList = []


    for i in inputList:
        newList.append(lilypondConversion(i))

    # print(newList)

    lilyString = "{ \\time 4/4 \\key c \\major "

    for j in newList:
        lilyString += j + "8 "

    lilyString += "}"

    # print(lilyString)

    to_pdf(lilyString, "output.pdf")