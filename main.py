"""
Groahhh game.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
from tkinter import *
import math

# Local libraries.
from constants import *
from game import Game

def graphics():
    canvas.delete("all")
    canvas.create_text(10, 10, text="Health : " + str(game.player.health), anchor="nw", font="Arial 20", fill="black")
    canvas.create_oval(game.player.x - PLAYER_SIZE, game.player.y - PLAYER_SIZE, game.player.x + PLAYER_SIZE, game.player.y + PLAYER_SIZE, outline="green", fill="green")
    canvas.create_line(game.player.x, game.player.y, mousex, mousey, fill="black")
    for zombie in game.zombies:
        canvas.create_oval(zombie.x - ZOMBIE_SIZE, zombie.y - ZOMBIE_SIZE, zombie.x + ZOMBIE_SIZE, zombie.y + ZOMBIE_SIZE, fill="red")
    for bullet in game.player.bullets:
        canvas.create_oval(bullet.x - BULLET_SIZE, bullet.y - BULLET_SIZE, bullet.x + BULLET_SIZE, bullet.y + BULLET_SIZE, fill="black")

def updateCursor():
    global mousex, mousey
    mousex = window.winfo_pointerx() - window.winfo_rootx()
    mousey = window.winfo_pointery() - window.winfo_rooty()
    angle = math.atan2(mousey - game.player.y, mousex - game.player.x)
    game.player.direction = (math.cos(angle), math.sin(angle))

def keyPressHandler(action):
    if action in ("q", "d", "z", "s"):
        if action == "q":
            game.player.left = True
        elif action == "d":
            game.player.right = True
        elif action == "z":
            game.player.up = True
        elif action == "s":
            game.player.down = True

def keyReleaseHandler(action):
    if action in ("q", "d", "z", "s"):
        if action == "q":
            game.player.left = False
        elif action == "d":
            game.player.right = False
        elif action == "z":
            game.player.up = False
        elif action == "s":
            game.player.down = False

def clickPress():
    game.player.fire = True

def clickRelease():
    game.player.fire = False

def update():
    graphics()
    game.update()
    window.after(DELAY, update)

if __name__ == "__main__":
    
    # Variables.
    mousex = 0
    mousey = 0
    direction = 0

    # Game creation.
    game = Game()

    # Tkinter section.
    window = Tk()
    window.title("Groahhh")

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
    canvas.pack()
    
    window.update()

    # Bindings.
    window.bind("<KeyPress>", lambda event: keyPressHandler(event.keysym))
    window.bind("<KeyRelease>", lambda event: keyReleaseHandler(event.keysym))
    window.bind("<Motion>", lambda event: updateCursor())
    window.bind("<ButtonPress-1>", lambda event: clickPress())
    window.bind("<ButtonRelease-1>", lambda event: clickRelease())

    # Main loop.
    update()

    window.mainloop()