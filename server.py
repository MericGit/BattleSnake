import os
import random
import json
import numpy
import cherrypy
from termcolor import colored
import calculations
import pathfind2
import floodfill

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
turn = 0
hunt = False
aggroRange = 2
murdercd = 0
class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "Lawrence Zhang",
            "color": "#5E8773",
            "head": "tiger-king", 
            "tail": "hook",  
        }
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        global turn
        turn = 0
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        xSize = data['board']['height']
        ySize = data['board']['width']

    #    boardData = [ [0] * xSize for _ in range(ySize)]
        #print(numpy.matrix(boardData))
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        global turn
        print(colored("Turn count is: " + str(turn),"magenta"))
        turn+=1

        #TDefine and init the size and locs of some stuff
        #--------------------------------------
        data = cherrypy.request.json

        xSize = data['board']['height']
        ySize = data['board']['width']

        boardData = [ [0] * xSize for _ in range(ySize)]
        snakeList = data['board']['snakes']
        xHead = data['you']['head']['x']
        yHead = ySize - 1 - data['you']['head']['y']
        #-------------------------------------

        #print("xHead is")
        #print(xHead)
        #print("yHead is")
        #print(yHead)
        Food = []
        for i in data['board']['food']:
            Food.append((xSize - 1 - i['y'],i['x']))


        #Begin initializing and loading board data
        tuples = []
        for x in snakeList:
            body = x['body']
        #    head = x['head']
            for y in body[:-1]:
                boardData[ySize - 1 - y['y']][y['x']] = 1
        for x in snakeList:
            head = x['head']
            if x['name'] != data['you']['name']:
                tuples.append((ySize - 1 - head['y'] - 1,head['x'])) # 1 above
                tuples.append((ySize - 1 - head['y'] + 1,head['x'])) # below
                tuples.append((ySize - 1 - head['y'],head['x'] - 1)) # left
                tuples.append((ySize - 1 - head['y'],head['x'] + 1)) # right


        closestSnake = calculations.getClosestSnake(ySize,xHead,yHead,snakeList)






        # ----------------------------------------------
        #
        # FIGHT OR FLIGHT MODULE
        # Determines if the snake should avoid the closet enemy head, 
        # or aim towards it to kill it.
        # Code is messy as path2head is broken
        # TODO: FIX path2head
        #
        #-------------------------------------------------
        global hunt
        global aggroRange
        global murdercd

        if murdercd >= 2:
            murdercd = 5
        sH = calculations.path2head(yHead,xHead,tuples)
        print("POSt-SORT: " + str(sH))
        print("CLOSEST SNAKE LENGTH: " + str(closestSnake['length']))
        if len(sH) > 1 and closestSnake['length'] >= data['you']['length']:
            print("SH IS: ")
            print(sH)
            print("ENEMY HEAD LOC: ")
            hunt = False
            if sH[0][0] < ySize and sH[0][0] > -1 and sH[0][1]  > -1 and sH[0][1] < xSize:
                print("Added block at " + str(sH[0][0]) + str(sH[0][1]))
                boardData[   sH[0][0]   ]      [  sH[0][1]    ] = 1   #First closest area
            if sH[1][0] < ySize and sH[1][0] > -1 and sH[1][1]  > -1 and sH[1][1] < xSize:
                print("Added block at " + str(sH[1][0]) + str(sH[1][1]))
                boardData[   sH[1][0]   ]      [  sH[1][1]    ] = 1   #Second closest
            if sH[2][0] < ySize and sH[2][0] > -1 and sH[2][1]  > -1 and sH[2][1] < xSize:
                print("Added block at " + str(sH[2][0]) + str(sH[2][1]))
                boardData[   sH[2][0]   ]      [  sH[2][1]    ] = 1   #Third closest area
#            if sH[3][0] < ySize and sH[3][0] > -1 and sH[3][1]  > -1 and sH[3][1] < xSize:
#                print("Added block at " + str(sH[3][0]) + str(sH[3][1]))
#                boardData[   sH[3][0]   ]      [  sH[3][1]    ] = 1   #Fourth closest area                
        elif len(sH) > 1 and closestSnake['length'] < data['you']['length'] and data['you']['health'] > 20 and calculations.simpleDist((yHead,xHead),(ySize - 1 - closestSnake['head']['y'],closestSnake['head']['x'])) < aggroRange:
            hunt = True
            if sH[0][0] < ySize - 1 and sH[0][0] - 1 > 0 and sH[0][1]  > -1 and sH[0][1] < xSize and boardData[   sH[0][0]   ]      [  sH[0][1]    ] != 1:
                print("Added TARGET at " + str(sH[0][0]) + str(sH[0][1]))
                Food.append((sH[0][0],sH[0][1]))
            if sH[1][0] < ySize - 1 and sH[1][0] - 1 > 0 and sH[1][1]  > -1 and sH[1][1] < xSize and boardData[   sH[1][0]   ]      [  sH[1][1]    ] != 1:
                print("Added TARGET at " + str(sH[1][0]) + str(sH[1][1]))
                Food.append((sH[1][0],sH[1][1]))
            if sH[2][0] < ySize - 1 and sH[2][0] - 1 > 0 and sH[2][1]  > -1 and sH[2][1] < xSize and boardData[   sH[2][0]   ]      [  sH[2][1]    ] != 1:
                print("Added TARGET at " + str(sH[2][0]) + str(sH[2][1]))
                Food.append((sH[2][0],sH[2][1]))
