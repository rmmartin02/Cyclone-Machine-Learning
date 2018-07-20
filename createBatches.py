from PIL import Image
import numpy as np
import os
import pickle
from random import randrange

size = 64

labels = [[],[]]
imageArray = [[],[]]
filenames = [[],[]]
#num = 0
for storm in os.listdir('./images/'):
    directory = './data/{}/STRMSTAT/'.format(storm)
    if os.path.exists(directory):
        stats = os.listdir(directory)
        directory = './images/{}/4KMIRIMG/'.format(storm)
        if os.path.exists(directory):
            for image in os.listdir(directory):
                for stat in stats:
                    imageDate = int(image[-16:-5])
                    statDate = int(stat[-16:-5])
                    if statDate<imageDate+15 and statDate>imageDate-15:
                        try:
                            print('processing image: {}'.format(image))
                            im = Image.open(directory+'/'+image)
                            im = im.resize((size,size))
                            im = (np.array(im))

                            index = randrange(len(imageArray))

                            imageArray[index].append(im.flatten())
                            with open('./data/{}/STRMSTAT/{}'.format(storm,stat)) as f:
                                windSpeed = int(f.readline().split()[4])
                            if windSpeed<64:
                                labels[index].append(0)
                            else:
                                labels[index].append(1)
                            filenames[index].append(image)

                        except OSError:
                            pass
i=0
d = {'filenames':filenames[i],'batch_label':'training batch {} of {}'.format(i+1,len(imageArray)),'data':np.array(imageArray[i]),'labels':labels[i]}
pickle.dump( d, open( "./hurr-batches/data_batch", "wb" ) )
i=1
d = {'filenames':filenames[i],'batch_label':'testing batch {} of {}'.format(1,1),'data':np.array(imageArray[i]),'labels':labels[i]}
pickle.dump( d, open( "./hurr-batches/test_batch", "wb" ) )

print(sizes)
d = {'label_names':['storm','hurricane'],'num_cases_per_batch':sizes,'num_vis':size*size}
pickle.dump( d, open( "./hurr-batches/batches.meta", "wb" ) )