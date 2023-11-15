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

class Block(Actor):
    id = 0
    def __init__(self, tag: str, center: tuple, position: tuple, colors: list) -> None:
        tag = f'{tag}{Block.id}'
        super().__init__(tag, center)
        self.position = position
        self.colors = colors
        Block.id += 1

class Player(Actor):
    def __init__(self, tag: str, center: tuple, currentBlock: Block) -> None:
        super().__init__(tag, center)
        self.currentBlock = currentBlock

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

        Enemy.id += 1
        Enemy.count += 1