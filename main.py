import pygame
import random
import math
import time

class Gui():

    def __init__(self, coords):
        self.fps = 60
        self.width = 800
        self.gridSize = 20
        self.boxWidth = self.width/self.gridSize
        self.coords = coords
        self.placingWalls = False
        self.removingWalls = False
        self.animationSpeed = 3

        self.coords.maze = [[0 for x in range(self.gridSize)] for x in range(self.gridSize)]
        
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.width))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("A* Algorithm - James Robinson")

    def main(self, running=False):
        
        self.clock.tick(self.fps)

        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        # gets key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            elif event.type == pygame.KEYDOWN:
                
                key = event.key
                if key == 115 and running == False: # s key
                    self.placeStart()
                elif key == 101 and running == False: # e key
                    self.placeEnd()
                elif key == 13 and running == False: # enter
                    self.runAlgorithm()
                elif key == 99 and running == False: # c
                    self.coords.removeAll()
                elif key == 114 and running == False: # r
                    self.coords.removeLast()
                elif (key > 48 and key < 58) and running == False:
                    self.placeCheckPoint(key-48)
                elif key == 61 and self.animationSpeed > 0: # + key
                    self.animationSpeed -= 1
                    print(self.animationSpeed)
                elif key == 45: # - key
                    self.animationSpeed += 1
                else:
                    print(key)

      
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and running == False: # left down
                    self.placingWalls = True
                elif event.button == 3 and running == False: # right down
                    self.removingWalls = True

                if event.button == 4: # scroll up
                    self.gridSize -= 1
                    self.boxWidth = self.width/self.gridSize
                elif event.button == 5: # scroll down
                    self.gridSize += 1
                    self.boxWidth = self.width/self.gridSize

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left up
                    self.placingWalls = False
                elif event.button == 3: # right up
                    self.removingWalls = False

                    

        if self.placingWalls == True and running == False:
            self.placeWall()
        elif self.removingWalls == True and running == False:
            self.remove()


        self.redraw()
        pygame.display.update()
        
    def redraw(self):

        self.win.fill((255,255,255))
        self.drawPoints()
        self.drawGrid()
        
    def drawGrid(self):
        for i in range(self.gridSize-1):
            pygame.draw.rect(self.win, (0, 0, 0), (((i+1)*self.boxWidth)-2, 0, 4, self.width))
            pygame.draw.rect(self.win, (0, 0, 0), (0, ((i+1)*self.boxWidth)-2, self.width, 4))

    def drawPoints(self):


        for node in self.coords.openList:
            self.drawBox(node.position, (0, 255, 0))

        for node in self.coords.closedList:
            self.drawBox(node.position, (0, 0, 255))


        for wall in self.coords.finalPath:
            self.drawBox(wall, (255, 0, 255))

        for wall in self.coords.walls:
            self.drawBox(wall, (0, 0, 0))

        for i,point in enumerate(self.coords.checkPoints):
            if point != "None":
                self.drawBox(point, (255, 30, 30))
                self.displayText(str(i+1), (255, 255, 255), self.boxCenter(point), int(self.boxWidth))
        
        if self.coords.start != None:
            self.drawBox(self.coords.start, (255, 0, 0))
            self.displayText("S", (255, 255, 255), self.boxCenter(self.coords.start), int(self.boxWidth))

            
        if self.coords.end != None:
            self.drawBox(self.coords.end, (255, 0, 0))
            self.displayText("E", (255, 255, 255), self.boxCenter(self.coords.end), int(self.boxWidth))
            

    def boxCenter(self, box):
        boxX, boxY = box
        center = ((boxX*self.boxWidth+(self.boxWidth/2)), (boxY*self.boxWidth+(self.boxWidth/2)))
        return center

    def drawBox(self, box, colour):
        boxX, boxY = box
        pygame.draw.rect(self.win, colour,
                        (boxX*self.boxWidth, boxY*self.boxWidth, self.boxWidth, self.boxWidth))

    def getBoxCoords(self):
        boxX = int((self.mouseX + 2) / self.boxWidth)
        boxY = int((self.mouseY + 2) / self.boxWidth)
        return (boxX, boxY)

    def placeStart(self):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls and coords not in self.coords.checkPoints:
            self.coords.start = coords

    def placeCheckPoint(self, index):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls and coords not in self.coords.checkPoints:
            while len(self.coords.checkPoints) <= index-1:
                self.coords.checkPoints.append("None")
            self.coords.checkPoints[index-1] = coords
        
    def placeEnd(self):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls and coords not in self.coords.checkPoints:
            self.coords.end = coords

    def placeWall(self):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls and coords not in self.coords.checkPoints:
            self.coords.walls.append(coords)

    def remove(self):
        coords = self.getBoxCoords()
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)
        elif coords in self.coords.checkPoints:
            self.coords.checkPoints.remove(coords)
        elif coords == self.coords.start:
            self.coords.start = None
        elif coords == self.coords.end:
            self.coords.end = None


    def runAlgorithm(self):
        self.placingWalls == False
        self.removingWalls == False
        coords.removeLast()
        if self.coords.start != None and self.coords.end != None:
            
            self.coords.createMaze(gui)
            checkPoints = self.coords.checkPoints[:]
            checkPoints.append(self.coords.end)
            checkPoints.insert(0, self.coords.start)
            checkPoints = [point for point in checkPoints if point != "None"]
            
            for i,point in enumerate(checkPoints):
                if i != len(checkPoints)-1:
                    start = point
                    end = checkPoints[i+1]
                    newPath = astar(self.coords.maze, start, end, self, self.coords)
                    if newPath == None:
                        newPath = []
                    self.coords.finalPath.extend(newPath)


    def displayText(self, txt, colour, center, size):
        font = pygame.font.Font(None, size)
        textSurf = font.render(txt, True, colour)
        textRect = textSurf.get_rect()
        textRect.center = (center)
        self.win.blit(textSurf, textRect)
        
