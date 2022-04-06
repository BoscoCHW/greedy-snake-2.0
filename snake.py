import pygame 
import random

class Snake:
  """A doubly linked list implementation of a snake"""
  WIDTH = 10
 
  def __init__(self):
    """Initializes a snake at a random location of a random length between 3-8 parts"""
    self.length = random.randint(3, 8)
    self.start_x = random.randint(30, 370)
    self.start_y = random.randint(100, 350)

    self.direction = "UP"
    self.head = Part(self.start_x, self.start_y)
    current_part = self.head
    for _ in range(self.length - 1):
      current_part.next = Part(current_part.rect.x, current_part.rect.y+self.WIDTH)
      prev = current_part
      current_part = current_part.next
      current_part.prev = prev

    self.tail = current_part
    self.state = "ALIVE"
    
  def move(self):
    """Implements the movment of the snake by moving the last Part of the snake to the front."""
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
    sec_last = self.tail.prev

    sec_last.next = None
    self.tail = sec_last

    tmp.next = self.head
    tmp.prev = None
    self.head.prev = tmp
    self.head = tmp
    
  def grow(self):
    """Implements the growth of the snake by adding a new Part in the front."""
    if self.direction == "UP":
      part = Part(self.head.rect.x, self.head.rect.y-self.WIDTH)
    elif self.direction == "RIGHT": 
      part = Part(self.head.rect.x+self.WIDTH, self.head.rect.y)
    elif self.direction == "DOWN": 
      part = Part(self.head.rect.x, self.head.rect.y+self.WIDTH)
    elif self.direction == "LEFT": 
      part = Part(self.head.rect.x-self.WIDTH, self.head.rect.y)

    old_head = self.head
    self.head = part
    part.next = old_head
    old_head.prev = self.head

    self.length += 1
    

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
    """return a list of snake body parts"""
    snake = []
    tmp = self.head
    while tmp != None:
      snake.append(tmp)
      tmp = tmp.next
    return snake

class Part:
  """Represents a part of the snake."""
  def __init__(self, x, y):
    self.next = None
    self.prev = None
    self.rect = pygame.Rect(x, y, Snake.WIDTH, Snake.WIDTH)