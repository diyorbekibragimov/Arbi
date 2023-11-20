from cmu_graphics import *
from models import (Player, Enemy)
from helper_functions import *

from random import randint
import time

# TODO: continue watching https://www.youtube.com/watch?v=M6e3_8LHc7A
# to learn how to work with sprites

# TODO: then watch https://www.youtube.com/watch?v=nXOVcOBqFwM
# to learn how to animate sprites

################

def onAppStart(app):
    app.background = 'black'

    # Global
    # Colors
    app.levels = 5
    app.level = 1
    app.rounds = 3
    app.round = 1

    # Initial Completion Bonus
    app.completionBonus = 250
    app.maxBonus = 5000
    # app.bonuses = getBonusData(app)
    # Bonus Animation
    app.bonusAnimationStart = None
    app.bonusAnimationDuration = 5

    app.mainColor = 'royalBlue'
    app.sideColors = [
        ['cadetBlue', 'slateGray']
    ]
    app.targetColors = ['yellow', 'blue', 'blueViolet']
    app.targetColor = app.targetColors[app.level-1]

    app.rows, app.blockSize, app.radius, app.margin = getDimenstions()
    app.wrapperWidth = (app.rows + 1) * app.blockSize
    app.wrapperHeight = app.rows * app.blockSize + 2 * app.margin
    app.board = createBoard(app)
    app.rawBlocks = countBlocks(app.board)

    # player starts on the highest col of the pyramid
    app.playerImageBase = 'media/spritesheet/player-'
    app.playerImage = app.playerImageBase + 'down-right-idle.png'
    app.playerLives = 3
    app.player = Player('player', app.board[0][0].getCenter(), app.board[0][0], 'right', app.playerImage, app.playerLives)
    app.playerStates = ['spawn', 'idle', 'jump']
    app.playerState = app.playerStates[0]
    app.playerNumber = 1

    # Image sources
    app.labelImageWidth = 93
    app.interfaceBaseImage = 'media/interface/' 
    # small image
    # NOTE: We can make the game resizable
    # if we do, we have to change the sizes of some pictures
    # such as logo
    app.logoImage = app.interfaceBaseImage + 'logo50.png'
    app.creditsImage = app.interfaceBaseImage + 'credits-3-15.png'
    app.playerLabelImage = app.interfaceBaseImage + 'player.png'
    app.playerLifeImage = app.interfaceBaseImage + 'player-small.png'
    app.levelLabelImage = app.interfaceBaseImage + 'level.png'
    app.roundLabelImage = app.interfaceBaseImage + 'round.png'    
    app.bonusTextImage = app.interfaceBaseImage + 'bonusText.png'
    app.bonusScoreImage = app.interfaceBaseImage + 'AddScore250.png'
    app.bonusPointsImage = app.interfaceBaseImage + 'bonusPoints.png'

    app.allowedMovementKeys = ['down', 'right', 'up', 'left']
    app.gameStates = ['start', 'inprogress', 'levelComplete', 'playerDied', 'pass']
    app.gameState = 'start'
    app.paused = False

    app.enemyTypes = ['red']
    app.enemyImageBase = 'media/spritesheet/enemies/'
    app.enemies = list()
    app.enemySpawnInterval = 5
    app.enemySpawned = False
    app.maximumEnemiesOnBoard = 3
    app.fixedInterval = 5
    app.initialTime = time.time()
    app.enemyControlInterval = 3
    app.fixedEnemyControlInterval = app.enemyControlInterval
    
    app.enemyImageChangeInterval = 0.3
    app.fixedEnemyImageChangeInterval = 0.3

    app.animationStartTime = None
    app.animationCount = 5
    app.animationInterval = 0.3
    app.animationFixedInterval = app.animationInterval

    app.playerDeathTime = None
    app.playerRevivalTime = 5

    app.gravity = 0.5

    # Level
    app.labelMargin = 30

def redrawAll(app):
    if app.gameState == 'start':
        drawnHomeScreen(app)
    else:
        drawPyramid(app)
        drawEnemies(app)
        drawPlayer(app)
        drawInterface(app)

    # if the level is complete, display animation
    if app.bonusAnimationStart is not None:
        getBonusAnimation(app)

