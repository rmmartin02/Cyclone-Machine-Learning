import numpy as np
import data_helpers
import pickle
from PIL import Image

#im = Image.open('D:/Projects/Cyclone-Machine-Learning/images/2015EP20/4KMIRIMG/2015EP20_4KMIRIMG_201510222345.GIF')

def newAverage(a,avg,n):
	avg = (avg+a)/(n+1)


filename = './hurr-batches/CATs_data_batch64'
with open(filename, 'rb') as f:
	datadict = pickle.load(f, encoding='latin1')
filename = './hurr-batches/CATs_test_batch64'
with open(filename, 'rb') as f:
	testdict = pickle.load(f, encoding='latin1')

print(datadict['data'].shape)
nums = datadict['classNums']

maxVals = np.argwhere(datadict['data']==datadict['data'].max())
for i in maxVals:
	print(datadict['filenames'][i[0]])

'''
CATs = np.array([
	np.empty( (nums[0],4096) ),
	np.empty( (nums[1],4096) ),
	np.empty( (nums[2],4096) ),
	np.empty( (nums[3],4096) ),
	np.empty( (nums[4],4096) ),
	np.empty( (nums[5],4096) )])

counts = [0,0,0,0,0,0]
for i, l in enumerate(dict['labels']):
    print('{}/{} ({}%)'.format(i,len( dict['labels'] ),(i/len( dict['labels']))*100))
    CATs[l][counts[l]] = dict['data'][i]
    counts[l] += 1

CATs = np.array(CATs)
print(CATs.shape)

for i in range(len(nums)):
	mean_image = np.mean(CATs[i], axis=0)
	print(mean_image)
	Image.fromarray(np.reshape(mean_image.astype(np.uint8),(64,64)),'P').save('./RefImages/cat{}TestMean.GIF'.format(i))
	'''