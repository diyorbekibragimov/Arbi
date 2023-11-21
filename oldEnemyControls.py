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
                app.gameState = app.gameStates[5]
                break
            # the game gets paused
            app.paused = True
            # the state of the game changes to 'playerDied'
            app.gameState = app.gameStates[3]
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
                    #if enemy.state == app.enemyStates[0]:
                    redEnemyControls(app, enemy)
                    # else:
                    #     if not enemy.landed:
                    #         enemy.handleJump()
                    #     else:
                    #         enemy.landed = False
                    #         # the enemy has fully jumped to the block
                    #         enemy.moveTime += app.fixedEnemyControlInterval
                    #         enemy.velocity = 0
                    #         enemy.state = app.enemyStates[0]
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
        app.enemies[index] = enemy
        enemy.move = randint(0, 1)
        # nextBlock = app.board[nextRow][nextCol]
        # _, curBlockCy = app.player.block.getCenter()
        # _, nxtBlockCy = nextBlock.getCenter()
        # angle = 45
        # initialVelocity = (nxtBlockCy - curBlockCy) // 10
        # enemy.jump(nextBlock, initialVelocity, angle) # sets the next jumping block of the enemy
        # enemy.move = randint(0, 1)
        # enemy.direction = 'down-left' if enemy.move == 0 else 'down-right'
        # enemy.state = app.enemyStates[1]
    else:
        app.enemies.pop(index)



class Enemy(MovingActor):
    id = 0
    count = 0
    def __init__(self, tag: str, center: tuple, block: Block, type: str, move: int, imageId: int, direction: str, velocity: int, state: str) -> None:
        tag = f'{tag}{Enemy.id}'
        # add a falling effect when the enemy spawns
        cx, cy = center
        cy -= 100
        center = (cx, cy)
        super().__init__(tag, center, block, nextBlock=None, direction=direction, velocity=velocity, angle=0)

        self.id = Enemy.id
        self.block = block
        self.type = type
        self.move = move
        self.spawnTime = time.time()
        self.moveTime = time.time()
        self.imageChangeInterval = 0.3
        self.imageId = imageId
        self.state = state
        self.landed = False

        Enemy.id += 1
        Enemy.count += 1
    
    def increaseImageChangeInterval(self, interval: int):
        self.imageChangeInterval += interval