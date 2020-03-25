import pygame
from bs4 import *
import requests as rq
import os
import soupsieve
from bs4 import BeautifulSoup
import urllib.request as urllib2
from requests_futures.sessions import FuturesSession
import random
import json
import itertools
import uuid
import sys
import re
import requests
import time
import datetime
import pandas as pd
import logging
from tkinter import *
from tkinter import messagebox

#log file
logging.basicConfig(filename='test.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

clock = pygame.time.Clock()
progress = 0

#Colours
background = ((0,0,0))
blue = (0,0,200)
bright_blue = (0,0,255)
green = (0,100,0)
bright_green = (0,128,0)
black = (0,0,0)
white = (255,255,255)

pygame.init()
pygame.display.set_caption('Kihtraks Image Downloader')
screen = pygame.display.set_mode([800,600])
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
FONT = pygame.font.Font(None, 32)
query = ""
time_secs = 0
smallfont = pygame.font.SysFont("comicsansms",25)

def text_objects(text , color , size):
    if size == small:
        textSurface = smallfont.render(text , True , color)

    return textSurface , textSurface.get_Rect()

def loading(progress):
    if progress < 100:
        text = smallfont.render("Loading : " + str(int(progress)) + "%" , True , bright_green)

    else:
        text = smallfont.render("Download Completed", True , bright_green)

    screen.blit(text , [300,300])

def message_to_screen(msg, color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2, display_height/2 + y_displace)
    screen.blit(textSurf, textRect)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    logging.debug(self.text)
                    global query 
                    query = self.text
                    print(query)
                    logging.debug(query)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class WebCrawler(object):
    def __init__(self, Query, numberImage=100):
        
        self.maxImage = numberImage
        self.query = Query
        self.baseurl = BaseUrl(Query=self.query)

    def soup(self):
        
        response = requests.get(self.baseurl.baseurl, headers=self.baseurl.headers)
        return BeautifulSoup(response.text, 'html.parser')

    def getImageURl(self):

        if (self.maxImage >100):
            print("Number of Images cannot exceeds 100")
            logging.debug("Number of Images cannot exceeds 100")
        else:
            soup = self.soup()
            image_elements = soup.find_all("div", {"class": "rg_meta"})
            metadata_dicts = (json.loads(e.text) for e in image_elements)
            link_type_records = ((d["ou"], d["ity"]) for d in metadata_dicts)
            return itertools.islice(link_type_records, self.maxImage)


class GoogleImageDownloader(object):
    def __init__(self, Query, numberImage=100):
        
        self.query = Query
        self.numofImage = numberImage
        self.crawler = WebCrawler(Query=self.query, numberImage=self.numofImage)

    def getUrls(self):
        
        data = self.crawler.getImageURl()
        data = [ (i, url) for i, (url, image_type) in enumerate(data) ]
        return data

    def saveCsv(self):
        
        data = self.getUrls()
        df = pd.DataFrame(data=data)
        df.to_csv("Result.csv")
        print("Saved on your Computer with Result.csv")
        logging.debug("Saved on your Computer with Result.csv")

    def saveJson(self):
        
        data = self.getUrls()
        df = pd.DataFrame(data=data)
        df.to_json("Result.json")
        print("Saved on your Computer with Result.json")
        logging.debug("Saved on your Computer with Result.json")

    def downloadImages(self):

        data = self.getUrls()
        df = pd.DataFrame(data=data, columns=["No", "Url"])

        start = datetime.datetime.now()

        with FuturesSession() as sess:
            futures = [sess.get(url) for i, url in enumerate(df["Url"].to_list())]
            for i, url in enumerate(futures):

                print("Downloading Image {}".format(i))
                logging.debug("Downloading Image {}".format(i))

                data = url.result().content

                cwd = os.getcwd()                           # get CWD
                folder = 'Images'                           # Create Folder Logs
                newPath = os.path.join(cwd, folder)         # change Path


                try:
                    """ try to create directory """
                    os.mkdir(newPath)                   # create Folder

                except Exception as e:

                    """ Directory already exists """

                    filename = "{}.jpg".format(i)
                    completePath = os.path.join(newPath, filename)

                    with open(completePath, "wb") as f:
                        f.write(data)

        end = datetime.datetime.now()
        print("Total Time : {}".format(end-start))
        logging.debug("Total Time : {}".format(end-start))

class BaseUrl(object):
    def __init__(self, Query=''):
        
        self.url = "https://www.google.co.in/search?q=%s&source=lnms&tbm=isch"
        self.__query = Query
        self.baseurl = self.url % self.__query
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"}
        print(self.baseurl)
        logging.debug(self.baseurl)

def text_objects(text, font):
    
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac):
    
    mouse = pygame.mouse.get_pos()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def image_scrape():  
    
    start = time.time()
    html_page = urllib2.urlopen("https://imgur.com/search?q=" + query)
    soup = BeautifulSoup(html_page , features = 'lxml')
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))    
        
    for i in range (5):
        result = requests.get("http:" + images[i], stream=True)
        if result.status_code == 200:
            image = result.raw.read()
            open(str(i)+".jpg","wb").write(image)

    end = time.time()
    global time_secs
    time_secs = (end - start)
    print("Total Time : {}".format(end-start))
    logging.debug("Total Time : {}".format(end-start))
    print(time_secs)
    logging.debug(time_secs)

    df = pd.DataFrame(data=images)
    df.to_csv("Result_Scrape.csv")
    print("Saved on your Computer with Result_Scrape.csv")
    logging.debug("Saved on your Computer with Result_Scrape.csv")

    df = pd.DataFrame(data=images)
    df.to_json("Result_Scrape.json")
    print("Saved on your Computer with Result_Scrape.json")
    logging.debug("Saved on your Computer with Result_Scrape.json")

    display_scrape_status()

