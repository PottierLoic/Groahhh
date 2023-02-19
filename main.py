"""
Groahhh game.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
from tkinter import *
import math
from PIL import Image, ImageTk

# Local libraries.
from constants import *
from game import Game

def graphics():
    canvas.delete("all")
    if game.state == "menu":
        canvas.create_rectangle(WIDTH/2 - 200, HEIGHT/2 - 100, WIDTH/2 + 200, HEIGHT/2 + 100, fill="grey")
        canvas.create_text(WIDTH/2, HEIGHT/2, text="Groahhh", font="Arial 50", fill="black")
    elif game.state == "running":
        # Health bar.
        canvas.create_rectangle(10, 10, 10 + game.player.maxHealth, 40, fill="black")
        canvas.create_rectangle(15, 15, 15 + game.player.health-10, 35, fill="green")
       
        # Player animation sprite choice
        if game.player.moving:
            img = playerWalk[game.player.animation]
        else:
            img = playerIdle[game.player.animation]

        # Player sprite display
        canvas.create_image(game.player.x, game.player.y, image=img, anchor="center")
        
        for zombie in game.zombies:
            # Zombie animation sprite choice
            img = bat[zombie.animation]
            # Zombie sprite display
            canvas.create_image(zombie.x, zombie.y, image=img, anchor="center")

        # Bullet sprite display
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
        game.player.moving = True
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
        game.player.moving = False
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
    click()

def clickRelease():
    game.player.fire = False

def click():
    if game.state == "menu":
        if WIDTH/2 - 200 < mousex < WIDTH/2 + 200 and HEIGHT/2 - 100 < mousey < HEIGHT/2 + 100:
            game.start()
            print("oue ça commence")
 
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

    # Images.
    playerIdle = [ImageTk.PhotoImage(Image.open("img/orc/idle_0.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/idle_1.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/idle_2.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/idle_3.png"))]
                
    playerWalk = [ImageTk.PhotoImage(Image.open("img/orc/walk_0.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_1.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_2.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_3.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_4.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_5.png"))]

    bat = [ImageTk.PhotoImage(Image.open("img/bat/idle_0.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_1.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_2.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_3.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_4.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_5.png"))]

    



    # Main loop.
    update()

    window.mainloop()