import os
import tensorflow as tf

labels = []
filenames = []
num = 0
for storm in os.listdir('./images/'):
	directory = './data/{}/STRMSTAT/'.format(storm)
	if os.path.exists(directory):
		stats = os.listdir(directory)
		directory = './images/{}/4KMIRIMG/'.format(storm)
		if os.path.exists(directory):
			for image in os.listdir(directory):
				for stat in stats:
					if image[-16:-5] == stat[-16:-5]:
						with open('./data/{}/STRMSTAT/{}'.format(storm,stat)) as f:
							windSpeed = f.readline().split()[4]
						labels.append(windSpeed)
						filenames.append('./images/{}/4KMIRIMG/{}'.format(storm,image))
						num += 1
						print(num,windSpeed,image)

# Reads an image from a file, decodes it into a dense tensor, and resizes it
# to a fixed shape.
def _parse_function(filename, label):
  image_string = tf.read_file(filename)
  image_decoded = tf.image.decode_gif(image_string)
  image_resized = tf.image.resize_images(image_decoded, [28, 28])
  return image_resized, label

# A vector of filenames.
filenames = tf.constant(["/var/data/image1.jpg", "/var/data/image2.jpg", ...])

# `labels[i]` is the label for the image in `filenames[i].
labels = tf.constant([0, 37, ...])

dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
dataset = dataset.map(_parse_function)