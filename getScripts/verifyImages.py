import os
import urllib.request
from PIL import Image

for storm in os.listdir('./images/'):
	directory = './data/{}/STRMSTAT/'.format(storm)
	if os.path.exists(directory):
		stats = os.listdir(directory)
		directory = './images/{}/4KMIRIMG/'.format(storm)
		if os.path.exists(directory):
			for image in os.listdir(directory):
				try:
					im = Image.open(directory+'/'+image)
					im = im.resize((32,32),Image.NEAREST)
					print('OK: {}'.format(image))
				except OSError:
					print('Error: {}'.format(image))
					url = 'http://rammb.cira.colostate.edu/products/tc_realtime/products/storms/{}/4KMIRIMG/{}'.format(storm,image)
					urllib.request.urlretrieve(url, directory+'/'+image)
