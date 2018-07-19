from PIL import Image
import numpy as np
import os

labels = []
filenames = []
#num = 0
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
							windSpeed = int(f.readline().split()[4])
						if windSpeed<64:
							labels.append(0)
						else:
							labels.append(1)
						filenames.append('./images/{}/4KMIRIMG/{}'.format(storm,image))
print('Got list of images')

size = 32
out = np.zeros((len(filenames),size*size),np.uint8)
for i in range(len(filenames)):
	im = Image.open(filenames[i])
	im = im.resize((size,size),Image.NEAREST)
	im = (np.array(im))
	out[i] = im.flatten()

d = {'data':out,'labels':labels}
pickle.dump( d, open( "hurr.bin", "wb" ) )