#            if sH[3][0] < ySize - 1 and sH[3][0] - 1 > 0 and sH[3][1]  > -1 and sH[3][1] < xSize and boardData[   sH[3][0]   ]      [  sH[3][1]    ] != 1:
#                print("Added TARGET at " + str(sH[3][0]) + str(sH[3][1]))
#                Food.append((sH[3][0],sH[3][1]))
        #boardData[xSize - 1 - head['y']][head['x']] = 1
        print("Distance to nearest is: ")
        print(calculations.simpleDist((yHead,xHead),(ySize - 1 - closestSnake['head']['y'],closestSnake['head']['x'])))

        #print("-----------\nSTATE UPDATED:")
        #print(numpy.matrix(boardData))
        #print("-----------")
        #---------------------
        #print("Size is: ")
        #print(size)
        # Choose a random direction to move in.




        path = []
        if data['you']['health'] > 30 and hunt is True and data['you']['length'] > 4 and murdercd < 2:
            print(colored("Aggro Hunt","red"))
            murdercd +=2
            path = pathfind2.astar(boardData, (yHead,xHead), calculations.distanceSort(xHead,yHead,Food)[0])
        elif data['you']['health'] > 35 and data['you']['length'] > 5:
            print(colored("Survive","red"))
            path = pathfind2.astar(boardData, (yHead,xHead),(ySize - 1 - data['you']['body'][-1]['y'],data['you']['body'][-1]['x']))
        else:
            print(colored("Seek food","yellow"))
            path = pathfind2.astar(boardData, (yHead,xHead), calculations.distanceSort(xHead,yHead,Food)[0])
        moves = []

        if path:
            for step in path:
                boardData[step[0]][step[1]] = 2

            for row in boardData:
                line = []
                for col in row:
                    if col == 1:
                        line.append(colored("□","green"))
                    elif col == 0:
                        line.append(colored("□","white"))
                    elif col == 2:
                        line.append(colored("□","red"))
                print("".join(line))

            print(path)
        else:
            print(boardData)

        
        #print(colored("Path is: ","cyan"))
        #print(colored(path,'yellow'))
        #print("head: " + str(xHead) + " " + str(yHead))
        #print(colored("TARGET MOVE:","cyan"))
        #print(path[1])
        #print(colored("MOVES LIST: ","cyan"))
        if path is not None:
            target = path[1]
            if target[1] > xHead:
                #print(colored("right","yellow"))
                moves.append('right')
            if target[1] < xHead:
                #print(colored("left","yellow"))
                moves.append('left')
            if target[0] > yHead:
                #print(colored("down","yellow"))
                moves.append('down')
            if target[0] < yHead:
                #print(colored("up","yellow"))
                moves.append('up')
        else:
            print("ERROR: - PATHFIND RETURN NULL -")
            print("RUNNING SURVIVAL MODE UNTIL PATHFIND RECONNECTS")
            moves = ['left','right','down','up']
            print(numpy.matrix(boardData))

        #print("Move removals: ")
        #print(xHead)
        #print(yHead)
        print("Precheck: " + str(moves))
        if moves:
            moveCheck(xHead,yHead,xSize,ySize,boardData,moves)
        
        if not moves:
            print("ERROR: - PATHFIND RETURN WRONG SOLUTION -")
            print("RUNNING SURVIVAL MODE UNTIL PATHFIND RECONNECTS")
            moves = ['left','right','down','up']            
            moveCheck(xHead,yHead,xSize,ySize,boardData,moves)
        
        if not moves: 
            print("Survival mode check failed. Running gamble")
            moves = ['left','right','down','up']
            if sH[0][0] < ySize - 1 and sH[0][0] -1 > -1 and sH[0][1]  > -1 and sH[0][1] < xSize:
                print("Removing block at " + str(sH[0][0]) + str(sH[0][1]))
                boardData[   sH[0][0]   ]      [  sH[0][1]    ] = 0   #First closest area
            if sH[1][0] < ySize  and sH[1][0] -1 > -1 and sH[1][1]  > -1 and sH[1][1] < xSize:
                print("Removing block at " + str(sH[1][0]) + str(sH[1][1]))
                boardData[   sH[1][0]   ]      [  sH[1][1]    ] = 0   #Second closest
            if sH[2][0] < ySize  and sH[2][0] - 1 > -1 and sH[2][1]  > -1 and sH[2][1] < xSize:
                print("Removing block at " + str(sH[2][0]) + str(sH[2][1]))
                boardData[   sH[2][0]   ]      [  sH[2][1]    ] = 0   #Third closest area
            if sH[3][0] < ySize  and sH[3][0] -1 > -1 and sH[3][1]  > -1 and sH[3][1] < xSize:
                print("Removing block at " + str(sH[3][0]) + str(sH[3][1]))
                boardData[   sH[3][0]   ]      [  sH[3][1]    ] = 0   #Fourth closest area  
            for x in snakeList:
                body = x['body']
            #    head = x['head']
                for y in body[:-1]:
                    boardData[ySize - 1 - y['y']][y['x']] = 1
            if 'left' in moves:
                print("Checking Left")
                if (xHead - 1 < 0) or (boardData[yHead][xHead - 1] == 1):
                #if boardData[yHead][xHead - 1] == 1 or xHead - 1 < 0:
                    print(colored("Illegal move: LEFT removed","red"))
                    moves.remove('left')
            if 'right' in moves:
                print("Checking Right")
                if xHead + 1 > (xSize - 1) or boardData[yHead][xHead + 1] == 1:
                #if boardData[yHead][xHead + 1] == 1 or xHead + 1 > xSize:
                    print(colored("Illegal move: RIGHT removed","red"))
                    moves.remove('right')
            if 'up' in moves:
                print("Checking Up")
                if yHead - 1 < 0 or boardData[yHead - 1][xHead] == 1:
                #if boardData[yHead - 1][xHead] == 1 or yHead - 1 < 0:
                    print(colored("Illegal move: UP removed","red"))
                    moves.remove('up')
            if 'down' in moves:
                print("Checking Down")
                if yHead + 1 > (ySize - 1) or boardData[yHead + 1][xHead] == 1:
                #if boardData[yHead + 1][xHead] == 1 or yHead + 1 > ySize:
                    print(colored("Illegal move: DOWN removed","red"))
                    moves.remove('down')
        murdercd -=1
        #print(moves). 
        if moves:
            print("Debug list: xHead: " + str(xHead) + " yHead: " + str(yHead) + "Tail x: " + str(data['you']['body'][-1]['x']) + "Tail y: " + str(ySize - 1 - data['you']['body'][-1]['y']))
            print("Path is: " + str(path))
            print("Possible moves are: " + str(moves))
            print("Target: " + str(moves[0]))
            return {"move": moves[0]}
    

            

        

        #.def safety(clone,x,y,num): d


