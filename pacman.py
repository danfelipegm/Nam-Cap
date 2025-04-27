import pygame
import random
import math
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("nombre del juego ")

# Colores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
SCARED_COLOR = (100, 100, 255)

# Mapa (1 = pared, 0 = camino, 2 = punto pequeño, 3 = power-up)
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
    [1,3,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,1,1],
    [3,0,0,1,2,1,2,2,2,2,2,2,2,2,1,2,1,0,0,3],
    [1,1,1,1,2,1,2,1,1,0,0,1,1,2,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,1,0,0,0,0,1,2,2,2,2,2,2,1],
    [1,1,1,1,2,1,2,1,1,1,1,1,1,2,1,2,1,1,1,1],
    [1,2,2,2,2,1,2,2,2,0,0,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,0,0,1,2,1,2,1,2,1,1,1],
    [1,2,2,2,2,1,2,2,2,0,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,1,1,1,1,2,0,1,2,1,1,1,0,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Tamaño de cada celda del mapa
CELL_SIZE = 30

class Player:
    def __init__(self):
        self.velocidad = 1.0  # Velocidad inicial
        self.x = 0
        self.x = 14 * CELL_SIZE
        self.y = 17 * CELL_SIZE
        self.radius = 12
        self.speed = 2
        self.direction = "left"
        self.next_direction = "left"

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)

    def reset_position(self):
        self.x = 14 * CELL_SIZE
        self.y = 17 * CELL_SIZE
        self.direction = "left"
        self.next_direction = "left"

    def move(self):
        if self.can_move(self.next_direction):
            self.direction = self.next_direction

        if self.can_move(self.direction):
            if self.direction == "up":
                self.y -= self.speed
            elif self.direction == "down":
                self.y += self.speed
            elif self.direction == "left":
                self.x -= self.speed
            elif self.direction == "right":
                self.x += self.speed

    def can_move(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dy = -self.speed
        elif direction == "down":
            dy = self.speed
        elif direction == "left":
            dx = -self.speed
        elif direction == "right":
            dx = self.speed

        new_x = self.x + dx
        new_y = self.y + dy

        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)

        if 0 <= row < len(MAP) and 0 <= col < len(MAP[0]):
            return MAP[row][col] != 1
        return False
    
    def mover(self):
        self.x += self.velocidad

