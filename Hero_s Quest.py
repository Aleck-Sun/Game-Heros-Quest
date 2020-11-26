from tkinter import *
from math import *
from time import *
from random import *
from winsound import *

root = Tk()
s = Canvas(root, width = 700, height = 900, background = "black")

#Import Imagwes
def images():
    global background, titlePage, difficultyPage
    global snowball, snowHit, snowBlock, hero, splash
    global heroUp, heroRight, heroLeft, life, end, story1, story2

    titlePage = PhotoImage(file = "TitlePage.gif")
    background = PhotoImage(file = "Background.gif")
    snowball = PhotoImage(file = "Snowball.gif")
    difficultyPage = PhotoImage(file = "DifficultyPage.gif")
    snowHit = PhotoImage(file = "Hit.gif")
    snowBlock = PhotoImage(file = "SnowballBlock.gif")
    hero = PhotoImage(file = "Hero.gif")
    heroRight = PhotoImage(file = "HeroRight.gif")
    heroLeft = PhotoImage(file = "HeroLeft.gif")
    heroUp = PhotoImage(file = "HeroUp.gif")
    life = PhotoImage(file = "Heart.gif")
    end = PhotoImage(file = "EndScreen.gif")
    splash = PhotoImage(file = "SplashScreen.gif")
    story1 = PhotoImage(file = "Story1.gif")
    story2 = PhotoImage(file = "Story2.gif")

#Set Initial Values
def variables():
    global xMouse, yMouse, lives, points, difficulty 
    global LxBall, LRyBall, RxBall, UxBall, UyBall, score, scoreTxt
    global ball, hit, block, points, ballSpeed, ballDirection, delaySpd
    global scene, gameTime, character, xHero, yHero, delay, ballAppeared

    xMouse = 0
    yMouse = 0
    ball = []
    hit = []
    block = []
    LxBall = []
    LRyBall = 0
    RxBall = []
    UxBall = 0
    UyBall = []
    score = 0
    scoreTxt = 0
    ballDirection = 0
    scene = 3
    gameTime = 0
    character = hero
    xHero = 350
    yHero = 320
    lives = 3
    delay = 0

    #Values based on difficulty
    #Hard
    if difficulty == "h":
        points = 5
        ballSpeed = 10
        ballAppeared = 10
        delaySpd = 5

    #Medium
    elif difficulty == "m":
        points = 2
        ballSpeed = 8
        ballAppeared = 20
        delaySpd = 10

    #Easy
    elif difficulty == "e":
        points = 1
        ballSpeed = 3
        ballAppeared = 50
        delaySpd = 25


#Game Mechanics
#Create objects and BG
def Background():
    global BG, life3, life2, life1, score

    #Background and score of 0
    BG = s.create_image(350, 450, image = background)
    score = s.create_text(590, 64, text = str(scoreTxt), font = "FixedSys 42")

    #3 lives
    life3 = s.create_image(177, 65, image = life)
    life2 = s.create_image(122, 65, image = life)
    life1 = s.create_image(67, 65, image = life)
        

#Launch snowballs
def launchSnowball():
    global ballDirection, gameTime, ballAppeared
    global LxBall, LRyBall, RxBall, UxBall, UyBall

    #Send snowballs within intervals of time
    if gameTime > ballAppeared:
        #Reset interval of time for snwoballs to appear
        gameTime = 0

        #Choose random snowball direction
        ballDirection = randint(1,3)

        #Appending starting x and y values depending on ball direction
        if ballDirection == 1:
            LxBall.append(-25)
            LRyBall = 338

        elif ballDirection == 2:
            RxBall.append(725)
            LRyBall = 338

        elif ballDirection == 3:
            UxBall = 350
            UyBall.append(700)

