# banana2 : create and move one minion with random velocities (normalized to 1)
import time, pygame
from random import random

from myvectors import Vec

WIDTH, HEIGHT = 800, 800
background_color = (20,20,20)
yellow = (250,250,0)

msize = 4

class Minion():
    def __init__(self,pos=(WIDTH/2,HEIGHT-50),vel=(random()-0.5,random()-0.5),acc=(0,0)):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.vel.vnorm()    # added from now on, so speed of minions are the same
        self.acc = Vec(acc)

    def move(self):
        self.vel.vadd(self.acc)
        self.pos.vadd(self.vel)
        self.acc.vtimes(0)
        

minion = Minion((WIDTH/2,HEIGHT-50), (random()-0.5,random()-0.5))
minion2 = Minion((WIDTH/2,HEIGHT-50), (random()-0.5,random()-0.5))

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("B : 2 Minions instanciated, moving towards random directions")

running = True

while running:

    win.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    
    pygame.draw.circle(win,yellow,(minion2.pos.x, minion2.pos.y), msize)
    pygame.draw.circle(win,yellow,(minion.pos.x, minion.pos.y), msize)

    minion.move()
    minion2.move()

  
    
    time.sleep(0.005)

    pygame.display.update()

pygame.quit()