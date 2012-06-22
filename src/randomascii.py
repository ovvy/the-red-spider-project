'''
ASCII Art maker
A (very simple) class for creating an ASCII string
Picks a random image in a given directory and generates an ASCII art from it.
Takes in .jpg, .jpeg, .bmp and .png image files.
Author: leo
Date: 06/12/2012
'''

#TODO: Clean up the code. Maybe split it into two different files (the class and the I/O functionality).
#      Also, try to change the output size according to the environment.

from PIL import Image
import random
from bisect import bisect
import os
import sys


#Size (in pixels) of the output image. I think that making
#these variables to adapt to some environment will be implementation dependable.
#Will try to make a UNIX/POSIX one afterwards.
#leo

_HEIGHT = 160
_WIDTH = 75

# The following strings represent
# 16 tonal ranges, from lighter to darker, so that they
# are the greyscale.
# An alternative greyscale can be picked at http://local.wasp.uwa.edu.au/~pbourke/dataformats/asciiart/

greyscale = [
            " ",
            ".",
            ",",
            ":",
            ";",
            "+",
            "=",
            "o",
            "a",
            "e",
            "0",
            "$",
            "@",
            "A",
            "#",
            "M"
            ]

# There are 16 luminosity bands, of equal sizes. They can be changed accordingly;
# for instance, to boost contrast.

zonebounds=[16, 32, 48, 64, 80, 96, 128, 144, 160, 176, 192, 208, 224, 240, 255]

class AsciiGenerator(object):
  #This assumes that correct path checking was done previously.
  #May want to change the panic mode and not exiting like this.
  def __init__(self, image_path):
    try:
      self.image = Image.open(image_path)
    except IOError:
      print 'Could not open image. Are you sure you entered the correct path?\n'
      print 'Target path: %(target_path)s' % {'target_path':image_path}
      sys.exit(-1)
    self.image = self.image.resize((_HEIGHT, _WIDTH),Image.BILINEAR)
    self.image = self.image.convert("L") # convert to mono

  def __str__(self):
    ascii_string = ''
    for height in xrange(0, self.image.size[1]):
      for width in xrange(0, self.image.size[0]):
        lum = 255 - self.image.getpixel((width, height))
        row = bisect(zonebounds, lum)
        try:
         possibles = greyscale[row]
        except IndexError:
         continue
      ascii_string = ascii_string + possibles[random.randint(0, len(possibles) - 1)]
      ascii_string = ascii_string + '\n'
    return ascii_string

def isImage(extension):
  # Found a cleaner way to code it
  patterns = ['.bmp', '.jpg', '.jpeg', '.png']
  matches = set(patterns)
  if extension in matches:
    return True
  return False

def chooseRandomImage(image_list):
  size = len(image_list)
  return image_list[random.randint(0, size - 1)]

def _usage():
  print 'Usage: python randomascii.py [SOURCE FOLDER]'

def generateImageList(target_directory):
  dir_list = os.listdir(target_directory)
  image_list = []
  for file_target in dir_list:
    file_name, file_extension = os.path.splitext(os.path.join(target_directory, file_target))
    if isImage(file_extension):
      image_list.append( file_name + file_extension )
  if not image_list:
    print 'Found no images in the target directory %(directory)s' % {'directory':target_directory}
    print 'Supported format for images are .png, .bmp, .jpg and .jpeg'
    sys.exit(-1)
  return image_list

def main():
  if len(sys.argv) != 2:
    _usage()
    sys.exit(-1)
  curr_dir = sys.argv[1]
  while not os.path.exists(curr_dir):
    curr_dir = raw_input('Path not found. Please, try again: ')
  image_list = generateImageList(curr_dir)
  image_to_print = chooseRandomImage(image_list)
  print image_to_print
  ascii_string = AsciiGenerator(image_to_print)
  if ascii_string:
    print ascii_string
    
if __name__ == '__main__':
  main()
