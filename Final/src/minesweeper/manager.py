#Justin Orr
#Final Project
#Python: 3.6.1

'''The manager defines the screen manager as well as each available screen'''

try:
    from pygame.locals import Rect
except:
    print("Error importing Rect module from pygame.locals")
    
try:    
    from minesweeper.util import *
except:
    print("Error importing * from minesweeper.util")

try:
    from minesweeper.content.board.Board import Board
except:
    print("Error importing Board module from minesweeper.content.board.Board")

try:
    from minesweeper.content.ui.Button import Button
except:
    print("Error importing Button module from minesweeper.content.ui.Button")

try:
    from minesweeper.content.ui.HUD import HUD
except:
    print("Error importing HUD module from minesweeper.content.ui.HUD")

class ScreenManager():
    '''Manages the screens to be displayed based on the current screen state'''
    def __init__(self):
        '''Initializes default screen state as well as possible screens (Intro, Game, etc.)'''
        self.state = ScreenState.INTRO
        
        self.Intro = None
        self.Game = None
        self.HScores = None
    
    def checkDrawIntro(self):
        '''Checks whether the Intro screen should still be drawn based on current screen state'''
        if self.state == ScreenState.INTRO or self.state == ScreenState.SELECT or self.state == ScreenState.HIGHSCORE:
            return True
        else:
            return False
        
    def update(self, pygame, window):
        '''manager update loop: controls flow to current screen that should be updating/drawn'''
        if self.checkDrawIntro():
            self.drawIntro(pygame, window)
            
        elif self.state == ScreenState.GAME or self.state == ScreenState.LOAD:                
            self.drawGame(pygame, window)
            
        elif self.state == ScreenState.SAVE:
            self.Game.saveGame()
            self.setState(ScreenState.INTRO)
            
    def checkQuit(self):
        '''Checks if the QUIT state has been set'''
        return (self.state == ScreenState.QUIT)
    
    def setState(self, state):
        '''sets the current screen state and clears out no longer needed screens'''
        if not state == ScreenState.INTRO and not state == ScreenState.SELECT:
            self.Intro = None
            
        if not state == ScreenState.GAME and not state == ScreenState.SAVE:
            self.Game = None
            
        self.state = state
    
    def drawIntro(self, pygame, window):
        '''initializes the intro screen (if needed) and passes control to intro's update method'''
        if self.Intro == None:
            self.Intro = IntroScreen()
            self.Intro.InitUI(pygame)
            
        self.Intro.update(pygame, window, self.state, self.setState)
    
    def drawGame(self, pygame, window):
        '''initializes the game screen (if needed) and passes control to game's update method'''
        if self.Game == None:
            level = None
            if self.state == ScreenState.LOAD:
                level = self.loadGame()
                self.setState(ScreenState.GAME)
            self.Game = GameScreen(level)
            
        self.Game.update(pygame, window, self.setState)
        
    def loadGame(self):
        '''loads and returns a previous save; to be passed to game screen initialization'''
        return Board.loadBoard()
        
