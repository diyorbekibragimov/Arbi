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
        Block.id += 1

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

        self.block = block
        self.nextBlock = None
        self.score = 0
        self.image = image
        self.lives = lives
        self.state = state
    
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

class Enemy(MovingActor):
    id = 0
    count = 0
    def __init__(self, tag: str, center: tuple, block: Block, type: str, imageId: int, state: str, image: str) -> None:
        tag = f'{tag}{Enemy.id}'

        # add a falling effect when the enemy spawns
        cx, cy = center
        cy -= 100
        center = (cx, cy)

        super().__init__(tag, center, block, direction='down-left')

        self.id = Enemy.id
        self.type = type
        self.move = 0
        self.spawnTime = time.time()
        self.moveTime = time.time()
        self.imageChangeInterval = 0.3
        self.imageId = imageId
        self.state = state
        self.inPursue = False
        self.transformation = False
        self.image = image
        self.direction = None

        Enemy.id += 1
        Enemy.count += 1
    
    def increaseImageChangeInterval(self, interval: int):
        self.imageChangeInterval += interval

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