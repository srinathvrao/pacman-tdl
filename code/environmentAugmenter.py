import random
import numpy as np

def layoutCorrector(layout, agent_position, firstRoom=True):
    '''
        Layout Correction:
            - layout: h x w 2d list of the interior
            - agent_position: (x,y) of the agent

        The layout we make with the genLayout() function might have 
            unreachable locations blocked by walls.
        
        The correctLayout() function below detects this situation, 
            and makes these locations reachable.

        Implementation: BFS to check reachability, and 
                        BFS again to make a navigable path
    '''

    h, w = len(layout), len(layout[0])
    numSpaces = sum([ True if layout[p][q] in [' ','.','P','G','o'] else False for p in range(h) for q in range(w)])
    queue = [agent_position]
    visited = np.zeros((h,w)).astype(np.uint8)

    if firstRoom:
        mid_x, mid_y = w-1, h//2
        layout[mid_y][mid_x] = random.choice(['.',' '])
    else:
        mid_x, mid_y = w-1, h//2
        layout[mid_y][mid_x] = random.choice(['.',' '])
        mid_x = 0
        layout[mid_y][mid_x] = random.choice(['.',' '])


    # BFS to verify there are no unreachable spaces.
    while len(queue) > 0:
        x,y = queue.pop(0)
        if not visited[y,x]:
            visited[y,x] = 1
            # add the valid neighbors to the queue
            coords = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
            for coord in coords:
                xn, yn = coord
                if xn<0 or xn>=w or yn<0 or yn>=h:
                    pass
                elif layout[yn][xn] != '%':
                    queue.append((xn,yn))

    # if we are able to visit all the spaces, then we don't need to change the layout
    numVisited = visited.sum()
    if numVisited == numSpaces:
        return layout
    
    for y in range(h):
        for x in range(w):
            if visited[y,x] == 0:
                if layout[y][x] == '%':
                    visited[y,x] = 2
                elif layout[y][x] == 'G':
                    visited[y,x] = 3

    unvisited_list = list(zip(*np.where(visited == 0))) # get all unvisited spaces

    for u in unvisited_list:
        print("Location",u,"is unreachable. Modifying layout..")
        # BFS for removing walls that block the path
        queue = [(u,[])]
        foundPath = False
        nav_path = []
        unvis = np.zeros((h,w)).astype(np.uint8)
        while len(queue)>0 and not foundPath:
            qp = queue.pop(0)
            y,x = qp[0]
            if not unvis[y,x]:
                unvis[y,x] = 1
                # add the valid neighbors to the queue
                coords = [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]
                for coord in coords:
                    xn, yn = coord
                    if xn<0 or xn>=w or yn<0 or yn>=h:
                        pass
                    else:
                        path = qp[1].copy()
                        path.append((y,x))
                        if visited[yn,xn]==1:
                            nav_path = path.copy()
                            foundPath = True
                            break
                        queue.append(( (yn,xn), path ))

        for coord in nav_path:
            y,x = coord
            visited[y,x] = 1
            if layout[y][x]=='%':
                layout[y][x] = random.choice(['.',' '])



    return layout
