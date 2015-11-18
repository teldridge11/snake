# SNAKE: THE GAME
import pygame
import time
import random
import os

# Initialize Pygame
pygame.init()

# Colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

# Display
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')
icon = pygame.image.load('apple.bmp')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

# Sprites
snakeHead = pygame.image.load('snakehead.bmp')
apple = pygame.image.load('apple.bmp')
appleThickness = 30
block_size = 20
fps = 15 # Speed
direction = "right"

# Fonts
smallFont = pygame.font.SysFont("comicsansms", 25)
medFont = pygame.font.SysFont("comicsansms", 50)
largeFont = pygame.font.SysFont("comicsansms", 80)

# Pauses game and gives continue and quit options
def pause():
    paused = True
    message_to_screen("Paused", black, -100, size="large")
    message_to_screen("Press P to play, or Q to quit.", black, 25, size="small")
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        pygame.display.update()
        clock.tick(fps)

# Keeps track of, and displays the score
def score(score):
    text = smallFont.render(" Score: " + str(score), True, black)
    gameDisplay.blit(text, [0,0])

# Randomly generates apple coordinates
def randAppleGen():
    randAppleX = round(random.randrange(0, display_width-block_size))
    randAppleY = round(random.randrange(0, display_height-block_size))
    return randAppleX, randAppleY

# Intro screen - Title and directions
def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Welcome to Snake!", green, -100, size="large")
        message_to_screen("The objective of the game is to eat the apples", black, -30, size="small")
        message_to_screen("Every apple you eat makes you longer", black, 10, size="small")
        message_to_screen("If you run into yourself or the edges, you die", black, 50, size="small")
        message_to_screen("Press C to play, P to pause, or Q to quit", black, 180, size="small")
        pygame.display.update()
        clock.tick(fps)

# Controls snake head direction
def snake(block_size, snakelist):
    if direction == "right":
        head = pygame.transform.rotate(snakeHead, 270)
    if direction == "left":
        head = pygame.transform.rotate(snakeHead, 90)
    if direction == "up":
        head = snakeHead
    if direction == "down":
        head = pygame.transform.rotate(snakeHead, 180)
    gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))    
    for XnY in snakelist[:-1]:
        gameDisplay.fill(green, rect=[XnY[0],XnY[1],block_size,block_size])

# Font sizes        
def text_objects(text, color, size):
    if size == "small":
        textSurface = smallFont.render(text, True, color)
    elif size == "medium":
        textSurface = medFont.render(text, True, color)
    elif size == "large":
        textSurface = largeFont.render(text, True, color)
    return textSurface, textSurface.get_rect()

# Displays a message: Requires message, color, y-displacement, and size arguments
def message_to_screen(msg, color, y_displace=0, size="small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (display_width/2), (display_height/2) + y_displace
    gameDisplay.blit(textSurf, textRect)

# Main game loop
def gameLoop():
    global direction
    direction = "right"
    gameExit = False
    gameOver = False

    # Sets starting position and speed.  Snake and apple initializers.
    lead_x = display_width/2
    lead_y = display_height/2    
    lead_x_change = 20
    lead_y_change = 0
    snakeList = []
    snakeLength = 1
    randAppleX, randAppleY = randAppleGen()

    # Game over screen and changes for key inputs
    while not gameExit:
        if gameOver == True:
            message_to_screen("Game over!", red, -50, size="large")
            message_to_screen("Press C to play again, Q to quit.", black, 50, size="medium")
            pygame.display.update()
        while gameOver == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        # Make changes for specific key inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction = "left"
                    lead_x_change = -block_size
                    lead_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                    lead_x_change = block_size
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    direction = "up"
                    lead_y_change = -block_size
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    lead_y_change = block_size
                    lead_x_change = 0
                elif event.key == pygame.K_p:
                    pause()

        # Display collision detection
        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        # Updates x and y values for snake position
        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white) # Makes screen white for next clock frame
        
        # Snake movement 
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLength:
            del snakeList[0]

        # Snake collision detection
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True      
        snake(block_size, snakeList)

        # Update score
        score(snakeLength-1)

        # Snake grows when apple is eaten, and new apple is created
        gameDisplay.blit(apple, (randAppleX, randAppleY))
        if lead_x > randAppleX and lead_x < randAppleX + appleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + appleThickness:
            if lead_y > randAppleY and lead_y < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + appleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength += 1

        pygame.display.update()
        
        # Clock tick
        clock.tick(fps)

    # Quits
    pygame.quit()
    quit()

# Loads game intro screen
game_intro()

# gameLoop calls itself to begin game
gameLoop()
