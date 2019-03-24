# Client
#######e##############################################################
# Sockets Client template from Rohan Varma, modified by Kyle Chin: 
# https://drive.google.com/drive/folders/0B3Jab-H-9UIiZ2pXMExjdDV1dW8
######################################################################

import socket
import threading
from queue import Queue

HOST = "127.0.0.1" # put your IP address here if playing on multiple computers
PORT = 50003

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.connect((HOST,PORT))
print("connected to server")

def handleServerMsg(server, serverMsg):
    server.setblocking(1)
    msg = ""
    command = ""
    while True:
        msg += server.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverMsg.put(readyMsg)
            command = msg.split("\n")

# Animation framework from 15-112 website 
# https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
import random
from tkinter import *
from tkinter import messagebox
from Platforms import Platforms
from Items import Items, GoldCoin, SilverCoin, BronzeCoin, ResurrectionStone, Snitch, Egg
from Character import *
from Bullets import Bullets, Spell, Patronus
from Monster import Monster, Muggle, Dementor, Dragon
from loadImages import loadImages

##################################
# customize these functions
##################################

def createObjects(data):
    # create items
    data.items = set()
    GoldCoin(0, 0, data)
    SilverCoin(0, 0, data)
    BronzeCoin(0, 0, data)
    ResurrectionStone(0, 0, data)
    Snitch(0, 0, data)
    Egg(0, 0, data)
    data.storage = set()
    data.items.clear()
    # create monsters
    data.monsters = set()
    Muggle(0, 0, data)
    Dementor(0, 0, data)
    Dragon(0, 0, "red", data)
    data.monsters.clear()
    data.monsterCollisions = set()
    # create bullets
    data.bullets = set()
    Spell(0, 0, data)
    data.bullets.clear()
    
def init(data):
    data.start = False
    data.message = "None" # for login
    data.drawn = 0
    data.temp = 0 
    data.mode = "start"
    data.timeLimit = 20000 # 30 seconds 
    loadImages(data) 
    data.time = 0
    data.level = 1
    data.numPlayers = -1
    data.numPlayerClicks = 0
    data.myClicks = 0
    data.highScore = 0
    data.play = False
    data.nextClicks = 0
    data.minTotalScrollX, data.minTotalScrollY = 0, 0 # for last player
    data.maxTotalScrollX, data.maxTotalScrollY = 0, 0 # for first player
    createObjects(data) # all objects of the game (except the characters)
    data.scrollX = data.width//50 # speed of horizontal scrolling
    data.scrollY = data.scrollX # speed of vertical scrolling
    data.jump, data.speed = data.height//5, data.width//20
    data.jumpStep = data.jump//15
    data.platforms = set()
    Platforms(0, 0, data)
    data.platforms.clear()
    data.me = FlyingCharacter("Lonely", data)
    Patronus(0, 0, data)
    data.bullets.clear()
    data.others = dict() # other players
            
###################################
# mode dispatcher
###################################

def mousePressed(event, data): pass

def keyPressed(event, data):
    #if (data.mode == "play"): 
    playKeyPressed(event, data)
    
def timerFired(data): playTimerFired(data)

def redrawAll(canvas, data):
    if (data.mode == "start"): startRedrawAll(canvas, data)
    elif (data.mode == "chooseHouse"): houseRedrawAll(canvas, data)
    elif (data.mode == "store"): storeRedrawAll(canvas, data)
    elif (data.mode == "instructions"): instructionsRedrawAll(canvas, data)
    elif (data.mode == "play"): playRedrawAll(canvas, data)
    elif (data.mode == "gameOver"): gameOverRedrawAll(canvas, data)
   # elif (data.mode == "scores"): scoresRedrawAll(canvas, data)

####################################
# start mode
####################################

def numPlayerClick(data, buttonID):
    data.numPlayerClicks += 1
    # button already clicked 
    if (data.numPlayerClicks > 1):
        data.buttonDown.config(relief=RAISED)
        data.buttonDown.config(bg=rgbString(100,107,130))
    # data.numPlayers is the number of other players
    data.numPlayers = buttonID 
    if (buttonID == 1): data.buttonDown =  data.oneButton
    elif (buttonID == 2): data.buttonDown = data.twoButton
    elif (buttonID == 3): data.buttonDown = data.threeButton
    else: data.buttonDown = data.fourButton
    data.buttonDown.config(relief=SUNKEN)
    data.buttonDown.config(bg=rgbString(50,70,115))
    if (data.numPlayerClicks == 1):
        data.scrollX = data.width//40
    
def loginClick(data):
    data.drawn = 0 
    data.usernameEntry = data.username.get()
    data.me.PID = data.usernameEntry
    msg = "nameChanged %s\n" % data.me.PID
    print ("sending: ", msg,)
    data.server.send(msg.encode())
    data.passwordEntry = data.password.get()
    # store username and password in storage.txt if it's not there already
    findLogin(data)

# basic template for File IO from https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
def readFile(path):
    with open(path, "rt") as f:
        return f.read()
        
def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)
      
def findLogin(data):
    found = False
    file = readFile("storage.txt")
    f = file.splitlines()
    for line in f:
        line = line.split(" ") # convert to a list
        if (data.usernameEntry == line[0]): # username in file
            found = True
            if (data.passwordEntry == line[1]):
                found = True
                data.me.coins = int(line[2])
                data.mode = "chooseHouse"
            else: 
            # from http://www.kosbie.net/cmu/spring-17/15-112/notes/notes-tkinter-demos.html
                message = "Wrong password! Try again."
                messagebox.showerror("Error", message)
                return
    if (found == False): # new user          
        file += "%s %s %d\n" % (data.usernameEntry, data.passwordEntry, 0)
        writeFile("storage.txt", file)
        found = True
        msg = "newUser %s %s\n" % (data.usernameEntry, data.passwordEntry)
        print("sending: ", msg, )
        data.server.send(msg.encode())
        data.mode = "chooseHouse"

