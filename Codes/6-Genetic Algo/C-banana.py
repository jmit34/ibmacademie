# banana2 : create a population of minions, with random velocities (normalized to 1)
import time, pygame
from random import random, randrange
from myvectors import Vec

WIDTH, HEIGHT = 800, 800
background_color = (20,20,20)
yellow = (250,250,0)


msize = 4

class Minion():
    def __init__(self,pos=(WIDTH/2,HEIGHT-50),vel=(random()-0.5,random()-0.5),acc=(0,0)):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.vel.vnorm()
        self.acc = Vec(acc)

    def move(self):
        self.vel.vadd(self.acc)
        self.pos.vadd(self.vel)
        self.acc.vtimes(0)
        
class Population():
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.minions = []
        for i in range(self.pop_size):
            self.minions.append(Minion((WIDTH/2,HEIGHT-50), (random()-0.5,random()-0.5), (0,0)))
        
    def move(self):
        for m in self.minions:
            m.move()

pop = Population(10)

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("C : Now running a population of Minions")

running = True

while running:
    win.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    for i in range(pop.pop_size):
        pygame.draw.circle(win,yellow, (pop.minions[i].pos.x, pop.minions[i].pos.y), msize)
        
    pop.move()
    
    time.sleep(0.01)

    pygame.display.update()

pygame.quit()