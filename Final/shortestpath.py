'''
* Team Id : #2149
* Author List :<Anirudh S>,<Rahul KR>
* Filename: shortestpath.py
* Theme: Thirsty Crow
* Functions: connect,dijkstras,get_next,step,print_path,distance,route,loop
* Global Variables:finalroute
'''
####  WE ARE IMPORTING ALL THE FUNCTIONS of GLteapot to this python file##



from collections import defaultdict
import math
import serial
import time
from GLteapot import *
from threading import Thread



 


class DirectedGraph(dict):
    path=[]
  
    """Create a directed Graph. Root keys contain a dictionary of other nodes they are directed to with 
    corresponding weight"""
    def __missing__(self, key):
        value = self[key] = {key: 0}  # A keys distance to itself is always 0
        return value
    
    def connect(self, node1, node2, weight):
        nodes = self.keys()
        if node1 not in nodes:
            self[node1]
        if node2 not in nodes:
            self[node2]
        self[node1][node2] = weight
        
    def connected_nodes(self, node):
        return {k: v for k, v in self[node].items() if k != node}
    '''
    * Function Name: dijkstras
    * Input: start node, destination node
    * Output: path to be travelled in terms of nodes
    * Logic: makes use of dijkstras algorithm
    * Example Call: dijkstras('35','44')
    '''
        
    def dijkstras(self, start, end):
        
        def get_next():
            remaining = {k: v for k, v in distance.items() if k not in finished}
            next_node = min(remaining, key=remaining.get)
            return next_node 
            
        def step(node):
            cost = 0 if parent[node] is None else distance[node]  # If no parents, then this is the starting node
            for n, w in self.connected_nodes(node).items():
                if distance[n] is None or distance[n] > w + cost:
                    parent[n] = node
                    distance[n] = cost + w
            finished.append(node)
        '''
        * Function Name: print_path
        * Input: 
        * Output: path to be travelled in terms of nodes
        * Logic: appends the nodes and gives the path
        * Example Call: print_path()
        '''    
        
        def print_path():
            path = [end]
            node = end
            while parent[node] != start:
                path.append(parent[node])
                node = parent[node]
            path.append(start)
            path.reverse()
            return path
        
            
        
        finished = []
        distance = {}
        parent = {}
        for node in self.keys():
            distance[node] = 0 if (node == start) else math.inf   
            parent[node] = None

        step(start)
        while end not in finished:
            nextNode = get_next()
            step(nextNode)
        
        
        return print_path()


  
    
        
       
       

global pebblenodes
finalroute=""
global counter
counter=0


'''
* Function Name:distance
* Input: x coordinate of node1,y cooedinate of node 1,x coordinate of node 2, y coordinate of node 2
* Output: distance between the two nodes
* Logic: makes use of distance formula
* Example Call: distance(1,2,3,4)
'''
    
def distance(a,b,c,d):
    distance=math.sqrt(((c-a)**2)+((d-b)**2))
    return distance





cell_nodes={                #cell_nodes is a dictonary in which each cell has nodes in cyclic order
      1: [1,2,5,10,9,4],
      2: [3,4,9,15,14,8],
      3: [9,10,16,22,21,15],
      4: [5,6,11,17,16,10],
      5: [7,8,14,20,19,13],
      6: [14,15,21,27,26,20],
      7: [21,22,28,34,33,27],
      8: [16,17,23,29,28,22],
      9: [11,12,18,24,23,17],
      10:[19,20,26,32,31,25],
      11:[26,27,33,39,38,32],
      12:[33,34,40,46,45,39],
      13:[28,29,35,41,40,34],
      14:[23,24,30,36,35,29],
      15:[31,32,38,44,43,37],
      16:[38,39,45,50,49,44],
      17:[45,46,51,54,53,50],
      18:[40,41,47,52,51,46],
      19:[35,36,42,48,49,41]
 }
