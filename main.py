import sys
import pygame
from pygame.locals import *


pygame.init()

size = [1024,768]
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("Some bullshit")

clock = pygame.time.Clock()
done = False


# Declare map
mapCellOnColor = [0,0,0]
mapCellOffColor = [255,255,255]
mapCellSize = 10
mapPos = [200,100]
mapCurrentBuffer = 0
mapBackBuffer = 1-mapCurrentBuffer
mapWidth = 10
mapHeight = 10
# Map of [mapHeight][mapWidth] size, with a 2nd buffer of same size for calculating next step
mapCells = [[[0 for x in range(mapWidth)] for y in range(mapHeight)] for i in range(2) ]

for y in range(0,10):
    for x in range(0,10):
        #print("");
        mapCells[1][y][x] = x + (y*10)
        sys.stdout.write(str(mapCells[0][y][x]))
    sys.stdout.write('\n')

while done == False:
    screen.fill((20,0,100))
    #pygame.draw.rect(screen, (255,255,255), (100,100,300,300))

    for y in range(0, 10):
        yCur = mapPos[1] + (y*mapCellSize)
        for x in range(0, 10):
            xCur = mapPos[0] + (x*mapCellSize)
            print(xCur , ", " , yCur)



    # Event handling
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            #print("Quitting...")
            done = True
        elif event.type == pygame.MOUSEMOTION:
            #print("Mouse moved")
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print("Mouse down")
            pass
        elif event.type == pygame.MOUSEBUTTONUP:
            #print("Mouse up")
            pass
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or pygame.K_ESCAPE:
                done = True;
        else:
            print(event)



    # Updates
    pygame.display.update()
    clock.tick(20)

print("Exited")