#Snowball flying in animation
def updateBall():
    global LxBall, LRyBall, RxBall, UxBall, UyBall, ball, hit

    #Snowballs coming from left
    #Loops through coordinate arrays to check if ball has reached center (hit main character)
    for i in range(len(LxBall)-1, -1, -1):
        #Updates (animation)
        LxBall[i] += ballSpeed

        #If abll will hit center
        if LxBall[i]>= 300:
            #Appends image of ball getting hit and how long the image will last until deleted
            #Note: 5 second in game = 0.03 seconds
            hit.append([s.create_image(LxBall[i], LRyBall, image = snowHit), 5])
            del LxBall[i]
            lostLife()

        #Otherwise append to snowballs existing on screen    
        else:
            ball.append(s.create_image(LxBall[i], LRyBall, image = snowball))
            
    #Snowballs coming from right
    for i in range(len(RxBall)-1, -1, -1):
        RxBall[i] -= ballSpeed
        if RxBall[i] <= 400:
            hit.append([s.create_image(RxBall[i], LRyBall, image = snowHit), 5])
            del RxBall[i]
            lostLife()
                       
        else:
            ball.append(s.create_image(RxBall[i], LRyBall, image = snowball))

    #Snowballs coming from down
    for i in range(len(UyBall)-1, -1, -1):
        UyBall[i] -= ballSpeed
        if UyBall[i] <= 390:
            hit.append([s.create_image(UxBall, UyBall[i], image = snowHit), 5])
            del UyBall[i]
            lostLife()
            
        else:
            ball.append(s.create_image(UxBall, UyBall[i], image = snowball))

#You blocked a snowball
def snowballHit():
    global score, scoreTxt

    #deletes original score
    s.delete(score)
    #Updates score
    scoreTxt += points
    #Creates new score
    score = s.create_text(590, 64, text = str(scoreTxt), font = "FixedSys 42")

def lostLife():
    global lives

    #Depending on how many lives you have, deletes the lives from right to left
    if lives == 3:
        s.delete(life3)
    elif lives == 2:
        s.delete(life2)
    else:
        s.delete(life1)

    lives -= 1
    
def drawHero():
    global main, xHero, yHero, character

    #Creates hero
    main = s.create_image(xHero, yHero, image = character)

    #Set hero normally to upright position unless arrow key clicked
    if delay <= 0:
        character = hero
        xHero = 350
        yHero = 320

#Displays final score
def scoreDisplay():
    global scene

    scene = 4
    s.delete("all")
    s.create_image(350, 450, image = end)
    s.create_text(350, 400, text = str(scoreTxt), font = "FixedSys 120", fill = "white")

#Updates in-game time
def updateTime():
    global gameTime, delay

    #Increases time since a snowball is created when gametime reaches a certain value
    gameTime += 1

    #Subtracts from how long main character stays in same position
    delay -= 1

#Deletes ball and main character
def deleteBall():
    global ball

    s.delete(main)

    #Deletes ball
    for i in ball:
        s.delete(i)
    
    for i in range(len(hit)-1,-1,-1):
        hit[i][1] -= 1

        #Deletes hit snowball after 0.15 seconds
        if hit[i][1] == 0:
            s.delete(hit[i][0])
            del hit[i]

    for i in range(len(block)-1,-1,-1):
        block[i][1] -= 1

        #Deletes blocked snowball after 0.15 seconds
        if block[i][1] == 0:
            s.delete(block[i][0])
            del block[i]

def mouseClickHandler(event):
    global xMouse, yMouse, difficulty, scene

    #Mouse coordinates
    xMouse = event.x
    yMouse = event.y

    #If play selected  
    if xMouse > 190 and xMouse < 510 and yMouse > 535 and yMouse < 645 and scene == 1:
        s.delete("all")
        difficultySelect()

    #Difficulty level selecting
    if xMouse > 154 and xMouse < 546 and scene == 2:
        if yMouse > 69 and yMouse < 231:
            difficulty = "e"
            runGame()

        elif yMouse > 369 and yMouse < 531:
            difficulty = "m"
            runGame()

        elif yMouse > 669 and yMouse < 831:
            difficulty = "h"
            runGame()

    #Home selected(Gameover screen)
    if xMouse > 115 and xMouse < 585 and yMouse > 745 and yMouse < 850 and scene == 4:
        s.delete("all")
        titleScreen()

