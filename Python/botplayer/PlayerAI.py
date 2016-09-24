from PythonClientAPI.libs.Game.Enums import *
from PythonClientAPI.libs.Game.MapOutOfBoundsException import *
import heapq
import math

class Cell(object):
    def __init__(self, x, y, reachable):
        """Initialize new cell.
        @param reachable is cell reachable? not a wall?
        @param x cell x coordinate
        @param y cell y coordinate
        @param g cost to move from the starting cell to this cell.
        @param h estimation of the cost to move from this cell
                 to the ending cell.
        @param f f = g + h
        """
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
def directionalAdder(direction, obj, value):
    '''
    return a + b in direction
    '''
    directAdder = {Direction.UP: lambda a: a.y += value, \
        Direction.DOWN:lambda a: a.y -= value, \
        Direction.LEFT:lambda a: a.x -= value, \
        Direction.RIGHT:lambda a: a.x += value}
    directAdder[direction](obj)
    return obj
    
def isDangerZone(gameBoard, g, cell):
    #dangerMap = {}
    for bullet in gameBoard.bullets:
        dloc =directionalAdder(direction, bullet.copy(), g)
        if dloc.x == cell.x and dloc.y == cell.y:
            return True
        #dangerMap[(dloc.x, dloc.y)] = 1

    for turret in gameBoard.turrets:
        if turret.is_dead:
            continue
        if turret.is_firing_next_turn:
            mod = turret.fire_time + turret.cooldown_time
            result = g % mod
            if result >= 1 and result <= turret.fire_time:
                if isInTurretRange(): return True
        else:
            if isInTurretRange(): return True
    return False
def isInTurretRange():
    # assume in danger
    # find wall that stop the fire
    if cell.x != turret.x and cell.y != turret.y:
        return False
    for wall in gameBoard.walls:
        if cell.y == turret.y:
            if wall.x < cell.x and wall.x > turret.x:
            # fine for now
                pass
            elif wall.x > cell.x and wall.x < turret.x:
                pass
            else:
                return True
        if cell.x == turret.x:
            if wall.y < cell.y and wall.y > turret.y:
            # fine for now
                pass
            elif wall.y > cell.y and wall.y < turret.y:
                pass
            else:
                return True
     return False
            

class AStar(object):
    def __init__(self):
        # open list
        self.opened = []
        heapq.heapify(self.opened)
        # visited cells list
        self.closed = set()
        # grid cells
        self.cells = []
        self.grid_height = None
        self.grid_width = None

    def init_grid(self, width, height, walls, start, end):
        """Prepare grid cells, walls.
        @param width grid's width.
        @param height grid's height.
        @param walls list of wall x,y tuples.
        @param start grid starting point x,y tuple.
        @param end grid ending point x,y tuple.
        """
        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))
        self.start = self.get_cell(*start)
        self.end = self.get_cell(*end)

    def get_heuristic(self, cell):
        """Compute the heuristic value H for a cell.
        Distance between this cell and the ending cell multiply by 10.
        @returns heuristic value H
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_cell(self, x, y):
        """Returns a cell from the cells list.
        @param x cell x coordinate
        @param y cell y coordinate
        @returns cell
        """
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        """Returns adjacent cells to a cell.
        Clockwise starting from the one on the right.
        @param cell get adjacent cells for this cell
        @returns adjacent cells list.
        """
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self):
        cell = self.end
        path = [(cell.x, cell.y)]
        while cell.parent is not self.start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell):
        """Update adjacent cell.
        @param adj adjacent cell to current cell
        @param cell current cell being processed
        """
        adj.g = cell.g + 10
        adj.h = self.get_heuristic(adj)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def solve(self):
        """Solve maze, find path to ending cell.
        @returns path or None if not found.
        """
        try:
            # add starting cell to open heap queue
            heapq.heappush(self.opened, (self.start.f, self.start))
            F_Value ={}
            while len(self.opened):
                # pop cell from heap queue
                (f, cell) = heapq.heappop(self.opened)
                # add cell to closed list so we don't process it twice
                self.closed.add(cell)
                # if ending cell, return found path
                if cell is self.end:
                    return self.get_path()
                # get adjacent cells for cell
                adj_cells = self.get_adjacent_cells(cell)
                for adj_cell in adj_cells:
                    if adj_cell.reachable and adj_cell not in self.closed \
                            and not isDangerZone(gameboard, (cell.g+10)/10, adj_cell):
                        if (adj_cell.f, adj_cell) in self.opened:
                            # if adj cell in open list, check if current path is
                            # better than the one previously found
                            # for this adj cell.
                            if adj_cell.g > cell.g + 10:
                                self.update_cell(adj_cell, cell)
                        else:
                            self.update_cell(adj_cell, cell)
                            # add adj cell to open list
                            if  len(self.opened) == 0:
                                heapq.heappush(self.opened, (adj_cell.f, adj_cell))
                                F_Value[adj_cell.f] = adj_cell.f
                            elif adj_cell.f in F_Value:
                                F_Value[adj_cell.f] = F_Value[adj_cell.f] + 0.01
                                heapq.heappush(self.opened, (F_Value[adj_cell.f] + 0.01, adj_cell))
                            else:
                                heapq.heappush(self.opened, (adj_cell.f, adj_cell))
                                F_Value[adj_cell.f] = adj_cell.f
        except:
            print (self.opened)

class item:
        def __init__(self,itemPosition, playerPosition):
            self.itemPosition = itemPosition
            self.distance = 10 * (abs(itemPosition[0] - playerPosition[0]) + abs(itemPosition[1] - playerPosition[1]))


def getDangers():
    gameboard.
class PlayerAI:
        def __init__(self):
            # Initialize any objects or variables you need here.
            self.searchObject = AStar()
            self.firstTime = True

        def get_move(self, gameboard, player, opponent):
            # Write your AI here.
            if (self.firstTime == True):
                wallPositionList =[]
                for wall in gameboard.walls:
                    wallPositionList.append((wall.x,wall.y))
                for turret in gameboard.turrets:
                    wallPositionList.append((turret.x,turret.y))

                self.searchObject.init_grid(gameboard.width, gameboard.height,wallPositionList,(0,0),(gameboard.width-1,gameboard.height-1))
                self.firstTime = False


            itemPositionList =[]
            for power_up in gameboard.power_ups:
                itemObject = item((power_up.x,power_up.y), (player.x,player.y))
                itemPositionList.append(itemObject)
            itemPositionList.sort(key=lambda item:item.distance)

            self.searchObject.start = self.searchObject.get_cell(player.x,player.y)
            self.searchObject.end = self.searchObject.get_cell(itemPositionList[0].itemPosition[0], itemPositionList[0].itemPosition[1])
            self.searchObject.solve();
            path = self.searchObject.get_path()
            nextDestination = path[1]
            x_difference = nextDestination[0] - player.x
            y_difference = nextDestination[1] - player.y
            if (x_difference == 1):
                if (player.direction == Direction.RIGHT):
                    return Move.FORWARD
                else:
                    return Move.FACE_RIGHT
            elif(x_difference == -1):
                if (player.direction == Direction.LEFT):
                    return Move.FORWARD
                else:
                    return Move.FACE_LEFT
            elif(y_difference == 1):
                if (player.direction == Direction.DOWN):
                    return Move.FORWARD
                else:
                    return Move.FACE_DOWN
            elif(y_difference == -1):
                if (player.direction == Direction.UP):
                    return Move.FORWARD
                else:
                    return Move.FACE_UP
            else:
                return