x=9.5
y=8.5
z=4.75
node_coordinates={  #node coordinates is a dictionary of nodes and its coordinates with center as the origin
    1:(-z,5*y),
    2:(z,5*y),
    3:(-3*x,4*y),
    4:(-x,4*y),
    5:(3*x,4*y),
    6:(x,4*y),
    7:(-5*z,3*y),
    8:(-3*z,3*y),
    9:(-z,3*y),
    10:(z,3*y),
    11:(3*z,3*y),
    12:(5*z,3*y),
    13:(-5*x,2*y),
    14:(-3*x,2*y),
    15:(-x,2*y),
    16:(x,2*y),
    17:(3*x,2*y),
    18:(5*x,2*y),
    19:(-5*z,y),
    20:(-3*z,y),
    21:(-z,y),
    22:(z,y),
    23:(3*z,y),
    24:(5*z,y),
    25:(-5*x,0),
    26:(-3*x,0),
    27:(-x,0),
    28:(x,0),
    29:(3*x,0),
    30:(5*x,0),
    31:(-5*z,-y),
    32:(-3*z,-y),
    33:(-z,-y),
    34:(z,-y),
    35:(3*z,-y),
    36:(5*z,-y),
    37:(-5*x,-2*y),
    38:(-3*x,-2*y),
    39:(-x,-2*y),
    40:(x,-2*y),
    41:(3*x,-2*y),
    42:(5*x,-2*y),
    43:(-5*z,-3*y),
    44:(-3*z,-3*y),
    45:(-z,-3*y),
    46:(z,-3*y),
    47:(3*z,-3*y),
    48:(5*z,-3*y),
    49:(-3*x,-4*y),
    50:(-x,-4*y),
    51:(3*x,-4*y),
    52:(x,-4*y),
    53:(-z,-5*y),
    54:(z,-5*y),
    }
arena_config = {0: ('Water Pitcher', 6, '2-2'),2:('Pebble',8, '3-3'),4:('Pebble',16, '2-2'),6:('Pebble',19, '1-1')
                }#the initial configaration
Robot_start = 'START-1'
if(Robot_start== "START-1"):  #defines the startng node from the arena_config
    start_node=25
if( Robot_start== "START-2"):
    start_node=30
    
pebblenodes=list()

waterpitchernodes=list()

for _,v in arena_config.items():
    if(v[0]=="Pebble"):
        if(v[2]=="1-1"):
            pebblenodes.append(list((cell_nodes[v[1]][2],cell_nodes[v[1]][5])) )#getting nodes from cell_nodes dictionary
        if(v[2]=="2-2"):
            pebblenodes.append(list((cell_nodes[v[1]][0],cell_nodes[v[1]][3])))
        if(v[2]=="3-3"):
            pebblenodes.append(list((cell_nodes[v[1]][1],cell_nodes[v[1]][4])))
for _,v in arena_config.items():
    if(v[0]=="Water Pitcher"):
        if(v[2]=="1-1"):
            waterpitchernodes=list((cell_nodes[v[1]][2],cell_nodes[v[1]][5])) #getting nodes from cell_nodes dictionary
        if(v[2]=="2-2"):
            waterpitchernodes=list((cell_nodes[v[1]][0],cell_nodes[v[1]][3]))
        if(v[2]=="3-3"):
            waterpitchernodes=list((cell_nodes[v[1]][1],cell_nodes[v[1]][4]))
print(pebblenodes)            
    


#print(target_pebble_node)
#print(target_waterpitcher_node)

'''
    * Function Name:shortest_distance
    * Input: starting node,list conataiing two opposite nodes of destinatiom
    * Output:distination node
    * Logic:Compares the distace between the starting node and both nodes and gives the destination node with
            minimum distance
    * Example Call:shortest_distance(25,[5,10])
'''
def shortest_distance(start_node,dest_list_nodes):
   
    start_x_node=node_coordinates[start_node][0]
    start_y_node=node_coordinates[start_node][1]
    dist_one_x_node=node_coordinates[dest_list_nodes[0]][0]
    dist_one_y_node=node_coordinates[dest_list_nodes[0]][1]
    dist_two_x_node=node_coordinates[dest_list_nodes[1]][0]
    dist_two_y_node=node_coordinates[dest_list_nodes[1]][1]
    
    distanceone=distance(start_x_node,start_y_node,dist_one_x_node,dist_one_y_node)
    distancetwo=distance(start_x_node,start_y_node,dist_two_x_node,dist_two_y_node)
    if(distanceone<distancetwo):
        return dest_list_nodes[0]
    else:
        return dest_list_nodes[1]
        

target_pebble_node=shortest_distance(start_node,pebblenodes[0])
print(target_pebble_node)
target_water_pitcher_node=shortest_distance(target_pebble_node,waterpitchernodes)
for i in  range(2):
    if(waterpitchernodes[i]==target_water_pitcher_node):
        if(i==0):
            target_opp_wp_node=waterpitchernodes[1]
        else:    
            target_opp_wp_node=waterpitchernodes[0]
    




