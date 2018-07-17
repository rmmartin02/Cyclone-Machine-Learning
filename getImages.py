import threading
import urllib.request
import requests
import os
from bs4 import BeautifulSoup

def downloadImage(url, file_name):
    print('Downloading: {}'.format(file_name))
    urllib.request.urlretrieve(url, file_name)
    print('Finished Downloading: {}'.format(file_name))

def getImages(stormURL,storm,product):
    productURL = '{}{}'.format(stormURL,product)
    print(productURL)
    page = requests.get(productURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    allAs = soup.find_all('a', href=True)

    images = []
    for a in allAs:
        if '.GIF' in str(a):
            images.append(str(a).split('"')[1].split('/')[7])

    for image in images:
        threading.Thread(target=checkImages,args=(image, storm,product,productURL)).start()

def checkImages(image,storm,product,productURL):
    directory = './images/{}/{}/'.format(storm,product)
    file_name = directory + image
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.isfile(file_name):
        url = '{}/{}'.format(productURL,image)
        threading.Thread(target=downloadImage,args=(url, file_name)).start()
    else:
        print('Already have: {}'.format(image))


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
            if int(stormName[-2:])<=90:
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
        threading.Thread(target=getImages,args=(stormURL, storm, product)).start()

#print(stormDIRs)