import urllib.request
import requests
import os
from bs4 import BeautifulSoup

#reconArchive = 'https://www.nhc.noaa.gov/archive/recon/{}/{}/{}.{}.txt'.format(year,dataType,dataType,date)
year = 2006
dataType = 'REPPN0'
reconArchive = 'https://www.nhc.noaa.gov/archive/recon/{}/{}/'.format(year,dataType)
print(reconArchive)

page = requests.get(reconArchive)
soup = BeautifulSoup(page.text,'html.parser')

allAs = soup.find_all('a',href=True)
txtFiles = []
for a in allAs:
	if '.txt' in str(a):
		txtFiles.append(str(a).split('"')[1])

print(txtFiles)

for t in txtFiles:
	if not os.path.exists('./{}/{}/'.format(year,dataType)):
		os.makedirs('./{}/{}/'.format(year,dataType))
	file_name = './{}/{}/{}'.format(year,dataType,t)
	url = reconArchive + '/' + t
	urllib.request.urlretrieve(url, file_name)