'''
    * Function Name:route
    * Input: path of list of nodes returned by dijkstra
    * Output: string with collection of l-left,r-right characters
    * Logic:compares the posiiton among neighbours and gives the left or right direction to the final path
    * Example Call:route(path) where path is a list of nodes
''' 




def route(pathf):
    global counter
    route=[]
    cell_matrix=[                          #nested list containg the position of each node in the arena
       
    [0 ,0 ,0 ,0 ,0 ,1 ,2 ,0 ,0 ,0 ,0 ,0 ],
    [0 ,0 ,0 ,3 ,4 ,0 ,0 ,5 ,6 ,0 ,0 ,0 ],
    [0 ,7 ,8 ,0 ,0 ,9 ,10,0 ,0 ,11,12,0 ],
    [13,0 ,0 ,14,15,0 ,0 ,16,17,0 ,0 ,18],
    [0 ,19,20,0 ,0 ,21,22,0 ,0 ,23,24,0 ],
    [25,0 ,0 ,26,27,0 ,0 ,28,29,0 ,0 ,30],
    [0 ,31,32,0 ,0 ,33,34,0 ,0 ,35,36,0 ],
    [37,0 ,0 ,38,39,0 ,0 ,40,41,0 ,0 ,42],
    [0 ,43,44,0 ,0 ,45,46,0 ,0 ,47,48,0 ],
    [0 ,0 ,0 ,49,50,0 ,0 ,51,52,0 ,0 ,0 ],
    [0 ,0 ,0 ,0 ,0 ,53,54,0 ,0 ,0 ,0 ,0 ]]

    

    

    for i in range (len(pathf)-2):
          nodeone=int(pathf[i])
          nodetwo=int(pathf[i+1])
          nodethree=int(pathf[i+2])
          for j in range(11):
            for k in range(12):
                if nodeone==cell_matrix[j][k]:
                    firstnode=list((j,k)) #gets the current node in the loop from the list
                if nodetwo==cell_matrix[j][k]:
                    secondnode=list((j,k))#gets the node next to the current node in the loop
                if nodethree==cell_matrix[j][k]:
                    thirdnode=list((j,k))# gets the second nect node from the current node in loop
                    
        #compares the position of all these three nodes relatively in arena and append l or r to the route
          if(firstnode==thirdnode):
              route.append("0")
          else:    
              if((secondnode[0]==thirdnode[0]) and (firstnode[0]==secondnode[0]+1) and (firstnode[1]+1==secondnode[1])and
               (secondnode[1]+1==thirdnode[1])):
                route.append("r")
              if((secondnode[0]+1==thirdnode[0]) and (firstnode[0]==secondnode[0]) and (firstnode[1]+1==secondnode[1])and
               (secondnode[1]+1==thirdnode[1])):
                route.append("r")
              if((secondnode[0]+1==thirdnode[0]) and (firstnode[0]+1==secondnode[0]) and (firstnode[1]+1==secondnode[1])and
               (secondnode[1]==thirdnode[1]+1)):
                route.append("r")
              if((secondnode[0]==thirdnode[0]+1) and (firstnode[0]==secondnode[0]) and (firstnode[1]+1==secondnode[1])and
               (secondnode[1]+1==thirdnode[1])):
                route.append("l")
              if((secondnode[0]==thirdnode[0]) and (firstnode[0]+1==secondnode[0]) and (firstnode[1]+1==secondnode[1])and
               (secondnode[1]+1==thirdnode[1])):
                route.append("l")
              if((secondnode[0]+1==thirdnode[0]) and (firstnode[0]+1==secondnode[0]) and (firstnode[1]==secondnode[1]+1)and
               (secondnode[1]+1==thirdnode[1])):
                route.append("l")

                
              if((secondnode[0]==firstnode[0]) and (thirdnode[0]==secondnode[0]+1) and (thirdnode[1]+1==secondnode[1])and
               (secondnode[1]+1==firstnode[1])):
                route.append("l")

              if((secondnode[0]+1==firstnode[0]) and (thirdnode[0]==secondnode[0]) and (thirdnode[1]+1==secondnode[1])and
               (secondnode[1]+1==firstnode[1])):
                route.append("l")
                

              if((secondnode[0]+1==firstnode[0]) and (thirdnode[0]+1==secondnode[0]) and (thirdnode[1]+1==secondnode[1])and
               (secondnode[1]==firstnode[1]+1)):
                route.append("l")

              if((secondnode[0]==firstnode[0]+1) and (thirdnode[0]==secondnode[0]) and (thirdnode[1]+1==secondnode[1])and
               (secondnode[1]+1==firstnode[1])):
                route.append("r")
                
              if((secondnode[0]==firstnode[0]) and (thirdnode[0]+1==secondnode[0]) and (thirdnode[1]+1==secondnode[1])and
               (secondnode[1]+1==firstnode[1])):
                route.append("r")
              if((secondnode[0]+1==firstnode[0]) and (thirdnode[0]+1==secondnode[0]) and (thirdnode[1]==secondnode[1]+1)and
               (secondnode[1]+1==firstnode[1])):
                route.append("r")
    lastsecondnode=int(pathf[-1])
    lastthirdnode=int(pathf[-2])
    lastnode=""    
    for i in range(len(pebblenodes)):
            if(pebblenodes[i][0]==int(pathf[-1])):
               lastnode=pebblenodes[i][1]
             
               break;
            elif(pebblenodes[i][1]==int(pathf[-1])):
               lastnode=pebblenodes[i][0]
               
               break;
    if(lastnode==""):
        lastnode=target_opp_wp_node
       
    for j in range(11):
            for k in range(12):
                if lastthirdnode==cell_matrix[j][k]:
                    firstnode=list((j,k)) #gets the current node in the loop from the list
                if lastsecondnode==cell_matrix[j][k]:
                    secondnode=list((j,k))#gets the node next to the current node in the loop
                if lastnode==cell_matrix[j][k]:
                    thirdnode=list((j,k))# gets the second nect node from the current node in loop
    
    print(firstnode,secondnode,thirdnode)
    if((((firstnode[0]==secondnode[0]==thirdnode[0]+2)
       and((firstnode[1]+1==secondnode[1]==thirdnode[1]+1))))or
       (((firstnode[0]==secondnode[0]+1==thirdnode[0]+2)
       and((firstnode[1]+1==secondnode[1]==thirdnode[1]+2))))or
       (((firstnode[0]+1==secondnode[0]+2==thirdnode[0])
       and((firstnode[1]==secondnode[1]+1==thirdnode[1]+2))))or
       (((firstnode[0]+2==secondnode[0]+2==thirdnode[0])
       and((firstnode[1]==secondnode[1]+1==thirdnode[1]))))or
       (((firstnode[0]+1==secondnode[0]==thirdnode[0])
       and((firstnode[1]+2==secondnode[1]+3==thirdnode[1]))))or
       (((firstnode[0]+1==secondnode[0]==thirdnode[0]+2)
       and((firstnode[1]+2==secondnode[1]+1==thirdnode[1]))))):
            route.append("i")
            turn_direction="i"#left turn
            
        
    elif((((firstnode[0]==secondnode[0]==thirdnode[0]+2)
       and((firstnode[1]==secondnode[1]+1==thirdnode[1]))))or
       (((firstnode[0]==secondnode[0]+1==thirdnode[0]+2)
       and((firstnode[1]+2==secondnode[1]+3==thirdnode[1]))))or
       (((firstnode[0]+1==secondnode[0]+2==thirdnode[0])
       and((firstnode[1]+2==secondnode[1]+1==thirdnode[1]))))or
       (((firstnode[0]+2==secondnode[0]+2==thirdnode[0])
       and((firstnode[1]+1==secondnode[1]==thirdnode[1]))))or
       (((firstnode[0]+1==secondnode[0]==thirdnode[0])
       and((firstnode[1]+1==secondnode[1]==thirdnode[1]+3))))or
       (((firstnode[0]+1==secondnode[0]==thirdnode[0]+2)
       and((firstnode[1]==secondnode[1]+1==thirdnode[1]+2))))):
            route.append("j")
            turn_direction="j"#right turn
    else:
            route.append("k")
            turn_direction="k"#straight turn
    if(counter%2==0):
            route.append("m")
    else:
            route.append("d")
    counter=counter+1


    if(turn_direction=="i"):
        route.append("f")#retrace the steps to the node
    elif(turn_direction=="j"):
        route.append("g")#retrace the steps to the node
    elif(turn_direction=="k"):
        route.append("h")#retrace the steps to the node
                    
                        
     
    
       
        
        
                    








                    

    
    route1="".join(route);#convers the route list to a string
    #print(route1)
    return(route1) #returns the command string 
