from cmu_graphics import *
from models import (Player, Enemy)
from helper_functions import *

from random import randint
import time, pathlib

# TODO: continue watching https://www.youtube.com/watch?v=M6e3_8LHc7A
# to learn how to work with sprites

# TODO: then watch https://www.youtube.com/watch?v=nXOVcOBqFwM
# to learn how to animate sprites

################

def onAppStart(app):
    app.background = 'black'

    # Global
    app.levels = 5
    app.level = 1
    app.rounds = 3
    app.round = 1

    app.labelMargin = 30

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
    app.board = createBoard(app, app.rows)
    app.rawBlocks = countBlocks(app.board)

    # player starts on the highest col of the pyramid
    app.playerImageBase = 'media/spritesheet/player-'
    app.playerLives = 3
    app.playerInitDirection = 'down-right'
    app.playerStates = ['spawn', 'idle', 'jump']
    app.playerState = app.playerStates[0]
    app.playerImage = app.playerImageBase + f'{app.playerInitDirection}-idle.png'
    app.playerWidth = 45
    app.playerHeight = 45
    app.player = Player('player', app.board[0][0].getCenter(), app.board[0][0], app.playerInitDirection, app.playerImage, app.playerLives)
    app.playerNumber = 1

    # Image sources
    app.labelImageWidth = 93
    app.interfaceBaseImage = 'media/interface/' 
    # small image
    # NOTE: We can make the game resizable
    # if we do, we have to change the sizes of some pictures
    # such as logo
    app.starImage = app.interfaceBaseImage + 'star.png'
    app.logoImage = app.interfaceBaseImage + 'logo50.png'
    app.gameOverImage = app.interfaceBaseImage + 'gameOver50.png'
    app.creditsImage = app.interfaceBaseImage + 'credits-3-15.png'
    app.playBtnHollowImage = app.interfaceBaseImage + 'playButtonHollow.png'
    app.playBtnImage = app.interfaceBaseImage + 'playButton.png'
    app.playBtnTextImageF = app.interfaceBaseImage + 'playFirst.png'
    app.playBtnTextImageS = app.interfaceBaseImage + 'playSecond.png'
    app.playerLabelImage = app.interfaceBaseImage + 'player.png'
    app.playerLifeImage = app.interfaceBaseImage + 'player-small.png'
    app.startLevelImage = app.interfaceBaseImage + 'startLevel.png'
    app.startRound = app.interfaceBaseImage + 'startRound.png'
    app.levelStartOne = app.interfaceBaseImage + 'startLevel1.png'
    app.levelLabelImage = app.interfaceBaseImage + 'level.png'
    app.roundLabelImage = app.interfaceBaseImage + 'round.png'    
    app.bonusTextImage = app.interfaceBaseImage + 'bonusText.png'
    app.bonusScoreImage = app.interfaceBaseImage + 'AddScore250.png'
    app.bonusPointsImage = app.interfaceBaseImage + 'bonusPoints.png'

    app.swearImage = app.interfaceBaseImage + 'swear80.png'
    app.stars = generateStars(app, maxCap=5, image=app.starImage)
    app.starAnimation = 3

    app.playButtonState = 'off'
    app.btnIsPressed = False
    app.btnWidth = 150
    app.btnHeight = 50

    app.allowedMovementKeys = ['down', 'right', 'up', 'left']
    app.gameStates = ['start', 'levelTrans', 'inprogress', 'levelComplete', 'playerDied', 'pass', 'fail']
    app.gameState = 'start'
    app.paused = False

    app.enemyTypes = ['red']
    app.enemyImageBase = 'media/spritesheet/enemies/'
    app.enemies = list()
    app.enemySpawnInterval = 2
    app.enemyStates = ['idle', 'jump']
    app.enemiesSpawned = False
    app.readyEnemies = 0
    app.maximumEnemiesOnBoard = 4
    app.fixedMaxEnemiesOnBoard = 10
    app.numberOfEnemiesSpawn = 1
    app.maxEnemiesSpawn = 2
    app.fixedInterval = 2
    app.gameStartTime = None
    app.enemyCntrlIntrval = 1
    app.fixedEnemyCntrlIntrval = app.enemyCntrlIntrval
    
    app.enemyImageChangeInterval = 0.3
    app.fixedEnemyImageChangeInterval = 0.3

    app.animationStartTime = None
    app.animationCount = 3
    app.animationInterval = 0.1
    app.animationFixedInterval = app.animationInterval

    app.playerDeathTime = None
    app.playerRevivalTime = 3

    app.gravity = 0.9
    app.jumpAngle = 45

    # Start level transition
    app.startLevelInitTime = None
    app.startLevelDuration = 3

    # Music Effects
    # Cite: Professor Eduardo [Piazza]
    cntPath = pathlib.Path(__file__).parent.resolve()
    app.jump1Music = Sound(f'file://{cntPath}/media/music/jump1.mp3')
    app.swear = Sound(f'file://{cntPath}/media/music/swear.mp3')
    app.victoryMusic = Sound(f'file://{cntPath}/media/music/victory.mp3')
    app.mainTheme = Sound(f'file://{cntPath}/media/music/mainTheme.mp3')
    app.redEnemyJump = Sound(f'file://{cntPath}/media/music/redEnemyJump.mp3')
    app.levelStartMusic = Sound(f'file://{cntPath}/media/music/levelStart.mp3')