# if another user joins the game        
def newUser(data, username, password):
    found = False
    file = readFile("storage.txt")
    f = file.splitlines()
    for line in f:
        line = line.split(" ")
        if (username == line[0]): found = True
    if (found == False):
        file += "%s %s %d\n" % (username, password, 0)
        writeFile("storage.txt", file)
    
# from 15112 website: https://www.cs.cmu.edu/~112/notes/notes-graphics.html        
def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)
    
def createStartButtons(data):
    color1 = rgbString(100,107,130)
    color2 = rgbString(217,218,221)
    color3 = rgbString(50,70,115)
    # username entry 
    w = 18 # number of characters of entry
    data.username = Entry(data.root, width=w, font="System 20 bold", 
                          bg=color1, fg=color2, bd=5, insertbackground=color2)
    # password entry
    data.password = Entry(data.root, width=w, font="System 20 bold", 
                          bg=color1, fg=color2, bd=5, insertbackground=color2, show="*")
    # number of player buttons 1-4
    n = 50 # button size
    data.oneButton = Button(data.root, width=n, height=n, image=data.oneButtonImage, 
                            command=lambda:numPlayerClick(data, 1), bg=color1, activebackground=color3)
    data.twoButton = Button(data.root, width=n, height=n, image=data.twoButtonImage, 
                            command=lambda:numPlayerClick(data, 2), bg=color1, activebackground=color3)
    data.threeButton = Button(data.root, width=n, height=n, image=data.threeButtonImage, 
                            command=lambda:numPlayerClick(data, 3), bg=color1, activebackground=color3)
    data.fourButton = Button(data.root, width=n, height=n, image=data.fourButtonImage, 
                            command=lambda:numPlayerClick(data, 4), bg=color1, activebackground=color3)
    # login button
    h = 70 # height of button
    data.loginButton = Button(data.root, width=2*h, height=h, image=data.loginButtonImage,
                            command=lambda:loginClick(data), bg=color1, activebackground=color3)

def startRedrawAll(canvas, data):
    x1, y1 = data.width/2, data.height/2 - data.height/9
    canvas.create_image(x1, y1, image=data.hogwartsCastleImage) # background image
    canvas.create_image(x1, data.height/4, image=data.titleImage)
    if (data.drawn == 0):  # buttons not drawn yet
        createStartButtons(data)
        data.drawn += 1
    # draw number of player buttons
    canvas.create_image(data.width/2 - 50 - data.numPlayersImage.width(), data.height/4 + data.height/7, image=data.numPlayersImage)
    canvas.create_window(data.width/2 - 100, data.height/4 + data.height/7, window=data.oneButton)
    canvas.create_window(data.width/2 - 33.5, data.height/4 + data.height/7, window=data.twoButton)
    canvas.create_window(data.width/2 + 33.5, data.height/4 + data.height/7, window=data.threeButton)
    canvas.create_window(data.width/2 + 100, data.height/4 + data.height/7, window=data.fourButton)
    # draw username box
    canvas.create_image(data.width/2 - data.userImage.width()*2.2, data.height/2, image=data.userImage)
    canvas.create_window(data.width/2, data.height/2, window=data.username)
    # draw password box
    canvas.create_image(data.width/2 - data.passwordImage.width()*2.2, data.height/2 + data.height/10, 
                        
                        image=data.passwordImage)
    canvas.create_window(data.width/2, data.height/2 + data.height/10, window=data.password) 
    # draw login button
    canvas.create_window(data.width/2, data.height*3/4, window=data.loginButton)
    
####################################
# choose house mode
####################################

def chooseHouse(data, buttonID):
    msg = ""
    if (buttonID=="Gryffindor"): data.me.house = "Gryffindor"
    elif (buttonID=="Hufflepuff"): data.me.house = "Hufflepuff"
    elif (buttonID=="Ravenclaw"): data.me.house = "Ravenclaw"
    elif (buttonID=="Slytherin"): data.me.house = "Slytherin"
    msg = "changeHouse %s\n" % data.me.house
    print("sending: ", msg,)
    data.server.send(msg.encode())
    data.drawn = 0
    data.dementor = data.dementorImage.subsample(2,2)
    data.mode = "instructions"
        
def houseRedrawAll(canvas, data):
    # background
    canvas.create_rectangle(0,0,data.width, data.height, fill="black")
    width = data.width/4
    if (data.drawn==0):
        # gryffindor button
        data.gryffindorButton = Button(canvas, width=width - 10, height=data.gryffindor.height()-20, 
                                image=data.gryffindor, bg="black", activebackground=rgbString(165,88,43),                               
                                command=lambda:chooseHouse(data, "Gryffindor"))
        # hufflepuff button
        data.hufflepuffButton = Button(canvas, width=width - 10, height=data.hufflepuff.height()-20, 
                                image=data.hufflepuff, bg="black", activebackground=rgbString(214,158,47), 
                                command=lambda:chooseHouse(data, "Hufflepuff"))
        # ravenclaw button
        data.ravenclawButton = Button(canvas, width=width - 10, height=data.ravenclaw.height()-20, 
                                image=data.ravenclaw, bg="black", activebackground=rgbString(42,89,130), 
                                command=lambda:chooseHouse(data, "Ravenclaw"))
        # slytherin button
        data.slytherinButton = Button(canvas, width=width - 10, height=data.slytherin.height()-20, 
                                image=data.slytherin, bg="black", activebackground=rgbString(61,109,72),
                                 command=lambda:chooseHouse(data, "Slytherin"))
        data.drawn += 1
    
    # draw buttons
    w = data.width/8 # position of first button
    canvas.create_window(data.width/8 + 5, data.gryffindor.height()/2, window=data.gryffindorButton)
    canvas.create_window(3*w + 3, data.hufflepuff.height()/2, window=data.hufflepuffButton)
    canvas.create_window(5*w , data.ravenclaw.height()/2, window=data.ravenclawButton)
    canvas.create_window(7*w - 2, data.slytherin.height()/2, window=data.slytherinButton)
    # instructions
    canvas.create_image(data.width/2, data.height-data.height/7, image=data.chooseHouseImage)

