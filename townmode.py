""" Copyright 2014, 2015 Andrew Russell 

This file is part of PotionWars.  PotionWars is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

PotionWars is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PotionWars.  If not, see <http://www.gnu.org/licenses/>.
"""
import universal
from universal import *
import os
import sets
import person
import re
import conversation
import music
import episode
import copy
import textrect
import sys
from pygame.locals import *

def town_mode(sayDescription=True):
    """
    Goes into town mode (i.e. displays the commands for town-mode, and says the description of the current location, if sayDescription is True. Otherwise, it doesn't
    say the description.
    """
    room = universal.state.location
    if sayDescription:
        universal.say_title(room.name)
    if sayDescription:
        universal.say_replace(room.get_description())
    universal.set_commands(['(P)arty', '(G)o', '(S)ave', '(Q)uick Save', '(T)alk', '(L)oad', '(Esc)Quit', 't(I)tle Screen'])
    universal.set_command_interpreter(town_mode_interpreter)
    music.play_music(room.bgMusic)

def rest_mode(bedroomIn=None, sayDescription=True):
    if bedroomIn is None:
        bedroomIn = universal.state.bedroom
    town_mode(sayDescription)
    if bedroomIn:
        universal.set_commands(['(P)arty', '(G)o', '(S)ave', '(Q)uick Save', '(T)alk', '(L)oad', '(Esc)Quit', '(R)oom Actions'] if bedroomIn.boarding else 
                ['(P)arty', '(G)o', '(S)ave', '(Q)uick Save', '(T)alk', '(L)oad', '(Esc)Quit'])
    universal.set_command_interpreter(bedroom_interpreter)


#TODO: Fix problems with (S)tore Item
def bedroom_actions():
    universal.set_commands(['(R)est', '(B)raid Hair', '<==Back']) #'(S)tore Item', '<==Back'])
    universal.set_command_interpreter(bedroom_actions_interpreter)

def set_bedroom(bedroomIn):
    universal.state.bedroom = bedroomIn

def bedroom_interpreter(keyEvent):
    global previousMode
    bedroom = universal.state.bedroom
    previousMode = rest_mode
    if keyEvent.key == K_r and bedroom.boarding:
        bedroom_actions()
    else:
        town_mode_interpreter(keyEvent, rest_mode)

def bedroom_actions_interpreter(keyEvent):
    bedroom = universal.state.bedroom
    if keyEvent.key == K_r:
        bedroom.sleep()
    elif keyEvent.key == K_b:
        style_character()
    elif keyEvent.key == K_c:
        #bedroom.clean()
        pass
    elif keyEvent.key == K_s and False:
        bedroom.store_items()
    elif keyEvent.key == K_BACKSPACE:
        rest_mode(bedroom)

def style_character():
        universal.say_title('Whose hair should be styled?')
        universal.say(universal.numbered_list([member.printedName for member in universal.state.party.members]), justification=0)
        set_command_interpreter(universal.SELECT_NUMBER_BACK_COMMAND)
        set_command_interpreter(style_character_interpreter)
chosenPerson = None
def style_character_interpreter(keyEvent):
    bedroom = universal.state.bedroom
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            rest_mode(bedroom)
    else:
        global chosenPerson
        try:
            chosenPerson = universal.state.party[num]
        except IndexError:
            return
        else:
            say_title(format_line(['How should', chosenPerson.name + "'s", '''hair be styled?''']))
            if chosenPerson.hairLength == 'short':
                hairStyles = person.SHORT_HAIR_STYLE
            universal.say('\n'.join(universal.numbered_list(chosenPerson.hair_styles())), justification=0)
            set_command_interpreter(style_hair_interpreter)
            set_commands(universal.SELECT_NUMBER_BACK_COMMAND)

