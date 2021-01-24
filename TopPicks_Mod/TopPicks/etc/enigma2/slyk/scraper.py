#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import sys

pythonVer = 2
if sys.version_info.major == 3:
    pythonVer = 3


if pythonVer == 2:
    print("python 2")
    from urllib2 import urlopen, Request, unquote, URLError
else:
    from urllib.request import urlopen, Request
    from urllib.parse import unquote
    from urllib.error import URLError


urls = []
urls.append({'channel': 'Sky Cinema', 'url': 'https://www.sky.com/watch/channel/sky-cinema/'})
urls.append({'channel': 'Sky One', 'url': 'https://www.sky.com/watch/channel/sky-one/'})
urls.append({'channel': 'Sky Witness', 'url': 'https://www.sky.com/watch/channel/sky-witness/'})
urls.append({'channel': 'Sky Atlantic', 'url': 'https://www.sky.com/watch/channel/sky-atlantic/'})
# urls.append({'channel': 'Sky Documentaries', 'url': 'https://www.sky.com/watch/channel/sky-documentaries/'})
# urls.append({'channel': 'Sky Comedy', 'url': 'https://www.sky.com/watch/channel/sky-comedy/'})
# urls.append({'channel': 'Sky Crime', 'url': 'https://www.sky.com/watch/channel/sky-crime/'})
# urls.append({'channel': 'Sky Nature', 'url': 'https://www.sky.com/watch/channel/sky-nature/'})

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}


def scraper():
    tilelist = []
    tilevalues = {}
    tilevalues = {}
    response = ""
    content = []

    for url in urls:
        req = Request(url['url'], headers=hdr)

        try:
            response = urlopen(req)
            sys.stderr.write("Scraping :" + url['channel'] + "\n")
        except URLError as e:
            print(e)
            response = ""
            pass

        initialdatabase = {}

        if response:
            response = response.read().decode('utf-8')
            content = response.split('\n')

            for line in content:
                if '<script id="initialData" type="application/json">' in line:
                    line = str(line)
                    line = line.replace('<script id="initialData" type="application/json">', '').replace('</script>', '')
                    jsonsnippet = unquote(line)

                    initialdata = json.loads(jsonsnippet)

                    if url['channel'] != "Sky Cinema":
                        if 'state' in initialdata:
                            if 'tiles' in initialdata['state']:

                                initialdatabase = initialdata['state']['tiles']

                                for tile in initialdatabase:

                                    t_uuid = ''
                                    t_title = ''
                                    t_channel = ''
                                    t_original = ''
                                    t_cover = ''
                                    t_background = ''
                                    t_16_9 = ''

                                    if 'uuid' in tile:
                                        t_uuid = tile['uuid'].replace('series:', '').replace('programme:', '').replace('season:', '')

                                        if 'title' in tile:
                                            t_title = tile['title'].replace("&nbsp;", "").replace("<br>", "").replace("%E2%80%99", "'").encode("utf-8")

                                        if 'brand' in tile:
                                            if'id' in tile['brand']:
                                                t_channel = tile['brand']['id']

                                        if 'tileImage' in tile:
                                            if 'url' in tile['tileImage']:
                                                t_original = tile['tileImage']['url']

                                            else:
                                                if 'medium' in tile['tileImage']:
                                                    t_original = tile['tileImage']['medium']

                                        t_cover = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/cover/500"
                                        t_background = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/background/1280"
                                        t_16_9 = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/16-9/500"

                                        tilevalues['UUID'] = str(t_uuid)
                                        tilevalues['Title'] = str(t_title)
                                        tilevalues['Channel'] = str(t_channel)
                                        tilevalues['Original'] = str(t_original)
                                        tilevalues['Background'] = str(t_background)
                                        tilevalues['16_9'] = str(t_16_9)
                                        tilevalues['Cover'] = str(t_cover)

                                        tilelist.append(tilevalues.copy())

                    if url['channel'] == "Sky Cinema":

                        if 'state' in initialdata:
                            if 'tiles' in initialdata['state']:

                                initialdatabase = initialdata['state']['tiles'][0]['collectionTiles']

                                for tile in initialdatabase:

                                    t_uuid = ''
                                    t_title = ''
                                    t_channel = ''
                                    t_original = ''
                                    t_cover = ''
                                    t_background = ''
                                    t_16_9 = ''

                                    if 'uuid' in tile:
                                        t_uuid = tile['uuid'].replace('series:', '').replace('programme:', '').replace('season:', '')

                                        if 'title' in tile:
                                            t_title = tile['title'].replace("&nbsp;", "").replace("<br>", "").replace("%E2%80%99", "'").encode("utf-8")

                                        t_channel = "sky-premiere"

                                        if 'tileImage' in tile:
                                            if 'url' in tile['tileImage']:
                                                t_original = tile['tileImage']['url']
                                            elif 'medium' in tile['tileImage']:
                                                t_original = tile['tileImage']['medium']

                                        t_cover = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/cover/500"
                                        t_background = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/background/1280"
                                        t_16_9 = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/16-9/500"

                                        tilevalues['UUID'] = str(t_uuid)
                                        tilevalues['Title'] = str(t_title)
                                        tilevalues['Channel'] = str(t_channel)
                                        tilevalues['Original'] = str(t_original)
                                        tilevalues['Background'] = str(t_background)
                                        tilevalues['16_9'] = str(t_16_9)
                                        tilevalues['Cover'] = str(t_cover)

                                        tilelist.append(tilevalues.copy())

                            if 'galleries' in initialdata['state']:
                                initialdatabase = initialdata['state']['galleries']

                                for gallery in initialdatabase:
                                    if 'collectionTiles' in gallery:
                                        for tile in gallery['collectionTiles']:

                                            if 'uuid' in tile:
                                                t_uuid = tile['uuid'].replace('series:', '').replace('programme:', '').replace('season:', '')

                                                if 'title' in tile:
                                                    t_title = tile['title'].replace("&nbsp;", "").replace("<br>", "").replace("%E2%80%99", "'").encode("utf-8")

                                                t_channel = "sky-cinema"

                                                if 'tileImage' in tile:
                                                    if 'url' in tile['tileImage']:
                                                        t_original = tile['tileImage']['url']
                                                    elif 'medium' in tile['tileImage']:
                                                        t_original = tile['tileImage']['medium']

                                                t_cover = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/cover/500"
                                                t_background = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/background/1280"
                                                t_16_9 = "https://images.metadata.sky.com/pd-image/" + t_uuid + "/16-9/500"

                                                tilevalues['UUID'] = str(t_uuid)
                                                tilevalues['Title'] = str(t_title)
                                                tilevalues['Channel'] = str(t_channel)
                                                tilevalues['Original'] = str(t_original)
                                                tilevalues['Background'] = str(t_background)
                                                tilevalues['16_9'] = str(t_16_9)
                                                tilevalues['Cover'] = str(t_cover)

                                                tilelist.append(tilevalues.copy())

                    filename = '/etc/enigma2/slyk/test %s.json' % url['channel']
                    with open(filename, 'w') as f:
                        json.dump(initialdatabase, f)

            filename = '/etc/enigma2/slyk/image_scrape.json'
            with open(filename, 'w') as f:
                json.dump(tilelist, f)


scraper()
