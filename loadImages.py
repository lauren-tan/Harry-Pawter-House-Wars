# load images

from tkinter import *

def loadImages(data):
    loadPusheenImages(data)
    loadDragonImages(data)
    loadFontImages(data) 
    loadCoinImages(data)
    # Hogwarts Castle background from https://nokeek.deviantart.com/art/Welcome-to-Hogwarts-479802474
    data.hogwartsCastleImage = PhotoImage(file="Images/hogwarts.png")
    # brick background from https://www.maxpixel.net/Wall-Background-Clinker-Facade-Home-Red-Brick-1694360
    data.brickImage = PhotoImage(file="Images/brick.png")
    # for choosing your house screen
    loadHouseImages(data)
    # from https://www.pinterest.com/pin/391391023838972249/
    data.spellImage = PhotoImage(file="Images/spell.png").subsample(2,2)
    # dementor from pixel art 
    data.dementorImage = PhotoImage(file="Images/dementor.png")
    # egg from http://pixelartmaker.com/art/7929a237527a744
    data.eggImage = PhotoImage(file="Images/egg.png").subsample(2,2)
    # All other images drawn by me using pixelart.com
    data.platformImage = PhotoImage(file="Images/cloud.png").subsample(2,2)
    if (data.width < 800): 
        data.instructionPlatformImage = data.platformImage.subsample(2,2)
    else: data.instructionPlatformImage = data.platformImage
    data.snitchImage1 = PhotoImage(file="Images/snitch.png").subsample(2,2) # snitch with wings up
    data.snitchImage2 = PhotoImage(file="images/snitch2.png").subsample(2,2) # snitch with wings down
    data.snitches = [data.snitchImage1, data.snitchImage2]
    data.resurrectionStoneImage = PhotoImage(file="Images/resurrectionStone.png")
    data.wandImage = PhotoImage(file="Images/wand.png")
    data.invisibleImage = PhotoImage(file="Images/invisible.png").subsample(2,2)
    data.trolley = PhotoImage(file="Images/trolley.png").subsample(2,2)
    data.instructionTrolley = data.trolley.subsample(2,2)

def loadPusheenImages(data):
    # Pusheen on a broomstick image from Pusheen.tumblr
    data.broomstickImage = PhotoImage(file="Images/pusheenBroomstick.png")
    data.ravenclawBroomstickImage = PhotoImage(file="Images/ravenclawBroomstick.png").subsample(2,2)
    data.hufflepuffBroomstickImage = PhotoImage(file="Images/hufflepuffBroomstick.png").subsample(2,2)
    data.slytherinBroomstickImage = PhotoImage(file="Images/slytherinBroomstick.png").subsample(2,2)
    # regular pusheen from https://store.line.me/stickershop/product/1014241/en
    data.muggleImage = PhotoImage(file="Images/pusheen.png").subsample(2,2)
    # walking pusheen from from http://www.fanpop.com/clubs/pusheen-the-cat/images/26391938/title/pusheen-costume-ideas-photo
    data.pusheen1 = PhotoImage(file="Images/pusheen1.png").subsample(2,2) #gryffindor
    data.pusheen2 = PhotoImage(file="Images/pusheen2.png").subsample(2,2)
    data.pusheen3 = PhotoImage(file="Images/pusheen3.png").subsample(2,2)
    data.pusheens = [data.pusheen1, data.pusheen2, data.pusheen3, data.pusheen2]
    # Ravenclaw pusheen edited from walking pusheen
    data.ravenclaw1 = PhotoImage(file="Images/ravenclaw1.png").subsample(2,2)
    data.ravenclaw2 = PhotoImage(file="Images/ravenclaw2.png").subsample(2,2)
    data.ravenclaw3 = PhotoImage(file="Images/ravenclaw3.png").subsample(2,2)
    data.ravenclaws = [data.ravenclaw1, data.ravenclaw2, data.ravenclaw3, data.ravenclaw2]
    # Hufflepuff pusheen edited from walking pusheen
    data.hufflepuff1 = PhotoImage(file="Images/hufflepuff1.png").subsample(2,2)
    data.hufflepuff2 = PhotoImage(file="Images/hufflepuff2.png").subsample(2,2)
    data.hufflepuff3 = PhotoImage(file="Images/hufflepuff3.png").subsample(2,2)
    data.hufflepuffs = [data.hufflepuff1, data.hufflepuff2, data.hufflepuff3, data.hufflepuff2]
    # Slytherin pusheen edited from walking pusheen
    data.slytherin1 = PhotoImage(file="Images/slytherin1.png").subsample(2,2)
    data.slytherin2 = PhotoImage(file="Images/slytherin2.png").subsample(2,2)
    data.slytherin3 = PhotoImage(file="Images/slytherin3.png").subsample(2,2)
    data.slytherins = [data.slytherin1, data.slytherin2, data.slytherin3, data.slytherin2]
    # Patronus pusheen edited from walking pusheen
    data.patronusImage1 = PhotoImage(file="Images/patronus1.png").subsample(2,2)
    data.patronusImage2 = PhotoImage(file="Images/patronus2.png").subsample(2,2)
    data.patronusImage3 = PhotoImage(file="Images/patronus3.png").subsample(2,2)
    data.patronusImage4 = PhotoImage(file="Images/patronus4.png").subsample(2,2)
    data.patronuses = [data.patronusImage1, data.patronusImage2, data.patronusImage3, data.patronusImage4]
    data.patronusIndex = 0

