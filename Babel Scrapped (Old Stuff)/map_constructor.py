import math
import pygame
import random
import os
'''
The general legend for the map is the following
0 = placeholder / nothing
1 = normal combat
2 = elite combat
3 = event
4 = shop
5 = forge
6 = altar
7 = rest site
8 = chest
9 = boss
A general rule of thumb for where certains things will happen are:
Floor 1 is always 4 normal fights
Floor 8 always has 4 chests
Floor 3, 6-7, 10-11 will generally contain elite fights (Can be others)
Floor 15 always has rest sites, 4
'''

def createMap():
    map = {
        1: {1 : 1, 2 : 1, 3 : 1, 4 : 1},
        2: {},
        3: {},
        4: {},
        5: {},
        6: {},
        7: {},
        8: {1 : 8, 2 : 8, 3 : 8, 4 : 8},
        9: {},
        10: {},
        11: {},
        12: {},
        13: {},
        14: {},
        15: {1 : 7, 2 : 7, 3 : 7, 4 : 7},
        16: {1 : 9}
    }
    # assigning room types to each room and keeping track of what might already be maxed out
    def assigningRoom(currentNumberOfShop, currentNumberOfForge, currentNumberOfElites, currentNumberOfRestSites, currentFloor):
        maxNumberOfShop = 4
        maxNumberOfForge = 3
        maxNumberOfElites = 7
        maxNumberOfRestSites = 3
        roomTypeID = 0 # Placeholder
        if currentFloor in {2, 3, 4}: # We don't want any "unique" events hapening before floor 5
            splitChance = random.randint(1, 100)
            if splitChance <= 70:
                return 1
            else:
                return 3
        elif currentFloor == 5:
            splitChance = random.randint(1, 100)
            if splitChance <= 30:
                return 1
            elif splitChance <= 70:
                if currentNumberOfElites == maxNumberOfElites:
                    return 1
                return 2
            elif splitChance <= 80:
                if currentNumberOfShop == maxNumberOfShop:
                    return 1
                return 4
            elif splitChance <= 90:
                if currentNumberOfForge == maxNumberOfForge:
                    return 1
                return 5
            else:
                return 3
        elif currentFloor == 6:
            splitChance = random.randint(1, 100)
            if splitChance <= 30:
                return 1
            elif splitChance <= 45:
                if currentNumberOfElites == maxNumberOfElites:
                    return 3
                return 2
            elif splitChance <= 70:
                if currentNumberOfShop == maxNumberOfShop:
                    return 3
                return 4
            elif splitChance <= 85:
                if currentNumberOfForge == maxNumberOfForge:
                    return 1
                return 5
            elif splitChance <= 90:
                if currentNumberOfRestSites == maxNumberOfRestSites:
                    return 3
                return 7
            else:
                return 3
        elif currentFloor == 7:
            splitChance = random.randint(1, 100)
            if splitChance <= 30:
                return 1
            elif splitChance <= 45:
                if currentNumberOfElites == maxNumberOfElites:
                    return 3
                return 2
            elif splitChance <= 60:
                if currentNumberOfShop == maxNumberOfShop:
                    return 3
                return 4
            elif splitChance <= 85:
                if currentNumberOfForge == maxNumberOfForge:
                    return 1
                return 5
            elif splitChance <= 90:
                if currentNumberOfRestSites == maxNumberOfRestSites:
                    return 3
                return 7
            else:
                return 3
        else:
            splitChance = random.randint(1, 100)
            # The chances for each room (43% for normal fight, 10% chance for elite, 10% chance for shop, 8% chance for forge, 22% chance for occurrence, 7% chance for rest site)
            if splitChance <= 43:
                return 1
            elif splitChance <= 53:
                return 2
            elif splitChance <= 63:
                return 4
            elif splitChance <= 71:
                return 5
            elif splitChance <= 78:
                return 7
            else:
                return 3
        # End of function assigningRooms

    # The maximum amount of elite fight, shops, forges, and rest sites
    maxNumberOfShop = 4
    maxNumberOfForge = 3
    maxNumberOfElites = 7
    maxNumberOfRestSites = 3
    currentNumberOfShop = 0
    currentNumberOfForge = 0
    currentNumberOfElites = 0
    currentNumberOfRestSites = 0

    for floorNumber in range(2, 8): # Does floor 2 - 7
        currentFloor = floorNumber
        numberOfRooms = random.randint(3, 6)
        for roomNumber in range(1, numberOfRooms+1):
            roomType = assigningRoom(currentNumberOfShop, currentNumberOfForge, currentNumberOfElites, currentNumberOfRestSites, currentFloor)
            map[floorNumber][roomNumber] = roomType

    for floorNumber in range(9, 15): # Does floor 9 - 14
        currentFloor = floorNumber
        numberOfRooms = random.randint(3, 6)
        if floorNumber == 9: # The altar will always be on floor 9 and will be placed randomly into one of the room position
            altarRoomNumber = random.randint(1, numberOfRooms)
            for roomNumber in range(1, numberOfRooms+1):
                if roomNumber == altarRoomNumber:
                    map[floorNumber][roomNumber] = 6
                else:
                    roomType = assigningRoom(currentNumberOfShop, currentNumberOfForge, currentNumberOfElites, currentNumberOfRestSites, currentFloor)
                    map[floorNumber][roomNumber] = roomType
        else:
            for roomNumber in range(1, numberOfRooms+1):
                roomType = assigningRoom(currentNumberOfShop, currentNumberOfForge, currentNumberOfElites, currentNumberOfRestSites, currentFloor)
                map[floorNumber][roomNumber] = roomType
    # create path function
    '''
    We need if statements to check if both the current floor and next floor have the same number of rooms
    This is important because a lower # of rooms going to higher can leave some rooms impossible to reach via RNG
    While lower to higher can still have this a lower chance, and depending on which is which. We will need to code fail safes
    '''
    path = {}
    path[0, 0] = [1, 2, 3, 4]
    for floor in range(1, 15): # Only goes to floor 14 beause floor 15 to 16 is always just the 4 rest sites connecting up
        if len(map[floor]) == len(map[floor+1]): # If the number of rooms for the current floor is equal to the above floor
            for room in map[floor].keys():
                amountOfBanches = random.randint(1,2)
                if amountOfBanches == 1:
                    connectingLine = 0
                    if (floor, room) not in path:
                        path[floor, room] = [room+connectingLine]
                    else:
                        path[floor, room].append(room+connectingLine)
                else:
                    for times in range(1, 3):
                        if room == 1:
                            if times == 1:
                                connectingLine = 0
                            else:
                                connectingLine = 1
                        elif room == len(map[floor]):
                            if times == 1:
                                connectingLine = 0
                            else:
                                connectingLine = -1
                        else:
                            if times == 1:
                                connectingLine = 0
                            else:
                                connectingLine = random.randint(-1, 1)
                                if connectingLine == 0:
                                    connectingLine == 1
                        if (floor, room) not in path:
                            path[floor, room] = [room+connectingLine]
                        else:
                            path[floor, room].append(room+connectingLine)
        elif len(map[floor]) < len(map[floor+1]): # If the current floor has less rooms than the one above
            if len(map[floor]) == len(map[floor+1]) - 1: # if difference in room amounts is 1
                for room in map[floor]:
                    if room == len(map[floor]):
                        path[floor, room] = [room]
                        path[floor, room].append(room+1)
                    elif room == 1:
                        path[floor, room] = [room]
                    else:
                        amountOfBanches = random.randint(1,2)
                        if amountOfBanches == 1:
                            connectingLine = 0
                            if (floor, room) not in path:
                                path[floor, room] = [room+connectingLine]
                            else:
                                path[floor, room].append(room+connectingLine)
                        else:
                            for times in range(1, 3):
                                if times == 1:
                                    connectingLine = 0
                                    break
                                else:
                                    connectingLine = random.randint(-1, 1)
                                    if connectingLine == 0:
                                        connectingLine = 1
                                        break
                            if (floor, room) not in path:
                                path[floor, room] = [room+connectingLine]
                            else:
                                path[floor, room].append(room+connectingLine)
            elif len(map[floor]) == len(map[floor+1]) - 2: # if difference in room amounts is 2
                for room in map[floor]:
                    if room == 1:
                        path[floor, room] = [room]
                        path[floor, room].append(room + 1)
                    elif room == len(map[floor]):
                        path[floor, room] = [room + 1]
                        path[floor, room].append(room + 2)
                    else:
                        amountOfBanches = random.randint(1,2)
                        if amountOfBanches == 1:
                            connectingLine = 1
                            if (floor, room) not in path:
                                path[floor, room] = [room+connectingLine]
                            else:
                                path[floor, room].append(room+connectingLine)
                        else:
                            for times in range(1, 3):
                                if times == 1:
                                    connectingLine = 1
                                    break
                                else:
                                    connectingLine = random.randint(-1, 1)
                                    if connectingLine == 1:
                                        connectingLine == 0
                                        break
                            if (floor, room) not in path:
                                path[floor, room] = [room+connectingLine]
                            else:
                                path[floor, room].append(room+connectingLine)
            else: # hard coding if the difference in room amounts is 3
                for room in map[floor]:
                    if room == 1:
                        path[floor, room] = [room]
                        path[floor, room].append(room+1)
                    elif room == 2:
                        path[floor, room] = [room+1]
                        path[floor, room].append(room+2)
                    else:
                        path[floor, room] = [room+2]
                        path[floor, room].append(room+3)
        else: # If the current floor has more rooms than the above floor
            if len(map[floor]) == len(map[floor + 1]) + 3: # Difference of 3 form current to above floor
                for room in map[floor]:
                    if room == 1:
                        path[floor, room] = [room]
                    elif room == 2:
                        path[floor, room] = [room - 1]
                    elif room == 3:
                        path[floor, 3] = [room - 1]
                    elif room == 4:
                        path[floor, 4] = [room - 2]
                    elif room == 5:
                        path[floor, 5] = [room - 2]
                    else:
                        path[floor, 6] = [room - 3]
            elif len(map[floor]) == len(map[floor + 1]) + 2: # Difference of 2
                for room in map[floor]:
                    if room == 1:
                        path[floor, room] = [room]
                    elif room == len(map[floor]):
                        path[floor, room] = [room-2]
                    elif room == 2:
                        path[floor, room] = [room - 1]
                    elif room == len(map[floor]) - 1:
                        path[floor, room] = [room - 1]
                    else:
                        amountOfBanches = random.randint(1,2)
                        if amountOfBanches == 1:
                            connectingLine = -1
                            if (floor, room) not in path:
                                path[floor, room] = [room+connectingLine]
                            else:
                                path[floor, room].append(room+connectingLine)
                        else:
                            for times in range(1, 3):
                                if times == 1:
                                    connectingLine = -1
                                else:
                                    connectingLine = random.randint(-1, 0)
                                    if connectingLine == -1:
                                        connectingLine == 0
                                if (floor, room) not in path:
                                    path[floor, room] = [room+connectingLine]
                                else:
                                    path[floor, room].append(room+connectingLine)
            else: #Difference of 1
                for room in map[floor]:
                    if room == len(map[floor]):
                        path[floor, room] = [room - 1]
                    elif room == len(map[floor]) - 1:
                        path[floor, room] = [room]
                    else:
                        amountOfBanches = random.randint(1,2)
                        if amountOfBanches == 1:
                            connectingLine = 0
                            if (floor, room) not in path:
                                path[floor, room] = [room+connectingLine]
                            else:
                                path[floor, room].append(room+connectingLine)
                        else:
                            for times in range(1, 3):
                                if room == 1:
                                    if times == 1:
                                        connectingLine = 0
                                    else:
                                        connectingLine = 1
                                else:
                                    if times == 1:
                                        connectingLine = 0
                                    else:
                                        connectingLine = random.randint(-1, 1)
                                        if connectingLine == 0:
                                            connectingLine == 1
                                if (floor, room) not in path:
                                    path[floor, room] = [room+connectingLine]
                                else:
                                    path[floor, room].append(room+connectingLine)
    path[15, 1] = [1]
    path[15, 2] = [1]
    path[15, 3] = [1]
    path[15, 4] = [1]
    # end of creating path
    # End of create map function
    return map, path