class IntroScreen():
    '''Manages and draws the Intro Screen; this includes the save and load screen'''
    def __init__(self):        
        '''Initializes default Intro screen buttons and artwork'''
        # LOGO
        self.logo = None
        self.logoRect = None
        
        # INTRO
        self.btnPlay = None
        self.btnScores = None
        self.btnQuit = None
        
        self.btnBack = None
        
        # SELECT
        self.btnNew = None
        self.btnLoad = None
    
    def InitUI(self, pygame):
        '''loads and creates default buttons and artwork'''
        # LOGO
        self.logo = pygame.image.load("minesweeper/assets/logo.png").convert() 
        self.logoRect = Rect((480/2)-150, 50, 300, 100)
        
        # INTRO
        self.btnPlay = self.createButton(pygame, ScreenState.SELECT, "minesweeper/assets/button_play.png", (480/2)-62, 200, 125, 50)
        self.btnScores = self.createButton(pygame, ScreenState.HIGHSCORE, "minesweeper/assets/button_scores.png", (480/2)-62, 275, 125, 50)
        self.btnQuit = self.createButton(pygame, ScreenState.QUIT, "minesweeper/assets/button_quit.png", (480/2)-62, 275, 125, 50)#(480/2)-62, 350, 125, 50)
        
        self.btnBack = self.createButton(pygame, ScreenState.INTRO, "minesweeper/assets/button_back.png", 15, 15, 30, 30)
        
        # SELECT
        self.btnNew = self.createButton(pygame, ScreenState.GAME, "minesweeper/assets/button_newgame.png", (480/2)-62, 200, 125, 50)
        self.btnLoad = self.createButton(pygame, ScreenState.LOAD, "minesweeper/assets/button_loadgame.png", (480/2)-62, 275, 125, 50)
           
    def createButton(self, pygame, toState, asset, x, y, w, h):
        '''creates and returns a button with its artwork'''
        image = pygame.image.load(asset).convert()
        return Button(toState, image, x, y, w, h)
        
    def update(self, pygame, window, state, setStateFunc):
        '''intro update loop: controls flow between all screens under the intro umbrella'''
        if state == ScreenState.INTRO:
            self.updateIntro(pygame, window, setStateFunc)
        elif state == ScreenState.SELECT:
            self.updateSelect(pygame, window, setStateFunc)
        else:
            self.updateHS(pygame, window, setStateFunc)
    
    def updateIntro(self, pygame, window, setStateFunc):
        '''start screen intro loop: draws buttons and artwork'''
        self.btnPlay.update(pygame, setStateFunc)
        self.btnScores.update(pygame, setStateFunc)
        self.btnQuit.update(pygame, setStateFunc)
        
        window.blit(self.logo, [self.logoRect.x, self.logoRect.y])
                    
        window.blit(self.btnPlay.image, [self.btnPlay.rect.x, self.btnPlay.rect.y])
        #window.blit(self.btnScores.image, [self.btnScores.rect.x, self.btnScores.rect.y])
        window.blit(self.btnQuit.image, [self.btnQuit.rect.x, self.btnQuit.rect.y])
        
    def updateSelect(self, pygame, window, setStateFunc):
        '''New/Load screen loop: draws buttons and artwork'''
        self.btnNew.update(pygame, setStateFunc)
        self.btnLoad.update(pygame, setStateFunc)
        
        self.btnBack.update(pygame, setStateFunc)
            
        window.blit(self.logo, [self.logoRect.x, self.logoRect.y])
        
        window.blit(self.btnBack.image, [self.btnBack.rect.x, self.btnBack.rect.y])       
                 
        window.blit(self.btnNew.image, [self.btnNew.rect.x, self.btnNew.rect.y])            
        window.blit(self.btnLoad.image, [self.btnLoad.rect.x, self.btnLoad.rect.y])
    
    def updateHS(self, pygame, window, setStateFunc):
        '''(not implemented) HighScore screen loop: draws buttons and artwork'''
        self.btnBack.update(pygame, setStateFunc)
        
        window.blit(self.btnBack.image, [self.btnBack.rect.x, self.btnBack.rect.y])
        
class GameScreen():
    '''Manages and draws the Game Screen; this controls the physical game play'''
    def __init__(self, level=None):        
        '''Initializes default Game screen's level, HUD, and game board'''
        self.level = level
        self.loaded = False
        
        self.hud = HUD()
        self.board = Board()
        
    def update(self, pygame, window, setStateFunc):
        '''game screen update loop: controls game logic and exit/save events'''
        if self.loaded == False:
            self.board.createBoard(self.level)
            self.loaded = True
            
        self.board.update(pygame, window)
        self.hud.update(pygame, window, setStateFunc, self.board.isOver, self.board.isWin)
        
    def saveGame(self):
        '''calls board's save method to save the current game state to XML'''
        self.board.saveBoard()
