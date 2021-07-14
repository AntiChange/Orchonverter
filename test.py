from mingus.extra.lilypond import *
from mingus.containers import Bar


b = Bar()
b + "C"
b + "E"
b + "G"
b + "B"
testString = from_Bar(b)
print(testString)

to_pdf(testString, "test.pdf")