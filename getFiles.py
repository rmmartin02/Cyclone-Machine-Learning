import urllib.request
import requests
import os
from bs4 import BeautifulSoup
import datetime

def saveTextFiles(year,reconArchive,dataType,plane=None,):
    print(reconArchive)
    page = requests.get(reconArchive)
    soup = BeautifulSoup(page.text, 'html.parser')

    allAs = soup.find_all('a', href=True)
    txtFiles = []
    for a in allAs:
        if '.txt' in str(a):
            txtFiles.append(str(a).split('"')[1])

    for t in txtFiles:
        directory = './{}/{}/'.format(year, dataType)
        if year>2006 and year < 2012:
            directory = './{}/{}/{}/'.format(year, plane, dataType)
        if year>2011:
            directory = './{}/{}/'.format(year, dataType)
        if not os.path.exists(directory):
            os.makedirs(directory)
        file_name = directory + t
        if not os.path.isfile(file_name):
            url = reconArchive + t
            print('Downloading: {}'.format(t))
            urllib.request.urlretrieve(url, file_name)
        else:
            print('Already have: {}'.format(t))

# reconArchive = 'https://www.nhc.noaa.gov/archive/recon/{}/{}/{}.{}.txt'.format(year,dataType,dataType,date)

# year satellite archive starts
year = 2006
while year<=datetime.date.today().year:
    # this only works for 2006-2011
    # observation names change, also adds western pacific
    dataTypes2006 = ['HDOB']
    # for HDOB 2007-2011
    orgs = ['NOAA', 'USAF']
    planes = ['URNT15', 'URPN15']

    # 2012
    dataTypes2012 = ['AHONT1', 'AHOPA1', 'AHOPN1']
    # 2016-2017 has no AHOPA1
    reconArchive = 'https://www.nhc.noaa.gov/archive/recon/'+str(year)+'/'
    if year<=2011:
        for dataType in dataTypes2006:
            reconArchive = reconArchive + dataType + '/'
            if year!=2006:
                for org in orgs:
                    reconArchive = reconArchive + org + '/'
                    if year!=2007:
                        for plane in planes:
                            reconArchive = reconArchive + plane + '/'
                            saveTextFiles(year, reconArchive, dataType, plane=plane)
                            reconArchive = 'https://www.nhc.noaa.gov/archive/recon/' + str(year) + '/'
                            reconArchive = reconArchive + dataType + '/'
                            reconArchive = reconArchive + org + '/'
                    else:
                        saveTextFiles(year, reconArchive, dataType)
                        reconArchive = 'https://www.nhc.noaa.gov/archive/recon/' + str(year) + '/'
                        reconArchive = reconArchive + dataType + '/'
            else:
                saveTextFiles(year, reconArchive, dataType)
    else:
        for dataType in dataTypes2012:
            '{}{}/'.format(reconArchive,dataType)
            saveTextFiles(year, reconArchive, dataType)

    year += 1

