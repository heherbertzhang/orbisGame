from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *

import random

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
                        horiScore = 100 /xDist
                vertiScore = 0
                if yDist != 0:
                        vertiScore = 100 /yDist

                xratio = 0.5 * vertiScore
                yratio = 0.5 * horiScore

                if xDist < 0:
                        right = -(horiScore)
                        left = 100 / (gameboard.width - absXdist)
                elif xDist > 0:
                        left = horiScore
                        right = 100 / (gameboard.width - absXdist)
                left += xratio
                right += xratio
                #only keep one side's score
                if(right > left):
                        left = left/2
                else:
                        right = right/2

                if yDist < 0:
                        down = -(vertiScore)
                        up = 100 / (gameboard.height - absYdist)
                elif yDist > 0:
                        up = vertiScore
                        down = 100/(gameboard.height - absYdist)
                if(up > down):
                        down = down/2
                else:
                        up = up/2
                up += yratio
                down += yratio
                rightTotal += right
                leftTotal += left
                upTotal += up
                downTotal += down

                if player.direction == Direction.UP:
                        upTotal += 10
                elif player.direction == Direction.DOWN:
                        downTotal += 10
                elif player.direction == Direction.LEFT:
                        leftTotal += 10
                elif player.direction == Direction.RIGHT:
                        rightTotal += 10

        #tune down the total mark to be within range 100
        
        rightTotal = rightTotal / maxScore * 100
        leftTotal = leftTotal / maxScore * 100
        upTotal = upTotal / maxScore * 100
        downTotal = downTotal / maxScore * 100

        return [upTotal, downTotal, leftTotal, rightTotal]

def getMorePowerPoint(gameboard, player, directions):
        powerUps = gameboard.power_ups
        for powerUp in powerUps:
                if(powerUp.x == player.x):
                        ydist = powerUp.y - player.y
                        if ydist > 0:
                                directions[1] += 25/ydist
                        elif ydist < 0:
                                directions[0] -= 25/ydist
                if(powerUp.y == player.y):
                        xdist = powerUp.x - player.x
                        if xdist > 0:
                                directions[3] += 25/xdist
                        elif xdist < 0:
                                directions[2] -= 25/xdist


def calculateRightThreatScore(xDist, playerDirect, gameboardwidth):
        #bullet at the travel from right to left
        #bullet at the right side
        if xDist == 0:
                left = 0
                right = 0
        elif xDist < 0:
                absXdist = abs(xDist)
                if playerDirect == Direction.RIGHT:
                        if absXdist > 1:
                                right = 100/(absXdist - 1)#need one turn to turn away
                        else:
                                right = 100
                else:
                        if absXdist > 2:
                                right = 100/(absXdist - 2)# need one more turn to turn right and then turn away
                        else:
                                right = 100
                if playerDirect != Direction.LEFT:
                #turn to left can cause bullet hit if too close
                        left = 100/(absXdist)
                else:#player face left
                        left = 100/(absXdist + 1) + 5 #not that good so + 5
        elif xDist > 0:
                #bullet at the left side
                absXdist = gameboardwidth - xDist
                if playerDirect == Direction.RIGHT:
                        if absXdist > 1:
                                right = 100/(absXdist - 1)#need one turn to turn away
                        else:
                                right = 100
                else:
                        if absXdist > 2:
                                right = 100/(absXdist - 2)# need one more turn to turn right and then turn away
                        else:
                                right = 100
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
        if(maxScore == 0):
                return [0, 0, 0, 0]
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
                if (bullets == None or bullet == None):
                        break
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
def converDirectionToNum(directionName):
        return {
                        Direction.UP: 0,
                        Direction.DOWN: 1,
                        Direction.LEFT: 2,
                        Direction.RIGHT: 3
                }[directionName]
def convertNumToDirect(num):
        return {
                        0:Direction.UP,
                        1:Direction.DOWN,
                        2:Direction.LEFT,
                        3:Direction.RIGHT
                }[num]
