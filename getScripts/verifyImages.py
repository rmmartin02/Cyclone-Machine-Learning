import os
import urllib.request
from PIL import Image
from threading import Thread
from queue import Queue

def verify(storm):
	directory = './data/{}/STRMSTAT/'.format(storm)
	if os.path.exists(directory):
		stats = os.listdir(directory)
		directory = './images/{}/4KMIRIMG/'.format(storm)
		if os.path.exists(directory):
			for image in os.listdir(directory):
				try:
					im = Image.open(directory+'/'+image)
					im = im.resize((32,32),Image.NEAREST)
					#print('OK: {}'.format(image))
				except OSError:
					print('Error: {}'.format(image))
					os.remove(directory+'/'+image)
					url = 'http://rammb.cira.colostate.edu/products/tc_realtime/products/storms/{}/4KMIRIMG/{}'.format(storm,image)
					urllib.request.urlretrieve(url, directory+'/'+image)
 
def do_work(q):
    while True:
        items = q.get()
        func = items[0]
        args = items[1:]
        func(*args)
        q.task_done()

q = Queue(maxsize=0)
num_threads = 64
for i in range(num_threads):
    worker = Thread(target=do_work,args=(q,))
    worker.setDaemon(True)
    worker.start()   

for storm in os.listdir('./images/'):
	q.put( (verify,storm))
	
q.join()