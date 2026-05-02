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

def test_snake_growth(handler):
    handler.snake = [(WINDOW_WIDTH//2,WINDOW_HEIGHT//2), (WINDOW_WIDTH//2 - TILE_SIZE,WINDOW_HEIGHT//2)]
    handler.fruit = [(WINDOW_WIDTH//2 + TILE_SIZE,WINDOW_HEIGHT//2)]
    len_before = len(handler.snake)
    handler.last_input = 'd'
    handler.move_snake()
    assert len(handler.snake) == len_before + 1
    # verifica também que a cabeça foi para a posição da fruta
    assert handler.snake[0] == (WINDOW_WIDTH//2 + TILE_SIZE, WINDOW_HEIGHT//2)

def test_game_over(handler):
    handler.snake = [
        (WINDOW_WIDTH//2, WINDOW_HEIGHT//2),
        (WINDOW_WIDTH//2 - TILE_SIZE, WINDOW_HEIGHT//2),
        (WINDOW_WIDTH//2 - 2 * TILE_SIZE, WINDOW_HEIGHT//2),
    ]
    handler.last_input = 'a'
    handler.move_snake()
    handler.check_game_over()
    assert len(handler.snake) != len(set(handler.snake))  # verifica posições duplicadas
    assert handler.last_input == 'end'


@pytest.mark.parametrize("start,dir,expected", [
    ([(WINDOW_WIDTH//2, WINDOW_HEIGHT), (WINDOW_WIDTH//2, WINDOW_HEIGHT - TILE_SIZE)], 's', [(WINDOW_WIDTH//2, 0), (WINDOW_WIDTH//2, WINDOW_HEIGHT)]),
    
    ([(WINDOW_WIDTH, WINDOW_HEIGHT//2), (WINDOW_WIDTH - TILE_SIZE, WINDOW_HEIGHT//2)], 'd', [(0, WINDOW_HEIGHT//2), (WINDOW_WIDTH, WINDOW_HEIGHT//2)]),
])
def test_wrap_both_axes(handler, start, dir, expected):
    handler.snake = start
    handler.last_input = dir
    handler.move_snake()
    assert handler.snake == expected


def test_fruit_generation(handler):
    # configura um corpo pequeno e gera várias frutas
    handler.snake = [(0, 0), (TILE_SIZE, 0), (2 * TILE_SIZE, 0)]
    for _ in range(10):
        handler.gerar_nova_fruta()
        # todas as frutas devem estar alinhadas e não sobrepor o corpo
        assert all(x % TILE_SIZE == 0 and y % TILE_SIZE == 0 for x, y in handler.fruit)
        assert all(f not in handler.snake for f in handler.fruit)


def test_prevent_reverse_direction(handler):
    handler.last_input = 'w'
    handler.change_direction('s')
    assert handler.last_input == 'w'


def test_get_sprite_returns_enum(handler):
    from snake import SpriteDirection
    val = handler.get_sprite(0)
    assert isinstance(val, SpriteDirection)

