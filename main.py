import sys
import pygame
from random import randint
from pygame.locals import *



class GOLmap:
    _mapCellOnColor = None
    _mapCellOffColor = None
    _mapCellSize = 0
    _mapPos = None
    _mapCurrentBuffer = 0
    _mapBackBuffer = 0
    _mapWidth = 0
    _mapHeight = 0
    # Map of [mapHeight][mapWidth] size, with a 2nd buffer of same size for calculating next step
    _mapCells = None



    def __init__(self):
        self.Init(80,80,10)

    def Init(self, mapWidth=10, mapHeight=10, mapCellSize=10, mapPosX=50, mapPosY=50):

        self._mapCellOnColor = [0, 0, 0]
        self._mapCellOffColor = [255, 255, 255]
        self._mapCellSize = mapCellSize
        self._mapPos = [mapPosX, mapPosY]
        self._mapCurrentBuffer = 0
        self._mapBackBuffer = 1 - self._mapCurrentBuffer
        self._mapWidth = mapWidth
        self._mapHeight = mapHeight


        self._mapCells = [[[0 for x in range(self._mapWidth)] for y in range(self._mapHeight)] for i in range(2)]

        for y in range(0, self._mapHeight):
            for x in range(0, self._mapWidth):
                # print("");
                self._mapCells[0][y][x] = randint(0, 1)
                # sys.stdout.write(str(mapCells[0][y][x]))
            sys.stdout.write('\n')




    def DrawMap(self, surface):
        # Draw Map
        for y in range(0, self._mapHeight):
            yCur = self._mapPos[1] + (y * self._mapCellSize)
            for x in range(0, self._mapWidth):
                xCur = self._mapPos[0] + (x * self._mapCellSize)

                if self._mapCells[self._mapCurrentBuffer][y][x] == 0:
                    pygame.draw.rect(surface, self._mapCellOffColor, (xCur, yCur, self._mapCellSize, self._mapCellSize))
                else:
                    pygame.draw.rect(surface, self._mapCellOnColor, (xCur, yCur, self._mapCellSize, self._mapCellSize))




    def IsCellInBounds(self, x,y):
        if (x >= 0 and x < self._mapWidth and y >= 0 and y < self._mapHeight):
            return True

        return False


    def GetLiveNeighborCount(self, x, y):
        # 4 == Current Cell.  Skip
        # 0 1 2
        # 3 4 5
        # 6 7 8
        liveNeighbors = 0

        px = x-1; py = y-1;
        xCount = 0

        #loop through 0-9
        #if i == 4, skip
        #if xCount > 2, xCount = 0, px = x-1, py += 1

        for i in range(0,9):
            print("Index: ", i, " # ", px, ", ", py )
            if i != 4:
                if self.IsCellInBounds(px, py) == True:
                    if (self._mapCells[self._mapCurrentBuffer][py][px] == 1):
                        liveNeighbors += 1

            px += 1
            xCount += 1
            if xCount > 2:
                xCount = 0
                px = x-1
                py += 1


        print("****************************")
        return liveNeighbors





    def UpdateBackBuffer(self):
        for y in range(0, self._mapHeight):
            for x in range(0, self._mapWidth):
                pass



def Main():
    pygame.init()

    size = [900, 900]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Some bullshit")

    clock = pygame.time.Clock()
    done = False

    # Declare map
    gmap = GOLmap()



    while done == False:
        screen.fill((20, 0, 100))

        gmap.DrawMap(screen)

        print("Live neighbors: ", gmap.GetLiveNeighborCount(1,1))

        # Event handling
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                # print("Quitting...")
                done = True
            elif event.type == pygame.MOUSEMOTION:
                # print("Mouse moved")
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # print("Mouse down")
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                # print("Mouse up")
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or pygame.K_ESCAPE:
                    done = True;
            else:
                print(event)

        # Updates
        pygame.display.update()
        clock.tick(20)



print("Calling Main")
Main()

print("Exited")