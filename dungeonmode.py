"""
Copyright 2014, 2015 Andrew Russell

This file is part of PotionWars.
PotionWars is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

PotionWars is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PotionWars.  If not, see <http://www.gnu.org/licenses/>.

"""
from __future__ import division
import universal
from universal import *
import townmode
import operator
import ast
import pygame
import os
import person
import music
import math
import copy
import random

"""
TODO: My dungeon display code just outright isn't working. I need to delete the whole thing, and start over.

I should probably better organize the whole damn thing.
"""

"""
For the GUI of the dungeon view:
    We'll replace the commands with the character names, health and mana. We'll dynamically resize the commandView and worldView to be the minimum size needed to fit all the
    party members (ranging from 1/3rd the standard size for one character in the party up to double the standard size for 6 characters).
"""

dungeon = None
HERE = 0
NORTH = 1
SOUTH = -1
EAST = 2
WEST = -2
MARKED = 3

#stepEffect = pygame.mixer.Sound(os.path.join('data', 'step.wav'))

#TODO: Build another surface for the current facing direction.
pygame.font.init()
fontSize = pygame.font.SysFont(universal.FONT_LIST_TITLE, universal.TITLE_SIZE).size(str((10,10,10)))
coordinateSurface = pygame.Surface((fontSize[0] + 20, fontSize[1] + 20))
coordinateSurface.fill(universal.DARK_GREY)
fontSize = pygame.font.SysFont(universal.FONT_LIST_TITLE, universal.TITLE_SIZE).size('N')
directionSurface = pygame.Surface((fontSize[0] + (fontSize[1] - fontSize[0]), fontSize[1] + 20))
directionSurface.fill(universal.DARK_GREY)

def set_dungeon_commands(dungeon=None):
    commandColors = [LIGHT_GREY] * 8
    universal.set_commands(['(P)arty', '(S)ave', '(Q)uick Save', '(L)oad', 't(I)tle Screen', '(C)ast', '(G)o', '(Esc)Quit'])
    if dungeon is not None:
        floor = dungeon.coordinates[0]
        row = dungeon.coordinates[1]
        column = dungeon.coordinates[2]
        square = dungeon[floor][row][column]
        if has_char('e', square):
            commandColors.insert(0, BLUE)
            universal.set_commands(['(E)xit'] + get_commands(), commandColors)
        if has_char('u', square):
            #changingFloors = True
            commandColors.insert(0, GREEN) 
            universal.set_commands(['(U)p'] + get_commands(), commandColors)
        if has_char('d', square):
            #changingFloors = True
            commandColors.insert(0, GREEN)
            universal.set_commands(['(D)own'] + get_commands(), commandColors)
        if has_char('s', square):
            commandColors.insert(0, GREEN)
            universal.set_commands(['(E)xit'] + get_commands(), commandColors)


def print_dir(direction):
    if direction == NORTH:
        return "N"
    elif direction == SOUTH:
        return "S"
    elif direction == EAST:
        return "E"
    elif direction == WEST:
        return "W"

def dungeon_mode(sayDescription=True):
    global dungeon
    dungeon = universal.state.get_room(dungeon.name)
    universal.state.location = dungeon
    music.play_music(dungeon.bgMusic)
    if dungeon.coordinates == (-1, -1, -1):
        dungeon.coordinates = start_coordinate(dungeon)
        previousRoom = [room for room in universal.state.rooms.keys() if universal.state.get_room(room).characters is not None and 
            person.get_party()[0] in universal.state.get_room(room).characters.values()][0]
        universal.state.get_room(previousRoom).remove_characters(universal.state.party.members)
        dungeon.add_characters(universal.state.party.members)
        dungeon.display_event()
        dungeon.visitedSquares.add(start_coordinate(dungeon))
    else:
        dungeon.display()

def inverse(direction):
    return 0 - direction

def left(direction):
    if direction == NORTH:
        return WEST
    elif direction == SOUTH:
        return EAST
    elif direction == WEST:
        return SOUTH
    elif direction == EAST:
        return NORTH

def dir_name(direction):
    if direction == NORTH:
        return "NORTH"
    elif direction == SOUTH:
        return "SOUTH"
    elif direction == EAST:
        return "EAST"
    elif direction == WEST:
        return "WEST"
    elif direction == HERE:
        return "HERE"
    else:
        return(str(direction) + " is not a valid direction.")

def right(direction):
    return inverse(left(direction))

class DungeonFloor(universal.RPGObject):

    MAX_HEIGHT = 20
    MAX_WIDTH = 20
    """
        Implements a single floor. See the documentation for Dungeon for details.
        Floor should be a tuple of tuple of strings, events a list of list of functions.
    """
    def __init__(self, floor, events=None, visibility=4, encounterRate=0, enemies=None, maxEnemies=2, ambushChance=0):
        self.floor = floor
        if not events:
            events = []
        self.events = events
        self.height = len(floor)
        self.visibility = visibility
        self.width = len(max(floor, key=lambda x : len(x)))
        self.convert_dungeon_map()
        self.encounterRate = encounterRate
        self.enemies = enemies
        self.maxEnemies = maxEnemies
        self.ambushChance = ambushChance

    def convert_dungeon_map(self):
        """
        Converts this dungeon's map into a three dimensional list, where each square consists of a string containing the icons associated with each square.
        """
        convertedMap = []
        convertedMap.extend([[] for i in range(len(self))])
        count = len(self) - 1
        for row in range(len(self)):
            for column in range(len(self[row])):
                data = {NORTH:'', SOUTH:'', EAST:'', WEST:'', HERE:''}
                data = self[row][column]
                convertedMap[count].append(data)
            count -= 1
        self.floor = convertedMap



    def __getitem__(self, key):
        if key >= self.height:
            key = self.height - key
        if key < 0:
            key = self.height + key
        if key < 0 or key >= self.height:
            raise IndexError(' '.join([str(key), 'has indexed past the height', str(self.height), 'of this dungeon floor.']))
        key = (self.height - 1) - key
        return self.floor[key]

    def __len__(self):
        return len(self.floor)

