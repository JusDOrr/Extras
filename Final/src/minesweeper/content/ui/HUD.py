#Justin Orr
#Final Project
#Python: 3.6.1

'''The HUD module defines the Heads Up Display drawn on top of a game board'''

try:
    from pygame.locals import Rect
except:
    print("Error importing Rect module from pygame.locals")

try:    
    from minesweeper.util import ScreenState
except:
    print("Error importing ScreenState module from minesweeper.util")

try:
    from minesweeper.content.ui.Button import Button
except:
    print("Error importing Button module from minesweeper.content.ui.Button")

class HUD():
    '''Manages the HUD to be displayed on top of the game board'''    
    def __init__(self):
        '''Initializes the font and artwork as well as save and exit buttons'''
        self.font = None
        self.logo = None
        
        self.btnSave = None
        self.btnExit = None
        
        ##not implemented
        #self.score = 0
        #self.time = 0
           
    def createButton(self, pygame, toState, asset, x, y, w, h):
        '''creates and returns a button with its artwork'''
        image = pygame.image.load(asset).convert()
        return Button(toState, image, x, y, w, h)

    def update(self, pygame, window, setStateFunc, isGameOver, isWin):
        '''HUD update loop: controls display of save/quit buttons or exit button based on current game state'''
        if self.btnSave == None:
            self.logo = pygame.image.load("minesweeper/assets/logo.png").convert() 
            self.logoRect = Rect((480/2)-150, -10, 300, 100)
            
            self.btnSave = self.createButton(pygame, ScreenState.SAVE, "minesweeper/assets/button_save.png", 100, 85, 75, 30)
            self.btnQuit = self.createButton(pygame, ScreenState.INTRO, "minesweeper/assets/button_quit2.png", 300, 85, 75, 30)            
            self.btnExit = self.createButton(pygame, ScreenState.INTRO, "minesweeper/assets/button_exit.png", (480/2)-37, 85, 75, 30)
            
            self.font = pygame.font.Font(None, 80)
        
        window.blit(self.logo, [self.logoRect.x, self.logoRect.y])
        
        # If the game is not over, draw the save and quit buttons
        if not isGameOver:
            labelfont = pygame.font.Font(None, 22)       
            label = labelfont.render("Bombs: 18", True, (0,0,0)) 
            window.blit(label, ((480/2)-42, 70))
            
            self.btnSave.update(pygame, setStateFunc)
            self.btnQuit.update(pygame, setStateFunc)

            window.blit(self.btnSave.image, [self.btnSave.rect.x, self.btnSave.rect.y])
            window.blit(self.btnQuit.image, [self.btnQuit.rect.x, self.btnQuit.rect.y])
        else:
            self.btnExit.update(pygame, setStateFunc)        
            window.blit(self.btnExit.image, [self.btnExit.rect.x, self.btnExit.rect.y])
            
            # Draw whether the user Won or Lost
            color = (200,0,0)
            if not isWin:
                label2 = self.font.render("You Lose", True, (200,0,0)) 
                window.blit(label2, (114, 250))
            else:
                label3 = self.font.render("You Win", True, (0,200,0)) 
                window.blit(label3, (129, 250))
                color = (0, 200, 0)
                
            label = self.font.render("Game Over", True, color)
            window.blit(label, (84, 200))
