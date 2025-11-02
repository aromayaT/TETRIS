import tkinter as tk
from tkinter import *
import random

fenetre = tk.Tk()
fenetre.title("TETRIS")

case = 30
col = 10
rang = 20
plateau = set()
game_over = False

def right(event=None):
    global piece
    for x, y in piece:
        if x + 1 > 9 or (x + 1, y) in plateau:
            return
    piece = [(x + 1, y) for x, y in piece]
    dessiner(can, piece, couleur)

def left(event=None):
    global piece
    for x, y in piece:
        if x - 1 < 0 or (x - 1, y) in plateau:
            return
    piece = [(x - 1, y) for x, y in piece]
    dessiner(can, piece, couleur)

can = tk.Canvas(fenetre, width=col * case, height=rang * case, bg='black')
can.pack()

def grille(can, case, col, rang):
    for x in range(col):
        for y in range(rang):
            x1 = x * case
            y1 = y * case
            x2 = x1 + case
            y2 = y1 + case
            can.create_rectangle(x1, y1, x2, y2, outline = '#333333', fill = 'black')
            
def dessiner(can, piece, color):
    can.delete("piece")
    for (x, y) in piece:
        x1 = x * case
        y1 = y * case
        x2 = x1 + case
        y2 = y1 + case
        can.create_rectangle(x1, y1, x2, y2, fill=color, outline="black", tags="piece")

pieces = [
    [(4,0),(5,0),(4,1),(5,1)],      
    [(3,0),(4,0),(5,0),(6,0)],      
    [(4,0),(3,1),(4,1),(5,1)],     
    [(3,0),(3,1),(4,1),(5,1)],      
    [(5,0),(3,1),(4,1),(5,1)],      
    [(4,0),(5,0),(3,1),(4,1)],      
    [(3,0),(4,0),(4,1),(5,1)]       
]

couleurs = ["cyan", "yellow", "purple", "orange", "blue", "green", "red"]

def newp():
    piece = random.choice(pieces)
    couleur = random.choice(couleurs)
    return piece, couleur

def nouvelle_piece():
    global piece, couleur, game_over
    piece, couleur = newp()
    for (x, y) in piece:
        if (x, y) in plateau:
            game_over = True
            can.delete("all")
            can.create_text(
                col * case // 2, rang * case // 2,
                text="GAME OVER",
                fill="red",
                font=("Arial", 30)
            )
            return

    dessiner(can, piece, couleur)
    chute()

def rotate(event=None):
    global piece
    # Choisir un bloc pivot (par ex. le 2e bloc)
    pivot = piece[1]
    x0, y0 = pivot
    
    new_piece = []
    for (x, y) in piece:
        new_x = x0 - (y - y0)
        new_y = y0 + (x - x0)
        new_piece.append((new_x, new_y))
    
    for (x, y) in new_piece:
        if x < 0 or x >= col or y < 0 or (x, y) in plateau:
            return
    
    piece = new_piece
    dessiner(can, piece, couleur)
    

def chute():
    global piece, plateau
    if game_over:
        return
    
    desc = []
    for x, y in piece:
        desc.append((x, y + 1))
    
    #Vérifie les collisions avec le bas ou les blocs
    for (x, y) in desc:
        if y >= rang or (x, y) in plateau:
            #Fixe la pièce sur le plateau
            for bloc in piece:
                plateau[bloc] = couleur
            
            pleine()
            
            nouvelle_piece()
            return
        
    piece = desc
    dessiner(can, piece, couleur)
    fenetre.after(500, chute)
    
def bas(event=None):
    global piece
    desc = []
    for x, y in piece:
            desc.append((x, y + 1))
    
    for (x, y) in desc:
        if y >= rang or (x, y) in plateau:
            return
        
    piece = desc
    dessiner(can, piece, couleur)
    
def pose(event=None):
    global piece, plateau
    descend = True
    while descend:
        desc = []
        for x, y in piece:
            desc.append((x, y + 1))
        descend = True
        for x, y in desc:
            if y >= rang or (x, y) in plateau:
                descend = False
                break
        if descend:
            piece[:] = desc
    # Fixer la pièce
    for x, y in piece:
        plateau.add((x, y))
        can.create_rectangle(x*case, y*case, (x+1)*case, (y+1)*case, fill=couleur, outline="black")
    nouvelle_piece()
    
def pleine():
    global plateau
    supprimer = []
    
    for y in range(rang):
        compte = 0
        for x in range(col):
            if (x, y) in plateau:
                compte += 1
        if compte == col:
            supprimer.append(y)
            
    if not supprimer:
        return
        
    new_plateau = set()
    for x, y in plateau:
        if y not in supprimer:
            decalage = 0
            for ligne in supprimer:
                if y < ligne:
                    decalage += 1
            new_plateau.add((x, y + decalage))
    plateau = new_plateau
    
    can.delete("all")
    grille(can, case, col, rang)
    for (x, y), color in plateau.items():
        can.create_rectangle(
            x * case, y * case,
            (x + 1) * case, (y + 1) * case,
            fill = "gray", outline = "black"
        )
            

fenetre.bind('<d>', right)
fenetre.bind('<Right>', right)
fenetre.bind('<q>', left)
fenetre.bind('<Left>', left)
fenetre.bind('<z>', rotate)
fenetre.bind('<Up>', rotate)
fenetre.bind('<Button-3>', rotate)
fenetre.bind('<s>', bas)
fenetre.bind('<Down>', bas)
fenetre.bind('<Button-1>', pose)
fenetre.bind('<space>', pose)

grille(can, case, col, rang)
piece, couleur = newp()
dessiner(can, piece, couleur)
chute()

fenetre.mainloop()

