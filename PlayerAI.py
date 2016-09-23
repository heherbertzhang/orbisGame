from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *

DODGEWEIGHT = 20
GETPOWERWEIGHT = 15 #dynamic changing after get all the powers
SHOOTWEIGHT = 10

nextRight, nextLeft, nextUp, nextDown = 0, 0, 0, 0
nextCount = 0

def getPowerPoints(gameboard, player):
#full mark is 100 per direction
        powerUps = gameboard.power_ups
        pX = player.x
        pY = player.y
        rightTotal, leftTotal, upTotal, downTotal = 0, 0, 0, 0
        maxScore = len(powerUps) * 100
        if(maxScore == 0):
                return [0, 0, 0, 0]
        for powerUp in powerUps:

                xDist = pX - powerUp.x
                yDist = pY - powerUp.y
                absXdist = abs(xDist)
                absYdist = abs(yDist)
                #print('!!!!!', xDist, yDist)
                #shortXDist = min(absXdist, gameboard.width - absXdist)
                #calculate scores
                right, left, up, down = 0, 0, 0, 0
                horiScore = 0
                if xDist != 0:
                        horiScore = 100/xDist
                vertiScore = 0
                if yDist != 0:
                        vertiScore = 100/yDist

                xratio = 0.5 * vertiScore
                yratio = 0.5 * horiScore

                if xDist < 0:
                        right = -(horiScore)
                        left = 100/(gameboard.width - absXdist)
                elif xDist > 0:
                        left = horiScore
                        right = 100/(gameboard.width - absXdist)
                left += xratio
                right += xratio
                #only keep one side's score
                if(right > left):
                        left = 0
                else:
                        right = 0

                if yDist < 0:
                        down = -(vertiScore)
                        up = 100/(gameboard.height - absYdist)
                elif yDist > 0:
                        up = vertiScore
                        down = 100/(gameboard.height - absYdist)
                if(up > down):
                        down = 0
                else:
                        up = 0
                up += yratio
                down += yratio
                rightTotal += right
                leftTotal += left
                upTotal += up
                downTotal += down

                if player.direction == Direction.UP:
                        upTotal += 0
                elif player.direction == Direction.DOWN:
                        downTotal += 0
                elif player.direction == Direction.LEFT:
                        leftTotal += 0
                elif player.direction == Direction.RIGHT:
                        rightTotal += 0

        #tune down the total mark to be within range 100

        rightTotal = rightTotal / maxScore * 100
        leftTotal = leftTotal / maxScore * 100
        upTotal = upTotal / maxScore * 100
        downTotal = downTotal / maxScore * 100

        return [upTotal, downTotal, leftTotal, rightTotal]



def calculateRightThreatScore(xDist, playerDirect, gameboardwidth):
        #bullet at the travel from right to left
        #bullet at the right side
        if xDist == 0:
                left = 0
                right = 0
        elif xDist < 0:
                absXdist = abs(xDist)
                if playerDirect == Direction.RIGHT:
                        right = 100/(absXdist - 1)#need one turn to turn away
                else:
                        right = 100/(absXdist - 2)# need one more turn to turn right and then turn away
                if playerDirect != Direction.LEFT:
                #turn to left can cause bullet hit if too close
                        left = 100/(absXdist)
                else:#player face left
                        left = 100/(absXdist + 1) + 5 #not that good so + 5
        elif xDist > 0:
                #bullet at the left side
                absXdist = gameboardwidth - xDist
                if playerDirect == Direction.RIGHT:
                        right = 100/(absXdist - 1)#need one turn to turn away
                else:
                        right = 100/(absXdist - 2)# need one more turn to turn right and then turn away
                if playerDirect != Direction.LEFT:
                        #turn to left can cause bullet hit if too close
                        left = 100/(absXdist)
                else:#player face left
                        left = 100/(absXdist + 1) + 5 #not that good so + 5

                return (right, left)

def calculateLeftThreatScore(xDist, playerDirect, gameboardwidth):
        #bullet at the travel from left to right
        #bullet at the left side
        if xDist == 0:
                left = 0
                right = 0

        elif xDist > 0:
                absXdist = abs(xDist)
                if playerDirect == Direction.LEFT:
                        if absXdist > 1:
                                left = 100/(absXdist - 1)#need one turn to turn away
                        else:
                                left = 100
                else:
                        if absXdist > 2:
                                left = 100/(absXdist - 2)# need one more turn to turn right and then turn away
                        else:
                                left = 100
                if playerDirect != Direction.RIGHT:
                        #turn to left can cause bullet hit if too close
                        right = 100/(absXdist)
                else:#player face left
                        right = 100/(absXdist + 1) + 5 #not that good so + 5
        elif xDist < 0:
                #bullet at the right side
                absXdist = gameboardwidth - xDist
                if playerDirect == Direction.LEFT:
                        if absXdist > 1:
                                left = 100/(absXdist - 1)#need one turn to turn away
                        else:
                                left = 100
                else:
                        if absXdist > 2:
                                left = 100/(absXdist - 2)# need one more turn to turn right and then turn away
                        else:
                                left = 100
                if playerDirect != Direction.RIGHT:
                #turn to left can cause bullet hit if too close
                        right = 100/(absXdist)
                else:#player face left
                        right = 100/(absXdist + 1) + 5 #not that good so + 5

        return (left, right)
