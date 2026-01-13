import pygame
import random

pygame.init()

size = (1920, 1080)
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Salle 1 - obstacles simples")

#fond
image_fond = pygame.image.load("salle2/fond.png")
image_fond = pygame.transform.scale(image_fond, size)

#joueurs

#joueur 1
image_j1 = pygame.image.load("salle2/personnage1v2.png")
image_j1 = pygame.transform.scale(image_j1, (100, 100))
class Joueur1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3

    def draw(self, screen):
        screen.blit(image_j1, (self.x, self.y))
    
    def move(self, touches, obstacles):
        old_x, old_y = self.x, self.y
        if touches[pygame.K_UP]:
            self.y -= self.speed
        if touches[pygame.K_DOWN]:
            self.y += self.speed
        if touches[pygame.K_LEFT]:
            self.x -= self.speed
        if touches[pygame.K_RIGHT]:
            self.x += self.speed
        
        self.x = max(100, min(self.x, size[0]-100))
        self.y = max(100, min(self.y, size[1]-100))
        
        player_rect = pygame.Rect(self.x, self.y, 100, 100)
        
        if touches[pygame.K_e]:
            if player_rect.colliderect(buttons[5].rect):
                return 1
            if player_rect.colliderect(buttons[6].rect):
                return 2
            if player_rect.colliderect(buttons[7].rect):
                return 3
            if player_rect.colliderect(buttons[8].rect):
                return 4
                

        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.x = old_x
                self.y = old_y
                break        

jouer1 = Joueur1(300, 700)

#joueur 2
image_j2 = pygame.image.load("salle2/personnage2v2.png")
image_j2 = pygame.transform.scale(image_j2, (100, 100))
class Joueur2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3

    def draw(self, screen):
        screen.blit(image_j2, (self.x, self.y))
    
    def move(self, touches, obstacles):
        old_x = self.x
        old_y = self.y
        if touches[pygame.K_z]:
            self.y -= self.speed
        if touches[pygame.K_s]:
            self.y += self.speed
        if touches[pygame.K_q]:
            self.x -= self.speed
        if touches[pygame.K_d]:
            self.x += self.speed
        
        self.x = max(100, min(self.x, size[0]-100))
        self.y = max(100, min(self.y, size[1]-100))
        
        player_rect = pygame.Rect(self.x, self.y, 100, 100)
        
        if touches[pygame.K_e]:
            if player_rect.colliderect(buttons[0].rect) and len(obstacles) > 3:
                obstacles.remove(obstacles[3])
            if player_rect.colliderect(buttons[1].rect):
                return 1
            if player_rect.colliderect(buttons[2].rect):
                return 2
            if player_rect.colliderect(buttons[3].rect):
                return 3
            if player_rect.colliderect(buttons[4].rect):
                return 4
                
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle.rect):
                self.x = old_x
                self.y = old_y
                break

jouer2 = Joueur2(300, 400)

class Obstacle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 50, 50), self.rect)

obstacles = [
    Obstacle(300, 300, 200, 50),
    Obstacle(300, 600, 200, 50),
    Obstacle(300, 900, 200, 50),
    Obstacle(500, 600, 50, 350),
]

class bouton:
    def __init__(self, x, y, width, height, texte="E"):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (50, 50, 200)
        self.texte = texte
        self.font = pygame.font.Font(None, 34)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        txt = self.font.render(self.texte, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rect.center))
    
    
buttons = [
    bouton(500, 450, 70, 70, "E"),
    bouton(620, 450, 70, 70, "1"),
    bouton(620, 500, 70, 70, "2"),
    bouton(700, 450, 70, 70, "3"),
    bouton(700, 500, 70, 70, "4"),
    bouton(620, 700, 70, 70, "1"),
    bouton(620, 750, 70, 70, "2"),
    bouton(700, 700, 70, 70, "3"),
    bouton(700, 750, 70, 70, "4"),  
]

sequence = []
gsequence = [4, 2]
horloge = pygame.time.Clock()

running = True

while running:
    screen.blit(image_fond, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Déplacement joueur 1
    touches = pygame.key.get_pressed()
    jouer1.move(touches, obstacles)

    # Déplacement joueur 2
    jouer2.move(touches, obstacles)

    for obstacle in obstacles:
        obstacle.draw(screen)

    for button in buttons:
        button.draw(screen)

    if obstacles[3] != Obstacle(500, 600, 50, 350):
        texte_reussi = pygame.font.Font(None, 34).render("code : 42", True, (255, 255, 255))
        rect = texte_reussi.get_rect(center=(600, 400)) 
        screen.blit(texte_reussi, rect)
    
    if jouer1.move(touches, obstacles) == jouer2.move(touches, obstacles) == 4:
        sequence.append(4)
    
    if jouer1.move(touches, obstacles) == jouer2.move(touches, obstacles) == 2:
        sequence.append(2)
    
    if sequence == gsequence:
        texte_reussi = pygame.font.Font(None, 50).render("Puzzle réussi !", True, (255, 255, 255))
        rect = texte_reussi.get_rect(center=(size[0]//2, size[1]//2)) 
        screen.blit(texte_reussi, rect)


    jouer1.draw(screen)
    jouer2.draw(screen)

    pygame.display.flip() # Met à jour l'affichage
    horloge.tick(60)