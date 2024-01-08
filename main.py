import random
import math
import msvcrt
import os
import time

gameMap = []
basePlayerPos = []
playerPos = []
# 0 - bariers, 1 - Holes in the wall, 2 - 3 lives, 3 - Regenerate map after every 5 apples
active = [False, False, False, False]
move = ''
start = False
points = 0
highscore = 0
sizeX = 10
sizeY = 10
apples = 3
art = """
     ____              _        
    / ___| _ __   __ _| | _____ 
    \___ \| '_ \ / _` | |/ / _ \ 
     ___) | | | | (_| |   <  __/
    |____/|_| |_|\__,_|_|\_\___|
"""

def createMap (sizeX, sizeY):
    ax = 3
    ay = 3
    for i in range(sizeY + 2):
        temp = []
        for j in range(sizeX + 2):
            if i == 0 or i == sizeY + 1:
                temp.append('#')
            elif j == 0 or j == sizeX + 1:
                temp.append('#')
            else:
                temp.append('.')
        if active[0]:
            amount = math.floor(random.random() * 10)
            wall_temp = []
            for i in range(amount):
                place = math.floor(random.random() * 10)
                if place not in wall_temp:
                    wall_temp.append(place)
                    temp[place] = '#'
                else:
                    while place in wall_temp:
                        place = math.floor(random.random() * 10)
        gameMap.append(temp) 
                
    if active[1]:
        placeX = math.floor(random.random() * 10) + 1
        placeY = math.floor(random.random() * 10) + 1
        gameMap[0][placeX] = '.'
        gameMap[-1][placeX] = '.'
        gameMap[placeY][0] = '.'
        gameMap[placeY][-1] = '.'
        
def createApple(sizeX, sizeY):
    x = random.randint(0, sizeX - 1)
    y = random.randint(0, sizeY - 1)
    
    if gameMap[y][x] == '.':
        gameMap[y][x] = 'o'
        return True
    
    createApple(sizeX, sizeY)
    
def printMap(points):
    print(f'Points: {points}\n\n')
    for i in gameMap:
        for j in i:
            print(j, end='')
            for x in range(3):
                print(' ', end='')
        print('\n')

def movePlayer(sizeX, sizeY):
    global playerPos
    global gameMap
    global points
    global move
    global start
    
    x = 0
    y = 0
    
    # Key input
    if msvcrt.kbhit():
        key = msvcrt.getwch()
        
        if key == 'w':
            x = 0
            y = -1
            move = 'up'
        if key == 's':
            x = 0
            y = 1
            move = 'down'
        if key == 'a':
            x = -1
            y = 0
            move = 'left'
        if key == 'd':
            x = 1
            y = 0
            move = 'right'
            
        start = True
                    
    else:
        match move:
            case 'up':
                x = 0
                y = -1
            case 'down':
                x = 0
                y = 1
            case 'left':
                x = -1
                y = 0
            case 'right':
                x = 1
                y = 0
                
    
    newPlayerPos = [[playerPos[0][0] + x, playerPos[0][1] + y]]
    
    if newPlayerPos[0][1] == -1:
        newPlayerPos[0][1] = sizeY + 1
    elif newPlayerPos[0][1] == sizeY + 2:
        newPlayerPos[0][1] = 0
        
    if newPlayerPos[0][0] == -1:
        newPlayerPos[0][0] = sizeX + 1
    elif newPlayerPos[0][0] == sizeX + 2:
        newPlayerPos[0][0] = 0
            
    for segment in playerPos[:-1]:
        newPlayerPos.append(segment)
    playerPos = newPlayerPos
    
    # Losing condition 1/2
    if gameMap[playerPos[0][1]][playerPos[0][0]] == '#':
        os.system('cls')
        print('You lost, the snake drove into the wall')
        time.sleep(2)
        highscoreChanger(points)
        return False
    
    # Losing condition 2/2
    if gameMap[playerPos[0][1]][playerPos[0][0]] == '*' and start:
        os.system('cls')
        print('You lost, the snake drove into himself')
        time.sleep(2)
        highscoreChanger(points)
        return False
    
    # Add a new segment to the snake
    if gameMap[playerPos[0][1]][playerPos[0][0]] == 'o':
        playerPos.append(playerPos[-1])
        points += 1
        createApple(sizeX, sizeY)
    
    # Clear previous snake position
    for i in range(len(gameMap)):
        line = gameMap[i]
        for j in range(len(line)):
            if line[j] == '*':
                line[j] = '.'
    
    # Update snake position on the map
    for pos in playerPos:
        try:
            gameMap[pos[1]][pos[0]] = '*'
        except:
            doNothing()
    
    os.system('cls')
    printMap(points)
    
