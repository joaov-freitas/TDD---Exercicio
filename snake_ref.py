import os
import keyboard
import time
import random


class io_handler:
    
    x_size: int
    y_size: int
    game_speed: float
    last_input: str
    matrix = []
    snake: list[tuple[int, int]]
    fruit: list[tuple[int, int]]

    def __init__(self, dim, speed):
        self.x_size = dim[0]
        self.y_size = dim[1]
        
        self.game_speed = speed
        self.last_input = 'w'

        self.snake = [(self.x_size//2, self.y_size//2)]
        self.fruit = [(random.randint(0,self.x_size),random.randint(0,self.y_size))]

        if self.fruit == self.snake[0]:
            self.gerar_nova_fruta()

        for i in range (self.y_size): 
            self.matrix.append([0]*self.x_size)

    def move_snake(self):
        if len(self.snake) == 0: 
            return
        
        hx, hy = self.snake[0] 

        if self.last_input == 'w':
            nova_cabeca = (hx, self.y_size - 1 if hy == 0 else hy - 1)
        elif self.last_input == 'a':
            nova_cabeca = (self.x_size - 1 if hx == 0 else hx - 1, hy)
        elif self.last_input == 's':
            nova_cabeca = (hx, 0 if hy == self.y_size - 1 else hy + 1)
        elif self.last_input == 'd':
            nova_cabeca = (0 if hx == self.x_size - 1 else hx + 1, hy)
        else:
            nova_cabeca = (hx, hy)

        self.snake.insert(0, nova_cabeca)

        if nova_cabeca in self.fruit:
            self.gerar_nova_fruta()
            self.fruit.remove(nova_cabeca)
        else:
            self.snake.pop()

    def gerar_nova_fruta(self):
        amount_fruits = (len(self.snake)//10) + 1
        for _ in range(amount_fruits):
            while len(self.fruit) <= amount_fruits:
                nova_fruta = (random.randint(0, self.x_size - 1), random.randint(0, self.y_size - 1))
            
                if nova_fruta not in self.snake:
                    self.fruit.append(nova_fruta)
                    break

    def check_game_over(self):
        head = self.snake[0]
        if head in self.snake[1:]:
            self.last_input = 'end'

    def record_inputs(self):
        keyboard.add_hotkey('w', lambda: setattr(self, "last_input", 'w'))
        keyboard.add_hotkey('a', lambda: setattr(self, "last_input", 'a'))
        keyboard.add_hotkey('s', lambda: setattr(self, "last_input", 's'))
        keyboard.add_hotkey('d', lambda: setattr(self, "last_input", 'd'))
        keyboard.add_hotkey('esc', lambda: setattr(self, "last_input", 'end'))

    def display(self):
        # Limpar a matriz
        for i in range(self.y_size):
            for j in range(self.x_size):
                self.matrix[i][j] = 0

        # Marca o corpo da cobra
        for i in range(1, len(self.snake)):
            x, y = self.snake[i]
            if 0 <= x < self.x_size and 0 <= y < self.y_size:
                self.matrix[y][x] = 1  # 1 = corpo
        
        # Marca a cabeça da cobra
        if len(self.snake) > 0:
            x, y = self.snake[0]
            if 0 <= x < self.x_size and 0 <= y < self.y_size:
                self.matrix[y][x] = 2  # 2 = cabeça
        
        # Marca a fruta
        for fruit in self.fruit:
            fx, fy = fruit
            if 0 <= fx < self.x_size and 0 <= fy < self.y_size:
                self.matrix[fy][fx] = 3  # 3 = fruta

        def display_h_line(self):
            print ('+', end='')
            print ('--'* len(self.matrix[0]), end='')
            print ('+')
        
        def display_content_line(line):
            print ('|', end='')
            for item in line: 
                if item == 1:
                    print ('[]', end='')
                elif item == 2:
                    print ('<>', end='')
                elif item == 3:
                    print ('()', end='')
                else:
                    print ('  ', end='')

            print ('|')

        os.system('cls' if os.name == 'nt' else 'clear')
        display_h_line(self)
        for line in self.matrix:
            display_content_line(line)
        display_h_line(self)

### exemplo do uso da classe io_handler  
instance = io_handler((10,15), 0.25)

def game_loop():
    instance.record_inputs()
    while True:
        instance.display()
        print("mova com WASD, saia com esc. Ultimo botão:", end=' ')
        ###adicione seu código para lidar com o jogo aqui
        instance.move_snake()
        instance.check_game_over()

        
        print(instance.last_input)
        print("Pontuação:", len(instance.snake))
        if(instance.last_input == 'end'):
            print("Game Over! A cobra colidiu consigo mesma.")
            exit()
        time.sleep(instance.game_speed)

if __name__ == '__main__':
    game_loop()