def display_scrape_status():
    
    for i in pygame.event.get():
            if i.type == pygame.QUIT:
                    window = Tk()
                    window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                    window.withdraw()
                    if (messagebox.askokcancel('Kihtraks Image Downloader', 'Please go back to the home page') == True):
                        print("Go back to home page")
                        logging.debug("Go back to home page")
                    else:
                        continue
                
                    window.deiconify()
                    window.destroy()
                    window.quit() 
    
    returning = False
    progress_shown = False
    progress = 0    
    while(returning != True):
        screen.fill(background)
        for event in pygame.event.get():
            pass 
        
        time_count = random.randint(1,1)
        increase = random.randint(1,20)
        progress += increase
        if (progress/2) > 100:
            pygame.draw.rect(screen, green, [301, 225, 200, 45])
        else:
            pygame.draw.rect(screen, green, [301, 225, progress, 45])

        loading(progress/2)
        pygame.display.flip()
        time.sleep(time_count) 
        if(progress/2 > 100):
            screen.fill(background)
            print("Got in back button")
            display_scrape_back()

def display_scrape_back():
    returning = False
    progress_shown = False
    while(returning != True):
        screen.fill(background)
        for event in pygame.event.get():
            pass 
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Back button
        #Button Highlighting on hovering
        if 100+150 > mouse[0] > 100 and 50+50 > mouse[1] > 50:
            pygame.draw.rect(screen, bright_blue,(100,50,150,50))
            if click[0] == 1:
                returning = True 
        else:
            pygame.draw.rect(screen, blue,(100,50,150,50))
        
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Back", smallText)
        textRect.center = ( (100+(150/2)), (50+(50/2)) )
        screen.blit(textSurf, textRect)
        text = smallfont.render("Download Completed", True , bright_green)
        screen.blit(text , [300,300])
        pygame.draw.rect(screen, green, [302, 225, 200, 45])
        pygame.display.update()
    home()

