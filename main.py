import pygame
import random

# class for the gui of the application
class Gui():

    def __init__(self, coords):
        # gui variables
        self.fps = 60
        self.width = 800
        self.gridSize = 20
        self.boxWidth = self.width/self.gridSize
        self.coords = coords
        self.placingWalls = False
        self.removingWalls = False
        self.animationSpeed = 10

        self.coords.maze = [[0 for x in range(self.gridSize)] for x in range(self.gridSize)]

        # start pygame application
        pygame.init()
        self.win = pygame.display.set_mode((self.width, self.width))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pathfinding Algorithms - James Robinson")

    # main function for gui
    def main(self, running=False):
        
        self.clock.tick(self.fps)

        self.mouseX, self.mouseY = pygame.mouse.get_pos()
                
        # if the mouse button was pressed down continue placing walls
        if self.placingWalls == True and running == False:
            self.placeWall()
        elif self.removingWalls == True and running == False:
            self.remove()

        # get mouse and key presses
        self.eventHandle(running)

        # redraw and update the display
        self.redraw()
        pygame.display.update()
        

    # handles key and mouse presses
    def eventHandle(self, running):

        # gets key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # key presses
            elif event.type == pygame.KEYDOWN:
                
                key = event.key

                # run algorithm 
                if key == 113 or key == 119 or key == 101 or key == 114 and running == False: # q, w, e and r
                    self.runAlgorithm(key)              
                
                # clear the whole board
                elif key == 120 and running == False: # x
                    self.coords.removeAll()
                    
                # remove everything except the things placed by the user
                elif key == 122 and running == False: # z
                    self.coords.removeLast()
                    
                # place checkpoints with number keys
                elif (key > 48 and key < 58) and running == False: # 1-9
                    self.placeCheckPoint(key-48)

                # increase speed of the pathfinding
                elif key == 61 and self.animationSpeed > 0: # + key
                    if self.animationSpeed <= 2:
                        self.animationSpeed = 1
                    else:
                        self.animationSpeed = int(self.animationSpeed * 0.5) + 1

                # decrease speed of pathfinding
                elif key == 45: # - key
                    self.animationSpeed = int(self.animationSpeed * 2) + 1

                elif key == 32: # space
                    self.coords.generateRandomMaze(gui)


            # mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # place walls
                if event.button == 1 and running == False: # left down
                    self.placingWalls = True

                # remove walls
                elif event.button == 3 and running == False: # right down
                    self.removingWalls = True

                # zoom in
                if event.button == 4: # scroll up
                    self.gridSize -= 1
                    self.boxWidth = self.width/self.gridSize

                # zoom out
                elif event.button == 5: # scroll down
                    self.gridSize += 1
                    self.boxWidth = self.width/self.gridSize

            # mouse button up
            elif event.type == pygame.MOUSEBUTTONUP:

                # stop placing walls
                if event.button == 1: # left up
                    self.placingWalls = False

                # stop removing walls
                elif event.button == 3: # right up
                    self.removingWalls = False

    # redraws the gui
    def redraw(self):

        self.win.fill((255,255,255))
        self.drawPoints()
        self.drawGrid()

    # draw the grid lines
    def drawGrid(self):
        for i in range(self.gridSize-1):
            pygame.draw.rect(self.win, (0, 0, 0), (((i+1)*self.boxWidth)-2, 0, 4, self.width))
            pygame.draw.rect(self.win, (0, 0, 0), (0, ((i+1)*self.boxWidth)-2, self.width, 4))

    # draws all the squares for the walls, checkpoints ect
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
            
    # gets the center point of a node
    def boxCenter(self, box):
        boxX, boxY = box
        center = ((boxX*self.boxWidth+(self.boxWidth/2)), (boxY*self.boxWidth+(self.boxWidth/2)))
        return center

    # used to draw the boxed given colours and position
    def drawBox(self, box, colour):
        boxX, boxY = box
        pygame.draw.rect(self.win, colour,
                        (boxX*self.boxWidth, boxY*self.boxWidth, self.boxWidth, self.boxWidth))

    # gets the box coordinates given a mouse position
    def getBoxCoords(self):
        boxX = int((self.mouseX + 2) / self.boxWidth)
        boxY = int((self.mouseY + 2) / self.boxWidth)
        return (boxX, boxY)

    # placing checkpoints
    def placeCheckPoint(self, index):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls and coords not in self.coords.checkPoints:
            while len(self.coords.checkPoints) <= index-1:
                self.coords.checkPoints.append("None")
            self.coords.checkPoints[index-1] = coords
    
    # placing walls
    def placeWall(self):
        coords = self.getBoxCoords()
        if coords != self.coords.start and coords != self.coords.end and coords not in self.coords.walls and coords not in self.coords.checkPoints:
            self.coords.walls.append(coords)

    # removing nodes such as walls checkpoints ect
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

    # function that prepares for a pathfind and runs pathfind function
    def runAlgorithm(self, key):
        self.placingWalls == False
        self.removingWalls == False
        coords.removeLast()

        # if we have 2 or more checkpoints
        if len(self.coords.checkPoints) > 1:

            # create the maze array and remove missed checkpoint numbers
            self.coords.createMaze(gui)
            checkPoints = self.coords.checkPoints[:]
            checkPoints = [point for point in checkPoints if point != "None"]

            # iterate through every checkpoint and pathfind to it
            for i,point in enumerate(checkPoints):
                if i != len(checkPoints)-1:
                    
                    start = point
                    end = checkPoints[i+1]

                    newPath = pathfind(self.coords.maze, start, end, self, self.coords, key)
                    if newPath == None:
                        newPath = []
                        
                    self.coords.finalPath.extend(newPath)


    # displays text given text, colour and position/size
    def displayText(self, txt, colour, center, size):
        font = pygame.font.Font(None, size)
        textSurf = font.render(txt, True, colour)
        textRect = textSurf.get_rect()
        textRect.center = (center)
        self.win.blit(textSurf, textRect)


