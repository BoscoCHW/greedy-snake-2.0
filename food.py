import random 
import pygame

class Food:
  SIZE = 10
  def __init__(self):
    pos_x = random.randint(0, 390)
    pos_y = random.randint(0, 390)
    self.rect = pygame.Rect(pos_x, pos_y, self.SIZE, self.SIZE)
    # print(self.rect.center)
