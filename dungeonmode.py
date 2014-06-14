
"""
Copyright 2014 Andrew Russell

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

#stepEffect = pygame.mixer.Sound(os.path.join('data', 'step.wav'))

#TODO: Build another surface for the current facing direction.
pygame.font.init()
fontSize = pygame.font.SysFont(universal.FONT_LIST, universal.TITLE_SIZE).size(str((10,10,10)))
coordinateSurface = pygame.Surface((fontSize[0] + 20, fontSize[1] + 20))
coordinateSurface.fill(universal.DARK_GREY)
fontSize = pygame.font.SysFont(universal.FONT_LIST, universal.TITLE_SIZE).size('N')
directionSurface = pygame.Surface((fontSize[0] + (fontSize[1] - fontSize[0]), fontSize[1] + 5))
directionSurface.fill(universal.DARK_GREY)

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
    music.play_music(dungeon.bgMusic)
    if dungeon.coordinates == (-1, -1, -1):
        dungeon.coordinates = start_coordinate(dungeon)
        previousRoom = [room for room in townmode.allRooms.keys() if townmode.allRooms[room].characters is not None and 
            person.get_party()[0] in townmode.allRooms[room].characters.values()][0]
        townmode.allRooms[previousRoom].remove_characters(person.party.members)
        dungeon.add_characters(person.party.members)
        dungeon.display_event()
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
    """
        Implements a single floor. See the documentation for Dungeon for details.
        Floor should be a tuple of tuple of strings, events a list of list of functions.
    """
    def __init__(self, floor, events, visibility=4, encounterRate=5, enemies=None, maxEnemies=2, ambushChance=5):
        self.floor = floor
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
        Converts this dungeon's map into a three dimensional list, where each square consists of a map containing five items:
        1. HERE - Contains information about any special events (*, s, e, d, u) on the square the player is standing on.
        2. NORTH - Contains information about any walls, doors, and stairs on the square one to the north of this one.
        3. SOUTH, EAST, WEST - See 2.
        """
        convertedMap = []
        convertedMap.extend([[] for i in range(len(self))])
        count = len(self) - 1
        for row in range(len(self)):
            for column in range(len(self[row])):
                square = self.floor[row][column]
                data = {NORTH:'', SOUTH:'', EAST:'', WEST:'', HERE:''}
                data[WEST] = self[row][column]
                data[EAST] = self[row][(column+1) % len(self[row])]
                data[NORTH] = self[(row+1) % len(self.floor)][column]
                data[SOUTH] = self[row][column]
                data[HERE] = self[row][column]
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
    def __init__(self, name, dungeonMap, dungeonEvents, direction=NORTH, description="", visibility=[], adjacent=None, characters=None, after_arrival=None,
            bgMusic=None, enemies=None, maxEnemies=None, ambushChance=None):
        super(Dungeon, self).__init__(name, description, adjacent, characters, after_arrival, bgMusic)
        self.direction = direction
        self.coordinates = (-1, -1, -1)
        self.dungeonMap = {}
        count = 0
        self.dungeonEvents = {}
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
            for floor in dungeonMap:
                if visibility == []:
                    self.dungeonMap[count] = floor if type(floor) == DungeonFloor else DungeonFloor(floor, self.dungeonEvents[count])
                else:
                    self.dungeonMap[count] = floor if type(floor) == DungeonFloor else DungeonFloor(floor, self.dungeonEvents[count], visibility[count])
                if enemies is not None:
                    self.dungeonMap[count].enemies = enemies
                if maxEnemies is not None:
                    self.dungeonMap[count].maxEnemies = maxEnemies
                if ambushChance is not None:
                    self.dungeonMap[count].ambushChance = ambushChance
                count += 1
                    

    def exit_dungeon(self):
        """
        This function performs any necessary clean up that's needed when leaving the dungeon.
        """
        self.coordinates = (-1, -1, -1)
    def floor(self):
        return self.coordinates[0]

    def mode(self, sayDescription=True):
        return dungeon_mode()

    def _save(self):
        global dungeon
        saveText = super(Dungeon, self)._save()
        saveText = saveText.split('\n')
        saveText.insert(-2, 'coordinate= ' + ''.join(['(', ','.join([str(coord) for coord in self.coordinates]), ')']))
        saveText.insert(-2, 'direction= ' + str(self.direction))
        saveText.insert(-2, 'dungeon= ' + str(dungeon.name))
        return '\n'.join(saveText)

    @staticmethod
    def _load(saveText):
        thisDungeon = townmode.Room._load(saveText)
        for line in saveText:
            line = line.split()
            if line[0] == 'coordinate=':
                thisDungeon.coordinates = ast.literal_eval(line[1])
            elif line[0] == 'direction=':
                thisDungeon.direction = int(line[1])
            elif line[0] == 'dungeon=':
                global dungeon
                dungeon = townmode.allRooms[line[1]]
        return thisDungeon

    def __getitem__(self, key):
        return self.dungeonMap[key]

    def __len__(self):
        return len(self.dungeonMap)

    def set_dungeon_map(self, dungeonMap):
        self.dungeonMap = []
        for floor in dungeonMap:
            self.dungeonMap.append(floor if type(floor) == DungeonFloor else DungeonFloor(floor))

    def set_dungeon_events(dungeonEvents):
        self.dungeonEvents = []
        for floorEvents in dungeonEvents:
            self.dungeonMap.append(floorEvents if type(floorEvents) == FloorEvents else FloorEvents(floorEvents))

    def look(self, sqsAhead, lineCoordinates):
        pass
 
    def display_squares(self):
        pass

    def display(self):
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
        """
        set_command_interpreter(dungeon_interpreter)
        clear_screen()
        if not '(P)arty' in get_commands():
            set_commands(['(P)arty', '(S)ave', '(Q)uick Save', '(L)oad', 't(I)tle Screen', '(Esc)Quit'])
        #First, we build a 3 x visibility grid of all the potentially visible squares.
        visibleArea = ([], [], [])
        floor = self.coordinates[0]
        row = self.coordinates[1]
        column = self.coordinates[2]
        if self.direction == NORTH or self.direction == EAST:
            d = 1
        elif self.direction == SOUTH or self.direction == WEST:
            d = -1
        if self.direction == NORTH or self.direction == SOUTH:
            #Note: visibleArea[0] still has the squares to the west, and visibleArea[1] has the squares to the east, regardless of whether the player is facing north or
            #south.
            for i in range(self[floor].visibility):
                visibleArea[0].append(self.get_square((floor, row + d * i, column - 1)))
                visibleArea[1].append(self.get_square((floor, row + d * i, column)))
                visibleArea[2].append(self.get_square((floor, row + d * i, column + 1)))
        elif self.direction == WEST or self.direction == EAST:
            #Note: visibleArea[0] still has the squares to the south, and visibleArea[1] has the squares to the north, regardless of whether the player is facing east or
            #west.
            for i in range(self[floor].visibility):
                visibleArea[0].append(self.get_square((floor, row - 1, column + d * i)))
                visibleArea[1].append(self.get_square((floor, row, column + d * i)))
                visibleArea[2].append(self.get_square((floor, row + 1, column + d * i)))
        #Now we go through and replace each square with None if there's a wall or door in the way.
        for i in range(self[floor].visibility):
            mySquare = visibleArea[1][i]
            #print(self.print_visible_column(visibleArea[1]))
            if mySquare is not None:
                if self.direction == NORTH or self.direction == SOUTH:
                    if has_char('|', mySquare[WEST]) or has_char(':', mySquare[WEST]) or has_char(';', mySquare[WEST]):
                        visibleArea[0][i] = None
                    if has_char('_', mySquare[self.direction]) or has_char('..', mySquare[self.direction]) or has_char('.,', mySquare[self.direction]) or \
                        has_char('%', mySquare[self.direction]):
                            for j in range(i+1, self[floor].visibility):
                                visibleArea[1][j] = None
                    if has_char('|', mySquare[EAST]) or has_char(':', mySquare[EAST]) or has_char(';', mySquare[EAST]):
                        visibleArea[2][i] = None
                elif self.direction == EAST or self.direction == WEST:
                    if has_char('_', mySquare[NORTH]) or has_char('..', mySquare[NORTH]) or has_char('.,', mySquare[NORTH]):
                        visibleArea[0][i] = None
                    if has_char('|', mySquare[self.direction]) or has_char(':', mySquare[self.direction]) or has_char(';', mySquare[self.direction]) or \
                        has_char('#', mySquare[self.direction]):
                            for j in range(i+1, self[floor].visibility):
                                visibleArea[1][j] = None
                    if has_char('_', mySquare[SOUTH]) or has_char('..', mySquare[SOUTH]) or has_char('.,', mySquare[SOUTH]):
                        visibleArea[2][i] = None
                    
        #At this point, if visibleArea[i][j] does *not* have None, then we need to draw something.
        self.draw_walls(visibleArea)
        coordinate = str(self.coordinates)
        coordTopLeft = coordinateSurface.get_rect().topleft
        say_title(coordinate, surface=coordinateSurface)
        flush_text(13)
        pygame.draw.rect(coordinateSurface, LIGHT_GREY, pygame.Rect(coordTopLeft, (coordinateSurface.get_rect().width, coordinateSurface.get_rect().height + 5)), 5)
        direction = print_dir(self.direction)
        say_title(direction, surface=directionSurface)
        flush_text(13)
        pygame.draw.rect(directionSurface, LIGHT_GREY, pygame.Rect(directionSurface.get_rect().topleft, directionSurface.get_rect().size), 5)
        get_screen().blit(coordinateSurface, (get_world_view().midbottom[0] - coordinateSurface.get_rect().width // 2,
            get_world_view().midbottom[1] - coordinateSurface.get_rect().height))
        get_screen().blit(directionSurface, (get_world_view().midbottom[0] - directionSurface.get_rect().width // 2, get_world_view().midbottom[1] - 
            (coordinateSurface.get_rect().height + directionSurface.get_rect().height)))

    def print_visible_column(self, visibleArea):
        mapColumn = []
        for va in visibleArea:
            if va is not None:
                mapColumn.append([dir_name(key) + ": " + str(va[key]) for key in va.keys()])
            else:
                mapColumn.append(['None'])
        return ' '.join(['{' + ', '.join(column) + '}' for column in mapColumn])

    def draw_walls(self, visibleArea):
        """
        Visible area is a 3 x visibility grid of blocks. If a block is None, then it is not visible (and a wall needs to be drawn). If it is not None, then it is visible, 
        and needs to be handled depending on where it is.
        """
        westSouth = WEST if self.direction == NORTH or self.direction == SOUTH else SOUTH
        eastNorth = EAST if self.direction == NORTH or self.direction == SOUTH else NORTH
        leftCoordinates = ((-5, get_world_view().height // 40), (0, 39 * get_world_view().height // 40))
        pLeftCoordinates = leftCoordinates
        rightCoordinates = ((get_world_view().width+5, get_world_view().height // 40), (get_world_view().width, 39 * get_world_view().height // 40))
        pRightCoordinates = rightCoordinates
        angle = 24
        wallAngle = math.radians(angle)
        for i in range(len(visibleArea[1])):
            square = visibleArea[1][i]
            if self.direction == NORTH or self.direction == SOUTH:
                if square is not None:
                    north = self.direction == NORTH
                    coordinates = self.draw_wall(leftCoordinates if north else rightCoordinates, wallAngle, i, north, visibleArea[1][i][WEST])
                    if north:
                        pLeftCoordinates = leftCoordinates
                        leftCoordinates = coordinates
                    else:
                        pRightCoordinates = rightCoordinates
                        rightCoordinates = coordinates
                    coordinates = self.draw_wall(rightCoordinates if north else leftCoordinates, wallAngle, i, not north, visibleArea[1][i][EAST])
                    if north:
                        pRightCoordinates = rightCoordinates
                        rightCoordinates = coordinates
                    else:
                        pLeftCoordinates = leftCoordinates
                        leftCoordinates = coordinates
                    #Drawing wall right in front.       
                    if has_char('_', square[self.direction]) or has_char('..', square[self.direction]):
                        pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(leftCoordinates[0], (rightCoordinates[0][0] - leftCoordinates[0][0], 
                            leftCoordinates[1][1] - leftCoordinates[0][1])), 5)
                    elif has_char('.,', square[self.direction]):
                        pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(leftCoordinates[0], (rightCoordinates[0][0] - leftCoordinates[0][0], 
                            leftCoordinates[1][1] - leftCoordinates[0][1])), 5)
                        pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(leftCoordinates[0][0] + 20, rightCoordinates[0][1] + 20, 
                            rightCoordinates[0][0] - leftCoordinates[0][0] - 40, leftCoordinates[1][1] - leftCoordinates[0][1] - 40), 5)
                    #Drawing events
                    eventSquare = visibleArea[1][i][HERE]
                    self.draw_events(leftCoordinates, rightCoordinates, pLeftCoordinates, pRightCoordinates, eventSquare)
                            
            elif self.direction == EAST or self.direction == WEST:
                if square is not None:
                    east = self.direction == EAST
                    coordinates = self.draw_wall(leftCoordinates if east else rightCoordinates, wallAngle, i, east, visibleArea[1][i][NORTH])
                    if east:
                        pLeftCoordinates = leftCoordinates
                        leftCoordinates = coordinates
                    else:
                        pRightCoordinates = rightCoordinates
                        rightCoordinates = coordinates
                    coordinates = self.draw_wall(rightCoordinates if east else leftCoordinates, wallAngle, i, not east, visibleArea[1][i][SOUTH])
                    if east:
                        pRightCoordinates = rightCoordinates
                        rightCoordinates = coordinates
                    else:
                        pLeftCoordinates = leftCoordinates
                        leftCoordinates = coordinates
                    #Drawing square in front
                    if has_char('|', square[self.direction]) or has_char(':', square[self.direction]):
                        pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(leftCoordinates[0], (rightCoordinates[0][0] - leftCoordinates[0][0], 
                            leftCoordinates[1][1] - leftCoordinates[0][1])), 5)
                    elif has_char(';', square[self.direction]):
                        pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(leftCoordinates[0], (rightCoordinates[0][0] - leftCoordinates[0][0], 
                            leftCoordinates[1][1] - leftCoordinates[0][1])), 5)
                        pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(leftCoordinates[0][0] + 20, rightCoordinates[0][1] + 20, 
                            rightCoordinates[0][0] - leftCoordinates[0][0] - 40, leftCoordinates[1][1] - leftCoordinates[0][1] - 40), 5)
                    #Drawing events
                    eventSquare = visibleArea[1][i][HERE]
                    self.draw_events(leftCoordinates, rightCoordinates, pLeftCoordinates, pRightCoordinates, eventSquare)

    def draw_events(self, leftCoordinates, pLeftCoordinates, pRightCoordinates, rightCoordinates, square):
        top = False
        bottom = False
        if has_char('e', square):
            bColor = GREEN
            bottom = True
        elif has_char('d', square):
            bColor = SLATE_GREY
            bottom = True
        elif has_char('*', square) or has_char('s', square):
            bColor = BLUE
            bottom = True
        elif has_char('!', square):
            bColor = RED
            bottom = True
        if has_char('u', square):
            tColor = SLATE_GREY
            top = True
        if bottom:
            pygame.draw.line(get_screen(), bColor, leftCoordinates[1], rightCoordinates[1], 5)
            pygame.draw.line(get_screen(), bColor, pLeftCoordinates[1], pRightCoordinates[1], 5)
            #pygame.draw.line(get_screen(), bColor, leftCoordinates[1], pLeftCoordinates[1], 5)
            #pygame.draw.line(get_screen(), bColor, leftCoordinates[1], pRightCoordinates[1], 5)
            #pygame.draw.line(get_screen(), bColor, rightCoordinates[1], pLeftCoordinates[1], 5)
        if top:
            pygame.draw.line(get_screen(), tColor, leftCoordinates[0], rightCoordinates[0], 5)
            pygame.draw.line(get_screen(), tColor, pLeftCoordinates[0], pRightCoordinates[0], 5)
            #pygame.draw.line(get_screen(), tColor, leftCoordinates[0], pLeftCoordinates[0], 5)
            #pygame.draw.line(get_screen(), tColor, rightCoordinates[0], pRightCoordinates[0], 5)

    def draw_wall_help(self, start, wallAngle, stepsAhead, left, square):   
        neg = -1
        if left:
            neg = 1
        x0 = start[0][0]
        y0 = start[0][1]
        y0Prime = start[1][1]
        x1 = x0 + neg * (1/(4.5 * (stepsAhead + 1))) * get_world_view().width
        y1 = math.tan(wallAngle) * neg * (x1 - x0) + y0
        y1Prime = y0Prime - math.tan(wallAngle) * neg * (x1 - x0) 
        drawWall = False
        if (self.direction == NORTH or self.direction == SOUTH) and (has_char('|', square) or has_char(':', square)):
            drawWall = True
        elif (self.direction == EAST or self.direction == WEST) and (has_char('_', square) or has_char('..', square)):
            drawWall = True
        if drawWall:
            pygame.draw.line(get_screen(), LIGHT_GREY, (x0, y0), (x0, y0Prime), 5)
            pygame.draw.line(get_screen(), LIGHT_GREY, (x1, y1), (x1, y1Prime), 5)
            pygame.draw.line(get_screen(), LIGHT_GREY, (x0, y0), (x1, y1), 5)
            pygame.draw.line(get_screen(), LIGHT_GREY, (x0, y0Prime), (x1, y1Prime), 5)
        else:
            coordinates = self.coordinates
            if self.direction == SOUTH or self.direction == WEST:
                d = -1
            elif self.direction == NORTH or self.direction == EAST:
                d = 1
            if self.direction == NORTH or self.direction == SOUTH:
                coordinates = (coordinates[0], coordinates[1] + d * stepsAhead, coordinates[2] + d * (-1 if left else 1))
            elif self.direction == EAST or self.direction == WEST:
                coordinates = (coordinates[0], coordinates[1] + d * (1 if left else -1), coordinates[2] + d * stepsAhead)
            print('coordinates:')
            print(coordinates)
            square = self[coordinates[0]][coordinates[1]][coordinates[2]]
            print(square)

            if (self.direction == NORTH or self.direction == SOUTH) and (has_char('_', square[self.direction]) or has_char('..', square[self.direction])):
                pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x0, y1, x1 - x0, y1Prime - y1), 5)
            elif (self.direction == NORTH or self.direction == SOUTH) and has_char('.,', square[self.direction]):
                if left:
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x0, y1, x1 - x0, y1Prime - y1), 5)
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x0, y1 + 20, (x1 - x0) - 20, (y1Prime - y1) - 40), 5)
                else:
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x1, y1, x0 - x1, y1Prime - y1), 5)
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x1 + 20, y1 + 20, (x0 - x1) - 20, (y1Prime - y1) - 40), 5)

            elif (self.direction == EAST or self.direction == WEST) and (has_char('|', square[self.direction]) or has_char(':', square[self.direction])):
                print('printing wall!')
                print('self.direction:')
                print(self.direction)
                print(square[self.direction])
                pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x0, y1, x1 - x0, y1Prime - y1), 5)
            elif (self.direction == EAST or self.direction == WEST) and has_char(';', square[self.direction]):
                print('printing door!')
                if left:
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x0, y1, x1 - x0, y1Prime - y1), 5)
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x0, y1 + 20, (x1 - x0) - 20, (y1Prime - y1) - 40), 5)
                else:
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x1, y1, x0 - x1, y1Prime - y1), 5)
                    pygame.draw.rect(get_screen(), LIGHT_GREY, pygame.Rect(x1 + 20, y1 + 20, (x0 - x1) - 20, (y1Prime - y1) - 40), 5)

        return ((x1, y1), (x1, y1Prime))

    def draw_wall(self, start, wallAngle, stepsAhead, left, square):
        drawDoor = False
        if (self.direction == NORTH or self.direction == SOUTH) and has_char(';', square):
            drawDoor = True
            square += '|'
        elif (self.direction == EAST or self.direction == WEST) and has_char('.,', square):
            drawDoor = True
            square += '_'
        coordinates = self.draw_wall_help(start, wallAngle, stepsAhead, left, square)
        if drawDoor:
            neg = -1 
            if left:
                neg = 1
            x0 = start[0][0]
            y0 = start[0][1]
            y0Prime = start[1][1]
            x1 = coordinates[0][0]
            y1 = coordinates[0][1]
            y1Prime = coordinates[1][1]
            x2 = x0 + neg * 20
            y2 = y0 + 20
            y2Prime = y0Prime - 20
            m = (y1 - y0) / (x1 - x0)
            mPrime = (y1Prime - y0Prime) / (x1 - x0)
            x3 = x1 - neg * 20
            y3 = m * (x3 - x2) + y2
            y3Prime = mPrime * (x3 - x2) + y2Prime
            pygame.draw.line(get_screen(), LIGHT_GREY, (x2, y2), (x2, y2Prime), 5)
            pygame.draw.line(get_screen(), LIGHT_GREY, (x3, y3), (x3, y3Prime), 5)
            pygame.draw.line(get_screen(), LIGHT_GREY, (x2, y2), (x3, y3), 5)
            pygame.draw.line(get_screen(), LIGHT_GREY, (x2, y2Prime), (x3, y3Prime), 5)
        return coordinates
        
    def display_event(self):
        floor = self.coordinates[0]
        row = self.coordinates[1]
        column = self.coordinates[2]
        square = self[floor][row][column][HERE]
        event = False
        set_commands(['(P)arty', '(S)ave', '(Q)uick Save', '(L)oad', 't(I)tle Screen', '(Esc)Quit'])
        if (has_char('*', square) or has_char('s', square)) and self.dungeonEvents[floor][row][column] is not None:
            event = True
            self.dungeonEvents[floor][row][column]()
        elif has_char('!', square):
            event = True
            self.encounter()
        if has_char('e', square):
            set_commands(['(E)xit'] + get_commands())
            if self.dungeonEvents[floor][row][column] is not None:
                event = True
                self.dungeonEvents[floor][row][column]()
        if has_char('u', square):
            set_commands(['(U)p'] + get_commands())
        if has_char('d', square):
            print('Going down.')
            set_commands(['(D)own'] + get_commands())
        if not event and random.randint(0, 99) < self[floor].encounterRate:
            self.encounter()
        elif not event:
            dungeon.display()

    def encounter(self):
        currentFloor = self.dungeonMap[self.coordinates[0]]
        numEnemies = random.randint(1, currentFloor.maxEnemies)
        encounteredEnemies = []
        for i in range(numEnemies):
            gender = random.randint(0, 1)
            encounteredEnemies.append(currentFloor.enemies[random.randrange(0, len(currentFloor.enemies))](gender))
        ambush = random.randint(1, 100)
        ambushFlag = 0
        avgPartyStealth = person.get_party().avg_stealth()
        avgEnemyStealth = mean([enemy.stealth() for enemy in encounteredEnemies])
        print('ambush: ' + str(ambush))
        print('chance: ' + str(currentFloor.ambushChance + abs(avgPartyStealth - avgEnemyStealth)))
        if ambush <= currentFloor.ambushChance + abs(avgPartyStealth - avgEnemyStealth):
            partyAmbushes = random.random() * avgPartyStealth 
            enemyAmbushes = random.random() * avgEnemyStealth
            if enemyAmbushes < partyAmbushes:
                ambushFlag = 1
            elif partyAmbushes < enemyAmbushes:
                ambushFlag = -1
        import combat
        #combat.fight(encounteredEnemies, afterCombatEventIn=post_combat_spanking, ambushIn=ambushFlag) 
        combat.fight(encounteredEnemies, ambushIn=ambushFlag) 

    def move(self, forward=True, down=False, up=False):
        """
        Moves the character through the dungeon. If forward is True, then the player is going forwards (i.e. the player pressed the "Up" key). If forward is False,
        
        then the player moved backwards (i.e. pressed the "Down" key).
        """
        if down:
            self.coordinates = (self.coordinates[0]-1, self.coordinates[1], self.coordinates[2])
        elif up:
            self.coordinates = (self.coordinates[0]+1, self.coordinates[1], self.coordinates[2])
        else:
            direction = self.direction if forward else inverse(self.direction)
            if direction == NORTH or direction == EAST:
                movement = 1
            elif direction == SOUTH or direction == WEST:
                movement = -1
            if (direction == NORTH or direction == SOUTH) and not has_char('_', self.current_square()[direction]) and not has_char('-', self.current_square()[direction]):
                self.coordinates = (self.coordinates[0], self.coordinates[1] + movement, self.coordinates[2])
            elif (direction == EAST or direction == WEST) and not has_char('|', self.current_square()[direction]) and not has_char('^', self.current_square()[direction]):
                self.coordinates = (self.coordinates[0], self.coordinates[1], self.coordinates[2] + movement)
            #stepEffect.play()      
        self.display()
        self.display_event()

    def get_square(self, coordinate):
        floor = coordinate[0] % len(self)
        row = coordinate[1] % len(self[floor])
        column = coordinate[2] % len(self[floor][row])
        return self.dungeonMap[floor][row][column]

    def current_square(self):
        return self.get_square(self.coordinates)

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
    set_commands(['(#) Select an enemy.', '(Esc) To not spank anyone'])
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


def dungeon_interpreter(keyEvent):
    global dungeon
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
    elif keyEvent.key == K_p:
        set_commands(['(#)Character', '<==Back'])
        clear_screen()
        say_title('Characters:')
        universal.say('\t'.join(['Name:', 'Health:', 'Mana:\n\t',]), columnNum=3)
        universal.say(person.party.display_party(), columnNum=3)
        set_command_interpreter(select_character_interpreter)
    elif keyEvent.key == K_d:
        dungeon.move(down=True)
    elif keyEvent.key == K_u:
        dungeon.move(up=True)
    elif keyEvent.key == K_UP:
        dungeon.move(True)
    elif keyEvent.key == K_DOWN:
        dungeon.move(False)
    elif keyEvent.key == K_RIGHT:
        dungeon.direction = right(dungeon.direction)
        dungeon.display()
    elif keyEvent.key == K_LEFT:
        dungeon.direction = left(dungeon.direction)
        dungeon.display()

def select_character_interpreter(keyEvent):
    party = person.get_party()
    if keyEvent.key == K_BACKSPACE:
        dungeon_mode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        per = party.members[num-1]
        clear_screen()
        per.character_sheet(dungeon_mode)

def start_coordinate(dungeon):
    dungeonMap = dungeon.dungeonMap
    for floor in range(len(dungeonMap)):
        for row in range(len(dungeonMap[floor])):
            for column in range(len(dungeonMap[floor][row])):
                if has_symbol("s", dungeonMap[floor][row][column][HERE]):
                    return (floor, row, column)
    raise ValueError("Start square not found.")


def has_char(char, string):
    return char in string