class CoOrdinates():
    def __init__(self):
        self.removeAll()

    def removeAll(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.openList = []
        self.closedList = []
        self.finalPath = []
        self.checkPoints = []


    def removeLast(self):
        self.maze = []
        self.openList = []
        self.closedList = []
        self.finalPath = []

    def largestDistance(self):
        largest = 0
        for wall in self.walls:
            if wall[0] > largest: largest = wall[0]
            if wall[1] > largest: largest = wall[1]
        for point in self.checkPoints:
            if point[0] > largest: largest = point[0]
            if point[1] > largest: largest = point[1]
        if self.start[0] > largest: largest = self.start[0]
        if self.start[1] > largest: largest = self.start[1]
        if self.end[0] > largest: largest = self.end[0]
        if self.end[1] > largest: largest = self.end[1]
        return largest + 1
        
    def createMaze(self, giu):
        largestDistance = self.largestDistance()
        if gui.gridSize > largestDistance:
            largest = gui.gridSize
        else:
            largest = largestDistance
        self.maze = [[0 for x in range(largest)] for x in range(largest)]
        for wall in self.walls:
            try:
                wallX, wallY = wall
                self.maze[wallY][wallX] = 1
            except:
                pass

def astar(maze, start, end, gui, coords):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    
    # Create start and end node
    startNode = Node(None, start)
    startNode.g = startNode.h = startNode.f = 0
    endNode = Node(None, end)
    endNode.g = endNode.h = endNode.f = 0

    # Initialize both open and closed list
    openList = []
    closedList = []

    # Add the start node
    openList.append(startNode)

    count = 1

    # Loop until you find the end
    while len(openList) > 0:

        if count % gui.animationSpeed == 0:

            # Get the current node
            currentNode = openList[0]
            currentIndex = 0
            for index, item in enumerate(openList):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index

            # Pop current off open list, add to closed list
            openList.pop(currentIndex)
            closedList.append(currentNode)

            # Found the goal
            if currentNode == endNode:
                path = []
                current = currentNode
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.openList = openList
                coords.closedList = closedList
                return path # Return path

            # Generate children
            children = []
            for newPosition in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares

                # Get node position
                nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])

                # Make sure within range
                if nodePosition[0] > (len(maze) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(maze[len(maze)-1]) -1) or nodePosition[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[nodePosition[1]][nodePosition[0]] != 0:
                    continue

                if Node(currentNode, nodePosition) in closedList:
                    continue

                # Create new node
                new_node = Node(currentNode, nodePosition)

                # Append
                children.append(new_node)

                # Loop through children
                for child in children:
                    # Child is on the closed list
                    for closedChild in closedList:
                        if child == closedChild:
                            break
                    else:
                        # Create the f, g, and h values
                        child.g = currentNode.g + 1
                        # H: Manhattan distance to end point
                        child.h = math.sqrt((abs(child.position[0] - endNode.position[0]) ** 2) + (abs(child.position[1] - endNode.position[1]) ** 2))
                        child.f = child.g + child.h

                        # Child is already in the open list
                        for openNode in openList:
                            # check if the new path to children is worst or equal 
                            # than one already in the openList (by measuring g)
                            if child == openNode and child.g >= openNode.g:
                                break
                        else:
                            # Add the child to the open list
                            openList.append(child)
        else:

            coords.openList = openList
            coords.closedList = closedList
            gui.main(True)

        count += 1


class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

coords = CoOrdinates()
gui = Gui(coords)
while True:

    t = time.time()
    gui.main()