# from http://www.chickensmoothie.com/Forum/viewtopic.php?f=25&t=2902031    
def loadDragonImages(data):
    data.red1 = PhotoImage(file="Images/redDragon1.png").subsample(2,2)
    data.red2 = PhotoImage(file="Images/redDragon2.png").subsample(2,2)
    data.red3 = PhotoImage(file="Images/redDragon3.png").subsample(2,2)  
    data.red4 = PhotoImage(file="Images/redDragon4.png").subsample(2,2)
    data.red5 = PhotoImage(file="Images/redDragon5.png").subsample(2,2)        
    data.red6 = PhotoImage(file="Images/redDragon6.png").subsample(2,2)
    data.red7 = PhotoImage(file="Images/redDragon7.png").subsample(2,2)
    data.red8 = PhotoImage(file="Images/redDragon8.png").subsample(2,2)
    data.red9 = PhotoImage(file="Images/redDragon9.png").subsample(2,2)
    data.redDragons = [data.red1, data.red2, data.red3, data.red4, 
                       data.red5, data.red6, data.red7, data.red8, data.red9]
    data.blue1 = PhotoImage(file="Images/blueDragon1.png").subsample(2,2)
    data.blue2 = PhotoImage(file="Images/blueDragon2.png").subsample(2,2)
    data.blue3 = PhotoImage(file="Images/blueDragon3.png").subsample(2,2)  
    data.blue4 = PhotoImage(file="Images/blueDragon4.png").subsample(2,2)
    data.blue5 = PhotoImage(file="Images/blueDragon5.png").subsample(2,2)     
    data.blue6 = PhotoImage(file="Images/blueDragon6.png").subsample(2,2)
    data.blue7 = PhotoImage(file="Images/blueDragon7.png").subsample(2,2)
    data.blue8 = PhotoImage(file="Images/blueDragon8.png").subsample(2,2)
    data.blue9 = PhotoImage(file="Images/blueDragon9.png").subsample(2,2)
    data.blueDragons = [data.blue1, data.blue2, data.blue3, data.blue4, 
                       data.blue5, data.blue6, data.blue7, data.blue8, data.blue9]
    data.green1 = PhotoImage(file="Images/greenDragon1.png").subsample(2,2)
    data.green2 = PhotoImage(file="Images/greenDragon2.png").subsample(2,2)
    data.green3 = PhotoImage(file="Images/greenDragon3.png").subsample(2,2)  
    data.green4 = PhotoImage(file="Images/greenDragon4.png").subsample(2,2)
    data.green5 = PhotoImage(file="Images/greenDragon5.png").subsample(2,2)        
    data.green6 = PhotoImage(file="Images/greenDragon6.png").subsample(2,2)
    data.green7 = PhotoImage(file="Images/greenDragon7.png").subsample(2,2)
    data.green8 = PhotoImage(file="Images/greenDragon8.png").subsample(2,2)
    data.green9 = PhotoImage(file="Images/greenDragon9.png").subsample(2,2)
    data.greenDragons = [data.green1, data.green2, data.green3, data.green4, 
                       data.green5, data.green6, data.green7, data.green8, data.green9]
    data.dragonTypes = ["red", "blue", "green"]
    