def moveCheck(xHead,yHead,xSize,ySize,boardData,moves):
    if 'left' in moves:
        print("Checking Left")
        if (xHead - 1 < 0) or (boardData[yHead][xHead - 1] == 1) or floodfill.safety(xSize,ySize,yHead,xHead - 1,boardData,yHead,xHead,5):
        #if boardData[yHead][xHead - 1] == 1 or xHead - 1 < 0:
            print(colored("Illegal move: LEFT removed","red"))
            moves.remove('left')
    if 'right' in moves:
        print("Checking Right")
        if xHead + 1 > (xSize - 1) or boardData[yHead][xHead + 1] == 1  or floodfill.safety(xSize,ySize,yHead,xHead + 1,boardData,yHead,xHead,5):
        #if boardData[yHead][xHead + 1] == 1 or xHead + 1 > xSize:
            print(colored("Illegal move: RIGHT removed","red"))
            moves.remove('right')
    if 'up' in moves:
        print("Checking Up")
        if yHead - 1 < 0 or boardData[yHead - 1][xHead] == 1 or floodfill.safety(xSize,ySize,yHead - 1,xHead,boardData,yHead,xHead,5):
        #if boardData[yHead - 1][xHead] == 1 or yHead - 1 < 0:
            print(colored("Illegal move: UP removed","red"))
            moves.remove('up')
    if 'down' in moves:
        print("Checking Down")
        if yHead + 1 > (ySize - 1) or boardData[yHead + 1][xHead] == 1 or floodfill.safety(xSize,ySize,yHead + 1,xHead,boardData,yHead,xHead,5):
        #if boardData[yHead + 1][xHead] == 1 or yHead + 1 > ySize:
            print(colored("Illegal move: DOWN removed","red"))
            moves.remove('down')
    return


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.d 
    #    data = cherrypy.request.json
    #    print(data)
        print("                  ")
        print("                   ")
        print("END")
        global turn
        turn = 0
        return "ok"


if __name__ == "__main__":


    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
