import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, controls):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE
        self.speed = 3
        self.controls = controls  # dict avec les touches

    def update(self, collision_grid):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[self.controls['up']]:    dy = -self.speed
        if keys[self.controls['down']]:  dy =  self.speed
        if keys[self.controls['left']]:  dx = -self.speed
        if keys[self.controls['right']]: dx =  self.speed

        # Déplacement avec collision
        self.rect.x += dx
        if self._check_collision(collision_grid):
            self.rect.x -= dx

        self.rect.y += dy
        if self._check_collision(collision_grid):
            self.rect.y -= dy

    def _check_collision(self, collision_grid):
        # Vérifie les 4 coins du joueur
        corners = [
            (self.rect.left,  self.rect.top),
            (self.rect.right - 1, self.rect.top),
            (self.rect.left,  self.rect.bottom - 1),
            (self.rect.right - 1, self.rect.bottom - 1),
        ]
        for cx, cy in corners:
            tx = cx // TILE_SIZE
            ty = cy // TILE_SIZE
            if ty < 0 or ty >= len(collision_grid): continue
            if tx < 0 or tx >= len(collision_grid[0]): continue
            if collision_grid[ty][tx] == 1:
                return True
        return False

    def get_tile_pos(self):
        """Retourne la position en tiles (pour A*)."""
        return (self.rect.centerx // TILE_SIZE,
                self.rect.centery // TILE_SIZE)