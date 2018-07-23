import os
import urllib.request
from PIL import Image
from threading import Thread
from queue import Queue

def verify(storm):
    directory = './images/{}/4KMIRIMG/'.format(storm)
    if os.path.exists(directory):
        for image in os.listdir(directory):
            with Image.open(directory+'/'+image) as im:
                if im.height != 480 and im.width != 640:
                    print('wtf')
                '''
                try:
                    with Image.open(directory+'/'+image) as im:
                        im = im.resize((32,32),Image.NEAREST)
                    #print('OK: {}'.format(image))
                except OSError as err:
                    print('Error: {}\n{}'.format(image,err))
                    os.remove(directory+'/'+image)
                    url = 'http://rammb.cira.colostate.edu/products/tc_realtime/products/storms/{}/4KMIRIMG/{}'.format(storm,image)
                    urllib.request.urlretrieve(url, directory+'/'+image)
                '''
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

    for storm in os.listdir('./images/'):
        q.put( (verify,storm))
        
    q.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()