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
