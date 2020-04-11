import pygame
import random


class Gui():
    '''
    Class for the gui of the application
    '''
    
    # gui constants
    FPS = 60
    WIDTH = 800
    
    def __init__(self, coords):

        # gui variables
        self.grid_size = 20
        self.box_width = self.WIDTH/self.grid_size
        self.coords = coords
        self.placing_walls = False
        self.removing_walls = False
        self.animation_speed = 10

        self.coords.maze = [
            [0 for x in range(self.grid_size)] for y in range(self.grid_size)]

        # start pygame application
        pygame.init()
        self.win = pygame.display.set_mode((self.WIDTH, self.WIDTH))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pathfinding Algorithms - James Robinson")

    # main function for gui
    def main(self, running=False):
        
        self.clock.tick(self.FPS)

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
                
        # if the mouse button was pressed down continue placing walls
        if not running:
            if self.placing_walls == True:
                self.place_wall()
            elif self.removing_walls == True:
                self.remove()

        # get mouse and key presses
        self.event_handle(running)

        # redraw and update the display
        self.redraw()
        pygame.display.update()
        

    # handles key and mouse presses
    def event_handle(self, running):

        run_keys = {"q", "w", "e", "r"}
        checkpoint_keys = {"1", "2", "3", "4", "5", "6", "7", "8", "9"}

        # gets key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # key presses
            elif event.type == pygame.KEYDOWN:
                
                key = chr(event.key)

                if running == False:

                    # run algorithm 
                    if key in run_keys: # q, w, e and r
                        self.run_algorithm(key)              
                    
                    # clear the whole board
                    elif key == "x":
                        self.coords.remove_all()
                        
                    # remove everything except the things placed by the user
                    elif key == "z":
                        self.coords.remove_last()
                        
                    # place checkpoints with number keys
                    elif key in checkpoint_keys: # 1-9
                        self.place_check_point(key)


                # increase speed of the pathfinding
                elif (key == "+" or key == "=") and self.animation_speed > 0:
                    if self.animation_speed <= 2:
                        self.animation_speed = 1
                    else:
                        self.animation_speed = int(self.animation_speed * 0.5) + 1

                # decrease speed of pathfinding
                elif key == "-":
                    self.animation_speed = int(self.animation_speed * 2) + 1

                elif key == " ":
                    self.coords.generate_random_maze(gui)

                else:
                    print(key)


            # mouse button down
            elif event.type == pygame.MOUSEBUTTONDOWN:

                if running == False:
                
                    # place walls
                    if event.button == 1: # left down
                        self.placing_walls = True

                    # remove walls
                    elif event.button == 3: # right down
                        self.removing_walls = True

                # zoom in
                if event.button == 4: # scroll up
                    self.grid_size -= 1
                    self.box_width = self.WIDTH/self.grid_size

                # zoom out
                elif event.button == 5: # scroll down
                    self.grid_size += 1
                    self.box_width = self.WIDTH/self.grid_size

            # mouse button up
            elif event.type == pygame.MOUSEBUTTONUP:

                # stop placing walls
                if event.button == 1: # left up
                    self.placing_walls = False

                # stop removing walls
                elif event.button == 3: # right up
                    self.removing_walls = False

    # redraws the gui
    def redraw(self):

        self.win.fill((255,255,255))
        self.draw_points()
        self.draw_grid()

    # draw the grid lines
    def draw_grid(self):
        for i in range(self.grid_size-1):
            pygame.draw.rect(self.win, (0, 0, 0),
                             (((i+1)*self.box_width)-2, 0, 4, self.WIDTH))
            pygame.draw.rect(self.win, (0, 0, 0),
                             (0,((i+1)*self.box_width)-2, self.WIDTH, 4))

    # draws all the squares for the walls, checkpoints ect
    def draw_points(self):


        for node in self.coords.open_list:
            self.draw_box(node.position, (0, 255, 0))

        for node in self.coords.closed_list:
            self.draw_box(node.position, (0, 0, 255))


        for wall in self.coords.final_path:
            self.draw_box(wall, (255, 0, 255))

        for wall in self.coords.walls:
            self.draw_box(wall, (0, 0, 0))

        for i,point in enumerate(self.coords.check_points):
            if point != "None":
                self.draw_box(point, (255, 30, 30))
                self.display_text(str(i+1), (255, 255, 255),
                                  self.box_center(point), int(self.box_width))
        
        if self.coords.start != None:
            self.draw_box(self.coords.start, (255, 0, 0))
            self.display_text("S", (255, 255, 255),
                              self.box_center(self.coords.start), int(self.box_width))

            
        if self.coords.end != None:
            self.draw_box(self.coords.end, (255, 0, 0))
            self.display_text("E", (255, 255, 255),
                              self.box_center(self.coords.end), int(self.box_width))

    
    # gets the center point of a node
    def box_center(self, box):
        boxX, boxY = box
        center = ((boxX*self.box_width+(self.box_width/2)),
                  (boxY*self.box_width+(self.box_width/2)))
        return center


    # used to draw the boxed given colours and position
    def draw_box(self, box, colour):
        boxX, boxY = box
        pygame.draw.rect(self.win, colour,
                        (boxX*self.box_width, boxY*self.box_width,
                         self.box_width, self.box_width))


    # gets the box coordinates given a mouse position
    def get_box_coords(self):
        boxX = int((self.mouse_x + 2) / self.box_width)
        boxY = int((self.mouse_y + 2) / self.box_width)
        return (boxX, boxY)


    # placing checkpoints
    def place_check_point(self, index):
        coords = self.get_box_coords()
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.walls and coords
                not in self.coords.check_points):
            
            while len(self.coords.check_points) <= int(index)-1:
                self.coords.check_points.append("None")
            self.coords.check_points[int(index)-1] = coords

    
    # placing walls
    def place_wall(self):
        coords = self.get_box_coords()
        if (coords != self.coords.start and coords != self.coords.end
                and coords not in self.coords.walls and coords
                not in self.coords.check_points):
            self.coords.walls.append(coords)


    # removing nodes such as walls checkpoints ect
    def remove(self):
        coords = self.get_box_coords()
        if coords in self.coords.walls:
            self.coords.walls.remove(coords)
        elif coords in self.coords.check_points:
            self.coords.check_points.remove(coords)
        elif coords == self.coords.start:
            self.coords.start = None
        elif coords == self.coords.end:
            self.coords.end = None


    # function that prepares for a pathfind and runs pathfind function
    def run_algorithm(self, key):
        self.placing_walls == False
        self.removing_walls == False
        self.coords.remove_last()

        # if we have 2 or more checkpoints
        if len(self.coords.check_points) > 1:

            # create the maze array and remove missed checkpoint numbers
            self.coords.create_maze(gui)
            check_points = self.coords.check_points[:]
            check_points = [point for point in check_points if point != "None"]

            # iterate through every checkpoint and pathfind to it
            for i,point in enumerate(check_points):
                if i != len(check_points)-1:
                    
                    start = point
                    end = check_points[i+1]

                    new_path = pathfind(self.coords.maze, start, end,
                                        self, self.coords, key)
                    if new_path == None:
                        new_path = []
                        
                    self.coords.final_path.extend(new_path)


    # displays text given text, colour and position/size
    def display_text(self, txt, colour, center, size):
        font = pygame.font.Font(None, size)
        text_surf = font.render(txt, True, colour)
        text_rect = text_surf.get_rect()
        text_rect.center = (center)
        self.win.blit(text_surf, text_rect)