def redrawAll(app):
    if app.gameState == app.gameStates[0]:
        # the home page
        drawnHomeScreen(app)
    elif app.gameState == app.gameStates[1]:
        drawStartLevel(app)
    elif app.gameState == app.gameStates[5] \
        or app.gameState == app.gameStates[4]:
        # the player has either lost or won the game
        drawFinal(app)
    else:
        app.levelStartMusic.pause()
        drawPyramid(app)
        drawEnemies(app)
        drawPlayer(app)
        drawInterface(app)

        # if the player died, display a swear image
        if app.gameState == app.gameStates[3]:
            drawSwear(app)

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
        
        elif app.playerState == app.playerStates[2]:
            if not app.player.landed:
                # if the state of player is jumping
                app.player.handleJump()
            else:
                app.player.landed = False
                # the player has fully jumped to the block
                app.playerState = app.playerStates[1]

                # play jump sound effect
                app.jump1Music.play()

                # change the color of the new block
                # the player has jumped to
                if app.player.block.mainColor != app.targetColor:
                    app.player.block.mainColor = app.targetColor
                    app.rawBlocks -= 1

                # change the picture of the player to the original state
                app.player.image = app.playerImageBase + f'{app.player.direction}-idle.png'

        if app.gameState == app.gameStates[0]:
            if app.btnIsPressed:
                app.gameState = app.gameStates[1]
                app.mainTheme.pause()
    
        elif app.gameState == app.gameStates[1]:
            # play music
            elapsedTime = time.time() - app.startLevelInitTime
            if elapsedTime - app.startLevelDuration > 0:
                app.gameState = app.gameStates[2]
                app.gameStartTime = time.time()
        
        elif app.gameState == app.gameStates[2]:
            # if the game is in progress
            checkBlockColors(app)
            enemyControls(app)
            detectCollision(app)
            elapsedTime = time.time() - app.gameStartTime
            if len(app.enemies) < app.maximumEnemiesOnBoard:
                if elapsedTime - app.enemySpawnInterval > 0:
                    spawnEnemy(app)
                    app.enemiesSpawned = True
                    app.enemySpawnInterval += app.fixedInterval
   
        if app.enemiesSpawned and app.readyEnemies != app.numberOfEnemiesSpawn:
            enemy = app.enemies[-1]
            enemyCX, enemyCY = enemy.getCenter()
            _, currentBlockCY = enemy.block.getCenter()
            if enemyCY != currentBlockCY:
                enemyCY += 5
                enemy.changeCenter((enemyCX, enemyCY))
            else:
                app.readyEnemies += 1
        else:
            app.enemiesSpawned = False
            app.readyEnemies = 0

    elif app.gameState == app.gameStates[2]:
            # if the game level is complete, display a short animation.
            elapsedTime = time.time() - app.animationStartTime
            if elapsedTime - app.animationCount < 0:
                if elapsedTime - app.animationInterval > 0:
                    app.animationInterval += app.animationFixedInterval
                    playLevelTransitionAnimation(app)
            else:
                # the animation is over
                nextGame(app)

    elif app.gameState == app.gameStates[3] \
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
                app.gameState = app.gameStates[2]
                # the basically sort of 'restarts' with the initial time changing
                # to the current time.
                app.enemySpawnInterval += app.playerRevivalTime

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)
        
    if key == 'enter':
        if app.gameState == app.gameStates[0]:
            app.playButtonState = 'on'
            app.btnIsPressed = True
            app.startLevelInitTime = time.time()
            app.levelStartMusic.play()
        elif app.gameState == app.gameStates[2]:
            # the game can be stopped only if it is in progress
            app.paused = not app.paused

    if not app.paused \
        and app.playerState != app.playerStates[0] \
        and app.gameState != app.gameStates[0] \
        and app.playerState != app.playerStates[2]:
        if key in app.allowedMovementKeys:
            # the player is jumping
            playerJump(app, key)