def getDodgePoints(gameboard, player):

        bullets = gameboard.bullets
        walls = gameboard.walls
        turrets = gameboard.turrets
        maxScore = 100 * len(bullets)
        playerDirect = player.direction
        rightTotal, leftTotal, upTotal, downTotal = maxScore, maxScore, maxScore, maxScore

        for bullet in bullets:
                right, left, up, down = 0, 0, 0, 0
                xDist = player.x - bullet.x
                yDist = player.y - bullet.y
                threatXScore = 0
                if xDist != 0:
                        threatXScore = 100/xDist
                threatYScore = 0
                if yDist != 0:
                        threatYScore = 100/yDist
                #calculate the threatening value of each direction
                if (bullet.direction == Direction.RIGHT and abs(yDist) < 4):
                        right, left = calculateRightThreatScore(xDist, playerDirect, gameboard.width)
                        #bullet at the right side
                if bullet.direction == Direction.LEFT and abs(yDist) < 4:
                        left, right = calculateLeftThreatScore(xDist, playerDirect, gameboard.width)
                if bullet.direction == Direction.UP and abs(xDist) < 4:
                #similar condition to left threat convert up to left
                        if playerDirect == Direction.UP:
                                playerDirect = Direction.LEFT

                        elif playerDirect == Direction.DOWN:
                                playerDirect = Direction.RIGHT
                        up, down = calculateLeftThreatScore(yDist, playerDirect, gameboard.height)
                if bullet.direction == Direction.DOWN and abs(xDist) < 4:
                        if playerDirect == Direction.UP:
                                playerDirect = Direction.LEFT
                        elif playerDirect == Direction.DOWN:
                                playerDirect = Direction.RIGHT
                        down, up = calculateRightThreatScore(yDist, playerDirect, gameboard.height)

                rightTotal -= right
                leftTotal -= left
                upTotal -= up
                downTotal -= down
        #tune to out of 100
        if(maxScore != 0):
                rightTotal = rightTotal / maxScore * 100
                leftTotal = leftTotal / maxScore * 100
                upTotal = upTotal / maxScore * 100
                downTotal = downTotal / maxScore * 100

        #for turret in turrets:
               #if turret.x == player.x or turret.y == player.y:
                   #     if turret.cooldown_time < 2:
                         #       rightTotal -=

                return [upTotal, downTotal, leftTotal, rightTotal]
        else:
                return [0, 0, 0, 0]
def dodgeBullet(gameboard, player, directions):
        bullets = gameboard.bullets
        for bullet in bullets:
                if bullet.y == player.y:
                        xdist = bullet.x - player.x
                        if(bullet.direction == Direction.RIGHT):
                                if(xdist < 0 and abs(xdist) < 3):
                                        directions[2] -= 100
                                elif xdist > 0 and (gameboard.width - abs(xdist))<3:
                                        directions[2] -= 100
                        if(bullet.direction ==Direction.LEFT):
                                if xdist > 0 and xdist < 3:
                                        directions[3] -= 100
                                elif xdist < 0 and (gameboard.width - abs(xdist)) < 3:
                                        directions[3] -= 100
                #print("bulletx", bullet.x, player.x)
                if bullet.x == player.x:
                        ydist = bullet.y - player.y
                        if bullet.direction == Direction.UP:
                                if ydist > 0 and ydist < 3:
                                        #go up, bullet down
                                        directions[1] -= 100
                                        #print('avoid bullet!!!!!!!!!!!', directions[1])
                                elif ydist < 0 and (gameboard.width - abs(ydist)) < 3:
                                        directions[1] -= 100
                                        #print('avoid bullet2!!!!!!!!!!!', directions[1])
                        if bullet.direction == Direction.DOWN:
                                if ydist > 0 and (gameboard.width - ydist) < 3:
                                        #go down, down
                                        directions[0] -= 100
                                elif ydist < 0 and abs(ydist) < 3:
                                        directions[0] -= 100


