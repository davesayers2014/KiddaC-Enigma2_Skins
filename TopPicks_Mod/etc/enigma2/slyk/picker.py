
from PIL import Image, ImageEnhance, ImageOps, ImageFile
import os
import json
import random
import urllib2
import io
import sys  
import math


def create_background(background):
    
    mask = Image.open('/etc/enigma2/slyk/images/mask.png').convert('RGBA')
    mask = mask.resize((backgroundsize[0],backgroundsize[1]),Image.ANTIALIAS)
    plainbg = Image.open(skin_folder + image_folder + "background.jpg").convert('RGBA')
    background = background.resize((backgroundsize[0],backgroundsize[1]),Image.ANTIALIAS)
    backgroundw, backgroundh = background.size
    plainsizew,plainsizeh = plainbg.size
    plainbg.paste(background, (plainsizew - backgroundw, 0), mask)
    plainbg.save(skin_folder + image_folder + "hero.jpg", quality=85)
    return plainbg
    

def download_image(url):
    try:
        fd = urllib2.urlopen(url)
        
    except:
    
        if 'background' in url:
            url = url.replace('background', '16-9')
        if 'cover' in url:
            url = url.replace('cover', '16-9')
        if '16-9' in url:
            url = url.replace('16-9', 'cover')
        try:
            fd = urllib2.urlopen(url)
        except:
            im = ""
            return im
            
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file)
    im = im.convert('RGB')    
    return im
        
        
def crop_image(im,width,height):
        ratio = float(im.size[0])/im.size[1]
        
        if width/height < ratio:
            crop_width = int(height * ratio)
            crop_height = height
        elif width/height > ratio:
            crop_width = width
            crop_height = int(width / ratio)    
        else:
            crop_width = width
            crop_height = height
            
        size = crop_width,crop_height
        tl_w = (crop_width-width)/2
        tl_h = (crop_height-height)/2
        br_w = crop_width-((crop_width-width)/2)
        br_h = crop_height-((crop_height-height)/2)
        
        area = (tl_w, tl_h, br_w ,br_h)
        im = im.resize((size),Image.ANTIALIAS).crop(area)
        im = im.resize((width,height),Image.ANTIALIAS)
        
        contrast = ImageEnhance.Sharpness(im)
        im = contrast.enhance(1.25)
        
        return im
        
        
def add_logo(im, channel, logo_height):
        
        posx= 0
        posy = 0
        
        if skin_size == 1080:
            padding = 6
        else:
            padding = 4

        try:
            logo = Image.open('/etc/enigma2/slyk/channel_logos/' + channel + '.png').convert('RGBA')
        except:
            logo = Image.open('/etc/enigma2/slyk/channel_logos/blank.png').convert('RGBA')
        
        hpercent = (logo_height/float(logo.size[1]))
        wsize =  int((float(logo.size[0])*float(hpercent)))
        logo = logo.resize((wsize,logo_height),Image.ANTIALIAS)
        
        img_w,img_h = im.size
        logo_w, logo_h = logo.size
        
        if logo_halign == "left":
            posx = 0 + padding
        
        if logo_halign == "right":
            posx = img_w - logo_w - padding
            
        if logo_halign == "center":
            posx = ((img_w - logo_w)/2)

        if logo_valign == "top":
            posy = 0 + padding
            
        if logo_valign == "bottom":
            posy = img_h - logo_h - padding
            
        im.paste(logo, (posx, posy), logo)
        
        return im
        


# [ = list
# { = dictionary

with open('/etc/enigma2/settings', 'r') as settingsfile:
    for skin in settingsfile:
        if 'config.skin.primary_skin=' in skin:
            skin = skin.replace("config.skin.primary_skin=" ,"").replace("/skin.xml","")
            # print skin
            sys.stderr.write(skin + "\n")
            sys.stderr.write("Processing...Please Wait.\n")
            break

with open('/etc/enigma2/slyk/p_image_scrape.json') as p_json_data:      
    pfile = json.load(p_json_data)
                
with open('/etc/enigma2/slyk/l_image_scrape.json') as l_json_data:      
    lfile = json.load(l_json_data)


#defaults 
skin_size = 1080
number_of_images = 0
portrait_size = []
landscape_size = []
large_landscape_size = []
background = False
large_landscape_pic = False
portrait_pics = []
landscape_pics = []
logos = True
picons = []
logo_height = 21
logo_valign = "bottom"
logo_halign = "right"
backgroundsize = [1280,720]



if skin.strip() == "slyk-onyx-1080":
    number_of_images = 10
    portrait_size = [202,270]
    landscape_size = [407, 241]
    portrait_pics = [1,2,3,4,5,6,7]
    landscape_pics = [8,9,10]
    skin_folder = "/usr/share/enigma2/slyk-onyx-1080/"
    image_folder = "whatson-gfx/"
    image_prefix = "whatson"
    picons = [7,8,9,10]


elif skin.strip() == "slyk-onyx-720":
    skin_size = 720
    number_of_images = 10
    portrait_size = [134,180]
    landscape_size = [270, 161]
    portrait_pics = [1,2,3,4,5,6,7]
    landscape_pics = [8,9,10]
    skin_folder = "/usr/share/enigma2/slyk-onyx-720/"
    image_folder = "whatson-gfx/"
    image_prefix = "whatson"
    picons = [7,8,9,10]
    logo_height = 14

    
