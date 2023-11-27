import time, math

class Actor():
    id = 0
    def __init__(self, tag: str, center: tuple) -> None:
        self.tag = tag
        self.center = center # coordinates of the center of the object
        Actor.id += 1
    
    def __repr__(self) -> str:
        return f"{self.tag} at {self.center}"

    def getCenter(self) -> tuple:
        return self.center
    
    def changeCenter(self, newCenter: tuple):
        self.center = newCenter

class Block(Actor):
    id = 0
    def __init__(self, tag: str, center: tuple, position: tuple, mainColor: str, sideColors: list) -> None:
        tag = f'{tag}{Block.id}'
        super().__init__(tag, center)
        self.position = position
        self.mainColor = mainColor
        self.sideColors = sideColors
        self.sideCenter = None
        Block.id += 1

    def getSideCenter(self):
        return self.sideCenter
    
    def getLeftSideCenter(self):
        return self.sideCenter[0]

    def getRightSideCenter(self):
        return self.sideCenter[1]

class MovingActor(Actor):
    gravity = 0.9
    def __init__(self, tag: str, center: tuple, block: Block, direction: str):
        super().__init__(tag, center)
        self.block = block
        self.nextBlock = None
        self.direction = direction
        self.angle = 0
        self.velocity = 0
        self.landed = False

    def handleJump(self):
        curBlockCx, _ = self.block.getCenter()
        nxtBlockCx, nxtBlockCy = self.nextBlock.getCenter()
        distanceX = nxtBlockCx - curBlockCx
        deltaX = distanceX // 10
        actorCx, actorCy = super().getCenter()

        # based on the direction of the player
        # its x and y coordinates should either
        # increase or decrease.
        """
            bottom right block: 
                x increases
                y increases
            
            bottom left block:
                x decreases
                y increases

            top right block:
                x increases
                y decreases
            
            top left block:
                x decreases
                y decreaes
        """
        if self.direction == 'down-right':
            if actorCx < nxtBlockCx:
                actorCx += deltaX * math.cos(self.angle)
            if actorCy < nxtBlockCy:
                actorCy -= self.velocity * MovingActor.gravity

            if actorCx >= nxtBlockCx and actorCy >= nxtBlockCy:
                self.landed = True

        elif self.direction == 'down-left':
            if actorCx > nxtBlockCx:
                actorCx += deltaX * math.cos(self.angle)
            if actorCy < nxtBlockCy:
                actorCy -= self.velocity * MovingActor.gravity

            if actorCx <= nxtBlockCx and actorCy >= nxtBlockCy:
                self.landed = True
        
        elif self.direction == 'top-left':
            if actorCx > nxtBlockCx:
                actorCx += deltaX * math.cos(self.angle)
            if actorCy > nxtBlockCy:
                actorCy += self.velocity * MovingActor.gravity

            if actorCx <= nxtBlockCx and actorCy <= nxtBlockCy:
                self.landed = True
        
        elif self.direction == 'top-right':
            if actorCx < nxtBlockCx:
                actorCx += deltaX * math.cos(self.angle)
            if actorCy > nxtBlockCy:
                actorCy += self.velocity * MovingActor.gravity

            if actorCx >= nxtBlockCx and actorCy <= nxtBlockCy:
                self.landed = True

        if not self.landed:
            super().changeCenter((actorCx, actorCy))
            self.velocity -= MovingActor.gravity
        else:
            super().changeCenter((nxtBlockCx, nxtBlockCy))
            self.block = self.nextBlock

    def jump(self, nxtBlock, angle, direction):
        _, curBlockCy = self.block.getCenter()
        _, nxtBlockCy = nxtBlock.getCenter()
        self.nextBlock = nxtBlock
        self.velocity = (nxtBlockCy-curBlockCy) // 10
        self.angle = angle
        self.direction = direction

