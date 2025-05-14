# banana5 : ajout de la récompense et du calcul de fitness à la fin
import time, pygame
from random import random, randrange
from myvectors import Vec

WIDTH, HEIGHT = 800, 800
background_color = (20,20,20)
yellow = (250,250,0)
green = (51, 153, 51)
red = (250,0,0)

msize = 4

lifespan = 400

def maprange(num, inMin, inMax, outMin, outMax):
        if num > inMax: 
            num = inMax
        return outMin + (num - inMin) / (inMax - inMin) * (outMax - outMin)




reward = Vec((WIDTH/2,100))


class Minion():
    def __init__(self,pos=(WIDTH/2,HEIGHT-50),vel=(random()-0.5,random()-0.5),acc=(0,0)):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        self.vel.vnorm(1)
        self.acc = Vec(acc)
        self.dna = DNA()
        self.fitness = 0 

    def move(self,life_tick):
        self.acc.vadd(self.dna.genes[life_tick])
        self.vel.vadd(self.acc)
        self.pos.vadd(self.vel)
        self.acc.vtimes(0)

    def compute_fitness(self):
        d = self.pos.vdist(reward)
        self.fitness = maprange(d,0, WIDTH,1,0) 
        
class Population():
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.minions = []
        for i in range(self.pop_size):
            self.minions.append(Minion((WIDTH/2,HEIGHT-50), (0,0), (0,0)))
        
    def move(self,life_tick):
        for m in self.minions:
            m.move(life_tick)

    def evaluate(self): 
        maxfit = 0 
        for i in range(self.pop_size):
            self.minions[i].compute_fitness()
            if self.minions[i].fitness > maxfit:
                maxfit = self.minions[i].fitness
         
        self.dnapool = []
        for i in range(self.pop_size):
            qty = int(self.minions[i].fitness * 100)
            for j in range(qty): 
                self.dnapool.append(self.minions[i])
            
class DNA():
    def __init__(self) -> None:
        self.genes = []
        for i in range(lifespan): 
            #print(i)
            self.genes.append(Vec((random()-0.5,random()-0.5)))
            self.genes[i].vnorm(0.1)

pop = Population(40)

life_count = 0

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("E : Display target and compute fitness for next gen (but not used)")

running = True
while running:
    win.fill(background_color)

    # this is the reward / objective
    pygame.draw.circle(win,yellow, (reward.x, reward.y), 40)
    pygame.draw.circle(win,background_color,(reward.x,reward.y-20),40)
    pygame.draw.circle(win,green,(reward.x+40,reward.y),6)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                running = False

    life_count +=1
    if life_count == lifespan: 
        pop.evaluate()
        ## Maintenant il faut faire le mix pour les new dna et la génération des nouveaux dna
        ## et repartir.
        
        pop = Population(40)
        life_count = 0 

    for i in range(pop.pop_size):
        pygame.draw.circle(win,yellow, (pop.minions[i].pos.x, pop.minions[i].pos.y), msize)
        
    pop.move(life_count)

    time.sleep(0.01)

    pygame.display.update()

pygame.quit()