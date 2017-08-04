#Justin Orr
#Final Project
#Python: 3.6.1

'''The util defines any modules that could be needed in multiple modules'''

try:
    from enum import Enum
except:
    print("Error importing Enum module from enum")

class ScreenState(Enum):
    '''Defines the current Screen State for the game logic'''
    INTRO = 0,
    SELECT = 1,
    LOAD = 2,
    GAME = 3,
    SAVE = 4,
    HIGHSCORE = 5,
    QUIT = 6
    