# from https://fontmeme.com/harry-potter-font/    
def loadFontImages(data):
    data.titleImage = PhotoImage(file="Images/title.png")
    data.chooseHouseImage = PhotoImage(file="Images/chooseHouse.png")
    data.gameOverImage = PhotoImage(file="Images/gameOverFont.png")
    data.expectoPatronumImage = PhotoImage(file="Images/expectoPatronum.png")
    data.backImage = PhotoImage(file="Images/back.png")
    data.nextImage = PhotoImage(file="Images/next.png")
    data.instructionsImage = PhotoImage(file="Images/instructions.png")
    data.instructionsImage1 = PhotoImage(file="Images/instructions1.png")
    data.instructionsImage2 = PhotoImage(file="Images/instructions2.png")
    data.instructionsImage3 = PhotoImage(file="Images/instructions3.png")
    data.instructionsImage4 = PhotoImage(file="Images/instructions4.png")
    data.instructionsImage5 = PhotoImage(file="Images/instructions5.png")
    data.instructionsImage6 = PhotoImage(file="Images/instructions2.png")
    data.loginImage = PhotoImage(file="Images/login.png")
    data.userImage = PhotoImage(file="Images/user.png")
    data.passwordImage = PhotoImage(file="Images/password.png")
    data.numPlayersImage = PhotoImage(file="Images/numPlayers.png")
    data.loginButtonImage = PhotoImage(file="Images/loginButtonImage.png")
    data.oneButtonImage = PhotoImage(file="Images/oneButton.png")
    data.twoButtonImage = PhotoImage(file="Images/twoButton.png")
    data.threeButtonImage = PhotoImage(file="Images/threeButton.png")
    data.fourButtonImage = PhotoImage(file="Images/fourButton.png")
    data.level1Image = PhotoImage(file="Images/level1.png")
    data.level2Image = PhotoImage(file="Images/level2.png")
    data.level3Image = PhotoImage(file="Images/level3.png")
    data.winImage = PhotoImage(file="Images/win.png")
    data.loseImage = PhotoImage(file="Images/lost.png")
    data.oneImage = PhotoImage(file="Images/oneImage.png")
    data.twoImage = PhotoImage(file="Images/twoImage.png")
    data.threeImage = PhotoImage(file="Images/threeImage.png")
    data.gryffindorLettersImage = PhotoImage(file="Images/gryffindorLetters.png")
    data.hufflepuffLettersImage = PhotoImage(file="Images/hufflepuffLetters.png")
    data.ravenclawLettersImage = PhotoImage(file="Images/ravenclawLetters.png")
    data.slytherinLettersImage = PhotoImage(file="Images/slytherinLetters.png")
    data.waitingImage1 = PhotoImage(file="Images/waiting1.png")
    data.waitingImage2 = PhotoImage(file="Images/waiting2.png")
    data.waitingImage3 = PhotoImage(file="Images/waiting3.png")
    data.waitingImages = [data.waitingImage1, data.waitingImage2, data.waitingImage3]
    data.waitingIndex = 0
    data.timeImage = PhotoImage(file="Images/time.png")
    data.thousandCoinsImage = PhotoImage(file="Images/1000coins.png")
    data.storeImage = PhotoImage(file="Images/store.png")
    data.storeTitle = PhotoImage(file="Images/deathlyHallows.png")
    data.leaderboard = PhotoImage(file="Images/leaderboard.png")
    data.highScores = PhotoImage(file="Images/highScores.png")
    
