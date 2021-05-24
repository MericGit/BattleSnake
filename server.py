import os
import random
import json
import numpy
import cherrypy
from termcolor import colored
import pathfind
import calculations
import pathfind2

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""
turn = 0


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
            "color": "#00FF74",
            "head": "evil", 
            "tail": "curled",  
        }
    
    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
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
        turn+=1
        data = cherrypy.request.json
        Food = []
        xSize = data['board']['height']
        ySize = data['board']['width']
        #----------------------
        #Board Generation Data
        boardData = [ [0] * xSize for _ in range(ySize)]
        snakeList = data['board']['snakes']
        xHead = data['you']['head']['x']
        yHead = ySize - 1 - data['you']['head']['y']
        #print("xHead is")
        #print(xHead)
        #print("yHead is")
        #print(yHead)
        for i in data['board']['food']:
            Food.append((xSize - 1 - i['y'],i['x']))



        tuples = []
        for x in snakeList:
            body = x['body']
        #    head = x['head']
            for y in body[:-1]:
                boardData[xSize - 1 - y['y']][y['x']] = 1
        for x in snakeList[1: ]:
            head = x['head']
            tuples.append((ySize - 1 - head['y'] - 1,head['x'])) # 1 above
            tuples.append((ySize - 1 - head['y'] + 1,head['x'])) # below
            tuples.append((ySize - 1 - head['y'],head['x'] - 1)) # left
            tuples.append((ySize - 1 - head['y'],head['x'] + 1)) # right

        sH = calculations.path2head(xHead,yHead,tuples)
        if len(sH) > 1:
            boardData[ySize - 1 - sH[0][0]][sh[0][1]] = 1



#            boardData[xSize - 1 - head['y']][head['x']] = 1
            
        #print("-----------\nSTATE UPDATED:")
        #print(numpy.matrix(boardData))
        #print("-----------")
        #---------------------

        size = len(data['you']['body'])
        #print("Size is: ")
        #print(size)
        # Choose a random direction to move in.





        if data['you']['health'] > 40 and size > 5:
            #print("not too hungry so going just gonna try and survive")
            path = pathfind2.astar(boardData, (yHead,xHead),(data['you']['body'][-1]['y'],data['you']['body'][-1]['x']))
        else:
            #print("am hungry")
            path = pathfind2.astar(boardData, (yHead,xHead), calculations.distanceSort(xHead,yHead,Food)[0])
        moves = []
        #print(colored("Path is: ","cyan"))
        #print(colored(path,'yellow'))
        #print("head: " + str(xHead) + " " + str(yHead))
        #print(colored("TARGET MOVE:","cyan"))
        #print(path[1])
        #print(colored("MOVES LIST: ","cyan"))
        if len(path) >= 2:
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
            moves = ['left','right','down','up']

        #print("Move removals: ")
        #print(xHead)
        #print(yHead)
        if moves:
            moves = moveCheck(xHead,yHead,xSize,ySize,boardData,moves)

        #print(moves)
        if moves:
            print("Turn count: " + str(turn))
            print("Path is: " + str(path))
            print("Possible moves are: " + str(moves))
            print("Target: " + str(moves[0]))
            return {"move": moves[0]}
        else:
            print("ERROR: - PATHFIND RETURN NULL -")
            print("RUNNING SURVIVAL MODE UNTIL PATHFIND RECONNECTS")

        

        

def moveCheck(xHead,yHead,xSize,ySize,boardData,moves):
    if 'left' in moves:
        if (xHead - 1 < 0) or (boardData[yHead][xHead - 1] == 1):
        #if boardData[yHead][xHead - 1] == 1 or xHead - 1 < 0:
            print(colored("Illegal move: LEFT removed","red"))
            moves.remove('left')
    if 'right' in moves:
        if xHead + 1 > (xSize - 1) or boardData[yHead][xHead + 1] == 1:
        #if boardData[yHead][xHead + 1] == 1 or xHead + 1 > xSize:
            print(colored("Illegal move: RIGHT removed","red"))
            moves.remove('right')
    if 'up' in moves:
        if yHead - 1 < 0 or boardData[yHead - 1][xHead] == 1:
        #if boardData[yHead - 1][xHead] == 1 or yHead - 1 < 0:
            print(colored("Illegal move: UP removed","red"))
            moves.remove('up')
    if 'down' in moves:
        if yHead + 1 > (ySize - 1) or boardData[yHead + 1][xHead] == 1:
        #if boardData[yHead + 1][xHead] == 1 or yHead + 1 > ySize:
            print(colored("Illegal move: DOWN removed","red"))
            moves.remove('down')
    return moves


    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
    #    data = cherrypy.request.json
    #    print(data)
        print("END")
        return "ok"


if __name__ == "__main__":


    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
