# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 18:17:12 2020

@author: Karthikeyan S CED16I015
"""
import os
import requests
import sys
import shutil
import re
import threading
#import img2pdf
from fpdf import FPDF
from BeautifulSoup import BeautifulSoup as soup

THREAD_COUNTER = 0
THREAD_MAX     = 5
imagelist  = []
def get_source(link):
    r = requests.get(link)
    if r.status_code == 200:
        return soup(r.text)
    else:
        sys.exit("Invalid Response Received")

def filter(html):
    imgs = html.findAll("img")
    if imgs:
        return imgs
    else:
        sys.exit("No images detected on the page")

def requesthandle(link, name):
    global THREAD_COUNTER
    THREAD_COUNTER += 1
    try:
        r = requests.get(link, stream=True)
        if r.status_code == 200:
            r.raw.decode_content = True
            f = open( name, "wb")
            shutil.copyfileobj(r.raw, f)
            imagelist.append(name)
            f.close()
            print("Downloaded Image: %s" % name)
    except Exception, error:
        print("Error Occured with %s : %s" % (name, error))
    THREAD_COUNTER -= 1

def main():
    print("Device Drivers Mid Assignment Review")
    Website = raw_input("Please enter the website from which you want to download images : ")
    print(Website)
    
    #"https://wallpapercave.com/pokemon-pc-desktop-wallpapers"
    html = get_source(Website)
    tags = filter(html)
    for tag in tags:
        src = tag.get("src")
        if src:
            src = re.match( r"((?:https?:\/\/.*)?\/(.*\.(?:png|jpg)))", src )
            if src:
                (link, name) = src.groups()
                #if not link.startswith("http"):
                #    link = "https://www.drivespark.com" + link
                _t = threading.Thread( target=requesthandle, args=(link, name.split("/")[-1]) )
                _t.daemon = True
                _t.start()

                while THREAD_COUNTER >= THREAD_MAX:
                    pass

    while THREAD_COUNTER > 0:
        pass

    if(THREAD_COUNTER <= 0):
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open("output.pdf", "wb") as f:
            f.write(img2pdf.convert([i for i in dir_path if i.endswith(".jpg") or i.endswith(".png")]))
        """

        pdf = FPDF()
        # imagelist is the list with all image filenames
        for image in imagelist:
            pdf.add_page()
            pdf.image(image,x=100,y=100,w=100,h=100)
        pdf.output("images.pdf", "F")
        print("Downloaded images have been saved in the pdf images.pdf")

    
if __name__ == "__main__":
    main()
    