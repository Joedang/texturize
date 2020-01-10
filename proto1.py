#!/usr/bin/python3
# Joe Shields
# 2020-01-06

from PIL import ImageFont, Image, ImageDraw
import numpy as np
import texturize
spacing= 3 # This is the leading space between lines. My terminal happens to use this value.
fontSize= 20

# get a base image
base= Image.open('doge_small.jpg').convert('RGBA')
base_L= base.convert('L')
# make a blank, transparent image for the text
txt= Image.new('RGBA', base.size, (255,255,255,0))
# get a font
font= ImageFont.truetype('/truetype/ubuntu-font-family/UbuntuMono-R.ttf', fontSize)
# create a drawing context for the text
dwg= ImageDraw.Draw(txt)

# draw at half opacity
dwg.text((10,10), 'Wow, such example.', font=font, fill=(255,255,255,128))
# draw at full opacity
dwg.text((10,60), 'very tutorial underscore:_', font=font, fill=(255,255,255,255))

out= Image.alpha_composite(base, txt)

out.show()

# create an all-white character-sized image
# charBlock= Image.new('RGBA', (100,190), (255,255,255,255))
charBlock= Image.new('L', (100,190), 255)
# redefine the old drawing context
dwg= ImageDraw.Draw(charBlock)
# dwg.text((0,0), 'xXmM', font=font, fill=(0,0,0,255))
dwg.text((0,0), 'xXmM', font=font, fill=0)
#charBlock.show()

dummyImage= Image.new('L', (0,0), 255)
id= ImageDraw.ImageDraw(base)
charSize= id.textsize('X', font=font, spacing=spacing)
charWidth, charHeight= charSize
# leadSpace= id.textsize('X\nX', font=font, spacing=spacing)[1] - 2*charHeight
# The height of a block of text is n*charHeight + (n-1)*leadSpace.
# The leading spaces go between the lines.
# So, the total line height equals charHeight+leadSpace,
# however the first line doesn't get any leading space above it.
# Note that the height of a single character may also include some white space above it.
# Also note, these outputs are all in px, not pt.
# The calculation for leadSpace is redundant. It's given with the `spacing` argument.

# demoImage= Image.new('L', (charWidth*10, charHeight*10+(10-1)*leadSpace), 255)
# dwg= ImageDraw.Draw(demoImage)
# dwg.text((0,0), ('X'*10+'\n')*10, font=font, fill=0, spacing=spacing)
# demoImage.show()

# charlist= '`1234567890-=qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
charlist= ' .xX#'

charImgs= []
charArrays= []
charNorms= []
for i in range(len(charlist)):
    charImg= Image.new('L', charSize, 0)
    dwg= ImageDraw.Draw(charImg)
    dwg.text((0,0), charlist[i], font=font, fill=255, spacing=spacing)
    charImgs.append(charImg)
    # charArray= np.array(charImg, dtype='uint32')
    charArray= np.uint32(np.array(charImg))
    print('original pre-normalization array: \n', charArray)
    char_squared= np.uint32(np.tensordot(charArray, charArray))
    print('char_squared: ', char_squared, type(char_squared))
    if char_squared != 0: # kernel is not a whitespace character
        charNorm= charArray/np.sqrt(char_squared)
    else:
        charNorm= charArray
    print('post-normalization array: \n', charNorm)
    charArrays.append(charNorm)
    print('dotting that with itself: ', np.tensordot(charNorm,charNorm))
    # print('current charNorms: ', charNorms)
    # print('charNorm to append: ', charNorm)
    # print('charNorm type: ', type(charNorm))
    charNorms.append(charNorm)
    # charImg.save('chars/'+char+'.bmp') # CAUTION! It would be easy to make a pathological file name this way!
    # charImg.show()
    print()

targInd= 3
targetChar= charArrays[targInd]
cumMax= 0
maxInd= -1
for i in range(len(charlist)):
    score= np.sum(np.tensordot(charArrays[i], targetChar))
    # scoreDenominator= charNorms[i]
    print('i: ', i)
    print('char: ', charlist[i])
    # print('scoreNumerator: ', scoreNumerator)
    # print('scoreDenominator: ', scoreDenominator)
    print('score: ', score)
    if score > cumMax:
        cumMax= score
        maxInd= i
print()
print('target character:', charlist[targInd])
print('The winner is: ', charlist[maxInd])

# Okay, that's an interesting problem. 
# The `#` matches stronger with `X` than `X` itself.
# I think this is because `#` just has a lot of high values everywhere.
# Oh... I just have to normalize it, lol.
