from cmu_graphics import drawPolygon, drawImage
from helper_functions import calculateCoordinates
from loadMusic import mainTheme
from loadImages import *

# Pyramid
def drawPyramid(app, board):
    for row in range(len(board)):
        drawRow(app, board, row)

def drawRow(app, board, row):
    nRow = board[row]
    for block in nRow:
        top, left, right = calculateCoordinates(app, block)
        drawBlock(top, left, right, block.mainColor, block.sideColors)

def drawBlock(topCoordinates, leftSideCoordinates, rightSideCoordinates, mainColor, sideColors):
    # drawing top
    drawPolygon(*topCoordinates, fill=mainColor, border='black', borderWidth=1)
    drawPolygon(*leftSideCoordinates, fill=sideColors[0], border='black', borderWidth = 1)
    drawPolygon(*rightSideCoordinates, fill=sideColors[1], border='black', borderWidth=1)

# Disks
def drawDisks(app):
    for disk in app.disks:
        cx, cy = disk.getCenter()
        drawImage(disk.image, cx, cy, align='center')

# Player
def drawPlayer(player):
    playerX, playerY = player.getCenter()
    drawImage(player.image, playerX, playerY, align='bottom')

# Enemies
def drawEnemies(app):
    for enemy in app.enemies:
        enemyX, enemyY = enemy.getCenter()
        drawImage(enemy.image, enemyX, enemyY, align='bottom')

# Interface
def drawInterface(app):
    # Player Label

    playerLabelX = app.labelMargin
    playerLabelY = app.labelMargin

    drawImage(playerLabelImage, playerLabelX, playerLabelY)

    # Score
    scoreX = playerLabelX
    scoreY = playerLabelY + 2 * app.labelMargin
    scoreImage = INTERFACE_BASE_IMAGE + f'Score{app.player.score}.png'
    drawImage(scoreImage, scoreX, scoreY)

    # Lives counter
    remainingLives = app.player.getLives()
    for life in range(remainingLives):
        lifeCx = scoreX + 1.5 * app.labelMargin * life
        lifeCy = scoreY + 2 * app.labelMargin
        drawImage(playerLifeImage, lifeCx, lifeCy)

    # Level
    levelX = app.width - 5 * app.labelMargin
    levelY = app.labelMargin
    levelWidth = 93
    drawImage(levelLabelImage, levelX, levelY)

    # Level Number
    numberMargin = 15
    levelNumberX = levelX + app.labelImageWidth + numberMargin 
    levelNumberY = levelY
    drawImage(INTERFACE_BASE_IMAGE+f'{app.level}.png', levelNumberX, levelNumberY)

    # Round
    roundX = levelX
    roundY = levelY + 40
    drawImage(roundLabelImage, roundX, roundY)

    # RoundNumber
    roundNumberX = roundX + app.labelImageWidth + numberMargin 
    roundNumberY = roundY
    drawImage(INTERFACE_BASE_IMAGE+f'{app.round}.png', roundNumberX, roundNumberY)

def drawSwear(app):
    playerCx, playerCy = app.player.getCenter()
    imageCx = playerCx - 0.8 * app.playerWidth
    imageCy = playerCy - 2.5 * app.playerHeight
    drawImage(swearImage, imageCx, imageCy)

def drawStartLevel(app):
    # Level
    levelWidth = 201
    levelHeight = 37
    levelTxtWidth = 37
    roundWidth = 127
    roundHeight = 20
    roundTxtWidth = 14

    levelCx = app.width // 2 - levelTxtWidth
    levelCy = app.height // 3 - roundHeight
    drawImage(startLevelImage, levelCx, levelCy, align='center')

    txtCx = levelCx + levelWidth // 2 + app.labelMargin
    txtCy = levelCy
    startLevelTxt = startLevelTxtImage + f'{app.level}.png'
    drawImage(startLevelTxt, txtCx, txtCy, align='center')

    # Round
    roundCx = app.width // 2 - roundTxtWidth
    roundCy = levelCy + levelHeight
    drawImage(startRound, roundCx, roundCy, align='center')

    roundTxtCx = roundCx + roundWidth // 2 + app.labelMargin
    roundTxtCy = roundCy
    startRoundTxt = startRoundTxtImage + f'{app.round}.png'
    drawImage(startRoundTxt, roundTxtCx, roundTxtCy, align='center')

    # Pyramid
    drawPyramid(app, app.startBoard)
    # Player
    drawPlayer(app.startPlayer)

