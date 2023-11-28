from cmu_graphics import Sound
import pathlib
# Music Effects
# Cite: Professor Eduardo [Piazza]

cntPath = pathlib.Path(__file__).parent.resolve()

jump1Music = Sound(f'file://{cntPath}/media/music/jump1.mp3')
swear = Sound(f'file://{cntPath}/media/music/swear.mp3')
victoryMusic = Sound(f'file://{cntPath}/media/music/victory.mp3')
mainTheme = Sound(f'file://{cntPath}/media/music/mainTheme.mp3')
redEnemyJump = Sound(f'file://{cntPath}/media/music/redEnemyJump.mp3')
purpleEnemyJump = Sound(f'file://{cntPath}/media/music/snakeJump.mp3')
snakeJump = Sound(f'file://{cntPath}/media/music/grownSnakeJump.mp3')
levelStartMusic = Sound(f'file://{cntPath}/media/music/levelStart.mp3')
liftMusic = Sound(f'file://{cntPath}/media/music/lift.mp3')