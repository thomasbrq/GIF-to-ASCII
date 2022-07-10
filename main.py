import numpy as np
from PIL import Image, GifImagePlugin
import sys

def image_to_ascii(image, grayscale):
	pixels = image.getdata()
	art = ""

	# Divide 'pixel' by 25 to get the index of the grayscale array.
	# 255 / 25: 10 (11 characters max in the array).
	for pixel in pixels:
		art = art + "".join(grayscale[pixel // 25])

	return art

def resize_image(image, scale):
	aspect_ratio = image.size[1] / image.size[0]

	image = image.resize((scale, int(scale / 2 * aspect_ratio)))
	return image

def transform_image(image, grayscale, scale):
	image = resize_image(image, scale)

	# Convert RGB to gray-scale.
	image = image.convert('L')

	image_data = image_to_ascii(image, grayscale)
	pixel_count = len(image_data)
	image_width = image.size[0]

	# Save each characters and a new line character each 'image_width' characters.
	ascii_image = "\n".join(image_data[i:(i + image_width)] for i in range(0, pixel_count, image_width))

	return (ascii_image)

def main(argc, argv):
	if (argc < 2):
		print("Error arguments. Usage: python3 main.py <filename> <invert (0-1)> <scale> ")
		exit(1)

	# Change the ascii grayscale.
	if argc <= 2:
		grayscale = [" ", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
	elif int(argv[2]) == 0:
		grayscale = [" ", ",", ":", ";", "+", "*", "?", "%", "S", "#", "@"]
	else:
		grayscale = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", " "]

	# Check the path and the file format.
	try:
		image = Image.open(argv[1], "r", ['gif'])
	except FileNotFoundError:
		print("Image not found.")
		exit(-1)
	except:
		print("Only .gif images are accepted.")
		exit(-1)

	if argc <= 3:
		scale = 100
	else:
		scale = int(argv[3]);

	# Open/create a result file.
	with open("result", "a") as f:

		# Clear the file.
		f.truncate(0)

		# Transform each frame of the gif to ascii and append to the result file.
		for frame in range(0, image.n_frames):
			image.seek(frame)
			ascii_image = transform_image(image, grayscale, scale)
			f.write(ascii_image)
			f.write("\n\n")

		f.close()

	image.close()

main(len(sys.argv), sys.argv)