class Player(MovingActor):
    def __init__(self, tag: str, center: tuple, block: Block, direction: int, image: str, lives: int, state: str) -> None:
        super().__init__(tag, center, block, direction=direction)

        self.score = 0
        self.image = image
        self.lives = lives
        self.state = state
        self.disk = None
        self.landed = False
        self.dropOffVelocity = 0
    
    def getScore(self):
        return self.score
    
    def updateScore(self, value):
        self.score += value

    def getLives(self) -> int:
        return self.lives

    def takeLife(self) -> int:
        if self.lives > 1:
            self.lives -= 1
            return self.lives
        else:
            self.lives -= 1
            return -1
        
    def updateLives(self, val) -> bool:
        if 0 < val <= 3:
            self.lives = val
            return True
        else:
            return False
        
    def getDirection(self):
        return self.direction
    
    def jumpDisk(self, disk, angle, direction):
        _, cy = self.getCenter()
        _, diskCy = disk.getCenter()
        self.velocity = (diskCy-cy) // 10
        self.angle = angle
        self.direction = direction
        self.disk = disk

    def handleDiskJump(self):
        blockCx, _ = self.block.getCenter()
        diskX, diskY = self.disk.getCenter()
        distanceX = diskX - blockCx
        deltaX = distanceX // 10
        actorCx, actorCy = super().getCenter()

        # based on the direction of the player
        # its x and y coordinates should either
        # increase or decrease.
        if self.direction == 'top-left':
            if actorCx > diskX:
                actorCx += deltaX * math.cos(self.angle)
            if actorCy > diskY:
                actorCy += self.velocity * 0.9

            if actorCx <= diskX and actorCy <= diskY:
                self.landed = True
        
        elif self.direction == 'top-right':
            if actorCx < diskX:
                actorCx += deltaX * math.cos(self.angle)
            if actorCy > diskY:
                actorCy += self.velocity * 0.9

            if actorCx >= diskX and actorCy <= diskY:
                self.landed = True

        if not self.landed:
            super().changeCenter((actorCx, actorCy))
            self.velocity -= MovingActor.gravity
        else:
            super().changeCenter((diskX, diskY))

class Enemy(MovingActor):
    id = 0
    count = 0
    def __init__(self, tag: str, center: tuple, block: Block, type: str, state: str, image: str, direction: str) -> None:
        tag = f'{tag}{Enemy.id}'

        # add a falling effect when the enemy spawns
        cx, cy = center
        if type != 'revilo' and type != 'thavani':
            cy -= 100
        else:
            cx -= 100
        center = (cx, cy)

        super().__init__(tag, center, block, direction='down-left')

        # Each enemy has different 'speeds'
        # by speed, here I mean how quick the enemy
        # should start jumping to the next block
        if type == 'red':
            self.jumpInterval = 1
        elif type == 'snake':
            self.jumpInterval = 1.5
        elif type == 'dalekh' or type == 'chiwarra':
            # their speeds are equal
            self.jumpInterval = 0.8

        self.id = Enemy.id
        self.type = type
        self.image = image
        self.state = state
        self.direction = direction

        self.move = 0
        self.spawnTime = time.time()
        self.moveTime = time.time()
        self.inPursue = False
        self.transformation = False
        self.prevDirection = None

        Enemy.id += 1
        Enemy.count += 1

    def alienJump(self, nxtBlock, angle, direction):
        # special jump for aliens that jump on the sides of the block
        # revilo and thavani

        _, curSideCy = None
        _, nxtSideCy = None
        curSide = self.prevDirection.split('-')[1]
        nxtSide = direction.split('-')[1]

        if curSide == 'left':
            _, curSideCy = self.block.getLeftSideCenter()
        else:
            _, curSideCy = self.block.getRightSideCenter()
        
        if nxtSide == 'left':
            _, nxtSideCy = self.block.getLeftSideCenter()
        else:
            _, nxtSideCy = self.block.getRightSideCenter()

        self.nextBlock = nxtBlock
        self.velocity = (nxtSideCy-curSideCy) // 10
        self.angle = angle
        self.direction = direction

class Disk(Actor):
    id = 0
    def __init__(self, tag: str, center: tuple, imageId: int, image: str, position: tuple, blockUp: Block):
        tag = f'{tag}{Disk.id}'
        super().__init__(tag, center)

        self.id = Disk.id
        self.imageId = imageId
        self.image = image
        self.position = position
        self.imageSetTime = time.time()
        self.imageChangeInterval = 0.09
        self.blockUp = blockUp
        self.velocity = 0
        self.diagonalVelocityX = 0
        self.diagonalVelocityY = 0

        Disk.id += 1

class Star(Actor):
    id = 0
    count = 0
    def __init__(self, tag: str, center: tuple, image: str):
        super().__init__(tag, center)

        self.image = image
        self.id = Star.id
        Star.count += 1
    
    def getImage(self):
        return self.image