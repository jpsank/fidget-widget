import pygame
import math
import pickle
import os
import sys
import random


white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
orange = (255,155,0)
lightgrey = (200,200,200)
lightlightgrey = (245,245,245)
grey = (100,100,100)
purple = (255,0,255)
royalpurple = (200,0,255)
brown = (255,200,120)
cyan = (0,255,255)

UPGRADES = [
    {"title": "Your Little Fidget","desc": "This is where it all begins: your very first fidget spinner",
     "params": [150,.09,.93,(red,red,red)]},
    {"title": "Little green spidget","desc": "Environmentally-friendly because it is green",
     "params": [150,.085,.935,(green,green,green)]},
    {"title": "Fresh Spidget Finner","desc": "A fresh, new fidget spinner because you don't like plastic",
     "params": [200,.08,.95,(red,yellow,orange)]},
    {"title": "Banana Spinner","desc": "This spinner is totally bananas",
     "params": [200,.075,.95,(yellow,brown,yellow)]},
    {"title": "Metal Finner","desc": "Your first fidget spinner with metal bearings",
     "params": [220,.06,.95,(grey,lightgrey,lightgrey)]},

    {"title": "Spinnit Fidger","desc": "Spin it to win it",
     "params": [250,.05,.96,(yellow,orange,red)]},

    {"title": "PokeSpinner","desc": "Have to catch them all",
     "params": [250,.04,.96,(lightlightgrey,red,yellow,black)]},

    {"title": "King Spidget Finner","desc": "A fidget spinner fit for a king!",
     "params": [250,.06,.97,(yellow,cyan,green,royalpurple)]},
    {"title": "Invisi-Spinner","desc": "It's so fast you can't see it.",
     "params": [250,.04,.98,(white,white,white)]},
    {"title": "Slightly Invisi-Spinner","desc": "Because the last one was too invisible",
     "params": [250,.03,.985,(white,lightgrey,white)]},
    {"title": "Electric Spidget Finner","desc": "Batteries sold separately",
     "params": [250,.02,.995,(grey,green,blue,yellow)]},
    {"title": "Master Spinner","desc": "You are now a master in the art of spidget-finning",
     "params": [250,.005,.995,(purple,black,red,royalpurple)]},
    {"title": "Chaos Spinner","desc": "Mentally unstable fidget spidger",
     "params": [250,[-.1,.1],[.9,1.09],(black,red,red,purple)]},
    {"title": "Rainbow Spinner","desc": "There's gold at the end of this rainbow",
     "params": [250,.002,.997,(lightlightgrey,[orange,yellow,green],red,[blue,purple,royalpurple])]},
    {"title": "Zero Friction Spinner","desc": "Will spin for as long as you want it to spin",
     "params": [270,0.0,1.0,(black,red,cyan,red)]},
    {"title": "Pandora's Fidget Spinner","desc": "Whatever you do, don't spin it",
     "params": [300,0.0,1.01,(black,[cyan,green,yellow],red,[cyan,green,yellow])]},
]

if not os.path.exists('save.p'):
    with open('save.p','wb') as f:
        pickle.dump([0, 0], f)


def dist(pos1,pos2):
    return math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)


class Button:
    def __init__(self,rect,color=lightgrey,borderSize=0):
        self.rect = rect
        self.color = color
        self.borderSize = borderSize

    def is_overlapping(self,pos):
        return pygame.Rect.colliderect(pygame.Rect(*pos, 0, 0), self.rect)

    def update(self,buttonText):
        pygame.draw.rect(display,self.color,self.rect,self.borderSize)
        text = smallfont.render(buttonText, True, (0, 0, 0))
        display.blit(text,(int(self.rect[0]+self.rect[2]/2 - text.get_width() / 2), int(self.rect[1]+self.rect[3]/2 - text.get_height() / 2)))