def onStep(app):
    if not app.paused:
        if app.playerState == app.playerStates[0]:
            # if the player has just spawned, it needs
            # to fall into the topmost block on the pyramid
            # since at the initialization of the instance
            # of the player, the y coordinate of the player
            # is set to 100 - topBlock y coordinate
            # to create a simple animation of falling
            playerCX, playerCY = app.player.getCenter()
            _, currentBlockCY = app.player.block.getCenter()
            if playerCY != currentBlockCY:
                playerCY += 5
                app.player.changeCenter((playerCX, playerCY))
            else:
                app.playerState = app.playerStates[1] # the player is ready or idle.
                app.board[0][0].mainColor = app.targetColor
                app.rawBlocks -= 1
    
        checkBlockColors(app)
        enemyControls(app)
        
        # if the state of player is jumping
        if app.playerState == app.playerStates[2]:
            # playerJump(app)
            pass

        if app.gameState == app.gameStates[1]:
            elapsedTime = time.time() - app.initialTime
            if len(app.enemies) < app.maximumEnemiesOnBoard:
                if elapsedTime - app.enemySpawnInterval > 0:
                    enemy = spawnEnemy(app)
                    app.enemySpawnInterval += app.fixedInterval
                    app.enemies.append(enemy)
                    app.enemySpawned = True

        if app.enemySpawned:
            enemy = app.enemies[-1]
            enemyCX, enemyCY = enemy.getCenter()
            _, currentBlockCY = enemy.block.getCenter()
            if enemyCY != currentBlockCY:
                enemyCY += 5
                enemy.changeCenter((enemyCX, enemyCY))
            else:
                app.enenySpawned = False

    elif app.gameState == app.gameStates[1]:
        # if the game level is complete, display a short animation.
        elapsedTime = time.time() - app.animationStartTime
        if elapsedTime - app.animationCount < 0:
            if elapsedTime - app.animationInterval > 0:
                app.animationInterval += app.animationFixedInterval
                playLevelTransitionAnimation(app)
        else:
            # the animation is over
            nextGame(app)

    elif app.gameState == app.gameStates[2] \
            and app.playerDeathTime is not None \
            and app.playerLives > 0:
        # the player has died because of falling or collision with the enemy
        elapsedTime = time.time() - app.playerDeathTime
        if elapsedTime - app.playerRevivalTime > 0:
            # the player gets revived and the game continues
            # the progress and the position of the player does not change
            app.paused = False
            app.deathTime = None
            # the game state changes to 'inprogress'
            app.gameState = app.gameStates[1]
            # the enemies gets removed, giving a player a headstart
            app.enemies.clear()
            # the basically sort of 'restarts' with the initial time changing
            # to the current time.
            app.enemySpawnInterval += app.playerRevivalTime
    
    if app.playerLives == 0:
        onAppStart(app)

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)

    if key == 'enter':
        app.paused = not app.paused

    if not app.paused and app.playerState != app.playerStates[0]:
        if key in app.allowedMovementKeys:
            # the player is jumping
            app.playerState = app.playerStates[2]
            # if key == 'down':
            #     app.player.direction = 'down-left'
            # elif key == 'up':
            #     app.player.direction = 'up-right'
            # elif key == 'left':
            #     app.player.direction = 'up-left'
            # elif key == 'right':
            #     app.player.direction = 'down-right'
            # #app.player.image = app.playerImageBase + f'{app.player.direction}-{app.playerState}.png'
            app.playerState = app.playerStates[2]
            playerJump(app, key)

# Pyramid
def drawPyramid(app):
    for row in range(len(app.board)):
        drawRow(app, row)

def drawRow(app, row):
    nRow = app.board[row]
    for block in nRow:
        centerX, centerY = block.getCenter()
        top, left, right = calculateCoordinates(app, centerX, centerY)
        drawBlock(top, left, right, block.mainColor, block.sideColors)

