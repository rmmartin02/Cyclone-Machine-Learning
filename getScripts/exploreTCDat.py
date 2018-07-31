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

def checkUrl(url):
    for a in allowed:
        if a in url:
            return True
    return False

class TCDATSpider(Spider):
    name = 'Explore TCDAT'

    start_urls = allowed

    def parse(self, response):
        urls = response.css("a::attr('href')").extract()
        for url in urls:
            if url not in banned:
                url = response.urljoin(url)
                if checkUrl(url):
                    if '.jpg' in url or '.png' in url:
                        yield scrapy.Request(url,method='HEAD',callback=self.getSize)  
                    elif url not in visited and url[-1]=='/':
                        visited.append(url)
                        #print("url\t",url)
                        yield scrapy.Request(url, callback=self.parse)
        with open('./getScripts/TCDAT.csv','a') as file:
            file.writelines(towrite)
        del towrite[:]

    def getSize(self,response):
        size = int(response.headers[b'Content-Length'])
        print('image\t' + response.url + '\tsize\t' + str(size))
        r = response.url.split('/')
        path = r[4:-1]
        image = r[-1]
        if len(path)<6:
            while len(path)<6:
                path.append('')
        image = image.split('.')
        form = image[-1]
        image = image[:-1]
        if len(image)<9:
            while len(image)<9:
                image.append('')
            image.append(form)
        parsed = '{},{},{}\n'.format(','.join(path+image),size,response.url)
        towrite.append(parsed)