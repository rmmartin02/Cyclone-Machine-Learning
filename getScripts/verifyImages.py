import os
import urllib.request
from PIL import Image
import multiprocessing

def verify(storm):
    directory = './images/{}/4KMIRIMG/'.format(storm)
    if os.path.exists(directory):
        for image in os.listdir(directory):
            with Image.open(directory+'/'+image) as im:
                print(im.height)
                #if im.height != 480 and im.width != 640:
                    #print(image,im.height,im.width)
                    #os.remove(directory+'/'+image)
                '''
                try:
                    with Image.open(directory+'/'+image) as im:
                        im = im.resize((32,32),Image.NEAREST)
                    #print('OK: {}'.format(image))
                except OSError as err:
                    print('Error: {}\n{}'.format(image,err))
                    
                    url = 'http://rammb.cira.colostate.edu/products/tc_realtime/products/storms/{}/4KMIRIMG/{}'.format(storm,image)
                    urllib.request.urlretrieve(url, directory+'/'+image)
                '''

def main():

    pool = multiprocessing.Pool(processes=4)  # Num of CPUs
    pool.map(verify, os.listdir('./images/'))
    pool.close()
    pool.terminate()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()