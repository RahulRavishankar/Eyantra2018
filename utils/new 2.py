
from collections import defaultdict
import math
import serial
import time

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
    
        
       
       
class path_plan:
    

        
    def distance(a,b,c,d):
        distance=math.sqrt(((c-a)**2)+((d-b)**2))
        return distance





    cell_nodes={
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
    node_coordinates={
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
    arena_config = {0: ('Water Pitcher', 3, '1-1'), 1:('Pebble',5, '3-3')}
    Robot_start = 'START-1'
    if(Robot_start== "START-1"):
        start_node=25
    if( Robot_start== "START-2"):
        start_node=30
    pebblenodes=dict()
    waterpitchernodes=dict()
    distance_p_node=list()
    distance_w_node=list()
    
    for _,v in arena_config.items():
        if(v[0]=="Pebble"):
            if(v[2]=="1-1"):
                pebblenodes=list((cell_nodes[v[1]][1],cell_nodes[v[1]][4]))
            if(v[2]=="2-2"):
                pebblenodes=list((cell_nodes[v[1]][2],cell_nodes[v[1]][5]))
            if(v[2]=="3-3"):
                pebblenodes=list((cell_nodes[v[1]][0],cell_nodes[v[1]][3]))
    for _,v in arena_config.items():
        if(v[0]=="Water Pitcher"):
            if(v[2]=="1-1"):
                waterpitchernodes=list((cell_nodes[v[1]][1],cell_nodes[v[1]][4]))
            if(v[2]=="2-2"):
                waterpitchernodes=list((cell_nodes[v[1]][2],cell_nodes[v[1]][5]))
            if(v[2]=="3-3"):
                waterpitchernodes=list((cell_nodes[v[1]][0],cell_nodes[v[1]][3]))
    for i in range(2):
        a=node_coordinates[start_node][0]
        b=node_coordinates[start_node][1]
        c=node_coordinates[pebblenodes[i]][0]
        d=node_coordinates[pebblenodes[i]][1]
        distance_p_node.append(distance(a,b,c,d))
        target_pebble_node=pebblenodes[distance_p_node.index(min(distance_p_node))]
    for i in range(2):
        a=node_coordinates[target_pebble_node][0]
        b=node_coordinates[target_pebble_node][1]
        c=node_coordinates[waterpitchernodes[i]][0]
        d=node_coordinates[waterpitchernodes[i]][1]
        distance_w_node.append(distance(a,b,c,d))
        target_waterpitcher_node=waterpitchernodes[distance_w_node.index(min(distance_w_node))]   
        
        


    print(target_pebble_node)
    print(target_waterpitcher_node)
    
        
    


    
    
    



    def route(pathf):
        route=[]
        cell_matrix=[
           
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

        

        print(pathf)

        for i in range (len(pathf)-2):
              nodeone=int(pathf[i])
              nodetwo=int(pathf[i+1])
              nodethree=int(pathf[i+2])
              for j in range(11):
                for k in range(12):
                    if nodeone==cell_matrix[j][k]:
                        firstnode=list((j,k))
                    if nodetwo==cell_matrix[j][k]:
                        secondnode=list((j,k))
                    if nodethree==cell_matrix[j][k]:
                        thirdnode=list((j,k))

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
        
                
       
            
            
                        








                        

        
        route1="".join(route);
        #print(route1)
        return(route1)
    g = DirectedGraph()
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
    routeone=g.dijkstras(str(start_node), str(target_pebble_node))
    if(start_node==25):
        if(routeone[1]=='19'):
            finalroute="l"
        if(routeone[1]=='31'):
            finalroute="r"
            
    routetwo= g.dijkstras(str(target_pebble_node), str(target_waterpitcher_node))
    routetwo.insert(0,routeone[-2])
    finalroute=finalroute+route(routeone)+"b"+route(routetwo)
    print(finalroute)
    
    ##dummy
    finalroute="l"
    ser = serial.Serial("COM3", 9600,timeout=1)
    _= input("Enter any key to start the robot ")
    j=0
    while True:
        
        ########## ENTER YOUR CODE HERE ############
        
        
        
        
        character=ser.read()
        if(character.decode()=='.'):
            if(j<len(finalroute)):
                print("yes",character)
                ser.write((finalroute[j]).encode())
                j=j+1
        else:
            print("no",character)
            ser.write(("").encode())