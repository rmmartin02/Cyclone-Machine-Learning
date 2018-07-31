import scrapy
from scrapy.spiders import Spider

base_url = 'https://www.nrlmry.navy.mil/tcdat/'
banned = ['?C=N;O=D','?C=M;O=A','?C=S;O=A','?C=D;O=A','tcdat']
allowed = []
basins = ['ATL','CPAC','EPAC','IO','SHEM','WPAC']
#seasons = ['tc97','tc98','tc99','tc00','tc00','tc01','tc02','tc03','tc04','tc05','tc06','tc07','tc08','tc09','tc10','tc11','tc12','tc13','tc14','tc15','tc16','tc17','tc18','tc19']
seasons = ['tc97']
for season in seasons:
    allowed.append(base_url+season+'/')
visited = []
towrite = []

with open('./getScripts/TCDAT.csv','w') as file:
    file.write('')

def checkUrl(url):
    for a in allowed:
        if a in url:
            return True
    return False

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class TCDAT2Spider(Spider):
    name = 'Explore TCDAT2'

    start_urls = allowed

    def parse(self, response):
        urls = response.css("a::attr('href')").extract()
        isImageDir = False
        for url in urls:
            if url not in banned:
                url = response.urljoin(url)
                if checkUrl(url):
                    if '.jpg' in url or '.png' in url:
                        #print('image\t',url)
                        isImageDir = True
                        break
                    elif url not in visited and url[-1]=='/':
                        visited.append(url)
                        #print("url\t",url)
                        yield scrapy.Request(url, callback=self.parse)
        if isImageDir:
            for line in response.text.split('\n'):
                if '.jpg' in line or '.png' in line:
                    a = line.split()
                    if len(a)>4:
                        size = a[-1][:-1]
                        path = response.url.split('/')[4:-1]
                        imageUrl = a[4].split('"')[1]
                        image = imageUrl.split('.')
                        if RepresentsInt(image[0]):
                            if len(path)<6:
                                while len(path)<6:
                                    path.append('')
                            form = image[-1]
                            image = image[:-1]
                            if len(image)<9:
                                while len(image)<9:
                                    image.append('')
                                image.append(form)
                            parsed = '{},{},{}{}\n'.format(','.join(path+image),size,response.url,imageUrl)
                            towrite.append(parsed)
            with open('./getScripts/TCDAT.csv','a') as file:
                file.writelines(towrite)
            del towrite[:]