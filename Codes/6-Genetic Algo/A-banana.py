# banana1 : create canvas and single minion moving up from the starting position.
# imports
import time, pygame
from myvectors import Vec

# global things
WIDTH, HEIGHT = 800, 800       # canvas size
background_color = (20,20,20)
yellow = (250,250,0)
msize = 4  # minion size

# most used objects will be minions, so let's build the class :       
class Minion(): # velocity (0,-1) by default, means the minion goes up
    def __init__(self,pos=(WIDTH/2,HEIGHT-50),vel=(0,-1),acc=(0,0)):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.acc = Vec(acc)

    def move(self):
        self.vel.vadd(self.acc)
        self.pos.vadd(self.vel)
        self.acc.vtimes(0)

# instantiate one minion
minion = Minion()

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("A - first minion is borm, moves up")

running = True

while running:
    win.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    pygame.draw.circle(win,yellow,(minion.pos.x, minion.pos.y), msize)
    
    minion.move()

    time.sleep(0.01)
    pygame.display.update()

pygame.quit()