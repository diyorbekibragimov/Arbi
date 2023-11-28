from models import Player
from loadImages import (PLAYER_BASE_IMAGE, DISK_BASE_IMAGE)
from helper_functions import createBoard, createDisks, getDimensions

def loadGameStates() -> list:
    states = ['start', 'levelTrans', 'inprogress', \
              'levelComplete', 'playerDied', 'gameEnd', \
                'fail', 'instructions']
    return states

def loadPlayerStates() -> list:
    states = ['idle', 'jump', 'disk', 'fly', 'dropoff']
    return states

def loadEnemyTypes() -> list:
    states = ['red', 'snake', 'dalekh', 'chiwarra']
    return states

def loadMainColors() -> list:
    mainColors = [
        ['royalBlue', 'salmon', 'limeGreen'],
        ['gainsboro', 'lightSlateGray', 'lightCyan'],
        ['orange', 'mistyRose', 'springGreen']
    ]
    return mainColors

def loadSideColors() -> list:
    colors = [
        [['cadetBlue', 'slateGray'], ['darkGray', 'dimGray'], 
            ['black', 'black']],
        [['limeGreen', 'mediumSeaGreen'], ['darkOrchid', 'slateBlue'], 
            ['black', 'black']],
        [['peru', 'saddleBrown'], ['linen', 'antiqueWhite'], 
            ['black', 'black']]
    ]
    return colors

def loadTargetColors() -> list:
    colors = ['yellow', 'dodgerBlue', 'steelBlue']
    return colors

def loadJoystickDirections() -> list:
    directions = ['up', 'right', 'down', 'left']
    return directions

def loadAllowedMovements() -> list:
    movements = ['down', 'right', 'up', 'left']
    return movements

def loadEnemyStates() -> list:
    states = ['idle', 'jump']
    return states