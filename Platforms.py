# Platforms
import random
from tkinter import *

class Platforms(object):
    
    def __init__(self, x, y, data):
        self.x, self.y = x, y
        self.photo = data.platformImage
        Platforms.resize(self, data)
        data.platformHeight = self.height
        data.platformWidth = self.width
        data.platforms.add(self)
    
    @staticmethod
    def resize(self, data):
        height = PhotoImage.height(self.photo)
        if (data.height < 400):
            self.photo = self.photo.subsample(2, 2)
        #dimensions of new photo
        if (data.level == 1):
            self.photo = data.trolley
            self.height = data.trolley.height()
            self.width = data.trolley.width()
        else:
            self.height = self.photo.height()
            self.width = self.photo.width()
    
    @staticmethod    
    def draw(canvas, data):
        for platform in data.platforms:
            canvas.create_image(platform.x - data.me.totalScrollX, platform.y - data.me.totalScrollY, image=platform.photo)
        
    
        