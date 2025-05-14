# banana4 : ajout de la durée de vie de la population
#  et ajout de l'ADN 
import time, pygame
from random import random
from myvectors import Vec

WIDTH, HEIGHT = 800, 800
background_color = (20,20,20)
yellow = (250,250,0)


msize = 4
lifespan = 400

class Minion():
    def __init__(self,pos=(WIDTH/2,HEIGHT-50),vel=(random()-0.5,random()-0.5),acc=(0,0)):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.vel.vnorm(1)
        self.acc = Vec(acc)
        self.dna = DNA()

    def move(self,life_tick):
        self.acc.vadd(self.dna.genes[life_tick])
        self.vel.vadd(self.acc)
        self.pos.vadd(self.vel)
        self.acc.vtimes(0)
        
class Population():
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.minions = []
        for i in range(self.pop_size):
            self.minions.append(Minion((WIDTH/2,HEIGHT-50), (random()-0.5,random()-0.5), (0,0)))
        
    def move(self,life_tick):
        for m in self.minions:
            m.move(life_tick)

class DNA():
    def __init__(self) -> None:
        self.genes = []
        for i in range(lifespan): 
            self.genes.append(Vec((random()-0.5,random()-0.5)))
            self.genes[i].vnorm(0.1)

pop = Population(40)
life_count = 0

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("D : Population of Minions with DNA, no selection, no heredity")

running = True

while running:
    win.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    life_count +=1
    if life_count == lifespan: 
        pop = Population(40)
        life_count = 0 

    for i in range(pop.pop_size):
        pygame.draw.circle(win,yellow, (pop.minions[i].pos.x, pop.minions[i].pos.y), msize)
    
    pop.move(life_count)

    
    time.sleep(0.01)

    pygame.display.update()

pygame.quit()