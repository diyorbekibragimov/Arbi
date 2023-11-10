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
    board = []
    counter = 0
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

            block = Block(tag=f'block{counter}', center=(centerX, centerY), colors=app.colors)
            blocks.append(block)
            counter += 1
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

#################

################

# Models

class Object():
    def __init__(self, tag: str, center: tuple) -> None:
        self.tag = tag
        self.center = center # coordinates of the center of the object
    
    def __repr__(self) -> str:
        return f"{self.tag} at {self.center}"
    
class Block(Object):
    def __init__(self, tag: str, center: tuple, colors: list) -> None:
        super().__init__(tag, center)
        self.colors = colors

################

def onAppStart(app):
    app.colors = ['slateBlue', 'lightGreen', 'darkGreen']
    app.targetColor = 'yellow'
    app.rows, app.blockSize, app.radius, app.margin = getDimenstions()
    app.wrapperWidth = (app.rows + 1) * app.blockSize
    app.wrapperHeight = app.rows * app.blockSize + 2 * app.margin
    app.board = createBoard(app)

def redrawAll(app):
    drawPyramid(app)

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
    drawPolygon(*topCoordinates, fill=colors[0], border='black')
    drawPolygon(*leftSideCoordinates, fill=colors[1], border='black')
    drawPolygon(*rightSideCoordinates, fill=colors[2], border='black')

def playGame(app):
    rows, blockSize, radius, margin = getDimenstions()

    wrapperWidth = (rows + 1) * blockSize
    wrapperHeight = rows * blockSize + (rows + 1) * radius + 2 * margin

    width = wrapperWidth * 2
    height = int(wrapperHeight * 1.5)
    runApp(width=width, height=height)

def main():
    playGame(app)

if __name__ == "__main__":
    main()