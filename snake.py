import pygame 
import random

class Snake:
  """Singly linked list implementation of a snake"""
  WIDTH = 10
  LENGTH = random.randint(3, 8)
  START_X = random.randint(30, 370)
  START_Y = random.randint(100, 350)

  def __init__(self):
    self.direction = "UP"
    self.head = Part(self.START_X, self.START_Y)
    part = self.head
    for _ in range(self.LENGTH):
      part.next = Part(part.rect.x, part.rect.y+self.WIDTH)
      part = part.next

    self.tail = self.find_last()
    self.state = "ALIVE"
    
  def move(self):
    
    if self.direction == "UP":
      self.tail.rect.x = self.head.rect.x
      self.tail.rect.y = self.head.rect.y - self.WIDTH 
    elif self.direction == "RIGHT":
      self.tail.rect.x = self.head.rect.x + self.WIDTH 
      self.tail.rect.y = self.head.rect.y
    elif self.direction == "DOWN":
      self.tail.rect.x = self.head.rect.x
      self.tail.rect.y = self.head.rect.y + self.WIDTH 
    elif self.direction == "LEFT":
      self.tail.rect.x = self.head.rect.x - self.WIDTH 
      self.tail.rect.y = self.head.rect.y

    tmp = self.tail
    sec_last = self.find_sec_last()

    sec_last.next = None
    self.tail = sec_last

    tmp.next = self.head
    self.head = tmp
    
  def grow(self):
    if self.direction == "UP":
      part = Part(self.head.rect.x, self.head.rect.y-self.WIDTH)
    elif self.direction == "RIGHT": 
      part = Part(self.head.rect.x+self.WIDTH, self.head.rect.y)
    elif self.direction == "DOWN": 
      part = Part(self.head.rect.x, self.head.rect.y+self.WIDTH)
    elif self.direction == "LEFT": 
      part = Part(self.head.rect.x-self.WIDTH, self.head.rect.y)

    tmp = self.head
    self.head = part
    part.next = tmp
    

  def find_last(self):
    tmp = self.head
    while tmp and tmp.next:
      tmp = tmp.next
    return tmp

  def find_sec_last(self):
    tmp = self.head
    sec_last = None
    while tmp and tmp.next:
      sec_last = tmp
      tmp = tmp.next

    return sec_last

  def to_list(self):
    """return a list a snake body parts"""
    snake = []
    tmp = self.head
    while tmp.next:
      snake.append(tmp)
      tmp = tmp.next
    return snake

class Part:
  def __init__(self, x, y):
    self.next = None
    self.rect = pygame.Rect(x, y, Snake.WIDTH, Snake.WIDTH)