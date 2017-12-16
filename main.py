import time
import sys
import pygame
from random import randint
from time import sleep
#from pygame.locals import *

#1. Any live cell with fewer than two live neighbours dies (referred to as underpopulation or exposure[1]).
#2. Any live cell with more than three live neighbours dies (referred to as overpopulation or overcrowding).
#3. Any live cell with two or three live neighbours lives, unchanged, to the next generation.
#4. Any dead cell with exactly three live neighbours will come to life.

class CellStatus:
    Alive = 1
    Dead = 0

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



    def __init__(self, mapWidth=10, mapHeight=10, mapCellSize=10):
        self.Init(mapWidth, mapHeight, mapCellSize)

    def Init(self, mapWidth=10, mapHeight=10, mapCellSize=10, mapPosX=0, mapPosY=0):

        self._mapCellOnColor = [0, 0, 0]
        self._mapCellOffColor = [255, 255, 255]
        self._mapCellSize = mapCellSize
        self._mapPos = [mapPosX, mapPosY]
        self._mapCurrentBuffer = 0
        self._mapBackBuffer = 1 - self._mapCurrentBuffer
        self._mapWidth = mapWidth
        self._mapHeight = mapHeight


        self._mapCells = [[[0 for x in range(self._mapWidth)] for y in range(self._mapHeight)] for i in range(2)]


        self.RandomizeMap()
        #self.SwapBuffers()
        #self.RandomizeMap()
        #self.SwapBuffers()

        #self.SetCellStatus(2, 1, CellStatus.Alive)
        #self.SetCellStatus(2, 2, CellStatus.Alive)
        #self.SetCellStatus(2, 3, CellStatus.Alive)

        self.ClearBackBuffer()

        return


    def RandomizeMap(self):
        for y in range(0, self._mapHeight):
            for x in range(0, self._mapWidth):
                self._mapCells[self._mapCurrentBuffer][y][x] = randint(0, 1)

    def FillMap(self, fillVal):
        for y in range(0, self._mapHeight):
            for x in range(0, self._mapWidth):
                self._mapCells[self._mapCurrentBuffer][y][x] = fillVal

    def FillMapRect(self, x,y,width,height,fillVal):
        for py in range(0,height):
            for px in range(0,width):
                if self.IsCellInBounds(x+px,y+py) == True:
                    self._mapCells[self._mapCurrentBuffer][y+py][x+px] = fillVal



    def DrawMap(self, surface):
        # Draw Map
        for y in range(0, self._mapHeight):
            yCur = self._mapPos[1] + (y * self._mapCellSize)
            xCur = self._mapPos[0]
            for x in range(0, self._mapWidth):
                #xCur = self._mapPos[0] + (x * self._mapCellSize)

                #if self.GetCellStatus(x,y) == CellStatus.Dead:
                #    pygame.draw.rect(surface, self._mapCellOffColor, (xCur, yCur, self._mapCellSize-1, self._mapCellSize-1))
                #else:
                #    pygame.draw.rect(surface, self._mapCellOnColor, (xCur, yCur, self._mapCellSize-1, self._mapCellSize-1))

                #if self.GetCellStatus(x,y) == CellStatus.Alive:
                #    pygame.draw.rect(surface, self._mapCellOnColor, (xCur, yCur, self._mapCellSize-1, self._mapCellSize-1))

                if self.GetCellStatus(x,y) == CellStatus.Dead:
                    pygame.draw.rect(surface, self._mapCellOffColor, (xCur, yCur, self._mapCellSize-1, self._mapCellSize-1))

                xCur += self._mapCellSize
        return



    # Convert screen coord to cell coord
    def ScreenToCell(self,sx, sy):
        localX = sx - self._mapPos[0]
        localY = sy - self._mapPos[1]

        cellX = localX / self._mapCellSize
        cellY = localY / self._mapCellSize

        return [int(cellX), int(cellY)]

    def IsCellInBounds(self, x,y):
        if (x >= 0 and x < self._mapWidth and y >= 0 and y < self._mapHeight):
            return True

        return False

    def GetCellStatus(self, x,y):
        if self.IsCellInBounds(x, y):
            return self._mapCells[self._mapCurrentBuffer][y][x]

        return CellStatus.Dead

    def SetCellStatus(self, x,y, status):
        if self.IsCellInBounds(x, y):
            self._mapCells[self._mapCurrentBuffer][y][x] = status

    def GetCellStatusBackBuf(self, x,y):
        if self.IsCellInBounds(x, y):
            return self._mapCells[self._mapBackBuffer][y][x]

        return CellStatus.Dead

    def SetCellStatusBackBuf(self, x,y, status):
        if self.IsCellInBounds(x,y):
            self._mapCells[self._mapBackBuffer][y][x] = status

    def GetLiveNeighborCount(self, x, y):
        # 4 == Current Cell.  Skip
        # 0 1 2
        # 3 4 5
        # 6 7 8

        # loop through 0-9
        # if i == 4, skip
        # if xCount > 2, xCount = 0, px = x-1, py += 1

        liveNeighbors = 0

        px = x-1; py = y-1;
        xMax = x+1

        for i in range(0,9):
            if i != 4:
                if self.IsCellInBounds(px, py) == True:
                    if (self.GetCellStatus(px,py) == CellStatus.Alive):
                        liveNeighbors += 1

            px += 1
            if px > xMax:
                px = x-1
                py += 1

        return liveNeighbors





    def UpdateBackBuffer(self):
        liveNeighbors = 0
        cellStatus = 0
        curBuffer = self._mapCurrentBuffer

        for y in range(0, self._mapHeight):
            for x in range(0, self._mapWidth):
                #self.SetCellStatusBackBuf(x, y, cellStatus)


                liveNeighbors = self.GetLiveNeighborCount(x,y)
                #cellStatus = self.GetCellStatus(x,y)
                cellStatus = self._mapCells[curBuffer][y][x]

                if cellStatus == CellStatus.Alive:
                    if (liveNeighbors < 2 or liveNeighbors > 3):
                        self.SetCellStatusBackBuf(x,y, CellStatus.Dead)
                    else:
                        self.SetCellStatusBackBuf(x, y, CellStatus.Alive)
                elif cellStatus == CellStatus.Dead:
                    if (liveNeighbors == 3):
                        self.SetCellStatusBackBuf(x, y, CellStatus.Alive)
                    else:
                        self.SetCellStatusBackBuf(x, y, CellStatus.Dead)

        return


    def ClearBackBuffer(self):
        liveNeighbors = 0
        cellStatus = 0

        for y in range(0, self._mapHeight):
            for x in range(0, self._mapWidth):
                self.SetCellStatusBackBuf(x,y, CellStatus.Dead)

    # Swap buffers so the front and back buffers are now reversed
    def SwapBuffers(self):
        self._mapCurrentBuffer = 1 - self._mapCurrentBuffer
        self._mapBackBuffer = 1 - self._mapCurrentBuffer