def keyClickHandler(event):
    global character, xHero, yHero, block, delay, delaySpd, scene

    #Story(go through story with spacebar)
    if event.keysym == "space":
        if scene == -6:
            s.create_text(350, 50, text = """After 5 years of training, you are finally ready to become a master swordsman.
The sensei is waiting at the peak of the dangerous Mt. Everisk to honour you
with this title. After several weeks of gruesome climbing, the peak is just
within your reach.""", font = "FixedSys 15", fill = "white")
            scene = -5
            s.update()

        elif scene == -5:
            s.create_image(350, 400, image = story1)
            s.update()
            scene = -4

        elif scene == -4:
            s.create_text(350, 400, text = """Suddenly, a pack of vicious Yetis begin hurling snowballs towards you!
It is up to you to defend against these snowballs! This is your final
test to become a master swordsman!""", font = "FixedSys 15", fill = "white")
            s.update()
            scene = -3

        elif scene == -3:
            s.create_image(350, 400, image = story2)
            s.update()
            scene = -2

        elif scene == -2:
            s.create_text(350, 750, text = """Each snowball you block will increase your score! Survive the attack,
conquer Mt. Everisk, and reach for the highest score possible to
become a master swordsman!""", font = "FixedSys 15", fill = "white")
            s.update()
            scene = -1

        elif scene == -1:
            instructions()

        elif scene == 0:
            titleScreen()

    #Game screen
    if scene == 3:

        #Sets a delay on character movement (stays in blocking position for a little bit)
        #This prevents players from spamming the arrow keys to block rather than timing blocks strategically
        if delay < 0:
            delay = delaySpd

            #If left arrow key selected    
            if event.keysym == "Left":

                #Set character to corresponding arrow key position
                character = heroLeft
                xHero = 330
                yHero = 325

                #Checks if snowball was hit, loop through x values until matches conditions
                for i in range(len(LxBall)-1, -1, -1):
                    if LxBall[i] >= 250 and LxBall[i] <= 300:
                        #Deletes the snowball
                        s.delete(ball[i])
                        #Appending the picture of blocked snowball and how long ti lasts on screen
                        block.append([s.create_image(LxBall[i], LRyBall, image = snowBlock), 5])
                        del LxBall[i]
                        #Update score
                        snowballHit()

            #Right arrow key selected               
            elif event.keysym == "Right":
                character = heroRight
                xHero = 370
                yHero = 325

                for i in range(len(RxBall)-1, -1, -1):
                    if RxBall[i] >= 400 and RxBall[i] <= 450:
                        s.delete(ball[i])
                        block.append([s.create_image(RxBall[i], LRyBall, image = snowBlock), 5])
                        del RxBall[i]
                        snowballHit()

            #Down key pressed
            elif event.keysym == "Down":
                character = heroUp
                xHero = 350
                yHero = 350

                for i in range(len(UyBall)-1, -1, -1):
                    if UyBall[i] >= 390 and UyBall[i] <= 440:
                        s.delete(ball[i])
                        block.append([s.create_image(UxBall, UyBall[i], image = snowBlock), 5])
                        del UyBall[i]
                        snowballHit()
    
#Credits    
def splashScreen():
    images()
    s.create_image(350, 450, image = splash)
    s.update()
    sleep(3)
    story()

#Storyline
def story():
    global scene
    
    PlaySound("Music.wav", SND_LOOP + SND_ASYNC)
    s.delete("all")
    scene = -6
    s.create_text(350, 850, text = "Press 'Space' To Continue", font = "FixedSys 10", fill = "white")
    s.update()

#How to play
def instructions():
    global scene
    s.delete("all")
    scene = 0
    s.create_text(350, 100, text = "INSTRUCTIONS:", font = "FixedSys 100", fill = "white")
    s.create_text(360, 450, text = """Snowballs will be coming in from
different paths. Use the right, down,
and left arrow keys to block snowballs
coming from the corresponding direction.
Press the arrow keys when the snowballs
are inside the range of your sword, which
is represented by the dark grey box on
the path. Time it too early and you will
miss! Time it too late and you will be hit
by the snowball and lose a life. If you
lose all your lives, the game will be over.
Each snowball blocked will increase your
score.""", font = "FixedSys 18", fill = "white")
    s.create_text(350, 850, text = "Press 'Space' To Continue", font = "FixedSys 10", fill = "white")

#Can select play from here
def titleScreen():
    global scene

    PlaySound("Music3.wav", SND_LOOP + SND_ASYNC)
    scene = 1
    s.create_image(350, 450, image = titlePage)

#Can select difficulties    
def difficultySelect():
    global scene

    scene = 2
    difficulty = s.create_image(350, 450, image = difficultyPage)

#Actual Game
def runGame():
    global ball

    PlaySound("Music.wav", SND_LOOP + SND_ASYNC)
    #Get variables
    variables()

    #Create background
    Background()
 
    #Game Loop
    while lives > 0:
        updateTime()
        drawHero()
        launchSnowball()
        updateBall()

        s.update()
        sleep(0.03)
        deleteBall()
        
    sleep(1)
    scoreDisplay()

#Goes to splash screen
root.after(0, splashScreen)

#Mouse clicks and key clicks
s.bind("<Button-1>", mouseClickHandler)
s.bind( "<KeyPress>", keyClickHandler )

s.pack()
s.focus_set()
root.mainloop()
