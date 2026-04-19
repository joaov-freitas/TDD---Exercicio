from snake import io_handler
import pytest

@pytest.fixture
def handler():
    return io_handler((10,15), 0.5)

def test_initialization(handler):
    assert handler.x_size == 10
    assert handler.y_size == 15
    assert handler.game_speed == 0.5
    assert handler.last_input == 'w'
