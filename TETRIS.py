import tkinter as tk
import random

class Tetris:
    def __init__(self, fenetre):
        self.fenetre = fenetre
        self.fenetre.title("TETRIS")
        
        self.case = 30
        self.col = 10
        self.rang = 20
        self.plateau = {}
        self.game_over = False
        
        self.can = tk.Canvas(self.fenetre, width=self.col * self.case, height=self.rang * self.case, bg='black')
        self.can.pack()

        self.pieces = [
            [(4,0),(5,0),(4,1),(5,1)],      
            [(3,0),(4,0),(5,0),(6,0)],      
            [(4,0),(3,1),(4,1),(5,1)],     
            [(3,0),(3,1),(4,1),(5,1)],      
            [(5,0),(3,1),(4,1),(5,1)],      
            [(4,0),(5,0),(3,1),(4,1)],     
            [(3,0),(4,0),(4,1),(5,1)]       
        ]
        self.couleurs = ["cyan", "yellow", "purple", "orange", "blue", "green", "red"]

        # Bind des touches
        self.fenetre.bind('<d>', self.right)
        self.fenetre.bind('<Right>', self.right)
        self.fenetre.bind('<q>', self.left)
        self.fenetre.bind('<Left>', self.left)
        self.fenetre.bind('<z>', self.rotate)
        self.fenetre.bind('<Up>', self.rotate)
        self.fenetre.bind('<Button-3>', self.rotate)
        self.fenetre.bind('<s>', self.bas)
        self.fenetre.bind('<Down>', self.bas)
        self.fenetre.bind('<Button-1>', self.pose)
        self.fenetre.bind('<space>', self.pose)

        self.grille()
        self.nouvelle_piece()
        self.chute()

    def grille(self):
        for x in range(self.col):
            for y in range(self.rang):
                x1 = x * self.case
                y1 = y * self.case
                x2 = x1 + self.case
                y2 = y1 + self.case
                self.can.create_rectangle(x1, y1, x2, y2, outline='black', fill='black')

    def dessiner(self):
        self.can.delete("piece")
        
        for (x,y), color in self.plateau.items():
            x1 = x * self.case
            y1 = y * self.case
            x2 = (x + 1) * self.case
            y2 = (y + 1) * self.case
            self.can.create_rectangle(x1, y1, x2, y2, fill = color, outline = "black", tags="piece")
        
        for (x, y) in self.piece:
            x1 = x * self.case
            y1 = y * self.case
            x2 = x1 + self.case
            y2 = y1 + self.case
            self.can.create_rectangle(x1, y1, x2, y2, fill=self.couleur, outline="black", tags="piece")    
            
    def right(self, event=None):
        for x, y in self.piece:
            if x + 1 > 9 or (x + 1, y) in self.plateau:
                return
        self.piece = [(x + 1, y) for x, y in self.piece]
        self.dessiner()

    def left(self, event=None):
        for x, y in self.piece:
            if x - 1 < 0 or (x - 1, y) in self.plateau:
                return
        self.piece = [(x - 1, y) for x, y in self.piece]
        self.dessiner()

    def rotate(self, event=None):
        pivot = self.piece[1]
        x0, y0 = pivot
        new_piece = []
        for (x, y) in self.piece:
            new_x = x0 - (y - y0)
            new_y = y0 + (x - x0)
            new_piece.append((new_x, new_y))

        for (x, y) in new_piece:
            if x < 0 or x >= self.col or y < 0 or (x, y) in self.plateau:
                return

        self.piece = new_piece
        self.dessiner()

    def bas(self, event=None):
        desc = [(x, y + 1) for x, y in self.piece]
        for (x, y) in desc:
            if y >= self.rang or (x, y) in self.plateau:
                return
        self.piece = desc
        self.dessiner()

    def pose(self, event=None):
        descend = True
        while descend:
            desc = [(x, y + 1) for x, y in self.piece]
            for x, y in desc:
                if y >= self.rang or (x, y) in self.plateau:
                    descend = False
                    break
            if descend:
                self.piece[:] = desc
        for x, y in self.piece:
            self.plateau[(x, y)] = self.couleur
            self.can.create_rectangle(x*self.case, y*self.case, (x+1)*self.case, (y+1)*self.case, fill=self.couleur, outline="black")
        self.pleine()
        self.nouvelle_piece()

    def nouvelle_piece(self):
        self.piece = random.choice(self.pieces)
        self.couleur = random.choice(self.couleurs)
        for (x, y) in self.piece:
            if (x, y) in self.plateau:
                self.game_over = True
                self.can.delete("all")
                self.can.create_text(
                    self.col * self.case // 2, self.rang * self.case // 2,
                    text="GAME OVER", fill="red", font=("Arial", 30)
                )
                return None
        self.dessiner()
        
        self.fenetre.after(500, self.chute)

    def chute(self):
        if self.game_over:
            return
        desc = [(x, y + 1) for x, y in self.piece]
        for (x, y) in desc:
            if y >= self.rang or (x, y) in self.plateau:
                # Fixe la pièce sur le plateau
                for bloc in self.piece:
                    self.plateau[bloc] = self.couleur
                self.pleine()
                self.nouvelle_piece()
                return
        self.piece = desc
        self.dessiner()
        self.fenetre.after(500, self.chute)

    def pleine(self):
        supprimer = []
        for y in range(self.rang):
            if all((x, y) in self.plateau for x in range(self.col)):
                supprimer.append(y)

        if not supprimer:
            return

        new_plateau = {}
        for (x, y), color in self.plateau.items():
            if y not in supprimer:
                decalage = sum(1 for ligne in supprimer if y < ligne)
                new_plateau[(x, y + decalage)] = color

        self.plateau = new_plateau
        self.can.delete("all")
        self.grille()

        for (x, y), color in self.plateau.items():
            self.can.create_rectangle(
                x * self.case, y * self.case,
                (x + 1) * self.case, (y + 1) * self.case,
                fill=color, outline="black"
            )

if __name__ == "__main__":
    fenetre = tk.Tk()
    jeu = Tetris(fenetre)
    fenetre.mainloop()