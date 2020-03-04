import pygame
import pygame.locals as Locals
import random
import math
import time
import colorsys
from collections import deque
#import winsound


# Variables
FULLSCREEN = False

window_size = (1000,500)
Cell_Size = 20



CellValues = [0]
Start_Pos = (-1,-1)
End_Pos = (-1,-1)

pygame.init()
if FULLSCREEN:
    window = pygame.display.set_mode(flags = pygame.FULLSCREEN)
else:
    window = pygame.display.set_mode(window_size)

pygame.display.set_caption("Search App")

Width,Height= pygame.display.get_surface().get_size()

Height_Padding = 100
Cell_Start = (Height - Height_Padding)

Text_Pos = (math.floor(Width/2),(Height - math.floor((Height_Padding/2))))

run = True
searchType = 0
doSearch = False
useDiag = False
showPos = False

Num_Cells_X = math.floor(Width/Cell_Size)
Num_Cells_Y = math.floor(Cell_Start/Cell_Size)
CellValues = [0] * (Num_Cells_X * Num_Cells_Y)
MaxCellValue = 4
# 0 - Open cell
# 1 - Start Cell
# 2 - End Cell
# 3 - Wall Cell
# 4 - Path Cell
# 5 - Visited Cell
# 6 - Test cell



font = pygame.font.SysFont("comicsansms",30)
fontIndex = pygame.font.SysFont("comicsansms",5)

cachedText = {}

drawRect = pygame.draw.rect

def doRender():
    global cachedText
    window.fill((0,0,0))
    
    
    for x in range(Num_Cells_X):
        for y in range(Num_Cells_Y):
            if CellValues[PosToIndex((x,y))] == 0:    
                Color = (200,200,200)
            elif CellValues[PosToIndex((x,y))] == 1:
                Color = (0,255,0)
            elif CellValues[PosToIndex((x,y))] == 2:
                Color = (0,0,255)
            elif CellValues[PosToIndex((x,y))] == 3:
                Color = (20,20,20)
            elif CellValues[PosToIndex((x,y))] == 4:
                Color = (92, 64, 87)
            elif CellValues[PosToIndex((x,y))] == 5:
                Color = (255,0,0)
            elif CellValues[PosToIndex((x,y))] == 6:
                Color = (255,255,0)

            rect = (x* Cell_Size,Cell_Start - (y*Cell_Size),Cell_Size-0.5,Cell_Size-0.5)
            cell = drawRect(window,Color,rect)

            if (not doSearch) and (x,y) in path:
                index = path.index((x,y))
                if not index == 0:
                    
                    diff = (x - path[index-1][0],y - path[index-1][1])
                    anlgeRad =  math.atan2(diff[0],diff[1]) + math.pi/2
                    anlgeDeg = math.degrees(anlgeRad)

                    pointList = [cell.topright,cell.midleft,cell.bottomright]

                    if anlgeDeg == 0:
                        pointList = [cell.topleft,cell.midright,cell.bottomleft]
                    elif anlgeDeg == 90:
                        pointList = [cell.topleft,cell.midbottom,cell.topright]
                    elif anlgeDeg == 180:
                        pointList = [cell.topright,cell.midleft,cell.bottomright]
                    elif anlgeDeg == 270:
                        pointList = [cell.bottomleft,cell.midtop,cell.bottomright]
                    elif anlgeDeg == 45:
                        pointList = [cell.midleft,cell.bottomright,cell.midtop]
                    elif anlgeDeg == 135:
                        pointList = [cell.midright,cell.bottomleft,cell.midtop]
                    elif anlgeDeg == -45:
                        pointList = [cell.midleft,cell.topright,cell.midbottom]
                    elif anlgeDeg == 225:
                        pointList = [cell.midright,cell.topleft,cell.midbottom]

                    #print(anlgeDeg)

                    triangle = pygame.draw.polygon(window,(0,0,0),pointList)
                    triangle = pygame.transform.rotate(window,anlgeDeg)
          
            if showPos:
                if PosToIndex((x,y)) + 7 not in cachedText:
                   cachedText[PosToIndex((x,y)) + 7] = fontIndex.render(str(IndexToPos(PosToIndex((x,y)))),True,(0,0,0))
                text = cachedText[PosToIndex((x,y)) + 7]
                textRect = text.get_rect()
                textRect.center = cell.center
                pygame.display.get_surface().blit(text,textRect)
            
    

    sorterText = ""

    if(searchType == 0):
        sorterText = "Current Searcher: Dijkstra"
    elif(searchType == 1):
        sorterText = "Current Searcher: DFS"
    elif(searchType == 2):
        sorterText = "Current Searcher: BFS"
    elif(searchType == 3):
        sorterText = "Current Searcher: A*"
    elif(searchType == 4):
        sorterText = "Current Searcher: "
    elif(searchType == 5):
        sorterText = "Current Searcher: "
    elif(searchType == 6):
        sorterText = "Current Searcher: "
  
    if searchType not in cachedText:
        cachedText[searchType] = font.render(sorterText,True,(200,200,200))
    text = cachedText[searchType]
    textRect = text.get_rect()
    textRect.center = Text_Pos
    pygame.display.get_surface().blit(text,textRect)
    pygame.display.update()


