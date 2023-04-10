# Python Standard Library
import random as rd
from random import randint
from random import choices
import numpy as np
import copy as c
# Third-Party Libraries
import pygame as pg
from itertools import product

# Constants
# ------------------------------------------------------------------------------

X,Y = 30, 40 #taille de la fenêtre de jeu
W,H = 15,15 #taille de nos carrés élémentaires de jeu
DIRECTIONS = {
    "DOWN": (0, +1),
    "UP": (0, -1),
    "RIGHT": (+1, 0),
    "LEFT": (-1, 0),
}
FLOOR = (240, 240, 250)
WALL = (139,69,19)
PATH = (210,180,140)
count_gold = 0
rouge = ( 255, 0,0)
blue = (0, 0, 128)
life_point = 50
weapons_number = 0
villains = [(25,25),(25,26),(25,27),(26,25),(27,25)]
villains_killed = []

# Game state
# ------------------------------------------------------------------------------
player = (2,2)

# Helper functions
# ------------------------------------------------------------------------------

def quit(snake, reason):
    print(f"Game over ({reason}) with a score of {len(snake)}")
    pg.quit()
    exit()

def draw_path(départ,arrivée):
    if départ[0]==arrivée[0]:

        t=min(départ[1],arrivée[1])
        for k in range (abs(départ[1]-arrivée[1])):
            draw_tile(départ[0],t+k,PATH)

    if départ[1]==arrivée[1]:
        
        t=min(départ[0],arrivée[0])
        for k in range (abs(départ[0]-arrivée[0])):
            draw_tile(t+k,départ[1],PATH)

def draw_tile(x, y, color):
    """
    x and y in tiles coordinates
    translate into pixel coordinates for painting
    """
    rect = pg.Rect(x * W, y * H, W, H)
    pg.draw.rect(screen, color, rect)

walls = [
    ((1,1),8,8),((1,11),8,8),((1,21),8,8),
    ((11,1),8,8),((11,11),8,8),((11,21),8,8),
    ((21,1),8,8),((21,11),8,8),((21,21),8,8),
] #liste de tuple (coins HG,horizontal,vertical) les longueurs sont en unités de W*H

nombre_salles = 9
salles = []


for k in range(nombre_salles):
    d = dict()
    wall = walls[k]
    d['corner'] = wall[0]
    d['size'] = (wall[1],wall[2]) # horizontal, vertical
    corner = d['corner']
    size = d['size']
    d['doors'] = [(corner[0]+int(size[0]/2),corner[1]+size[1]-1),
                    (corner[0]+int(size[0]/2),corner[1]),
                    (corner[0],corner[1]+int(size[1]/2)),
                    (corner[0]+size[0]-1,corner[1]+int(size[1]/2))
                    ] # liste de tuples des positions des portes
    #if k >=1:
        #dict['neighbors'] = [salles[k-1]]
    salles.append(d)

DOORS = []
PATHS = []

for salle in salles:
    doors = salle['doors']
        
    for door in doors:
        DOORS.append(door)

            

    for (door_1,door_2) in product(DOORS,DOORS):
        x1,y1,x2,y2 = door_1[0],door_1[1],door_2[0],door_2[1]
        if (x1==x2 and abs(y2-y1)==3):
            PATHS.append(((x1,y1),(0,1),3))
            PATHS.append(((x1,y1),(0,-1),3))
        elif (y1==y2 and abs(x2-x1)==3):
            PATHS.append(((x1,y1),(1,0),3))
            PATHS.append(((x1,y1),(-1,0),3))

Case_path = []

for path in PATHS:
    (xp,yp), (dxp,dyp), lenght = path
    for k in range(lenght):
        Case_path.append((xp+dxp*k,yp+dyp*k)) 

def draw_background():
    screen.fill(FLOOR)

    for wall in walls:
        corner,largeur,longueur = wall[0],wall[1]-1,wall[2]-1
        for x in range(largeur+1):
            draw_tile(corner[0]+x,corner[1],WALL)
            draw_tile(corner[0]+x,corner[1]+longueur,WALL)

        for y in range(longueur):
            draw_tile(corner[0],corner[1]+y,WALL)
            draw_tile(corner[0]+largeur,corner[1]+y,WALL)
    
    
    for salle in salles:
        
        doors = salle['doors']
        
        for door in doors:
            if (door[0]>2 and door[0]<28 and door[1]>2 and door[1]<28):
                draw_tile(door[0],door[1],PATH)
        

    for (door_1,door_2) in product(DOORS,DOORS):
        x1,y1,x2,y2 = door_1[0],door_1[1],door_2[0],door_2[1]
        if (x1==x2 and abs(y2-y1)==3):
            draw_path(door_1,door_2)
            
        elif (y1==y2 and abs(x2-x1)==3):
            draw_path(door_1,door_2)

    for i in range(X):
        draw_tile(i,30,(0,0,0))
        
coord_rooms = [product([salle['corner'][0] + k for k in range(1, salle['size'][0]-1)], [salle['corner'][1] + l for l in range(1, salle['size'][1]-1)]) for salle in salles]
coords_vrac = []
for room in coord_rooms:
    coords_vrac += room