g = DirectedGraph()#defining neighbours for the dijkstra function note thst all the weights are the same
g.connect('2', '1', 8)
g.connect('5', '2', 8)
g.connect('10', '5',8)
g.connect('9', '10',8)
g.connect('4', '9', 8)
g.connect('1', '4', 8)
g.connect('15', '9',8)
g.connect('14', '15',8)
g.connect('8', '14', 8)
g.connect('3', '8', 8)
g.connect('16', '10', 8)
g.connect('22', '16', 8)
g.connect('21', '22',8)
g.connect('15', '21',8)
g.connect('6', '5', 8)
g.connect('11', '6', 8)
g.connect('17', '11',8)
g.connect('16', '17',8)
g.connect('12', '11', 8)
g.connect('18', '12', 8)
g.connect('24', '18', 8)
g.connect('23', '24', 8)
g.connect('17', '23',8)
g.connect('8', '7',8)
g.connect('20', '14', 8)
g.connect('19', '20', 8)
g.connect('13', '19',8)
g.connect('7', '13',8)
g.connect('27', '21', 8)
g.connect('26', '27', 8)
g.connect('20', '26',8)
g.connect('29', '23',8)
g.connect('28', '29', 8)
g.connect('22', '28', 8)
g.connect('32', '26', 8)
g.connect('31', '32', 8)
g.connect('25', '31',8)
g.connect('19', '25',8)
g.connect('34', '28', 8)
g.connect('33', '34', 8)
g.connect('27', '33',8)
g.connect('4', '3',8)
g.connect('30', '24', 8)
g.connect('36', '30', 8)
g.connect('35', '36',8)
g.connect('29', '35',8)
g.connect('39', '33', 8)
g.connect('38', '39', 8)
g.connect('32', '38',8)
g.connect('40', '34', 8)
g.connect('46', '40', 8)
g.connect('45', '46',8)
g.connect('39', '45',8)
g.connect('41', '35', 8)
g.connect('40', '41', 8)
g.connect('44', '38', 8)
g.connect('43', '44', 8)
g.connect('37', '43',8)
g.connect('31', '37',8)
g.connect('50', '45', 8)
g.connect('49', '50', 8)
g.connect('44', '49',8)
g.connect('51', '46', 8)
g.connect('54', '51', 8)
g.connect('53', '54',8)
g.connect('50', '53',8)
g.connect('47', '41', 8)
g.connect('52', '47', 8)
g.connect('51', '52',8)
g.connect('42', '36', 8)
g.connect('48', '42', 8)
g.connect('47', '48',8)
g.connect('1', '2', 8)
g.connect('2', '5', 8)
g.connect('5', '10',8)
g.connect('10', '9',8)
g.connect('9', '4', 8)
g.connect('4', '1', 8)
g.connect('9', '15',8)
g.connect('15', '14',8)
g.connect('14', '8', 8)
g.connect('8', '3', 8)
g.connect('10', '16', 8)
g.connect('16', '22', 8)
g.connect('22', '21',8)
g.connect('21', '15',8)
g.connect('5', '6', 8)
g.connect('6', '11', 8)
g.connect('11', '17',8)
g.connect('17', '16',8)
g.connect('11', '12', 8)
g.connect('12', '18', 8)
g.connect('18', '24', 8)
g.connect('24', '23', 8)
g.connect('23', '17',8)
g.connect('7', '8',8)
g.connect('14', '20', 8)
g.connect('20', '19', 8)
g.connect('19', '13',8)
g.connect('13', '7',8)
g.connect('21', '27', 8)
g.connect('27', '26', 8)
g.connect('26', '20',8)
g.connect('23', '29',8)
g.connect('29', '28', 8)
g.connect('28', '22', 8)
g.connect('26', '32', 8)
g.connect('32', '31', 8)
g.connect('31', '25',8)
g.connect('25', '19',8)
g.connect('28', '34', 8)
g.connect('34', '33', 8)
g.connect('33', '27',8)
g.connect('24', '30', 8)
g.connect('30', '36', 8)
g.connect('36', '35',8)
g.connect('35', '29',8)
g.connect('33', '39', 8)
g.connect('39', '38', 8)
g.connect('38', '32',8)
g.connect('34', '40', 8)
g.connect('40', '46', 8)
g.connect('46', '45',8)
g.connect('45', '39',8)
g.connect('35', '41', 8)
g.connect('41', '40', 8)
g.connect('38', '44', 8)
g.connect('44', '43', 8)
g.connect('43', '37',8)
g.connect('37', '31',8)
g.connect('45', '50', 8)
g.connect('50', '49', 8)
g.connect('49', '44',8)
g.connect('46', '51', 8)
g.connect('51', '54', 8)
g.connect('54', '53',8)
g.connect('53', '50',8)
g.connect('41', '47', 8)
g.connect('47', '52', 8)
g.connect('52', '51',8)
g.connect('36', '42', 8)
g.connect('42', '48', 8)
g.connect('48', '47',8)
'''
pakka code
routeone=g.dijkstras(str(start_node), str(target_pebble_node))#gets the path from start node to pebble node

if(routeone[1]=='19'):
    finalroute="l"#initial turning left or right by comparing the position in the arena
if(routeone[1]=='31'):
    finalroute="r"

if(routeone[1]=='36'):
    finalroute="l"
if(routeone[1]=='24'):
    finalroute="r"
    '''
    
       
        
