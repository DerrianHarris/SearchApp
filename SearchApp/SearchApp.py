import pygame
import pygame.locals as Locals
import random
import math
import time
import colorsys
#import winsound


# Variables
FULLSCREEN = False

window_size = (500,500)
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



def doRender():
    global cachedText
    window.fill((0,0,0))
    
    drawRect = pygame.draw.rect
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
        sorterText = "Current Searcher: "
    elif(searchType == 3):
        sorterText = "Current Searcher: "
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
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_RETURN:
            doSearch = True
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_ESCAPE:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_r:
            ResetCells(CellValues)
            Start_Pos = (-1,-1)
            End_Pos = (-1,-1)


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

def doLogic():
    global doSearch
    if doSearch:
        path = []
        if(searchType == 0):
            path = Dijkstra(CellValues,Start_Pos,End_Pos)
        elif(searchType == 1):
            path = DFS(CellValues,Start_Pos,End_Pos)
        HighlightPath(CellValues,Start_Pos, End_Pos, path)
        doSearch = False

def DFS(Graph, Start, End):
    path = []
    Visited = [False] * (len(Graph)) 
    DFSHelper(Graph,Start,End,Visited,path)
    return path

def DFSHelper(Graph, Curr, End, Visited, Path):
    Visited[PosToIndex(Curr)] = True
    for Neighbor in GetNeighbors(Curr):
        index = PosToIndex(Neighbor)
        if Visited[index] == False:
                if(End == Neighbor):
                    return Neighbor
                Path.append(DFSHelper(Graph,Neighbor,End,Visited,Path))


def Dijkstra(Graph, Start, End):
    timer = 0
    Q = [0] * len(Graph) # Vertex Set
    dist = [float(math.inf)] * len(Graph) # Distance set
    prev = [None] * len(Graph) # Prev Index List

    for index in range(len(Graph)):
        Q[index] = IndexToPos(index)
    dist[PosToIndex(Start)] = 0

    while len(Q) > 0:
        uIndex = minDistance(dist,Q)
        u = IndexToPos(uIndex)
        try:
            Q.remove(u)
        except:
            break

        if( not (u  == Start) and not (u == End) and not isWall(CellValues,uIndex)):
                Graph[uIndex] = 5

        if u == End:
            break
       
        for v in GetNeighbors(u):
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

def minDistance(dist,Q):
    min = float(math.inf)
    minIndex = 0

    for index in range(len(dist)):
        if(dist[index] < min and IndexToPos(index) in Q):
            minIndex = index
            min = dist[index]
    return minIndex

def GetNeighbors(pos):
    Neighbors = []
    for x in range(-1,2):
        for y in range(-1,2):
            if(x == 0 and y == 0):
                continue

            neighborPos = (pos[0] + x, pos[1]+ y)

            if length(pos, neighborPos) == 14 and not useDiag:
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

def ResetCells(Graph):
    for i in range(len(Graph)):
        Graph[i] = 0

while run:
    doEvent()
    doLogic()
    doRender()
pygame.quit()
try:
    exit()
except:
    print("An exception occurred.")
