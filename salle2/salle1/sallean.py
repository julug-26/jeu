import pygame
import random

pygame.init()

size = (1920, 1080)
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Salle 1 - obstacles simples")

#joueurs

#joueur 1
image_j1 = pygame.image.load("salle2/personnage1v2.png")
class Joueur1:
    def init(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(image_j1, (self.x, self.y))

horloge = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    pygame.display.flip() # Met à jour l'affichage
    horloge.tick(60)