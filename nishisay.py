#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#####################
#importing liblaries#
#####################

from sys import *
from os import *
from threading import Timer
from textwrap import wrap

############################
#declaring static variables#
############################

baseAsciiart = [
                      "     /|_   ___/|",
                      "    / __\\_/    |",
                      "   | /     \\   >",
                      "  / | Ó  °_ | /",
                "        | \\ ░ W ░/  |",
                "         \\_ |   _| /",
                "           < \\// -\\\  ___",
                "         /  /  _ --|\\/   \\",
                "         | /  / --/ |    /",
                "         \\   / \\     >  /",
                "   __     \\/__/_  / \\_  \\",
                "  O   \\  / /O O \\     \\  \\",
                "   O   \\/  °(_)°|      \\  |",
                "    \\   \\   \\   |      |  |",
                "     \\   \\   |   \\     | /",
                "      \\      |    |   /",
                "       \\_____\\___/___/",
]
mods = {
    "imgNoColor" : [
                          "     /|_   ___/|",
                          "    / __\\_/    |",
                          "   | /     \\   >",
                          "  / | Ó  °_ | /",
                    "        | \\ ░ W ░/  |",
                    "         \\_ |   _| /",
                    "           < \\// -\\\  ___",
                    "         /  /  _ --|\\/   \\",
                    "         | /  / --/ |    /",
                    "         \\   / \\     >  /",
                    "   __     \\/__/_  / \\_  \\",
                    "  O   \\  / /O O \\     \\  \\",
                    "   O   \\/  °(_)°|      \\  |",
                    "    \\   \\   \\   |      |  |",
                    "     \\   \\   |   \\     | /",
                    "      \\      |    |   /",
                    "nocolor\\_____\\___/___/(todo)"
    ],
    "uwu" : [
             "*",
             "*",
             "*",
             "  / | U   U | /",
    ],
    "ono" : [
                   "*",
                   "*",
                   "*",
                   "  / | O   O | /",
             "        | \\ ░ n ░/  |",
    ],
}
maxWidth = 35

#################
#setting options#
#################

#determining options
forcePipe = think = wrapping = force = colorDisabled = False
nextIterWidth = nextIterMod = False
textSupplied = False
textOffset = 1
modsEnabled = []
for i in argv[1:]:

    #setting width
    if nextIterWidth:
        if i == "0":
            print("Error: Width can't be set to 0.")
            continue
        try:
            width = int(i)
        except:
            print("Error: Width value incorrect.")
            continue
        wrapping = True

        nextIterWidth = False
        textOffset += 1
        continue

    if nextIterMod:
        modsEnabled.extend(i.split("+"))
        nextIterMod = False
        textOffset += 1
        continue

    #stopping at the end of options
    if not i.startswith("-") and not nextIterWidth:
        textSupplied = True
        break

    if "p" in i:
        forcePipe = True
    if "t" in i:
        think = True
    if "n" in i:
        wrapping = True
    if "f" in i:
        force = True
    if "c" in i:
        colorDisabled = True

    if "w" in i:
        nextIterWidth = True
    if "m" in i:
        nextIterMod = True

    textOffset += 1

#setting width to max if not specified
try: width
except:
    width = maxWidth

#turning on text wrapping if text supplied as argument
if textSupplied and not "\\n" in " ".join(argv[textOffset:]):
    wrapping = True

#configuring asciiart
asciiart = baseAsciiart
try: modsEnabled
except:
    pass
else:
    for modName in modsEnabled:
        mod = mods.get(modName)
        lineIndex = 0
        for line in mod:
            if line != "*":
                #replacing line with the mod
                asciiart[lineIndex] = line
            lineIndex +=1

###############
#fetching text#
###############

#fetching text from arguments
if textSupplied:
    text = " ".join(argv[textOffset:]).split("\\n")

#if no text supplied in arguments
def usageMsg():
    print("Usage: nishisay [options] <text>")
    print("This program comes with " + chr(0x1B) + "[38;5;196mABSOLUTELY NO" \
        + "WARRANTY" + chr(0x1B) + "[39m, to the extent permitted by "\
        + "\napplicable law.")
    print("Options:")
    print("  -t -> think")
    print("  -m -> specify what modifications to apply to the base asciiart " \
        + "(seperated by \n" \
          "        a plus sign, start with the ones that do the most changes " 
          + "first)")
    print("  -n -> toggle word wrapping")
    print("  -w [number] -> set the width for word wrapping")
    #print("  -f force")
    print("  -c -> disable color (todo)")
    print("  -p -> force reading from pipe")
    print("Usage examples:")
    print("  -> nishisay XD")
    print("  -> figlet XD | nishisay")
    print("  -> nishisay -m uwu uwu")
    print("  -> cat file.txt | nishisay -n")
    print('  -> nishisay "Hi, \\nhow are you?"')
    _exit(0)

if not textSupplied and not forcePipe:
    #prinring usage message after a set time (I am so fucking smart :3)
    usageMsgTimer = Timer(0.1, usageMsg)
    usageMsgTimer.start()
    #awaiting for text on stdin (peek() is blocking) and cancelling timer asap
    stdin.buffer.peek(1)
    usageMsgTimer.cancel()
    text = stdin.read().splitlines()

#-p specified
if forcePipe:
    text = stdin.read().splitlines()

#########################
#parsing text (wrapping)#
#########################

#checking if text supplied
if not force:
    if (len(text) == 1 and (text[0] == "" or text[0] == " ")) or len(text) == 0:
        print("Error: No text Supplied.")
        _exit(1)

#wrapping text
if wrapping:
    textTmp = text
    text = []
    for i in textTmp:
        text.extend(wrap(i, width))

#calculating width
width = max(len(i) for i in text)

####################
#printing (finally)#
####################

#printing top line
stdout.write(" _")
for i in range(0, width):
    stdout.write('_')
stdout.write("_")

#printing one line of text
if len(text) == 1:
    stdout.write("   " + asciiart[0] + "\n")
    stdout.write("< " + text[0] + " >  " + asciiart[1] + "\n")

#printing multiple lines of text
elif len(text) > 1:
    stdout.write("\n")
    for i in range(0, len(text)):
        if i == 0:
            stdout.write("/ " + text[0].ljust(width)  + " \\  ")
        elif len(text) - i == 1:
            stdout.write("\\ " + text[i].ljust(width)  + " /  ")
        else:
            stdout.write("│ " + text[i].ljust(width)  + " │  ")

        #printing asciiart
        if len(text) - i == 2:
            stdout.write(asciiart[0])
        elif len(text) - i == 1:
            stdout.write(asciiart[1])

        stdout.write("\n")

spacing = " " * width

#printing bottom line
stdout.write(" ¯")
for i in range(0, width):
    stdout.write('¯')
stdout.write("¯ ")
if not think:
    stdout.write("\\ " + asciiart[2] + "\n")
    stdout.write(spacing + "     \\" + asciiart[3] + "\n")
else:
    stdout.write("o " + asciiart[2] + "\n")
    stdout.write(spacing + "     o" + asciiart[3] + "\n")

#printing rest of asciiart
for i in range(4,len(asciiart)):
    stdout.write(spacing + asciiart[i] + "\n")