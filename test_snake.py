from snake_ref import io_handler
import pytest

@pytest.fixture
def handler():
    return io_handler((10,15), 0.5)

def test_initialization(handler):
    assert handler.x_size == 10
    assert handler.y_size == 15
    assert handler.game_speed == 0.5
    assert handler.last_input == 'w'

def test_move(handler):
    handler.snake = [(5,5)]
    handler.last_input = 'w'
    handler.move_snake()
    assert handler.snake == [(5,4)]

def test_move_cross_boundaries(handler):
    handler.snake = [(handler.x_size,handler.y_size)]
    handler.last_input = 's'
    handler.move_snake()
    assert handler.snake == [(handler.x_size,0)]
    handler.last_input = 'd'
    handler.move_snake()
    assert handler.snake == [(0,0)]
    
