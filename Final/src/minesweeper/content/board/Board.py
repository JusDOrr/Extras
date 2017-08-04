#Justin Orr
#Final Project
#Python: 3.6.1

'''The Board module defines the game play and control the game board'''

try:
    from random import randint
except:
    print("Error importing randint module from random")

try:    
    from collections import deque
except:
    print("Error importing deque module from collections")

try:
    from xml.etree import ElementTree
except:
    print("Error importing ElementTree module from xml.etree")
    
try:
    from xml.etree.ElementTree import Element, SubElement, tostring
except:
    print("Error importing Element, SubElement, and/or tostring modules from xml.etree.ElementTree")
    
try:
    from xml.dom import minidom
except:
    print("Error importing minidom module from xml.dom")

try:
    from minesweeper.content.board.Cell import Cell
except:
    print("Error importing Cell module from minesweeper.content.board.Cell")

class Board():
    '''Manages the Board state and all game play logic''' 
    def __init__(self):
        '''Initializes the board, remaining cells, and game over logic'''
        self.board = None
        
        self.remaining = 0 
        self.isWin = False       
        self.isOver = False
    
    def createBoard(self, board=None):
        '''creates a new game board; if a board is provided via load, it re-initializes the saved board'''
        self.remaining = 81
        if board == None:
            self.generateBoard()
        else:
            self.board = board
            for row in self.board:
                for cell in row:
                    if cell.isVisible:
                        self.remaining -= 1
            
    @staticmethod
    def loadBoard():
        '''loads the saved game board (if one exists) from the recentsave.xml file'''
        level = None
        
        try:
            with open("minesweeper/recentsave.xml", "r") as xml_file:
                boardElement = ElementTree.parse(xml_file)
            
            level = []    
            for cells in boardElement.findall(".//Row"):
                row = []
                for node in cells.findall(".//Cell"):
                    cell = Cell()
                    if cell.createCell(node):
                        row.append(cell)
                    else:
                        # Failed to load a cell
                        raise Exception("Failed to load a cell")
                        
                level.append(row)
                
        except:
            level = None
        
        return level
     
    def saveBoard(self):
        '''builds the current game board into an XML format and saves to the recentsave.xml file'''
        root = Element("Board")
    
        for row in self.board:
            element = SubElement(root, "Row")
            for cell in row:
                cell.createXMLElement(element)
    
        parsedRoot = minidom.parseString(tostring(root))
        prettyRoot = parsedRoot.toprettyxml(indent="    ")
    
        with open("minesweeper/recentsave.xml", "w") as xml_file:
            xml_file.write(prettyRoot)
        
    def update(self, pygame, window):
        '''game board update loop: checks the state of all 81 cells and checks for win/loss conditions'''
        for y in range(0, 9):
            for x in range (0, 9):
                cell = self.board[x][y]
                if cell.justDown:
                    if cell.isBomb:
                        self.GameOver()
                    elif cell.value == 0:
                        self.floodShow(x, y)
                    else:
                        self.setCellVisible(cell)
                                        
                cell.update(pygame, window, self.isOver)
        
        self.checkWin()
    
    def setCellVisible(self, cell):
        '''calls the cell's set visible method as well as updates the remaining cell count'''
        self.remaining -= 1
        cell.setVisible()
    
    def checkWin(self):
        '''checks if only the 18 bombs are still not visible'''
        if self.remaining == 18:
            self.Win()
    
    def Win(self):
        '''sets the appropriate conditions for a win state'''
        self.isOver = True
        self.isWin = True
           
    def GameOver(self):
        '''sets the appropriate conditions for a loss state'''
        self.isOver = True
        self.isWin = False
            
    def floodShow(self, x, y):
        '''uses the given coordinates to run a breadth first search algorithm to show all connected empty cells and there adjacent values'''
        que = deque([])
        
        cell = self.board[x][y]
        que.append(cell)
        
        while not len(que) == 0:
            cell = que.popleft()
            
            if cell.isVisible:
                continue
            
            x = cell.xLoc
            y = cell.yLoc
            
            # LEFT
            self.checkShow(que, x-1, y)
            # RIGHT
            self.checkShow(que, x+1, y)
            # DOWN
            self.checkShow(que, x, y-1)
            # UP
            self.checkShow(que, x, y+1)
            
            # DOWN-LEFT
            self.checkShow(que, x-1, y+1)
            # UP-LEFT
            self.checkShow(que, x-1, y-1)
            # DOWN-RIGHT
            self.checkShow(que, x+1, y+1)
            # UP-RIGHT
            self.checkShow(que, x+1, y-1)
            
            self.setCellVisible(cell)
            
    def checkShow(self, q, x, y):
        '''checks if the given cell coordinates are either in need of being visible or need to be added to the Queue for further flood fill'''
        if x >= 0 and x < 9 and y >= 0 and y < 9:
            cell = self.board[x][y]
            if (not cell.isVisible):
                if cell.value == 0:
                    q.append(cell)
                else:
                    self.setCellVisible(cell)
    
    def generateBoard(self):
        '''initializes a new board of 9x9 cells and then calls a method to randomly generate 18 bombs'''
        w, h = 9, 9
        startLocX = 45
        startLocY = 90
        offset = 35        
        
        # Build the board
        self.board = []
        row = []
        for y in range(0, 9):
            for x in range (0, 9):
                cell = Cell(startLocX + (offset * (x+1)), startLocY + (offset * (y+1)), 35, 35, y, x)
                row.append(cell)
                
            self.board.append(row)
            row = []
                
        # Generate Bombs and Values
        self.generateBombs()
    
    def generateBombs(self):
        '''calls the generate bomb method 18 times'''
        for x in range(0, 18):
            self.generateBomb()
            
    def generateBomb(self):
        '''searches for a cell that is not already a bomb and increments all the adjacent cells'''
        randX, randY = 0, 0
        found = False
        
        while not found:
            randX = randint(0, 8)
            randY = randint(0, 8)
            cell = self.board[randX][randY]
            if not cell.isBomb:
                cell.isBomb = True
                cell.value = "X"
                found = True
                
        self.generateNumbers(randX, randY)
        
    def generateNumbers(self, x, y):
        '''checks all adjacent cells to the given coordinates and increments value if applicable'''
        if self.isValid(x-1, y-1):
            self.board[x-1][y-1].value += 1
        if self.isValid(x-1, y):
            self.board[x-1][y].value += 1
        if self.isValid(x-1, y+1):
            self.board[x-1][y+1].value += 1
            
        if self.isValid(x+1, y-1):
            self.board[x+1][y-1].value += 1
        if self.isValid(x+1, y):
            self.board[x+1][y].value += 1
        if self.isValid(x+1, y+1):
            self.board[x+1][y+1].value += 1
            
        if self.isValid(x, y-1):
            self.board[x][y-1].value += 1
        if self.isValid(x, y+1):
            self.board[x][y+1].value += 1
        
    def isValid(self, x, y):
        '''checks if the coordinates is a valid value between 0 and 9 and is not already a bomb'''
        if x >= 0 and x < 9 and y >= 0 and y < 9:
            cell = self.board[x][y]
            if not cell.isBomb:
                return True
            
        return False
        