####################################
# instructions page mode
####################################

def back(data):
    data.drawn = 0
    data.mode = "chooseHouse"
    
def nextClick(data):
    msg = ""
    data.drawn = 0
    data.nextClicks += 1
    data.myClicks += 1
    msg = "nextClick %d\n" % 1
    if (msg != ""):
        print("sending: ", msg,)
        data.server.send(msg.encode())
    data.me.gameOver = False
    data.time = 0
    data.mode = "play"

def storeClicked(data):
    data.drawn = 0
    data.mode = "store"
    
def scoresMode(data):
    data.drawn = 0
    data.mode = "scores"
    
def createInstructionsButtons(data):
    color1, color2 = rgbString(135,110,29), rgbString(186,152,42)
    # back button
    w1, h1 = data.backImage.width() + 10, data.backImage.height() + 10
    data.backButton = Button(data.root, width=w1, height=h1, image=data.backImage, 
                            bg=color1, activebackground=color2, command=lambda:back(data))
    # next button
    w2, h2 = data.nextImage.width() + 10, data.nextImage.height()
    data.nextButton = Button(data.root, width=w2, height=h2, image=data.nextImage, 
                            bg=color1, activebackground=color2, command=lambda:nextClick(data))
    w3, h3 = data.storeImage.width() + 10, data.storeImage.height() + 10
    data.storeButton = Button(data.root, width=w3, height=h3, image=data.storeImage, 
                        bg=color2, activebackground=color2, command=lambda:storeClicked(data))
    w4, h4 = data.highScores.width() + 10, data.highScores.height() + 10
    data.scoresButton = Button(data.root, width=w4, height=h4, image=data.highScores, 
                        bg=color2, activebackground=color2, command=lambda:scoresMode(data))
    
# images that correspond with instructions    
def drawInstructionsImages(canvas, data):
    # monsters
    y = data.height*3/8
    left = data.width/9
    canvas.create_image(left + data.instructionsImage2.width()/2, y, 
                        image=data.instructionsImage2)
    # draw monster
    if (data.level == 1): monsterImage = data.muggleImage
    elif (data.level == 2): monsterImage = data.dementor
    elif (data.level == 3): monsterImage = data.red1
    canvas.create_image(data.width*3/4, y, image=monsterImage)
    # items
    canvas.create_image(left + data.instructionsImage3.width()/2, data.height/2, 
                        image=data.instructionsImage3)
    x = data.width*2/3
    canvas.create_image(x, data.height/2, image=data.goldCoins[data.coinIndex])
    canvas.create_image(x + data.silverCoinImage1.width()*2, data.height/2, 
                        image=data.silverCoins[data.coinIndex])
    canvas.create_image(x + data.bronzeCoinImage1.width()*4, data.height/2, 
                        image=data.bronzeCoins[data.coinIndex])
                        
def instructionsRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.parchmentImage)
    canvas.create_image(data.width/2, data.height/10, image=data.instructionsImage)
    # level in between back and next buttons
    if (data.level == 1): levelImage = data.level1Image
    elif (data.level == 2): levelImage = data.level2Image
    elif (data.level == 3): levelImage = data.level3Image
    canvas.create_image(data.width/2, data.height*7/8, image=levelImage)
    # instructions on top
    left = data.width/9
    canvas.create_image(left + data.instructionsImage1.width()/2, data.height/4, 
                        image=data.instructionsImage1)
    if (data.level != 1): 
        canvas.create_image(data.width*3/4, data.height/4, image=data.instructionPlatformImage)
    else: canvas.create_image(data.width*3/4, data.height/4, image=data.instructionTrolley)
    drawInstructionsImages(canvas, data) # objects in instructions page
    # gameplay instructions
    x1, y1 = left + data.instructionsImage4.width()/2, data.height*3/5
    canvas.create_image(x1, y1, image=data.instructionsImage4)
    x2, y2 = left + data.instructionsImage5.width()/2, y1 + data.instructionsImage5.height()*1.5
    canvas.create_image(x2, y2, image=data.instructionsImage5)
    # draw bullet 
    if (data.level == 1 or data.level == 3): 
        canvas.create_image(data.width*3/4, y2, image=data.spellImage)
    elif (data.level == 2):
        canvas.create_image(data.width*3/4, y2, image=data.patronuses[data.patronusIndex])
    if (data.drawn==0):
        createInstructionsButtons(data) # back and next buttons
        data.drawn += 1
    x3, y3 = data.width/8, data.height*7/8
    canvas.create_window(7*x3, y3, window=data.nextButton) # next button
    canvas.create_window(x3, y3, window=data.backButton) # back button
   # canvas.create_window(x3, data.height/10, window=data.scoresButton)
    canvas.create_window(7*x3, data.height/10, window=data.storeButton) # store button

####################################
# powerups store mode
####################################

def drawPage(canvas, data):
    h = data.height*4/5 - data.resurrectionStoneImage.height()
    canvas.create_image(data.width/4, h, image=data.resurrectionStoneImage)
    canvas.create_image(data.width/2, data.height*3/5, image=data.wandImage)
    canvas.create_image(data.width*3/4, data.height*3/5, image=data.invisibleImage)
    canvas.create_text(data.width*8/9, data.height/9, text="%d coins" % (data.me.coins), font="System 20 bold")
        
def backClick(data):
    data.drawn = 0
    data.mode = "instructions"
    
def buyButton(data, ID):
    if (data.me.coins >= 1000): 
        data.me.coins -= 1000
        if (ID == 1): data.me.wand = True
        elif (ID == 2): data.me.stone = True
        elif (ID == 3): data.me.cloak = True
    else:
        message = "Not enough coins! Play again!"
        messagebox.showerror("$$$", message)
        return
        
