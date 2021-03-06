import pygame
import random
import math

class pacman(object):
    def __init__(self, pos):
        self.pos = pos
        self.color = (0,255,255)
        self.rect = pygame.Rect(self.pos[0]*gridSize, self.pos[1]*gridSize, gridSize , gridSize )
        self.speed = 5
        self.dir = (1,0)
        self.prevDir = (0,0)
        self.done = False

    def move(self):
        events = pygame.event.get()

        # Takes the input from keyboard and creates a tuple for the input direction
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.dir = (0,-1)
                    self.desiredDir = self.dir
                elif event.key == pygame.K_DOWN:
                    self.dir = (0,1)
                    self.desiredDir = self.dir
                elif event.key == pygame.K_RIGHT:
                    self.dir = (1,0)
                    self.desiredDir = self.dir
                elif event.key == pygame.K_LEFT:
                    self.dir = (-1,0)
                    self.desiredDir = self.dir
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        if not self.checkCollision(self.dir):
            self.rect.left = self.rect.left + self.dir[0] * self.speed
            self.rect.top = self.rect.top + self.dir[1] * self.speed
            self.prevDir = self.dir
        else:
            if not self.checkCollision(self.prevDir):
                self.rect.left = self.rect.left + self.prevDir[0] * self.speed
                self.rect.top = self.rect.top + self.prevDir[1] * self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

    def checkCollision(self, dir):
        testRect = self.rect.copy()
        testRect.left = self.rect.left + dir[0]
        testRect.top = self.rect.top + dir[1]
        return testRect.collidelistall(wallObjects)

class monsterStruct(object):
    '''
    Monster objects are created like player object.
    Monster's direction is changed whenever it hit something
    '''
    def __init__(self, pos):
        self.pos = pos
        self.color = (255, 122, 0)
        self.rect = pygame.Rect(self.pos[0]*gridSize, self.pos[1]*gridSize, gridSize, gridSize)
        self.dir = (1, 0)
        self.speed = 4

    def move(self):
        if self.checkCollision(self.dir) or self.isAvailableWay():
            minDir = self.decideWay()
            self.dir = (minDir[0], minDir[1])

        self.rect.left = self.rect.left + self.dir[0] * self.speed
        self.rect.top = self.rect.top + self.dir[1] * self.speed

    def checkCollision(self, dir):
        testMonsterList = monsterObjects.copy()
        testMonsterList.remove(self)
        testRect = self.rect.copy()
        testRect.left = testRect.left + dir[0]
        testRect.top = testRect.top + dir[1]
        return testRect.collidelistall(wallObjects) or testRect.collidelistall(testMonsterList)

    def findWays(self):
        possibleWays = [(0,1), (0,-1), (1,0), (-1,0)]
        self.availableWays = []
        for dir in possibleWays:
            if not self.checkCollision(dir):
                self.availableWays.append(dir)

    def isAvailableWay(self):
        possibleWays = [(0,1), (0,-1), (1,0), (-1,0)]
        for dir in possibleWays:
            self.findWays()
            if len(self.availableWays) > 2:
                return True
        return False

    def decideWay(self):
        self.findWays()
        minimumDir = (0,0)
        minimumDist = 2000
        for way in self.availableWays:
            testRect = self.rect.copy()
            testRect.left = testRect.left + way[0]
            testRect.top = testRect.top + way[1]
            distance = math.pow(player.rect.left - testRect.left, 2) + math.pow(player.rect.top - testRect.top, 2)
            distance = math.sqrt(distance)
            if distance < minimumDist:
                minimumDist = distance
                minimumDir = way

        if distance > 300:
            choice = random.randint(0, len(self.availableWays)-1)
            minimumDir = self.availableWays[choice]

        # print("MinDir: "+str(minimumDir))
        # print("AvailableWays: " + str(self.availableWays))
        return minimumDir


    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class wallStruct(object):
    def __init__(self, pos):
        self.pos = pos
        self.color = (130, 130, 130)
        self.rect = pygame.Rect(self.pos[0]*gridSize, self.pos[1]*gridSize, gridSize, gridSize)

        pygame.draw.rect(screen, self.color, self.rect)

class foodStruct(object):
    '''A rectangle object with half of the gridsize and centered in the middle'''
    def __init__(self, pos):
        self.pos = pos
        self.size = gridSize / 2
        self.color = (0, 220, 130)
        self.rect = pygame.Rect(self.pos[0]*gridSize+self.size/2, self.pos[1]*gridSize+self.size/2, self.size, self.size)

        pygame.draw.rect(screen, self.color, self.rect)

def checkGame():
    '''Checks for global actions in game, such as score or death.'''
    global score, foodObjects, player

    if player.rect.collidelistall(foodObjects):
        score = score + 10
        i = player.rect.collidelistall(foodObjects)
        del foodCoords[i[0]]

    if player.rect.collidelistall(monsterObjects):
        player.done = True

def drawMonsters():
    for monster in monsterObjects:
        monster.move()
        monster.draw()

