import pygame
import sys

pygame.init()

fond = pygame.image.load("salle2/fond.png")
font = pygame.font.Font(None, 24)
instructions_j1 = "Joueur 1: E pour interagir"
instructions_j2 = "Joueur 2: R pour interagir"


#sizes = pygame.display.get_desktop_sizes()
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Salle 2 - Le puzzle des statues")
fond = pygame.transform.scale(fond, size)


#inisialisation des joueurs

#positions
personnage1_pos = [100, 100]
personnage2_pos = [300, 100]
#tailles
personnage1_size = (50, 50)
personnage2_size = (50, 50)
#couleurs
personnage1_color = (0, 128, 255)
personnage2_color = (255, 100, 100)
#vitesses
personnage1_speed = 2
personnage2_speed = 2
#mur
mur_j1 = pygame.Rect(0, 0, 60, size[1]) #mur gauche
mur_j2 = pygame.Rect(size[0]-60, 0, 60, size[1]) #mur droit

# Texte mur
texte_mur_j1 = [
    "Le Soleil ne ment jamais.",
    "La Racine se souvient du premier serment.",
    "Le Cristal trahit toujours son porteur."
]

texte_mur_j2 = [
    "Celui qui touche la Lune devra mentir.",
    "La Racine n’a jamais vu la lumiere.",
    "Le Soleil n’a pas ete le premier."
]

# Taille des statues
statue_size = (50, 50)

# Centre de la salle
cx, cy = size[0]//2, size[1]//2
r = 100  # rayon pour espacer les statues

# Création des 4 statues autour du centre
statues = [
    {"nom": "Soleil", "pos": [cx + r, cy], "color": (255, 255, 0), "a": False},      # jaune
    {"nom": "Lune", "pos": [cx - r, cy], "color": (200, 200, 255), "a": False},      # bleu clair
    {"nom": "Racine", "pos": [cx, cy - r], "color": (100, 50, 0), "a": False},       # marron
    {"nom": "Cristal", "pos": [cx, cy + r], "color": (0, 255, 255), "a": False},     # cyan
]

# Ordre correct pour le puzzle
ordre_correct = ["Racine", "Soleil", "Lune"]

# Liste pour stocker les activations
activations = []

# Positions de départ
depart_j1 = [100, 100]
depart_j2 = [300, 100]

personnage1_pos = depart_j1.copy()
personnage2_pos = depart_j2.copy()

puzzle_reussi = False
statues1 = False
statues2 = False

