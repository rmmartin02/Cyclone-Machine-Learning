import imageio
from PIL import Image
from bs4 import BeautifulSoup
import urllib.request
import requests
import os
import multiprocessing

def downloadImage(url):
    file_name = './gifs/temp/{}'.format(url.split('/')[-1])
    if os.path.exists(file_name):
        try:
            Image.open(file_name).load()
            print('Image {} already exists. Skipping download.'.format(file_name))
            return
        except:
            print('Image {} is corrupted. Redownloading'.format(file_name))
    print('Downloading: {}'.format(file_name))
    while True:
        try:
            urllib.request.urlretrieve(url, file_name)
            Image.open(file_name).load()
            print('Finished Downloading: {}'.format(file_name))
            return
        except:
            time.sleep(.1)
            print('Retrying download: {}'.format(file_name))

def main():
    imagesURL = 'https://www.nrlmry.navy.mil/tcdat/tc2017/AL/AL152017/png/Visible/'
    filenames = []
    URLs = []

    page = requests.get(imagesURL)
    soup = BeautifulSoup(page.text, 'html.parser')
    allAs = soup.find_all('a', href=True)
    dates = [] 
    count = 1
    for idx,a in enumerate(allAs):
        print('{}/{} ({}%)'.format(idx+1,len( allAs ),((idx+1)/len( allAs))*100))
        if a.text:
            imagehref = a['href']
            
            if  '.png' in imagehref and '_abi_' in imagehref and 'LATEST' not in imagehref:
                date = int(imagehref[:12])
                if date not in dates:
                #if urllib.request.urlopen(imagesURL+imagehref).length>100000:
                #date = int(''.join(imagehref.split('.')[:2]))
                #if date>201708241200:
                    URLs.append(imagesURL+imagehref)
                    #urllib.request.urlretrieve(imagesURL+imagehref, './gifs/temp/{}'.format(imagehref))
                    dates.append(date)
                #Image.open('./gifs/temp/{}'.format(imagehref)).save('./gifs/temp/{}'.format(imagehref).replace('jpg','png'))
                #os.remove('./gifs/temp/{}'.format(imagehref))
                #print('Content length: {}'.format(urllib.request.urlopen(imagesURL+imagehref).length))

    print(multiprocessing.cpu_count() * 2)
    pool = multiprocessing.Pool(multiprocessing.cpu_count() * 2)  # Num of CPUs
    pool.map(downloadImage, URLs)
    pool.close()
    pool.terminate()

    print('Finished all downloads')

    filedates = []
    for file in os.listdir('./gifs/temp/'):
        filedates.append( (int(file[:12]), './gifs/temp/'+file) )
    datesorted = sorted(filedates, key=lambda date: date[0])
    for idx,date in enumerate(datesorted):
        os.rename(date[1],'./gifs/temp/img{0:04d}.png'.format(idx))

#images = []
#for filename in filenames:
#    images.append(imageio.imread(filename))
#imageio.mimsave('./gifs/harveyRadar.gif', images, duration=0.1)

if __name__ == '__main__':
    main()

#ffmpeg -r 10 -i ./gifs/temp/img%04d.png -vcodec mpeg4 -y ./gifs/mariaVis.mp4
#ffmpeg -r 10 -i ./gifs/mariaIR/img%04d.png  -c:v huffyuv ./gifs/mariaIR.avi
#ffmpeg -i ./gifs/mariaIR.avi -c:v libx264 -crf 19 -preset slow -c:a libfdk_aac -b:a 192k -ac 2 ./gifs/out.mp4