def createStoreButtons(data):
    color1, color2 = rgbString(135,110,29), rgbString(186,152,42)
    # left arrow
    w1, h1 = data.backImage.width() + 10, data.backImage.height() + 10
    data.left = Button(data.root, width=w1, height=h1, image=data.backImage, 
                    bg=color1, activebackground=color2, command=lambda:backClick(data))
    w3, h3 = data.thousandCoinsImage.width(), data.thousandCoinsImage.height()
    data.wandButton = Button(data.root, width=w3, height=h3, image=data.thousandCoinsImage, 
                    bg=color1, activebackground=color2, command=lambda:buyButton(data, 1))
    data.stoneButton = Button(data.root, width=w3, height=h3, image=data.thousandCoinsImage, 
                    bg=color1, activebackground=color2, command=lambda:buyButton(data, 2))
    data.cloakButton = Button(data.root, width=w3, height=h3, image=data.thousandCoinsImage, 
                    bg=color1, activebackground=color2, command=lambda:buyButton(data, 3))

def storeRedrawAll(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.parchmentImage)
    canvas.create_image(data.width/2, data.height/3, image=data.storeTitle)
    drawPage(canvas, data)
    if (data.drawn == 0):
        createStoreButtons(data) # back button, buy buttons
        data.drawn += 1
    x, y = data.width/9, data.height/9
    # back button
    canvas.create_window(x, y, window=data.left)
    # buy buttons
    h = data.height*4/5
    canvas.create_window(data.width/4, h, window=data.stoneButton)
    canvas.create_window(data.width/2, h, window=data.wandButton)
    canvas.create_window(data.width*3/4, h, window=data.cloakButton)
        
####################################
# play mode
####################################
 
def playKeyPressed(event, data):
    dx, dy = 0, 0
    msg = ""

    # moving
    if (event.keysym in ["Up", "Right"]):
        if (event.keysym == "Up"):
            dy = -data.jumpStep
        else:
            dx = data.scrollX
            # move myself
        data.me.move(dx, dy, data)
        # update message to send
        msg = "playerMoved %d %d\n" % (dx, dy)
    
    elif (event.keysym == "q"): init(data)
    elif (event.keysym == "z"): data.me.gameOver = True
    elif (event.keysym == "Return"): loginClick(data)
    elif (event.keysym in ["1", "2", "3"]): data.level = int(event.keysym)
    
    
    # shooting bullets
    elif (event.keysym=="space"):
        x = data.me.x + data.me.width//2 + data.me.totalScrollX
        y = data.me.y + data.me.totalScrollY
        if (data.level==1 or data.level==3):
            x += data.spellWidth//2
            Spell(int(x), y, data)
            msg = "newSpell %d %d\n" % (x, y)
        elif (data.level==2):
            x += data.patronusWidth//2
            Patronus(int(x), y, data)
            msg = "newPatronus %d %d\n" % (x, y) 
    if (msg != ""):
        print("sending: ", msg,)
        data.server.send(msg.encode())

# completes downwards part of jump unless character collides with a platform     
def recursiveFall(data, character):
    # end of jump
    if (data.time == character.jumpStart + 500): return
    result = checkPlatformCollision(data, character)
    # character collided with top of platform
    if (result == data.me.y): 
        character.jump, character.jumpCount = False, 0
        return
    else:
        character.move(0, data.jumpStep, data)
        # character is not colliding with any platforms
        if (result == -1): return
        # character is colliding with part of a platform (not the top)
        else:
            recursiveFall(data, character)
                