class CoOrdinates():
    '''
    class containing all coordinates and functions for calculations todo with them
    '''

    
    def __init__(self):
        self.remove_all()


    def remove_all(self):
        self.start = None
        self.end = None
        self.walls = []
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []
        self.check_points = []


    def remove_last(self):
        self.maze = []
        self.open_list = []
        self.closed_list = []
        self.final_path = []


    # gets the furthest distance of a node from the (0, 0)
    def largest_distance(self):
        largest = 0
        for wall in self.walls:
            if wall[0] > largest: largest = wall[0]
            if wall[1] > largest: largest = wall[1]
        for point in self.check_points:
            if point[0] > largest: largest = point[0]
            if point[1] > largest: largest = point[1]
        return largest + 1


    # creates a 2d array of the maze and its walls
    def create_maze(self, giu):
        
        largest_distance = self.largest_distance()
        
        # makes sure the size of the maze if either the size of the gui
        # or the size of the maze made using the walls and checkpoints
        if gui.grid_size > largest_distance:
            largest = gui.grid_size
        else:
            largest = largest_distance
            
        self.maze = [[0 for x in range(largest)] for y in range(largest)]
        for wall in self.walls:
            try:
                wall_x, wall_y = wall
                self.maze[wall_x][wall_y] = 1
            except:
                pass


    # creates a random maze
    def generate_random_maze(self, gui):
        self.walls = []
        for i in range(gui.grid_size*gui.grid_size):
            if random.random() > 0.6:
                wall = (random.randint(0, gui.grid_size-1),
                        random.randint(0, gui.grid_size-1))
                if wall not in self.walls:
                    self.walls.append(wall)


