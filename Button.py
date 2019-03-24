# Buttons

from tkinter import *

class Button(object):
    
    def __init__(self, image, text, command, data):
        self.button = Button(data.root, width = image.width, 
                      height = image.height, text = text, compound = Center,
                      bg = "black", command = command)  
        self.clicks, self.totalClicks = 0, 0
    
    

