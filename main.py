from cmu_graphics import *
from models import (Player, Enemy)
from helper_functions import *

from random import randint
import time, math

# TODO: continue watching https://www.youtube.com/watch?v=M6e3_8LHc7A
# to learn how to work with sprites

# TODO: then watch https://www.youtube.com/watch?v=nXOVcOBqFwM
# to learn how to animate sprites

################

def onAppStart(app):
    # Private
    __playerSpriteSheetURL = 'media/player.png'
    __playerImageSize = 24

    # Global
    # Colors
    app.levels = 5
    app.level = 1

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
    app.player = Player('player', app.board[0][0].getCenter(), app.board[0][0])
    app.playerSpiteSheetImage = (__playerSpriteSheetURL, *app.player.center)
    app.playerStates = ['spawn', 'ready', 'jumping']
    app.playerState = app.playerStates[0]
    app.playerLives = 3

    app.allowedMovementKeys = ['down', 'right', 'up', 'left']
    app.gameStates = ['inprogress', 'levelComplete', 'playerDied']
    app.gameState = 'inprogress'
    app.paused = False
    app.enemyTypes = ['red']
    app.enemies = list()
    app.enemySpawnInterval = 5
    app.enemySpawned = None
    app.maximumEnemiesOnBoard = 3
    app.fixedInterval = 5
    app.initialTime = time.time()
    app.enemyControlInterval = 3
    app.fixedEnemyControlInterval = app.enemyControlInterval

    app.animationStartTime = None
    app.animationCount = 5
    app.animationInterval = 0.3
    app.animationFixedInterval = app.animationInterval

    app.playerDeathTime = None
    app.playerRevivalTime = 5

def redrawAll(app):
    drawBackground(app)
    drawPyramid(app)
    drawPlayer(app)
    drawEnemies(app)

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
                app.playerState = app.playerStates[1] # the player is ready
                app.board[0][0].mainColor = app.targetColor
                app.rawBlocks -= 1
    
        checkBlockColors(app)
        enemyControls(app)
        # if the state of player is jumping
        if app.playerState == app.playerStates[1]:
            # playerJump(app)
            pass

        if app.gameState == app.gameStates[0]:
            elapsedTime = time.time() - app.initialTime
            if len(app.enemies) < app.maximumEnemiesOnBoard:
                if elapsedTime - app.enemySpawnInterval > 0:
                    enemy = spawnEnemy(app)
                    app.enemySpawnInterval += app.fixedInterval
                    app.enemySpawned = enemy

        if app.enemySpawned is not None:
            enemyCX, enemyCY = app.enemySpawned.getCenter()
            _, currentBlockCY = app.enemySpawned.block.getCenter()
            if enemyCY != currentBlockCY:
                enemyCY += 5
                app.enemySpawned.changeCenter((enemyCX, enemyCY))
                index = findModelIndex(app.enemies, app.enemySpawned.id)
                app.enemies[index] = app.enemySpawned
            else:
                app.enenySpawned = None

    elif app.gameState == app.gameStates[1]:
        # if the game level is complete, display a short animation.
        elapsedTime = time.time() - app.animationStartTime
        if elapsedTime - app.animationCount < 0:
            if elapsedTime - app.animationInterval > 0:
                app.animationInterval += app.animationFixedInterval
                playLevelTransitionAnimation(app)

    elif app.gameState == app.gameStates[2] \
            and app.playerDeathTime is not None \
            and app.playerLives > 0:
        # the player has died because of falling or collision with the enemy
        elapsedTime = time.time() - app.playerDeathTime
        if elapsedTime - app.playerRevivalTime > 0:
            # the playerGetsRevived and the game continues
            # the progress and the position of the player does not change
            app.paused = False
            app.deathTime = None
            # the game state changes to 'inprogress'
            app.gameState = app.gameStates[0]
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
            app.playerState = app.playerStates[1]
            playerJump(app, key)

# Background
def drawBackground(app):
    drawRect(0, 0, app.width, app.height, fill='black')

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
    drawRect(playerX, playerY, 15, 15, fill='violet', align='center')

def drawEnemies(app):
    for enemy in app.enemies:
        enemyX, enemyY = enemy.getCenter()
        drawRect(enemyX, enemyY, 15, 15, fill=enemy.type, align='center')

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

def spawnEnemy(app):
    enemyType = randomEnemySelection(app.enemyTypes)
    randomBlockIndex = randint(0, 1)
    randomBlock = app.board[1][randomBlockIndex]
    newEnemy = Enemy(tag=enemyType, center=randomBlock.getCenter(), 
                     block=randomBlock, type=enemyType, move=0)
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
        detectCollision(app, enemy)
        # movement
        elapsedTime = time.time() - enemy.moveTime
        if elapsedTime - app.enemyControlInterval > 0:
            if enemy.type == 'red':
                redEnemyControls(app, enemy)
            else:
                greenEnemyControls(app, enemy)

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
        # the player has collided with one of the enemies
        # thus, one life of the player gets removed
        if app.playerLives > 0:
            app.playerLives -= 1
        # the game gets paused
        app.paused = True
        # the state of the game changes to 'playerDied'
        app.gameState = app.gameStates[2]
        # setting the death time of the player
        # this is needed to count the time till the revival
        app.playerDeathTime = time.time()

def checkBlockColors(app):
    if app.rawBlocks == 0:
       # player has successfuly passed the level!
       app.animationStartTime = time.time()
       app.gameState = app.gameStates[1]
       app.paused = True

def playLevelTransitionAnimation(app):
    for row in range(len(app.board)):
        for col in range(len(app.board[row])):
            block = app.board[row][col]
            if block.mainColor == app.targetColor:
                block.mainColor = app.mainColor
            else:
                block.mainColor = app.targetColor

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