class FloorEvents(universal.RPGObject):
    """
    Events should be a tuple of tuples of functions, one function for each square of this particular floor (note: the function may be None if a floor doesn't have a special
    event. In that case, the game will see if a random encounter should be generated).
    Note that FloorEvents is indistinguishable from a tuple of tuple of functions, except that it ensures that the coordinates from a dungeon map, and the coordinates of
    the function line up, if you define the functions for the 0th row of the dungeon floor as the last list of functions in the list of list of functions.
    For example, if you call D[1][2][3] 

    Essentially, this allows you to define a dungeon floor as:
        map = ( ('|____', '___','|'),
                ('|    ', '   ','|'),
                ('|_se_', '_*_','|'),
              )

        and the associated functions as:
        func = ((None, None),
                (start, event1)
        rather than as the mirror image:
        func = ((start, event1),
                (None, None))
    Note: The FloorEvents does NOT include the Buffer row and column that the Dungeon Floor does. That's because the Buffer floor and column aren't actual squares, and so
    should have no event associated with them.
    """
    def __init__(self, events):
        self.events = events
        self.height = len(events)
        self.width = len(max(events, key=lambda x : len(x)))

    def __getitem__(self, key):
        """
        Floor should NOT have the buffer row and column.
        """
        if key < 0:
            key = (self.height - 1) + key
        if key < 0 or key >= self.height:
            raise IndexError(' '.join([str(key), 'has indexed past the height', str(self.height), 'of this dungeon floor.']))
        key = self.height - 1 - key
        return self.events[key]


currentCoordinate = 0
COORDINATE_DIMENSION = 3
moveTo = ["_"] * 3
def go_interpreter(keyEvent):
    global currentCoordinate, moveTo, dungeon
    dirtyRects = []
    if keyEvent.key in universal.NUMBER_KEYS:
        moveTo[currentCoordinate] = moveTo[currentCoordinate][:-1] + pygame.key.name(keyEvent.key) + moveTo[currentCoordinate][-1]
        universal.set_commands([''.join(["Coordinates to travel to:", ', '.join(moveTo)]), '(Esc) Cancel', '<==Back'])  
    elif keyEvent.key == K_RETURN:
        if moveTo[currentCoordinate] == '_':
            return
        moveTo[currentCoordinate] = moveTo[currentCoordinate][:-1]
        currentCoordinate += 1
        if currentCoordinate >= COORDINATE_DIMENSION:
            z, x, y = tuple(map(int, moveTo))
            newCoordinates = (z, y, x)
            if newCoordinates in dungeon.visitedSquares:
                moveTo = ["_"] * 3
                previousCoordinates = dungeon.coordinates
                dungeon.coordinates = newCoordinates
                dirtyRects = dungeon.display_event(previousCoordinates)
            else:
                set_commands(["Cannot travel to unvisited square.", "(Enter) Acknowledge."])
                set_command_interpreter(go_error_interpreter)
        else:
            universal.set_commands([''.join(["Coordinates to travel to:", ', '.join(moveTo)]), '(Esc) Cancel', '<==Back'])  
    elif keyEvent.key == K_BACKSPACE:
        if moveTo[currentCoordinate] == '_':
            currentCoordinate -= 1
            if currentCoordinate < 0:
                set_dungeon_commands(dungeon)
                universal.set_command_interpreter(dungeon_interpreter)
                return dirtyRects
            else:
                moveTo[currentCoordinate] = moveTo[currentCoordinate][:-1] + '_'
        else:
            moveTo[currentCoordinate] = moveTo[currentCoordinate][:-2] + '_'
        universal.set_commands([''.join(["Coordinates to travel to:", ', '.join(moveTo)]), '(Esc) Cancel', '<==Back'])  
    elif keyEvent.key == K_ESCAPE:
        set_dungeon_commands(dungeon)
        universal.set_command_interpreter(dungeon_interpreter)
    dirtyRects.append(universal.commandView)
    return dirtyRects

def go_error_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        global currentCoordinate, moveTo
        currentCoordinate = COORDINATE_DIMENSION-1
        moveTo[-1] += '_'
        universal.set_commands([''.join(["Coordinates to travel to:", ', '.join(moveTo)]), '(Esc) Cancel', '<==Back'])  
        universal.set_command_interpreter(go_interpreter)



