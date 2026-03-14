import pygame
from settings import *
from player import Player
from enemy import Enemy

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

GRID_COLS = 25
GRID_ROWS = 15

collision_grid = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,0,1],
    [1,0,0,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1,1,1,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Position de la porte (tile x=23, y=7)
DOOR_TILE = (23, 7)
door_rect = pygame.Rect(
    DOOR_TILE[0] * TILE_SIZE,
    DOOR_TILE[1] * TILE_SIZE,
    TILE_SIZE, TILE_SIZE
)

def draw_grid(surface):
    for y in range(GRID_ROWS):
        for x in range(GRID_COLS):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if collision_grid[y][x] == 1:
                pygame.draw.rect(surface, GREY, rect)
            else:
                pygame.draw.rect(surface, (40, 40, 40), rect)
            pygame.draw.rect(surface, (60, 60, 60), rect, 1)
    # Porte en jaune
    pygame.draw.rect(surface, YELLOW, door_rect)
    font = pygame.font.SysFont(None, 20)
    txt = font.render("EXIT", True, BLACK)
    surface.blit(txt, (door_rect.x + 2, door_rect.y + 8))

def check_door(player, reached_set, player_id):
    tx = player.rect.centerx // TILE_SIZE
    ty = player.rect.centery // TILE_SIZE
    if (tx, ty) == DOOR_TILE:
        reached_set.add(player_id)

def draw_ui(surface, p1_done, p2_done):
    font = pygame.font.SysFont(None, 28)
    p1_txt = font.render(f"P1: {'✓ Sorti !' if p1_done else 'En jeu'}", True, BLUE)
    p2_txt = font.render(f"P2: {'✓ Sorti !' if p2_done else 'En jeu'}", True, GREEN)
    surface.blit(p1_txt, (10, 10))
    surface.blit(p2_txt, (10, 35))

# Joueurs — partent tous les 2 à gauche
controls_p1 = {
    'up': pygame.K_z, 'down': pygame.K_s,
    'left': pygame.K_q, 'right': pygame.K_d,
}
controls_p2 = {
    'up': pygame.K_UP, 'down': pygame.K_DOWN,
    'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
}

player1 = Player(2, 6, BLUE,  controls_p1)
player2 = Player(2, 8, GREEN, controls_p2)

# Ennemis
patrol1 = [(5, 7),  (12, 7), (12, 2), (5, 2)]
patrol2 = [(15, 7), (22, 7), (22, 12), (15, 12)]
enemy1  = Enemy(5,  7, patrol1)
enemy2  = Enemy(15, 7, patrol2)

all_sprites = pygame.sprite.Group(player1, player2, enemy1, enemy2)

reached = set()
game_over = False
font_big = pygame.font.SysFont(None, 64)

running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            # Restart avec R
            if event.key == pygame.K_r and game_over:
                player1.rect.x = 2 * TILE_SIZE
                player1.rect.y = 6 * TILE_SIZE
                player2.rect.x = 2 * TILE_SIZE
                player2.rect.y = 8 * TILE_SIZE
                reached.clear()
                game_over = False

    if not game_over:
        player1.update(collision_grid)
        player2.update(collision_grid)
        enemy1.update(collision_grid, [player1, player2])
        enemy2.update(collision_grid, [player1, player2])

        check_door(player1, reached, 1)
        check_door(player2, reached, 2)

        if 1 in reached and 2 in reached:
            game_over = True

    # Affichage
    draw_grid(screen)
    for sprite in all_sprites:
        screen.blit(sprite.image, sprite.rect)

    draw_ui(screen, 1 in reached, 2 in reached)

    if game_over:
        txt = font_big.render("VICTOIRE ! (R pour rejouer)", True, YELLOW)
        screen.blit(txt, (SCREEN_WIDTH // 2 - txt.get_width() // 2,
                          SCREEN_HEIGHT // 2 - txt.get_height() // 2))

    pygame.display.flip()

pygame.quit()