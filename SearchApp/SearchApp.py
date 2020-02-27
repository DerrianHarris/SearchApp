import pygame
import pygame.locals as Locals
import random
import math
import colorsys
#import winsound


# Variables
FULLSCREEN = False
window_size = (1000,1000)
Cell_Size = 20



CellValues = [0]


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




font = pygame.font.SysFont("comicsansms",30)
cachedText = {}



def doRender():
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

            rect = (x* Cell_Size,Cell_Start - (y*Cell_Size),Cell_Size-0.5,Cell_Size-0.5)
            cell = drawRect(window,Color,rect)
            

    
    sorterText = ""

    global searchType
    if(searchType == 0):
        sorterText = "Current Sorter: Selection Sort"
    elif(searchType == 1):
        sorterText = "Current Sorter: Insertion Sort"
    elif(searchType == 2):
        sorterText = "Current Sorter: Bubble Sort"
    elif(searchType == 3):
        sorterText = "Current Sorter: Merge Sort"
    elif(searchType == 4):
        sorterText = "Current Sorter: Quick Sort"
    elif(searchType == 5):
        sorterText = "Current Sorter: Heap Sort"
    elif(searchType == 6):
        sorterText = "Current Sorter: Shell Sort"
    global font
    global cachedText
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



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:        
            x,y = (event.pos[0],(Height-1) - event.pos[1] - (Height_Padding - Cell_Size))

            if y <= Cell_Start and y >= 0: 
                print ("You pressed the left mouse button at (%d, %d)" % (x,y))
                cellPos = (math.floor(x/Cell_Size),math.floor(y/Cell_Size))
                CycleCellValue(CellValues,PosToIndex(cellPos))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            
            x,y = (event.pos[0],(Height-1) - event.pos[1] - (Height_Padding - Cell_Size))

            if y <= Cell_Start and y >= 0: 
                print ("You pressed the left mouse button at (%d, %d)" % (x,y))
                cellPos = (math.floor(x/Cell_Size),math.floor(y/Cell_Size))
                CycleCellValue(CellValues,PosToIndex(cellPos),-1)
        elif event.type == pygame.KEYDOWN and event.key == Locals.K_ESCAPE:
            run = False


def PosToIndex(pos):
    return pos[0] * Num_Cells_Y + pos[1]

def CycleCellValue(arr,index, inc = 1):
    arr[index] = (arr[index] + inc)

    if(arr[index] < 0):
        arr[index] = MaxCellValue - 1
    elif(arr[index] >= MaxCellValue):
        arr[index] = 0

def doLogic():
    pass
while run:
    doEvent()
    doLogic()
    doRender()
pygame.quit()
try:
    exit()
except:
    print("An exception occurred.")