# from http://pixelart.studio/Gallery/Details/6b180138-1c14-4b18-9973-6e796c5a25b8    
def loadCoinImages(data):
    data.coinIndex = 0
    # gold coins
    data.goldCoinImage1 = PhotoImage(file="Images/goldCoin1.png").subsample(2,2)
    data.goldCoinImage2 = PhotoImage(file="Images/goldCoin2.png").subsample(2,2)
    data.goldCoinImage3 = PhotoImage(file="Images/goldCoin3.png").subsample(2,2)
    data.goldCoinImage4 = PhotoImage(file="Images/goldCoin4.png").subsample(2,2)
    data.goldCoinImage5 = PhotoImage(file="Images/goldCoin5.png").subsample(2,2)
    data.goldCoinImage6 = PhotoImage(file="Images/goldCoin6.png").subsample(2,2)    
    data.goldCoinImage7 = PhotoImage(file="Images/goldCoin7.png").subsample(2,2)   
    data.goldCoinImage8 = PhotoImage(file="Images/goldCoin8.png").subsample(2,2)
    data.goldCoinImage9 = PhotoImage(file="Images/goldCoin9.png").subsample(2,2)
    data.goldCoinImage10 = PhotoImage(file="Images/goldCoin10.png").subsample(2,2)
    data.goldCoinImage11 = PhotoImage(file="Images/goldCoin11.png").subsample(2,2)
    data.goldCoinImage12 = PhotoImage(file="Images/goldCoin12.png").subsample(2,2)
    data.goldCoins = [data.goldCoinImage1, data.goldCoinImage2, data.goldCoinImage3, data.goldCoinImage4, data.goldCoinImage5, data.goldCoinImage6, data.goldCoinImage7, data.goldCoinImage8, data.goldCoinImage9, data.goldCoinImage10, data.goldCoinImage11, data.goldCoinImage12]
    # silver coins
    data.silverCoinImage1 = PhotoImage(file="Images/silverCoin1.png").subsample(2,2)
    data.silverCoinImage2 = PhotoImage(file="Images/silverCoin2.png").subsample(2,2)
    data.silverCoinImage3 = PhotoImage(file="Images/silverCoin3.png").subsample(2,2)
    data.silverCoinImage4 = PhotoImage(file="Images/silverCoin4.png").subsample(2,2)
    data.silverCoinImage5 = PhotoImage(file="Images/silverCoin5.png").subsample(2,2)
    data.silverCoinImage6 = PhotoImage(file="Images/silverCoin6.png").subsample(2,2)    
    data.silverCoinImage7 = PhotoImage(file="Images/silverCoin7.png").subsample(2,2)    
    data.silverCoinImage8 = PhotoImage(file="Images/silverCoin8.png").subsample(2,2)
    data.silverCoinImage9 = PhotoImage(file="Images/silverCoin9.png").subsample(2,2)
    data.silverCoinImage10 = PhotoImage(file="Images/silverCoin10.png").subsample(2,2)
    data.silverCoinImage11 = PhotoImage(file="Images/silverCoin11.png").subsample(2,2)
    data.silverCoinImage12 = PhotoImage(file="Images/silverCoin12.png").subsample(2,2)
    data.silverCoins = [data.silverCoinImage1, data.silverCoinImage2, data.silverCoinImage3, data.silverCoinImage4, data.silverCoinImage5, data.silverCoinImage6, data.silverCoinImage7, data.silverCoinImage8, data.silverCoinImage9, data.silverCoinImage10, data.silverCoinImage11, data.silverCoinImage12]
    # bronze coins
    data.bronzeCoinImage1 = PhotoImage(file="Images/bronzeCoin1.png").subsample(2,2)
    data.bronzeCoinImage2 = PhotoImage(file="Images/bronzeCoin2.png").subsample(2,2)
    data.bronzeCoinImage3 = PhotoImage(file="Images/bronzeCoin3.png").subsample(2,2)
    data.bronzeCoinImage4 = PhotoImage(file="Images/bronzeCoin4.png").subsample(2,2)
    data.bronzeCoinImage5 = PhotoImage(file="Images/bronzeCoin5.png").subsample(2,2)
    data.bronzeCoinImage6 = PhotoImage(file="Images/bronzeCoin6.png").subsample(2,2)    
    data.bronzeCoinImage7 = PhotoImage(file="Images/bronzeCoin7.png").subsample(2,2)    
    data.bronzeCoinImage8 = PhotoImage(file="Images/bronzeCoin8.png").subsample(2,2)
    data.bronzeCoinImage9 = PhotoImage(file="Images/bronzeCoin9.png").subsample(2,2)
    data.bronzeCoinImage10 = PhotoImage(file="Images/bronzeCoin10.png").subsample(2,2)
    data.bronzeCoinImage11 = PhotoImage(file="Images/bronzeCoin11.png").subsample(2,2)
    data.bronzeCoinImage12 = PhotoImage(file="Images/bronzeCoin12.png").subsample(2,2)
    data.bronzeCoins = [data.bronzeCoinImage1, data.bronzeCoinImage2, data.bronzeCoinImage3, data.bronzeCoinImage4, data.bronzeCoinImage5, data.bronzeCoinImage6, data.bronzeCoinImage7, data.bronzeCoinImage8, data.bronzeCoinImage9, data.bronzeCoinImage10, data.bronzeCoinImage11, data.bronzeCoinImage12]
    data.coinIndex = 0

def loadHouseImages(data):
    # from http://www.playbuzz.com/lilyanna10/which-horcrux-are-you-from-harry-potter
    data.gryffindor = PhotoImage(file="Images/gryffindor.png").zoom(2,2)
    data.slytherin = PhotoImage(file="Images/slytherin.png").zoom(2,2)
    data.ravenclaw = PhotoImage(file="Images/ravenclaw.png").zoom(2,2)
    data.hufflepuff = PhotoImage(file="Images/hufflepuff.png").zoom(2,2)
    # from https://wallpapercave.com/parchment-wallpapers
    data.parchmentImage = PhotoImage(file="Images/parchment.png").subsample(2,2)