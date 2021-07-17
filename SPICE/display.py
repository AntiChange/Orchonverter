from mingus.extra.lilypond import *
from mingus.containers import Bar


#2D LIST
exampleList = [["C4", "D4","D4","E4","E4","E4","F4","F4","F4","F4","G4","G4","G4","G4", "G4","A4","A4","A4","A4","A4","A4","G4","G4","G4","G4","G4","G4", "G4","A4","A4","A4","A4","A4","A4","A4","A4","C4","A#4","B4","C4", "C#4","D4","D#4","E4","E#4","F4","F#4","G4","G#4","A4","A#4","B4"], ["B4", "A#4","A4","G#4","G4","F#4","F4","E4","D#4","D4","C#4","C4","B4", "A#4","A4","G#4","G4","F#4","F4","E4","D#4","D4","C#4","C4","B4", "A#4","A4","G#4","G4","F#4","F4","E4","D#4","D4","C#4","C4","B4", "A#4","A4","G#4","G4","F#4","F4","E4","D#4","D4","C#4","C4"]]


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
    newOuterList = []
    for i in inputList:
        newInnerList = []
        for j in i:
            newInnerList.append(lilypondConversion(j))
        
        newOuterList.append(newInnerList)
    
    print(newOuterList)

    lilyStringfull = "\\time 4/4 \\key c \\major {\n<<\n"

    for i in newOuterList:
        currentLilyString = "\\new Staff { "

        currentCount = 1
        for j in range(len(i)):
            try:
                if currentCount == 8:
                    currentLilyString += i[j] + "1 "
                    currentCount = 1

                elif i[j] == i[j + 1]:
                    currentCount += 1
                    continue
                
                else:
                    newFloat = 8 / currentCount
                    if newFloat.is_integer():
                        currentLilyString += i[j] + str(int(newFloat)) + " "
                    else:
                        if currentCount == 3:
                            currentLilyString +=  i[j] + "4. "
                        elif currentCount == 5:
                            currentLilyString +=  i[j] + "2~ " + i[j] + "8 "
                        elif currentCount == 6:
                            currentLilyString +=  i[j] + "2~ " + i[j] + "4 "
                        elif currentCount == 7:
                            currentLilyString += i[j] + "2~ " + i[j] + "4. " 
                    
                    currentCount = 1
           
            except IndexError:
                newFloat = 8 / currentCount
                if newFloat.is_integer():
                    currentLilyString += i[j] + str(int(newFloat)) + " "
                else:
                    if currentCount == 3:
                        currentLilyString += i[j] + "4. "
                    elif currentCount == 5:
                        currentLilyString += i[j] + "2 " + i[j] + "8 "
                    elif currentCount == 7:
                        currentLilyString += i[j] + "2 " + i[j] + "4. "
                 

        currentLilyString += "}\n"

        lilyStringfull +=  currentLilyString
        # to_pdf(currentLilyString, "output" + str(counter) + ".pdf")
        # counter += 1
    lilyStringfull += ">>\n}"
    # to_pdf(lilyString, "output.pdf")

    print(lilyStringfull)
    to_pdf(lilyStringfull, 'output.pdf')

exportSheet(exampleList)