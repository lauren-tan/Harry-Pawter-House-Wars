# Game Character
from tkinter import *
import string
import random
from Bullets import Bullets

class Character(object):
    allCharacters = set()
    
    def __init__(self, PID, data):
        self.PID = PID
        self.number = 0
        if (self.PID[-1] in string.digits): self.number = int(self.PID[-1])
        self.x, self.y = data.width//4, int(10*data.jump) #initial cx, cy
        self.life = 100
        self.score = 0
        self.coins = 0
        self.highScore = 0
        self.wand, self.stone, self.cloak = False, False, False
        self.index = random.randint(0,3) 
        self.win = False
        self.gameOver = False
        self.jump = False
        self.house = "Gryffindor"
        self.jumpStart, self.jumpCount = 0, 0 #when jump starts, jump in progress/not in progress
        self.jumps = 0 #number of consecutive jumps in the air
        self.photo = data.broomstickImage
        self.bullets = data.bullets
        self.totalScrollX, self.totalScrollY = 0, 0
        self.collision = 0
        self.patronus = 0
        Character.allCharacters.add(self)
        
    def move(self, dx, dy, data):
        if (dx != 0): #move horizontally
            self.totalScrollX += int(data.scrollX)
        if (dy < 0): #jumping up
            if (dy == -data.jumpStep):
                self.jump, self.jumpCount = True, 0
            else:
                self.totalScrollY += int(dy)
        if (dy > 0): 
            self.totalScrollY += int(dy) 
                        
    def changePID(self, PID):
        self.PID = PID
        if (self.PID[-1] in string.digits): self.number = int(self.PID[-1])
        
    def shoot(self, data):
        Bullets(data, self.x, self.y)    
           
class FlyingCharacter(Character):
    def __init__(self, PID, data):
        super().__init__(PID, data)
        FlyingCharacter.resize(self, data)
        self.scoreSize = self.height
        if (data.level == 1):
            self.height = data.pusheen1.height()
            self.width = data.pusheen1.width()
        data.characterHeight = self.height
        data.characterWidth = self.width
        self.y = data.height/2 - data.characterHeight/4 - data.platformHeight/4

    def resize(self, data):
        height = self.photo.height()
        self.size = data.height//height - 2   
        if (self.size % 2) != 0: self.size -= 1
        if (self.size <= 0): self.size = 2
        if (data.height < 650):
            self.photo = self.photo.subsample(self.size, self.size)
        # dimensions of new photo
        self.height = self.photo.height()
        self.width = self.photo.width()
        self.fontSize = self.height/3
        self.numSize = self.height/5
            
    def draw(self, canvas, scrollX, scrollY, data):
        if (self.gameOver): return
        if (data.level == 1): 
            if (self.house == "Ravenclaw"): charImage = data.ravenclaws[self.index]
            elif (self.house == "Hufflepuff"): charImage = data.hufflepuffs[self.index]
            elif (self.house == "Slytherin"): charImage = data.slytherins[self.index]
            else: charImage = data.pusheens[self.index]
        elif (data.level == 2 or data.level == 3): charImage = self.photo
        canvas.create_image(self.x - scrollX, self.y - scrollY, image=charImage)
        # player name
        numFont = "System %d bold" % (self.numSize)
        if (data.level == 1): cx = self.x
        else: cx = self.x + self.width/6
        cy = self.y - self.height
        canvas.create_text(cx - scrollX, cy - scrollY, text=self.PID, font=numFont)
        # draw life percentage
        lifeText = "%d%s" % (self.life, "%")
        canvas.create_text(cx - scrollX , cy - scrollY - self.height/5, text=lifeText, font=numFont)
        # score title
        if (self.house == "Gryffindor"): houseImage = data.gryffindorLettersImage
        elif (self.house == "Hufflepuff"): 
            houseImage = data.hufflepuffLettersImage
            self.photo = data.hufflepuffBroomstickImage
        elif (self.house == "Ravenclaw"): 
            houseImage = data.ravenclawLettersImage
            self.photo = data.ravenclawBroomstickImage
        elif (self.house == "Hufflepuff"):
            houseImage = data.hufflepuffLettersImage
            self.photo = data.hufflepuffBroomstickImage
        else: 
            houseImage = data.slytherinLettersImage
            self.photo = data.slytherinBroomstickImage
        x, y = 0, data.height*8/9
        if (data.numPlayers == 1): x = data.width/2
        elif (data.numPlayers == 2):
            if (self.number == 1): x = data.width/3
            elif (self.number == 2): x = data.width*2/3
        elif (data.numPlayers == 3):
            if (self.number == 1): x = data.width/4
            elif (self.number == 2): x = data.width/2
            elif (self.number == 3): x = data.width*3/4
        else: # 4 players
            if (self.number == 1): x = data.width/8
            elif (self.number == 2): x = data.width/8 + data.width/4
            elif (self.number == 3): x = data.width/8 + data.width/2
            elif (self.number == 4): x = data.width/8 + data.width*3/4
        canvas.create_image(x, y, image=houseImage)
        width, height = houseImage.width(), houseImage.height()
        scoreFont = "System %d bold" % (self.fontSize)
        canvas.create_text(x, y + height, text="%d" % self.score, font=scoreFont)
        # draw time left
        x, y = data.width/2 - data.timeImage.width()/2, data.height/14
        canvas.create_image(x, y, image=data.timeImage)
        canvas.create_text(x + data.timeImage.width(), y, 
        text="%d%s" % ((data.timeLimit - data.time)//1000, "s"), font=scoreFont)
            
