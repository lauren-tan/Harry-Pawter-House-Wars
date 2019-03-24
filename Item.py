# items on platforms
from tkinter import *

class Items(object):
    allItems = []
    
    def __init__(self, x, y):
        self.x, self.y = x, y
        Item.allItems.append(self)
        
class GoldCoin(Items):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = data.goldCoinImage1
        GoldCoin.resize(self, data)
        data.coinWidth = self.image.width()
        data.coinHeight = self.image.height()
        
    @staticmethod    
    def draw(canvas, data):
        for item in Items.allItems:
            if isinstance(item, GoldCoin):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=data.goldCoins[coinIndex])
        
class ResurrectionStone(Items): 
    def __init__(self, x, y):
        super().__init__(x, y)
        self.image = data.resurrectionStoneImage
        ResurrectionStone.resize(self, data)
        data.resurrectionStoneWidth = self.width
        data.resurrectionStoneHeight = self.height
        
    @staticmethod
    def resize(self, data):
        height = PhotoImage.height(self.photo)
        self.size = data.height//height - 2   
        if (self.size % 2) != 0: self.size -= 1
        if (self.size <= 0): self.size = 2
        if (data.height < 650):
            self.photo = self.photo.subsample(self.size, self.size)
        #dimensions of new photo
        self.height = PhotoImage.height(self.photo)
        self.width = PhotoImage.width(self.photo) 
        
    @staticmethod    
    def draw(canvas, data):
        for item in Items.allItems:
            if isinstance(item, ResurrectionStone):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=item.photo)
        