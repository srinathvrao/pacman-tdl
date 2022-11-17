import random
import numpy as np
from optparse import OptionParser
from environmentAugmenter import layoutCorrector
import sys
import os
import copy

t_height = 2 #default tunnel height
t_width = 40 #default tunnel width

# It is assumed Pacman always has Agent ID 0, and ghosts can take every other ID.

def genLayout(width, height,isTunnel=False):
    
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
    if isTunnel:
        midIndex = height//2
        top_border_tunnel=midIndex-t_height
        bottom_border_tunnel=midIndex+t_height
        for y in range(height):
            row=[]
            if y>top_border_tunnel and y<bottom_border_tunnel:
                for x in range(width+t_width):
                    fill = random.choice(interior)
                    #we don't want pacman to start in tunnel
                    #if fill==' ': possible_agent_positions.append((x,y))
                    row.append(fill)
            else:
                for x in range(width):
                    fill = random.choice(interior)
                    if fill==' ': possible_agent_positions.append((x,y))
                    row.append(fill)
            layout.append(row)
    else:
        for y in range(height):
            row = []
            for x in range(width):
                fill = random.choice(interior)
                if fill==' ': possible_agent_positions.append((x,y))
                row.append(fill)
            layout.append(row)
    return layout,possible_agent_positions

#fill layout with ghost and pacman 
def addItems(layout,possible_agent_positions):

    agent_positions = random.sample(possible_agent_positions, numGhosts + numPacman)
    pacman_position = agent_positions[0]
    ghost_positions = agent_positions[1:]
    pac_x, pac_y = pacman_position
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

    #adding the border for the tunnel
    for y in range(len(lay)):
        if y<=top_border_tunnel or y>=bottom_border_tunnel:
            lay[y].extend(['%']*t_width)
        elif y>top_border_tunnel or y<bottom_border_tunnel:
            continue
        
    #constructing new room
    room_list,_ = genLayout(mazeWidth-2,mazeHeight-2)
    room_list = layoutCorrector(room_list,[]) #making sure all food is traversable for new room

    #appending room to our layout
    for y in range(len(lay)):
        if y <len(room_list):
            lay[y].extend(room_list[y])

    return lay


def createLayout(width, height):
    
    layout, possible_pacman_pos = genLayout(width-2,height-2,isTunnel=True)
    layout, pacman_position, ghost_positions = addItems(layout, possible_pacman_pos)
    for ghost_pos in ghost_positions:
        layout = layoutCorrector(layout, ghost_pos)
    layout = putTunnel(layout)
    layout = wrapLayout(layout)
    layout = layoutCorrector(layout,pacman_position)
    
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
    

    options, otherjunk = parser.parse_args(sys.argv[1:])

    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    global mazeHeight,mazeWidth,numGhosts

    numPacman = 1 # not implemented for >1 pacman agent
    numGhosts = 2 # can be changed from command line
    mazeWidth = options.width
    mazeHeight = options.height
    numGhosts = options.numGhosts


    layout = createLayout(mazeWidth, mazeHeight)
    

    #writeLayout(mazeWidth, mazeHeight)
    for row in layout:
        print("".join(row))

