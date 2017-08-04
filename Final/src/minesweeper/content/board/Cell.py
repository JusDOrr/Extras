#Justin Orr
#Final Project
#Python: 3.6.1

'''The Cell module defines a single cell in the game board; essentially these are modified buttons'''

try:
    from pygame.locals import Rect
except:
    print("Error importing Rect module from pygame.locals")

try:
    from xml.etree.ElementTree import SubElement
except:
    print("Error importing SubElement module from xml.etree.ElementTree")

class Cell():
    '''Manages the Cell's state, values, and event logic''' 
    def __init__(self, x=0, y=0, w=0, h=0, xLoc=0, yLoc=0): 
        '''Initializes the cell's location, image, font, grid location, and game values'''       
        self.rect = Rect(x,y,w,h)
        self.image = None
        self.flippedImage = None
        self.font = None
        
        self.xLoc = xLoc
        self.yLoc = yLoc
        
        self.isVisible = False
        self.isBomb = False
        
        self.justDown = False
        self.isDown = False
        
        self.value = 0
        
        # Flagging a Cell
        self.isFlagged = False
        self.isRightDown = False
    
    def createXMLElement(self, parent):
        '''generates an XML element that represents the given Cell'''   
        element = SubElement(parent, "Cell")
        element.attrib = {"rX":str(self.rect.x),"rY":str(self.rect.y),"rW":str(self.rect.w),"rH":str(self.rect.h),"X":str(self.xLoc),"Y":str(self.yLoc),"isFlagged":str(self.isFlagged), "isVisible":str(self.isVisible), "isBomb":str(self.isBomb), "value":str(self.value)}
    
    def createCell(self, xmlNode):
        '''generates a Cell from a given Cell XML Element'''

        try:
            x = int(xmlNode.attrib["rX"])
            y = int(xmlNode.attrib["rY"])
            w = int(xmlNode.attrib["rW"])
            h = int(xmlNode.attrib["rH"]) 
            self.rect = Rect(x,y,w,h)
            
            self.xLoc = int(xmlNode.attrib["X"])
            self.yLoc = int(xmlNode.attrib["Y"])
            
            flag = xmlNode.attrib["isFlagged"]
            if flag == "False":
                self.isFlagged = False
            else:
                self.isFlagged = True
            
            vis = xmlNode.attrib["isVisible"]
            if vis == "False":
                self.isVisible = False
            else:
                self.isVisible = True
                
            bomb = xmlNode.attrib["isBomb"]
            if bomb == "False":
                self.isBomb = False
            else:
                self.isBomb = True
            
            temp = xmlNode.attrib["value"]
            if not temp == "X":
                temp = int(temp)            
            self.value = temp
        except:
            return False
        
        return True
        
    def checkCollision(self, mousePos):
        '''Checks if the mouse position is contained within the cell's rectangle''' 
        if self.rect.collidepoint(mousePos):
            return True
        else:
            return False
    
    def setVisible(self):
        '''sets the cell as visible and changes the artwork representing the cell'''
        self.isFlagged = False
        self.isVisible = True
        self.image = self.flippedImage    
        self.justDown = False
    
    def update(self, pygame, window, isGameOver):
        '''Cell update loop: checks for click events and manages content visibility''' 
        text = ""
        
        # Check if the artwork needs to be initialized
        if self.image == None:
            self.font = pygame.font.Font(None, 42)
            self.flippedImage = pygame.image.load("minesweeper/assets/button_flipped.png").convert()
            
            if self.isVisible and not self.isBomb:
                self.image = self.flippedImage
            else:
                self.image = pygame.image.load("minesweeper/assets/button_normal.png").convert()
        
        # If not visible (and game not over) check if the state needs to be updated        
        if not self.isVisible and not isGameOver:
            mousePos = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            
            # Check Right Click Events
            if self.checkCollision(mousePos) and click[2] == 1 and not self.isRightDown:
                self.isFlagged = (not self.isFlagged)
                self.isRightDown = True
            elif self.checkCollision(mousePos) and click[2] == 0 and self.isRightDown:
                self.isRightDown = False
                
            # Check Left Click Events
            elif self.checkCollision(mousePos) and click[0] == 1:
                self.isDown = True
            elif self.checkCollision(mousePos) and click[0] == 0 and self.isDown:                
                self.justDown = True
                self.isDown = False
            else:
                self.isDown = False
        else:
            if self.justDown:
                self.setVisible()
                
            if not self.value == 0:
                text = str(self.value)
            
        # Button Image
        window.blit(self.image, [self.rect.x, self.rect.y])  
        
        if self.isFlagged:
            # Flag Value
            label = self.font.render("?", True, (0,0,0))
            window.blit(label, (self.rect.x + 9, self.rect.y + 5))            
        else:    
            # Text Value
            label = self.font.render(text, True, (0,0,0))  
            window.blit(label, (self.rect.x + 9, self.rect.y + 5))    
        