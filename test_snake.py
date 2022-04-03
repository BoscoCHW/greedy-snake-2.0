from snake import Snake
from unittest.mock import patch
import pytest

INITIAL_LENGTH = 5
INITIAL_X = 6
INITIAL_Y = 7

@pytest.fixture
@patch("random.randint", side_effect=[INITIAL_LENGTH, INITIAL_X, INITIAL_Y])
def snake(mock_randint):
  snake = Snake()
  mock_randint.assert_called()
  return snake


def test_snake(snake):
  assert snake.WIDTH == 10
  assert snake.length == 5
  assert snake.start_x == 6
  assert snake.start_y == 7
  assert snake.state == "ALIVE"

@pytest.mark.parametrize("direction", ["UP","DOWN","LEFT","RIGHT"])
def test_move(direction, snake):
  """after the snake moved, the second last Part would become the last Part
    and the last Part would become the Head
  """
  snake.direction = direction
  original_second_last = snake.find_sec_last()
  original_last = snake.find_last()
  snake.move()
  last = snake.find_last()
  assert original_second_last == last
  assert original_last == snake.head

def test_to_list(snake):
  snake_list = snake.to_list()
  assert isinstance(snake_list, list)
  assert len(snake_list) == snake.length

@pytest.mark.parametrize("direction,length", [("UP", INITIAL_LENGTH + 1), ("DOWN", INITIAL_LENGTH + 1), ("LEFT", INITIAL_LENGTH + 1), ("RIGHT", INITIAL_LENGTH + 1)])
def test_grow(direction, length, snake):
  snake.direction = direction
  snake.grow()
  snake_list = snake.to_list()
  assert len(snake_list) == length