# checks if character jumps 
def checkJumps(data, character):
    # time required for one full jump
    jumpTime = 700
    # check my jumps
    if (character.jump == True): 
        character.jumps += 1
        # jumpStart = time when jump occurred
        # jumpCount = jump incomplete
        if (character.jumpStart < data.time and character.jumpCount == 0):
            character.jumpStart = data.time
            character.jumpCount += 1
        else:
            if (data.time == character.jumpStart + jumpTime): 
                character.jump, character.jumpCount = False, 0
            elif (character.jumpStart <= data.time < character.jumpStart + jumpTime//2):
                character.totalScrollY -= data.jumpStep
            elif (character.jumpStart + jumpTime//2 < data.time < character.jumpStart + jumpTime):
                # completes the character's fall unless the character 
                # reaches the top of a platform
                recursiveFall(data, character)

def continuousScrolling(data): # horizontal
    if (data.time % 50 == 0): # scrolls left
        for player in data.others:
            data.others[player].totalScrollX += data.scrollX//1.5
        data.me.totalScrollX += data.scrollX//1.5
            
def newPlatform(data):
    if (data.numPlayers > 1): 
        for i in data.others:
            player = data.others[i]
            if (data.me.totalScrollX < player.totalScrollX): return
    if (data.time % 1000 == 0):
        msg = ""
        x = data.width + data.me.totalScrollX + data.platformWidth//2
        ratio = int(data.height//data.jump)
        y = random.choice([int(i*data.jump) for i in range(1, ratio, 2)])
        y += data.me.totalScrollY
        x, y = int(x), int(y)
        Platforms(x, y, data) # new platform
        placeItem(x, y, data) # place item on platform
        newMonster(x, data) # new monster
        msg = "newPlatform %d %d\n" % (x, y)
        print("sending: ", msg,)
        data.server.send(msg.encode())
        newPlatformBelow(data, x, ratio) # makes new platforms below player 
        
def newPlatformBelow(data, x, ratio):
    msg = ""
    y = random.choice([int(i*data.jump) for i in range(1, ratio*3, 2)])
    y += data.me.totalScrollY
    x, y = int(x), int(y)
    Platforms(x, y, data) # new platform
    placeItem(x, y, data) # place item on platform
    msg = "newPlatform %d %d\n" % (x, y)
    print("sending: ", msg,)
    data.server.send(msg.encode())
    newPlatformOther(data, x)
    
# places platform in line with other players    
def newPlatformOther(data, x):
    x = int(x)
    for i in data.others:
        player = data.others[i]
        ratio = int(data.height//data.jump)
        y = random.choice([int(i*data.jump) for i in range(1, ratio, 2)])
        y += player.totalScrollY
        x, y = int(x), int(y)
        msg = "newPlatform %d %d\n" % (x, y)
        print("sending: ", msg,)
        data.server.send(msg.encode())
        Platforms(x, y, data) # new platform
        placeItem(x, y, data) # place item on platform
        newPlatformOtherBelow(data, x, player.totalScrollY, ratio)
    
def newPlatformOtherBelow(data, x, scrollY, ratio):
    msg = ""
    y = random.choice([int(i*data.jump) for i in range(1, ratio*3, 2)])
    y += scrollY
    x, y = int(x), int(y)
    msg = "newPlatform %d %d\n" % (x, y)
    print("sending: ", msg,)
    data.server.send(msg.encode())
    Platforms(x, y, data)
    placeItem(x, y, data)
                
def newMonster(x, data):
    msg = ""
    if (data.level==1): 
        monsterWidth, monsterHeight = data.muggleWidth, data.muggleHeight
    elif (data.level==2): 
        monsterWidth, monsterHeight = data.dementorWidth, data.dementorHeight
    elif (data.level==3): 
        monsterWidth, monsterHeight = data.dragonWidth, data.dragonHeight
    x = int(x)
    y = random.randint(1, data.height) + data.me.totalScrollY
    dragonType = random.choice(data.dragonTypes)
    if (data.level==1):
        Muggle(x, y, data)
        msg = "newMuggle %d %d\n" % (x, y)
    elif (data.level==2):
        Dementor(x, y, data)
        msg = "newDementor %d %d\n" % (x, y)
    elif (data.level==3):
        Dragon(x, y, dragonType, data)
        msg = "newDragon %d %d %s\n" % (x, y, dragonType)
    if (msg != ""):
        print("sending: ", msg,)
        data.server.send(msg.encode())
            
# places item on platform
def placeItem(x, y, data):
    msg = "" 
    cx, cy = x, y - data.platformHeight//2
    itemProbability = random.randint(1,100)
    #if (itemProbability <= 1): # 1% chance
    if (data.time == 20):
        if (data.level == 2):
            Snitch(cx, cy - data.snitchHeight//2, data)
            msg = "newSnitch %d %d\n" % (cx, cy - data.snitchHeight//2)
        elif (data.level == 3):
            Egg(cx, cy - data.eggHeight//2, data)
            msg = "newEgg %d %d\n" % (cx, cy - data.eggHeight//2)
    elif (itemProbability <= 21): # 20% chance
        cy -= data.coinHeight//2
        GoldCoin(cx, cy, data)
        msg = "newGoldCoin %d %d\n" % (cx, cy)
    elif (itemProbability <= 51): # 30% chance
        cy -= data.coinHeight//2
        SilverCoin(cx, cy, data)
        msg = "newSilverCoin %d %d\n" % (cx, cy)
    elif (itemProbability <= 100): # 49% chance
        cy -= data.coinHeight//2
        BronzeCoin(cx, cy, data)
        msg = "newBronzeCoin %d %d\n" % (cx, cy)
    if (msg != ""):
        print("sending: ", msg,)
        data.server.send(msg.encode())
        
#returns True if character collides with platform                        
def checkPlatformCollision(data, character):
    for platform in data.platforms:
        # check me
        cx, cy = platform.x - character.totalScrollX, platform.y - character.totalScrollY
        # platform in character's screen
        if ((-platform.width/2 <= cx <= data.width + platform.width/2)
            and (-platform.height/2 <= cy <= data.height + platform.height/2)):
            top, bottom = cy - data.platformHeight/2, cy + data.platformHeight/2
            left, right = cx - data.platformWidth/2, cx + data.platformWidth/2
            yMin, yMax = top - character.height/2, bottom - character.height/2
            if (data.level == 2 or data.level == 3):
                yMin = top - character.height/4
            if ((left - character.width/2 <= character.x <= right + character.width/2) 
                and (yMin <= character.y <= yMax)):
                # top of platform that character collided with
                return yMin
    return -1 

# moves character down if character collides with platform          
def checkPlatformCollisions(data, character):
    if character.jump: return # allow jumps to happen
    # scroll down if character doesn't collide with a platform
    result = checkPlatformCollision(data, character)
    # character collided with top of platform
    dy = data.scrollY
    if (result == -1): character.move(0, dy, data)
    elif (result == data.me.y): return
    else: character.move(0, int(result - character.y), data)
            
def moveBullets(data): # right
    for bullet in data.bullets:
        if (data.level == 2):
            bullet.x += data.scrollX/1.1
        else: bullet.x += data.scrollX*1.5
    checkBulletsCollided(data)
    
def moveMonsters(data): # left
    for monster in data.monsters:
        monster.x -= data.scrollX/2
        
def checkBulletsCollided(data):
    collidedBullets, collidedMonsters = set(), set()
    for bullet in data.bullets:
        for monster in data.monsters:
            # monster boundaries
            left, right = monster.x - monster.width/2, monster.x + monster.width/2
            top, bottom = monster.y - monster.height/2, monster.y + monster.height/2
            # bullet collided with monster
            if (left < bullet.x < right) and (top < bullet.y < bottom):
                collidedMonsters.add(monster)
                collidedBullets.add(bullet)
    # remove items and monsters that collided
    for bullet in collidedBullets:
        data.bullets.remove(bullet)
    for monster in collidedMonsters:
        data.monsters.remove(monster)
        
# checks if player collides with monster and removes part of player's life        
def checkMonsterCollisions(data, character):
    for monster in data.monsters:
        msg = ""
        if (monster not in data.monsterCollisions):
            # monster boundaries
            left, right = monster.x - monster.width/2, monster.x + monster.width/2
            top, bottom = monster.y - monster.height/2, monster.y + monster.height/2
            # player collided with monster
            if ((left - character.totalScrollX < character.x + character.width/2 < right - character.totalScrollX) 
                and (top - character.totalScrollY < character.y < bottom - character.totalScrollY)):
                data.monsterCollisions.add(monster)
                character.life -= 20 # removes 20% of player's life

def checkItemCollisions(data, character):
    itemsCollided = set()
    for item in data.items:
        cx, cy = item.x - character.totalScrollX, item.y - character.totalScrollY
        if ((abs(character.x - cx) <= (character.width/2 + item.width/4)) #collided
            and (abs(character.y - cy) <= (character.height/2 + item.height/4))):
            character.score += item.score #add points
            itemsCollided.add(item) #add item to be removed
    if (itemsCollided != set()):
        for item in itemsCollided: data.items.remove(item)
    
def updateImageMovements(data):
    # spin coins
    for item in data.items:
        if isinstance(item, GoldCoin):
            item.coinIndex = (item.coinIndex + 1) % len(data.goldCoins)
        elif isinstance(item, SilverCoin):
            item.coinIndex = (item.coinIndex + 1) % len(data.silverCoins)
        elif isinstance(item, BronzeCoin):
            item.coinIndex = (item.coinIndex + 1) % len(data.bronzeCoins)
    # animate patronuses
    if (data.time % 100 == 0): 
        data.patronusIndex = (data.patronusIndex + 1) % len(data.patronuses)
    if (data.time % 100 == 0):
        # animate player for level 1
        if (data.level == 1):
            data.me.index = (data.me.index + 1) % 4
            for i in data.others:
                player = data.others[i]
                player.index = (player.index + 1) % 4
    # move dragons in level 3
    if (data.level == 3):
        for dragon in data.monsters:
            dragon.index = (dragon.index + 1) % 9

# starting platforms on screen)    
def starting(data):
    x = data.me.x
    y = data.me.y + data.characterHeight/4 + data.platformHeight/2
    Platforms(x, y, data)
    Platforms(x + data.platformWidth, y + data.platformHeight/2, data)
    Platforms(x + 2* data.platformWidth, y + data.platformHeight, data)
    Platforms(x + 2*data.platformWidth, y + data.platformHeight*1.5, data)
    
def checkScores(data):
    scores = set()
    scores.add(data.me.score)
    for i in data.others:
        player = data.others[i]
        scores.add(player.score)
    if (data.numPlayers > 1) and (data.time == data.timeLimit):
        if (max(scores) == data.me.score): data.me.win = True
        else: return
    if (data.numPlayers == 1) and (data.time == data.timeLimit):
        data.me.win = True

# animates instruction images    
def animateInstructions(data):
    # spin coins
    data.coinIndex = (data.coinIndex + 1) % len(data.goldCoins)
    if (data.level == 2):
        if (data.temp % 100):
            # animate patronus
            data.patronusIndex = (data.patronusIndex + 1) % len(data.patronuses)
            
def saveScores(data):
    new = ""
    file = readFile("storage.txt")
    f = file.splitlines()
    for line in f:
        line = line.split(" ") # convert to a list
        if (data.usernameEntry == line[0]): # username in file
            score = int(line[2])
            data.me.coins = score + data.me.score
            line = line[:-1]
            line += [str(data.me.coins)]
        for i in data.others:
            player = data.others[i]
            if (i == line[0]): # other player's username in file
                score = int(line[2])
                player.coins = score + player.score
                line = line[:-1]
                line += [str(player.coins)]
        line = " ".join(line)
        line += "\n"
        new += line
    writeFile("storage.txt", new)
                     
def gameOver(data):
    checkScores(data)
    saveScores(data)
    data.me.life = 100
    data.drawn = 0
    data.me.time = 0
    data.start = False
    data.mode = "gameOver"
    return
    
def syncPositions(data):
    if (data.me.totalScrollX != data.maxTotalScrollX): return
    msg = ""
    if (data.time % 100):
        msg = "updatePosition %d %d\n" % (data.me.totalScrollX, data.me.totalScrollY)
    if (msg != ""):
        print("sending: ", msg, )
        data.server.send(msg.encode())
        
def syncTime(data):
    msg = "time %d\n" % (data.time)
    print("sending: ", msg, )
    data.server.send(msg.encode())
        
def syncPoints(data):
    for i in data.others:
        msg = ""
        player = data.others[i]
        msg = "points %d %d" % (data.me.score, player.score)
        print("sending: ", msg)
        data.server.send(msg.encode())
        
# generates game state and checks game state    
def play(data):
    data.minTotalScrollX, data.minTotalScrollY = findLastPlayer(data)
    data.maxTotalScrollX, data.maxTotalScrollY = findFirstPlayer(data)
    data.time += data.timerDelay
    for i in data.others:
        player = data.others[i]
        checkJumps(data, player)
        checkPlatformCollisions(data, player)
        checkMonsterCollisions(data, player)
        checkItemCollisions(data, player)
        if (player.life <= 0):
            data.me.win = True
            data.me.gameOver = True
            return
    newPlatform(data)
    continuousScrolling(data)
    checkJumps(data, data.me) # check my jumps
    checkPlatformCollisions(data, data.me) # check platform collisions with me
    checkMonsterCollisions(data, data.me)
    checkItemCollisions(data, data.me)
    if (len(data.bullets) != 0): moveBullets(data)
    if (len(data.monsters) != 0): moveMonsters(data)
    updateImageMovements(data)
    if (data.me.life <= 0): data.me.gameOver = True
    
def playTimerFired(data): 
    if (data.mode == "play"):
        if (data.time == data.timeLimit): data.me.gameOver = True
        if data.me.gameOver: gameOver(data)
    data.temp += data.timerDelay
    if (data.myClicks == 1 and data.numPlayers > 1):
        if (data.temp % 225): data.waitingIndex = (data.waitingIndex + 1) % 3
    if (data.nextClicks == data.numPlayers) and (data.mode == "play"): 
        data.myClicks = 0
        starting(data) # starting platforms on screen
        data.start = True
    if (data.start == True): play(data)
    if (data.mode == "instructions"): animateInstructions(data)           
    # timerFired receives instructions and executes them
    while (serverMsg.qsize() > 0):
        msg = serverMsg.get(False)
        try:
            print("received: ", msg, "\n")
            msg = msg.split()
            command = msg[0]

            if (command == "myIDis"):
                myPID = msg[1]
                data.me.changePID(myPID)
            
            elif (command == "points"):
                PID = msg[1]
                otherScore = int(msg[2])
                myScore = int(msg[3])
                for i in data.others:
                    data.others[PID].score = otherScore
                data.me.score = myScore
                
            elif (command == "updatePosition"):
                PID = msg[1]
                scrollX, scrollY = int(msg[2]), int(msg[3])
                data.others[PID].totalScrollX = scrollX
                data.other[PID].totalScrollY = scrollY
                
            elif (command == "time"):
                time = int(msg[2])
                data.otherTime = time
            
            elif (command == "nextClick"):
                num = int(msg[2])
                data.nextClicks += num
                
            elif (command == "startGame"):
                data.play = True
                
            elif (command == "nameChanged"):
                PID = msg[1]
                name = msg[2]
                data.others[PID].changePID(name)
            
            elif (command == "newPlayer"):
                newPID = msg[1]
                data.others[newPID] = FlyingCharacter(newPID, data)
            
            elif (command == "newUser"):
                username, password = msg[2], msg[3]
                newUser(data, username, password)
                
            elif (command == "changeHouse"):
                PID = msg[1]
                house = msg[2]
                data.others[PID].house = house
                
            elif (command == "playerMoved"):
                PID = msg[1]
                dx = int(msg[2])
                dy = int(msg[3])
                data.others[PID].move(dx, dy, data)
                
            elif (command == "newPlatform"):
                x, y = int(msg[2]), int(msg[3])
                Platforms(x, y, data)
                
            elif (command == "newGoldCoin"):
                x, y = int(msg[2]), int(msg[3])
                GoldCoin(x, y, data)
                
            elif (command == "newSilverCoin"):
                x, y = int(msg[2]), int(msg[3])
                SilverCoin(x, y, data)
            
            elif (command == "newBronzeCoin"):
                x, y = int(msg[2]), int(msg[3])
                BronzeCoin(x, y, data)
            
            elif (command == "newResurrectionStone"):
                x, y = int(msg[2]), int(msg[3])
                ResurrectionStone(x, y, data)
            
            elif (command == "newSnitch"):
                x, y = int(msg[2]), int(msg[3])
                Snitch(x, y, data)
                
            elif (command == "newEgg"):
                x, y = int(msg[2]), int(msg[3])
                Egg(x, y, data)
                
            elif (command == "newMuggle"):
               x, y = int(msg[2]), int(msg[3])
               Muggle(x, y, data)
               data.monsterCollisions += [False]
            
            elif (command == "newDementor"):
                x, y = int(msg[2]), int(msg[3])
                Dementor(x, y, data)
                data.monsterCollisions += [False]
                
            elif (command == "newDragon"):
                x, y = int(msg[2]), int(msg[3])
                dragonType = msg[4]
                Dragon(x, y, dragonType, data)
                data.monsterCollisions += [False]
                
            elif (command == "newSpell"):
                x, y = int(msg[2]), int(msg[3])
                Spell(x, y, data)
                
            elif (command == "newPatronus"):
                x, y = int(msg[2]), int(msg[3])
                Patronus(x, y, data)
        except:
            print("failed")
        serverMsg.task_done()
        
# finds first player's totalScrollX & totalScrollY
def findFirstPlayer(data):
    maxX, maxY = [data.me.totalScrollX], [data.me.totalScrollY]
    for i in data.others:
        player = data.others[i]
        x, y = player.totalScrollX, player.totalScrollY
        maxX += [x]
        maxY += [y]
    return (max(maxX), max(maxY))
    
# finds last player's totalScrollX & totalScrollY for object keeping purposes between all players       
def findLastPlayer(data):
    minX, minY = [data.me.totalScrollX], [data.me.totalScrollY]
    for i in data.others:
        player = data.others[i]
        x, y = player.totalScrollX, player.totalScrollY
        minX += [x]
        minY += [y]
    return (min(minX), min(minY))
    
def drawPlatforms(canvas, data):
    # updated = all platforms between players
    # drawn = platforms in the current player's screen
    updatedPlatforms, drawnPlatforms = set(), set()
    for platform in data.platforms:
        x, y = platform.x - data.minTotalScrollX, platform.y - data.minTotalScrollY
        if (-platform.width/2 <= x): updatedPlatforms.add(platform)
        x, y = platform.x - data.me.totalScrollX, platform.y - data.me.totalScrollY
        if ((-platform.width/2 <= x <= data.width + platform.width/2)
            and (-platform.height/2 <= y <= data.height + platform.height/2)):
            drawnPlatforms.add(platform)
    # temporarily set all platforms to only seen platforms in player's screen
    data.platforms = drawnPlatforms 
    # draw all platforms in screen
    Platforms.draw(canvas, data)
    # reset platforms to all platforms between players
    data.platforms = updatedPlatforms
    
def drawItems(canvas, data):
    # updated = all items between players
    # drawn = items in the current player's screen
    updatedItems, drawnItems = set(), set()
    for item in data.items:
        x, y = item.x - data.minTotalScrollX, item.y - data.minTotalScrollY
        if (-item.width/2 <= x): updatedItems.add(item)
        x, y = item.x - data.me.totalScrollX, item.y - data.me.totalScrollY
        if ((-item.width/2 <= x <= data.width + item.width/2)
            and (-item.height/2 <= y <= data.height + item.height/2)):
            drawnItems.add(item)
    # temporarily set all items to only seen items in player's screen
    data.items = drawnItems 
    # draw all items in screen
    GoldCoin.draw(canvas, data)
    SilverCoin.draw(canvas, data)
    BronzeCoin.draw(canvas, data)
    ResurrectionStone.draw(canvas, data)
    if (data.level == 2): Snitch.draw(canvas, data)
    elif (data.level == 3): Egg.draw(canvas, data)
    # reset items to all items between players
    data.items = updatedItems

def drawMonsters(canvas, data):
    # updated = all monsters between players
    # drawn = monsters in the current player's screen
    updatedMonsters, drawnMonsters = set(), set()
    for monster in data.monsters:
        x, y = monster.x - data.minTotalScrollX, monster.y - data.minTotalScrollY
        if (-monster.width/2 <= x): updatedMonsters.add(monster)
        x, y = monster.x - data.me.totalScrollX, monster.y - data.me.totalScrollY
        if ((-monster.width/2 <= x <= data.width + monster.width/2)
            and (-monster.height/2 <= y <= data.height + monster.height/2)):
            drawnMonsters.add(monster)
    # temporarily set all monsters to only seen monsters in player's screen
    data.monsters = drawnMonsters
    # draw all monsters in screen
    if (data.level == 1): Muggle.draw(canvas, data)
    elif (data.level == 2): Dementor.draw(canvas, data)
    elif (data.level == 3): Dragon.draw(canvas, data)
    # reset monsters to all monsters between players
    data.monsters = updatedMonsters  
    
def drawBullets(canvas, data):
    # updated = all bullets between players
    # drawn = bullets in the current player's screen
    updatedBullets, drawnBullets = set(), set()
    for bullet in data.bullets:
        x, y = bullet.x - data.minTotalScrollX, bullet.y - data.minTotalScrollY
        if (-bullet.width/2 <= x): updatedBullets.add(bullet)
        x, y = bullet.x - data.me.totalScrollX, bullet.y - data.me.totalScrollY
        if ((-bullet.width/2 <= x <= data.width + bullet.width/2)
            and (-bullet.height/2 <= y <= data.height + bullet.height/2)):
            drawnBullets.add(bullet)
    # temporarily set all bullets to only seen bullets in player's screen
    data.bullets = drawnBullets 
    # draw all bullets in screen
    if (data.level==1 or data.level==3): Spell.draw(canvas, data)
    if (data.level==2): Patronus.draw(canvas, data)
    # reset bullets to all bullets between players
    data.bullets = updatedBullets 

# waiting for the right number of players to join    
def drawWaitingScreen(canvas, data):
    canvas.create_image(data.width/2, data.height/2, image=data.parchmentImage)
    canvas.create_image(data.width/2, data.height/2, image=data.waitingImages[data.waitingIndex])
   
def playRedrawAll(canvas, data):
    if (data.level == 1): canvas.create_image(data.width/2, data.height/2, image=data.brickImage)
    else: canvas.create_rectangle(0, 0, data.width, data.height, fill="light sky blue", outline="light sky blue")
    drawPlatforms(canvas, data)
    drawItems(canvas, data)
    # draw other players from perspective of me
    for player in data.others:
        x = data.me.totalScrollX - data.others[player].totalScrollX
        y = data.me.totalScrollY - data.others[player].totalScrollY
        data.others[player].draw(canvas, x, y, data)
    # draw me
    data.me.draw(canvas, 0, 0, data)
    # draw monsters
    drawMonsters(canvas, data)
    # draw bullets
    drawBullets(canvas, data)
    if (data.myClicks == 1 and data.numPlayers > 1): 
        drawWaitingScreen(canvas, data)
    
####################################
# game over mode
####################################

def resetGame(data):
    data.nextClicks = 0
    data.myClicks = 0
    data.me.score = 0
    data.time = 0
    data.monsterCollisions = set()
    data.me.jumpStart = 0
    data.me.jump = False
    data.me.totalScrollX, data.me.totalScrollY = 0, 0
    for i in data.others:
        player = data.others[i]
        player.totalScrollX, player.totalScrollY = 0, 0
        player.life = 100
        player.score = 0
        player.jumpStart = 0
        player.jump = False
        player.gameOver = False
        player.win = False
    data.me.gameOver = False
    data.me.win = False
    data.items = set()
    data.bullets = set()
    data.monsters = set()
    data.platforms = set()
    data.minTotalScrollX, data.minTotalScrollY = 0, 0
    data.maxTotalScrollX, data.maxTotalScrollY = 0, 0
    
def nextButton2Click(data):
    resetGame(data)
    if (data.level != 3): data.level += 1
    else: print("The End!")
    data.mode = "instructions"
    
def gameOverRedrawAll(canvas, data):
    x1, y1 = data.width/2, data.height/2
    # background
    canvas.create_image(x1, y1, image=data.parchmentImage)
    # win/lose
    if (data.me.win): canvas.create_image(x1, y1, image=data.winImage)
    else: canvas.create_image(x1, y1, image=data.loseImage)
    y2 = data.height/6
    # level number as title
    if (data.level == 1): canvas.create_image(x1, y2, image=data.level1Image)
    elif (data.level == 2): canvas.create_image(x1, y2, image=data.level2Image)
    elif (data.level == 3): canvas.create_image(x1, y2, image=data.level3Image)
    color1, color2 = rgbString(135,110,29), rgbString(186,152,42)
    # next button to go to instructions page
    if (data.drawn == 0): # button not drawn yet
        w1, h1 = data.nextImage.width(), data.nextImage.height()
        data.nextButton2 = Button(canvas, width=w1, height=h1, image=data.nextImage, 
                        command=lambda:nextButton2Click(data), bg=color1, activebackground=color2)
        data.drawn += 1
    x3, y3 = data.width/8, data.height*7/8
    if (data.level != 3): canvas.create_window(7*x3, y3, window=data.nextButton2) # draw button
    
    
####################################
# use the run function as-is
####################################

def run(width, height, serverMsg=None, server=None):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.server = server
    data.serverMsg = serverMsg
    data.width = width
    data.height = height
    data.timerDelay = 50 # milliseconds
    # create the root and the canvas
    root = Tk()
    data.root = root # for buttons
    init(data) # put the root first to load images in init
    canvas = Canvas(data.root, width=data.width, height=data.height)
    canvas.pack()
    data.canvas = canvas # for buttons
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

serverMsg = Queue(100)
threading.Thread(target = handleServerMsg, args = (server, serverMsg)).start()

# ideally 1000, 600 for one screen, 750, 550 for two # 760 590
run(760,590, serverMsg, server)