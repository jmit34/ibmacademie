#snake ai : Youtube FreecodeCamp : Python + Pytorch + Pygame Reinforcement learning - Train an AI to play snake
# Patrick Loeber
# https://www.youtube.com/watch?v=L8ypSXwyBds

# reward : eat food = +10, game over = - 10, sinon : 0
# action : tout droit [1,0,0] , à droite [0,1,0], à gauche [0,0,1] 
#          (pas de tournant à 180 degrés)
# état   : 11 valeurs : [danger: straight, right, left, 
#                        direction:  left, right, up, down,
#                        food:  left right, up, down]
# le NN feed forward) aura 11 entrées(états), une chouche cachée, et 3 sorties (actions)
# 
import pygame
import random
from enum import Enum
from collections import namedtuple
import os

current_dir = os.path.dirname(__file__) 

pygame.init()
font = pygame.font.Font(current_dir+"/arial.ttf", 25)


self.reset()  #AI

# todos :
#--------
# reset function
# reward 
# play(action) -> direction
# game iteration
# is_collision doit changer


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200,0,0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
BLACK = (0,0,0)

BLOCK_SIZE = 20
SPEED = 10

class SnakeGameAI:  #AI
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        
       
    def reset(self):  #AI
        # init game state  
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0 
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self,action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            ##if event.type == pygame.KEYDOWN:
            ##    if event.key == pygame.K_LEFT:
            ##        self.direction = Direction.LEFT
            ##    elif event.key == pygame.K_RIGHT:
            ##        self.direction = Direction.RIGHT
            ##    elif event.key == pygame.K_UP:
            ##        self.direction = Direction.UP
            ##    elif event.key == pygame.K_DOWN:
            ##        self.direction = Direction.DOWN
        
        # 2. move
        self._move(action) # update the head #AI
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        reward = 0  # AI 
        game_over = False
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10 #AI
            return reward, game_over, self.score
        
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):  #AI
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGameAI()
    
    # game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
    for i in range(5): 
        print('* * * * * * * * * * * *  * * * *') 
        print('* * * * * * * * * * * *  * * * *')
        print('GAME OVER !!! Final Score', score)
        print('* * * * * * * * * * * *  * * * *')
        
    pygame.quit()
