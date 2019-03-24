# Bullets superclass

class Bullets(object):
    
    def __init__(self, x, y, data):
        self.x, self.y = x, y 
        data.bullets.add(self)

# for level 1 and 3    
class Spell(Bullets):
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.photo = data.spellImage
        data.spellWidth = self.width = self.photo.width()
        data.spellHeight = self.height = self.photo.height()
    
    @staticmethod
    def draw(canvas, data):
        for bullet in data.bullets:
            canvas.create_image(bullet.x - data.me.totalScrollX, bullet.y - data.me.totalScrollY, image=bullet.photo)
 
# for level 2
class Patronus(Bullets):
    
    def __init__(self, x, y, data):
        super().__init__(x, y, data)
        self.photo = data.patronusImage1
        data.patronusWidth = self.width = self.photo.width()
        data.patronusHeight = self.height = self.photo.height()
        data.me.patronus = data.time
    
    @staticmethod
    def draw(canvas, data):
        for bullet in data.bullets:
            canvas.create_image(bullet.x - data.me.totalScrollX, bullet.y - data.me.totalScrollY, image=data.patronuses[data.patronusIndex])

                    
                    
        