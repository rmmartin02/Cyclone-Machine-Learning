from threading import Thread
from queue import Queue
import urllib.request
import requests
import os
import time
from bs4 import BeautifulSoup

def downloadImage(url, file_name):
    print('Downloading: {}'.format(file_name))
    while True:
        try:
            urllib.request.urlretrieve(url, file_name)
            break
        except:
            time.sleep(1)
    print('Finished Downloading: {}'.format(file_name))

def getImages(stormURL,storm,product):
    productURL = '{}{}'.format(stormURL,product)
    print(productURL)
    page = None
    while True:
        try:
            page = requests.get(productURL)
            break
        except:
            time.sleep(1)
    soup = BeautifulSoup(page.text, 'html.parser')
    allAs = soup.find_all('a', href=True)

    images = []
    for a in allAs:
        if '.GIF' in str(a):
            images.append(str(a).split('"')[1].split('/')[7])

    for image in images:
        directory = './images/{}/{}/'.format(storm,product)
        file_name = directory + image
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.isfile(file_name):
            url = '{}/{}'.format(productURL,image)
            q.put( (downloadImage,url, file_name) )
        else:
            print('Already have: {}'.format(image))
 
def do_work(q):
    while True:
        items = q.get()
        func = items[0]
        args = items[1:]
        func(*args)
        q.task_done()

q = Queue(maxsize=0)
num_threads = 4
for i in range(num_threads):
    worker = Thread(target=do_work,args=(q,))
    worker.setDaemon(True)
    worker.start()   


baseURL = 'http://rammb.cira.colostate.edu/'
stormsURL = baseURL + 'products/tc_realtime/products/storms/'

page = requests.get(stormsURL)
soup = BeautifulSoup(page.text, 'html.parser')
allAs = soup.find_all('a', href=True)

stormDIRs = []
toRemove = []
for a in allAs:
    if 'storms' in str(a):
        stormName = str(a).split('"')[1].split('/')[5]
        try:
            if int(stormName[-2:])<90:
                stormDIRs.append(stormName)
            else:
                toRemove.append(stormName)
        except:
            pass

for storm in stormDIRs:
    stormURL = '{}{}/'.format(stormsURL,storm)
    #get 4KMIRIMG
    products = ['4KMIRIMG']
    for product in products:
        q.put( (getImages,stormURL, storm, product) )

q.join()