def style_hair_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            bedroom = universal.state.bedroom
            rest_mode(bedroom)
    else:
        global chosenPerson
        try:
            chosenPerson.hairStyle = chosenPerson.hair_styles()[num]
        except IndexError:
            return
        else:
            universal.say(format_line([chosenPerson.name, format_line(['''frees''', person.hisher(chosenPerson), '''hair.''']) if chosenPerson.hair_styles()[num] == 'down' else
                format_line(['''pulls''', person.hisher(chosenPerson), '''hair into''', '''some cute pigtails''' if chosenPerson.hair_styles()[num] == 'pigtails' else 
                    format_line(['''a''', chosenPerson.hair_styles()[num]]) + "."])]), justification=0)


class Room(universal.RPGObject):
    """
    before_arrival does any necessary processing before entering a room. It is expected to return a value of True or False. If before_arrival returns True, then the
    player is allowed to go there. Otherwise the player is not.
    """
    def __init__(self, name, description="", adjacent=None, characters=None, 
            after_arrival=None, bgMusic=None, bgMusicName="", before_arrival=None, leaving=None):
        self.name = name
        self.leaving = leaving
        if bgMusic is None:
            self.bgMusic = music.TOWN
            self.bgMusicName = "music.TOWN"
        else:
            self.bgMusic = bgMusic
            self.bgMusicName = bgMusicName
        self.description = ' '.join(description) if not isinstance(description, str) else description
        if not isinstance(adjacent, list):
            if adjacent:
                self.adjacent = [adjacent]
                adjacent.add_adjacent(self)
            else:
                self.adjacent = []
        else:
            self.adjacent = adjacent
            for adj in self.adjacent:
                adj.add_adjacent(self)
        if characters is None:
            self.characters = {}
        else:
            self.characters = characters
        self.after_arrival = after_arrival
        self.before_arrival = before_arrival
        universal.state.add_room(self)

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Room Data:", data])

    def save(self):
        saveData = []
        Room.add_data(self.name, saveData)
        Room.add_data(self.bgMusicName, saveData)
        Room.add_data(self.description.strip(), saveData)
        adjList = [room.name for room in self.adjacent]
        if adjList:
            Room.add_data('\n'.join(adjList), saveData)
        else:
            Room.add_data('', saveData)
        if self.characters:
            Room.add_data('\n'.join(charName for charName in self.characters), saveData)
        else:
            Room.add_data('', saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(loadData, room):
        rest = ""
        try:
            _, name, bgMusicName, description, adjacent, characters, rest = loadData.split("Room Data:")
        except ValueError:
            _, name, bgMusicName, description, adjacent, characters = loadData.split("Room Data:")
        room.name = name.strip()
        room.description = description.strip()
        room.bgMusicName = bgMusicName.strip()
        if bgMusicName.strip():
            moduleName, musicName = bgMusicName.strip().split('.')
            module = sys.modules[moduleName]
            room.bgMusic = getattr(module, musicName)
        adjacent = [roomName.strip() for roomName in adjacent.split('\n') if roomName.strip()]
        room.adjacent = [universal.state.get_room(roomName) for roomName in adjacent]
        characters = [charName.strip() for charName in characters.split('\n') if charName.strip()]
        room.characters = {}
        for charName in characters:
            room.characters[charName] = universal.state.get_character(charName)
        #Note: This is a terrible approach, and breaks the whole object-oriented thing. A much better approach would be to save the type of object, and have the state object call the appropriate version.
        #But whatevs. I'm lazy.
        if rest and "Bedroom Only:" in rest:
            Bedroom.load(rest, room)
        elif rest and "Dungeon Only:" in rest:
            import dungeonmode
            dungeonmode.Dungeon.load(rest, room)




    def __getstate__(self):
        state = copy.copy(self.__dict__)
        try:
            state['bgMusic'] = [name for name, song in music.musicFiles.items() if song == self.bgMusic][0]
        except IndexError:
            state['bgMusic'] = None 
        return state

    def __setstate__(self, state):
        self.__dict__ = state
        try:
            self.bgMusic = music.musicFiles[self.bgMusic]
        except KeyError:
            pass


    def mode(self, sayDescription=True):
        return town_mode(sayDescription)

    def add_characters(self, characters):
        for character in characters:
            self.add_character(character)

    def add_character(self, character):
        if self.characters is None: self.characters = {}
        self.characters[character.get_id()] = character
        if character.get_id() == universal.state.player.get_id():
            universal.state.location = self

    def get_description(self):
        return self.description
    def set_description(self, description):
        if not type(description) is list:
            self.description = [description]
        else:
            self.description = description

    def remove_characters(self, characters):
        for character in characters:
            self.remove_character(character)
    def clear_characters(self):
        self.characters = {}
    def remove_character(self, character):
        if character.get_id() in self.characters:
            del self.characters[character.get_id()]

    def has(self, character):
        return character.get_id() in self.characters.keys()
    def add_adjacent(self, adjacentIn):
        if not self.adjacent:
            if type(adjacentIn) is list:
                self.adjacent = adjacentIn
                for adj in adjacentIn:
                    if self not in adj.adjacent:
                        adj.adjacent.append(self)
            else:
                self.adjacent = [adjacentIn]
                if self not in adjacentIn.adjacent:
                    adjacentIn.adjacent.append(self)
        elif adjacentIn in self.adjacent:
            if self not in adjacentIn.adjacent:
                adjacentIn.adjacent.append(self)
            return
        elif type(adjacentIn) is list:
            self.adjacent.extend(adjacentIn)
            for adj in adjacentIn:
                if self not in adj:
                    adj.adjacent.append(self)
        else:
            self.adjacent.append(adjacentIn)
            if self not in adjacentIn.adjacent:
                adjacentIn.adjacent.append(self)

    def remove_adjacent(self, adjacent):
        global startRooms
        if not adjacent in self.adjacent:
            return
        if type(adjacent) is list:
            self.adjacent = [a for a in self.adjacent if not a in adjacent]
            for adj in adjacent:
                adj.remove_adjacent(self)
        else:
            self.adjacent.remove(adjacent)
            adjacent.remove_adjacent(self)
            

    def set_adjacent(self, adjacent):
        self.remove_adjacent(self.adjacent)
        self.add_adjacent(adjacent)

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(dataList):
        raise NotImplementedError()

class Bedroom(Room):
    def __init__(self, name, description="", adjacent=None, characters=None, before_arrival=None, bgMusic=None, bgMusicName=None, punishment=None, punisher=None, weeklyTasks=None,
            after_arrival=None):
        super(Bedroom, self).__init__(name, description, adjacent, characters, self.after_arrival, bgMusic, bgMusicName, before_arrival)
        self.dayNum = 1
        self.dirtiness = 0
        self.numTransgressions = 0
        self.punisher = punisher
        #punishment is the function that should be invoked if the player's space is too dirty.
        self.punishment = punishment
        self.weeklyTasks = weeklyTasks
        self.after_after_arrival = after_arrival
        self.boarding = False
        self.items = []

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Bedroom Data:", data])

    def save(self):
        saveData = [super(Bedroom, self).save(), "Room Data:", 'Bedroom Only:']
        Bedroom.add_data(str(self.dayNum), saveData)
        Bedroom.add_data(str(self.dirtiness), saveData)
        Bedroom.add_data(str(self.numTransgressions), saveData)
        #It may be the case that "punisher" is a function that returns the desired punisher, based upon some property of the player (i.e. gender), in which case we invoke the 
        #function.
        try:
            Bedroom.add_data(self.punisher().name, saveData)
        except TypeError:
            try:
                Bedroom.add_data(self.punisher.name, saveData)
            except AttributeError:
                Bedroom.add_data("None", saveData)
        Bedroom.add_data(str(self.boarding), saveData)
        Bedroom.add_data('\n'.join(item.save() for item in self.items), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(loadData, bedroom):
        _, dayNum, dirtiness, numTransgressions, punisherName, boarding, itemList = loadData.split("Bedroom Data:")
        bedroom.dayNum = int(dayNum.strip())
        bedroom.dirtiness = int(dirtiness.strip())
        bedroom.numTransgressions = int(numTransgressions.strip())
        bedroom.punisher = None if punisherName.strip() == "None" else universal.state.get_character(punisherName.strip())
        bedroom.boarding = boarding.strip() == "True"
        bedroom.items = [universal.state.get_item(itemName) for itemName in itemList]


    def mode(self, sayDescription=True):
        return rest_mode(self, sayDescription)

    def store_items(self):
        universal.say_title('Stored Items')
        universal.say(', '.join(universal.numbered_list(self.items)))
        set_commands(['(#)View Item', '(Enter) View Inventory', '<==Back'])
        set_command_interpreter(store_items_interpreter)

    def store_inventory(self):
        universal.say_title('Inventory')
        universal.say(universal.state.player.display_inventory())
        set_commands(['(#)View Item', '(Enter) View Stored Items', '<==Back'])
        set_command_interpreter(store_inventory_interpreter)


    def after_arrival(self):
        universal.say_title('Bedroom')
        if self.after_after_arrival is not None:
            self.after_after_arrival()
        universal.say(self.description)
        if self.boarding:
            rest_mode(self)
        else:
            town_mode()

    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(saveText):
        raise NotImplementedError()

    def sleep(self):
        try:
            #I don't know what this is doing, or why it's here but I'm not going to mess with it.
            self.punisher = self.punisher()
        except TypeError:
            pass
        #This is such a horrible, quick and dirty hack. I really need to make a function that allows one to modify this
        #kind of thing without having to dig into this code, but I'm too lazy. I'll rework this the next time I need to have some episode-specific event trigger on
        #rest.
        try:
            import episode1
        except ImportError, e:
            self.clean_check()
        else:
            #Horrible, horrible hack. Must figure out a better way of implementing this kind of thing.
            if universal.state.player.currentEpisode == "Tension":
                if 'taking_Carrie_home' in person.get_PC().keywords:
                    episode1.ep1_carrie_sex()
                else:
                    episode1.ep1_catalin()
            else:
                self.clean_check()
                universal.say(universal.format_text([[person.get_PC().name, '''plops down in''', person.hisher(), '''nice bed, and sleeps the night away.''']]), justification=0)
        person.get_PC().restores()
        self.dayNum += 1
        self.dirtiness += 1
        
    def clean_check(self):
        pass
    """
        if self.dayNum % 7 == 0:
            if self.tooDirty():
                self.numTransgressions += 1
                self.punishment()
            else:
                universal.say(universal.format_text([['''"Inspection time," says''', self.punisher.name, '''appearing besides''', person.get_PC().name + "."],
                    [person.get_PC().name, '''looks up groggily. "Hmm. Is it Chiday already?"'''],
                    ['''"Yup," says''', self.punisher.name + ".", person.HeShe(), '''walks around''', person.get_PC().name + "'s", 
                        '''space for a moment, checking the ground underneath the bedding, checking''', person.get_PC().name + "'s",
                        '''bedding, and studying the floor.'''],
                    [person.HeShe(), '''nods in satisfaction.''', '''"Excellent," says''', punisher.name + "."],
                    [person.get_PC().name, '''nods. "Can I go to bed now?"'''],
                    ['''"Of course," says''', punisher.name + " with a smile."]]), justification=0)
        if self.dayNum % 7 == 0:
            self.weeklyTasks()
    """

    def tooDirty(self):
        return self.dirtiness > 3


    def clean(self):
        if person.get_PC().current_health() < person.get_PC().health() // 2 or person.get_PC().current_mana() < person.get_PC().mana() // 2:
            universal.say(universal.format_text([[person.get_PC().name, '''considers taking some time to clean, but plops down on''', person.hisher(), '''bed instead.''', 
                person.HeShe(), '''is too darn tired to clean.''']]), justification=0)
        else:
            universal.say(universal.format_text([[person.get_PC().name, '''takes some time to do some cleaning.''', person.HeShe(), 
                '''cleans dirty clothing, scrapes the mud off''', person.hisher(), '''boots, washes''', person.hisher(), 
                '''linens, and makes sure''', person.hisher(), '''equipment is in good condition.''']]), justification=0)
            self.dirtiness = 0


def clear_rooms():
    for room in allRooms:
        allRooms[room].clear_characters()
offStage = Room('offStage', "If you're seeing this, it means you've reached the end of the content.")
def after_arrival_offstage():
    nextEpisode = episode.allEpisodes[universal.state.player.currentEpisode]
    episode.set_post_title_card(nextEpisode.init)
    episode.allEpisodes[universal.state.player.currentEpisode].start_episode()

    
offStage.after_arrival = after_arrival_offstage
person.set_PC(person.PlayerCharacter("DEFAULT", person.FEMALE))
person.set_party(person.Party([person.get_PC()]))
offStage.add_character(person.get_PC())

def load_initial_room():
    town_mode()


def set_current_room(room):
    universal.state.location = room

chosenItemIndex = None

def store_inventory_interpreter(keyEvent):
    global chosenItemIndex
    try:
        chosenItemIndex = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_RETURN:
            store_items()
        elif keyEvent.key == K_BACKSPACE:
            bedroom_actions()
    else:
        display_inventory_item()

def display_inventory_item():
    try:
        universal.say(universal.player.inventory[chosenItemIndex])
    except (IndexError, TypeError):
        bedroom.store_inventory()
    else:
        set_commands(['(Enter) Store Item', '<==Back'])
        set_command_interpreter(display_inventory_item_interpreter)

def display_inventory_item_interpreter(keyEvent):
    global chosenItemIndex
    if keyEvent.key == K_RETURN:
        bedroom.items.append(universal.state.player.inventory[chosenItemIndex])
        del universal.state.player.inventory[chosenItemIndex]
    elif keyEvent.key == K_BACKSPACE:
        bedroom.store_inventory()



def store_items_interpreter(keyEvent):
    global chosenItemIndex, bedroom
    try:
        chosenItemIndex = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_i:
            bedroom.store_inventory()
        elif keyEvent.key == K_BACKSPACE:
            bedroom_actions()
    else:
        display_item()
   
def display_item():
    global chosenItemIndex
    try:
        universal.say(bedroom.items[chosenItemIndex].display())
    except IndexError:
        bedroom.store_items()
    else:
        set_commands(['(Enter) Take item', '<==Back'])
        set_command_interpreter(display_item_interpreter)

def display_item_interpreter(keyEvent):
    global chosenItemIndex
    if keyEvent.key == K_RETURN:
        universal.state.player.take_item(bedroom.items[chosenItemIndex])
        del bedroom.items[chosenItemIndex]
        chosenItemIndex = None
    elif keyEvent.key == K_BACKSPACE:
        bedroom.store_items()
        chosenItemIndex = None

lastSaveFile = 'pw'
lastQuickSaveFile = ''
loadName = ''
quickSaveNum = 0

def set_initial_room(room):
    universal.state.location = room

def get_current_room(room):
    return universal.state.location


def town_mode_interpreter(keyEvent, previousModeIn=None):
    if previousModeIn is None:
        previousModeIn = town_mode
    global previousMode
    if keyEvent.key == K_ESCAPE:
        confirm_quit(previousMode)
    elif keyEvent.key == K_i:
        confirm_title_screen(previousMode)
    elif keyEvent.key == K_s:
        save(previousMode)
    elif keyEvent.key == K_l:
        load(previousMode)
    elif keyEvent.key == K_q:
        save_game('quick', previousMode)
    elif keyEvent.key == K_t:
        talk(previousMode)
    elif keyEvent.key == K_g:
        select_destination(previousMode)
    elif keyEvent.key == K_p:
        previousMode = previousModeIn
        universal.set_commands(['(#)Character', '<==Back'])
        universal.say_title('Characters:')
        #universal.say(''.join(['Name:', universal.tab("Name:"), 'Health:', universal.tab("Health:"), 'Mana:\n']))
        universal.say('\t'.join(['Name:', 'Health:', 'Mana:\n\t']), columnNum=3)
        universal.say(universal.state.party.display_party(), columnNum=3)
        universal.set_command_interpreter(select_character_interpreter)



def select_char_quickspells(previousModeIn):
    universal.clear_screen()
    global previousMode
    previousMode = previousModeIn
    if len(universal.state.party) == 1:
        modify_quick_spells(universal.state.party[0])
    else:
        universal.say_title(format_line([chosenPerson.name + "'s", "Quick Spells"]))
        universal.say(universal.numbered_list(universal.state.party.members))
        set_commands(['(#) Select a character.', '<==Back'])
        set_command_interpreter(select_char_quickspells_interpreter)

def select_char_quickspells_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            previousMode()
    else:
        try:
            modify_quick_spells(universal.state.party[num])
        except IndexError:
            return


def select_character_interpreter(keyEvent):
    party = person.get_party()
    global previousMode
    if keyEvent.key == K_BACKSPACE:
        if previousMode is None:
            previousMode = town_mode
        previousMode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        per = party.members[num-1]
        per.character_sheet(previousMode)

def confirm_quit(previousModeIn):
    global previousMode
    previousMode = previousModeIn
    universal.set_commands(['Would you like to save before quitting? Y/N', '<==Back'])
    universal.set_command_interpreter(confirm_quit_interpreter)

def confirm_title_screen(previousModeIn):
    global previousMode
    previousMode = previousModeIn
    universal.set_commands(['Would you like to save before returning to the title screen? Y/N', '<==Back'])
    universal.set_command_interpreter(confirm_title_screen_interpreter)

quitting = False
def confirm_quit_interpreter(keyEvent):
    global previousMode
    if keyEvent.key == K_y: 
        global quitting
        quitting = True
        save(previousMode)
    elif keyEvent.key == K_n:
        quit()
    elif keyEvent.key == K_BACKSPACE:
        if previousMode is None:
            previousMode = town_mode
        previousMode()

showTitleScreen = False
def confirm_title_screen_interpreter(keyEvent):
    global previousMode
    if keyEvent.key == K_y: 
        global showTitleScreen
        showTitleScreen = True
        save(previousMode)
    elif keyEvent.key == K_n:
        import titleScreen
        titleScreen.title_screen()
        return
    elif keyEvent.key == K_BACKSPACE:
        if previousMode is None:
            previousMode = town_mode
        previousMode()

saveName = ''
previousMode = None
def save(previousModeIn):
    global saveFiles, previousMode
    previousMode = previousModeIn
    try:
        saveFiles = [f for f in os.listdir('save') if f[0] != '.']
    except FileNotFoundError:
        os.mkdir('save')
        saveFiles = [f for f in os.listdir('save') if f[0] != '.']
    universal.clear_world_view()
    universal.say_title('Save')
    try:
        saveFiles.insert(0, saveFiles.pop(saveFiles.index('quick.sav')))
    except ValueError:
        pass
    universal.say('\n'.join(universal.numbered_list(saveFiles)))
    if len(saveFiles) < 10:
        universal.set_commands(['Provide a save name:_', '(#) Select a save file.', '<==Back'])
    else:
        universal.set_commands([' '.join(['Provide a save name:_']), '(#) Select a save file:_', '<==Back'])
    universal.set_command_interpreter(save_interpreter)

numLastInput = False
saveNum = ''
MAX_SAVE_NAME_LENGTH = 20
def save_interpreter(keyEvent):
    global saveName, saveNum, numLastInput, previousMode
    playerInput = pygame.key.name(keyEvent.key)
    if keyEvent.key == K_BACKSPACE:
        if saveNum == '' and saveName == '':
            if previousMode is not None:
                previousMode()
            else:
                town_mode()
            return
        else:
            saveName = saveName[:-1]
    elif keyEvent.key == K_RETURN:
        if numLastInput:
            try:
                saveName = saveFiles[int(saveNum)-1]
            except (IndexError, ValueError):
                return
        confirm_save(saveName)
        return
    elif keyEvent.key in NUMBER_KEYS and saveName == '':
        if len(saveFiles) < 10 and saveName == '':
            try:
                saveName = saveFiles[int(playerInput)-1]
            except IndexError:
                return
            confirm_save(saveName)
            return
        else:
            if len(saveNum) < MAX_SAVE_NAME_LENGTH:
                saveNum += playerInput
            numLastInput = True
    elif re.match(re.compile(r'^\w$'), playerInput):
        if len(saveName) < MAX_SAVE_NAME_LENGTH:
            if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
                saveName += str.capitalize(playerInput)
            else:
                saveName += playerInput
        numLastInput = False
    universal.set_commands([''.join(['Provide a save name:', saveName, '_']), 
        ''.join(['(#) Select a save file:', saveNum, '_']), '<==Back'])
    return universal.get_command_view()


possibleSave = ''
def confirm_save(saveName):
    global possibleSave
    possibleSave = saveName
    universal.set_commands(' '.join(['Save to', saveName, 'this correct? Y/N']))
    universal.set_command_interpreter(confirm_save_interpreter)

def confirm_save_interpreter(keyEvent):
    if keyEvent.key == K_y:
        global possibleSave, saveName, saveNum, previousMode
        save_game(possibleSave)
        possibleSave = ''
        saveName = ''
        saveNum = ''
    elif keyEvent.key == K_n:
        save(previousMode)

saveDirectory = os.path.join(os.getcwd(), 'save')
def save_game(saveName, previousModeIn=None, preserveSaveName=True):
    global previousMode
    if previousModeIn is not None:
        previousMode = previousModeIn
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    if saveName.split('.')[-1] != 'sav':
        saveName += '.sav'
    with open(os.path.join(saveDirectory, saveName), 'wb') as saveFile:
        universal.state.save(saveFile)
        saveFile.flush()
    global showTitleScreen, previousMode
    if quitting:
        quit()
    elif showTitleScreen:
        import titleScreen
        showTitleScreen = False
        titleScreen.title_screen()
    else:
        if previousMode is not None:
            previousMode()
        else:
            town_mode()


returnTo = None
saveFiles = []
def load(returnMode=None):
    global returnTo, loadName, saveFiles
    if returnMode is not None:
        returnTo = returnMode
    else:
        returnTo = town_mode
    saveFiles = [fileName for fileName in os.listdir('save') if fileName[0] != '.']
    try:
        saveFiles.insert(0, saveFiles.pop(saveFiles.index('quick.sav')))
    except ValueError: 
        pass
    universal.clear_world_view()
    universal.say_title('Load')
    universal.say('\n'.join(universal.numbered_list([sf for sf in saveFiles if sf[0] != '.'])))
    if len(saveFiles) < 10:
        universal.set_commands(['(#) Select a file to load:', '<==Back'])
    else:
        universal.set_commands(['(#) Select a file to load:_', '<==Back'])
    universal.set_command_interpreter(load_interpreter)

def load_interpreter(keyEvent):
    #I really need to figure out a way to turn this code into its own function...
    global loadName
    playerInput = pygame.key.name(keyEvent.key)
    if keyEvent.key in NUMBER_KEYS:
        if len(saveFiles) < 10:
            num = int(playerInput) - 1  
            try:
                loadName = saveFiles[num]
            except IndexError:
                return
            confirm_load()
            return
        else:
            loadName += playerInput
    elif keyEvent.key == K_BACKSPACE:
        if loadName == '':
            returnTo()
            return
        else:
            loadName = loadName[:-1] 
    elif keyEvent.key == K_RETURN:
        try:
            loadName = saveFiles[int(loadName)-1]
        except (ValueError, IndexError):
            return
        confirm_load()
        return
    universal.set_commands([''.join(['(#) Select a file to load:', loadName, '_']), '<==Back'])
    return universal.get_command_view()

def confirm_load():
    global loadName
    universal.set_commands([' '.join(['(Enter) Load ', loadName]), '<==Back'])
    universal.set_command_interpreter(confirm_load_interpreter)

def confirm_load_interpreter(keyEvent):
    global loadName
    if keyEvent.key == K_RETURN:
        load_game()
        loadName = ''
    elif keyEvent.key == K_BACKSPACE:
        load(returnTo)
        global loadName
        loadName = ''
    elif keyEvent.key == K_BACKSPACE:
        returnTo()

def load_game(loadNameIn=None, preserveLoadName=True):
    clear_screen()
    global loadName
    if loadNameIn:
        loadName = loadNameIn
    try:
        with open(os.path.join(saveDirectory, loadName), 'rb') as loadFile:
            universal.state.load(loadFile)
    except IOError:
        universal.say([loadName, 'does not exist!'])
        acknowledge(load, returnTo)
    else:
        assert(person.get_PC().name != '')
        if not preserveLoadName:
            #global loadName
            loadName = ''
        if universal.state.location == universal.state.get_room("offStage"):
            try:
                episode.allEpisodes[universal.state.player.currentEpisode].start_episode(False)
            except KeyError:
                return
        else:
            go(universal.state.location)



def select_destination(previousModeIn):
    global adjacentList
    global previousMode
    if previousModeIn is None:
        previousMode = town_mode
    else:
        previousMode = previousModeIn
    currentRoom = universal.state.location
    adjacent = currentRoom.adjacent
    if currentRoom.adjacent is not None:
        universal.say('\n'.join([str(i) + '. ' + adj.name for i, adj in zip([j for j in range(1, len(adjacent) + 1)], adjacent)]))
        universal.set_commands(['(#) Select destination', '<==Back'])
    else:
        universal.set_commands(['<==Back'])
    previousMode = previousModeIn
    universal.set_command_interpreter(select_destination_interpreter)

def select_destination_interpreter(keyEvent):
    global previousMode
    currentRoom = universal.state.location
    if keyEvent.key == K_BACKSPACE:
        if previousMode is None:
            previousMode = town_mode
        previousMode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if currentRoom.adjacent is not None and 0 < num and num <= len(currentRoom.adjacent):
            go(currentRoom.adjacent[num-1])

def go(room, party=None, sayDescription=True):
    try:
        universal.state.location.leaving()    
    except (TypeError, AttributeError):       
        pass
    try:
        if room.before_arrival():
            perform_go(room, party, sayDescription)
    except (TypeError, AttributeError):
        perform_go(room, party, sayDescription)
    assert universal.state.location == room

def perform_go(room, party=None, sayDescription=True):
    if party is None:
        party = person.get_party()
    if universal.state.location is not None:
        universal.state.location.remove_characters(party)
    room.add_characters(party)
    set_current_room(room)
    if universal.state.location.after_arrival is None:
        universal.state.location.mode(sayDescription)
    else:
        try:
            universal.state.location.after_arrival(room)
        except TypeError:
            universal.state.location.after_arrival()
        #universal.state.location.mode()

def talk(previousModeIn):
    party = person.get_party()
    talkableCharacters = [c for cName, c in universal.state.location.characters.iteritems() if 
            not party.inParty(c)]
    if talkableCharacters:
        universal.say('Who would you like to speak to?\n')
        universal.say('\n'.join([j + name for j, name in zip(
            [str(i) + '. ' for i in range(1, len(talkableCharacters)+1)],
            [c.printedName for c in talkableCharacters])]))
        universal.set_commands(['(#) Select person', '<==Back'])
        global previousMode
        previousMode = previousModeIn
        universal.set_command_interpreter(talk_interpreter)

def talk_interpreter(keyEvent):
    global previousMode
    if keyEvent.key == K_BACKSPACE:
        if previousMode is None:
            previousMode = town_mode
        previousMode()
    elif keyEvent.key in NUMBER_KEYS:
        chosenNum = int(pygame.key.name(keyEvent.key)) - 1
        talkableCharacters = [c for cName, c in universal.state.location.characters.iteritems() if c not in person.get_party().members]
        if 0 <= chosenNum and chosenNum < len(talkableCharacters):
            conversation.converse_with(talkableCharacters[chosenNum], town_mode)

