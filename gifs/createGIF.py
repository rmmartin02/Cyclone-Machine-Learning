import imageio
from PIL import Image
from bs4 import BeautifulSoup
import urllib.request
import requests
import os

imagesURL = 'https://www.nrlmry.navy.mil/tcdat/tc17/ATL/09L.HARVEY/radar/'
filenames = []

page = requests.get(imagesURL)
soup = BeautifulSoup(page.text, 'html.parser')
allAs = soup.find_all('a', href=True)
count = 0
for idx,a in enumerate(allAs):
    print('{}/{} ({}%)'.format(idx+1,len( allAs ),((idx+1)/len( allAs))*100))
    if a.text:
        imagehref = a['href']
        if '.jpg' in imagehref and 'LATEST' not in imagehref:
            if urllib.request.urlopen(imagesURL+imagehref).length>100000:
                urllib.request.urlretrieve(imagesURL+imagehref, './gifs/temp/{0:05d}.jpg'.format(count))
                count += 1
            #Image.open('./gifs/temp/{}'.format(imagehref)).save('./gifs/temp/{}'.format(imagehref).replace('jpg','png'))
            #os.remove('./gifs/temp/{}'.format(imagehref))
            #print('Content length: {}'.format(urllib.request.urlopen(imagesURL+imagehref).length))

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('./gifs/harveyRadar.gif', images, duration=0.1)