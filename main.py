import pygame
import pygame.locals
from snake import Snake
from food import Food


WIDTH, HEIGHT = 400, 400
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Greedy Snake")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
MODAL_BACKGROUND = (50, 50, 50)

# Text 
SMALL_FONT_SIZE = 12
BIG_FONT_SIZE = 30
SNAKE_SCORE_POS = (WIDTH-90, 5)
PLAYER2_SCORE_POS = (5, 5)

# Game duration in seconds
DURATION = 2 * 60


FPS = 20

def render_text_surface(text: str, color: tuple, size: int):
  """Utility function to render a text surface"""
  arial = pygame.font.SysFont("arial", size)
  text_surface = arial.render(text, True, color)

  return text_surface

def draw_window(snake: Snake, food: Food, snake_score: int, player2_score: int, time_remained: int):
  """ draw the window at the end of every loop"""
  WINDOW.fill(BLACK)

  time_surf = render_text_surface(f"Remaining time: {time_remained}s", WHITE, SMALL_FONT_SIZE)
  time_pos_x = WINDOW.get_rect().centerx - time_surf.get_rect().width / 2
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
  modal_bg = pygame.draw.rect(WINDOW, MODAL_BACKGROUND, WINDOW.get_rect().inflate(-200, -300))
  if snake.state == "DEAD":
    modal_text = render_text_surface("Snake Lost!", WHITE, BIG_FONT_SIZE)
  else:
    if snake_score > player2_score:
      modal_text = render_text_surface("Snake Won!", WHITE, BIG_FONT_SIZE)
    else:
      modal_text = render_text_surface("Snake Lost!", WHITE, BIG_FONT_SIZE)
  
  modal_text_width, modal_text_height = modal_text.get_rect().width, modal_text.get_rect().height
  modal_text_pos = (modal_bg.centerx - modal_text_width / 2, modal_bg.centery - modal_text_height / 2)
  WINDOW.blit(modal_text, modal_text_pos)
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
  snake_rects = [part.rect for part in snake.to_list()]

  # if the snake hit the window border or eats itself, it'll be dead
  if (not WINDOW.get_rect().contains(snake.head.rect) or 
      snake.head.rect.collidelist(snake_rects[2:]) != -1):

    snake.state = "DEAD"



def main():
  pygame.init()
  pygame.font.init()
  clock = pygame.time.Clock()

  # initialize snake, food and scores
  snake = Snake()
  snake_score = 0
  food = create_food(snake)
  player2_score = 0

  running = True
  while running:

    clock.tick(FPS)

    time_in_sec = int(pygame.time.get_ticks() / 1000)
    time_remaining = DURATION - time_in_sec  # calculate remaining time

    for event in pygame.event.get():
      # quit the game if the close window button is clicked
      if event.type == pygame.locals.QUIT:
        running = False
        pygame.quit()


    keys = pygame.key.get_pressed()

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
      break
    
    draw_window(snake, food, snake_score, player2_score, time_remaining)

  # when game ends, draw the end game modal
  draw_end(snake_score, player2_score, snake)
  pygame.time.wait(4000)

if __name__ == "__main__":
  main()