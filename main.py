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
        canvas.create_text(WIDTH/2, HEIGHT/2, text=" ", font="Arial 50", fill="black")
    elif game.state in ("running", "reward"):
        # Player animation sprite choice AND DISPLAY
        if game.player.moving:
            img = playerWalkImg[game.player.animation]
        else:
            img = playerIdleImg[game.player.animation]
        canvas.create_image(game.player.x, game.player.y, image=img, anchor="center")
        # Zombie display
        for zombie in game.zombies:
            if abs(game.player.x - zombie.x) < WIDTH and abs(game.player.y - zombie.y) < HEIGHT:
                # Zombie animation sprite choice and display
                img = batImg[zombie.animation]
                canvas.create_image(zombie.x, zombie.y, image=img, anchor="center")
        # Diamond display
        for diamond in game.diamonds:
            if abs(game.player.x - diamond.x) < WIDTH and abs(game.player.y - diamond.y) < HEIGHT:
                # Diamond sprite display
                canvas.create_image(diamond.x, diamond.y, image=diamondImg, anchor="center")
        # Chest display
        for chest in game.chests:
            if abs(game.player.x - chest.x) < WIDTH and abs(game.player.y - chest.y) < HEIGHT:
                # Diamond sprite display
                img = chestImg[chest.animation]
                canvas.create_image(chest.x, chest.y, image=img, anchor="center")
        # Bullet sprite display
        for bullet in game.player.bullets:
            canvas.create_oval(bullet.x - BULLET_SIZE, bullet.y - BULLET_SIZE, bullet.x + BULLET_SIZE, bullet.y + BULLET_SIZE, fill="black")
        # Orbs sprite display
        for orb in game.player.orbs:
            canvas.create_oval(orb.x-ORB_RADIUS/2, orb.y-ORB_RADIUS/2, orb.x+ORB_RADIUS/2, orb.y+ORB_RADIUS/2, fill="blue")
        # Health bar display.
        health_ratio = game.player.health/game.player.maxHealth
        canvas.create_rectangle(game.player.x - 20, game.player.y + 20, game.player.x + 20, game.player.y + 25, fill="black")
        canvas.create_rectangle(game.player.x - 18, game.player.y + 21, game.player.x - 18 + 36 * health_ratio, game.player.y + 24, outline="green", fill="green")
        # Display experience
        try:
            exp_ratio = game.player.exp/EXPERIENCE_AMOUNT[game.player.level-1]
        except ZeroDivisionError:
            exp_ratio = 0
        canvas.create_rectangle(5, 5, WIDTH-5, 15, fill="black")
        canvas.create_rectangle(7, 7, 7 + (WIDTH - 5) * exp_ratio, 13, fill="cyan")
        # Display level
        canvas.create_text(10, 20, text=f"Level: {game.player.level}", anchor="nw", font="Arial 15", fill="black")
        # Display rounds
        canvas.create_text(WIDTH - 100, 20, text=f"Round: {game.round}", anchor="nw", font="Arial 15", fill="black")
        # Display fps
        canvas.create_text(WIDTH - 80, HEIGHT - 20, text=f"FPS: {round(frameRate)}", anchor="nw", font="Arial 10", fill="black")

        if game.state == "reward":
            # Display reward selection
            canvas.create_rectangle(WIDTH/2-100, HEIGHT/2-150, WIDTH/2+100, HEIGHT/2+150, fill="brown")
            canvas.create_text(WIDTH/2, HEIGHT/2-140, text="Choose a reward")

            canvas.create_rectangle(WIDTH/2-80, HEIGHT/2-120, WIDTH/2+80, HEIGHT/2-40, fill="#C4A484")
            canvas.create_text(WIDTH/2, HEIGHT/2-80, text=game.rewardQueue[0][0])

            canvas.create_rectangle(WIDTH/2-80, HEIGHT/2-30, WIDTH/2+80, HEIGHT/2+50, fill="#C4A484")
            canvas.create_text(WIDTH/2, HEIGHT/2+10, text=game.rewardQueue[0][1])

            canvas.create_rectangle(WIDTH/2-80, HEIGHT/2+60, WIDTH/2+80, HEIGHT/2+140, fill="#C4A484")
            canvas.create_text(WIDTH/2, HEIGHT/2+100, text=game.rewardQueue[0][2])

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
    if game.state == "reward":
        if WIDTH/2 - 80 < mousex < WIDTH/2 + 80 and HEIGHT/2 - 120 < mousey < HEIGHT/2 - 40:
            game.chooseReward(0)
        elif WIDTH/2 - 80 < mousex < WIDTH/2 + 80 and HEIGHT/2 - 30 < mousey < HEIGHT/2 + 50:
            game.chooseReward(1)
        elif WIDTH/2 - 80 < mousex < WIDTH/2 + 80 and HEIGHT/2 + 60 < mousey < HEIGHT/2 + 140:
            game.chooseReward(2)
 
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

    chestImg = [ImageTk.PhotoImage(Image.open("img/chest/chest_0.png")),
                ImageTk.PhotoImage(Image.open("img/chest/chest_1.png")),
                ImageTk.PhotoImage(Image.open("img/chest/chest_2.png"))]

    # Main loop.
    update()

    window.mainloop()