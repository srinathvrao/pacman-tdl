import random
import numpy as np
from optparse import OptionParser
from environmentAugmenter import layoutCorrector
import sys
import os
import copy

def genLayout(width, height):
    
    '''
        Layout Generation:
            - width, height of the game.
            - numGhosts: number of ghosts in the game.
            - numPacman not implemented (assumed to be 1).

        Creates a simple random layout with the given width and height.
            - interiors (walls / free space / dots) are assigned probabilities
                of occurrence.

        Returns a layout of the given dimensions.
    '''

    interior = []
    interior.extend([" "]*3) # 30% free space
    interior.extend(["%"]*2) # 20% walls
    interior.extend(["."]*5) # 50% food dots
    

    layout = []
    possible_agent_positions = []
    #need to fill extra items in tunnel, hence we need separate conditional
    for y in range(height):
        row = []
        for x in range(width):
            fill = random.choice(interior)
            if fill==' ': possible_agent_positions.append((x,y))
            row.append(fill)
        layout.append(row)
    return layout,possible_agent_positions

#fill layout with ghost and pacman 
def addItems(layout,possible_agent_positions,extraRoom = False):

    agent_positions = random.sample(possible_agent_positions, numGhosts + numPacman)
    pacman_position = agent_positions[0]
    ghost_positions = agent_positions[1:]
    pac_x, pac_y = pacman_position
    if not extraRoom:
        layout[pac_y][pac_x] = 'P'

    for ghost_position in ghost_positions:
        ghost_x, ghost_y = ghost_position
        layout[ghost_y][ghost_x] = 'G'

    return layout, pacman_position, ghost_positions

def wrapLayout(layout):
    
    #   wraps the layout with walls
    h,w = len(layout),len(layout[0])
    lay = [['%']*(w+2)]
    for y in range(h):
        row = ['%']
        row.extend(layout[y])
        row.append('%')
        lay.append(row)
    lay.append(['%']*(w+2))
    return lay

def putTunnel(lay):
    #create new layout

    #calculating the borders for the tunnel
    midIndex = len(lay)//2
    top_border_tunnel=midIndex-t_height
    bottom_border_tunnel=midIndex+t_height


    no_wall_interior = []
    no_wall_interior.extend([" "]*5)
    no_wall_interior.extend(["."]*5)


    #constructing the tunnel
    for y in range(len(lay)):
        #adding the border for the tunnel
        if y<=top_border_tunnel or y>=bottom_border_tunnel:
            lay[y].extend(['%']*t_width)
        #adding items inside the tunnel
        elif y>top_border_tunnel or y<bottom_border_tunnel:
            row=[]
            #tunnel without possibility of walls
            for x in range(t_width):
                fill = random.choice(no_wall_interior)
                #we don't want pacman to start in tunnel
                #if fill==' ': possible_agent_positions.append((x,y))
                row.append(fill)
            lay[y].extend(row)

        
    #constructing new room
    room_list,pac_ghost_pos = genLayout(mazeWidth-2,mazeHeight-2)
    #layout, pacman_position, ghost_positions
    room_list,_,__ = addItems(room_list,pac_ghost_pos,extraRoom=True)
    room_list = layoutCorrector(room_list,[]) #making sure all food is traversable for new room

    #appending room to our layout
    for y in range(len(lay)):
        if y <len(room_list):
            lay[y].extend(room_list[y])

    return lay


def createLayout(width, height):
    
    layout, possible_pacman_pos = genLayout(width-2,height-2)
    layout, pacman_position, ghost_positions = addItems(layout, possible_pacman_pos,extraRoom=False)
    for ghost_pos in ghost_positions:
        layout = layoutCorrector(layout, ghost_pos)

    for rooms in range(1,numRooms):
        layout = putTunnel(layout)

    layout = wrapLayout(layout)
    
    return layout

def writeLayout(width, height, numGhosts):
    lay = createLayout(width, height)
    file = open("./layouts/custom_{0}_{1}_{2}.lay".format(width, height, numGhosts),"w")
    for i in lay:
        file.write("".join(i)+'\n')
    file.close()


    


if __name__ == "__main__":

    usageStr = """
    USAGE:      python environmentGenerator.py <options>
    EXAMPLES:   (1) python environmentGenerator.py
                    - creates a random 10x10 pacman game layout, with 2 ghosts.
                (2) python pacman.py -w 20 -l 25 -g 5
                    - creates a pacman game layout with width 20, height 25, and 5 ghost agents
    """
    parser = OptionParser(usageStr)

    parser.add_option('-w', '--width', dest='width', type='int',
                      help='the width of the maze', metavar='WIDTH', default=10)
    parser.add_option('-l', '--height', dest='height', type='int',
                      help='the height of the maze', metavar='HEIGHT', default=10)
    parser.add_option('-g', '--numGhosts', dest='numGhosts', type='int',
                      help='the number of ghost agents in the game', metavar='NUMGHOSTS', default=2)
    parser.add_option('-r', '--rooms', dest='rooms', type='int',
                      help='number of rooms', metavar='ROOMS', default=1)
    

    options, otherjunk = parser.parse_args(sys.argv[1:])

    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))

    global mazeHeight,mazeWidth,numGhosts,numRooms,t_height,t_width

    numPacman = 1 # not implemented for >1 pacman agent
    numGhosts = 1 # ghost per room
    mazeWidth = options.width
    mazeHeight = options.height
    numGhosts = options.numGhosts
    numRooms = options.rooms
    t_height = 2 #default tunnel height
    t_width = mazeWidth #default tunnel width

    layout = createLayout(mazeWidth, mazeHeight)
    

    #writeLayout(mazeWidth, mazeHeight)
    for row in layout:
        print("".join(row))

