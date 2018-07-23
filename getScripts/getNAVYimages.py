from threading import Thread
from queue import Queue
import urllib.request
import requests
import os
import time
import re
from bs4 import BeautifulSoup

baseURL = 'https://www.nrlmry.navy.mil/tcdat/'
seasons = ['tc97','tc98','tc99','tc00','tc01','tc02','tc03','tc04','tc05','tc06','tc07','tc08','tc09','tc10','tc11','tc12','tc13','tc14','tc15','tc16','tc17','tc18']
basins = ['ATL','CPAC','EPAC','IO','SHEM','WPAC']
products = ['vis/geo/1km/']
URLs = []

def downloadImage(url, file_name):
    if not os.path.exists(directory):
        os.makedirs(directory)
    print('Downloading: {}'.format(file_name))
    while True:
        try:
            urllib.request.urlretrieve(url, file_name)
            break
        except:
            time.sleep(1)
    print('Finished Downloading: {}'.format(file_name))
 
def do_work(q):
    while True:
        items = q.get()
        func = items[0]
        args = items[1:]
        func(*args)
        q.task_done()


def getImages(url, q):
    #print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    allAs = soup.find_all('a', href=True)
    for a in allAs:
        if a.text:
            imagehref = a['href']
            if '.jpg' in imagehref and 'LATEST' not in imagehref:
                print('{}{}'.format(url,imagehref))
                URLs.append('{}{}'.format(url,imagehref))

def getStorms(url, q):
    #print(url)
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    allAs = soup.find_all('a', href=True)
    for a in allAs:
        if a.text:
            href = a['href']
            #print(href)
            obj = re.match(r'\d\d\.*',str(href))
            if obj != None:
                for product in products:
                    q.put( (getImages, '{}/{}{}'.format(url,href,product), q) )

def main():
    q = Queue(maxsize=0)
    num_threads = 64
    for i in range(num_threads):
        worker = Thread(target=do_work,args=(q,))
        worker.setDaemon(True)
        worker.start()

    for season in seasons:
        for basin in basins:
            q.put( (getStorms, '{}{}/{}'.format(baseURL,season,basin), q) )

    q.join()
    print(len(URLs))

    for u in URLs:
        filename = './{}'.format('/'.join(u.split('/')[3:]))
        directory = './{}'.format('/'.join(filename.split('/')[:-1]))
        print(directory)
        if not os.path.exists(directory):
            print('Making DIR: {}'.format(directory))
            os.makedirs(directory)

    for u in URLs:
        q.put( (downloadImage, u, './{}'.format('/'.join(u.split('/')[3:]))) )

    q.join()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print()