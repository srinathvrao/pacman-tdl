import random
import numpy as np
from optparse import OptionParser
from environmentAugmenter import layoutCorrector
import sys

numGhosts = 2 # can be changed from command line
numPacman = 1 # not implemented for >1 pacman agent

# It is assumed Pacman always has Agent ID 0, and ghosts can take every other ID.

def genLayout(width, height, numGhosts):
    
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

    for y in range(height):
        row = []
        for x in range(width):
            fill = random.choice(interior)
            if fill==' ': possible_agent_positions.append((x,y))
            row.append(fill)
        layout.append(row)

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


def createLayout(width, height, numGhosts):
    
    layout, pac_pos, ghost_positions = genLayout(width-2,height-2,numGhosts)
    layout = layoutCorrector(layout, pac_pos)
    for ghost_pos in ghost_positions:
        layout = layoutCorrector(layout, ghost_pos)

    return wrapLayout(layout)


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
    
    mazeWidth = options.width
    mazeHeight = options.height
    numGhosts = options.numGhosts
    numPacman = 1 # not implemented for >1 pacman agent

    layout = createLayout(mazeWidth, mazeHeight, numGhosts)

    for row in layout:
        print("".join(row))