class Ghost:
    def __init__(self, color, col, row):
        self.velocidad = 1.0
        self.x = 0
        self.color = color
        self.x = col * CELL_SIZE
        self.y = row * CELL_SIZE
        self.radius = 12
        self.speed = 2
        self.direction = random.choice(["up", "down", "left", "right"])
        self.scared = False
        self.scared_time = 0

    def draw(self):
        color = SCARED_COLOR if self.scared else self.color
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def reset_position(self):
        self.x = 14 * CELL_SIZE
        self.y = 11 * CELL_SIZE
        self.direction = random.choice(["up", "down", "left", "right"])
        self.scared = False
        self.scared_time = 0

    def can_move(self, direction):
        dx, dy = 0, 0
        if direction == "up":
            dy = -self.speed
        elif direction == "down":
            dy = self.speed
        elif direction == "left":
            dx = -self.speed
        elif direction == "right":
            dx = self.speed

        new_x = self.x + dx
        new_y = self.y + dy

        col = int(new_x // CELL_SIZE)
        row = int(new_y // CELL_SIZE)

        if 0 <= row < len(MAP) and 0 <= col < len(MAP[0]):
            return MAP[row][col] != 1
        return False

    def move(self, player):
        if self.scared:
            self.scared_time -= 1
            if self.scared_time <= 0:
                self.scared = False

        directions = ["up", "down", "left", "right"]
        best_direction = None
        best_distance = None

        for direction in directions:
            if self.can_move(direction):
                dx, dy = 0, 0
                if direction == "up":
                    dy = -self.speed
                elif direction == "down":
                    dy = self.speed
                elif direction == "left":
                    dx = -self.speed
                elif direction == "right":
                    dx = self.speed

                new_x = self.x + dx
                new_y = self.y + dy

                # Distancia al jugador
                distance = ((player.x - new_x) ** 2 + (player.y - new_y) ** 2) ** 0.5

                if best_distance is None:
                    best_distance = distance
                    best_direction = direction
                else:
                    if self.scared:
                        if distance > best_distance:
                            best_distance = distance
                            best_direction = direction
                    else:
                        if distance < best_distance:
                            best_distance = distance
                            best_direction = direction

        if best_direction:
            self.direction = best_direction

        dx, dy = 0, 0
        if self.direction == "up":
            dy = -self.speed
        elif self.direction == "down":
            dy = self.speed
        elif self.direction == "left":
            dx = -self.speed
        elif self.direction == "right":
            dx = self.speed

        self.x += dx
        self.y += dy

    def mover(self):
        self.x += self.velocidad

class Game:
    def __init__(self):
        self.player = Player()
        self.ghosts = [
            Ghost(RED, 9, 7),
            Ghost(PINK, 10, 7),
            Ghost(CYAN, 9, 8),
        ]
        self.running = True
        self.clock = pygame.time.Clock()
        self.score = 0
        self.lives = 3
        self.font = pygame.font.SysFont(None, 30)

    def draw_map(self):
        for row_index, row in enumerate(MAP):
            for col_index, cell in enumerate(row):
                x = col_index * CELL_SIZE
                y = row_index * CELL_SIZE
                if cell == 1:
                    pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                elif cell == 2:
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 3)
                elif cell == 3:
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 6)

    def draw_ui(self):
        score_text = self.font.render(f"Puntos: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Vidas: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))
        screen.blit(lives_text, (WIDTH - 100, HEIGHT - 40))

    def check_collisions(self):
        col = max(0, min(int(self.player.x // CELL_SIZE), len(MAP[0]) - 1))
        row = max(0, min(int(self.player.y // CELL_SIZE), len(MAP) - 1))

        if MAP[row][col] == 2:
            MAP[row][col] = 0
            self.score += 10
        elif MAP[row][col] == 3:
            MAP[row][col] = 0
            self.score += 50
            for ghost in self.ghosts:
                ghost.scared = True
                ghost.scared_time = 300

        for ghost in self.ghosts:
            distance = math.hypot(self.player.x - ghost.x, self.player.y - ghost.y)
            if distance < self.player.radius + ghost.radius:
                if ghost.scared:
                    ghost.reset_position()
                    self.score += 200
                else:
                    self.lives -= 1
                    self.player.reset_position()
                    if self.lives <= 0:
                        self.running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.next_direction = "up"
                elif event.key == pygame.K_DOWN:
                    self.player.next_direction = "down"
                elif event.key == pygame.K_LEFT:
                    self.player.next_direction = "left"
                elif event.key == pygame.K_RIGHT:
                    self.player.next_direction = "right"

    def update(self):
        self.player.move()
        for ghost in self.ghosts:
            ghost.move(self.player)
        self.check_collisions()

    def draw(self):
        screen.fill(BLACK)
        self.draw_map()
        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()
        self.draw_ui()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def calcular_derivada(self, puntuacion, tiempo_actual):
        delta_puntos = puntuacion - self.puntuacion_anterior
        delta_tiempo = tiempo_actual - self.tiempo_anterior
        if delta_tiempo > 0:
            derivada = delta_puntos / delta_tiempo
        else:
            derivada = 0
        
        # Guardamos los valores actuales para el próximo cálculo
        self.puntuacion_anterior = puntuacion
        self.tiempo_anterior = tiempo_actual
        return derivada

    def calcular_velocidad(self, puntuacion, tiempo_actual):
        derivada = self.calcular_derivada(puntuacion, tiempo_actual)
        velocidad_base = 1.0
        velocidad_maxima = 5.0
        velocidad = velocidad_base + (derivada * 0.1)
        return min(velocidad, velocidad_maxima)
    
    def actualizar(self):
        
        self.puntuacion += 10  
        tiempo_actual = pygame.time.get_ticks() / 1000  
        nueva_velocidad = self.calcular_velocidad(self.puntuacion, tiempo_actual)
        
        self.jugador.velocidad = nueva_velocidad
        for fantasma in self.fantasmas:
            fantasma.velocidad = nueva_velocidad

    

# Ejecutar el juego
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit()