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
for idx,a in enumerate(allAs):
    print('{}/{} ({}%)'.format(idx,len( allAs ),(idx/len( allAs))*100))
    if a.text:
        imagehref = a['href']
        if '.jpg' in imagehref and 'LATEST' not in imagehref:
            urllib.request.urlretrieve(imagesURL+imagehref, './gifs/temp/{}'.format(imagehref))
            #Image.open('./gifs/temp/{}'.format(imagehref)).save('./gifs/temp/{}'.format(imagehref).replace('jpg','png'))
            #os.remove('./gifs/temp/{}'.format(imagehref))
            filenames.append('./gifs/temp/{}'.format(imagehref))

images = []
for filename in filenames:
    images.append(imageio.imread(filename))
imageio.mimsave('./gifs/harveyRadar.gif', images, duration=0.1)