class FidgetSpinner(pygame.sprite.Sprite):
    def __init__(self,x,y,size=250,friction=.05,dampening=.98,colors=(red, yellow, orange)):
        super().__init__()
        self.x,self.y = x,y
        self.rot = 0
        self.size = size
        self.rotAccel = 0
        self.padding = self.size/5

        self.colors = colors

        self.friction, self.dampening = friction, dampening

        self.rotCount = 0

        self.image = pygame.Surface((int(self.size+self.padding), int(self.size+self.padding)))
        self.image.convert()
        self.rect = pygame.Rect(x+self.padding/2, y+self.padding/2, int(self.size), int(self.size))

    def changeTheme(self,size=250,friction=.05,dampening=.98,colors=(red, yellow, orange)):
        self.size = size
        self.padding = self.size / 4

        self.x,self.y = int(dispWidth/2) - (UPGRADES[LEVEL]["params"][0] * 1.2) / 2, int(dispHeight / 2) - (UPGRADES[LEVEL]["params"][0] * 1.2) / 2

        self.image = pygame.Surface((int(self.size + self.padding), int(self.size + self.padding)))
        self.image.convert()
        self.rect = pygame.Rect(self.x + self.padding / 2, self.y + self.padding / 2, int(self.size), int(self.size))

        self.friction = friction
        self.dampening = dampening
        self.colors = colors

    def spin(self):
        self.rot += self.rotAccel
        if self.rot >= 360:
            m = int(self.rot/360)
            self.rotCount += m
            self.rot -= 360*m
        elif self.rot <= -360:
            m = abs(int(self.rot / 360))
            self.rotCount += m
            self.rot += 360 * m
        self.dampen()

    def dampen(self):
        dampen = random.uniform(*self.dampening) if isinstance(self.dampening,list) else self.dampening
        friction = random.uniform(*self.friction) if isinstance(self.friction, list) else self.friction

        self.rotAccel *= dampen
        if self.rotAccel > friction:
            self.rotAccel -= friction
        elif self.rotAccel < -friction:
            self.rotAccel += friction
        else:
            self.rotAccel = 0

    def is_overlapping(self,pos):
        return pygame.Rect.colliderect(pygame.Rect(*pos,0,0),self.rect)

    def update(self):
        self.image.fill(white)
        width,height = self.size,self.size
        for i in range(0,3):
            a = i*120
            x = (width/2+self.padding/2) - math.cos(math.radians(self.rot+a)) * width/2
            y = (height/2+self.padding/2) + math.sin(math.radians(self.rot+a)) * height/2
            pygame.draw.line(self.image,self.colors[0],((width/2+self.padding/2),(height/2+self.padding/2)),(x,y),int(width/4))
            if len(self.colors) >= 4:
                pygame.draw.line(self.image, self.colors[3][i] if isinstance(self.colors[3],list) else self.colors[3],
                                 ((width / 2 + self.padding / 2), (height / 2 + self.padding / 2)), (x, y))
            pygame.draw.circle(self.image, self.colors[0], (int(x), int(y)), int(width / 8))
            pygame.draw.circle(self.image,self.colors[1][i] if isinstance(self.colors[1],list) else self.colors[1],
                               (int(x),int(y)),int(width/12))
        pygame.draw.circle(self.image, self.colors[2], (int(width/2+self.padding/2), int(height/2+self.padding/2)), int(width / 10))


pygame.init()

FPS = 60

dispWidth,dispHeight = 800,600

display = pygame.display.set_mode((dispWidth,dispHeight))
pygame.display.set_caption("Fidget Widget")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Comic Sans MS", 36)
smallfont = pygame.font.SysFont("Comic Sans MS", 24)

with open('save.p','rb') as f:
    LEVEL,rotCount = pickle.load(f)

fidget = FidgetSpinner(int(dispWidth/2) - (UPGRADES[LEVEL]["params"][0] * 1.2) / 2,
                       int(dispHeight/2) - (UPGRADES[LEVEL]["params"][0] * 1.2) / 2)
fidget.rotCount = rotCount
fidget.changeTheme(*UPGRADES[LEVEL]["params"])


upgradeButton = Button((dispWidth*.25,dispHeight*.9,dispWidth*.5,dispHeight*.1))

dragStart = False
dragEnd = False

index = 0
while True:
    cost = int(5 * (1.4 ** LEVEL))

    mousepos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            if LEVEL < len(UPGRADES) - 1:
                if upgradeButton.is_overlapping(mousepos):
                    if fidget.rotCount >= cost:
                        fidget.rotCount -= cost
                        LEVEL += 1
                        fidget.changeTheme(*UPGRADES[LEVEL]["params"])

                        with open('save.p', 'wb') as f:
                            pickle.dump([LEVEL, fidget.rotCount], f)
                    else:
                        upgradeButton.update("not enough R")
    if index%FPS == 0:
        with open('save.p', 'wb') as f:
            pickle.dump([LEVEL, fidget.rotCount], f)

    display.fill(white)

    if pygame.mouse.get_pressed()[0] == 1:
        if fidget.is_overlapping(mousepos):
            if not dragStart:
                dragStart = mousepos
            else:
                dragEnd = mousepos
        if dragStart and dragEnd:
            x = 0
            y = 0
            if dragEnd[1] > fidget.y+fidget.size/2+fidget.padding/2:
                x = dragEnd[0]-dragStart[0]
            else:
                x = dragStart[0]-dragEnd[0]
            if dragEnd[0] > fidget.x+fidget.size/2+fidget.padding/2:
                y = dragStart[1]-dragEnd[1]
            else:
                y = dragEnd[1]-dragStart[1]
            fidget.rotAccel = (x+y)/2
            dragStart = False
            dragEnd = False

    fidget.spin()
    fidget.update()
    display.blit(fidget.image, (fidget.x, fidget.y))

    text = font.render("%s rotations" % fidget.rotCount, True, (0, 0, 0))
    display.blit(text,(int(dispWidth/2-text.get_width()/2),int(dispHeight/10-text.get_height()/2)))

    text = font.render(UPGRADES[LEVEL]["title"], True, (0, 0, 0))
    display.blit(text, (int(dispWidth / 2 - text.get_width() / 2), int((3.7 * dispHeight / 5) - text.get_height() / 2)))
    text = smallfont.render(UPGRADES[LEVEL]["desc"], True, (0, 0, 0))
    display.blit(text, (int(dispWidth / 2 - text.get_width() / 2), int((4.2 * dispHeight / 5) - text.get_height() / 2)))

    if LEVEL < len(UPGRADES) - 1:
        upgradeButton.update("upgrade %s R" % cost)

    width,height = fidget.rect.width,fidget.rect.height
    for i in range(0, 360, 120):
        x = (fidget.x + width/2 + fidget.padding / 2) - math.cos(math.radians(fidget.rot + i)) * width / 2
        y = (fidget.y + height/2 + fidget.padding / 2) + math.sin(math.radians(fidget.rot + i)) * height / 2
        pygame.draw.line(display, lightgrey, mousepos, (x, y))

    pygame.display.update()
    clock.tick(FPS)
    index += 1