def drawBlock(topCoordinates, leftSideCoordinates, rightSideCoordinates, mainColor, sideColors):
    # drawing top
    drawPolygon(*topCoordinates, fill=mainColor, border='black', borderWidth=1)
    drawPolygon(*leftSideCoordinates, fill=sideColors[0], border='black', borderWidth = 1)
    drawPolygon(*rightSideCoordinates, fill=sideColors[1], border='black', borderWidth=1)

# Player

def drawPlayer(app):
    playerX, playerY = app.player.getCenter()
    drawImage(app.player.image, playerX, playerY, align='bottom')

# Enemies

def drawEnemies(app):
    for enemy in app.enemies:
        enemyX, enemyY = enemy.getCenter()
        imageURL = app.enemyImageBase + f'{enemy.type}{enemy.imageId}.png'
        drawImage(imageURL, enemyX, enemyY, align='bottom')

# Interface

def drawInterface(app):
    # Player Label
    playerLabelText = 'PLAYER'

    playerLabelX = app.labelMargin
    playerLabelY = app.labelMargin

    playerLabelWidth = 24 * len(playerLabelText)
    drawImage(app.playerLabelImage, playerLabelX, playerLabelY)

    # Score
    scoreX = playerLabelX
    scoreY = playerLabelY + 2 * app.labelMargin
    scoreImage = app.interfaceBaseImage + f'Score{app.player.score}.png'
    drawImage(scoreImage, scoreX, scoreY)

    # Lives counter
    remainingLives = app.player.getLives()
    for life in range(remainingLives):
        lifeCx = scoreX + app.labelMargin * life
        lifeCy = scoreY + 2 * app.labelMargin
        drawImage(app.playerLifeImage, lifeCx, lifeCy)

    # playerNumberX = playerLabelX + playerLabelWidth - app.labelMargin
    # playerNumberY = playerLabelY
    # # background for a number
    # drawRect(playerNumberX, playerNumberY, 20, 25, fill='red', align='center')
    # drawLabel(app.playerNumber, playerNumberX, playerNumberY, fill=playerNumberColor, bold=True, size=24)

    # # Target 
    # targetLabelX = 
    # targetLabelY = 

    # Level
    levelX = app.width - 5 * app.labelMargin
    levelY = app.labelMargin
    levelWidth = 93
    drawImage(app.levelLabelImage, levelX, levelY)

    # Level Number
    numberMargin = 15
    levelNumberX = levelX + app.labelImageWidth + numberMargin 
    levelNumberY = levelY
    drawImage(app.interfaceBaseImage+f'{app.level}.png', levelNumberX, levelNumberY)

    # Round
    roundX = levelX
    roundY = levelY + 40
    drawImage(app.roundLabelImage, roundX, roundY)

    # RoundNumber
    roundNumberX = roundX + app.labelImageWidth + numberMargin 
    roundNumberY = roundY
    drawImage(app.interfaceBaseImage+f'{app.round}.png', roundNumberX, roundNumberY)

def playerJump(app, key):
    # first X coordinate of the player should reach the X0 coordinate of the parabola
    # this is a vertical line 
    # change will be 5 pixels
    row, col = app.player.block.position
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
        if nextBlock.mainColor != app.targetColor:
            nextBlock.mainColor = app.targetColor
            app.rawBlocks -= 1
        app.player.block = nextBlock
        app.player.changeCenter(nextBlock.getCenter())
    else:
        # the player will fall out of the pyramid
        print("Falling")

def drawnHomeScreen(app):
    logoCx = app.width // 2 
    logoCy = app.height // 2 - 3 * app.labelMargin
    drawImage(app.logoImage, logoCx, logoCy, align='center')

    creditsCx = logoCx
    creditsCy = app.height - app.labelMargin
    drawImage(app.creditsImage, creditsCx, creditsCy, align='center')

    drawClickButton(app, logoCy)

def drawClickButton(app, offset):
    buttonWidth = 150
    buttonHeight = 50
    buttonCx = app.width // 2 - buttonWidth // 2
    buttonCy = offset + 2.5 * app.labelMargin
    buttonColor = rgb(254, 170, 2)
    drawRect(buttonCx, buttonCy, buttonWidth, buttonHeight, fill=buttonColor)