def dodgeExploding(gameboard, player, directions):
        unsafey ={};
        unsafex ={};

        for i in gameboard.turrets:

                if (i.is_firing_next_turn  == True):
                    unsafex[i.x] = 1
                    unsafey[i.y] =1

        if (player.x -1) in unsafex:
                directions[2] -= 100
                print ("HAPPY")
        if (player.x+1) in unsafex:
                directions[3]-=100
                print ("SAD")
        if (player.y+1) in unsafey:
                directions[1]-=100
                print ("FUCK")
        if (player.y-1) in unsafey:
                directions[0]-=100
                print ("SEX")

        return

def getMaxValue(directions):
        direction = 0;
        for i in range(1,4):
                if directions[i] > directions[direction]:
                        direction = i
        return direction

def checkWall(gameboard, player, opponent, directions):
        #if it is wall, score set to 0
        walls = gameboard.walls
        walls.append(opponent)
        #walls = walls + gameboard.bullets
        for wall in walls:
                xWallDist = wall.x - player.x
                yWallDist = wall.y - player.y
                if wall.y == player.y:
                        print ('wall y ', wall.y)
                        if xWallDist == 1:
                        #wall at right
                                if(getMaxValue(directions) == 3):
                                        global nextRight
                                        nextRight = directions[3]
                                        #print ('!!!!!!!!!', nextRight)
                                directions[3] = 0
                                #if directions[0] == directions[1]:
                                 #       directions[2] += directions[1]+5

                        elif xWallDist == -1:
                                if(getMaxValue(directions) == 2):
                                        global nextLeft
                                        nextLeft = directions[2]
                                directions[2] = 0
                                print ("left: 01")
                                #if directions[0] == directions[1]:
                                 #       directions[3] += directions[1]+5
                        elif xWallDist > 0:
                                directions[3] -= (50/xWallDist)
                        else:
                                directions[2] -= (50/abs(xWallDist))
                                print ("left: 0")
                if wall.x == player.x:
                        if yWallDist == 1:
                        #wall down side
                                if(getMaxValue(directions) == 1):
                                        global nextDown
                                        nextDown = directions[1]
                                directions[1] = 0
                                #if directions[2] == directions[3]:
                                 #       directions[0] += directions[2]+5
                        elif yWallDist == -1:
                                if(getMaxValue(directions) == 0):
                                        global nextUp
                                        nextUp = directions[0]
                                directions[0] = 0
                                #if directions[2] == directions[3]:
                                 #       directions[1] += directions[2]+5
                        elif yWallDist > 0:
                                directions[1] -= (50/yWallDist)
                        else:
                                directions[0] -= (50/abs(yWallDist))

class PathNode(GameObject):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.g = 0
		self.f = 0 # f = h + g
def getAllObstacles():
	pass # bullet and wall and laser

def getNeighbours():
	pass

class PlayerAI:
        def __init__(self):
	# Initialize any objects or variables you need here.
                pass

        def get_move(self, gameboard, player, opponent):
                # Write your AI here.


                #print (pX, pY, oX, oY)
                #for powerUp in powerUps:
                directions = getPowerPoints(gameboard, player)
                dodgepoints = getDodgePoints(gameboard, player)
                #print (dodgepoints)
                for i in range(4):
                        directions[i] += dodgepoints[i] * 2

                #print ('!!!!!', nextRight)
                #if(nextRight != 0):
                        #print('before', directions[3])
                directions[0] += nextUp
                directions[1] += nextDown
                directions[2] += nextLeft
                directions[3] += nextRight
                #if(nextRight != 0):
                       # print('after', directions[3])

                global nextCount
                nextCount += 1

                if(nextCount >= 2):
                        global nextUp
                        global nextDown
                        global nextRight
                        global nextLeft
                        nextUp, nextDown, nextLeft, nextRight = 0, 0, 0, 0
                        nextCount = 0

                checkWall(gameboard, player, opponent, directions)
                dodgeBullet(gameboard, player, directions)
                dodgeExploding(gameboard, player, directions)




                print(directions)
                direction = 0;
                for i in range(1,4):
                        if directions[i] > directions[direction]:
                                direction = i

                #print ("gameboard!", gameboard.power_ups[0].x, gameboard.power_ups[0].y)


                directionName = {
                        0: Direction.UP,
                        1: Direction.DOWN,
                        2: Direction.LEFT,
                        3: Direction.RIGHT,
                }[direction]
                #print (directionName)

                if player.direction == directionName:
                        return Move.FORWARD
                elif direction == 0:
                        return Move.FACE_UP
                elif direction == 1:
                        return Move.FACE_DOWN
                elif direction == 2:
                        return Move.FACE_LEFT
                elif direction == 3:
                        return Move.FACE_RIGHT

