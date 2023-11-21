from cmu_graphics import *


def onAppStart(app):
    app.g = 10 # gravitational force
    app.initialSpeed = -90 # initial speed
    app.stepsPerSecond = 30 # frames per second
    app.speed = app.initialSpeed # cube speed
    app.jumping = False # is cube jumping 'up' or 'down'
    app.x = app.width // 2
    app.y = app.height // 2
    app.ground = app.height // 2 + 60


def redrawAll(app):
    drawRect(app.x, app.y, 60, 60, fill=rgb(60, 60, 220))
    drawLine(0, app.ground, app.width, app.ground)


def onStep(app):
    if app.jumping:
        if app.jumping == "up":
            # when the speed reaches 0 start going down
            if app.speed + app.g > 0:
                app.jumping = "down"
            else:
                # else decrease the speed and change the cube coordinate
                app.speed += app.g
                app.y += app.speed
        else:
            # when speed reaches initial speed stop the cube on the ground
            if app.speed + app.g >= abs(app.initialSpeed):
                app.jumping = False
                app.speed = app.initialSpeed
            else:
                # or else accelerate by g and keep going down
                app.speed += app.g
                app.y += app.speed


def onKeyPress(app, key):
    if key == "space":
        app.jumping = True


if __name__ == "__main__":
    runApp(800, 800)