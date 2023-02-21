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
    xoffset = game.player.x - WIDTH/2
    yoffset = game.player.y - HEIGHT/2
    canvas.delete("all")
    if quadTreeDisplay:
        game.quadtree.draw(canvas, xoffset, yoffset)
    if game.state == "menu":
        canvas.create_rectangle(WIDTH/2 - 200, HEIGHT/2 - 100, WIDTH/2 + 200, HEIGHT/2 + 100, fill="grey")
        canvas.create_text(WIDTH/2, HEIGHT/2, text=" Groahhh ", font="Arial 50", fill="black")
    elif game.state in ("running", "reward"):
        # Player animation sprite choice and display
        direct = 0
        if game.player.left: direct = 1
        if game.player.moving:
            img = playerMovingImg[direct][game.player.animation]
        else:
            img = playerIdleImg[direct][game.player.animation]
        canvas.create_image(game.player.x - xoffset, game.player.y - yoffset, image=img, anchor="center")
        # Monster display.
        for monster in game.monsters:
            if abs(game.player.x - monster.x) < WIDTH and abs(game.player.y - monster.y) < HEIGHT:
                # monster animation sprite choice and display
                turn = 0
                if monster.tag != "player":
                    if monster.x > game.player.x: turn = 1
                match monster.type:
                    case "zombie":
                        img = zombieImg[turn][monster.animation]
                    case "skeleton":
                        img = skeletonImg[turn][monster.animation]
                    case "orc":
                        img = orcImg[turn][monster.animation]
                    case "pig":
                        img = pigImg[turn][monster.animation]
                    case "skeletonBig":
                        img = skeletonBigImg[turn][monster.animation]
                    case "zombieBig":
                        img = zombieBigImg[turn][monster.animation]
                    case "orcBig":
                        img = orcBigImg[turn][monster.animation]
                    case "pigBig":
                        img = pigBigImg[turn][monster.animation]
                canvas.create_image(monster.x - xoffset, monster.y - yoffset, image=img, anchor="center")
        # Diamond display
        for diamond in game.diamonds:
            if abs(game.player.x - diamond.x) < WIDTH and abs(game.player.y - diamond.y) < HEIGHT:
                # Diamond sprite display
                canvas.create_image(diamond.x - xoffset, diamond.y - yoffset, image=diamondImg, anchor="center")
        # Chest display
        for chest in game.chests:
            if abs(game.player.x - chest.x) < WIDTH and abs(game.player.y - chest.y) < HEIGHT:
                # Diamond sprite display
                img = chestImg[chest.animation]
                canvas.create_image(chest.x - xoffset, chest.y - yoffset, image=img, anchor="center")
        # Bullet sprite display
        for bullet in game.player.bullets:
            canvas.create_oval(bullet.x - BULLET_SIZE - xoffset, bullet.y - BULLET_SIZE - yoffset, bullet.x + BULLET_SIZE - xoffset, bullet.y + BULLET_SIZE - yoffset, fill="black")
        # Orbs sprite display
        for orb in game.player.orbs:
            canvas.create_image(orb.x - xoffset, orb.y - yoffset, image=orbImg, anchor="center")
        # Fireball sprite display
        for fireball in game.player.fireballs:
            canvas.create_image(fireball.x - xoffset, fireball.y - yoffset, image=fireballImg[fireball.animation], anchor="center")
        # Health bar display.
        health_ratio = game.player.health/game.player.maxHealth
        canvas.create_rectangle(game.player.x - 20 - xoffset, game.player.y + 20 - yoffset, game.player.x + 20 - xoffset, game.player.y + 25 - yoffset, fill="black")
        canvas.create_rectangle(game.player.x - 18 - xoffset, game.player.y + 21 - yoffset, game.player.x - 18 + 36 * health_ratio - xoffset, game.player.y + 24 - yoffset, outline="green", fill="green")
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
        # Display spawn left
        canvas.create_text(WIDTH - 100, 40, text=f"Spawns: {game.spawnLeft}", anchor="nw", font="Arial 10", fill="black")

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

def rectDisplay():
    global quadTreeDisplay
    quadTreeDisplay = not quadTreeDisplay
    print(quadTreeDisplay)