def doEvent():
    global run
    global searchType
    global CellValues
    global doSearch
    global Start_Pos
    global End_Pos
    global searchType
    global path
    global useDiag


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:        
            x,y = (event.pos[0],(Height-1) - event.pos[1] - (Height_Padding - Cell_Size))

            if y <= Cell_Start and y >= 0: 
                
                cellPos = (math.floor(x/Cell_Size),math.floor(y/Cell_Size))
                print ("You pressed the left mouse button at (%d, %d)" % cellPos)
                CycleCellValue(CellValues,PosToIndex(cellPos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            
            x,y = (event.pos[0],(Height-1) - event.pos[1] - (Height_Padding - Cell_Size))

            if y <= Cell_Start and y >= 0: 
                cellPos = (math.floor(x/Cell_Size),math.floor(y/Cell_Size))
                print ("You pressed the right mouse button at (%d, %d)" % cellPos)
                CycleCellValue(CellValues,PosToIndex(cellPos),-1)
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_1:
            searchType = 0
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_2:
            searchType = 1
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_3:
            searchType = 2
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_4:
            searchType = 3
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_RETURN:
            if Start_Pos == (-1,-1) or End_Pos == (-1,-1):
                return

            doSearch = True
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_ESCAPE:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_d:
            useDiag = not useDiag
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_m:
            Start_Pos = (-1,-1)
            End_Pos = (-1,-1)
            path = []
            MazeGen(CellValues)
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_r:
            path = []
            ResetCells(CellValues)
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_c:
            SetAllCells(CellValues,0)
            Start_Pos = (-1,-1)
            End_Pos = (-1,-1)
            path = []


def PosToIndex(pos):
    Index = pos[1] * Num_Cells_X + pos[0]
    return Index

def IndexToPos(index):
    posX = index%Num_Cells_X
    posY = index/Num_Cells_X
    return (int(posX),int(posY))

def CycleCellValue(arr,index, inc = 1):
    val = (arr[index] + inc)
    if(val < 0):
        val = MaxCellValue - 1
    elif(val >= MaxCellValue):
        val = 0
    SetCellValue(arr,index,val,inc)


def SetCellValue(arr, index, val,inc):
    global Start_Pos
    global End_Pos

    if val not in [1,2]:
        if(IndexToPos(index) == Start_Pos):
            Start_Pos = (-1,-1)
        elif (IndexToPos(index) == End_Pos):
            End_Pos = (-1,-1)
        arr[index] = val
    else:
        if (val == 1 and Start_Pos == (-1,-1)):
            arr[index] = val
            Start_Pos = IndexToPos(index)
        elif (val == 2 and End_Pos == (-1,-1)):
            arr[index] = val
            End_Pos = IndexToPos(index)
        else:
            arr[index] = val
            CycleCellValue(arr,index,inc)


path = []
def doLogic():
    global doSearch
    global path

    if doSearch:
        
        path = []
        ResetCells(CellValues)
        if(searchType == 0):
            path = Dijkstra(CellValues,Start_Pos,End_Pos)
        elif(searchType == 1):
            path = DFS(CellValues,Start_Pos,End_Pos)
            path.reverse()
        elif(searchType == 2):
            path = BFS(CellValues,Start_Pos,End_Pos)
        elif(searchType == 3):
            path = A_Star(CellValues,Start_Pos,End_Pos)
        HighlightPath(CellValues,Start_Pos, End_Pos, path)
        doSearch = False

def DFS(Graph, Start, End):
    path = []
    Visited = [False] * (len(Graph)) 
    Stack = [Start]
    while len(Stack) > 0:
        u = Stack.pop()
        uIndex = PosToIndex(u)
        if not Visited[uIndex]:
            Visited[uIndex] = True

            if( not (u  == Start) and not (u == End) and not isWall(CellValues,uIndex)):
                Graph[uIndex] = 5

            path.append(u)

            if(u == End):
                break
            for Neighbor in GetNeighbors(u,useDiag):
                
                nIndex = PosToIndex(Neighbor)

                if isWall(CellValues,nIndex):
                    continue

                if not Visited[nIndex]:
                    Stack.append(Neighbor)
            doRender()

    if not End in path:
        return []
    return path

def A_Star(Graph, Start, End):
    openSet = [Start]
    cameFrom = [None] * (len(Graph))
    gScore = [float(math.inf)] * len(Graph)
    fScore = [float(math.inf)] * len(Graph)

    startIndex = PosToIndex(Start)

    gScore[startIndex] = 0
    fScore[startIndex] = heuristic(Start,End)

    while len(openSet) > 0:
        currentIndex = GetMin(fScore,openSet)
        current = IndexToPos(currentIndex)

        if( not (current  == Start) and not (current == End) and not isWall(CellValues,currentIndex)):
                Graph[currentIndex] = 5
        if current == End:
            break
        openSet.remove(current)
        
        for Neighbor in GetNeighbors(current,useDiag):
            nIndex = PosToIndex(Neighbor)

            if isWall(CellValues,nIndex):
                    continue

            tentative_gScore = gScore[currentIndex] + length(current,Neighbor)
            if tentative_gScore < gScore[nIndex]:
                cameFrom[nIndex] = current
                gScore[nIndex] = tentative_gScore
                fScore[nIndex] = gScore[nIndex] + heuristic(Neighbor,End)
                if not (Neighbor in openSet):
                    openSet.append(Neighbor)
        doRender()

    S = []
    u = End
    uIndex = PosToIndex(u)
    if cameFrom[uIndex] is not None or u == Start:          #Do something only if the vertex is reachable
        while u is not None:                         #Construct the shortest path with a stack S
            uIndex = PosToIndex(u)
            S.append(u)                             #Push the vertex onto the stack
            u = cameFrom[uIndex]

    return S


def heuristic(cell,goal):
    return length(cell,goal)


def BFS(Graph, Start, End):
    Q = deque([Start])
    Visited = [False] * (len(Graph)) 
    prev = [None] * (len(Graph)) 

    Visited[PosToIndex(Start)] = True
    while len(Q) > 0:
        v = Q.popleft()
        vIndex = PosToIndex(v)
        if( not (v  == Start) and not (v == End) and not isWall(CellValues,vIndex)):
            Graph[vIndex] = 5
        path.append(v)
        if(v == End):
            break
        
        for Neighbor in GetNeighbors(v,useDiag):
            nIndex = PosToIndex(Neighbor)
            if isWall(CellValues,nIndex):
                    continue
            if not Visited[nIndex]:
                Visited[nIndex] = True
                prev[nIndex] = v
                Q.append(Neighbor)
        doRender()

    S = []
    u = End
    uIndex = PosToIndex(u)
    if prev[uIndex] is not None or u == Start:          #Do something only if the vertex is reachable
        while u is not None:                         #Construct the shortest path with a stack S
            uIndex = PosToIndex(u)
            S.append(u)                             #Push the vertex onto the stack
            u = prev[uIndex]

    return S

def Dijkstra(Graph, Start, End):
    timer = 0
    Q = [0] * len(Graph) # Vertex Set
    dist = [float(math.inf)] * len(Graph) # Distance set
    prev = [None] * len(Graph) # Prev Index List

    for index in range(len(Graph)):
        Q[index] = IndexToPos(index)
    dist[PosToIndex(Start)] = 0

    while len(Q) > 0:
        uIndex = GetMin(dist,Q)
        u = IndexToPos(uIndex)
        try:
            Q.remove(u)
        except:
            break

        if( not (u  == Start) and not (u == End) and not isWall(CellValues,uIndex)):
                Graph[uIndex] = 5

        if u == End:
            break
       
        for v in GetNeighbors(u,useDiag):
            vIndex = PosToIndex(v)

            if isWall(CellValues,vIndex):
                continue

            alt = dist[uIndex] + length(u,v)

            if(alt < dist[vIndex]):
                dist[vIndex] = alt
                prev[vIndex] = u
        doRender()

    S = []
    u = End
    uIndex = PosToIndex(u)

    if prev[uIndex] is not None or u == Start:          #Do something only if the vertex is reachable
        while u is not None:                         #Construct the shortest path with a stack S
            uIndex = PosToIndex(u)
            S.append(u)                             #Push the vertex onto the stack
            u = prev[uIndex]
            
    return S


def length(a,b):
    return int(math.sqrt( (b[0]- a[0]) * (b[0]- a[0]) + (b[1]- a[1]) * (b[1]- a[1]) ) * 10)

def GetMin(dist,Q):
    min = float(math.inf)
    minIndex = 0

    for v in Q:
        vIndex = PosToIndex(v)
        if(dist[vIndex] < min):
            minIndex = vIndex
            min = dist[vIndex]
    return minIndex

def GetNeighbors(pos, useDiagnal):
    Neighbors = []
    for x in range(-1,2):
        for y in range(-1,2):
            if(x == 0 and y == 0):
                continue

            neighborPos = (pos[0] + x, pos[1]+ y)

            if length(pos, neighborPos) == 14 and not useDiagnal:
                continue

            if(neighborPos[0] >= 0 and neighborPos[1] >= 0 and neighborPos[0] < Num_Cells_X and neighborPos[1] < Num_Cells_Y):
                Neighbors.append(neighborPos)
    return Neighbors

def isWall(Graph,index):
    return Graph[index] == 3
def HighlightPath(Graph, Start, End, Path):
    global CellValues
    for V in Path:
        if( not (V  == Start) and not (V == End)):
            CellValues[PosToIndex(V)] = 4

def SetAllCells(Graph,val):
    
    for i in range(len(Graph)):
        Graph[i] = val

def ResetCells(Graph):
    for i in range(len(Graph)):
        val = Graph[i]
        if val >= MaxCellValue:
            Graph[i] = 0



def MazeGen(Graph):
    SetAllCells(Graph,3)

    StartIndex = random.randint(0,len(Graph)-1)
    Start = IndexToPos(StartIndex)

    Graph[StartIndex] = 0
    Walls = []
    
    Walls.extend(GetNeighbors(Start, False))


    while len(Walls) > 0:
        UV = []
        Wall = random.choice(Walls)
        WallIndex = PosToIndex(Wall)


        Neighbors = GetNeighbors(Wall,False)
        for Neighbor in Neighbors:
            nIndex = PosToIndex(Neighbor)

            diff = (Neighbor[0] - Wall[0],Neighbor[1]- Wall[1])
            opp = (Wall[0]-diff[0],Wall[1]-diff[1])

            if(opp[0] >= 0 and opp[1] >= 0 and opp[0] < Num_Cells_X and opp[1] < Num_Cells_Y) and Graph[nIndex] == 0:
                UV.append(opp)


        if len(UV) == 1:
            Graph[WallIndex] = 0
            uvIndex = PosToIndex(UV[0])
            Graph[uvIndex] = 0
            for Neighbor in GetNeighbors(UV[0], False):
                nIndex = PosToIndex(Neighbor)
                if Graph[nIndex] == 3:
                    Walls.append(Neighbor)
        Walls.remove(Wall)
        doRender()

while run:
    doEvent()
    doLogic()
    doRender()
pygame.quit()
try:
    exit()
except:
    print("An exception occurred.")