def Main():
    pygame.init()

    size = [1400, 900]
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Some bullshit")

    clock = pygame.time.Clock()
    done = False

    # Declare map
    #gmap = GOLmap(140,90,10)
    gmap = GOLmap(280, 180, 5)

    gmap.DrawMap(screen)
    pygame.display.update()

    lastTimer = time.time()
    mouseDown = False
    mouseCellPlaceType = 1
    paused = False

    while done == False:
        screen.fill((20, 20, 20))
        #screen.fill((200, 200, 200))



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
                mouseDown = True
                if event.button == 1:
                    mouseCellPlaceType = 1
                elif event.button == 3:
                    mouseCellPlaceType = 0
                elif event.button == 2:
                    pos = pygame.mouse.get_pos()
                    cell = gmap.ScreenToCell(pos[0],pos[1])
                    radius = randint(5,20)
                    gmap.FillMapRect(cell[0]-radius, cell[1]-radius, radius+radius, radius+radius, 1)

                #print(event.button)

                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                # print("Mouse up")
                mouseDown = False
                pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    done = True
                elif event.key == pygame.K_f:
                    gmap.FillMapRect(randint(0,gmap._mapWidth), randint(0,gmap._mapHeight),randint(0,50),randint(0,50),1)
                elif event.key == pygame.K_c:
                    gmap.FillMapRect(0, 0, gmap._mapWidth, gmap._mapHeight, 0)
                elif event.key == pygame.K_g:
                    gmap.RandomizeMap()

                elif event.key == pygame.K_SPACE:
                    paused = 1 - paused
            else:
                print(event)

        if mouseDown == True:
            pos = pygame.mouse.get_pos()
            cell = gmap.ScreenToCell(pos[0], pos[1])
            gmap.SetCellStatus(cell[0], cell[1], mouseCellPlaceType)

        lastTimer = time.time()
        gmap.DrawMap(screen)


        # Updates
        #lastTimer = time.time()
        if paused == False:

            gmap.UpdateBackBuffer()
            thisTimer = time.time()
            print(thisTimer - lastTimer)
            gmap.SwapBuffers()
        #gmap.ClearBackBuffer()

        lastTimer = thisTimer

        pygame.display.update()
        #sleep(0.1);
        #




print("Calling Main")
Main()
print("Exited")