def doNothing():
    return 0
          
def game():
    global sizeX
    global sizeY
    global apples
    global gameMap
    global playerPos
    global points
    global basePlayerPos
    global move
    global start
    
    gameOn = True
    move = ''
    start = False
    gameMap = []
    playerPos = []
    points = 0
    
    basePlayerPos = [math.floor(sizeY / 2), math.floor(sizeX / 2)]
    
    createMap(sizeX, sizeY)
    
    playerPos.append(basePlayerPos)
    gameMap[playerPos[0][1]][playerPos[0][0]] = '*'
    
    for i in range(apples):
        createApple(sizeX, sizeY)
        
    printMap(0)

    while gameOn:
        time.sleep(0.3)
        if movePlayer(sizeX, sizeY) == False:
            gameOn = False
          
def highscoreChanger(x):
    global highscore
    if x > highscore:
        highscore = x

def executeActual(i):
    global sizeX
    global sizeY
    global apples
    global active
    
    match i:
        case 0:
            os.system('cls')
            game()
        case 1:
            x = True
            
            while x:
                try:
                    os.system('cls')
                    print(f"Actual amount of starting apples {apples}\n\nThere must be at least 1 apple at the beginning of the game and max amount of apples is equal to max fields / 2")
                    tempApples = int(input("New amount of apples: "))
                    if tempApples >= 1 and tempApples <= (sizeX * sizeY) / 2:
                        apples = tempApples
                        return 0
                    else:
                        print("Entered ammount of apples is incorrect, changes not saved")
                        time.sleep(0.3)
                        return 0
                except:
                    doNothing()
        case 2:
            x = True
            actualPosition = 0
            modifiers = ['[ ] More barriers on the map', '[ ] Holes in the walls', '[ ] 3 lives', '[ ] Regenerate barriers after eating every 5 apples']
            for i in range(len(modifiers)):
                if active[i]:
                    modifiers[i] = f'[*]{modifiers[i][3:]}'
            modifiers[0] = f'-> {modifiers[0]}'
            
            while x:
                try:
                    time.sleep(0.4)
                    os.system('cls')
                    print('Here you can add modifiers to your game\nPress backspace to go back\n')
                    
                    for i in modifiers:
                        print(i)
                        
                    modifiers[actualPosition] = f'{modifiers[actualPosition][3:]}'
                    if msvcrt.kbhit():
                        key = msvcrt.getwch()
                        
                        if key == 'w':
                            if actualPosition >= 1:
                                actualPosition -= 1
                        if key == 's':
                            if actualPosition <= len(modifiers) - 2:
                                actualPosition += 1
                        if key == '\r':
                            if active[actualPosition]:
                                modifiers[actualPosition] = f'[ ]{modifiers[actualPosition][3:]}'
                                active[actualPosition] = False
                                if actualPosition == 0:
                                    modifiers[3] = f'[ ]{modifiers[3][3:]}'
                                    active[3] = False
                            else:
                                modifiers[actualPosition] = f'[*]{modifiers[actualPosition][3:]}'
                                active[actualPosition] = True
                                if actualPosition == 3:
                                    modifiers[0] = f'[*]{modifiers[0][3:]}'
                                    active[0] = True
                        if key == '\x08':
                            os.system('cls')
                            print('Changes saved')
                            return 0
                    modifiers[actualPosition] = f'-> {modifiers[actualPosition]}'
                except:
                    doNothing()
        case 3:
            return 1
            
def menu ():
    actualPosition = 0
    menuElements = ['-> Play game', 'Change number of starting apples', 'Modifiers', 'Exit']
       
    os.system('cls')
        
    while True:
        time.sleep(0.4)
        os.system('cls')
    
        for line in art.splitlines():
            print(line)
            
        print(f"\nHighscore: {highscore}\n")
        
        for i in range(len(menuElements)):
            print(f"{menuElements[i]}")
        
        menuElements[actualPosition] = f'{menuElements[actualPosition][3:]}'
        
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            
            if key == 'w':
                if actualPosition >= 1:
                    actualPosition -= 1
            if key == 's':
                if actualPosition <= len(menuElements) - 2:
                    actualPosition += 1
            if key == '\r':
                if executeActual(actualPosition) == 1:
                    return 0
                
        menuElements[actualPosition] = f'-> {menuElements[actualPosition]}'
    
menu()