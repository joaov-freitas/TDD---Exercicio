from snake import io_handler
from snake import WINDOW_HEIGHT,WINDOW_WIDTH,TILE_SIZE, GRID_WIDTH,GRID_HEIGHT
import pytest

@pytest.fixture
def handler():
    return io_handler()

def test_initialization(handler):
    assert handler.snake == [((GRID_WIDTH // 2) * TILE_SIZE, (GRID_HEIGHT // 2) * TILE_SIZE), ((GRID_WIDTH // 2 - 1) * TILE_SIZE, (GRID_HEIGHT // 2) * TILE_SIZE)]  
    assert handler.last_input == 'w'

def test_move(handler):
    snake = handler.snake.copy()
    handler.last_input = 'w'
    handler.move_snake()
    assert handler.snake == [(snake[0][0], snake[0][1] - TILE_SIZE), snake[0]]

def test_move_cross_boundaries(handler):
    handler.snake = [(WINDOW_WIDTH//2,WINDOW_HEIGHT), (WINDOW_WIDTH//2,WINDOW_HEIGHT - TILE_SIZE)]
    handler.last_input = 's'
    handler.move_snake()
    assert handler.snake == [(WINDOW_WIDTH//2,0), (WINDOW_WIDTH//2,WINDOW_HEIGHT)]
    
    
def test_snake_growth(handler):
    handler.snake = [(WINDOW_WIDTH//2,WINDOW_HEIGHT//2), (WINDOW_WIDTH//2 - TILE_SIZE,WINDOW_HEIGHT//2)]
    handler.fruit = (WINDOW_WIDTH//2 + TILE_SIZE,WINDOW_HEIGHT//2)
    len_before = len(handler.snake)
    handler.last_input = 'd'
    handler.move_snake()
    assert len(handler.snake) == len_before + 1

def test_game_over(handler):
    handler.snake = [(WINDOW_WIDTH//2,WINDOW_HEIGHT//2), (WINDOW_WIDTH//2 - TILE_SIZE,WINDOW_HEIGHT//2),(WINDOW_WIDTH//2 - 2*TILE_SIZE,WINDOW_HEIGHT//2)]
    handler.last_input = 'a'
    handler.move_snake()
    handler.check_game_over()
    assert len(handler.snake) != len(set(handler.snake)) # check for duplicates in snake body
