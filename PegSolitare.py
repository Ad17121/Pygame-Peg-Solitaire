import pygame
import math

pygame.init()

#Font

myFont = pygame.font.SysFont("Calibri", 50)

#? Colour Constants

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (22, 219, 42)
BLUE = (0,77,255)
GREY = (175,175,175)

#? Screen

screenWidth = 360
screenHeight = 360

#? Circle

class circle:
    def __init__(self, x, y, radius, gridX, gridY,  color=BLACK, width=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.width = width
        self.color = color
        self.visible = True
        self.gridX = gridX
        self.gridY = gridY
        self.oldX = 0
        self.oldY = 0
        self.oldGridX = 0
        self.oldGridY = 0

    def draw(self):
        if self.visible:
            pygame.draw.circle(window,self.color,(self.x,self.y),self.radius, self.width)

    def mouseOver(self):
        if self.visible:
            mouseX, mouseY = pygame.mouse.get_pos()
            if math.sqrt((mouseX-self.x)**2 + (mouseY-self.y)**2) < self.radius:
                return True


window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Test")

#? Create background grid

def drawGrid():
    global circles

    width, height, margin, color = 40, 40, 10, GREY
    circles = []
    
    for row in range(7):
        for column in range(7):
            circles.append(circle((0 + width * column)+margin*column+margin+20, (0 + height * row)+margin*row+margin+20, 20, column, row, color))
            if not (row < 2 and column < 2) and not (row > 4 and column > 4) and not (row > 4 and column < 2) and not (row < 2 and column > 4):
                circles[-1].draw()



def updateDisplay():
    window.fill(WHITE)
    drawGrid()
    for piece in pieces:
        piece.draw()
    pygame.display.update()


#? Displays end of game message
def GameOver(state):
    running = True
    while running:

        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                running = False

        if state.lower() == "win":
            textSurface = myFont.render("You Win!", True, GREEN, WHITE)
            
        elif state.lower() == "lose":
            textSurface = myFont.render("Try Again!", True, RED, WHITE)
            
            
        window.blit(textSurface,(screenWidth//2 - 90,screenHeight//2 - myFont.get_height()))
        pygame.display.update()
         

width, height, margin, color = 40, 40, 10, BLUE
circles = []

#? Main loop
drawGrid()

#? Place pieces
pieces = []
for row in range(7):
        for column in range(7):
            if not (row == 3 and column == 3):
                pieces.append(circle((0 + width * column)+margin*column+margin+20, (0 + height * row)+margin*row+margin+20, 20,column, row, color))
                if (row < 2 and column < 2) or (row > 4 and column > 4) or (row > 4 and column < 2) or (row < 2 and column > 4):
                    pieces[-1].visible = False
                pieces[-1].draw()

#? Remove missing pieces from board
for piece in pieces: 
    if not piece.visible:
        pieces.remove(piece)



running = True
holding = None
 
#? Create grid array
grid = []

def updateGrid():
    global grid
    grid = []
    for row in range(7):
        grid.append([])
        for column in range(7):
            grid[row].append("0")      

    for piece in pieces:
        if piece.visible:
            grid[piece.gridX][piece.gridY] = "1"
        else:
            grid[piece.gridX][piece.gridY] = "#"

    
updateGrid()

def movePeice(circle, holding):
    global isHolding
    holding.x, holding.y = circle.x, circle.y
    holding.gridX, holding.gridY = circle.gridX, circle.gridY    
    holding = None
    isHolding = False
    pieces.remove(piece)
    updateGrid()



#? Main loop
isHolding = False

while running:
    dragging = False
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False

    mouseDown = pygame.mouse.get_pressed()[0]

    mouseX, mouseY = pygame.mouse.get_pos()
    
    count = 0
    for piece in pieces:
        if piece.mouseOver() == True:
            count += 1

    if not count > 1:
        for piece in pieces:
            if piece.mouseOver() and mouseDown:
                piece.x, piece.y = mouseX, mouseY
                holding = piece
                for c in circles:
                    if c.mouseOver():
                        if not isHolding:
                            holding.oldX, holding.oldY = c.x, c.y
                            holding.oldGridX, holding.oldGridY = holding.gridX, holding.gridY
                    
                            isHolding = True
                            pass                 
    else:
        for piece in pieces:
            if holding == piece and mouseDown and piece.mouseOver():
                piece.x, piece.y = mouseX, mouseY

    possibleMoves = set()

    #? checks board for all posssible moves 
    for row in range(6):
        for column in range(6):
            if not row - 1 < 0:
                if grid[row][column] == "1" and grid[row-1][column] == "1" and grid[row+1][column] == "0":
                    possibleMoves.add((row+1,column))
                if grid[row][column] == "1" and grid[row-1][column] == "0" and grid[row+1][column] == "1":
                    possibleMoves.add((row-1,column))
            if not column - 1 < 0:
                if grid[row][column] == "1" and grid[row][column+1] == "1" and grid[row][column-1] == "0":
                    possibleMoves.add((row,column-1))
                if grid[row][column] == "1" and grid[row][column+1] == "0" and grid[row][column-1] == "1":
                    possibleMoves.add((row,column+1))
            if grid[6][2] == "1" and grid[6][3] == "1" and grid[6][4] == "0":
                possibleMoves.add((6,4))
            elif grid[6][4] == "1" and grid[6][3] == "1" and grid[6][2] == "0":
                possibleMoves.add((6,2))
            if grid[2][6] == "1" and grid[3][6] == "1" and grid[4][6] == "0":
                possibleMoves.add((4,6))
            elif grid[4][6] == "1" and grid[3][6] == "1" and grid[2][6] == "0":
                possibleMoves.add((2,6))

   
    if len(possibleMoves) == 0:
        
        if len(pieces) == 9 and grid[3][3] == "1":
            
            running = False
            GameOver("win")
        else:
            
            running = False
            GameOver("lose")

    for c in circles: 
        if grid[c.gridX][c.gridY] != "#":
            if c.mouseOver() and (c.gridX,c.gridY) in possibleMoves and holding != None:
                if not mouseDown:                
                    if c.gridX == holding.oldGridX - 2 and c.gridY == holding.oldGridY:
                        for piece in pieces:
                            if holding != None:
                                if piece.gridX == holding.oldGridX - 1 and piece.gridY == holding.oldGridY:
                                    movePeice(c, holding)
                                    
                    elif c.gridX == holding.oldGridX + 2 and c.gridY == holding.oldGridY:
                        for piece in pieces:
                            if holding != None:
                                if piece.gridX == holding.oldGridX + 1 and piece.gridY == holding.oldGridY:
                                    movePeice(c, holding)
                    elif c.gridY == holding.oldGridY - 2 and c.gridX == holding.oldGridX:
                        for piece in pieces:
                            if holding != None:
                                if piece.gridY == holding.oldGridY - 1 and piece.gridX == holding.oldGridX:
                                    movePeice(c, holding)
                    elif c.gridY == holding.oldGridY + 2 and c.gridX == holding.oldGridX:
                        for piece in pieces:
                            if holding != None:
                                if piece.gridY == holding.oldGridY +  1 and piece.gridX == holding.oldGridX: 
                                    movePeice(c, holding)
    if isHolding:
        if not mouseDown and holding != None:
            holding.x, holding.y = holding.oldX, holding.oldY
            holding.gridX, holding.gridY = holding.oldGridX, holding.oldGridY
            holding = None
            isHolding = False
            updateGrid()
    updateDisplay()


pygame.quit()