import math
from random import randint
from models import Block, Star

def calculateDistance(size):
    return size // (2**0.5)

def getDimenstions():
    rows = 6
    blockSize = 45
    radius = (2**0.5) * blockSize // 2
    margin = 25
    return (rows, blockSize, radius, margin)

def createBoard(app, rows, offsetY, offsetX=0, sideColors=['cadetBlue', 'slateGray']):
    board = []
    for row in range(1, rows+1):
        numOfBlocks = row
        currentNumOfBlocks = numOfBlocks
        blocks = []

        for col in range(numOfBlocks):
            centerX = 0
            if row % 2 != 0:
                centerX += offsetX + app.width//2 + app.radius * (col - currentNumOfBlocks + 1)
            else:
                centerX += offsetX + app.width//2 + app.radius * (col - currentNumOfBlocks + 1)
            currentNumOfBlocks -= 1
            centerY = offsetY + app.margin + (app.radius // 2) * row + app.blockSize * (row - 1)
            # every time you create a block
            # we need to create an alien block for the special enemies
            # that move on the sides of the block
            block = Block(tag=f'block', center=(centerX, centerY), 
                          position=(row-1, col), mainColor=app.mainColor, 
                          sideColors=sideColors)
            blocks.append(block)
        board.append(blocks)
    return board

def calculateCoordinates(app, block):
    centerX, centerY = block.getCenter()
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

    # save center coordinates for the left side of the block
    leftSideCenter = findSideCenter(leftCoordinates, app.blockSize)
    block.sideCenter = [leftSideCenter]

    # coordinates of 4 points of the right side of the block

    rightX1 = rightX4 = topX4
    rightX2 = rightX3 = topX3

    rightY1 = topY4
    rightY2 = topY3
    rightY3 = rightY2 + app.blockSize
    rightY4 = rightY1 + app.blockSize
    rightCoordinates = [rightX1, rightY1, rightX2, rightY2, rightX3, rightY3, rightX4, rightY4]

    rightSideCenter = findSideCenter(rightCoordinates, app.radius)
    block.sideCenter.append(rightSideCenter)

    return (topCoordinates, leftCoordinates, rightCoordinates)

def isPositionLegal(app, row, col):
    # We take the absolute value of col since negative values
    # will always be lower than the row, which is always positive
    if row < len(app.board) and 0 <= col <= row:
        return True
    return False

def randomEnemySelection(enemies):
    numberOfEnemies = len(enemies)
    randomIndex = 0

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
    
# def getBonusData(app):
#     bonuses = {}
#     for l in range(app.levels):
#         levelName = f'Level{l+1}'
#         for _ in range(3):
#             bonuses[levelName] = bonuses.get(levelName, [])
#             bonuses[levelName].append(app.completionBonus)
#             if app.completionBonus < app.maxBonus:
#                 app.completionBonus += app.addBonus
#     return bonuses

def generateStars(app, maxCap: int, image: str):
    stars = []
    for _ in range(maxCap):
        starCx = randint(app.labelMargin, app.width - 2 * app.labelMargin)
        starCy = randint(app.labelMargin, app.height - 2 * app.labelMargin)
        star = Star(f'star', (starCx, starCy), image)
        stars.append(star)
    return stars

def calculateDistance(x1, x2, y1, y2):
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def findBlockByCenter(board, center):
    for row in len(board):
        for col in len(board[row]):
            block = board[row][col]
            if block.getCenter() == center:
                return block
            
def findSideCenter(coordinates: list, blockSize: int):
    """
    We have the radius of the block.
    
    If we add x1 and the blockSize // 2, then we get
    the x coordinate of the center.

    If we add y1 and the blockSize // 2, then we get
    the y coordinate of the center.
    """
    x1, y1, x2, y2, x3, y3, x4, y4 = coordinates
    midX = (x1 + x3) // 2
    midY = (y1 + y3) // 2
    return (midX, midY)