def spawnEnemy(app):
    enemyType = randomEnemySelection(app.enemyTypes)
    randomBlockIndex = randint(0, 1)
    randomBlock = app.board[1][randomBlockIndex]
    newEnemy = Enemy(tag=enemyType, center=randomBlock.getCenter(), 
                     block=randomBlock, type=enemyType, move=0, imageId=1)
    app.enemies.append(newEnemy)
    return newEnemy

def enemyControls(app):
    enemies = app.enemies
    """
    The game has 2 types of enemies.

    Red: It jumps, reaches the end, and then falls.
    Simple.

    Green: It jumps, reaches the end, then transforms
    into a more intelligent snake that follows the player
    until it either kills him or dies itself.
    """
    for enemy in enemies:
        # collision
        animateEnemy(app, enemy)
        isCollided = detectCollision(app, enemy)
        if isCollided:
            res = app.player.takeLife()
            if res == -1:
                # no lives left
                print('died')
            # the game gets paused
            app.paused = True
            # the state of the game changes to 'playerDied'
            app.gameState = app.gameStates[2]
            # setting the death time of the player
            # this is needed to count the time till the revival
            app.playerDeathTime = time.time()
            app.enemySpawned = False
            break
        else:
            # movement
            elapsedTime = time.time() - enemy.moveTime
            if elapsedTime - app.enemyControlInterval > 0:
                if enemy.type == 'red':
                    redEnemyControls(app, enemy)
                else:
                    greenEnemyControls(app, enemy)

def animateEnemy(app, enemy):
    elapsedTime = time.time() - enemy.spawnTime
    if elapsedTime - enemy.imageChangeInterval > 0:
        enemy.imageId = 2 if enemy.imageId == 1 else 1
        enemy.increaseImageChangeInterval(app.fixedEnemyImageChangeInterval)

def redEnemyControls(app, enemy: Enemy):
    row, col = enemy.block.position
    nextRow, nextCol = row + 1, col + enemy.move
    index = findModelIndex(app.enemies, enemy.id)
    if isPositionLegal(app, nextRow, nextCol):
        nextBlock = app.board[nextRow][nextCol]
        enemy.block = nextBlock
        enemy.changeCenter(nextBlock.getCenter())
        enemy.move = 1 if enemy.move == 0 else 0
        enemy.moveTime += app.fixedEnemyControlInterval
        app.enemies[index] = enemy
    else:
        app.enemies.pop(index)

def greenEnemyControls(enemy: Enemy):
    print("hello!")

def detectCollision(app, enemy: Enemy):
    playerCx, playerCy = app.player.getCenter()
    enemyCx, enemyCy = enemy.getCenter()
    if playerCx == enemyCx and playerCy == enemyCy:
        return True
    return False

def checkBlockColors(app):
    if app.rawBlocks == 0:
       # player has successfuly passed the level!
        app.animationStartTime = time.time()
        app.gameState = app.gameStates[1]
        app.bonusAnimationStart = time.time()
        app.paused = True   

def playLevelTransitionAnimation(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            block = app.board[row][col]
            if block.mainColor == app.targetColor:
                block.mainColor = app.mainColor
            else:
                block.mainColor = app.targetColor

def getBonusAnimation(app):
    # Bonus First Text: YOU RECEIVED
    elapsedTime = time.time() - app.bonusAnimationStart
    if app.bonusAnimationDuration - elapsedTime > 0:
        bonusTextX, bonusTextY = app.width // 2, app.height - 3 * app.labelMargin
        drawImage(app.bonusTextImage, bonusTextX, bonusTextY, align='center')

def nextGame(app):
    # Increase the score of the player
    currentRound = app.round
    currentLevel = app.level
    prevScore = app.player.getScore()
    remainingLives = app.player.getLives()
    onAppStart(app)
    
    print(currentLevel, currentRound)
    if currentRound < app.rounds:
        app.round = currentRound + 1
        app.level = currentLevel
    elif currentLevel < app.levels:
        app.level = currentLevel + 1
    else:
        # complete win
        print('complete win')
        app.gameState = app.gameStates[3]
    
    app.player.updateLives(remainingLives)
    app.player.updateScore(prevScore + app.completionBonus)

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