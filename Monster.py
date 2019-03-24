# Monster (for maze)
import random
from tkinter import *

class Monster(object):
    
    def __init__(self, x, y, data):
        self.x, self.y = x, y
        self.width, self.height = 10, 10
        data.monsters.add(self)
    
    @staticmethod
    def move(dx): #monsters only move left
        for monster in data.monsters:
            monster.x += dx

# level 1 monster
class Muggle(Monster):
    
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.photo = data.muggleImage
        self.height = self.photo.height()
        self.width = self.photo.width()
        data.muggleWidth = self.height
        data.muggleHeight = self.width
    
    def resize(self, data):
        height = PhotoImage.height(self.photo)
        self.size = data.height//height - 2   
        if (self.size % 2) != 0: self.size -= 1
        if (self.size <= 0): self.size = 2
        if (data.height < 650):
            self.photo = self.photo.subsample(self.size, self.size)
        #dimensions of new photo
        self.height = self.photo.height()
        self.width = self.photo.width()
        
    @staticmethod    
    def draw(canvas, data):
        for monster in data.monsters:
            canvas.create_image(monster.x - data.me.totalScrollX, monster.y - data.me.totalScrollY, image=monster.photo)

# level 2 monster        
class Dementor(Monster):
    
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.photo = data.dementorImage.subsample(2,2)
        self.height = self.photo.height()
        self.width = self.photo.width()
       # Dementor.resize(self, data)
        data.dementorWidth = self.height
        data.dementorHeight = self.width
    
    def resize(self, data):
        height = PhotoImage.height(self.photo)
        self.size = data.height//height - 2   
        if (self.size % 2) != 0: self.size -= 1
        if (self.size <= 0): self.size = 2
        if (data.height < 650):
            self.photo = self.photo.subsample(self.size, self.size)
        #dimensions of new photo
        self.height = self.photo.height()
        self.width = self.photo.width()
        
    @staticmethod    
    def draw(canvas, data):
        for monster in data.monsters:
            canvas.create_image(monster.x - data.me.totalScrollX, monster.y - data.me.totalScrollY, image=monster.photo)
            
# level 3 monster
class Dragon(Monster):
    def __init__(self, x, y, dragonType, data):
        super().__init__(x, y, data)
        self.dragonType = data.redDragons
        if (dragonType == "blue"): self.dragonType = data.blueDragons
        elif (dragonType == "green"): self.dragonType = data.greenDragons
        self.index = 0
        self.photo = self.dragonType[self.index]
        self.width, self.height = self.photo.width(), self.photo.height()
        data.dragonWidth, data.dragonHeight = self.width, self.height
    
    @staticmethod    
    def draw(canvas, data):
        for monster in data.monsters:
            canvas.create_image(monster.x - data.me.totalScrollX, monster.y - data.me.totalScrollY, image=monster.dragonType[monster.index])


        
        