def onMouseMove(app, mouseX, mouseY):
    if app.gameState == app.gameStates[0]:
        btnCx = app.width // 2
        btnCy = app.height // 2
        if (mouseX >= btnCx - app.btnWidth // 2 \
            and mouseX <= btnCx + app.btnWidth // 2):

            if (mouseY >= btnCy - app.btnHeight // 2 \
                and mouseY <= btnCy + app.btnHeight // 2):

                app.playButtonState = 'on'
            else:
                app.playButtonState = 'off'
        else:
            app.playButtonState = 'off'

def onMousePress(app, mouseX, mouseY):
    if app.gameState == app.gameStates[0]:
        if app.playButtonState == 'on':
            app.btnIsPressed = True
            if app.startLevelInitTime is None:
                app.startLevelInitTime = time.time()
            app.levelStartMusic.play()

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

def drawSwear(app):
    playerCx, playerCy = app.player.getCenter()
    imageCx = playerCx - 0.8 * app.playerWidth
    imageCy = playerCy - 2.5 * app.playerHeight
    drawImage(app.swearImage, imageCx, imageCy)

def drawStartLevel(app):
    # Level
    levelWidth = 201
    levelHeight = 37
    txtWidth = 37

    levelCx = app.width // 2 - txtWidth
    levelCy = app.height // 2
    drawImage(app.startLevelImage, levelCx, levelCy, align='center')

    txtCx = levelCx + levelWidth // 2 + app.labelMargin
    txtCy = levelCy
    drawImage(app.levelStartOne, txtCx, txtCy, align='center')

    # Round
    txtWidth = 
    roundCx = app.width // 2
    roundCy = app.height // 2 + levelHeight
    drawImage(app.startRound, roundCx, roundCy, align='center')

    roundTxtCx = roundCx


def playerJump(app, key):
    # first X coordinate of the player should reach the X0 coordinate of the parabola
    # this is a vertical line 
    # change will be 5 pixels
    row, col = app.player.block.position
    keyIndex = app.allowedMovementKeys.index(key)
    sign = +1 if key in ['down', 'right'] else -1
    nextRow, nextCol = row + sign, col + sign * (keyIndex % 2)

    direction = ''
    if key == 'down':
        direction += 'down-left'
    elif key == 'up':
        direction += 'top-right'
    elif key == 'left':
        direction += 'top-left'
    elif key == 'right':
        direction += 'down-right'

    if isPositionLegal(app, nextRow, nextCol):
        nxtBlock = app.board[nextRow][nextCol]
        app.player.jump(nxtBlock, app.jumpAngle, direction) # sets the next jumping block of the player
        app.playerState = app.playerStates[2]
        # change the picture of the player
        app.player.image = app.playerImageBase + f'{direction}-jump.png'
    else:
        # the player will fall out of the pyramid
        print("Falling")

def drawnHomeScreen(app):
    # background music
    app.mainTheme.play(loop=True)

    # drawStars(app)

    logoCx = app.width // 2 
    logoCy = app.height // 2 - 3 * app.labelMargin
    drawImage(app.logoImage, logoCx, logoCy, align='center')

    creditsCx = logoCx
    creditsCy = app.height - app.labelMargin
    drawImage(app.creditsImage, creditsCx, creditsCy, align='center')

    drawClickButton(app)

# Final
def drawFinal(app):
    cx, cy = app.width // 2, app.height // 2
    drawImage(app.gameOverImage, cx, cy, align='center')

def drawStars(app):
    for star in app.stars:
        cx, cy = star.getCenter()
        drawImage(star.getImage(), cx, cy, align='center')

def drawClickButton(app):
    if app.playButtonState == 'off':
        drawImage(app.playBtnHollowImage, app.width//2, app.height//2, align='center')
        drawImage(app.playBtnTextImageF, app.width//2, app.height//2, align='center')
    elif app.playButtonState == 'on':
        drawImage(app.playBtnImage, app.width//2, app.height//2, align='center')
        drawImage(app.playBtnTextImageS, app.width//2, app.height//2, align='center')

def spawnEnemy(app):
    enemyType = randomEnemySelection(app.enemyTypes)
    randomBlockIndex = randint(0, 1)
    randomBlock = app.board[1][randomBlockIndex]
    newEnemy = Enemy(tag=enemyType, center=randomBlock.getCenter(), 
                     block=randomBlock, type=enemyType, imageId=1,
                     state=app.enemyStates[0])
    app.enemies.append(newEnemy)

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
        # movement
        elapsedTime = time.time() - enemy.moveTime
        if elapsedTime - app.enemyCntrlIntrval > 0:
            enemyMove(app, enemy)

def animateEnemy(app, enemy):
    elapsedTime = time.time() - enemy.spawnTime
    if elapsedTime - enemy.imageChangeInterval > 0:
        enemy.imageId = 2 if enemy.imageId == 1 else 1
        enemy.increaseImageChangeInterval(app.fixedEnemyImageChangeInterval)

def enemyMove(app, enemy: Enemy):
    if enemy.state == app.enemyStates[0]:
        app.redEnemyJump.play()
        row, col = enemy.block.position
        direction = ''
        enemy.move = randint(0, 1)
        if enemy.move == 0:
            direction += 'down-left'
        else:
            direction += 'down-right'
        nextRow, nextCol = row + 1, col + enemy.move
        if isPositionLegal(app, nextRow, nextCol):
            # if the enemy can jump to the next block
            # first, update the enemy model by calling jump()
            # which updates next block, velocity, and angle
            nxtBlock = app.board[nextRow][nextCol]
            enemy.jump(nxtBlock, app.jumpAngle, direction)
            enemy.state = app.enemyStates[1]
        else:
            print("Falling")
            index = findModelIndex(app.enemies, enemy.id)
            app.enemies.pop(index)
    else:
        # enemy is jumping
        if not enemy.landed:
            enemy.handleJump()
        else:
            # enemy has landed on the block
            enemy.landed = False

            # enemy is not in the jumping state anymore
            enemy.state = app.enemyStates[0]
            # increase the move time of the enemy
            enemy.moveTime += app.fixedEnemyCntrlIntrval

def detectCollision(app):
    playerCx, playerCy = app.player.getCenter()
    enemies = app.enemies

    for enemy in enemies:
        enemyCx, enemyCy = enemy.getCenter()
        if enemyCx >= playerCx - app.playerWidth // 4 \
            and enemyCx <= playerCx + app.playerWidth // 4:

            if enemyCy >= playerCy - app.playerHeight // 4 \
                and enemyCy <= playerCy + app.playerHeight // 4:

                # no spawning enemy
                app.enemiesSpawned = False
                
                # enemies get removed immediately
                app.enemies.clear()

                res = app.player.takeLife()
                # display swear and play a swear music
                app.swear.play()

                if res == -1:
                    # no lives left
                    app.gameState = app.gameStates[5]
                else:
                    # the state of the game changes to 'playerDied'
                    app.gameState = app.gameStates[3]
                    # the game gets paused
                    app.paused = True
                    # setting the death time of the player
                    # this is needed to count the time till the revival
                    app.playerDeathTime = time.time()

def checkBlockColors(app):
    if app.rawBlocks == 0:
       # player has successfuly passed the level!
        app.animationStartTime = time.time()
        app.gameState = app.gameStates[2]
        app.victoryMusic.play()
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
    currentRows = app.rows
    prevScore = app.player.getScore()
    remainingLives = app.player.getLives()
    curMaxEnemiesOnBoard = app.maximumEnemiesOnBoard
    onAppStart(app)

    app.gameState = app.gameStates[1]

    if currentRound < app.rounds:
        app.round = currentRound + 1
        app.level = currentLevel
        app.numberOfEnemiesSpawn += 1
        if curMaxEnemiesOnBoard < app.fixedMaxEnemiesOnBoard:
            app.maximumEnemiesOnBoard = curMaxEnemiesOnBoard + 1

    elif currentLevel < app.levels:
        app.rows = currentRows + 1
        app.board = createBoard(app, app.rows)
        app.rawBlocks = countBlocks(app.board)
        app.level = currentLevel + 1
    else:
        # complete win
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