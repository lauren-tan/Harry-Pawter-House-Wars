# items on platforms
from tkinter import *

class Items(object):
    
    def __init__(self, x, y, data):
        self.x, self.y = x, y
        data.items.add(self)
     
class GoldCoin(Items):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.image = data.goldCoinImage1
        self.score = 30
        self.coinIndex = 0
        data.coinWidth = self.width = self.image.width()
        data.coinHeight = self.height = self.image.height()
        
    @staticmethod    
    def draw(canvas, data):
        for item in data.items:
            if isinstance(item, GoldCoin):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=data.goldCoins[item.coinIndex])
                
class SilverCoin(Items):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.image = data.silverCoinImage1
        self.coinIndex = 0
        data.coinWidth = self.width = self.image.width()
        data.coinHeight = self.height = self.image.height()
        self.score = 20
        
    @staticmethod    
    def draw(canvas, data):
        for item in data.items:
            if isinstance(item, SilverCoin):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=data.silverCoins[item.coinIndex])
                
class BronzeCoin(Items):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.image = data.bronzeCoinImage1
        self.coinIndex = 0
        data.coinWidth = self.width = self.image.width()
        data.coinHeight = self.height = self.image.height()
        self.score = 10
        
    @staticmethod    
    def draw(canvas, data):
        for item in data.items:
            if isinstance(item, BronzeCoin):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=data.bronzeCoins[item.coinIndex])
                
class ResurrectionStone(Items): 
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.photo = data.resurrectionStoneImage
        ResurrectionStone.resize(self, data)
        data.resurrectionStoneWidth = self.width
        data.resurrectionStoneHeight = self.height
        self.score = 10
    
    @staticmethod
    def resize(self, data):
        height = PhotoImage.height(self.photo)
        self.size = data.height//height - 2   
        if (self.size % 2) != 0: self.size -= 1
        if (self.size <= 0): self.size = 2
        if (data.height < 700):
            self.photo = self.photo.subsample(self.size, self.size)
        #dimensions of new photo
        self.height = self.photo.height()
        self.width = self.photo.width()
        
    @staticmethod    
    def draw(canvas, data):
        for item in data.items:
            if isinstance(item, ResurrectionStone):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=item.photo)

# level 2 special item
class Snitch(Items):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.image = data.snitchImage1
        self.index = 0
        self.width = self.image.width()
        self.height = self.image.height()
        data.snitchWidth = self.width
        data.snitchHeight = self.height
        self.score = 1000
        
    @staticmethod    
    def draw(canvas, data):
        for item in data.items:
            if isinstance(item, Snitch):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=data.snitches[item.index])
                
# level 3 special item
class Egg(Items):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.image = data.eggImage
        self.index = 0
        self.width = self.image.width()
        self.height = self.image.height()
        self.score = 1000
        data.eggWidth = self.width
        data.eggHeight = self.height
        
    @staticmethod    
    def draw(canvas, data):
        for item in data.items:
            if isinstance(item, Egg):
                canvas.create_image(item.x - data.me.totalScrollX, item.y - data.me.totalScrollY, image=item.image)
                
                
        