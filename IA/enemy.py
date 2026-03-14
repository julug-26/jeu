import pygame
from settings import *
from pathfinding import astar

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_points):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILE_SIZE
        self.rect.y = y * TILE_SIZE

        self.speed          = 2
        self.detection_range = 8   # en tiles
        self.attack_range    = 1   # en tiles
        self.patrol_points   = patrol_points
        self.patrol_index    = 0

        self.path           = []
        self.path_timer     = 0
        self.path_delay     = 30   # recalcule A* toutes les 30 frames
        self.state          = "patrol"  # "patrol" ou "chase"

    def get_tile_pos(self):
        return (self.rect.centerx // TILE_SIZE,
                self.rect.centery // TILE_SIZE)

    def _distance_to(self, tile_pos):
        my = self.get_tile_pos()
        return abs(my[0] - tile_pos[0]) + abs(my[1] - tile_pos[1])

    def _nearest_player(self, players):
        return min(players, key=lambda p: self._distance_to(p.get_tile_pos()))

    def update(self, collision_grid, players):
        nearest = self._nearest_player(players)
        dist    = self._distance_to(nearest.get_tile_pos())

        # --- Machine à états ---
        if dist <= self.detection_range:
            self.state = "chase"
        else:
            self.state = "patrol"

        # Recalcule le chemin périodiquement
        self.path_timer += 1
        if self.path_timer >= self.path_delay or not self.path:
            self.path_timer = 0
            if self.state == "chase":
                self.path = astar(collision_grid,
                                  self.get_tile_pos(),
                                  nearest.get_tile_pos())
            else:
                target = self.patrol_points[self.patrol_index]
                self.path = astar(collision_grid,
                                  self.get_tile_pos(),
                                  target)

        # Avance vers la prochaine tile du chemin
        if self.path:
            next_tile = self.path[0]
            target_x  = next_tile[0] * TILE_SIZE + TILE_SIZE // 2
            target_y  = next_tile[1] * TILE_SIZE + TILE_SIZE // 2

            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            dist_px = max(1, (dx**2 + dy**2) ** 0.5)

            self.rect.x += int(self.speed * dx / dist_px)
            self.rect.y += int(self.speed * dy / dist_px)

            # Si on est arrivé à la tile suivante, on la retire du chemin
            if abs(self.rect.centerx - target_x) < self.speed + 1 and \
               abs(self.rect.centery - target_y) < self.speed + 1:
                self.path.pop(0)
                # En patrol, passe au point suivant si arrivé
                if self.state == "patrol" and not self.path:
                    self.patrol_index = (self.patrol_index + 1) % len(self.patrol_points)

        # Change couleur selon l'état
        if self.state == "chase":
            self.image.fill((255, 50, 50))   # Rouge vif
        else:
            self.image.fill((200, 100, 50))  # Orange