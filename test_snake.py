from _pytest.config import directory_arg
from snake import Snake, Part
from unittest.mock import patch, mock_open
import pytest


@pytest.fixture
@patch("random.randint", side_effect=[5, 6, 7])
def snake(mock_randint):
  snake = Snake()
  mock_randint.assert_called()
  return snake


def test_snake(snake):
  assert snake.WIDTH == 10
  assert snake.LENGTH == 5
  assert snake.START_X == 6
  assert snake.START_Y == 7
  assert snake.state == "ALIVE"

@pytest.mark.parametrize("direction", ["UP","DOWN","LEFT","RIGHT"])
def test_move(direction, snake):
  snake.direction = direction
  snake.move()
  assert isinstance(snake.tail, Part)

def test_to_list(snake):
  snake_list = snake.to_list()
  assert isinstance(snake_list, list)
  assert len(snake_list) == 5

@pytest.mark.parametrize("direction,length", [("UP", 6), ("DOWN", 6), ("LEFT", 6), ("RIGHT", 6)])
def test_grow(direction, length, snake):
  snake.direction = direction
  snake.grow()
  snake_list = snake.to_list()
  assert len(snake_list) == length