import math
import time

x = 0

done = False

class Node():
    def __init__(self,x,y,typ,gh=[0,0],parent=None):
        self.position = (x,y)
        self.typ = typ
        self.gh = gh
        self.parent = parent

class Level():
    def __init__(self):
        self.map = []
        self.goal = None
        self.highest_node = 0

    def add_node(self,node):
        self.map.append(node)

    def remove_node(self,node):
        self.map.remove(node)
        
    def set_goal(self,goal):
        self.goal = goal

    def set_highest_node(self,node):
        self.highest_node = node

class Environment():
    def __init__(self):
        self.map = []
        self.level = Level()
        for i in xrange(0,10):
            for j in xrange(0,10):
                self.level.add_node(Node(i,j,0))
        self.level.set_goal((9,9))

class Buggy():
    def __init__(self,x,y):
        self.counter = 0
        self.mode = 0
        self.position = [x,y]
        self.known_level = Level()
        starting_node = Node(self.position[0],self.position[1],0)
        self.known_level.add_node(starting_node)
        self.goal = None
        self.current = starting_node
        self.closedset = []
        self.openset = []
        self.neighbours = []
        self.last_position = None
        self.backtrack_counter = 0
        self.holding_up = False
        self.holding_down = False
    def set_goal(self,goal_position_x,goal_position_y):
        self.goal = Node(goal_position_x,goal_position_y,0)
    def get_hyp(self,pos1,pos2):
        x_dist = abs(pos1[0]-pos2[0])
        y_dist = abs(pos1[1]-pos2[1])
        hyp = math.sqrt(pow(x_dist,2)+pow(y_dist,2))
        return hyp
    def follow_path(self,path):
        start = True
        for node in path:
            last_position = self.current.position
            self.current.position = [node[0],node[1]]
            if start:
                start = False
            else:
                pass
            buggy.counter += 1
    def add_neighbouring_nodes(self,environment,know_map):
        x = self.current.position[0]
        y = self.current.position[1]
        neighbours = []
        for node in environment:
            add_node = False
            if (x+1,y) == node.position:
                add_node = True
                for node2 in self.known_level.map:
                    if node2.position == (x+1,y):
                        add_node = False
                if add_node:
                    neighbours.append(Node(x+1,y,0))
                add_node = False
            if (x-1,y) == node.position and not Node(x-1,y,0) in self.known_level.map:
                add_node = True
                for node2 in self.known_level.map:
                    if node2.position == (x-1,y):
                        add_node = False
                if add_node:
                    neighbours.append(Node(x-1,y,0))
                add_node = False
            if (x,y+1) == node.position and not Node(x,y+1,0) in self.known_level.map:
                add_node = True
                for node2 in self.known_level.map:
                    if node2.position == (x,y+1):
                        add_node = False
                if add_node:
                    neighbours.append(Node(x,y+1,0))
                add_node = False
            if (x,y-1) == node.position and not Node(x,y-1,0) in self.known_level.map:
                add_node = True
                for node2 in self.known_level.map:
                    if node2.position == (x,y-1):
                        add_node = False
                if add_node:
                    neighbours.append(Node(x,y-1,0))
                add_node = False
        for node in neighbours:
            self.known_level.add_node(node)
        self.neighbours = neighbours
    def get_neighbours(self):
        x = self.current.position[0]
        y = self.current.position[1]
        neighbours = []
        ##### DETECT POSIBLE NEIGHBOURS HERE #####
        for node in self.known_level.map:
            if (x+1,y) == node.position or (x-1,y) == node.position:
                neighbours.append(node.position)
            if (x,y+1) == node.position or (x,y-1) == node.position:
                neighbours.append(node.position)
        return neighbours
    def get_next_position(self,know_map):
        lowest = None
        lowest_comb = None
        comb = None
        for node in self.openset:
            dist = self.get_hyp(self.current.position,node.position)
            score = self.get_hyp(node.position,self.goal.position)
            if self.mode == 0 and not know_map:
                comb = dist*3 + score*1
            elif self.mode == 1 and not know_map:
                comb = dist*1 + score*0
            else:
                comb = dist*0 + score*0
            if not lowest or comb < lowest_comb:
                lowest = node
                lowest_comb = comb
        neighbours = self.get_neighbours()
        if lowest.position not in neighbours:
            pos = self.current.position
            gol = self.goal.position
            if not know_map:
                self.backtrack_counter += 1
                probe = Buggy(self.current.position[0],self.current.position[1])
                probe.set_goal(lowest.position[0],lowest.position[1])
                path = probe.find_path(self.known_level,0,True)
                self.last_position = path[-1]
                probe.follow_path(path)
                
        return lowest
    def score_neighbours(self):
        for node in self.neighbours:
            tentative_g_score = self.current.gh[0] + 1
            node.parent = self.current.position
            node.gh[0] = tentative_g_score
            node.gh[1] = self.get_hyp(node.position,self.goal.position)
    def reconstruct_path(self):
        child = self.current.parent
        path = []
        path.insert(0,self.current.position)
        finding_path = True
        if len(self.closedset) <= 1:
            finding_path = False
        #print "child:",child,"closedset:",self.closedset
        while finding_path:
            for node in self.closedset:
                #print node.position,child
                #time.sleep(0.5)
                if node.position == child:
                    path.insert(0,node.position)
                    child = node.parent
                    #print node.position,child
                    if child == None:
                        finding_path = False
        return path
    def find_path(self,environment,mode=0,know_map=False):
        global done
        self.mode = mode #djikstra or (a*+buggy) depending on if the level has been discovered
        self.openset.append(Node(self.position[0],self.position[1],0)) #add current position to list of explorable paths
        while self.openset: #while there is an explorable path:
            if not know_map: print "current position:",self.current.position
            self.last_position = self.current.position #remember last position
            self.current = self.get_next_position(know_map) #and get the next position which will be the closest unexplored path
            #print "next position:",self.current.position
            if done: #if the global 'done' variable is true
                break #stop
            self.counter += 1
            if self.current.position == self.goal.position: #if the buggy has reached the goal
                if mode == 1 and len(self.openset) > 0: #and the buggy is not using djikstra
                    pass
                else:
                    return self.reconstruct_path() #output the found path
                    break
            self.openset.remove(self.current) #remove the currently occupied node from the list of explorable paths
            self.closedset.append(self.current) #add the node to the list of previously explored paths
            self.add_neighbouring_nodes(environment.map,know_map) #get the surrounding nodes
            for node in self.neighbours:
                self.openset.append(node) #and add them to the list of explorable path
            self.score_neighbours() #and score them based on the distance from them to the goal
            if len(self.openset) == 0 and not self.current.position == self.goal.position: #if the list of available node is empty but you have not reached the goal yet
                self.openset.append(self.goal) #add the goal to the list

