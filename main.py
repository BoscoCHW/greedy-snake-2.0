import pygame
import pygame.locals
from snake import Snake
from food import Food
import sys

WIDTH, HEIGHT = 600, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Greedy Snake 2.0")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
MODAL_BACKGROUND = (50, 50, 50)

# Text 
SMALL_FONT_SIZE = 12
MEDIUM_FONT_SIZE = 20
BIG_FONT_SIZE = 30
SNAKE_SCORE_POS = (WIDTH-90, 5)
PLAYER2_SCORE_POS = (5, 5)

# Game duration in seconds
DURATION = 2 * 60


FPS = 17

def quit_game():
  pygame.quit()
  sys.exit()

def render_text_surface(text: str, color: tuple, size: int):
  """Utility function to render a text surface"""
  arial = pygame.font.SysFont("arial", size)
  text_surface = arial.render(text, True, color)

  return text_surface

def pos_x_for_centering(bg: pygame.Surface, fg: pygame.Surface):
  """calculate the x pos of the foreground given a background
     if you were to center the foreground
  """
  return bg.get_rect().centerx - fg.get_rect().width / 2

def draw_start():
  """draw the start screen"""
  WINDOW.fill(BLACK)
  greeting_surf = render_text_surface("Welcome to Greedy Snake 2.0", WHITE, MEDIUM_FONT_SIZE)
  greeting_pos_x = pos_x_for_centering(WINDOW, greeting_surf)
  WINDOW.blit(greeting_surf, (greeting_pos_x, 100))

  instr_surf = render_text_surface("Press any key to start.", WHITE, SMALL_FONT_SIZE)
  instr_pos_x = pos_x_for_centering(WINDOW, instr_surf)
  WINDOW.blit(instr_surf, (instr_pos_x, 200))
  pygame.display.update()

def draw_window(snake: Snake, food: Food, snake_score: int, player2_score: int, time_remained: int):
  """ draw the game window"""
  WINDOW.fill(BLACK)

  time_surf = render_text_surface(f"Remaining time: {time_remained}s", WHITE, SMALL_FONT_SIZE)
  time_pos_x = pos_x_for_centering(WINDOW, time_surf)
  WINDOW.blit(time_surf, (time_pos_x, 5))

  snake_score_surf = render_text_surface(f"Snake Score: {snake_score}", WHITE, SMALL_FONT_SIZE)
  player2_score_surf = render_text_surface(f"Neutralized: {player2_score}", WHITE, SMALL_FONT_SIZE)
  WINDOW.blit(snake_score_surf, SNAKE_SCORE_POS)
  WINDOW.blit(player2_score_surf, PLAYER2_SCORE_POS)

  part = snake.head
  while part:
    pygame.draw.rect(WINDOW, WHITE, part.rect)
    part = part.next
  pygame.draw.circle(WINDOW, YELLOW, food.rect.center, food.SIZE/2)
  pygame.display.update()

def draw_end(snake_score, player2_score, snake):
  """ draw the end game window """
  modal_surf = pygame.Surface((300, 120))
  modal_surf.fill(MODAL_BACKGROUND)

  if snake.state == "DEAD":
    verdict_surf = render_text_surface("Snake Lost!", WHITE, BIG_FONT_SIZE)
  else:
    if snake_score > player2_score:
      verdict_surf = render_text_surface("Snake Won!", WHITE, BIG_FONT_SIZE)
    else:
      verdict_surf = render_text_surface("Snake Lost!", WHITE, BIG_FONT_SIZE)

  instr_surf = render_text_surface("Press any key to restart or Esc to exit.", WHITE, SMALL_FONT_SIZE)

  verdict_pos_x = pos_x_for_centering(modal_surf, verdict_surf)
  instr_pos_x = pos_x_for_centering(modal_surf, instr_surf)

  modal_surf.blit(verdict_surf, (verdict_pos_x, 20))
  modal_surf.blit(instr_surf, (instr_pos_x, 80))

  
  WINDOW.blit(modal_surf.convert(), (50, 100))

  pygame.display.update()

