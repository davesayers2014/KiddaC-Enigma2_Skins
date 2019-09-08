
from HTMLParser import HTMLParser
import urllib2
import os
import json
import sys  
import time
import random


# random delay to stop everyone scraping at the same time
#time.sleep(random.randint(1,120))

reload(sys)  
sys.setdefaultencoding('utf8')


urls = []
urls.append({'channel': 'Sky One','url': 'https://www.sky.com/watch/channel/sky-one/'})
urls.append({'channel': 'Sky Witness','url': 'https://www.sky.com/watch/channel/sky-witness/'})
urls.append({'channel': 'Sky Atlantic','url': 'https://www.sky.com/watch/channel/sky-atlantic/'})
urls.append({'channel': 'Sky Cinema','url': 'https://www.sky.com/watch/channel/sky-cinema/'})

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}

class MyHTMLParser(HTMLParser):
    
    ltile = []
    ptile = []
    tilevalues = {}
    ltilevalues = {}
    ptilevalues = {}
    readjson = ""
    x = 0
    y = 0
    z = 0


    def handle_starttag(self, tag, attrs):

        if tag == "script":
            for name, value in attrs:
                if name == "id" and value == "initialData":
                    self.readjson = True


    def handle_data(self, data):
        if self.readjson == True:
            data = data.replace("%E2%80%99", "'")
            self.jsondata = urllib2.unquote(data)
            self.jsondata = self.jsondata.replace("<br>", "")
            self.jsondata = self.jsondata.replace("&nbsp;", "")
            self.jsondata = self.jsondata.replace("series:", "")
            self.jsondata = self.jsondata.replace("programme:", "")
            
            initialdata = json.loads(self.jsondata)
            
            filename = '/etc/enigma2/slyk/test %s.json' % url['channel']
            with open(filename, 'w') as f:
                json.dump(initialdata, f)
            
            if url['channel'] == "Sky One" or url['channel'] == "Sky Witness" or url['channel'] == "Sky Atlantic":
                intialdatabase = initialdata['state']['tiles']
                
                for tile in intialdatabase:
                
                    if 'uuid' in intialdatabase[self.x]:
                
                        self.p_uuid = intialdatabase[self.x]['uuid']
                        self.p_title =  intialdatabase[self.x]['title'].encode("utf-8")
                        self.p_channel =  intialdatabase[self.x]['brand']['id']
                        
                        if 'url' in intialdatabase[self.x]['tileImage']:
                            self.p_original = intialdatabase[self.x]['tileImage']['url']
                        
                        elif 'medium' in intialdatabase[self.x]['tileImage']:
                            self.p_original = intialdatabase[self.x]['tileImage']['medium']
                        else:
                            self.p_original = ""

                        self.p_cover = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/cover/500"
                        self.p_background = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/background/1280"
                        self.p_16_9 = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/16-9/500"
                        
                        
                        self.ltilevalues['UUID'] = self.p_uuid
                        self.ltilevalues['Title'] = self.p_title
                        self.ltilevalues['Channel'] = self.p_channel
                        self.ltilevalues['Original'] = self.p_original
                        self.ltilevalues['Background'] = self.p_background
                        self.ltilevalues['16_9'] = self.p_16_9
                        self.ltile.append(self.ltilevalues.copy())
                        
                        self.ptilevalues['UUID'] = self.p_uuid
                        self.ptilevalues['Title'] = self.p_title
                        self.ptilevalues['Channel'] = self.p_channel
                        self.ptilevalues['Cover'] = self.p_cover
                        self.ptilevalues['Background'] = self.p_background
                        
                        self.ptile.append(self.ptilevalues.copy())
                        
                        
                        
                    self.x += 1
                    
            elif url['channel'] == "Sky Cinema":
                
                intialdatabase = initialdata['state']['tiles'][0]['collectionTiles']
                
                for tile in intialdatabase:
                    if 'uuid' in intialdatabase[self.y]:
                        
                        self.p_uuid = intialdatabase[self.y]['uuid']
                        self.p_title = intialdatabase[self.y]['title'].encode("utf-8")
                        self.p_channel = "sky-premiere" 
                        self.p_original = intialdatabase[self.y]['tileImage']['url']
                        self.p_cover = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/cover/500"
                        self.p_background = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/background/1280"
                        self.p_16_9 = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/16-9/500"
                        
                        self.ltilevalues['UUID'] = self.p_uuid
                        self.ltilevalues['Title'] = self.p_title
                        self.ltilevalues['Channel'] = self.p_channel
                        self.ltilevalues['Original'] = self.p_original
                        self.ltilevalues['Background'] = self.p_background
                        self.ltilevalues['16_9'] = self.p_16_9
                        self.ltile.append(self.ltilevalues.copy())
                
                        self.ptilevalues['UUID'] = self.p_uuid
                        self.ptilevalues['Title'] = self.p_title
                        self.ptilevalues['Channel'] = self.p_channel
                        self.ptilevalues['Cover'] = self.p_cover
                        self.ptilevalues['Background'] = self.p_background

                        self.ptile.append(self.ptilevalues.copy())
                        

                    self.y += 1
                
                intialdatabase = initialdata['state']['galleries']
                
                for gallery in intialdatabase:
                    
                    self.a = 0
                    for tile in intialdatabase[self.z]['collectionTiles']:
                    
                        if 'uuid' in intialdatabase[self.z]['collectionTiles'][self.a]:
                        
                            self.p_uuid = intialdatabase[self.z]['collectionTiles'][self.a]['uuid']
                            self.p_title = intialdatabase[self.z]['collectionTiles'][self.a]['title'].encode("utf-8")
                            self.p_channel = "sky-cinema" 
                            self.p_original = intialdatabase[self.z]['collectionTiles'][self.a]['tileImage']['url']
                            self.p_cover = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/cover/500"
                            self.p_background =  "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/background/1280"
                            self.p_16_9 = "https://images.metadata.sky.com/pd-image/" + self.p_uuid + "/16-9/500"
                            
                            self.ltilevalues['UUID'] = self.p_uuid
                            self.ltilevalues['Title'] = self.p_title
                            self.ltilevalues['Channel'] = self.p_channel
                            self.ltilevalues['Original'] = self.p_original
                            self.ltilevalues['Background'] = self.p_background
                            self.ltilevalues['16_9'] = self.p_16_9
                            self.ltile.append(self.ltilevalues.copy())
                    
                            self.ptilevalues['UUID'] = self.p_uuid
                            self.ptilevalues['Title'] = self.p_title
                            self.ptilevalues['Channel'] = self.p_channel
                            self.ptilevalues['Cover'] = self.p_cover
                            self.ptilevalues['Background'] = self.p_background

                            self.ptile.append(self.ptilevalues.copy())
                            
                        self.a += 1
                    
                    self.z += 1
            
            self.readjson = False;
            
for url in urls:
    
    req = urllib2.Request(url['url'], headers=hdr)      
    parser = MyHTMLParser()
    try:
        html_page = urllib2.urlopen(req)
        sys.stderr.write("Scraping :" + url['channel']+"\n")
        parser.feed(str(html_page.read()))
        html_page.close()
    except urllib2.URLError as e:
        html_page = ""
        pass
    
try: 
    os.makedirs('/etc/enigma2/slyk/')
except OSError:
    if not os.path.isdir('/etc/enigma2/slyk/'):
        raise

filename = '/etc/enigma2/slyk/l_image_scrape.json'
with open(filename, 'w') as f:
    json.dump(parser.ltile, f)

filename = '/etc/enigma2/slyk/p_image_scrape.json'
with open(filename, 'w') as f:
    json.dump(parser.ptile, f)
