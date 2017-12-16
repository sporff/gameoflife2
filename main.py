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
mapWidth = 10
mapHeight = 10
mapCells = [[0 for x in range(mapWidth)] for y in range(mapHeight)]
print(mapCells[0][0])
for y in range(0,10):
    for x in range(0,10):
        mapCells[y][x] = x + (y*10)
        sys.stdout.write(str(mapCells[y][x]))
    sys.stdout.write('\n')

while done == False:
    screen.fill((20,0,100))

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