def dodgeBullet(gameboard, player, directions):
        bullets = gameboard.bullets
        danger = False
        for bullet in bullets:
                if bullet.y == player.y:
                        xdist = bullet.x - player.x
                        if(bullet.direction == Direction.RIGHT):
                                if(xdist < 0 and abs(xdist) < 3):
                                        directions[2] -= 100
                                        danger = True
                                        print('avoid bullet8!!!!!!!!!!!', directions[2])
                                elif xdist > 0 and (gameboard.width - abs(xdist))<3:
                                        directions[2] -= 100
                                        danger = True
                                        print('avoid bullet7!!!!!!!!!!!', directions[2])
                        if(bullet.direction ==Direction.LEFT):
                                if xdist > 0 and xdist < 3:
                                        directions[3] -= 100
                                        danger = True
                                        print('avoid bullet6!!!!!!!!!!!', directions[3])
                                elif xdist < 0 and (gameboard.width - abs(xdist)) < 3:
                                        directions[3] -= 100
                                        danger = True
                                        print('avoid bullet5!!!!!!!!!!!', directions[3])
                print("bulletx", bullet.x, player.x)
                lessDanger, right = False, False
                xdist = bullet.x - player.x
                if abs(xdist) < 2:
                        lessDanger = True
                        if(xdist > 0):
                                right = True
                if bullet.x == player.x or lessDanger:
                        ydist = bullet.y - player.y
                        if bullet.direction == Direction.UP:
                                if ydist > 0 and ydist < 3:
                                        #go up, bullet down
                                        if(lessDanger):
                                                if right:
                                                        directions[3] -= 80
                                                else:
                                                        directions[2] -= 80
                                        else:
                                                directions[1] -= 100
                                                danger = True
                                        print ("player y", player.y, bullet.y)
                                        print('avoid bullet!!!!!!!!!!!', directions[1])
                                elif ydist < 0 and (gameboard.width - abs(ydist)) < 3:
                                        if(lessDanger):
                                                if right:
                                                        directions[3] -= 80
                                                else:
                                                        directions[2] -= 80
                                        else:
                                                directions[1] -= 100
                                                danger = True
                                
                                        print('avoid bullet2!!!!!!!!!!!', directions[1])
                        if bullet.direction == Direction.DOWN:
                                if ydist > 0 and (gameboard.width - ydist) < 3:
                                        #go down, down
                                        if(lessDanger):
                                                if right:
                                                        directions[3] -= 80
                                                else:
                                                        directions[2] -= 80
                                        else:
                                                directions[0] -= 100
                                                danger = True
                                        print('avoid bullet3!!!!!!!!!!!', directions[0])
                                elif ydist < 0 and abs(ydist) < 3:
                                        if(lessDanger):
                                                if right:
                                                        directions[3] -= 80
                                                else:
                                                        directions[2] -= 80
                                        else:
                                                directions[0] -= 100
                                                danger = True
                                        print('avoid bullet4!!!!!!!!!!!', directions[0])
        if danger:
                direct = converDirectionToNum(player.direction)
                directions[direct] += 20
def getOppositeDirec(direct):
        return {
                        0:1,
                        1:0,
                        2:3,
                        3:2
                }[direct]

def avoidFaceOppo(opponent, player, directions):
        currentDirect = getMaxValue(directions)
        if(opponent.x == player.x):
                if currentDirect < 2:
                        if opponent.direction == convertNumToDirect(getOppositeDirec(currentDirect)):
                                dist = abs(opponent.y - player.y)        
                                directions[currentDirect] -= 100/dist
        if(opponent.y == player.y):
                if currentDirect > 1:
                        if opponent.direction == convertNumToDirect(getOppositeDirec(currentDirect)):
                                dist = abs(opponent.x - player.x)        
                                directions[currentDirect] -= 100/dist

def dodgeExploding(gameboard, player, directions):
        unsafey ={};
        unsafex ={};
        
        for i in gameboard.turrets:
                
                if (i.is_firing_next_turn  == True or i.cooldown_time <3):
                    unsafex[i.x] = 1
                    unsafey[i.y] =1

        if (player.x -1>=0):
                if (player.x -1) in unsafex:
                        directions[2] -= 100
                      
        else:
                if(gameboard.width -1) in unsafex:
                        directions[2] -= 100
                        print ("FUCK")
        if (player.x+1 < gameboard.width):
                if (player.x+1) in unsafex:
                        directions[3]-=100

        else:
                if(0) in unsafex:
                        directions[3] -= 100
                        print ("SEX")

        if (player.y+1 < gameboard.height):
                if (player.y+1) in unsafey:
                        directions[1]-=100
        else:
                if (0) in unsafey:
                        directions[1]-=100
                        print ("BITCH")

        if (player.y-1 >= 0):
                if (player.y-1) in unsafey:
                        directions[0]-=100
        else:
                if (gameboard.height-1) in unsafey:
                        directions[0]-=100
                        print ("hate")
                        
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
        turrets = gameboard.turrets
        walls.append(opponent)
        walls = walls + turrets
        #walls = walls + gameboard.bullets
        for wall in walls:
                xWallDist = wall.x - player.x
                yWallDist = wall.y - player.y
                if wall.y == player.y:
                        if xWallDist == 1 or (player.x in [0, gameboard.width-1] and xWallDist == -(gameboard.width - 1)):
                        #wall at right
                                if(getMaxValue(directions) == 3):
                                        global nextRight 
                                        nextRight = directions[3]
                                        print ('!!!!!!!!!', nextRight)
                                directions[3] = 0
                                #if directions[0] == directions[1]:
                                 #       directions[2] += directions[1]+5

                        elif xWallDist == -1 or (player.x in [0, gameboard.width-1] and xWallDist == (gameboard.width - 1)):
                                if(getMaxValue(directions) == 2):
                                        global nextLeft 
                                        nextLeft = directions[2]
                                directions[2] = 0
                                #if directions[0] == directions[1]:
                                 #       directions[3] += directions[1]+5
                        elif xWallDist > 0:
                                directions[3] -= (100/xWallDist/len(walls))
                        else:
                                directions[2] -= (100/abs(xWallDist)/len(walls))
                if wall.x == player.x:
                        if yWallDist == 1 or (player.y in [0, gameboard.height-1] and yWallDist == -(gameboard.height - 1)):
                        #wall down side
                                if(getMaxValue(directions) == 1):
                                        global nextDown
                                        nextDown = directions[1]
                                directions[1] = 0
                                #if directions[2] == directions[3]:
                                 #       directions[0] += directions[2]+5
                        elif yWallDist == -1 or (player.y in [0, gameboard.height-1] and yWallDist == (gameboard.height - 1)):
                                if(getMaxValue(directions) == 0):
                                        global nextUp
                                        nextUp = directions[0]
                                directions[0] = 0
                                #if directions[2] == directions[3]:
                                 #       directions[1] += directions[2]+5
                        elif yWallDist > 0:
                                directions[1] -= (50/yWallDist/len(walls))
                        else:
                                directions[0] -= (50/abs(yWallDist)/len(walls))