if __name__ == "__main__":
    
    # Variables.
    mousex = 0
    mousey = 0
    direction = 0
    frameRate = 10
    quadTreeDisplay = True
    
    # Game creation.
    game = Game()

    # Tkinter section.
    window = Tk()
    #window.attributes("-fullscreen", True)
    window.title("Groahhh")

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=HEIGHT, width=WIDTH)
    canvas.pack()
    
    window.update()

    # Bindings.
    window.bind("<KeyPress>", lambda event: keyPressHandler(event.keysym))
    window.bind("<KeyRelease>", lambda event: keyReleaseHandler(event.keysym))
    window.bind("<Motion>", lambda event: updateCursor())
    window.bind("<Button-1>", lambda event: click())
    window.bind("<space>", lambda event: rectDisplay())

    # Images.
    playerIdleImg = [[ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_0.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_1.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_2.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_3.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_4.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_5.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_6.png")),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_7.png"))],
                   [ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/idle/playerIdle_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]
   
    playerMovingImg = [[ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_0.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_1.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_2.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_3.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_4.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_5.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_6.png")),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_7.png"))],
                    [ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/player/moving/playerMoving_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    zombieImg =   [[ImageTk.PhotoImage(Image.open("img/zombie/zombie_0.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_1.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_2.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_3.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_4.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_5.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_6.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_7.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_8.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_9.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_10.png")),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_11.png"))],
                   [ImageTk.PhotoImage(Image.open("img/zombie/zombie_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombie/zombie_11.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    zombieBigImg = [[ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_0.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_1.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_2.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_3.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_4.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_5.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_6.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_7.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_8.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_9.png")),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_10.png"))], 
                     [ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/zombieBig/zombieBig_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    skeletonImg = [[ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_0.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_1.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_2.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_3.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_4.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_5.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_6.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_7.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_8.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_9.png")),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_10.png"))],
                    [ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeleton/skeleton_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    skeletonBigImg = [[ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_0.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_1.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_2.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_3.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_4.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_5.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_6.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_7.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_8.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_9.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_10.png")),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_11.png"))],
                    [ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/skeletonBig/skeletonBig_11.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    orcImg = [[ImageTk.PhotoImage(Image.open("img/orc/orc_0.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_1.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_2.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_3.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_4.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_5.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_6.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_7.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_8.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_9.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_10.png")),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_11.png"))],
                    [ImageTk.PhotoImage(Image.open("img/orc/orc_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orc/orc_11.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    orcBigImg = [[ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_0.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_1.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_2.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_3.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_4.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_5.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_6.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_7.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_8.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_9.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_10.png")),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_11.png"))],
                    [ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/orcBig/orcBig_11.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    pigImg = [[ImageTk.PhotoImage(Image.open("img/pig/pig_0.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_1.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_2.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_3.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_4.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_5.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_6.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_7.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_8.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_9.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_10.png")),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_11.png"))],
                    [ImageTk.PhotoImage(Image.open("img/pig/pig_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pig/pig_11.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    pigBigImg = [[ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_0.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_1.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_2.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_3.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_4.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_5.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_6.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_7.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_8.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_9.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_10.png")),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_11.png"))],
                    [ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_0.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_1.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_2.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_3.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_4.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_5.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_6.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_7.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_8.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_9.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_10.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT)),
                    ImageTk.PhotoImage(Image.open("img/pigBig/pigBig_11.png").transpose(Image.Transpose.FLIP_LEFT_RIGHT))]]

    diamondImg = ImageTk.PhotoImage(Image.open("img/diamond/diamond.png"))

    chestImg = [ImageTk.PhotoImage(Image.open("img/chest/chest_0.png")),
                ImageTk.PhotoImage(Image.open("img/chest/chest_1.png")),
                ImageTk.PhotoImage(Image.open("img/chest/chest_2.png"))]

    orbImg = [ImageTk.PhotoImage(Image.open("img/orb/orb.png"))]

    fireballImg = [ImageTk.PhotoImage(Image.open("img/fireball/fireball_0.png")),
                    ImageTk.PhotoImage(Image.open("img/fireball/fireball_1.png")),
                    ImageTk.PhotoImage(Image.open("img/fireball/fireball_2.png")),
                    ImageTk.PhotoImage(Image.open("img/fireball/fireball_3.png"))]


    # Main loop.
    update()

    window.mainloop()