def initMonsters():
    '''Monster objects are created from hard-coded coordinates'''
    global monsterObjects

    # monsterCoords = [(15, 0), (4,8), (16,6), (18,10), (3, 16), (2,6)]
    monsterCoords = [(15, 0), (18,10), (3, 16)]
    monsterObjects = []

    for m in monsterCoords:
        monster = monsterStruct(m)
        monsterObjects.append(monster)

def initFoods(renew=False):
    '''
    If renew is True, all food coordinates are decided amongst the empty places
    with 0.6 chance. After that all food objects are created as global.
    '''
    global foodObjects, foodCoords

    if renew:
        foodCoords = []
        for x in range(20):
            for y in range(20):
                if([x,y] not in wallCoords and [x,y] != [0,0] and [x,y] != [10,2]):
                    if random.randint(0,10) < 6:
                        foodCoords.append([x,y])
    foodObjects = []

    for f in foodCoords:
        food = foodStruct(f)
        foodObjects.append(food)

def initWalls():
    '''
    Walls are hard-coded into the game. Depending on the coorddinates wall objects
    are created as a global list
    '''
    global wallObjects, wallCoords

    wallCoords = [
    [1,1],[2,1],[3,1],[4,1],[6,1],[8,1],[9,1],[10,1],[11,1],[12,1],[13,1],[14,1],[16,1],[17,1],[18,1],
    [6,2],[8,2],[14,2],
    [1,3],[2,3],[3,3],[4,3],[6,3],[8,3],[10,3],[11,3],[12,3],[14,3],[15,3],[17,3],[18,3],[19,3],
    [10,4],[0,5],
    [1,5],[2,5],[3,5],[4,5],[6,5],[8,5],[9,5],[10,5],[11,5],[12,5],[13,5],[14,5],[16,5],[17,5],[18,5],[5,5],
    [1,7],[2,7],[4,7],[5,7],[6,7],[8,7],[9,7],[10,7],[11,7],[12,7],[14,7],[15,7],[16,7],[17,7],[18,7],[7,7],
    [11,8],[17,8],
    [1,9],[3,9],[4,9],[5,9],[6,9],[0,9],[9,9],[10,9],[11,9],[12,9],[14,9],[13,9],[16,9],[17,9],[19,9],[7,9],
    [5,10],[12,10],
    [1,11],[2,11],[3,11],[4,11],[6,11],[8,11],[9,11],[10,11],[11,11],[12,11],[13,11],[14,11],[16,11],[17,11],[18,11],[5,11],
    [6,12],[8,12],[14,12],
    [1,13],[2,13],[3,13],[4,13],[6,13],[8,13],[10,13],[11,13],[12,13],[14,13],[15,13],[17,13],[18,13],[19,13],
    [10,14],[1,14],
    [1,15],[2,15],[4,15],[5,15],[6,15],[8,15],[9,15],[10,15],[11,15],[12,15],[14,15],[15,15],[16,15],[17,15],[18,15],[7,15],
    [11,16],[17,16],
    [1,17],[3,17],[4,17],[5,17],[6,17],[0,17],[9,17],[10,17],[11,17],[12,17],[14,17],[13,17],[16,17],[17,17],[19,17],[7,17],
    [17,18],[16,18],[10,18],[11,18],[3,18],[1,18],
    [5,19],[6,19],[7,19],[14,19],[13,19],[19,19]
    ]
    for i in range(20):
        wallCoords.append((-1,i))
        wallCoords.append((20,i))
        wallCoords.append((i,-1))
        wallCoords.append((i, 20))
    wallObjects = []

    for w in wallCoords:
        wall = wallStruct(w)
        wallObjects.append(wall)

def updateScreen():
    screen.fill((0, 0, 0)) # Fill the surface w/ black
    initFoods()

    drawMonsters()
    player.move()
    player.draw()
    checkGame()

    initWalls()
    pygame.display.update() # Update screen

def gatherInput():
    monsterDistanceList = []
    wallDistanceList = []
    foodDistanceList = []

    for food in foodObjects:
        findDistance(food, foodDistanceList)

    for wall in wallObjects:
        findDistance(wall, wallDistanceList)

    for monster in monsterObjects:
        findDistance(monster, monsterDistanceList)

    print(len(foodDistanceList)+len(monsterDistanceList)+len(wallDistanceList))
    # print("Food: " + str(foodDistanceList))
    # print("Wall: " + str(wallDistanceList))
    # print("Monster: " + str(monsterDistanceList))

def findDistance(obj, lst):
    distance = math.pow(player.rect.left - obj.rect.left, 2) + math.pow(player.rect.top - obj.rect.top, 2)
    distance = math.sqrt(distance)
    lst.append(distance)

def main():
    while True:
        global screen, player, res, rows, gridSize, score
        score = 0
        res = 800
        rows = 20
        gridSize = res // rows

        screen = pygame.display.set_mode((res,res))
        clock = pygame.time.Clock()

        player = pacman((0,0))
        initMonsters()
        initWalls()
        initFoods(True)

        while True:
            clock.tick(30) # 30 fps

            updateScreen()
            gatherInput()
            if player.done:
                break

if __name__ == "__main__":
    main()