class Map:
    def __init__(self, map_info = None):
        if map_info == None:
            self.map, self.path = createMap()
            self.map_copy = self.map.copy()
            self.path_copy = self.path.copy()
        else:
            self.map, self.path = map_info
            self.map_copy = self.map.copy()
            self.path_copy = self.path.copy()

        self.xOffSet = 0
        self.yOffSet = 0
        
    def drawMap(self):
        self.screen = pygame.display.set_mode((1600, 900))
        self.map_surface = pygame.Surface((1600, 1800), pygame.SRCALPHA)

        x_spacing_three = 275
        x_spacing_four = 225
        x_spacing_five = 175
        x_spacing_six = 150
        y_spacing = 100

        x_off_set = 300

        roomPosition = {} # Store room position to then draw lines based on their x and y values
        for floor in range(1, 17):
            for room_number in self.map_copy[floor].keys():
                if len(self.map_copy[floor]) == 3:
                    roomPosition[floor, room_number] = (x_off_set + x_spacing_three * room_number, y_spacing * floor)
                elif len(self.map_copy[floor]) == 4:
                    roomPosition[floor, room_number] = (x_off_set + x_spacing_four * room_number, y_spacing * floor)
                elif len(self.map_copy[floor]) == 5:
                    roomPosition[floor, room_number] = (x_off_set + x_spacing_five * room_number, y_spacing * floor)
                elif len(self.map_copy[floor]) == 6:
                    roomPosition[floor, room_number] = (x_off_set + x_spacing_six * room_number, y_spacing * floor)
                else:
                    roomPosition[floor, room_number] = (800, y_spacing * floor)
        
        # Fix this later and properly display screen
        '''for connection in roomPosition:
            if connection == (16, 1):
                pass
            else:
                x_source_room, y_source_room = roomPosition[connection]
                for dest_room in self.path_copy[connection]:
                    x_dest_room, y_dest_room = roomPosition[connection[0] + 1, dest_room]

                    # calculate angle and distance to the dest room
                    angle = -math.atan2(y_dest_room - y_source_room, x_dest_room - x_source_room)
                    distance = math.sqrt((x_dest_room - x_source_room)**2 + (y_dest_room - y_source_room)**2)

                    rect_width = 10
                    dx = math.cos(angle) * distance
                    dy = math.sin(angle) * distance

                    p1 = (x_source_room, y_source_room)
                    p2 = (x_source_room + dx, y_source_room + dy)
                    p3 = (x_source_room + dx - math.sin(angle) * rect_width, y_source_room + dy + math.cos(angle) * rect_width)
                    p4 = (x_source_room - math.sin(angle) * rect_width, y_source_room + math.cos(angle) * rect_width)

                    pygame.draw.polygon(self.map_surface, (255, 0, 0), [p1, p2, p3, p4])'''

    def drawRooms():
        pass