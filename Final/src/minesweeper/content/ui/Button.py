#Justin Orr
#Final Project
#Python: 3.6.1

'''The Button module defines custom events for creating and clicking an image as a button'''

try:
    from pygame.locals import Rect
except:
    print("Error importing Rect module from pygame.locals")

class Button():    
    '''Manages Button creation and click events'''
    def __init__(self, toState, image, x, y, w, h):
        '''Initializes button's draw rectangle, image, isDown state and click event transition state'''
        self.rect = Rect(x,y,w,h)
        self.image = image
        
        self.toState = toState        
        self.isDown = False
        
    def checkCollision(self, mousePos):
        '''Checks if the current mouse position is inside the button's rectangle'''
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False
    
    def checkClicked(self, pygame):
        '''Checks if the current mouse is inside the button and a left click has occurred'''
        mousePos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if self.checkCollision(mousePos) and click[0] == 1:
            return True
        else:
            return False
    
    def update(self, pygame, stateFunc):
        '''button's update loop: constantly checks for click events'''
        click = pygame.mouse.get_pressed()
        if self.checkClicked(pygame):
            self.isDown = True
        elif self.isDown and click[0] == 0:
            stateFunc(self.toState)
            self.isDown = False  
            