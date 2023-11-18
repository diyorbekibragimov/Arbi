import time

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

class Player(Actor):
    def __init__(self, tag: str, center: tuple, block: Block, direction: str, image: str) -> None:
        cx, cy = center
        cy -= 100
        center = (cx, cy)
        super().__init__(tag, center)

        self.block = block
        self.direction = direction
        self.image = image

class Enemy(Actor):
    id = 0
    count = 0
    def __init__(self, tag: str, center: tuple, block: Block, type: str, move: int) -> None:
        tag = f'{tag}{Enemy.id}'
        # add a falling effect when the enemy spawns
        cx, cy = center
        cy -= 100
        center = (cx, cy)
        super().__init__(tag, center)

        self.id = Enemy.id
        self.block = block
        self.type = type
        self.move = move
        self.moveTime = time.time()

        Enemy.id += 1
        Enemy.count += 1