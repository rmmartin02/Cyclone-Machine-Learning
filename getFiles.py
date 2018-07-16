import urllib.request
import requests
import os
from bs4 import BeautifulSoup

#reconArchive = 'https://www.nhc.noaa.gov/archive/recon/{}/{}/{}.{}.txt'.format(year,dataType,dataType,date)

#year satellite archive starts
year = 2006
while True:
	#observation names change, also adds western pacific
	dataType2011 = ['HDOB','REPNT2','REPNT3','URNT40']
	dataType2012 = ['AHONT1','REPNT2','REPNT3','AHOPN1','REPPN2','REPPN3','AHOPA1','REPPA2','REPPA3']
	reconArchive = 'https://www.nhc.noaa.gov/archive/recon/{}/{}/'.format(year,dataType)
	print(reconArchive)

	page = requests.get(reconArchive)
	soup = BeautifulSoup(page.text,'html.parser')

	allAs = soup.find_all('a',href=True)
	txtFiles = []
	for a in allAs:
		if '.txt' in str(a):
			txtFiles.append(str(a).split('"')[1])

	if len(txtFiles)==0:
		break

	for t in txtFiles:
		if not os.path.exists('./{}/{}/'.format(year,dataType)):
			os.makedirs('./{}/{}/'.format(year,dataType))
		file_name = './{}/{}/{}'.format(year,dataType,t)
		if not os.path.isfile(file_name):
			url = reconArchive + t
			print('Downloading: {}'.format(t))
			urllib.request.urlretrieve(url, file_name)
		else:
			print('Already have: {}'.format(t))
	year += 1