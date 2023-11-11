from cmu_graphics import *

#################
# Helper functions
def calculateDistance(size):
    return size // (2**0.5)

def getDimenstions():
    rows = 7
    blockSize = 50
    radius = (2**0.5) * blockSize // 2
    margin = 25
    return (rows, blockSize, radius, margin)

def createBoard(app):
    Object.id = 0
    board = []
    for row in range(1, app.rows+1):
        numOfBlocks = row
        currentNumOfBlocks = numOfBlocks
        blocks = []

        for col in range(numOfBlocks):
            centerX = 0
            if row % 2 != 0:
                centerX += app.width//2 + app.radius * (col - currentNumOfBlocks + 1)
            else:
                centerX += app.width//2 + app.radius * (col - currentNumOfBlocks + 1)
            currentNumOfBlocks -= 1
            centerY = app.wrapperHeight//2 + app.margin + (app.radius // 2) * row + app.blockSize * (row - 1)

            block = Block(tag=f'block', center=(centerX, centerY), position=(row-1, col), colors=app.colors)
            blocks.append(block)
        board.append(blocks)
    return board

def calculateCoordinates(app, centerX, centerY):
    # coordinates of 4 points of the top side of the block
    topX1 = centerX - app.radius
    topX2 = centerX
    topX3 = centerX + app.radius
    topX4 = centerX

    topY1 = centerY
    topY2 = centerY - app.radius // 2
    topY3 = centerY
    topY4 = centerY + app.radius // 2
    topCoordinates = [topX1, topY1, topX2, topY2, topX3, topY3, topX4, topY4]

    # coordinates of 4 points of the left side of the block
    
    leftX1 = leftX4 = topX1
    leftX2 = leftX3 = topX4

    leftY1 = topY1
    leftY2 = topY4
    leftY3 = leftY2 + app.blockSize
    leftY4 = leftY1 + app.blockSize
    leftCoordinates = [leftX1, leftY1, leftX2, leftY2, leftX3, leftY3, leftX4, leftY4]

    # coordinates of 4 points of the right side of the block

    rightX1 = rightX4 = topX4
    rightX2 = rightX3 = topX3

    rightY1 = topY4
    rightY2 = topY3
    rightY3 = rightY2 + app.blockSize
    rightY4 = rightY1 + app.blockSize
    rightCoordinates = [rightX1, rightY1, rightX2, rightY2, rightX3, rightY3, rightX4, rightY4]
    return (topCoordinates, leftCoordinates, rightCoordinates)

def isPositionLegal(app, row, col):
    # We take the absolute value of col since negative values
    # will always be lower than the row, which is always positive
    if row < len(app.board) and 0 <= col <= row:
        return True
    return False

# TODO: continue watching https://www.youtube.com/watch?v=M6e3_8LHc7A
# to learn how to work with sprites

# TODO: then watch https://www.youtube.com/watch?v=nXOVcOBqFwM
# to learn how to animate sprites

#################

################

# Models

class Object():
    id = 0
    def __init__(self, tag: str, center: tuple) -> None:
        self.tag = f'{tag}{Object.id}'
        self.center = center # coordinates of the center of the object
        Object.id += 1
    
    def __repr__(self) -> str:
        return f"{self.tag} at {self.center}"

    def getCenter(self) -> tuple:
        return self.center

class Block(Object):
    def __init__(self, tag: str, center: tuple, position: tuple, colors: list) -> None:
        super().__init__(tag, center)
        self.position = position
        self.colors = colors

class Player(Object):
    def __init__(self, tag: str, center: tuple, currentBlock: Block) -> None:
        super().__init__(tag, center)
        self.currentBlock = currentBlock

################

def onAppStart(app):
    # Private
    __playerSpriteSheetURL = 'media/player.png'
    __playerImageSize = 24

    # Global
    app.colors = ['slateBlue', 'lightGreen', 'darkGreen']
    app.targetColor = 'yellow'
    app.rows, app.blockSize, app.radius, app.margin = getDimenstions()
    app.wrapperWidth = (app.rows + 1) * app.blockSize
    app.wrapperHeight = app.rows * app.blockSize + 2 * app.margin
    app.board = createBoard(app)
    # player starts on the highest col of the pyramid
    app.player = Player('player', app.board[0][0].getCenter(), app.board[0][0])
    app.playerSpiteSheetImage = (__playerSpriteSheetURL, *app.player.center)
    app.playerStates = ['idle', 'jumping']
    app.playerState = app.playerStates[0]
    app.allowedMovementKeys = ['down', 'right', 'up', 'left']
    app.elevationAngle = 0.5

def redrawAll(app):
    drawPyramid(app)
    drawPlayer(app)
    drawImage(*app.playerSpiteSheetImage)

def onStep(app):
    # if the state of player is jumping
    if app.playerState == app.playerStates[1]:
        # playerJump(app)
        pass

def onKeyPress(app, key):

    if key == 'r':
        onAppStart(app)

    if key in app.allowedMovementKeys:
        app.playerState = app.playerStates[1]
        playerJump(app, key)

# Pyramid

def drawPyramid(app):
    for row in range(len(app.board)):
        drawRow(app, row)

def drawRow(app, row):
    nRow = app.board[row]
    for block in nRow:
        centerX, centerY = block.center
        top, left, right = calculateCoordinates(app, centerX, centerY)
        drawBlock(top, left, right, block.colors)

def drawBlock(topCoordinates, leftSideCoordinates, rightSideCoordinates, colors):
    # drawing top
    drawPolygon(*topCoordinates, fill=colors[0], border='black', borderWidth=1)
    drawPolygon(*leftSideCoordinates, fill=colors[1], border='black', borderWidth = 1)
    drawPolygon(*rightSideCoordinates, fill=colors[2], border='black', borderWidth=1)

# Player

def drawPlayer(app):
    playerX, playerY = app.player.getCenter()
    drawRect(playerX, playerY, 15, 15, fill='black', align='center')

def playerJump(app, key):
    # first X coordinate of the player should reach the X0 coordinate of the parabola
    # this is a vertical line 
    # change will be 5 pixels
    row, col = app.player.currentBlock.position
    keyIndex = app.allowedMovementKeys.index(key)
    sign = +1 if key in ['down', 'right'] else -1
    nextRow, nextCol = row + sign, col + sign * (keyIndex % 2)
    if isPositionLegal(app, nextRow, nextCol):
        # if it is either down or right, then the row should increase
        # if it is either up or left, then the row should decrease
        # we mod by 2 because I want left and up to be indexed from 0 to 1, and not from 2 to 3
        # I find the indexes simply by looking their indexes in the app.allowedMovementKeys
        # I think there is a better and, perhaps, clearer way of finding the the index, though.
        nextBlock = app.board[nextRow][nextCol]
        app.player.currentBlock = nextBlock
        app.player.center = nextBlock.center
        print(nextBlock)
    else:
        # the player will fall out of the pyramid
        print("Falling")

def playGame():
    rows, blockSize, radius, margin = getDimenstions()

    wrapperWidth = (rows + 1) * blockSize
    wrapperHeight = rows * blockSize + (rows + 1) * radius + 2 * margin

    width = wrapperWidth * 2
    height = int(wrapperHeight * 1.5)
    runApp(width=width, height=height)

def main():
    playGame()

if __name__ == "__main__":
    main()