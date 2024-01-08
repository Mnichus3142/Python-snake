import random
import math
import msvcrt
import os
import time

gameMap = []
basePlayerPos = []
playerPos = []
# 0 - bariers, 1 - Holes in the wall, 2 - 3 lives, 3 - Regenerate map after every 5 apples, 4 - Enemies
active = [False, False, False, False, False]
move = ''
start = False
points = 0
highscore = 0
sizeX = 10
sizeY = 10
apples = 3
lives = 3
from_file = False
enemies = []
enemy_action = 0
enemy_direction = 'forward'
art = """
     ____              _        
    / ___| _ __   __ _| | _____ 
    \___ \| '_ \ / _` | |/ / _ \ 
     ___) | | | | (_| |   <  __/
    |____/|_| |_|\__,_|_|\_\___|
"""

def createMap (sizeX, sizeY):
    global from_file
    
    if from_file:
        with open('map.txt', 'r') as file:
            lines = file.readlines()
            for line in lines:
                temp = []
                for char in line.strip():
                    temp.append(char)
                gameMap.append(temp)
    else:
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
                amount = math.floor(random.random() * 6)
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
    
    if gameMap[y][x] == '.' and gameMap[y][x] != '#':
        gameMap[y][x] = 'o'
        return True
    
    createApple(sizeX, sizeY)
    
def printMap(points):
    if active[2]:
        print(f'Points: {points}\t Lives: {lives}\n\n')
    else:
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
    global lives
    
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
    
    # Losing condition 1/3
    if gameMap[playerPos[0][1]][playerPos[0][0]] == '#':
        os.system('cls')
        if active[2] and lives > 1:
            lives -= 1
            move = ''
            start = False
            basePlayerPos = [random.randint(1, sizeY), random.randint(1, sizeX)]
            for i in range(len(playerPos)):
                playerPos[i] = basePlayerPos
            print('You lost one live, the snake drove into the wall')
            time.sleep(2)
        else:
            print('You lost, the snake drove into the wall')
            time.sleep(2)
            highscoreChanger(points)
            return False
        
    # Losing condition 2/3
    if gameMap[playerPos[0][1]][playerPos[0][0]] == '%':
        os.system('cls')
        if active[2] and lives > 1:
            lives -= 1
            move = ''
            start = False
            basePlayerPos = [random.randint(1, sizeY), random.randint(1, sizeX)]
            for i in range(len(playerPos)):
                playerPos[i] = basePlayerPos
            print('You lost one live, the snake drove into the enemy')
            time.sleep(2)
        else:
            print('You lost, the snake drove into the enemy')
            time.sleep(2)
            highscoreChanger(points)
            return False  
        
    # Losing condition 3/3
    if gameMap[playerPos[0][1]][playerPos[0][0]] == '*' and start:
        os.system('cls')
        if active[2] and lives > 1:
            lives -= 1
            move = ''
            start = False
            basePlayerPos = [random.randint(1, sizeY), random.randint(1, sizeX)]
            for i in range(len(playerPos)):
                playerPos[i] = basePlayerPos
            print('You lost one live, the snake drove into himself')
            time.sleep(2)
        else:
            print('You lost, the snake drove into himself')
            time.sleep(2)
            highscoreChanger(points)
            return False
    
    # Add a new segment to the snake
    if gameMap[playerPos[0][1]][playerPos[0][0]] == 'o':
        playerPos.append(playerPos[-1])
        points += 1
        if active[3] and points % 5 == 0:
            gameMap = []
            createMap(sizeX, sizeY)
            for x in range(3):
                createApple(sizeX, sizeY)
        else:
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

def enemy():
    global enemies
    global enemy_action
    global enemy_direction
    global sizeX
    global sizeY

    if len(enemies) == 0:
        x1 = random.randint(2, sizeX - 2)
        y1 = random.randint(2, sizeY - 2)
        enemies.append([[y1 - 1, x1], [y1, x1], [y1 + 1, x1]])
        x2 = random.randint(2, sizeX - 2)
        y2 = random.randint(2, sizeY - 2)
        enemies.append([[y2, x2 - 1], [y2, x2], [y2, x2 + 1]])
    else:
        for i in range(len(enemies)):
            for pos in enemies[i]:
                gameMap[pos[0]][pos[1]] = '.'

        for i in range(len(enemies)):
            new_pos = []
            for x in range(3):
                new_y = enemies[i][x][0]
                new_x = enemies[i][x][1]

                if enemy_direction == 'forward':
                    if i == 0:
                        new_y += 1
                    else:
                        new_x += 1
                else:
                    if i == 0:
                        new_y -= 1
                    else:
                        new_x -= 1

                if 0 < new_y < sizeY and 0 < new_x < sizeX and gameMap[new_y][new_x] == '.':
                    new_pos.append([new_y, new_x])

            if len(new_pos) == 3:
                enemies[i] = new_pos
            else:
                enemy_direction = 'backward' if enemy_direction == 'forward' else 'forward'

        for i in range(len(enemies)):
            for pos in enemies[i]:
                gameMap[pos[0]][pos[1]] = '%'
            
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
    global lives
    
    gameOn = True
    move = ''
    start = False
    gameMap = []
    playerPos = []
    points = 0
    lives = 3
    
    basePlayerPos = [random.randint(1, sizeY), random.randint(1, sizeX)]
    
    createMap(sizeX, sizeY)
    
    playerPos.append(basePlayerPos)
    gameMap[playerPos[0][1]][playerPos[0][0]] = '*'
    
    for i in range(apples):
        createApple(sizeX, sizeY)
        
    printMap(0)

    while gameOn:
        time.sleep(0.3)
        if active[4]:
            enemy()
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
    global from_file
    
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
            modifiers = ['[ ] More barriers on the map', '[ ] Holes in the walls', '[ ] 3 lives', '[ ] Regenerate barriers after eating every 5 apples', '[ ] Enemies']
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
            os.system('cls')
            if from_file:
                from_file = False
                print("Map is no longer loaded from file")
                time.sleep(0.5)
                return 0
            else:
                from_file = True
                print("Map is loaded from file")
                time.sleep(0.5)
                return 0
        case 4:
            return 1
            
def menu ():
    global from_file
    
    actualPosition = 0
    menuElements = ['-> Play game', 'Change number of starting apples', 'Modifiers', 'Load map from file (map.txt)', 'Exit']
       
    os.system('cls')
        
    while True:
        time.sleep(0.4)
        os.system('cls')
    
        for line in art.splitlines():
            print(line)
            
        print(f"\nHighscore: {highscore}\tMap from file: {from_file}\n")
        
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