# class containing all coordinates and functions for calculations todo with them 
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

    # gets the furthest distance of a node from the (0, 0)
    def largestDistance(self):
        largest = 0
        for wall in self.walls:
            if wall[0] > largest: largest = wall[0]
            if wall[1] > largest: largest = wall[1]
        for point in self.checkPoints:
            if point[0] > largest: largest = point[0]
            if point[1] > largest: largest = point[1]
        return largest + 1

    # creates a 2d array of the maze and its walls
    def createMaze(self, giu):
        
        largestDistance = self.largestDistance()
        
        # makes sure the size of the maze if either the size of the gui
        # or the size of the maze made using the walls and checkpoints
        if gui.gridSize > largestDistance:
            largest = gui.gridSize
        else:
            largest = largestDistance
            
        self.maze = [[0 for x in range(largest)] for x in range(largest)]
        for wall in self.walls:
            try:
                wallX, wallY = wall
                self.maze[wallX][wallY] = 1
            except:
                pass

    # creates a random maze
    def generateRandomMaze(self, gui):
        self.walls = []
        for i in range(gui.gridSize*gui.gridSize):
            if random.random() > 0.6:
                wall = (random.randint(0, gui.gridSize-1), random.randint(0, gui.gridSize-1))
                if wall not in self.walls:
                    self.walls.append(wall)


# function for pathfinding using dfs, bfs, dijkstra and astar
# Returns a list of tuples as a path from the given start to the given end in the given maze
def pathfind(maze, start, end, gui, coords, key):
    
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

    count = 0

    # Loop until you find the end
    while len(openList) > 0:

        # skip pathfinding to create a wait effect. Ajustable speed
        if count >= gui.animationSpeed:

            count = 0

            # Get the current node
            
            if key == 113: # dfs, get the latest node
                currentNode = openList[-1]
                currentIndex = len(openList)-1
                
            elif key == 119: # bfs, get the newest node
                currentNode = openList[0]
                currentIndex = 0               
                
            elif key == 114: # a*, get the node with the lowest f value
                currentNode = openList[0]
                currentIndex = 0
                for index, item in enumerate(openList):
                    if item.f < currentNode.f:
                        currentNode = item
                        currentIndex = index
                        
            elif key == 101: # dijkstra, get the node with the lowest g value
                currentNode = openList[0]
                currentIndex = 0
                for index, item in enumerate(openList):
                    if item.g < currentNode.g:
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
            # left, down, right, up. Which makes dfs go in up, right, down, left order
            for newPosition in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # Adjacent squares

                # Get node position
                nodePosition = (currentNode.position[0] + newPosition[0], currentNode.position[1] + newPosition[1])

                # Make sure within range
                if nodePosition[0] > (len(maze) - 1) or nodePosition[0] < 0 or nodePosition[1] > (len(maze[len(maze)-1]) -1) or nodePosition[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[nodePosition[0]][nodePosition[1]] != 0:
                    continue

                if Node(currentNode, nodePosition) in closedList:
                    continue

                # Create new node
                child = Node(currentNode, nodePosition)

                # Child is on the closed list
                passList = [False for closedChild in closedList if child == closedChild]
                if False in passList:
                    continue

                # for dfs and bfs we dont add anything to the node values
                
                if key == 101: # dijkstra, add one to g value
                    child.g = currentNode.g + 1
                    
                elif key == 114: # a*, calculate f value
                    child.g = currentNode.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because it makes it prioritse diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better
                    child.h = ((abs(child.position[0] - endNode.position[0]) ** 2) + (abs(child.position[1] - endNode.position[1]) ** 2)) ** 0.6
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

        # if skipped just update the gui
        else:

            coords.openList = openList
            coords.closedList = closedList
            gui.main(True)

        count += 1





# node class for containing position, parent and costs
class Node():
    def __init__(self, parent, position):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# main loop
if __name__ == "__main__":
    coords = CoOrdinates()
    gui = Gui(coords)
    while True:
        gui.main()
