#!/usr/bin/python3
# Joe Shields
# 2020-01-06

import numpy as np
from PIL import ImageFont, Image, ImageDraw
import warnings
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def __init__():
    pass

class Block:
    def __init__(self):
        """
        Initialize self.array with an empty uint32 numpy array.
        """
        self.array= np.array([], dtype='uint32')

    def normalize(self):
        """
        Normalize the block so that it returns 1 when dotted with itself.

        """
        self.array= np.uint32(self.array)
        block_squared= self.dot(self)
        # Thanks to the "there is no zero vector" thing in dot(), we no longer need to avoid a divide-by-zero error here.
        # if block_squared != 0: 
        self.array= self.array/np.sqrt(block_squared)
        return(self)

    def dot(block1, block2=None):
        if block2 == None:
            block2= self
        result= np.tensordot(block1.array, block2.array)
        # if (result > 1) or (result < -1):
        #     warnings.warn("The dot product of the blocks was %f, \
        #             but it should always be between -1 and 1. \
        #             It's likely one of them wasn't normalized." % result)
        if block1.array.max() == 0 and block2.array.max() == 0:
            result= 1 # force the "zero vector" to not behave like zero
        return(result)

    def fromImage(img):
        """
        takes a PIL.Image.Image
        converts that into a 32 bit unsigned numpy array
        stores it in self.array
        """
        result= Block()
        result.array= np.uint32(np.array(img))
        # result.normalize()
        return(result)

    def fromChar(char, font):
        """
        char is a str where len(char) == 1
        The created block will be in the shape of this character.

        font is a PIL.ImageFont.FreeTypeFont
        The character will use this font.
        """
        charImg= imgFromChar(char, font)
        result= Block.fromImage(charImg)
        result.normalize()
        return(result)

    def getSize(self):
        """
        return the size of the array in px as a tuple (width px, height px)
        """
        height, width= self.array.shape
        return((width, height))

    def toImage(self):
        """
        return a PIL.Image.Image of the array
        """
        # print(args)
        return(Image.fromarray(self.array))

    def show(self):
        self.toImage().show()
        return(None)

def blockinate(img, blockSize):
    """
    img is a PIL.Image.Image
    blockSize is a tuple represening the size of blocks to use (horizontal px, vertical px)
    """
    img_cropped= img.crop()

def imgFromChar(char, font):
    """
    return a PIL.Image.Image rendering the given character in the given font

    char is a string of length 1
    font is a PIL.ImageFont.FreeTypeFont
    """
    # sanity check char
    if (type(char) != str) and (len(char) != 1):
        raise ValueErr('Variable char must be of type str with length 1.')

    # figure out how big of an image to make
    dummyImage= Image.new('L', (0,0), 255)
    id= ImageDraw.ImageDraw(dummyImage)
    charSize= id.textsize('X', font=font)
    charWidth, charHeight= charSize

    # create the image
    charImg= Image.new('L', charSize, 0)
    dwg= ImageDraw.Draw(charImg)
    dwg.text((0,0), char, font=font, fill=255) #, spacing=spacing)
    return(charImg)

def ttFontHasGlyph(ttfont, char):
    """
    ttfont is a fontTools.ttLib.ttFont.TTFont
    char is a str of length 1
    """
    for table in ttfont['cmap'].tables:
        if ord(char) in table.cmap.keys():
            return(True)
    return(False)

def filterChars(charList, fontPath):
    """
    return a list of characters which are supported by the referenced font 
    and are not duplicates of each other

    charlist is a list of characters (length 1 strings)
    fontPath is the path to a TrueType font (string)
    """
    filteredList= ''
    ttfont= TTFont(fontPath)
    for char in charList:
        if ttFontHasGlyph(ttfont, char) and (char not in filteredList):
            filteredList += char
    return(filteredList)
