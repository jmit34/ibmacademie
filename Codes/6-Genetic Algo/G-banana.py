# banana7 : ajout de la detection du choc avec le point rouge 
import time, pygame
from random import random, choice, randint
from myvectors import Vec

WIDTH, HEIGHT = 800, 800
background_color = (20,20,20)

yellow = (250,250,0)
red = (250,0,0)
green = (51, 153, 51)

msize = 4
pop_size = 50
lifespan = 2000

def maprange(num, inMin, inMax, outMin, outMax):
        if num > inMax: 
            num = inMax
        return outMin + (num - inMin) / (inMax - inMin) * (outMax - outMin)


reward = Vec((WIDTH/2,100))

class Minion():
    def __init__(self,dna,pos=(WIDTH/2,HEIGHT-50),vel=(random()-0.5,random()-0.5),acc=(0,0) ):
        self.pos = Vec(pos)
        self.vel = Vec(vel)
        #self.vel.vnorm(1)
        self.acc = Vec(acc)
        if dna == None: 
            self.dna = DNA(None)
        else: 
            self.dna = dna

        self.fitness = 0 
        self.eat_banana = False

    def move(self,life_tick):
        # while target hat not been hit : 
        if not self.eat_banana: 
            self.acc.vadd(self.dna.genes[life_tick])
            self.vel.vadd(self.acc)
            self.vel.vnorm(1)
            self.pos.vadd(self.vel)
            self.acc.vtimes(0)

        # check if target his hit
        if self.pos.vdist(reward) < 20: 
            self.eat_banana = True

    def compute_fitness(self):
        d = self.pos.vdist(reward)
        self.fitness = maprange(d,0, WIDTH,1,0) 
        if self.eat_banana :
            self.fitness = self.fitness * 25

class Population():
    def __init__(self, pop_size):
        self.pop_size = pop_size
        self.minions = []
        for i in range(self.pop_size):
            self.minions.append(Minion(None,(WIDTH/2,HEIGHT-50), (0,0), (0,0)))
        
    def move(self ,life_tick: int):
        for m in self.minions:
            m.move(life_tick)

    def evaluate(self): 
        maxfit = 0 
        for i in range(self.pop_size):
            self.minions[i].compute_fitness()
            if self.minions[i].fitness > maxfit:
                maxfit = self.minions[i].fitness
            #print(self.minions[i].fitness)
        for i in range(self.pop_size): 
            self.minions[i].fitness /= maxfit
        # now lets fill the dnapool for netx population
        self.dnapool = []
        for i in range(self.pop_size):
            qty = int(self.minions[i].fitness * 150)
            for j in range(qty): 
                self.dnapool.append(self.minions[i])

    def select(self ) -> list:
        # this is where we build a next population on minions by choosing at random 
        # 2 parents from the pull, making the crossover (select a cut point and build
        # a mixed dna to create a new minion in the new population
        newminions = []
        for i in range(self.pop_size): 
            parentA = choice(self.dnapool)
            parentB = choice(self.dnapool)
            child_dna = parentA.dna.crossover(parentB.dna)
            #newminions.append(Minion(child_dna,(WIDTH/2,HEIGHT-50), (random()-0.5,random()-0.5), (0,0)))
            newminions.append(Minion(child_dna,(WIDTH/2,HEIGHT-50), (0,0), (0,0)))
        
        return newminions
    
class DNA():
    def __init__(self, dna) -> None:
        if dna == None: 
            self.genes = []
            for i in range(lifespan): 
                #print(i)
                self.genes.append(Vec((random()-0.5,random()-0.5)))
                self.genes[i].vnorm(0.3)
        else: 
            self.genes = dna

    def crossover(self, partner):
        newdna = []
        midpoint = randint(0,lifespan)

        for i in range(lifespan):
            if i < midpoint: 
                newdna.append(partner.genes[i])
            else: 
                newdna.append(self.genes[i])
        return DNA(newdna)

pop = Population(pop_size)
life_count = 0

pygame.init()

win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("G : stop on reward and get more fitness")

running = True
while running:
    win.fill(background_color)

    # this  is the reward / objective
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
        pop.minions = pop.select()
        life_count = 0 

    for i in range(pop.pop_size):
        pygame.draw.circle(win,yellow, (pop.minions[i].pos.x, pop.minions[i].pos.y), msize)
        
    pop.move(life_count)

    pygame.display.update()

pygame.quit()