####routetwo= g.dijkstras(str(target_pebble_node), str(target_waterpitcher_node))
#gets the path from pebble node to water pitcher node
####routetwo.insert(0,routeone[-2])
####finalroute=finalroute+route(routeone)+"b"+route(routetwo)# adding a b in between for the buzzer
####print("the final route is ",finalroute)
#print(start_node,target_pebble_node)
routeone=g.dijkstras(str(start_node),str(target_pebble_node));
route_list=list()
route_list.append(routeone)


if(routeone[1]=='19'):
    finalroute="l"#initial turning left or right by comparing the position in the arena
if(routeone[1]=='31'):
    finalroute="r"

if(routeone[1]=='36'):
    finalroute="l"
if(routeone[1]=='24'):
    finalroute="r"

print(target_water_pitcher_node)    

routetwo=g.dijkstras(str(target_pebble_node),str(target_water_pitcher_node));
routetwo.insert(0,routeone[-2])
route_list.append(routetwo)
finalroute=finalroute+route(routeone)+route(routetwo)
k=1;

for i in range (1,len(pebblenodes)):
    print(shortest_distance(target_water_pitcher_node,pebblenodes[i]))
    
    routeone=g.dijkstras(str(target_water_pitcher_node),str(shortest_distance(target_water_pitcher_node,pebblenodes[i])));
    routeone.insert(0,route_list[k][-2])
    route_list.append(routeone)
    
    routetwo=g.dijkstras(str(shortest_distance(target_water_pitcher_node,pebblenodes[i])),str(target_water_pitcher_node));
    routetwo.insert(0,routeone[-2])
    route_list.append(routetwo)
    print("final",route_list)
    
    k=k+2
    print(routeone)
    print(routetwo)
  
    finalroute=finalroute+route(routeone)+route(routetwo)       



