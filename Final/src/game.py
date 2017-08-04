#Justin Orr
#Final Project
#Python: 3.6.1

'''The Main Game module'''

try:
    import pygame
except:
    print("Error importing pygame module. Please \'pip install pygame\' for python 3.6.1")

try:
    from pygame.locals import *
except:
    print("Error importing * from pygame.locals")
    
try:    
    from minesweeper.manager import ScreenManager
except:
    print("Error importing ScreenManager module from minesweeper.manager")

def initPyGame():
    '''Initializes Pygame and Pygame Font as well as sets the window size and title'''
    pygame.init()
    pygame.font.init()
    
    window = pygame.display.set_mode((480, 480))
    pygame.display.set_caption("MineSweeper Lite")
    
    return window

# MAIN PROGRAM

gameWindow = initPyGame()
clock = pygame.time.Clock()
screenManager = ScreenManager()

done = False
while not done: 
    # CHECK FOR EXIT COMMAND
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
    
    # CLEAR WINDOW BEFORE REDRAW
    gameWindow.fill((195, 195, 195))
    
    # MAIN GAME LOOP
    screenManager.update(pygame, gameWindow)
    if screenManager.checkQuit():
        done = True
    
    # PREPARE FOR NEXT LOOP        
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
quit()

# END MAIN PROGRAM