def image_download():
    
    start = time.time()
    html_page = urllib2.urlopen(query)
    soup = BeautifulSoup(html_page , features = 'lxml')
    images = []
    for img in soup.findAll('img'):
        images.append(img.get('src'))
    
    for i in range (5):
        result = requests.get("http:" + images[i], stream=True)
        if result.status_code == 200:
            image = result.raw.read()
            open(str(i)+".jpg","wb").write(image)

    end = time.time()
    global time_secs
    time_secs = (end - start)
    print("Total Time : {}".format(end-start))
    logging.debug("Total Time : {}".format(end-start))
    print(time_secs)
    logging.debug(time_secs)

    df = pd.DataFrame(data=images)
    df.to_csv("Result_Image_Download.csv")
    print("Saved on your Computer with Result_Image_Download.csv")
    logging.debug("Saved on your Computer with Result_Image_Download.csv")
    
    df = pd.DataFrame(data=images)
    df.to_json("Result_Image_Download.json")
    print("Saved on your Computer with Result_Image_Download.json")
    logging.debug("Saved on your Computer with Result_Image_Download.json")
    
    image_download_status()

def image_download_status():
    
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            window = Tk()
            window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
            window.withdraw()
            if (messagebox.askokcancel('Kihtraks Image Downloader', 'Please go back to the home page') == True):
                print("Go back to home page")
                logging.debug("Go back to home page")
            else:
                continue                
            window.deiconify()
            window.destroy()
            window.quit() 
    
    returning = False
    progress_shown = False
    progress = 0    
    while(returning != True):
        screen.fill(background)
        for event in pygame.event.get():
            pass 
        
        time_count = random.randint(1,1)
        increase = random.randint(1,20)
        progress += increase
        if (progress/2) > 100:
            pygame.draw.rect(screen, green, [302, 225, 200, 45])
        else:
            pygame.draw.rect(screen, green, [302, 225, progress, 45])

        loading(progress/2)
        pygame.display.flip()
        time.sleep(time_count) 
        if(progress/2 > 100):
            screen.fill(background)
            print("Got in back button")
            display_image_back()

def display_image_back():
    returning = False
    progress_shown = False
    while(returning != True):
        screen.fill(background)
        for event in pygame.event.get():
            pass 
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Back button
        #Button Highlighting on hovering
        if 100+150 > mouse[0] > 100 and 50+50 > mouse[1] > 50:
            pygame.draw.rect(screen, bright_blue,(100,50,150,50))
            if click[0] == 1:
                returning = True 
        else:
            pygame.draw.rect(screen, blue,(100,50,150,50))
        
        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Back", smallText)
        textRect.center = ( (100+(150/2)), (50+(50/2)) )
        screen.blit(textSurf, textRect)
        text = smallfont.render("Download Completed", True , bright_green)
        screen.blit(text , [300,300])
        pygame.draw.rect(screen, green, [302, 225, 200, 45])
        pygame.display.update()
    home()

def home():
    input_box1 = InputBox(325, 100, 140, 32)
    input_boxes=[input_box1]    
    running = True
    while running:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                window = Tk()
                window.eval('tk::PlaceWindow %s center' % window.winfo_toplevel())
                window.withdraw()
                if (messagebox.askyesno('Kihtraks Image Downloader', 'Do you really want to quit?') == True):
                    print("Quitting")
                    logging.debug("Qutting")
                    running = False
                else:
                    continue
                
                window.deiconify()
                window.destroy()
                window.quit()

            for box in input_boxes:
                box.handle_event(i)

        for box in input_boxes:
            box.update()
        
        screen.fill(background)
        
        for box in input_boxes:
            box.draw(screen)    
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        #Button1 Highlighting on hovering
        if 100+200 > mouse[0] > 100 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(screen, bright_blue,(100,450,200,50))
            if click[0] == 1:
                image_download()

        else:
            pygame.draw.rect(screen, blue,(100,450,200,50))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("URL Download", smallText)
        textRect.center = ( (100+(200/2)), (450+(50/2)) )
        screen.blit(textSurf, textRect)

        #Button2 Highlighting on hovering
        if 550+200 > mouse[0] > 550 and 450+50 > mouse[1] > 450:
            pygame.draw.rect(screen, bright_green,(550,450,200,50))
            if click[0] == 1:
                image_scrape()

        else:
            pygame.draw.rect(screen, green,(550,450,200,50))

        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Scrape Images", smallText)
        textRect.center = ( (550+(200/2)), (450+(50/2)) )
        screen.blit(textSurf, textRect)
        
        pygame.display.update()
        
    pygame.quit()

home()