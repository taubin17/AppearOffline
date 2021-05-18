from PIL import Image
import os

image_to_convert = 'instagram'

im = Image.open('Images/' + image_to_convert + '.jpg')

im.save('Images/' + image_to_convert + '.png')

os.remove ('Images/' + image_to_convert + '.jpg')