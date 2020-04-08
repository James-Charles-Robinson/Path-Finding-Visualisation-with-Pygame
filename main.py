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

        self.coords.maze = [[0 for x in range(self.gridSize)] for x in range(self.gridSize)]
        
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.width))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("A* Algorithm - James Robinson")

    def main(self):
        
        self.clock.tick(self.fps)

        self.mouseX, self.mouseY = pygame.mouse.get_pos()

        # gets key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                
                self.keyPressed(event.key)
            else:
                self.mousePressed(event)

        if self.placingWalls == True:
            self.placeWall()
        elif self.removingWalls == True:
            self.removeWall()


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
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls:
            self.coords.start = coords
        
    def placeEnd(self):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls:
            self.coords.end = coords

    def placeWall(self):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls:
            self.coords.walls.append(coords)

    def removeWall(self):
        if self.getBoxCoords() in self.coords.walls:
            self.coords.walls.remove(self.getBoxCoords())

    def mousePressed(self, event):
  
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.placingWalls = True
            elif event.button == 3:
                self.removingWalls = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.placingWalls = False
            elif event.button == 3:
                self.removingWalls = False
    
    def keyPressed(self, key):
        if key == 115: # s key
            self.placeStart()
        elif key == 101: # e key
            self.placeEnd()
        elif key == 13: # enter
            self.runAlgorithm()
        elif key == 99: # c
            self.coords.removeAll()
        elif key == 114: # r
            self.coords.removeLast()

        else:
            print(key)

    def pygameWait(self):
        self.clock.tick(self.fps)
        pygame.event.get()
        self.redraw()
        pygame.display.update()

    def runAlgorithm(self):
        coords.removeLast()
        if self.coords.start != None and self.coords.end != None:
            self.coords.createMaze(gui)
            self.coords.finalPath = astar(self.coords.maze, coords.start, coords.end, self, self.coords)
            if self.coords.finalPath == None:
                self.coords.finalPath = []

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


    def removeLast(self):
        self.maze = []
        self.openList = []
        self.closedList = []
        self.finalPath = []

    def createMaze(self, giu):
        self.maze = [[0 for x in range(gui.gridSize)] for x in range(gui.gridSize)]
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

        if count % 3 == 0:

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
            gui.pygameWait()

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
