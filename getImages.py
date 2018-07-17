import threading
import urllib.request
import requests
import os
from bs4 import BeautifulSoup

def downloadImage(url,file_name):
    print('Downloading: {}'.format(file_name))
    urllib.request.urlretrieve(url, file_name)
    print('Finished Downloading: {}'.format(file_name))

baseURL = 'http://rammb.cira.colostate.edu/'
stormsURL = baseURL + 'products/tc_realtime/products/storms/'

page = requests.get(stormsURL)
soup = BeautifulSoup(page.text, 'html.parser')
allAs = soup.find_all('a', href=True)

stormDIRs = []
for a in allAs:
    if 'storms' in str(a):
        stormDIRs.append(str(a).split('"')[1].split('/')[5])

for storm in stormDIRs:
    stormURL = '{}{}/'.format(stormsURL,storm)
    #get 4KMIRIMG
    products = ['4KMIRIMG']
    for product in products:
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
            directory = './images/{}/{}/'.format(storm,product)
            if not os.path.exists(directory):
                os.makedirs(directory)
            file_name = directory + image
            if not os.path.isfile(file_name):
                url = '{}/{}'.format(productURL,image)
                threading.Thread(target=downloadImage,args=(url, file_name)).start()
            else:
                print('Already have: {}'.format(image))

#print(stormDIRs)