environment = Environment()
level = environment.level
buggy = Buggy(0,0) #create the buggy and it's start point
buggy.set_goal(level.goal[0],level.goal[1]) #set the goal
buggy.find_path(level,x) #find the path within the level, using (a*+buggy) mode
print "Found goal in",buggy.counter-1,"steps"
first_pass = buggy.counter-1
new_enviro = buggy.known_level
lvl = buggy.known_level
clo = buggy.closedset
ope = buggy.openset
if x == 0:
    buggy = Buggy(level.goal[0],level.goal[1])
    buggy.set_goal(0,0)
    buggy.known_level = lvl
    buggy.closedset = clo
    buggy.openset = ope
    buggy.find_path(level,1)
    print "Discovered entire map in",buggy.counter+first_pass,"steps, using",buggy.backtrack_counter,"backtracks"
    new_enviro = buggy.known_level
    buggy = Buggy(0,0)
    buggy.set_goal(level.goal[0],level.goal[1])
    path = buggy.find_path(new_enviro,0,True)
    print "Shortest path is",len(path),"steps\n"
    print path
    buggy.counter = 0
    buggy.follow_path(path)
    #print "got to goal in",len(path),"steps\n"
    
if x == 1:
    buggy = Buggy(0,0)
    buggy.set_goal(level.goal[0],level.goal[1])
    path = buggy.find_path(new_enviro,x,True)
    buggy.follow_path(path)
    #print "got to goal in",len(path),"steps\n"
