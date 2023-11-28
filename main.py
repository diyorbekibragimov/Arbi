from cmu_graphics import *
from models import (Player, Enemy, Disk, JoystickInstruction)
from helper_functions import *

from random import randint, randrange
import time, pathlib, copy, sys
import joystick

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
    app.board = createBoard(app, app.rows, app.wrapperHeight // 4)
    app.rawBlocks = countBlocks(app.board)

    # player starts on the highest col of the pyramid
    app.playerImageBase = 'media/spritesheet/player-'
    app.playerLives = 3
    app.playerInitDirection = 'down-right'
    app.playerStates = ['idle', 'jump', 'disk', 'fly', 'dropoff']
    app.playerImage = app.playerImageBase + f'{app.playerInitDirection}-idle.png'
    app.playerWidth = 45
    app.playerHeight = 45
    app.player = Player('player', app.board[0][0].getCenter(), app.board[0][0], \
                        app.playerInitDirection, app.playerImage, app.playerLives, \
                        app.playerStates[0])
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
    app.inspirationImage = app.interfaceBaseImage + 'inspirationText.png'
    app.playBtnHollowImage = app.interfaceBaseImage + 'playButtonHollow.png'
    app.playBtnImage = app.interfaceBaseImage + 'playButton.png'
    app.playBtnTextImageF = app.interfaceBaseImage + 'playFirst.png'
    app.playBtnTextImageS = app.interfaceBaseImage + 'playSecond.png'
    app.playerLabelImage = app.interfaceBaseImage + 'player.png'
    app.playerLifeImage = app.interfaceBaseImage + 'player-small.png'
    app.startLevelImage = app.interfaceBaseImage + 'startLevel.png'
    app.startRound = app.interfaceBaseImage + 'startRound.png'
    app.startLevelTxt = app.interfaceBaseImage + 'startLevel'
    app.startRoundTxt = app.interfaceBaseImage + 'startRound'
    app.levelLabelImage = app.interfaceBaseImage + 'level.png'
    app.roundLabelImage = app.interfaceBaseImage + 'round.png'    
    app.bonusTextImage = app.interfaceBaseImage + 'bonusText.png'
    app.bonusScoreImage = app.interfaceBaseImage + 'AddScore250.png'
    app.bonusPointsImage = app.interfaceBaseImage + 'bonusPoints.png'
    app.gameOverText = app.interfaceBaseImage + 'gameOverText.png'
    app.continueText = app.interfaceBaseImage + 'continueText.png'
    app.selectInstructionImage = app.interfaceBaseImage + 'instructionSelect.png'

    # End screen
    app.creator = app.interfaceBaseImage + 'creator2.png'
    app.creatorClass = app.interfaceBaseImage + 'class.png'
    app.developedBy = app.interfaceBaseImage + 'developedBy.png'
    app.returnImage = app.interfaceBaseImage + 'returnHome.png'
    app.thankImage = app.interfaceBaseImage + 'thankYou.png'
    app.exitImage = app.interfaceBaseImage + 'exit.png'
    app.exitImage = app.interfaceBaseImage + 'exit.png'

    app.joystickBase = app.interfaceBaseImage + 'joystick-'
    app.joystickDirections = ['up', 'right', 'down', 'left']
    app.joysticksInstruction = createJoysticks(app)
    # Instruction page
    app.instructionId = 0
    app.instructionStartTime = 0
    offsetY = app.height // 2 - 1.5 * (app.blockSize + 2 * app.radius)
    offsetX = - 5 * app.labelMargin
    app.instructionBoard = createBoard(app, 4, offsetY, offsetX)
    app.instructionPlayerInitDirection = 'top-right'
    app.instructionPlayerStates = ['idle', 'jump']
    app.instructionPlayer = Player('instructionPlayer', app.instructionBoard[2][1].getCenter(), app.instructionBoard[2][1],
                                   app.instructionPlayerInitDirection, app.playerImage, 0,
                                   app.instructionPlayerStates[0])
    app.instructionPlayerInterval = 0.5
    app.instructionPlayerFixedInterval = 1
    app.instructionJumpWait = 0.1
    app.maxInstruction = 4

    # Support for the Arcade
    app.pressStartText = app.interfaceBaseImage + 'arcade-press-start.png'

    app.swearImage = app.interfaceBaseImage + 'swear.png'
    app.stars = generateStars(app, maxCap=5, image=app.starImage)
    app.starAnimation = 3

    app.playButtonState = 'off'
    app.btnIsPressed = False
    app.btnWidth = 150
    app.btnHeight = 50

    app.allowedMovementKeys = ['down', 'right', 'up', 'left']
    app.gameStates = ['start', 'levelTrans', 'inprogress', 'levelComplete', 'playerDied', 'pass', 'fail', 'instructions', 'gameEnd']
    app.gameState = 'start'
    app.paused = False

    app.enemyTypes = ['red', 'snake', 'dalekh', 'chiwarra']
    app.enemyImageBase = 'media/spritesheet/enemies/'
    app.enemies = list()
    app.enemySpawnInterval = 2
    app.enemyStates = ['idle', 'jump']
    app.enemiesSpawned = False
    app.readyEnemies = 0
    app.gameStartTime = None

    # level management
    app.maximumEnemiesOnBoard = 4
    app.minEnemySpawnInterval = 1
    app.enemySpawnFixedInterval = 4
    app.fixedMaxEnemiesOnBoard = 10
    app.numberOfEnemiesSpawn = 1
    app.maxEnemiesSpawn = 2
    app.maxSnakesOnBoard = 1
    app.gameAddSpeed = 0
    app.maxGameAddSpeed = 0.4
    app.fixedGameAddSpeed = 0.2
    app.greenEnemyAppear = 0
    app.maxGreenEnemyAppear = 2

    # disks
    app.diskImageBase = 'media/spritesheet/disks/'
    app.disks = createDisks(app.board, app.radius, app.diskImageBase)
    app.diskImageChangeInterval = 0.09
    app.fixedDiskImageChangeInterval = 0.09
    firstBlockCx, firstBlockCy = app.board[0][0].getCenter()
    app.dropOffCoordinates = (firstBlockCx, firstBlockCy-2*app.blockSize)

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
    app.startLevelDuration = 3.5

    # Start Level Player Animation
    app.startPlayerCx = app.width // 2
    app.startPlayerCy = app.height - 10 * app.labelMargin
    offsetY = app.startPlayerCy
    app.startBoard = createBoard(app, 2, offsetY)
    app.startPlayerInitDirection = 'down-left'
    app.startPlayerStates = ['idle', 'jump']
    app.startPlayer = Player('startPlayer', app.startBoard[0][0].getCenter(), app.startBoard[0][0], \
                             app.playerInitDirection, app.playerImage, 0, app.startPlayerStates[0])
    app.startPlayerInterval = 0.5
    app.startPlayerFixedInterval = 1
    app.startPlayerJumpCount = 0

    # Music Effects
    # Cite: Professor Eduardo [Piazza]
    cntPath = pathlib.Path(__file__).parent.resolve()
    app.jump1Music = Sound(f'file://{cntPath}/media/music/jump1.mp3')
    app.swear = Sound(f'file://{cntPath}/media/music/swear.mp3')
    app.victoryMusic = Sound(f'file://{cntPath}/media/music/victory.mp3')
    app.mainTheme = Sound(f'file://{cntPath}/media/music/mainTheme.mp3')
    app.redEnemyJump = Sound(f'file://{cntPath}/media/music/redEnemyJump.mp3')
    app.purpleEnemyJump = Sound(f'file://{cntPath}/media/music/snakeJump.mp3')
    app.snakeJump = Sound(f'file://{cntPath}/media/music/grownSnakeJump.mp3')
    app.levelStartMusic = Sound(f'file://{cntPath}/media/music/levelStart.mp3')
    app.liftMusic = Sound(f'file://{cntPath}/media/music/lift.mp3')

def redrawAll(app):
    if app.gameState == app.gameStates[0]:
        # the home page
        drawnHomeScreen(app)
    elif app.gameState == app.gameStates[1]:
        drawStartLevel(app)
    elif app.gameState == app.gameStates[5] \
        or app.gameState == app.gameStates[6]:
        # the player has either lost or won the game
        drawFinal(app)
    elif app.gameState == app.gameStates[7]:
        # instructions
        drawInstruction(app)
    elif app.gameState == app.gameStates[8]:
        # the player has completely ended the game
        drawEndScreen(app)
        app.mainTheme.play()
    else:
        app.levelStartMusic.pause()
        drawPyramid(app, app.board)
        drawEnemies(app)
        drawDisks(app)
        drawPlayer(app.player)
        drawInterface(app)

        # if the player died, display a swear image
        if app.gameState == app.gameStates[4]:
            drawSwear(app)

    # if the level is complete, display animation
    if app.bonusAnimationStart is not None:
        getBonusAnimation(app)

def onStep(app):
    if not app.paused:
        
        if app.gameState == app.gameStates[0]:
            if app.btnIsPressed:
                app.gameState = app.gameStates[7]
                app.instructionStartTime = time.time()
    
        elif app.gameState == app.gameStates[1]:
            elapsedTime = time.time() - app.startLevelInitTime
            # player animation
            if elapsedTime - app.startPlayerInterval > 0:
                app.startPlayerInterval += app.startPlayerFixedInterval
                app.startPlayer.state = app.startPlayerStates[1]
                
                if app.startPlayerJumpCount == 0:
                    playerJump(app, app.startBoard, app.startPlayer, app.startPlayerStates, 'right')
                elif app.startPlayerJumpCount == 1:
                    playerJump(app, app.startBoard, app.startPlayer, app.startPlayerStates, 'left')
                elif app.startPlayerJumpCount == 2:
                    playerJump(app, app.startBoard, app.startPlayer, app.startPlayerStates, 'down')

                if app.startPlayerJumpCount < 3:
                    app.startPlayerJumpCount += 1

            if app.startPlayer.state == app.startPlayerStates[1]:
                if not app.startPlayer.landed:
                    app.startPlayer.handleJump()
                else:
                    app.startPlayer.landed = False
                    # the player has fully jumped to the block
                    app.startPlayer.state = app.startPlayerStates[0]

                    # change the color of the new block
                    # the player has jumped to
                    if app.startPlayer.block.mainColor != app.targetColor:
                        app.startPlayer.block.mainColor = app.targetColor

                    # change the picture of the player to the original state
                    app.startPlayer.image = app.playerImageBase + f'{app.startPlayer.direction}-idle.png'

            # level transition end time
            if elapsedTime - app.startLevelDuration > 0:
                app.gameState = app.gameStates[2]
                app.gameStartTime = time.time()
        
        detectCollision(app)
        if app.gameState == app.gameStates[2]:
            # mechanics of the player jump
            if app.player.state == app.playerStates[1]:
                if not app.player.landed:
                    # if the state of player is jumping
                    app.player.handleJump()
                else:
                    app.player.landed = False
                    # the player has fully jumped to the block
                    app.player.state = app.playerStates[0]

                    # play jump sound effect
                    app.jump1Music.play()

                    # change the color of the new block
                    # the player has jumped to
                    if app.player.block.mainColor != app.targetColor:
                        app.player.block.mainColor = app.targetColor
                        app.rawBlocks -= 1

                    # change the picture of the player to the original state
                    app.player.image = app.playerImageBase + f'{app.player.direction}-idle.png'
            elif app.player.state == app.playerStates[2]:
                # if the player is jumping to the disk
                if not app.player.landed:
                    # if the state of player is jumping
                    app.player.handleDiskJump()
                else:
                    app.player.landed = False
                    # the player has fully jumped to the disk
                    # now the flying mode should be activated
                    app.player.state = app.playerStates[3]

                    # change the picture of the player to the original state
                    app.player.image = app.playerImageBase + f'{app.player.direction}-idle.png'

                    # play the lift music
                    app.liftMusic.play()

            elif app.player.state == app.playerStates[3]:
                # start changing the coordinates of the player and the disk
                _, blockUpy = app.player.disk.blockUp.getCenter()
                playerCx, playerCy = app.player.getCenter()
                diskCx, diskCy = app.player.disk.getCenter()
                # until the disk does not reach the y coordinate of the 
                # block that is one block upper, it won't start moving
                # diagonally
                if diskCy >= blockUpy:
                    # change the y coordinate of the player really quickly
                    playerCy -= app.player.disk.velocity
                    diskCy -= app.player.disk.velocity

                    app.player.disk.changeCenter((diskCx, diskCy))
                    app.player.changeCenter((playerCx, playerCy))

                else:
                    # now let's start moving diagonally
                    dropCx, dropCy = app.dropOffCoordinates

                    if diskCy >= dropCy:
                        # changing the y coordinate
                        # of the disk and the player
                        diskCy += app.player.disk.diagonalVelocityY
                        playerCy += app.player.disk.diagonalVelocityY

                    if app.player.direction == 'top-left':
                        if diskCx <= dropCx:
                            # changing the x coordinate
                            # of the disk and the player
                            diskCx += app.player.disk.diagonalVelocityX + 1
                            playerCx += app.player.disk.diagonalVelocityX + 1

                    elif app.player.direction == 'top-right':
                        if diskCx >= dropCx:
                            # changing the x coordinate
                            # of the disk and the player
                            diskCx += app.player.disk.diagonalVelocityX
                            playerCx += app.player.disk.diagonalVelocityX 

                    app.player.disk.changeCenter((diskCx, diskCy))
                    app.player.changeCenter((playerCx, playerCy))

                    if ((app.player.direction == 'top-left' and diskCx >= dropCx) \
                        or (app.player.direction == 'top-right' and diskCx <= dropCx)
                        ) and diskCy <= dropCy:
                        # DROP OFF!
                        # first we make the disk disappear
                        index = findModelIndex(app.disks, app.player.disk.id)
                        app.disks.pop(index)
                        app.player.disk = None
                        app.player.state = app.playerStates[4]
                        _, blockCy = app.board[0][0].getCenter()

                        # set the drop off velocity
                        app.player.dropOffVelocity = (blockCy - playerCy) // 20

            elif app.player.state == app.playerStates[4]:
                playerCx, playerCy = app.player.getCenter()
                _, blockCy = app.board[0][0].getCenter()
                if playerCy <= blockCy:
                    playerCy += app.player.dropOffVelocity
                    app.player.changeCenter((playerCx, playerCy))
                else:
                    # the player has landed on the first block
                    app.player.block = app.board[0][0]
                    # change the state of the player
                    app.player.state = app.playerStates[0]
                    if app.player.block.mainColor != app.targetColor:
                        app.player.block.mainColor = app.targetColor
                        app.rawBlocks -= 1

            # if the game is in progress
            checkBlockColors(app)
            enemyControls(app)
            animateDisks(app)

            elapsedTime = time.time() - app.gameStartTime
            if len(app.enemies) < app.maximumEnemiesOnBoard:
                if elapsedTime - app.enemySpawnInterval > 0:
                    spawnEnemy(app)
                    app.enemiesSpawned = True
                    app.enemySpawnInterval += app.enemySpawnFixedInterval
        
        elif app.gameState == app.gameStates[7]:
            # instructions

            elapsedTime = time.time() - app.instructionStartTime
            stick = app.joysticksInstruction[app.instructionId]

            # player animation
            if elapsedTime - app.instructionPlayerInterval > 0:
                app.instructionPlayerInterval += app.instructionPlayerFixedInterval
                app.instructionPlayer.state = app.instructionPlayerStates[1]
                app.instructionPlayer.landedTime = None
                playerJump(app, app.instructionBoard, app.instructionPlayer, app.instructionPlayerStates, stick.direction)

            if app.instructionPlayer.state == app.instructionPlayerStates[1]:
                if not app.instructionPlayer.landed:
                    app.instructionPlayer.handleJump()
                else:
                    app.instructionPlayer.landed = False

                    # setting the time the player has landed to the block
                    if app.instructionPlayer.landedTime is None:
                        app.instructionPlayer.landedTime = time.time()

                    elapsedTime = time.time() - app.instructionPlayer.landedTime

                    # change the color of the new block
                    # the player has jumped to
                    if app.instructionPlayer.block.mainColor != app.targetColor:
                        app.instructionPlayer.block.mainColor = app.targetColor

                    # change the picture of the player to the original state
                    app.instructionPlayer.image = app.playerImageBase + f'{app.instructionPlayer.direction}-idle.png'

                    # return to the initial block
                    if elapsedTime - app.instructionJumpWait > 0:
                        app.instructionPlayer.block.mainColor = app.mainColor
                        app.instructionPlayer.block = app.instructionBoard[2][1]
                        app.instructionPlayer.changeCenter(app.instructionPlayer.block.getCenter())
                        # the player has fully returned to the block
                        app.instructionPlayer.state = app.instructionPlayerStates[0]

            # stick animation
            if elapsedTime - stick.imageChangeInterval > 0:
                if stick.state == 'idle':
                    stick.image = app.joystickBase + f'{stick.direction}.png'
                    stick.state = 'active'
                elif stick.state == 'active':
                    stick.image = app.joystickBase + f'idle.png'
                    stick.state = 'idle'
                stick.imageChangeInterval += stick.fixedJoystickChangeInterval

        if app.enemiesSpawned and app.readyEnemies != app.numberOfEnemiesSpawn:
            enemy = app.enemies[-1]
            enemyCX, enemyCY = enemy.getCenter()
            
            # UNDER DEVELOPMENT
            # if enemy.type == app.enemyTypes[2] \
            #     or enemy.type == app.enemyTypes[3]:
            #     # aliens: revilo or thavani
            #     side = enemy.direction.split('-')[1]

            #     curBlckCx = None

            #     if side == 'left':
            #         curBlckCx, _ = enemy.block.getLeftSideCenter()
            #     else:
            #         curBlckCx, _ = enemy.block.getRightSideCenter()

            #     if enemyCX != curBlckCx:
            #         enemyCX += 5
            #         enemy.changeCenter((enemyCX, enemyCY))
            #     else:
            #         app.readyEnemies += 1
            # else:
                # standard enemy
            _, currentBlockCY = enemy.block.getCenter()
            if enemyCY != currentBlockCY:
                enemyCY += 5
                enemy.changeCenter((enemyCX, enemyCY))
            else:
                if enemy.type == app.enemyTypes[2] or enemy.type == app.enemyTypes[3]:
                    block = enemy.block
                    if block.mainColor == app.targetColor:
                        block.mainColor = app.mainColor
                        app.rawBlocks += 1
                app.readyEnemies += 1
        else:
            app.enemiesSpawned = False
            app.readyEnemies = 0

    elif app.gameState == app.gameStates[3]:
            # if the game level is complete, display a short animation.
            elapsedTime = time.time() - app.animationStartTime
            if elapsedTime - app.animationCount < 0:
                if elapsedTime - app.animationInterval > 0:
                    app.animationInterval += app.animationFixedInterval
                    playLevelTransitionAnimation(app)
            else:
                # the animation is over
                nextGame(app)

    elif app.gameState == app.gameStates[4] \
                and app.playerDeathTime is not None \
                and app.playerLives > 0:
            # the player has died because of falling or collision with the enemy
            elapsedTime = time.time() - app.playerDeathTime
            if elapsedTime - app.playerRevivalTime > 0:
                # the player gets revived and the game continues
                # the progress and the position of the player does not change
                app.paused = False
                # revert the player to the previous block
                app.player.state = app.playerStates[0]
                app.player.changeCenter(app.player.block.getCenter())

                app.playerDeathTime = None
                # the game state changes to 'inprogress'
                app.gameState = app.gameStates[2]
                # this basically sort of 'restarts' with the initial time changing
                # to the current time.
                app.gameStartTime = time.time()
                app.diskImageChangeInterval = app.fixedDiskImageChangeInterval
                app.enemySpawnInterval = app.enemySpawnFixedInterval

def onKeyPress(app, key):
    if key == 'r':
        onAppStart(app)
        
    if key == 'enter':
        if app.gameState == app.gameStates[0]:
            app.playButtonState = 'on'
            app.btnIsPressed = True
        elif app.gameState == app.gameStates[2]:
            # the game can be stopped only if it is in progress
            app.paused = not app.paused
    
    if key == 'b':
        if app.gameState == app.gameStates[6]:
            # end the game
            app.gameState = app.gameStates[8]
    
    if key == 'a':
        if app.gameState == app.gameStates[6]:
            continueGame(app)

    if key == 'x':
        if app.gameState == app.gameStates[7]:
            app.jump1Music.play()
            nextInstruction(app)

    if key == 's':
        if app.gameState == app.gameStates[8]:
            # returning back to the main screen
            # with everything going to the default
            onAppStart(app)

    if not app.paused \
        and app.gameState == app.gameStates[2] \
        and app.player.state != app.playerStates[1] \
        and app.player.state != app.playerStates[3] \
        and app.player.state != app.playerStates[4]:
        if key in app.allowedMovementKeys:
            # the player is jumping
            playerJump(app, app.board, app.player, app.playerStates, key)

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

    drawImage(app.playerLabelImage, playerLabelX, playerLabelY)

    # Score
    scoreX = playerLabelX
    scoreY = playerLabelY + 2 * app.labelMargin
    scoreImage = app.interfaceBaseImage + f'Score{app.player.score}.png'
    drawImage(scoreImage, scoreX, scoreY)

    # Lives counter
    remainingLives = app.player.getLives()
    for life in range(remainingLives):
        lifeCx = scoreX + 1.5 * app.labelMargin * life
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
    levelTxtWidth = 37
    roundWidth = 127
    roundHeight = 20
    roundTxtWidth = 14

    levelCx = app.width // 2 - levelTxtWidth
    levelCy = app.height // 3 - roundHeight
    drawImage(app.startLevelImage, levelCx, levelCy, align='center')

    txtCx = levelCx + levelWidth // 2 + app.labelMargin
    txtCy = levelCy
    startLevelTxt = app.startLevelTxt + f'{app.level}.png'
    drawImage(startLevelTxt, txtCx, txtCy, align='center')

    # Round
    roundCx = app.width // 2 - roundTxtWidth
    roundCy = levelCy + levelHeight
    drawImage(app.startRound, roundCx, roundCy, align='center')

    roundTxtCx = roundCx + roundWidth // 2 + app.labelMargin
    roundTxtCy = roundCy
    startRoundTxt = app.startRoundTxt + f'{app.round}.png'
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
    drawImage(app.selectInstructionImage, selectTxtCx, selectTxtCy, align='center')

def playerJump(app, board, player, playerStates, key):
    # first X coordinate of the player should reach the X0 coordinate of the parabola
    # this is a vertical line 
    # change will be 5 pixels
    row, col = player.block.position
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
        try:
            nxtBlock = board[nextRow][nextCol]
        
            player.jump(nxtBlock, app.jumpAngle, direction) # sets the next jumping block of the player
            player.state = playerStates[1]
            # change the picture of the player
            player.image = app.playerImageBase + f'{direction}-jump.png'
        except:
            print("Failed to jump")
    else:
        # maybe player is jumping towards disks
        if row == len(app.board) - 2 and (col == 0 or col == row):
            # check if the disk is still there
            disk = isDiskPresent(app, row, col)
            if disk != -1:
                # disk is present
                player.jumpDisk(disk, 45, direction)
                player.state = playerStates[2] # flying state
                player.image = app.playerImageBase + f'{direction}-jump.png'

                # setting the velocity of the disk
                _, blockUpCy = disk.blockUp.getCenter()
                diskCx, diskCy = disk.getCenter()
                dropCx, dropCy = app.dropOffCoordinates

                disk.velocity = (diskCy - blockUpCy) // 10
                disk.diagonalVelocityX = (dropCx - diskCx) // 90
                disk.diagonalVelocityY = (dropCy - diskCy) // 90

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
    drawImage(app.inspirationImage, creditsCx, creditsCy, align='center')

    #buttonHeight = 50
    #drawClickButton(app)

    pressStartX = app.width // 2
    pressStartY = app.height // 2 + app.labelMargin
    drawImage(app.pressStartText, pressStartX, pressStartY, align='center')

# Final
def drawFinal(app):
    cx, cy = app.width // 2, app.height // 3
    drawImage(app.gameOverImage, cx, cy, align='center')

    # text
    continueHeight = 29
    gameOverHeight = 29

    continueX = cx
    continueY = app.height // 2 - gameOverHeight + app.labelMargin
    drawImage(app.continueText, continueX, continueY, align='center')

    gameOverX = cx 
    gameOverY = app.height // 2 + continueHeight + app.labelMargin
    drawImage(app.gameOverText, gameOverX, gameOverY, align='center')

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

def drawEndScreen(app):
    # thank you text
    thankX = app.width // 2
    thankY = app.height // 4
    drawImage(app.thankImage, thankX, thankY, align='center')

    # navigation 
    navigationImageHeight = 20

    returnX = app.width // 2
    returnY = app.height // 2 - navigationImageHeight
    drawImage(app.returnImage, returnX, returnY, align='center')

    exitX = app.width // 2
    exitY = app.height // 2 + navigationImageHeight + app.labelMargin
    drawImage(app.exitImage, exitX, exitY, align='center')

    # credits
    creatorHeight = 37
    creatorClassHeight = 22
    creatorX = app.width // 2
    creatorY = app.height - creatorHeight - creatorClassHeight - app.labelMargin
    drawImage(app.creator, creatorX, creatorY, align='center')

    creatorClassX = app.width // 2
    creatorClassY = creatorY + creatorHeight
    drawImage(app.creatorClass, creatorClassX, creatorClassY, align='center')

def spawnEnemy(app):
    # chiwarra and dalekh appear only in third rounds of each level
    snakeAllowed = False
    greenAllowed = False
    numSnakes = calculateSnakes(app.enemies)
    copyEnemyTypes = copy.copy(app.enemyTypes)

    if numSnakes < app.maxSnakesOnBoard:
        snakeAllowed = True

    # dalekh and chiwarra can appear a limited number of times
    if app.greenEnemyAppear < app.maxGreenEnemyAppear:
        # also they appear from the second round
        if app.round >= 2:
            # also it does not make sense for them to appear in the beginning
            # i will do implement the feature when they appear when only less than
            # a certain number of blocks left
            if app.rawBlocks <= 5:
                greenAllowed = True
    
    if not snakeAllowed:
        # if the snake is not allowed,
        # simply remove it from the copy version
        # of the enemyTypes
        copyEnemyTypes.remove(app.enemyTypes[1])
    
    if not greenAllowed:
        # if the green enemy is not allowed
        # do the same as snakeAllowed
        copyEnemyTypes.remove(app.enemyTypes[2])
        copyEnemyTypes.remove(app.enemyTypes[3])
    else:
        # if the green allowed, then they should appear immediately
        copyEnemyTypes.remove(app.enemyTypes[0])
        if app.enemyTypes[1] in copyEnemyTypes:
            copyEnemyTypes.remove(app.enemyTypes[1])

    enemyType = randomEnemySelection(copyEnemyTypes)

    if app.round >= 2:
        # check how many times dalekh and chiwarra appeared
        if enemyType == app.enemyTypes[2] or enemyType == app.enemyTypes[3]:
            app.greenEnemyAppear += 1

    randomBlockIndex = randint(0, 1)
    randomBlock = None
    enemyImage = None

    # UNDER DEVELOPMENT
    # if enemyType == app.enemyTypes[2]:
    #     # revilo
    #     # the last row but the first column
    #     randomBlock = app.board[-1][0]
    #     print(randomBlock.sideCenter)
    # elif enemyType == app.enemyTypes[3]:
    #     # thavani
    #     # the last row and the last column
    #     randomBlock = app.board[-1][-1]
    # else:
        # standard way

    randomBlock = app.board[1][randomBlockIndex]
    
    if enemyType == app.enemyTypes[0] \
        or enemyType == app.enemyTypes[1]:
        # simple enemies
        enemyImage = app.enemyImageBase + f'{enemyType}-idle.png'
    else:
        # special enemies: revilo, thavani, dalekh, and chiwarra
        direction = 'down-right'
        enemyImage = app.enemyImageBase + f'{enemyType}-{direction}-idle.png'

    # UNDER DEVELOPMENT
    # if enemyType == app.enemyTypes[2] \
    #     or enemyType == app.enemyTypes[3]:
    #     # aliens have different centers
    #     # the first time it appears
    #     # it is faced the down-right direction
    #     newEnemy = Enemy(tag=enemyType, center=randomBlock.getRightSideCenter(), 
    #                 block=randomBlock, type=enemyType, state=app.enemyStates[0], 
    #                 image=enemyImage, direction='down-right')
    # else:
    newEnemy = Enemy(tag=enemyType, center=randomBlock.getCenter(), 
        block=randomBlock, type=enemyType, state=app.enemyStates[0], 
        image=enemyImage, direction='')
    
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
        elapsedTime = time.time() - enemy.moveTime
        addSpeed = 0

        # how fast the enemy increases in speed upon each round and level
        # depends on its type
        if enemy.type == app.enemyTypes[0]:
            # the red enemy remains the same
            addSpeed = app.gameAddSpeed
        elif enemy.type == app.enemyTypes[1]:
            # the snake is twice the speed of the game
            addSpeed = 2 * app.gameAddSpeed

        if elapsedTime - (enemy.jumpInterval - addSpeed) > 0:
            enemyMove(app, enemy)

def enemyMove(app, enemy: Enemy):
    if enemy.state == app.enemyStates[0]:
        
        if enemy.type == app.enemyTypes[0]:
            app.redEnemyJump.play()
        elif enemy.type == app.enemyTypes[1]:
            if enemy.transformation:
                app.snakeJump.play()
            else:   
                app.purpleEnemyJump.play()
        row, col = enemy.block.position

        if not enemy.inPursue:
            enemy.move = randint(0, 1)
        else:
            enemyPursue(app, enemy)

        # UNDER DEVELOPMENT
        # we need to save the previous direction 
        # of the enemy, which is an alien, so
        # that we could identify centers of the block
        # the alien is currently located.
        # if enemy.type == app.enemyTypes[2] \
        #     or enemy.type == app.enemyTypes[3]:
        #     enemy.prevDirection = enemy.direction

        if enemy.move == 0:
            enemy.direction = 'down-left'
        elif enemy.move == 1:
            enemy.direction = 'down-right'
        elif enemy.move == 2:
            enemy.direction = 'top-right'
        else:
            enemy.direction = 'top-left'

        sign = +1 if enemy.move <= 1 else -1

        nextRow, nextCol = row + sign, col + sign * (enemy.move % 2)
        if isPositionLegal(app, nextRow, nextCol):
            # if the enemy can jump to the next block
            # first, update the enemy model by calling jump()
            # which updates next block, velocity, and angle
            nxtBlock = app.board[nextRow][nextCol]
            
            # UNDER DEVELOPMENT
            # aliens have a special type of jump
            # they jump on sides of the blocks rather than tops

            # if enemy.type == app.enemyTypes[2] \
            #     or enemy.type == app.enemyTypes[3]:
            #     enemy.alienJump(nxtBlock, app.jumpAngle, enemy.direction)
            # else:

            enemy.jump(nxtBlock, app.jumpAngle, enemy.direction)

            enemy.state = app.enemyStates[1]
            # change the picture of the enemy: snake, dalekh, chiwarra
            if enemy.transformation or (enemy.type == app.enemyTypes[2] or enemy.type == app.enemyTypes[3]):
                enemy.image = app.enemyImageBase + f'{enemy.type}-{enemy.direction}-jump.png'
            elif enemy.type == app.enemyTypes[0] or enemy.type == app.enemyTypes[1]:
                enemy.image = app.enemyImageBase + f'{enemy.type}-jump.png'
        else:
            if enemy.type == app.enemyTypes[1]:
                # snake should start pursuing the player
                # snake is in pursue
                # 
                if not enemy.transformation:
                    enemy.transformation = True
                enemy.inPursue = True
                enemyPursue(app, enemy)
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

            # the two enemies: dalekh and chiwarra change the colors of the blocks
            if enemy.type == app.enemyTypes[2] \
                or enemy.type == app.enemyTypes[3]:
                block = enemy.block
                if block.mainColor == app.targetColor:
                    block.mainColor = app.mainColor
                    app.rawBlocks += 1

            # enemy is not in the jumping state anymore
            enemy.state = app.enemyStates[0]
            # increase the move time of the enemy
            enemy.moveTime += enemy.jumpInterval

            # changing the picture of the enemy
            if enemy.transformation or (enemy.type == app.enemyTypes[2] or enemy.type == app.enemyTypes[3]):
                enemy.image = app.enemyImageBase + f'{enemy.type}-{enemy.direction}-idle.png'
            elif enemy.type == app.enemyTypes[0] or enemy.type == app.enemyTypes[1]:
                enemy.image = app.enemyImageBase + f'{enemy.type}-idle.png'

def enemyPursue(app, enemy):
    enemyBlckCx, enemyBlckCy = enemy.block.getCenter()
    playerBlckCx, playerBlckCy = app.player.block.getCenter()

    enemyBlckRow, _ = enemy.block.position

    yOffset = playerBlckCy - enemyBlckCy
    xOffset = playerBlckCx - enemyBlckCx

    if yOffset > 0:
        # the player is below the snake 
        if xOffset < 0:
            # the player is to the left of the snake
            # snake should jump down-left
            enemy.move = 0
        else:
            # the player is to the right of the snake
            # snake should jump down-right
            enemy.move = 1
    elif yOffset < 0:
        # the player is above the snake
        if xOffset < 0:
            # the player is to the left of the snake
            # snake should jump top-left
            enemy.move = 3
        else:
            # the player is to the right of the snake
            # snake should jump top-right
            enemy.move = 2
    else:
        # the enemy and the player are aligned horizontally
        # first calculate legal jump locations

        if xOffset < 0:
            # the player is to the left of the snake
            # snake can jump to either top or down left
            # but there is an exception if the snake is located at the bottom row
            if enemyBlckRow == app.rows:
                # the enemy is on the last row, it can jump only top left
                enemy.move = 3
            else:
                # the enemy is somewhere in the middle
                enemy.move = randrange(0, 4, 3)
        else:
            # the player is to the right of the snake
            # snake can jump to either top or down right
            # to be closer to the player
            # but there is an exception when the snake is located at the bottom row
            if enemyBlckRow == app.rows:
                # the enemy is on the last row, it can jump only top right
                enemy.move = 2
            else:
                # the enemy is somewhere in the middle
                enemy.move = randint(1, 2)

def detectCollision(app):
    playerCx, playerCy = app.player.getCenter()
    enemies = app.enemies

    for enemy in enemies:
        enemyCx, enemyCy = enemy.getCenter()

        if enemyCx >= playerCx - app.playerWidth // 4 \
            and enemyCx <= playerCx + app.playerWidth // 4:

            if enemyCy >= playerCy - app.playerHeight // 4 \
                and enemyCy <= playerCy + app.playerHeight // 4:

                if (enemy.type == app.enemyTypes[2] or enemy.type == app.enemyTypes[3]):
                    # the two enemies: dalekh and chiwarra do not kill the player

                    # the collision works only when the player is idle

                    if app.player.state == app.playerStates[0]:
                        index = findModelIndex(app.enemies, enemy.id)
                        app.enemies.pop(index)
                else:
                    # no spawning enemy
                    app.enemiesSpawned = False
                    
                    # enemies get removed immediately
                    app.enemies.clear()

                    res = app.player.takeLife()
                    # display swear and play a swear music
                    app.swear.play()

                    if res == -1:
                        # no lives left
                        app.gameState = app.gameStates[6]
                    else:
                        # the state of the game changes to 'playerDied'
                        app.gameState = app.gameStates[4]
                        # the game gets paused
                        app.paused = True
                        # setting the death time of the player
                        # this is needed to count the time till the revival
                        app.playerDeathTime = time.time()

def checkBlockColors(app):
    if app.rawBlocks == 0:
       # player has successfuly passed the level!
        app.animationStartTime = time.time()
        app.gameState = app.gameStates[3]
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

def calculateSnakes(enemies):
    count = 0
    for enemy in enemies:
        if enemy.type == 'snake':
            count += 1
    return count

def createDisks(board, blockRadius, diskImageBase, number=2):
    leftBlock = board[-2][0]
    rightBlock = board[-2][-1]
    
    leftBlockCx, leftBlockCy = leftBlock.getCenter()
    rightBlockCx, rightBlockCy = rightBlock.getCenter()

    leftDiskCx = leftBlockCx - blockRadius
    leftDiskCy = leftBlockCy - blockRadius

    rightDiskCx = rightBlockCx + blockRadius
    rightDiskCy = rightBlockCy - blockRadius

    centers = [(leftDiskCx, leftDiskCy), (rightDiskCx, rightDiskCy)]
    
    disks = list()
    for i in range(number):
        diskImage = diskImageBase + f'disk1.png'
        row = len(board) - 2
        col = 0 if i == 0 else len(board[row]) - 1
        blockUp = None
        if col == 0:
            blockUp = board[row-1][0]
        else:
            blockUp = board[row-1][row-1]
        disk = Disk('disk', centers[i], imageId=1, image=diskImage, \
                    position=(row, col), blockUp=blockUp)
        disks.append(disk)

    return disks

def animateDisks(app):
    animated = False
    for disk in app.disks:
        elapsedTime = time.time() - app.gameStartTime
        if elapsedTime - app.diskImageChangeInterval > 0:
            if disk.imageId < 4:
                disk.imageId += 1
            else:
                disk.imageId = 1
            disk.image = app.diskImageBase + f'disk{disk.imageId}.png'
            animated = True
    if animated:
        app.diskImageChangeInterval += app.fixedDiskImageChangeInterval

def isDiskPresent(app, row, col):
    for disk in app.disks:
        diskRow, diskCol = disk.position
        if row == diskRow and diskCol == col:
            return disk
    return -1

def nextGame(app):
    # Increase the score of the player
    currentRound = app.round
    currentLevel = app.level
    currentRows = app.rows
    prevScore = app.player.getScore()
    remainingLives = app.player.getLives()
    curMaxEnemiesOnBoard = app.maximumEnemiesOnBoard
    curGameAddSpeed = app.gameAddSpeed
    curMaxGreenEnemyAppear = app.maxGreenEnemyAppear
    curEnemySpawnFixedInterval = app.enemySpawnFixedInterval

    onAppStart(app)

    app.gameState = app.gameStates[1]
    app.levelStartMusic.play()
    app.startLevelInitTime = time.time()

    if currentRound < app.rounds:
        app.round = currentRound + 1
        app.level = currentLevel
        if app.level > 1 and app.round > 1:
            app.rows = currentRows
            app.board = createBoard(app, app.rows, app.wrapperHeight // 4)
            app.rawBlocks = countBlocks(app.board)
            app.disks = createDisks(app.board, app.radius, app.diskImageBase)

        if curMaxEnemiesOnBoard < app.fixedMaxEnemiesOnBoard:
            app.maximumEnemiesOnBoard = curMaxEnemiesOnBoard + 1

        if curGameAddSpeed < app.maxGameAddSpeed:
            app.gameAddSpeed = curGameAddSpeed + app.fixedGameAddSpeed
        
        if curEnemySpawnFixedInterval > app.minEnemySpawnInterval:
            app.enemySpawnFixedInterval = curEnemySpawnFixedInterval - 1

    elif currentLevel < app.levels:
        app.rows = currentRows + 1
        app.board = createBoard(app, app.rows, app.wrapperHeight // 4)
        app.rawBlocks = countBlocks(app.board)
        app.disks = createDisks(app.board, app.radius, app.diskImageBase)
        app.level = currentLevel + 1

        app.gameAddSpeed = app.fixedGameAddSpeed * (app.level - 1)
        app.maxGreenEnemyAppear = curMaxGreenEnemyAppear + 1

        app.enemySpawnFixedInterval -= (app.level - 1)
    else:
        # complete win
        app.gameState = app.gameStates[5]
    
    app.player.updateLives(remainingLives)
    app.player.updateScore(prevScore + app.completionBonus)

def continueGame(app):
    # The player has no lives left
    # but he has the option to continue playing the game
    # that will keep the difficulty level
    # the only thing that changes is that 
    # the player gets his lives back
    currentRound = app.round
    currentLevel = app.level
    currentRows = app.rows
    currentScore = app.player.getScore()
    curMaxEnemiesOnBoard = app.maximumEnemiesOnBoard
    curGameAddSpeed = app.gameAddSpeed
    curMaxGreenEnemyAppear = app.maxGreenEnemyAppear
    curEnemySpawnFixedInterval = app.enemySpawnFixedInterval

    onAppStart(app)

    app.round = currentRound
    app.level = currentLevel
    app.rows = currentRows
    app.board = createBoard(app, app.rows, app.wrapperHeight // 4)
    app.rawBlocks = countBlocks(app.board)
    app.gameAddSpeed = app.fixedGameAddSpeed * (app.level - 1)
    app.maximumEnemiesOnBoard = curMaxEnemiesOnBoard
    app.enemySpawnFixedInterval = curEnemySpawnFixedInterval
    app.gameAddSpeed = curGameAddSpeed
    app.maxGreenEnemyAppear = curMaxGreenEnemyAppear

    app.gameState = app.gameStates[2]
    app.gameStartTime = time.time()

    app.player.updateScore(currentScore)

def nextInstruction(app):
    if app.instructionId < app.maxInstruction - 1:
        app.instructionId += 1
        app.instructionStartTime = time.time()
        app.instructionPlayerInterval = 0.5
    else:
        # the game will start
        # stop the music
        app.mainTheme.pause()
        # change the state of the  game
        app.gameState = app.gameStates[1]
        app.startLevelInitTime = time.time()
        app.levelStartMusic.play()

def createJoysticks(app):
    joysticks = list()
    joystickWidth = 128
    cx = app.width - joystickWidth // 2 - 4 * app.labelMargin
    cy = app.height // 2
    state = 'idle'
    for direction in app.joystickDirections:
        image = app.joystickBase + f'{state}.png'
        stick = JoystickInstruction('joystick', (cx, cy), image, direction, state, 1)
        joysticks.append(stick)
    return joysticks

# Arcade Support
def onJoyPress(app, button, joystick):
    if button == '9':
        # Start
        if app.gameState == app.gameStates[0]:
            app.playButtonState = 'on'
            app.btnIsPressed = True
            app.startLevelInitTime = time.time()
            app.levelStartMusic.play()
        elif app.gameState == app.gameStates[8]:
            onAppStart(app)

    if button == '5':
        # P1
        sys.exit(0)

    if button == '1':
        # A: To continue the game when the player died
        continueGame(app)

    if button == '2':
        if app.gameState == app.gameStates[7]:
            # The instructions
            app.jump1Music.play()
            nextInstruction(app)

    if button == '0':
        # B: To end the game
        app.gameState = app.gameStates[8]

def onDigitalJoyAxis(app, results, joystick):
    """
    if key == 'down':
        direction += 'down-left'
    elif key == 'up':
        direction += 'top-right'
    elif key == 'left':
        direction += 'top-left'
    elif key == 'right':
        direction += 'down-right'
    """
    key = ''
    if (1, -1) in results:
        # top-right
        key = 'up'
    elif (1, 1) in results:
        # down-left
        key = 'down'
    
    if (0, -1) in results:
        # top-left
        key = 'left'
        
    elif (0, 1) in results:
        # down-right
        key = 'right'

    if not app.paused \
        and app.gameState == app.gameStates[2] \
        and app.player.state != app.playerStates[1] \
        and app.player.state != app.playerStates[3] \
        and app.player.state != app.playerStates[4]:
        if key in app.allowedMovementKeys:
            # the player is jumping
            playerJump(app, app.board, app.player, app.playerStates, key)

def playGame():
    runApp(width=800, height=600)

def main():
    playGame()

main()