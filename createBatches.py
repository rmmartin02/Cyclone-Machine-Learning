from PIL import Image
import numpy as np
import os
import pickle
from random import randrange
from threading import Thread
from queue import Queue

def do_work(q):
    while True:
        items = q.get()
        func = items[0]
        args = items[1:]
        func(*args)
        q.task_done()


def main():
    q = Queue(maxsize=0)
    num_threads = 8
    for i in range(num_threads):
        worker = Thread(target=do_work,args=(q,))
        worker.setDaemon(True)
        worker.start()   

    size = 64
    cropSize = 200
    cropType = 'center'
    #classes = ['storm','hurricane']

    labels = [[],[]]
    imageArray = [[],[]]
    filenames = [[],[]]
    numClass = [[0,0],[0,0]]
    #num = 0
    for storm in os.listdir('./images/'):
        directory = './data/{}/STRMSTAT/'.format(storm)
        if os.path.exists(directory):
            stats = os.listdir(directory)
            directory = './images/{}/4KMIRIMG/'.format(storm)
            if os.path.exists(directory):
                for image in os.listdir(directory):
                    found = False
                    for stat in stats:
                        imageDate = int(image[-16:-5])
                        statDate = int(stat[-16:-5])
                        if statDate<imageDate+15 and statDate>imageDate-15:
                            found = True
                            try:
                                print('processing image: {}'.format(image))
                                im = Image.open(directory+'/'+image)

                                cropSize = 200
                                im = im.crop((im.width/2-cropSize/2,im.height/2-cropSize/2,im.width/2+cropSize/2,im.height/2+cropSize/2))

                                def maskArray(arr,index,num):
                                    for j in range(len(arr[index])):
                                        if arr[index][j] < np.int64(num):
                                            arr[index][j] = 0

                                im = (np.array(im))
                                for i in range(len(im)):
                                    q.put( (maskArray, im, i, 70) )

                                q.join()

                                im = Image.fromarray(im,'P')
                                im = im.resize((size,size))
                                im = (np.array(im))

                                index = 0
                                if randrange(6)==0:
                                    index = 1

                                imageArray[index].append(im.flatten())
                                with open('./data/{}/STRMSTAT/{}'.format(storm,stat)) as f:
                                    windSpeed = int(f.readline().split()[4])
                                if windSpeed<64:
                                    labels[index].append(0)
                                    numClass[index][0] += 1
                                else:
                                    labels[index].append(1)
                                    numClass[index][1] += 1
                                filenames[index].append(image)

                            except OSError as err:
                                print(err)
                        if found:
                            break
    i=0
    d = {'classNums':numClass[i],'filenames':filenames[i],'batch_label':'training batch {} of {}'.format(i+1,len(imageArray)),'data':np.array(imageArray[i]),'labels':labels[i]}
    pickle.dump( d, open( "./hurr-batches/{}_{}_{}_data_batch".format(size,cropSize,cropType), "wb" ) )
    i=1
    d = {'classNums':numClass[i],'filenames':filenames[i],'batch_label':'testing batch {} of {}'.format(1,1),'data':np.array(imageArray[i]),'labels':labels[i]}
    pickle.dump( d, open( "./hurr-batches/{}_{}_{}_test_batch{}".format(size,cropSize,cropType), "wb" ) )

    sizes = [len(imageArray[0]),imageArray[1]]
    print(sizes)
    d = {'label_names':['storm','hurricane'],'num_cases_per_batch':sizes,'num_vis':size*size}
    pickle.dump( d, open( "./hurr-batches/batches.meta", "wb" ) )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()