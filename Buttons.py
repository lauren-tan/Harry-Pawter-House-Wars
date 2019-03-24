# Buttons
from tkinter import *

class MyButton(object):
    
    def __init__(self, image, text, command, data):
        self.myButton = Button(data.root, image=image, width = 50, 
                      height = 50, text = text, compound = CENTER,
                      bg = "black", command = command)  
                      #self.canvas.create_window
        self.myButton.image = image
        
        self.clicks, self.totalClicks = 0, 0
        
    def __hash__(self):
        return hash(self.myButton)
        




    
    