elif skin.strip() == "slyk-1080-r19":
    skin_size = 1080
    number_of_images = 12
    portrait_size = [246,328]
    background = True
    portrait_pics = [1,2,3,4,5,6,7,8,9,10,11,12]
    skin_folder = "/usr/share/enigma2/slyk-1080-r19/"
    image_folder = "toppicks/screens2/"
    image_prefix = "toppicks"
    logos = False
    
elif skin.strip() == "slyk-720-r19":
    skin_size = 720
    number_of_images = 12
    portrait_size = [164,219]
    background = True
    portrait_pics = [1,2,3,4,5,6,7,8,9,10,11,12]
    skin_folder = "/usr/share/enigma2/slyk-720-r19/"
    image_folder = "toppicks/screens2/"
    image_prefix = "toppicks"
    logos = False
    backgroundsize = [853,480]

elif skin.strip() == "slyk-q-1080":
    skin_size = 1080
    number_of_images = 10
    portrait_size = [240,320]
    background = True
    portrait_pics = [1,2,3,4,5,6,7,8,9,10]
    skin_folder = "/usr/share/enigma2/slyk-q-1080/"
    image_folder = "q-toppicks/"
    image_prefix = "toppicks"
    logos = False
    
elif skin.strip() == "slyk-q-720":
    skin_size = 720
    number_of_images = 10
    portrait_size = [160,213]
    background = True
    portrait_pics = [1,2,3,4,5,6,7,8,9,10]
    skin_folder = "/usr/share/enigma2/slyk-q-720/"
    image_folder = "q-toppicks/"
    image_prefix = "toppicks"
    logos = False
    backgroundsize = [853,480]
    
elif skin.strip() == "vskin-1080" or skin.strip() == "vskin-bolt-1080" or skin.strip() == "vskin-red-1080":
    number_of_images = 4
    landscape_size = [252,189]
    landscape_pics = [1,2,3,4]
    skin_folder = "/usr/share/enigma2/"
    image_folder = "vskin-gfx/"
    image_prefix = "whatson"
    logos = False
    
elif skin.strip() == "vskin-720" or skin.strip() == "vskin-bolt-720" or skin.strip() == "vskin-red-720":
    number_of_images = 4
    landscape_size = [168,126]
    landscape_pics = [1,2,3,4]
    skin_folder = "/usr/share/enigma2/"
    image_folder = "vskin-gfx/"
    image_prefix = "whatson"
    logos = False
    
   
    
    

logo_source_folder = "/etc/enigma2/slyk/channel_logos"

y = 0
z = 0
zz = 0


if portrait_pics != []: 
    if pfile != []:
        p_pick =  random.sample(xrange(0,len(pfile)-1), len(portrait_pics)+1)
    else:
        sys.stderr.write("No Valid Portrait Scrapes. Please run /usr/script.skyscraper.sh first. \n")
        sys.exit()
        
if landscape_pics != []:
    if lfile != []:        
        l_pick =  random.sample(xrange(0,len(lfile)-1), len(landscape_pics))
    else:
        sys.stderr.write("No Valid Scrapes. Please run /usr/script.skyscraper.sh first. \n")
        sys.exit()
        

for x in range (1,number_of_images+1):
    
    if x == 1 and large_landscape_pic:
        url = pfile[p_pick[y]]['16_9'].replace('500', str(large_landscape_size[0]*2)) 
        width = large_landscape_size[0]
        height = large_landscape_size[1]
        im = download_image(url)
        
        try:
            im.verify()
            im = crop_image(im,width,height)
            channel = pfile[p_pick[y]]['Channel']
            if logos:
                im = add_logo(im,channel,logo_height)
            im.save(skin_folder + image_folder + image_prefix + str(x) + ".jpg",quality=85)
        except Exception:
           
            pass
        y += 1
        
    elif x == 1 and background and portrait_pics != []:
        background_url = pfile[p_pick[0]]['Background']
        background = download_image(background_url)
        try:
           
            background = create_background(background)
        except Exception:
            pass
                
    elif x == 1 and background and portrait_pics == []:
        background_url = lfile[l_pick[0]]['Background']
        background = download_image(background_url)
        try:
           
            background = create_background(background)
        except Exception:
            pass
                    
    

    if portrait_pics != [] and x in portrait_pics:
        url = pfile[p_pick[y]]['Cover'].replace('500', str(portrait_size[1]*2)) 
        width = portrait_size[0]
        height = portrait_size[1]
        im = download_image(url)
        
        try:
            im.verify()
            im = crop_image(im,width,height)    
            channel = pfile[p_pick[y]]['Channel']
            if logos and x in picons:
                im = add_logo(im,channel,logo_height)
            im.save(skin_folder + image_folder + image_prefix + str(x) + ".jpg",quality=85)
        except Exception:
            pass
        y += 1
    

    if landscape_pics != [] and x in landscape_pics:
        
        url = lfile[l_pick[z]]['16_9'].replace('500', str(landscape_size[0]*2)) 
        width = landscape_size[0]
        height = landscape_size[1]
        im = download_image(url)
        
        try:
            im.verify()
            im = crop_image(im,width,height)
            channel = lfile[l_pick[z]]['Channel']
            if logos:
                im = add_logo(im,channel,logo_height)
            im.save(skin_folder + image_folder + image_prefix + str(x) + ".jpg",quality=85)
        except Exception:
            pass
            
        z += 1
