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

route=[]
nodeslist=[13,7,8,15,21,22,2,1,1]
poscurrent=[5,0]
posnext=[0,0]
for i in range (0,len(nodeslist)-1):
    currentnode=nodeslist[i]
    nextnode=nodeslist[i+1]
    for j in range(11):
        for k in range(12):
            if currentnode==cell_matrix[j][k]:
                poscurrent=list((j,k))
            if nextnode==cell_matrix[j][k]:
                posnext=list((j,k))

    if posnext[0]==poscurrent[0]-1 and posnext[1]==poscurrent[1]+1:
            route.append("left")
    if posnext[0]==poscurrent[0] and posnext[1]==poscurrent[1]+1:
            route.append("right")
    if posnext[0]==poscurrent[0]+1 and posnext[1]==poscurrent[1]+1:
            route.append("right")
    if posnext[0]==poscurrent[0]+1 and posnext[1]==poscurrent[1]-1:
            route.append("right")
    if posnext[0]==poscurrent[0] and posnext[1]==poscurrent[1]-1:
            route.append("right")
    if posnext[0]==poscurrent[0]-1 and posnext[1]==poscurrent[1]-1:
            route.append("right")
