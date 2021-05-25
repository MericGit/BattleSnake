import collections
from termcolor import colored
def distanceSort(posX,posY,fruitArray):
    #print(colored("DISTANCE SORT DEBUG:","cyan"))
    
    distances = []
    for x in fruitArray:
       thing = (abs(posX - x[1]) + abs(posY - x[0]))
       distances.append(thing)
    #print(fruitArray)
    #print(colored("RAW: Distances","cyan"))
    #print(colored(distances,"yellow"))
    output = [fruitArray for _, fruitArray in sorted(zip(distances, fruitArray))]
    #print(output)
    #.
    print("Fruit sort complete")
    return output




def simpleDist(tuple1,tuple2):
   distance = abs(tuple1[0] - tuple2[1]) + abs(tuple1[1] - tuple2[1])
   return distance

def path2head(headX,headY,tuples):
   distances = []
   for x in tuples:
      temp = simpleDist((headY,headX),x)
      distances.append(temp)
   output = [tuples for _, tuples in sorted(zip(distances, tuples))]
   return output
