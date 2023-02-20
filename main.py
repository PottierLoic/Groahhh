"""
Groahhh game.
    Author : Loïc Pottier.
    Creation date : 19/02/2023.
"""

# Basic libraries.
from tkinter import *
import math
from PIL import Image, ImageTk
import time

# Local libraries.
from constants import *
from game import Game

def graphics():
    canvas.delete("all")
    if game.state == "menu":
        canvas.create_rectangle(WIDTH/2 - 200, HEIGHT/2 - 100, WIDTH/2 + 200, HEIGHT/2 + 100, fill="grey")
        canvas.create_text(WIDTH/2, HEIGHT/2, text="Groahhh", font="Arial 50", fill="black")
    elif game.state == "running":
        # Player animation sprite choice
        if game.player.moving:
            img = playerWalkImg[game.player.animation]
        else:
            img = playerIdleImg[game.player.animation]

        # Player sprite display
        canvas.create_image(game.player.x, game.player.y, image=img, anchor="center")

        # Zombie display
        for zombie in game.zombies:
            if abs(game.player.x - zombie.x) < WIDTH and abs(game.player.y - zombie.y) < HEIGHT:
                # Zombie animation sprite choice
                img = batImg[zombie.animation]
                # Zombie sprite display
                canvas.create_image(zombie.x, zombie.y, image=img, anchor="center")

        # Diamond display
        for diamond in game.diamonds:
            if abs(game.player.x - diamond.x) < WIDTH and abs(game.player.y - diamond.y) < HEIGHT:
                # Diamond sprite display
                canvas.create_image(diamond.x, diamond.y, image=diamondImg, anchor="center")
        
        # Bullet sprite display
        for bullet in game.player.bullets:
            canvas.create_oval(bullet.x - BULLET_SIZE, bullet.y - BULLET_SIZE, bullet.x + BULLET_SIZE, bullet.y + BULLET_SIZE, fill="black")

        # Health bar display.
        canvas.create_rectangle(10, 10, 10 + game.player.maxHealth, 40, fill="black")
        canvas.create_rectangle(15, 15, 15 + game.player.health-10, 35, fill="green")
    
        # Display experience
        try:
            exp_ratio = game.player.exp/EXPERIENCE_AMOUNT[game.player.level-1]
        except ZeroDivisionError:
            exp_ratio = 0
        canvas.create_rectangle(10, 50, 200, 80, fill="black")
        canvas.create_rectangle(15, 55, 15+ 180 * exp_ratio, 75, fill="cyan")

        # Display level
        canvas.create_text(80, 55, text=f"Level: {game.player.level}", anchor="nw", font="Arial 15", fill="white")

        # Display rounds
        canvas.create_text(WIDTH - 100, 20, text=f"Round: {game.round}", anchor="nw", font="Arial 15", fill="black")

        # Display fps
        canvas.create_text(WIDTH - 80, HEIGHT - 20, text=f"FPS: {round(frameRate)}", anchor="nw", font="Arial 10", fill="black")



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

def click():
    if game.state == "menu":
        if WIDTH/2 - 200 < mousex < WIDTH/2 + 200 and HEIGHT/2 - 100 < mousey < HEIGHT/2 + 100:
            game.start()
 
def update():
    global frameRate
    time1 = time.time()
    graphics()
    game.update()
    time2 = time.time()
    try:
        frameRate = 1/(time2-time1)
    except ZeroDivisionError:
        pass
    window.after(DELAY, update)

if __name__ == "__main__":
    
    # Variables.
    mousex = 0
    mousey = 0
    direction = 0
    frameRate = 10
    
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
    window.bind("<Button-1>", lambda event: click())

    # Images.
    playerIdleImg = [ImageTk.PhotoImage(Image.open("img/orc/idle_0.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/idle_1.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/idle_2.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/idle_3.png"))]

    playerWalkImg = [ImageTk.PhotoImage(Image.open("img/orc/walk_0.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_1.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_2.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_3.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_4.png")),
                  ImageTk.PhotoImage(Image.open("img/orc/walk_5.png"))]

    batImg = [ImageTk.PhotoImage(Image.open("img/bat/idle_0.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_1.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_2.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_3.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_4.png")),
           ImageTk.PhotoImage(Image.open("img/bat/idle_5.png"))]
        
    diamondImg = ImageTk.PhotoImage(Image.open("img/diamond/diamond.png"))

    # Main loop.
    update()

    window.mainloop()