class Dungeon(townmode.Room):
    """
    A dungeon, D. D[i][j][k] corresponds to coordinate (j,k) on floor i.
    Note that it is assumed that dungeons are rectangular (i.e. the width of each row is the same, and the height of each column is the same)
    A dungeon contains two pieces:
    1. A DungeonMap: A dungeon map M is a map of tuples of tuples of strings. map[i] is the floor map of floor i, as a tuple of tuples.  
    Each tuple of strings contains the information about that square (whether the square has an east or south wall,
    any events, etc.) using special symbols for each event. The symbols are the following:
        a. "|"  - This square has a wall to the east
        b. "_"  - This square has a wall to the south
        c. "*"  - A special event occurs at this spot.
        d. ";"  - This square has a door to the east.
        e. ":"  - This square has a secret door to the east.
        f. ".," - This square has a door to the south.
        g. ".." - This square has a secret door to the south.
        h. "d"  - This square has a passage from the current floor to the floor below.
        i. "u"  - This square has a passage from the current floor to the floor above.
        j. "!"  - This square has a guaranteed random encounter
        k. "s"  - Start square
        l. "e"  - Exit Square
        m. "x" - A one time encounter

        The start square is where the player begins dungeon crawling. 
        The designer MUST provide a start square for the floor on which play begins, and should provide ONLY ONE start square. When the player enters the dungeon, the
        game scans through the dungeon map to locate the start square
        When the player enters the dungeon, the game will search for a corresponding event function. So, if the player is starting at (1,2) of floor 1, and the designer
        wants to say something when the player first enters the dungeon, then there should be a function in F[1][1][2]. If F[1][1][2] is None, then nothing is executed,
        and play continues as normal. Note that the start square function is executed *before* the game registers that the player enters the dungeon. Therefore, if you
        want the start square to do something different depending on whether the player is first entering, or coming onto the start square from another square in the 
        dungeon, then include the check if party.inDungeon, where the party is the game's party of PC's.

        The exit square is a little bit interesting. Because it is possible to have different exit squares go to different towns, the designer has to manually invoke
        town_mode. The only thing that the exit square does for you, is that it automatically fully heals the party just before invoking the exit event function. Note
        that a dungeon does *not* need an exit square (for situations where you don't want the player to leave the dungeon until they've accomplished something). However,
        if you don't include an exit square, make sure that the event function that handles whatever is the goal of the dungeon (a particularl item found, a boss fought)
        also moves the player back into the appropriate town and invokes town_mode. Otherwise, the player will be trapped in the dungeon!

        Each map starts with coordinate [0][0] in the bottom-left corner of the map (note that this is actually a mirror image of the coordinates of the tuple you define in
        Python, however, the Dungeon lookup function (which allows you to do something like D[i][j][k] handles this).
        Note that you must also provide a dummy row and column for the northern and western walls. If the player tries to go past the boundaries of the map, then the player
        will wrap back around to the other side.

        For example, in Python, if you draw the following map:

        map = ( ('|____', '___','|'),
                ('|    ', '   ','|'),
                ('|_se_', '_*_','|'),
              )
        Corresponds to a 2x2 square, where the player starts (and can exit) at (0,0),  and there is an event at (0, 1). Note that the extra spaces, and extra copies of "_" 
        are there only for readability. This map is equivalent to:
                ( ('|_', '_', '|'),
                ('|',  '','|'),
                ('|_se '_*', '|'),
              )
        which is in turn equivalent to:
            (('|_', '_', '|'), ('|',  '','|'), ('|_se', '_*', '|'))
              

    2. A list of lists of list of special event functions, F. F[i][j][k] is called when the player steps on M[i][j][k]. If M[i][j][k] does not have a special event, 
    then F[i][j][k] is not invoked.
    
    """

    """
    dungeonMap can be a tuple of tuple of strings, or a tuple of DungeonFloors and dungeonEvents can be a tuple of tuple of functions, or a tuple of FloorEvents.
    The dungeon also takes as an optional argument the direction the player should face when starting off in the dungeon. The direction defaults to north.
    """
    def __init__(self, name, dungeonMap, dungeonEvents, direction=NORTH, description="", visibility=None, adjacent=None, characters=None, after_arrival=None,
            bgMusic=None, enemies=None, maxEnemies=None, ambushChance=None, encounterRates=None):
        super(Dungeon, self).__init__(name, description, adjacent, characters, after_arrival, bgMusic)
        self.direction = direction
        self.coordinates = (-1, -1, -1)
        self.dungeonMap = {}
        count = 0
        self.dungeonEvents = {}
        self.visitedSquares = set()
        self.visibleSquares = set()
        self.mapSurface = None
        self.drawnSquares = set()
        if dungeonEvents is not None:
            for floorEvents in dungeonEvents:
                self.dungeonEvents[count] = floorEvents if type(floorEvents) == FloorEvents else FloorEvents(floorEvents)
                count += 1
        else:
            for i in range(len(dungeonMap)):
                self.dungeonEvents[count] = None
                count += 1
        if dungeonMap is not None:
            count = 0
            if not encounterRates:
                encounterRates = [0, 0]
            for floor in dungeonMap:
                if visibility is None:
                    self.dungeonMap[count] = floor if type(floor) == DungeonFloor else DungeonFloor(floor, self.dungeonEvents[count], encounterRate=encounterRates[count])
                else:
                    self.dungeonMap[count] = floor if type(floor) == DungeonFloor else DungeonFloor(floor, self.dungeonEvents[count], visibility[count], encounterRate=encounterRates[count])
                if enemies is not None:
                    self.dungeonMap[count].enemies = enemies
                if maxEnemies is not None:
                    self.dungeonMap[count].maxEnemies = maxEnemies
                if ambushChance is not None:
                    self.dungeonMap[count].ambushChance = ambushChance
                count += 1


    def go(self):
        universal.set_commands([''.join(["Coordinates to travel to:", ', '.join(moveTo)]), '(Esc) Cancel', '<==Back'])  
        set_command_interpreter(go_interpreter)


    def draw_vertical_line(self, startPos, verticalLineLength, mapSurface, width=1):
        endPos = (startPos[0], startPos[1]-verticalLineLength)
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, startPos, endPos, width)


    def draw_vertical_door(
            self, startPos, horizontalLineLength, verticalLineLength, verticalGap, mapSurface, 
            width=1):
        endPos = (startPos[0], startPos[1]-(verticalLineLength // 2) + verticalGap)
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, startPos, endPos, width)
        #Draw little horizontal dashes to mark doors
        horizontalStart = (startPos[0] - horizontalLineLength//16, endPos[1]) 
        horizontalEnd = (startPos[0] + horizontalLineLength//16, endPos[1]) 
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, horizontalStart, horizontalEnd, width) 
        #Each side of the gap contributes equally to the width of the gap.
        originalStart = startPos
        startPos = (startPos[0], endPos[1] - 2*verticalGap)
        endPos = (startPos[0], originalStart[1]-verticalLineLength)
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, startPos, endPos, width)
        #Draw little horizontal dash to mark door
        horizontalStart = (startPos[0] - horizontalLineLength//16, startPos[1]) 
        horizontalEnd = (startPos[0] + horizontalLineLength//16, startPos[1]) 
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, horizontalStart, horizontalEnd, width) 

    def draw_horizontal_line(self, startPos, horizontalLineLength, mapSurface, width=1):
        endPos = (startPos[0]+horizontalLineLength, startPos[1])
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, startPos, endPos, width)

    def draw_horizontal_door(self, startPos, horizontalLineLength, verticalLineLength, horizontalGap, mapSurface, width=1):
        #Could probably generalize this into a "draw door" function, but I'm lazy.
        endPos = (startPos[0]+(horizontalLineLength // 2) - horizontalGap, startPos[1])
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, startPos, endPos, width)
        #Draw little vertical dashes to mark doors
        verticalStart = (endPos[0], endPos[1] - verticalLineLength//16) 
        verticalEnd = (endPos[0], endPos[1] + verticalLineLength//16) 
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, verticalStart, verticalEnd, width) 
        #Each side of the gap contributes equally to the width of the gap.
        originalStart = startPos
        startPos = (endPos[0] + 2*horizontalGap, endPos[1])
        endPos = (originalStart[0]+horizontalLineLength, originalStart[1])
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, startPos, endPos, width)
        #Draw little horizontal dash to mark door
        verticalStart = (startPos[0], startPos[1] - verticalLineLength//16) 
        verticalEnd = (startPos[0], startPos[1] + verticalLineLength//16) 
        pygame.draw.line(mapSurface, universal.LIGHT_GREY, verticalStart, verticalEnd, width) 

    def draw_player(self, bottomLeft, width, height, mapSurface):
        playerInitial = universal.state.player.name[0].upper()
        self.draw_icon(playerInitial, bottomLeft, width, height, mapSurface)

    def draw_icon(self, icon, bottomLeft, width, height, mapSurface, color=universal.LIGHT_GREY, center=True):
        x, y = bottomLeft
        font = pygame.font.SysFont(universal.FONT_LIST_TITLE, universal.DEFAULT_SIZE)
        fontWidth, fontHeight = font.size(icon)
        try:
            heightRatio = height / fontHeight
        except TypeError:
            pass
        else:
            font = pygame.font.SysFont(universal.FONT_LIST_TITLE, int(math.floor(universal.DEFAULT_SIZE * (10 * heightRatio/11))))
            fontWidth, fontHeight = font.size(icon)
        iconSurface = font.render(icon, True, color)
        if center:
            coordinate = (x + (width // 2 - fontWidth // 2), y - height + 1)
        else:
            coordinate = bottomLeft
        mapSurface.blit(iconSurface, coordinate)

    def compute_visible_area(self, dungeonWidth, dungeonHeight):
        """
        Returns a set of coordinates that the player should be able to see.
        """
        visibility = self.dungeonMap[self.coordinates[0]].visibility
        visibleSquares = set()
        lookingEastWest = True
        lookingNorthSouth = True
        firstZero = False
        for i in range(0, -visibility, -1) + range(0, visibility):
            if not i and firstZero:
                lookingEastWest = True
                lookingNorthSouth = True
            else:
                firstZero = True
                floor = self.coordinates[0]
                if lookingEastWest:
                    eRow, eColumn = (self.coordinates[1], (self.coordinates[2] + i) % dungeonWidth)
                    eastWestSquare = self[floor][eRow][eColumn]
                    if '|' in eastWestSquare or ';' in eastWestSquare or '#' in eastWestSquare:
                        lookingEastWest = False
                        if i < 0:
                            visibleSquares.add((floor, eRow, eColumn))
                    else:
                        visibleSquares.add((floor, eRow, eColumn))
                if lookingNorthSouth:
                    nRow, nColumn = ((self.coordinates[1] + i) % dungeonHeight, self.coordinates[2])
                    northSouthSquare = self[floor][nRow][nColumn]
                    if '_' in northSouthSquare or '.,' in northSouthSquare or '%' in northSouthSquare: 
                        lookingNorthSouth = False
                        if i < 0:
                            visibleSquares.add((floor, nRow, nColumn))
                    else:
                        visibleSquares.add((floor, nRow, nColumn))
        return visibleSquares


    def display_coordinate_rect(self):
        coordTopLeft = coordinateSurface.get_rect().topleft
        z, y, x = self.coordinates
        universal.say_title(str((z, x, y)), coordinateSurface)
        flush_text(13)
        coordinateRect = pygame.Rect(coordTopLeft, (coordinateSurface.get_rect().width, coordinateSurface.get_rect().height))
        pygame.draw.rect(coordinateSurface, LIGHT_GREY, coordinateRect, 5)
        return coordinateRect
    
    def display_map(self, clearScreen, previousCoordinates):
        """
        Displays the auto-map of the current floor, showing what's been explored so far.
        """
        worldView = universal.get_world_view()
        coordinateRect = self.display_coordinate_rect()
        currentFloor = self.dungeonMap[self.coordinates[0]]
        dungeonHeight = currentFloor.height
        dungeonWidth = currentFloor.width
        viewWidth, viewHeight = worldView.width, worldView.height - coordinateRect.height // 2
        if not self.mapSurface:
            self.mapSurface = pygame.Surface((viewWidth, viewHeight))
            clearScreen = True
        mapSurface = self.mapSurface
        #If we're changing floors, then we need to redraw everything.
        if previousCoordinates and self.coordinates[0] != previousCoordinates[0]:
            clearScreen = True
        if clearScreen:
            universal.clear_world_view()
            mapSurface.fill(universal.DARK_GREY)
            self.drawnSquares = set()
        #originY -= verticalLineLength
        #originY -= universal.COMMAND_VIEW_LINE_WIDTH // 2
        font = pygame.font.SysFont(universal.FONT_LIST_TITLE, universal.DEFAULT_SIZE)
        rowNumberWidth, rowNumberHeight = font.size(str(dungeonWidth))
        columnNumberWidth, columnNumberHeight = font.size(str(dungeonHeight))
        viewHeight = viewHeight - 2 * columnNumberHeight 
        viewWidth = viewWidth - 2 * rowNumberWidth
        verticalLineLength = viewHeight // dungeonHeight
        horizontalLineLength = viewWidth // dungeonWidth
        originX, originY = (worldView.left + rowNumberWidth, worldView.bottom - columnNumberHeight - coordinateRect.height // 2)
        originY -= verticalLineLength
        originY -= universal.COMMAND_VIEW_LINE_WIDTH // 2
        rowLeftX, rowBottomY = (worldView.left, .99 * originY + universal.COMMAND_VIEW_LINE_WIDTH // 3)
        columnLeftX, columnTopY = (worldView.left + rowNumberWidth + horizontalLineLength // 2 - columnNumberWidth // 3, worldView.top)
        rowRightX = worldView.right - rowNumberWidth
        columnBottomY = originY - columnNumberHeight 
        #number rows
        #Don't need to track dirtyRects, because clearScreen means the entire worldview gets redrawn.
        if clearScreen:
            for i in range(dungeonWidth):
                self.draw_icon(str(i), (rowLeftX, rowBottomY), None, None, mapSurface, center=False)
                self.draw_icon(str(i), (rowRightX, rowBottomY), None, None, mapSurface, center=False)
                rowBottomY -= verticalLineLength
        #bottomY = worldView.bottomleft[1]
        #number columns
        if clearScreen:
            for i in range(dungeonHeight):
                self.draw_icon(str(i), (columnLeftX, columnTopY), None, None, mapSurface, center=False)
                #self.draw_icon(str(i), (columnLeftX, columnBottomY), None, None, mapSurface, center=False)
                columnLeftX += horizontalLineLength
        screen = universal.get_screen()
        visitedSquares = {square for square in self.visitedSquares if square[0] == self.coordinates[0]}
        VERTICAL_GAP = verticalLineLength // 6
        HORIZONTAL_GAP = horizontalLineLength // 6
        if clearScreen:
            for y in range(dungeonHeight):
                for x in range(dungeonWidth):
                    pygame.draw.rect(mapSurface, universal.DARK_SLATE_GREY, pygame.Rect(originX + horizontalLineLength * x, originY - verticalLineLength * y, 
                        horizontalLineLength, verticalLineLength), 1)
        LINE_WIDTH = 2
        #For some strange reason that I don't understand, I need to offset originY by the verticalLineLength in order to make the map display correctly, but then
        #I need to undo that offset in order to get the visited squares to display correctly. Goddammit I hate graphics programming.
        originY += verticalLineLength
        if previousCoordinates:
            try:
                self.drawnSquares.remove(previousCoordinates)
            except KeyError:
                pass
        try:
            self.drawnSquares.remove(self.coordinates)
        except KeyError:
            pass
        #Only care about visible squares on the current floor.
        self.visibleSquares |= visitedSquares | self.compute_visible_area(dungeonWidth, dungeonHeight)
        visibleSquares = {square for square in self.visibleSquares if square[0] == self.coordinates[0]}
        squaresToDraw = visibleSquares - self.drawnSquares
        dirtyRects = []
        for z, y, x in squaresToDraw:
            square = dungeon[z][y][x]
            self.drawnSquares.add((z, y, x))
            eastSquare = dungeon[z][y][(x+1) % dungeonWidth]
            northSquare = dungeon[z][(y+1) % dungeonHeight][x]
            startPos = (originX + x * horizontalLineLength, originY - y * verticalLineLength)
            eastPos = (startPos[0] + horizontalLineLength, startPos[1])
            northPos = (startPos[0], startPos[1]-verticalLineLength)
            #Colors the squares based on events.
            icon = None
            if has_char('e' , square):
                #Note: Will actually want to draw the letter 'e' instead of coloring the square. Similar for the stairs, we'll want to insert the numbers.
                color = universal.GOLD
                icon = 'e'
            elif has_char('s', square):
                color = universal.ORANGE
                icon = 's'
            elif has_char('d', square):
                color = universal.ORANGE
                icon = str(self.coordinates[0]-1)
            elif has_char('u', square):
                color = universal.ORANGE
                icon = str(self.coordinates[0]+1)
            elif has_char('*', square):
                color = universal.ORANGE
                icon = '*'
            elif has_char('!', square):
                color = universal.ORANGE
                icon = '!'
            elif (z, y, x) in visitedSquares:
                color = universal.DARK_BLUE
            else:
                color = universal.DARK_GREY
            leftTop = (startPos[0]+LINE_WIDTH, startPos[1]-verticalLineLength+LINE_WIDTH)
            widthHeight = (horizontalLineLength-LINE_WIDTH, verticalLineLength-LINE_WIDTH)
            squareRect = Rect(leftTop, widthHeight)
            mapSurface.fill(color, squareRect)
            '''
            If I don't have both of these, then sometimes walls along the southern wall aren't drawn properly. It probably has something to do with the 
            fact that the wall are right on the edge of the updated triangle, so they aren't always properly drawn, depending on whether pygame considers it to
            be inclusive or not. Or something. Or maybe I'm just incompetent. Regardless, making both of these rects dirty ensures proper wall drawing.
            '''
            dirtyRects.append(pygame.Rect((startPos[0], startPos[1]-verticalLineLength), (horizontalLineLength, verticalLineLength)))
            dirtyRects.append(pygame.Rect((startPos[0], startPos[1]), (horizontalLineLength, verticalLineLength)))
            if icon and (z, y, x) != self.coordinates:
                self.draw_icon(icon, (originX + horizontalLineLength * x, originY - verticalLineLength * y), horizontalLineLength, verticalLineLength, mapSurface)
            #Draws the walls.
            if has_char('|', eastSquare):
                self.draw_vertical_line(eastPos, verticalLineLength, mapSurface, LINE_WIDTH)
                dirtyRects.append(pygame.Rect((eastPos[0], eastPos[1] - verticalLineLength), (horizontalLineLength, verticalLineLength)))
            elif has_char(';', eastSquare):
                self.draw_vertical_door(eastPos, horizontalLineLength, verticalLineLength, VERTICAL_GAP, mapSurface, LINE_WIDTH)
                dirtyRects.append(pygame.Rect((eastPos[0], eastPos[1] - verticalLineLength), (horizontalLineLength, verticalLineLength)))
            if has_char('|', square):
                self.draw_vertical_line(startPos, verticalLineLength, mapSurface, LINE_WIDTH)
            elif has_char(';', square):
                self.draw_vertical_door(startPos, horizontalLineLength, verticalLineLength, VERTICAL_GAP, mapSurface, LINE_WIDTH)
            if has_char('_', square):
                self.draw_horizontal_line(startPos, horizontalLineLength, mapSurface, LINE_WIDTH)
            elif has_char('.,', square):
                self.draw_horizontal_door(startPos, horizontalLineLength, verticalLineLength, HORIZONTAL_GAP, mapSurface, LINE_WIDTH)
                dirtyRects.append(pygame.Rect((startPos[0], startPos[1]), (horizontalLineLength, verticalLineLength)))
            if has_char('_', northSquare):
                self.draw_horizontal_line(northPos, horizontalLineLength, mapSurface, LINE_WIDTH)
                dirtyRects.append(pygame.Rect(northPos, (horizontalLineLength, verticalLineLength)))
            elif has_char('.,', northSquare):
                self.draw_horizontal_door(northPos, horizontalLineLength, verticalLineLength, HORIZONTAL_GAP, mapSurface, LINE_WIDTH)
                dirtyRects.append(pygame.Rect(northPos, (horizontalLineLength, verticalLineLength)))
        z, y, x = self.coordinates
        self.draw_player((originX + horizontalLineLength * x, originY - verticalLineLength * y), horizontalLineLength, verticalLineLength, mapSurface)
        dirtyRects.append(pygame.Rect((originX + horizontalLineLength * x, originY - verticalLineLength * y), (horizontalLineLength, verticalLineLength)))
        screen.blit(mapSurface, worldView) 
        screen.blit(coordinateSurface, (worldView.midbottom[0] - coordinateRect.width // 2, worldView.midbottom[1] - coordinateSurface.get_rect().height))
        #If we've had to redraw the entire screen, then the entire worldview needs to be redrawn. Otherwise, we just redraw what changed.
        if clearScreen:
            dirtyRects = [worldView]
        dirtyRects.append(pygame.Rect((worldView.midbottom[0] - coordinateRect.width // 2, worldView.midbottom[1] - coordinateSurface.get_rect().height),
            (coordinateRect.width, coordinateRect.height)))
        return dirtyRects

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Dungeon Data:", data])

    def save(self):
        saveData = [super(Dungeon, self).save(), "Room Data:", "Dungeon Only:"]
        Dungeon.add_data(str(self.direction), saveData)
        Dungeon.add_data(str(self.coordinates), saveData)
        Dungeon.add_data('\n'.join([str(visited) for visited in self.visitedSquares]), saveData)
        Dungeon.add_data('\n'.join([str(visible) for visible in self.visibleSquares]), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(loadData, room):
        data = loadData.split("Dungeon Data:")
        try:
            _, direction, coordinates, visited, visible = data
        except ValueError:
            try:
                _, direction, coordinates, visited = data
            except ValueError:
                _, direction, coordinates = data
                visited = ''
            visible = ''
        room.direction = int(direction.strip())
        coordinates = coordinates.replace('(', '').replace(')', '')
        coordinates = coordinates.split(',')
        room.coordinates = tuple(int(coord.strip()) for coord in coordinates)
        try:
            visited = [coordinate.strip() for coordinate in visited.split('\n') if coordinate.strip()]
        except ValueError:
            visited = []
        try:
            visible = [coordinate.strip() for coordinate in visible.split('\n') if coordinate.strip()]
        except ValueError:
            visible = []
        room.visitedSquares = set()
        room.visitedSquares = {tuple(int(s) for s in t[1:-1].split(',')) for t in visited}
        room.visitedSquares.add(room.coordinates)
        room.visibleSquares = set()
        room.visibleSquares = {tuple(int(s) for s in t[1:-1].split(',')) for t in visible}
        room.visibleSquares.add(room.coordinates)
        room.drawnSquares = set()

    def exit_dungeon(self):
        """
        This function performs any necessary clean up that's needed when leaving the dungeon.
        """
        self.coordinates = (-1, -1, -1)
    def floor(self):
        return self.coordinates[0]

    def mode(self, sayDescription=True):
        global dungeon
        dungeon = self
        return dungeon_mode()

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(saveText):
        raise NotImplementedError()

    def __getitem__(self, key):
        return self.dungeonMap[key]

    def __len__(self):
        return len(self.dungeonMap)

    def set_dungeon_map(self, dungeonMap):
        self.dungeonMap = []
        for floor in dungeonMap:
            self.dungeonMap.append(floor if type(floor) == DungeonFloor else DungeonFloor(floor))

    def set_dungeon_events(self, dungeonEvents):
        self.dungeonEvents = []
        for floorEvents in dungeonEvents:
            self.dungeonMap.append(floorEvents if type(floorEvents) == FloorEvents else FloorEvents(floorEvents))

    def display(self, clear=True, previousCoordinates=None):
        """
        a. "|" - This square has a wall to the east
        b. "_" - This square has a wall to the south
        c. "*" - A special event occurs at this spot.
        d. ";" - This square has a door to the east.
        e. ":" - This square has a secret door to the east.
        f. ".," - This square has a door to the south.
        g. ".." - This square has a secret door to the south.
        h. d - This square has a passage from the current floor to the floor immediately below.
        i. u - This square has a passage from the current floor to the floor immediately above.
        j. "!" - This square has a guaranteed random encounter
        k. "s" - Start square
        l. "e" - Exit Square
        m. "%" - Darkness to the south
        n. "#" - Darkness to the west
        o. "-" - Invisible wall to the south
        p. "^" - Invisible wall to the west

        The argument clear is a Boolean that tells us whether we need to clear the screen before drawing the automap or not.
        """
        set_command_interpreter(dungeon_interpreter)
        set_dungeon_commands(self)
        dirtyRects = self.display_map(clear, previousCoordinates)
        return dirtyRects

    def print_visible_column(self, visibleArea):
        mapColumn = []
        for va in visibleArea:
            if va is not None:
                mapColumn.append([dir_name(key) + ": " + str(va[key]) for key in va.keys()])
            else:
                mapColumn.append(['None'])
        return ' '.join(['{' + ', '.join(column) + '}' for column in mapColumn])

    def display_event(self, previousCoordinates=None):
        floor = self.coordinates[0]
        row = self.coordinates[1]
        column = self.coordinates[2]
        square = self[floor][row][column]
        event = False
        global changingFloors
        changingFloors = 0
        set_dungeon_commands(self)
        if ((has_char('*', square) or has_char('s', square))) and self.dungeonEvents[floor][row][column]: #and (floor, row, column) not in self.visitedSquares:
            event = self.dungeonEvents[floor][row][column]()
            if event:
                universal.clear_world_view()
        elif has_char('!', square):
            event = True
            self.encounter()
        elif has_char('x', square) and not universal.state.is_clear((floor, row, column)):
            def clear_encounter(x, y, z):
                #These three are just dummy arguments that are used because the combat function expects the postCombatEvent to have three arguments.
                universal.state.clear_encounter((floor, row, column))

            event = True
            enemies = None
            if self.dungeonEvents[floor][row][column]:
                #One time combat events have associated with them a function that returns the list of enemies to be battled.
               enemies = self.dungeonEvents[floor][row][column]()
            self.encounter(clear_encounter, enemies)
        if has_char('e', square):
            universal.set_commands(get_commands())
            if self.dungeonEvents[floor][row][column]: #and (floor, row, column) not in self.visitedSquares:
                universal.clear_world_view()
                event = self.dungeonEvents[floor][row][column]()
        if has_char('u', square):
            changingFloors = 1
            universal.set_commands(get_commands())
        if has_char('d', square):
            changingFloors = -1
            universal.set_commands(get_commands())
        #if not event and random.randint(0, 99) < self[floor].encounterRate:
            #self.encounter()
        self.visitedSquares.add(self.coordinates)
        if not event:
            return self.display(False, previousCoordinates)

    def encounter(self, afterCombatEvent=None, encounteredEnemies=None):
        currentFloor = self.dungeonMap[self.coordinates[0]]
        if not encounteredEnemies:
            numEnemies = random.randint(1, currentFloor.maxEnemies)
            encounteredEnemies = []
            for i in range(numEnemies):
                gender = random.randint(0, 1)
                encounteredEnemies.append(currentFloor.enemies[random.randrange(0, len(currentFloor.enemies))](gender, identifier=i+1))
        ambush = random.randint(1, 100)
        ambushFlag = 0
        avgPartyStealth = person.get_party().avg_speed()
        avgEnemyStealth = mean([enemy.speed() for enemy in encounteredEnemies])
        if ambush <= currentFloor.ambushChance + abs(avgPartyStealth - avgEnemyStealth):
            partyAmbushes = random.random() * avgPartyStealth 
            enemyAmbushes = random.random() * avgEnemyStealth
            if enemyAmbushes < partyAmbushes:
                ambushFlag = 1
            elif partyAmbushes < enemyAmbushes:
                ambushFlag = -1
        import combat
        #combat.fight(encounteredEnemies, afterCombatEventIn=post_combat_spanking, ambushIn=ambushFlag) 
        combat.fight(encounteredEnemies, ambushIn=ambushFlag, randomEncounterIn=True, coordinatesIn=self.coordinates) 

    def move(self, key):
        """
        Moves the character through the dungeon, depending on the direction key pressed.
        """
        party = person.get_party()
        previousCoordinates = self.coordinates
        if key == K_d:
            self.coordinates = (self.coordinates[0]-1, self.coordinates[1], self.coordinates[2])
        elif key == K_u:
            self.coordinates = (self.coordinates[0]+1, self.coordinates[1], self.coordinates[2])
        else:
            dungeonHeight = self[self.coordinates[0]].height
            dungeonWidth = self[self.coordinates[0]].width
            if key == K_UP:
                movement = 1
                direction = NORTH
                currentSquare = self.get_square((self.coordinates[0], (self.coordinates[1] + 1) % dungeonHeight, self.coordinates[2]))
            elif key == K_DOWN:
                movement = -1
                direction = SOUTH
                currentSquare = self.current_square()
            elif key == K_RIGHT:
                movement = 1
                direction = EAST
                currentSquare = self.get_square((self.coordinates[0], self.coordinates[1], (self.coordinates[2] + 1) % dungeonWidth))
            elif key == K_LEFT:
                movement = -1
                direction = WEST
                currentSquare = self.current_square()
            if (direction == NORTH or direction == SOUTH) and not has_char('_', currentSquare) and not has_char('-', currentSquare):
                self.coordinates = (self.coordinates[0], (self.coordinates[1] + movement) % dungeonHeight, self.coordinates[2])
            elif (direction == EAST or direction == WEST) and not has_char('|', currentSquare) and not has_char('^', currentSquare):
                self.coordinates = (self.coordinates[0], self.coordinates[1], (self.coordinates[2] + movement) % dungeonWidth)
            #stepEffect.play()      
        complete_dungeon_action()
        displayRects = self.display_event(previousCoordinates)
        return displayRects
            

    def get_square(self, coordinate):
        floor = coordinate[0] % len(self)
        row = coordinate[1] % len(self[floor])
        column = coordinate[2] % len(self[floor][row])
        return self.dungeonMap[floor][row][column]

    def current_square(self):
        return self.get_square(self.coordinates)

def complete_dungeon_action():
    """
    This function should be called after each complete dungeon action (walking or casting spells).
    """
    party = person.get_party()
    for char in party:
        char.decrement_statuses()

def mean(listNums):
    total = 0
    for i in listNums:
        total += i
    return i // len(listNums)


defeatedEnemies = []
def post_combat_spanking(allies, enemies, won):
    say_title("Spanking Time")
    universal.say('Select an enemy to spank:\n')
    universal.say('\n'.join(numbered_list([enemy.printedName for enemy in enemies])))
    universal.set_commands(['(#) Select an enemy.', '(Esc) To not spank anyone'])
    set_command_interpreter(post_combat_spanking_interpreter)
    global defeatedEnemies
    defeatedEnemies = enemies

def post_combat_spanking_interpreter(keyEvent):
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(defeatedEnemies):
            text = defeatedEnemies[num].post_combat_spanking()
            universal.say(text, justification=0)
            acknowledge(dungeon_mode, ())
    elif keyEvent.key == K_ESCAPE:
        dungeon_mode()


def has_symbol(char, square):
    return char in square

def set_dungeon(dungeonIn):
    global dungeon
    dungeon = dungeonIn

changingFloors = 0
def dungeon_interpreter(keyEvent):
    global dungeon
    dirtyRects = None
    #if dungeon is not None:
    floor = dungeon.coordinates[0]
    row = dungeon.coordinates[1]
    column = dungeon.coordinates[2]
    square = dungeon[floor][row][column]
    if keyEvent.key == K_ESCAPE:
        townmode.confirm_quit(dungeon_mode)
    elif keyEvent.key == K_s:
        townmode.save(dungeon_mode)
    elif keyEvent.key == K_l:
        townmode.load(dungeon_mode)
    elif keyEvent.key == K_q:
        townmode.save_game('quick', dungeon_mode)
    elif keyEvent.key == K_i:
        townmode.confirm_title_screen(dungeon_mode)
    elif keyEvent.key == K_c:
        clear_screen()
        select_character_to_cast()
    elif keyEvent.key == K_p:
        universal.set_commands(['(#)Character', '<==Back'])
        clear_screen()
        say_title('Party:')
        universal.say('\t'.join(['Name:', 'Health:', 'Mana:\n\t',]), columnNum=3)
        universal.say(universal.state.party.display_party(), columnNum=3)
        set_command_interpreter(select_character_interpreter)
    elif keyEvent.key == K_d and changingFloors == -1:
        dungeon.move(K_d)
        dirtyRects = [universal.get_world_view()]
    elif keyEvent.key == K_u and changingFloors == 1:
        dirtyRects = dungeon.move(K_u)
    elif keyEvent.key in universal.ARROW_KEYS:
        dirtyRects = dungeon.move(keyEvent.key)
    elif keyEvent.key == K_g:
        dungeon.go()
    elif keyEvent.key == K_e and has_char('s', dungeon[floor][row][column]):
        try:
            townmode.go(dungeon.adjacent[0])
        except IndexError:
            pass
        else:
            universal.clear_screen()
    return dirtyRects

def select_character_interpreter(keyEvent):
    party = person.get_party()
    if keyEvent.key == K_BACKSPACE:
        dungeon_mode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        try:
            per = party.members[num-1]
        except IndexError:
            return
        clear_screen()
        per.character_sheet(dungeon_mode)

def select_character_to_cast():
    universal.set_commands(['(#)Character', '<==Back'])
    clear_screen()
    say_title('Select Character to Cast Spell:')
    universal.say('\t'.join(['Name:', 'Health:', 'Mana:\n\t',]), columnNum=3)
    universal.say(universal.state.party.display_party(), columnNum=3)
    set_command_interpreter(select_character_to_cast_interpreter)

selectedSlinger= None
def select_character_to_cast_interpreter(keyEvent):
    party = person.get_party()
    if keyEvent.key == K_BACKSPACE:
        dungeon_mode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if num > 0:
            char = party.members[num-1]
            clear_screen()
            global selectedSlinger
            selectedSlinger = char
            char.display_tiers(display_tiers_interpreter_dungeon)

def display_tiers_interpreter_dungeon(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        select_character_to_cast()
    if keyEvent.key in NUMBER_KEYS:
        playerInput = int(pygame.key.name(keyEvent.key))
        display_spells(playerInput)

availableSpells = None
chosenTier = None
def display_spells(tier):
    global chosenTier
    chosenTier = tier
    if chosenTier > selectedSlinger.tier:
        return
    say_title('Available Spells')
    global availableSpells
    try:
        availableSpells = [spell for spell in selectedSlinger.spellList[tier] if spell.castableOutsideCombat and spell.cost <= selectedSlinger.current_mana()]
    except TypeError:
        availableSpells = [' '.join([selectedSlinger.printedName, 'does not know any spells of this tier.'])]
    try:
        say('\n'.join(universal.numbered_list([spell.name for spell in availableSpells])))
    except AttributeError:
        say(availableSpells[0])
        acknowledge(selectedSlinger.display_tiers, display_tiers_interpreter_dungeon)
    else:
        universal.set_commands(['(#) Select a spell.', '<==Back'])
        set_command_interpreter(select_spell_interpreter)

chosenSpell = None
def select_spell_interpreter(keyEvent):
    global chosenSpell
    if keyEvent.key == K_BACKSPACE:
        selectedSlinger.display_tiers(display_tiers_interpreter_dungeon)
    elif keyEvent.key in NUMBER_KEYS:
        playerInput = int(pygame.key.name(keyEvent.key)) - 1
        try:
            chosenSpell = availableSpells[playerInput]
        except IndexError:
            return
        say_title(chosenSpell.name)
        say(person.get_party().display_party())
        universal.set_commands([ ' '.join(['(#) Select', str(chosenSpell.numTargets), 'target' + ('s.' if chosenSpell.numTargets > 1 else '.')]), '<==Back'])
        set_command_interpreter(select_targets_interpreter)

targetList = []
def select_targets_interpreter(keyEvent):
    party = person.get_party()
    global targetList
    if keyEvent.key == K_BACKSPACE:
        if targetList == []:
            display_spells(chosenTier)
            return
        else:
            targetList = targetList[:-1]
            numTargets = chosenSpell.numTargets - len(targetList)
            universal.set_commands([ ' '.join(['(#) Select', str(numTargets), 'target' + ('s.' if numTargets > 1 else '.')]), '<==Back'])
    elif keyEvent.key in NUMBER_KEYS:
        playerInput = int(pygame.key.name(keyEvent.key)) - 1
        try:
            targetList.append(party[playerInput])
        except IndexError:
            return
        numTargets = chosenSpell.numTargets - len(targetList)
        universal.set_commands([ ' '.join(['(#) Select', str(numTargets), 'target' + ('s.' if numTargets > 1 else '.')]), '<==Back'])
    if chosenSpell.numTargets == len(targetList):
        spellResult = chosenSpell.__class__(selectedSlinger, targetList).effect(inCombat=False, allies=person.get_party())
        selectedSlinger.uses_mana(chosenSpell.cost)
        say(spellResult[0])
        if spellResult[-1]:
            selectedSlinger.increaseStatPoints[universal.BUFF_MAGIC - universal.COMBAT_MAGIC] += chosenSpell.spell_points()
        targetList = []
        acknowledge(dungeon_mode, ())
        return
    say(person.get_party().display_party(targeted=targetList))

def confirm_cast_interpreter(keyEvent):
    #Cast spell if "y". Remove last target if "n."
    global targetList, selectedSlinger
    if keyEvent.key == K_y:
        spellResult = chosenSpell.__class__(selectedSlinger, targetList).effect(inCombat=False, allies=person.get_party())
        selectedSlinger.uses_mana(chosenSpell.cost)
        say(spellResult[0])
        targetList = []
        acknowledge(dungeon_mode, ())
    elif keyEvent.key == K_n:
        targetList = targetList[:-1]
        numTargets = chosenSpell.numTargets - len(targetList)
        universal.set_commands([ ' '.join(['(#) Select', str(numTargets), 'target' + ('s.' if numTargets > 1 else '.')]), '<==Back'])
        set_command_interpreter(select_targets_interpreter)

def start_coordinate(dungeon):
    dungeonMap = dungeon.dungeonMap
    for floor in range(len(dungeonMap)):
        for row in range(len(dungeonMap[floor])):
            for column in range(len(dungeonMap[floor][row])):
                if has_symbol("s", dungeonMap[floor][row][column]):
                    return (floor, row, column)
    raise ValueError("Start square not found.")


def has_char(char, string):
    return char in string