def escape(gameboard, player,opponent, predictions):
    

    # 0 for  nothing meaningful, 1 for shiled activate, 2 for teleport

    #detect if the plane is surrouended with bullets
    #consdier the bullet go over the board

    unsafex ={}
    unsafey ={}
    left =0
    right=0
    up=0
    down =0
    count = 4
    for k in predictions:
            if k<=0:
                    count -= 1
    if count == 0:
            if player.shield_count != 0:
                    return 1
            elif player.teleport_count !=0:
                    return 2
            else:
                    return 0
            
                
    for i in gameboard.bullets:
        if i.x == player.x +1 and i.y== player.y:
                right = 1
        if i.x == player.x -1 and i.y== player.y:
                left = 1
        if i.x == player.x  and i.y== player.y+1:
                up = 1
        if i.x == player.x  and i.y== player.y-1:
                down =1

   


    if (left ==1 and right==1 and up == 1 and down ==1):
        if player.shield_count != 0:
            return 1
        elif player.teleport_count !=0:
            return 2
        else:
            return 0
def facing_direction(player, opponent):
    
    #check if the guy is facing the direction the oppoenent
    #1 for yes, 0 for no, 3 for there is wall between
    if opponent.y == player.y:
        if opponent.x > player.x:
            print(player.direction)
            if player.direction == Direction.RIGHT:
                return 1
      
            else:
                return 0
                
        else:
  
            if player.direction == Direction.LEFT:
                return 1
            else:
                return 0
            
            
            
    elif opponent.x == player.x:
        if opponent.y>player.y:
            if player.direction ==Direction.DOWN:
                return 1
            else:
                return 0
        else:
            if player.direction == Direction.UP:
                return 1
            else:
                return 0

def attack(gameboard, player, opponent):
    # 1 for attack, 0 for non-attack
    a = facing_direction(player, opponent)
    if a == 1:
        return 1
    else:
        return 0

def walkable(gameboard, player, directions):
        dictionX = {}
        dictionY = {}
        walls = gameboard.walls
        for wall in walls:
                dictionX[wall.x] = wall.y
                dictionY[wall.y] = wall.x


class PlayerAI:
        def __init__(self):
	# Initialize any objects or variables you need here.
                pass

        def get_move(self, gameboard, player, opponent):
                # Write your AI here.
                

                #print (pX, pY, oX, oY)
                #for powerUp in powerUps:
                directions = getPowerPoints(gameboard, player)
                if directions == [0, 0, 0, 0]:
                        print ("no points!!!!!!!!!!!")
                        directions = [80, 80, 80, 80]
                dodgepoints = getDodgePoints(gameboard, player) 
                print (dodgepoints)
                for i in range(4):
                        directions[i] += dodgepoints[i] * 2
                if directions == [80, 80, 80, 80]:
                        #choose random direction
                        direct = random.randint(0, 3)
                        directions[direct] += 10
        

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

                getMorePowerPoint(gameboard, player, directions)
                checkWall(gameboard, player, opponent, directions)
                dodgeBullet(gameboard, player, directions)
                dodgeExploding(gameboard, player, directions)
                avoidFaceOppo(opponent, player, directions)

                toAttck = True
                if attack(gameboard, player, opponent):
                        for d in directions:
                                if d < 5:
                                        toAttck = False
                        if toAttck:
                                return Move.SHOOT



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
                print (directionName)

                r = escape(gameboard, player,opponent, directions)
                if r == 1:
                        return Move.SHIELD

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

