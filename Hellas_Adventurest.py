import pygame
import csv

# Arxikopoiisi pygame kai othoni
pygame.init()
screen_width, screen_height = 800, 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Hellas Adventures')

# Fortosi dedomenon epipedou
def load_level_data(level):
    world_data = []
    with open(f'level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row_data = [int(tile) for tile in row]
            world_data.append(row_data)
    return world_data

# Klasi gia ton kosmo
class World:
    def __init__(self, male_selected=True):
        self.male_selected = male_selected
        self.tiles = []

    def process_data(self, data):
        player = None
        health_bar = None
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile == 1:
                    self.tiles.append((x, y))
                elif tile == 2:
                    player = Player(x, y)
                elif tile == 3:
                    health_bar = HealthBar(x, y)
        return player, health_bar

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.jump = False
        self.alive = True

    def update(self):
        if self.jump:
            # Logiki gia to salto tou paikti
            pass

class HealthBar:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 100, 20)

# Epanafora epipedou
def reset_level():
    return [[0] * (screen_width // 50) for _ in range(screen_height // 50)]

# Arxikopoiisi tou paixnidiou
level = 1
MAX_LEVELS = 3
bg_scroll = 0
progress = False
moving_left = moving_right = attack = False

world_data = load_level_data(level)
world = World(male_selected=True)
player, health_bar = world.process_data(world_data)

# Vasikos broxos tou paixnidiou
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                attack = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                # jump_fx.play() # Afaireitai i anafora giati den exoume tin metabliti jump_fx
            if event.key == pygame.K_ESCAPE:
                menu_active = True
            if event.key == pygame.K_e:
                progress = True
            if event.key == pygame.K_q:
                end_game = True
            if event.key == pygame.K_m:
                muted_index = (muted_index + 1) % 2  # Enallagi metavlitis siopis

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                attack = False

    if progress:
        if level <= MAX_LEVELS:
            level += 1
            if level <= MAX_LEVELS:
                world_data = load_level_data(level)
                world = World(male_selected=True)
                player, health_bar = world.process_data(world_data)
            progress = False

    # Ananeosi tou paikti kai tou kosmou
    player.update()
    
    # Emfanisi tou kosmou
    screen.fill((0, 0, 0))  # Katharismos tis othonis
    for tile in world.tiles:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(tile[0]*50, tile[1]*50, 50, 50))
    
    # Emfanisi tou paikti kai tou health bar
    pygame.draw.rect(screen, (0, 0, 255), player.rect)
    pygame.draw.rect(screen, (255, 0, 0), health_bar.rect)

    pygame.display.update()

pygame.quit()
