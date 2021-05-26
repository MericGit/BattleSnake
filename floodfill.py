import numpy
# Python3 program to implement
# flood fill algorithm
 
# Dimentions of paint screen
M = 11
N = 11
 
# A recursive function to replace
# previous color 'prevC' at '(x, y)'
# and all surrounding pixels of (x, y) d
# with new color 'newC' and
def floodFillUtil(screen, x, y, prevC, newC):
     
    # Base cases
    if (x < 0 or x >= M or y < 0 or
        y >= N or screen[x][y] != prevC or
        screen[x][y] == newC):
        return
 
    # Replace the color at (x, y)
    screen[x][y] = newC
 
    # Recur for north, east, south and west
    floodFillUtil(screen, x + 1, y, prevC, newC)
    floodFillUtil(screen, x - 1, y, prevC, newC)
    floodFillUtil(screen, x, y + 1, prevC, newC)
    floodFillUtil(screen, x, y - 1, prevC, newC)
 
# It mainly finds the previous color on (x, y) and
# calls floodFillUtil()
def floodFill(screen, x, y, newC):
    prevC = screen[x][y]
    floodFillUtil(screen, x, y, prevC, newC)
 
# Driver Code




def safety(yHead,xHead,clone,y,x,num):
    clone[y][x] = 1
    #print("PRE FLOOD: ")
    boardData = [[_el if _el != 2 else 0 for _el in _ar] for _ar in clone]
    #print(numpy.matrix(boardData))
    print("Starting flood fill at: " + str(yHead) + " " + str(xHead))
    floodFill(boardData,yHead,xHead,num)
    offLimit = sum(x.count(1) for x in boardData)
    available = sum(x.count(5) for x in boardData)
    print("Floodfill available: " + str(available))
    print("Floodfill offlimit: " + str(offLimit))
    #print(numpy.matrix(boardData))

    if (available  / (121-offLimit)) < 0.8:
        print("Floodfill returned Invalid: " + str(available / (121- offLimit))  + "Valid moves")
        return True
    else:
        print("Floodfill returned valid: " + str(available / (121- offLimit))  + "Valid moves")
        return False