def drawInstruction(app):
    # illustration
    # Pyramid
    drawPyramid(app, app.instructionBoard)
    # Player
    drawPlayer(app.instructionPlayer)

    stick = app.joysticksInstruction[app.instructionId]
    drawImage(stick.image, *stick.getCenter(), align='center')

    # Select Text
    selectHeight = 20
    selectTxtCx = app.width // 2
    selectTxtCy = app.height - selectHeight - app.labelMargin
    drawImage(selectInstructionImage, selectTxtCx, selectTxtCy, align='center')

def drawnHomeScreen(app):
    # background music
    mainTheme.play(loop=True)

    # drawStars(app)

    logoCx = app.width // 2 
    logoCy = app.height // 2 - 3 * app.labelMargin
    drawImage(logoImage, logoCx, logoCy, align='center')

    creditsCx = logoCx
    creditsCy = app.height - app.labelMargin
    drawImage(inspirationImage, creditsCx, creditsCy, align='center')

    drawClickButton(app)

    pressStartX = app.width // 2
    pressStartY = creditsCy - 3 * app.labelMargin
    drawImage(pressStartText, pressStartX, pressStartY, align='center')

def drawFinal(app):
    cx, cy = app.width // 2, app.height // 3
    drawImage(gameOverImage, cx, cy, align='center')

    # score
    scoreTextWidth = 50 
    scoreHeight = 29
    scoreWidth = 200
    scoreX = app.width // 2 - scoreTextWidth
    scoreY = cy + 2 * app.labelMargin
    drawImage(yourScoreImage, scoreX, scoreY, align='center')

    scoreX = scoreX + scoreWidth // 2 + 2 * app.labelMargin
    scoreY = scoreY
    scoreImage = INTERFACE_BASE_IMAGE + f'Score{app.player.score}.png'
    drawImage(scoreImage, scoreX, scoreY, align='center')

    # navigation
    continueX = cx
    continueY = scoreY + scoreHeight + app.labelMargin
    drawImage(continueText, continueX, continueY, align='center')

    gameOverX = cx 
    gameOverY = continueY + 2 * app.labelMargin
    drawImage(gameOverText, gameOverX, gameOverY, align='center')

def drawClickButton(app):
    if app.playButtonState == 'off':
        drawImage(playBtnHollowImage, app.width//2, app.height//2, align='center')
        drawImage(playBtnTextImageF, app.width//2, app.height//2, align='center')
    elif app.playButtonState == 'on':
        drawImage(playBtnImage, app.width//2, app.height//2, align='center')
        drawImage(playBtnTextImageS, app.width//2, app.height//2, align='center')

def drawEndScreen(app):
    # thank you text
    thankX = app.width // 2
    thankY = app.height // 4
    drawImage(thankImage, thankX, thankY, align='center')
    
    scoreHeight = 29
    scoreWidth = 200
    scoreX = app.width // 2 
    scoreY = thankY + 2 * app.labelMargin
    drawImage(yourScoreImage, scoreX, scoreY, align='center')

    scoreX = scoreX + scoreWidth // 2 + app.labelMargin
    scoreY = scoreY
    scoreImage = INTERFACE_BASE_IMAGE + f'Score{app.player.score}.png'
    drawImage(scoreImage, scoreX, scoreY, align='center')

    # navigation 
    navigationImageHeight = 20

    returnX = app.width // 2
    returnY = app.height // 2 - navigationImageHeight
    drawImage(returnImage, returnX, returnY, align='center')

    exitX = app.width // 2
    exitY = app.height // 2 + navigationImageHeight + app.labelMargin
    drawImage(exitImage, exitX, exitY, align='center')

    # credits
    creatorHeight = 37
    creatorClassHeight = 22
    creatorX = app.width // 2
    creatorY = app.height - creatorHeight - creatorClassHeight - app.labelMargin
    drawImage(creator, creatorX, creatorY, align='center')

    creatorClassX = app.width // 2
    creatorClassY = creatorY + creatorHeight
    drawImage(creatorClass, creatorClassX, creatorClassY, align='center')