empty_cases = c.deepcopy(coords_vrac) 
nb = randint(1,4)
weapons = choices(empty_cases, k = nb)
for weapon in weapons:
    empty_cases.remove(weapon)

weapons_owned = []
paywall = 5

def move_player(player, direction):
    x, y = player
    dx, dy = direction
    if (x+dx, y+dy) in coords_vrac:
        '''if (x+dx, y+dy) == gold:
            count_gold += 1

            # if new_player in guards:
            #     if count_gold >= paywall:
            #         count_gold -= paywall
            #         new_player = x + dx, y + dy
            #     else:
            #         new_player = player'''
        new_player = x+dx, y+dy
            #gold = []

    elif (x+dx, y+dy) in Case_path:
        new_player = x+dx, y+dy

    elif (x+dx, y+dy) in DOORS:
        new_player = x+dx, y+dy

    else:
        return(player)

    return(new_player)
 
def find_weapons():
    if player in weapons:

        weapons_owned.append(player)
        weapons.remove(player)

def catch_weapon (pos, ls_weapons):
    return pos in ls_weapons

def damage(pos, ls_vilains):
    ls_damage = [(elem[0]-1,elem[1]) for elem in ls_vilains]
    ls_damage += [(elem[0]+1,elem[1]) for elem in ls_vilains]
    ls_damage += [(elem[0],elem[1]-1) for elem in ls_vilains]
    ls_damage += [(elem[0],elem[1]+1) for elem in ls_vilains]
    return pos in ls_damage

def kill_villain():
    if player in villains:
        if len(weapons_owned)>0:
            villains.remove(player)
            villains_killed.append(player)
            weapons_owned.pop()

# Game init and main loop
# ------------------------------------------------------------------------------
running = True
pg.init()
screen = pg.display.set_mode((X * W, Y * H))
clock = pg.time.Clock()
pg.display.set_caption('Show Text')


font_w = pg.font.Font('freesansbold.ttf', 80)
winning = font_w.render('Bravo :) ', True, (253,108,158), FLOOR)
losing = font_w.render('Tu es nul :/ ', True, (253,108,158), FLOOR)
losingRect = winning.get_rect()
losingRect.center = (6*X, 7*Y)
winningRect = winning.get_rect()
winningRect.center = (7*X, 7*Y)
pg.display.set_caption('Image')
image = pg.image.load(r'images/Couronne.png')

x_couronne,y_couronne = (26,26)
win = 0 # vaut 1 si on a gagné
playing = True
living = True
while playing:
    direction = (0,0)
    clock.tick(14)
    for event in pg.event.get():
            #print(f"{event=}")
            # chaque évênement à un type qui décrit la nature de l'évênement
            # un type de pg.QUIT signifie que l'on a cliqué sur la "croix" de la fenêtre
            if event.type == pg.QUIT:
                running = False
            # un type de pg.KEYDOWN signifie que l'on a appuyé une touche du clavier
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN:
                    direction = DIRECTIONS["DOWN"]
                elif event.key == pg.K_UP:
                    direction = DIRECTIONS["UP"]
                elif event.key == pg.K_RIGHT:
                    direction = DIRECTIONS["RIGHT"]
                elif event.key == pg.K_LEFT:
                    direction = DIRECTIONS["LEFT"]
                # si la touche est "Q" on veut quitter le programme
                elif event.key == pg.K_q:
                    running = False

    
    Longueur_ini = len(weapons_owned)
    if player in [(x_couronne,y_couronne),(x_couronne,y_couronne+1),(x_couronne+1,y_couronne),(x_couronne+1,y_couronne+1)]:
        win = 1

    draw_background()
    find_weapons()
    kill_villain()
    for villain in villains:
        draw_tile(villain[0],villain[1],(255,127,0))
    
    weapons_number = len(weapons_owned)

    font = pg.font.Font('freesansbold.ttf', 24)
    '''if catch_weapon(player, weapons):
        weapons_number += 1'''
    weapons_str  ='weapons : '
    weapons_str += str(weapons_number)
    weapon = font.render(weapons_str, True, blue, FLOOR)
    weaponRect = weapon.get_rect()
    weaponRect.center = (3*X, 14*Y)

    if damage(player, villains) and living == True:
        life_point = life_point - rd.randint(1,5)
    life_str  ='life : '
    life_str += str(life_point)
    life = font.render(life_str, True, rouge, FLOOR)
    lifeRect = life.get_rect()
    lifeRect.center = (4*X, 12.2*Y)
    
    screen.blit(life, lifeRect)
    screen.blit(weapon, weaponRect)

    player = move_player(player, direction)
    
    screen.blit(image, (x_couronne*W, y_couronne*H))
    if win == 1:
        screen.blit(winning, winningRect)
    
    if life_point<=0:
        living = False
        life_point = 0
        if win !=1:
            screen.blit(losing, winningRect)
        #playing = False


    draw_tile(player[0],player[1],(255,0,0))
    
    
    if len(weapons)!=0:
        for weapon in weapons:
            draw_tile(weapon[0],weapon[1],(50,50,50))

    pg.display.update()
    

pg.quit()
