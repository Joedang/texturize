#!/usr/bin/python3
# Joe Shields
# 2020-01-06

import numpy as np
from PIL import ImageFont, Image, ImageDraw
import random
import importlib
from texturize import *
# if 'texturize' in dir():
#     importlib.reload(texturize)
# else:
#     from texturize import *

exampleBlock= Block()

spacing= 3
fontSize= 100
charList_fav= ''
charList_punct= '()[]{}\/|<>:;"\'-_=+`1234567890~!@#$%^&*()'
charList_basic= ' .xX#'
charList_draw='\
Box drawing alignment tests:                                          █\
                                                                      ▉\
  ╔══╦══╗  ┌──┬──┐  ╭──┬──╮  ╭──┬──╮  ┏━━┳━━┓  ┎┒┏┑   ╷  ╻ ┏┯┓ ┌┰┐    ▊ ╱╲╱╲╳╳╳\
  ║┌─╨─┐║  │╔═╧═╗│  │╒═╪═╕│  │╓─╁─╖│  ┃┌─╂─┐┃  ┗╃╄┙  ╶┼╴╺╋╸┠┼┨ ┝╋┥    ▋ ╲╱╲╱╳╳╳\
  ║│╲ ╱│║  │║   ║│  ││ │ ││  │║ ┃ ║│  ┃│ ╿ │┃  ┍╅╆┓   ╵  ╹ ┗┷┛ └┸┘    ▌ ╱╲╱╲╳╳╳\
  ╠╡ ╳ ╞╣  ├╢   ╟┤  ├┼─┼─┼┤  ├╫─╂─╫┤  ┣┿╾┼╼┿┫  ┕┛┖┚     ┌┄┄┐ ╎ ┏┅┅┓ ┋ ▍ ╲╱╲╱╳╳╳\
  ║│╱ ╲│║  │║   ║│  ││ │ ││  │║ ┃ ║│  ┃│ ╽ │┃  ░░▒▒▓▓██ ┊  ┆ ╎ ╏  ┇ ┋ ▎\
  ║└─╥─┘║  │╚═╤═╝│  │╘═╪═╛│  │╙─╀─╜│  ┃└─╂─┘┃  ░░▒▒▓▓██ ┊  ┆ ╎ ╏  ┇ ┋ ▏\
  ╚══╩══╝  └──┴──┘  ╰──┴──╯  ╰──┴──╯  ┗━━┻━━┛  ▗▄▖▛▀▜   └╌╌┘ ╎ ┗╍╍┛ ┋  ▁▂▃▄▅▆▇█\
                                               ▝▀▘▙▄▟\
'
charList_weird= ' ℝ⊥╭Λ̊ ░▒▓█ ┊┆×Þæ÷ø╱╲╳█ ▉ ▊ ▋ ▌ ▍ ▎▏┋╎└┗┼╋╃╄┙┼╸┠'
charList_input= charList_fav+charList_punct+charList_basic+charList_draw+charList_weird
# charList_input= ' `1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
fontPath= '/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf'
font= ImageFont.truetype(fontPath, fontSize)
# open the image with 32 bit integer pixels
myimg= Image.open('doge_small.jpg').convert('I')

charList= filterChars(charList_input, fontPath)
if len(charList) != len(charList_input):
    print('There were some characters in that list that aren\'t supported by that font. They have been removed.')
    print('old list: ', charList_input)
    print('new list: ', charList)

charBlocks= []
for char in charList:
    charBlocks.append(Block.fromChar(char, font))
    
goodMatches= 0
badMatches= 0
for i in range(100):
    targInd= random.choice(range(len(charList)))
    targChar= charList[targInd]
    targCharBlock= Block.fromChar(targChar, font)
    scoreMax= -1
    winner=None
    for i in range(len(charList)):
        score= charBlocks[i].dot(targCharBlock)
        if score > scoreMax:
            scoreMax= score
            winner= i
    print('target was (%d):  ' % targInd, targChar)
    print('winner is  (%d):  ' % winner, charList[winner])
    if targInd == winner:
        print('good match')
        goodMatches+=1
    else:
        print('BAD MATCH OMG WTF BBQ!!!!!!!!1')
        badMatches+=1
    print()
print('good matches: ', goodMatches)
print('bad matches: ', badMatches)
