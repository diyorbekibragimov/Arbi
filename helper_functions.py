import copy
from random import randint
from models import Block

def calculateDistance(size):
    return size // (2**0.5)

def getDimenstions():
    rows = 8
    blockSize = 50
    radius = (2**0.5) * blockSize // 2
    margin = 25
    return (rows, blockSize, radius, margin)

def createBoard(app):
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
            block = Block(tag=f'block', center=(centerX, centerY), 
                          position=(row-1, col), mainColor=app.mainColor, 
                          sideColors=app.sideColors[app.level-1])
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

def randomEnemySelection(enemies):
    numberOfEnemies = len(enemies)
    randomIndex = randint(0, numberOfEnemies-1)
    return enemies[randomIndex]

# Source: ChatGPT
def findModelIndex(modelList: list, id: int):
    for modelIndex in range(len(modelList)):
        obj = modelList[modelIndex]
        if obj.id == id:
            return modelIndex

def countBlocks(pyramid: list):
    if len(pyramid) == 1:
        return 1
    else:
        return len(pyramid) + countBlocks(pyramid[1:])