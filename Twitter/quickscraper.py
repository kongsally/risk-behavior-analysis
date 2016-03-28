""" Quick web scraper """

from lxml import html
import urllib
from BeautifulSoup import *
from PIL import Image
import requests, gzip, urllib, os, re
import validators
import csv
import ssl
import sys
from urllib import urlretrieve
import urlparse

def validate_url(url):
    if url is None:
        return False
    elif re.search(".pdf", url):
        return False
    elif not validators.url(url):
        return False
    else:
        return True

if __name__ == "__main__":

    tweets = open('2015_tweets.csv')
    urls = []
    for row in csv.DictReader(tweets):
        splittweet = row['message'].split(' ')
        for w in splittweet:
            if "http" in w.strip():
                if validate_url(w.strip()):
                    urls.append((w.strip(), row['message'], row['user_id']))

    count = 0
    img_urls = []
    urls_with_imgs = []
    url_count = 0
    for url,tweet,user_id in urls:
        scontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        basename = "./url" + str(url_count)
        try:
            uh = urllib.urlopen(url, context=scontext)
            data = uh.read()
            soup = BeautifulSoup(data)
            for img in soup.findAll('img'):
                imgurl = urlparse.urljoin(url, img['src'])
                file_name = img['src'].split('/')[-1]
                if "jpg" in imgurl:
                    if imgurl not in img_urls:
                        urllib.urlretrieve(imgurl, str(count) + ".jpg")
                        image = Image.open(str(count) + ".jpg")
                        new_width = float(image.size[0])
                        new_height = float(image.size[1])
                        if new_width >= 250.0 or new_height >= 250.0:
                            if url not in urls_with_imgs:
                                urls_with_imgs.append(url)
                                sys.stderr.write("Tweet with img: " + tweet + "\n")
                                print '%s\t%s\t%s'%(user_id, url, tweet)
                            img_urls.append(imgurl)
                            if new_width > 400.0:
                                wpercent = 400.0/new_width
                                new_width = int(new_width* wpercent)
                                new_height = int(new_height * wpercent)
                            if new_height > 400.0:
                                hpercent = 400.0/new_height
                                new_width = int(new_width* hpercent)
                                new_height = int(new_height * hpercent)

                        	newsize = new_width, new_height
                        	image.thumbnail(newsize)
                        	image.save(str(count) + ".jpg", 'JPEG', quality=75, optimize=True)		
                            count += 1
                        os.remove(str(count) + ".jpg")
        except:
            continue
        url_count += 1