finalroute=finalroute+"b"

print(finalroute)



 




'''
    * Function Name: loop
    * Input: 
    * Output:
    * Logic: this function runs in an infinite loop giving commands to the microcontroller one by one
    note that it gives one charcter to the atmega at one time
    * Example Call: loop()
'''  


def loop():
        ser = serial.Serial("COM3", 9600,timeout=1)#initializes the serial function for serial communication
        _= input("Enter any key to start the robot ")#when the atmega is turned we can press any key to start

        j=0
        count=0
        while True:#infinite loop starts
            
            
            ########## ENTER YOUR CODE HERE ############
            character=ser.read()#it reads character
            if(character.decode()=='.'):#whenever it recieves a '.' from atmega it tranmits one charcter at a time
                if(j<len(finalroute)):
                    
                    print("Transmitting",character)
                    ser.write((finalroute[j]).encode())#transmiting character
                    if(finalroute[j]=='b'):
                        find_object("low","half")#calls a function from GLteapot.py for updating aruco object
                        #when robot reaches the pebble
                    
                    
                    j=j+1
                    
                
                    
                    
                else:
                    find_object("high","half")
                    #calls a function from GLteapot.py for updating texture file for water pitcher
                        #when robot reaches the  water pitcher
            
               
                    
                    
               
                
#Thread(target = main).start()#uses multithreading concept to run two functions at a time

#NOTE THAT main() is from GLteapot.py
Thread(target = loop).start()
                  
                
            
                
               
            
          