text_niveau2_reussi = "Niveau 2 réussi !"
font_niveau2 = pygame.font.Font(None, 68)
porte = pygame.Rect(size[0]//2 - 40, size[1] - 80, 80, 60)
clock = pygame.time.Clock()

def est_sur_statue(player_pos, player_size, statue_pos, statue_size):
    px, py = player_pos
    pw, ph = player_size
    sx, sy = statue_pos
    sw, sh = statue_size

    # Vérifie si les rectangles se chevauchent
    if (px + pw > sx and px < sx + sw) and (py + ph > sy and py < sy + sh):
        return True
    return False

def reset_puzzle():
    global activations, personnage1_pos, personnage2_pos, puzzle_reussi
    print("Mauvaise statue ! Reset !")
    activations = []
    puzzle_reussi = False
    personnage1_pos = depart_j1.copy()
    personnage2_pos = depart_j2.copy()
    

    for s in statues:
        s["a"] = False

def est_sur_mur(player_pos, player_size, mur):
    joueur_rect = pygame.Rect(player_pos, player_size)
    return joueur_rect.colliderect(mur)


running = True
while running:
    screen.blit(fond, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if statues1 and statues2:
                # Joueur 1 interagit avec E
                if event.key == pygame.K_e:
                    for s in statues:
                        if est_sur_statue(personnage1_pos, personnage1_size, s["pos"], statue_size):
                            prinssst(f"Joueur 1 a activé {s['nom']} !")
                            activations.append(s["nom"])
                            # Vérification
                            if activations[-1] != ordre_correct[len(activations)-1]:
                                reset_puzzle()
                            else:
                                s["a"] = True
                                if len(activations) == len(ordre_correct):
                                    print("Puzzle réussi !")
                                    puzzle_reussi = True
                # Joueur 2 interagit avec R
                if event.key == pygame.K_r:
                    for s in statues:
                        if est_sur_statue(personnage2_pos, personnage2_size, s["pos"], statue_size):
                            print(f"Joueur 2 a activé {s['nom']} !")
                            activations.append(s["nom"])
                            # Vérification
                            if activations[-1] != ordre_correct[len(activations)-1]:
                                reset_puzzle()
                            else:
                                s["a"] = True
                                if len(activations) == len(ordre_correct):
                                    print("Puzzle réussi !")
                                    puzzle_reussi = True

    if puzzle_reussi:
        texte_reussi = font_niveau2.render(text_niveau2_reussi, True, (255, 255, 255))
        rect = texte_reussi.get_rect(center=(size[0]//2, size[1]//2)) 
        screen.blit(texte_reussi, rect)
        pygame.draw.rect(screen, (50, 200, 50), porte) 

    
    
    if statues1 and statues2 and not puzzle_reussi:
        # Dessiner les statues (avec couleur dynamique)
        for s in statues:
            if s["a"]:
                color = (100, 255, 100)  # vert = activée
            else:
                color = s["color"]
            pygame.draw.rect(screen, color, (*s["pos"], *statue_size))
    
    if not puzzle_reussi:
        keys = pygame.key.get_pressed() #detecte les touches appuyees

        # Déplacement joueur 1
        if keys[pygame.K_z]:  # haut
            personnage1_pos[1] -= personnage1_speed
        if keys[pygame.K_s]:  # bas
            personnage1_pos[1] += personnage1_speed
        if keys[pygame.K_q]:  # gauche
            personnage1_pos[0] -= personnage1_speed
        if keys[pygame.K_d]:  # droite
            personnage1_pos[0] += personnage1_speed

        # Déplacement joueur 2
        if keys[pygame.K_UP]:
            personnage2_pos[1] -= personnage2_speed
        if keys[pygame.K_DOWN]:
            personnage2_pos[1] += personnage2_speed
        if keys[pygame.K_LEFT]:
            personnage2_pos[0] -= personnage2_speed
        if keys[pygame.K_RIGHT]:
            personnage2_pos[0] += personnage2_speed
        # Dessiner les joueurs
        pygame.draw.rect(screen, personnage1_color, (*personnage1_pos, *personnage1_size))
        pygame.draw.rect(screen, personnage2_color, (*personnage2_pos, *personnage2_size))
        mur1 = est_sur_mur(personnage1_pos, personnage1_size, mur_j1)
        mur2 = est_sur_mur(personnage2_pos, personnage2_size, mur_j2)
    
        if mur2:
            y = 100
            for ligne in texte_mur_j2:
                txt = font.render(ligne, True, (255, 255, 255))
                screen.blit(txt, (size[0] - 380, y))
                y += 25
            statues1 = True
        if mur1:
            y = 100
            for ligne in texte_mur_j1:
                txt = font.render(ligne, True, (255, 255, 255))
                screen.blit(txt, (70, y))
                y += 25
            statues2 = True

    #limites les positions des jouers aux bords de l'ecran
    personnage1_pos[0] = max(0, min(personnage1_pos[0], size[0]-personnage1_size[0]))
    personnage1_pos[1] = max(0, min(personnage1_pos[1], size[1]-personnage1_size[1]))
    personnage2_pos[0] = max(0, min(personnage2_pos[0], size[0]-personnage2_size[0]))
    personnage2_pos[1] = max(0, min(personnage2_pos[1], size[1]-personnage2_size[1]))
    
    
    # Affichage des instructions
    texte_j1 = font.render(instructions_j1, True, (255, 255, 255))
    texte_j2 = font.render(instructions_j2, True, (255, 255, 255))

    screen.blit(texte_j1, (20, size[1] - 50))
    screen.blit(texte_j2, (20, size[1] - 25))

    # Actualiser l'affichage
    pygame.display.flip()
    clock.tick(60) # Limiter à 60 FPS


pygame.quit()
sys.exit()