def create_food(snake: Snake):
  """create food and make sure the food doesn't collide with the snake"""
  food = Food()
  snake_parts = snake.to_list()
  snake_rects = [snake_part.rect for snake_part in snake_parts]
  while food.rect.collidelist(snake_rects) != -1:
    food = Food()
  return food

def check_neutralize(keys, snake: Snake):
  """Check if the second player neutralized the snake's food
    the neutralization key depends on the snake's direction
  """
  if (keys[pygame.locals.K_s] and snake.direction == "UP" or 
        keys[pygame.locals.K_w] and snake.direction == "DOWN" or 
        keys[pygame.locals.K_a] and snake.direction == "RIGHT" or
        keys[pygame.locals.K_d] and snake.direction == "LEFT"):
    print("neutralized")
    return True

  return False

def check_snake(snake):
  """Check if the snake hit the wall or ate itself"""
  snake_rects = [part.rect for part in snake.to_list()]

  # if the snake hit the window border or eats itself, it'll be dead
  if (not WINDOW.get_rect().contains(snake.head.rect) or 
      snake.head.rect.collidelist(snake_rects[2:]) != -1):

    snake.state = "DEAD"



def main():
  pygame.init()
  pygame.font.init()
  clock = pygame.time.Clock()
  
  # initialize the session, snake, food and scores
  new_session = True
  snake = Snake()
  snake_score = 0
  food = create_food(snake)
  player2_score = 0
  game_state = "READY"

  running = True
  while running:
    
    clock.tick(FPS)
    for event in pygame.event.get():
      # quit the game if the close window button is clicked or Esc is pressed
      if event.type == pygame.locals.QUIT:
        quit_game()
      elif event.type == pygame.KEYDOWN:
        if event.key == 27:   # Esc is pressed
          quit_game()

    keys = pygame.key.get_pressed()

    if game_state == "READY":
      """ start screen controller """
      draw_start()
      if any(keys):
        game_state = "RUNNING"
        
    elif game_state == "RUNNING":
      """ game controller """
      if new_session:
        session_start_time = pygame.time.get_ticks()
        new_session = False

      time_elapsed = int((pygame.time.get_ticks() - session_start_time) / 1000)
      time_remaining = DURATION - time_elapsed  # calculate remaining time

      # when key is pressed, change direction
      if keys[pygame.locals.K_UP] and snake.direction != "DOWN":
        snake.direction = "UP"
      elif keys[pygame.locals.K_DOWN] and snake.direction != "UP":
        snake.direction = "DOWN"
      elif keys[pygame.locals.K_LEFT] and snake.direction != "RIGHT":
        snake.direction = "LEFT"
      elif keys[pygame.locals.K_RIGHT] and snake.direction != "LEFT":
        snake.direction = "RIGHT"
      
      # move the snake
      snake.move()

      # when the snake eats the food
      if snake.head.rect.colliderect(food.rect):
        # make a new food
        food = create_food(snake)

        # only neutralize the growing when the second player pressed
        # a key that is opposite to the snake's direction
        if check_neutralize(keys, snake):
          player2_score += 2

        else:
          # the second player fails to press the corresponding key
          # the snake grows
          snake.grow()
          snake_score += 1

      
      # if the snake eats its body or hit the window, game ends 
      check_snake(snake)
      if snake.state == "DEAD" or time_remaining <= 0:
        game_state = "END"
      
      draw_window(snake, food, snake_score, player2_score, time_remaining)

    elif game_state == "END":
      """ end screen controller """
      draw_end(snake_score, player2_score, snake)
      if any(keys):
        new_session = True
        snake = Snake()
        snake_score = 0
        food = create_food(snake)
        player2_score = 0
        game_state = "RUNNING"

if __name__ == "__main__":
  main()