# function for pathfinding using dfs, bfs, dijkstra and astar
# Returns a list of tuples as a path from the given start to the given end in the given maze
def pathfind(maze, start, end, gui, coords, key):
    
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    count = 0

    # Loop until you find the end
    while len(open_list) > 0:

        # skip pathfinding to create a wait effect. Ajustable speed
        if count >= gui.animation_speed:

            count = 0

            # Get the current node
            
            if key == "q": # dfs, get the latest node
                current_node = open_list[-1]
                current_index = len(open_list)-1
                
            elif key == "w": # bfs, get the newest node
                current_node = open_list[0]
                current_index = 0               
                
            elif key == "r": # a*, get the node with the lowest f value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.f < current_node.f:
                        current_node = item
                        current_index = index
                        
            elif key == "e": # dijkstra, get the node with the lowest g value
                current_node = open_list[0]
                current_index = 0
                for index, item in enumerate(open_list):
                    if item.g < current_node.g:
                        current_node = item
                        current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                coords.open_list = open_list
                coords.closed_list = closed_list
                return path # Return path

            # Generate children
            # left, down, right, up. Which makes dfs go in up, right, down, left order
            for new_pos in [(-1, 0), (0, 1), (1, 0), (0, -1)]: # Adjacent squares

                # Get node position
                node_pos = (current_node.position[0] + new_pos[0],
                            current_node.position[1] + new_pos[1])

                # Make sure within range
                if (node_pos[0] > (len(maze) - 1) or node_pos[0] < 0
                        or node_pos[1] > (len(maze[len(maze)-1]) -1)
                        or node_pos[1] < 0):
                    continue

                # Make sure walkable terrain
                if maze[node_pos[0]][node_pos[1]] != 0:
                    continue

                if Node(current_node, node_pos) in closed_list:
                    continue

                # Create new node
                child = Node(current_node, node_pos)

                # Child is on the closed list
                passList = [False for closed_child in closed_list if child == closed_child]
                if False in passList:
                    continue

                # for dfs and bfs we dont add anything to the node values
                
                if key == "e": # dijkstra, add one to g value
                    child.g = current_node.g + 1
                    
                elif key == "r": # a*, calculate f value
                    child.g = current_node.g + 1
                    # distance to end point
                    # the reason the h distance is powered by 0.6 is because
                    #it makes it prioritse diagonal paths over straight ones
                    # even though they are technically the same g distance, this makes a* look better
                    child.h = (((abs(child.position[0] - end_node.position[0]) ** 2) +
                                (abs(child.position[1] - end_node.position[1]) ** 2)) ** 0.6)
                    child.f = child.g + child.h

                # Child is already in the open list
                
                for open_node in open_list:
                    # check if the new path to children is worst or equal 
                    # than one already in the open_list (by measuring g)
                    if child == open_node and child.g >= open_node.g:
                        break
                    
                else:
                    # Add the child to the open list
                    open_list.append(child)

        # if skipped just update the gui
        else:

            coords.open_list = open_list
            coords.closed_list = closed_list
            gui.main(True)

        count += 1


class Node():
    '''
    node class for containing position, parent and costs
    '''
    
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
    gui = Gui(CoOrdinates())
    while True:
        gui.main()
