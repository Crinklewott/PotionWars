import universal
from universal import *
import os
import sets
import person
import re
import conversation
import music
import episode
from pygame.locals import *

allRooms = {}

def town_mode(sayDescription=True):
    """
    Goes into town mode (i.e. displays the commands for town-mode, and says the description of the current location, if sayDescription is True. Otherwise, it doesn't
    say the description.
    """
    print(sayDescription)
    if sayDescription:
        universal.say_title(currentRoom.name)
    if sayDescription:
        universal.say_replace(currentRoom.get_description())
    universal.set_commands(['(P)arty', '(G)o', '(S)ave', '(Q)uick Save', '(T)alk', '(L)oad', '(Esc)Quit', 't(I)tle Screen'])
    universal.set_command_interpreter(town_mode_interpreter)
    music.play_music(currentRoom.bgMusic)

def rest_mode(sayDescription=True):
    town_mode(sayDescription)
    universal.set_commands(['(P)arty', '(G)o', '(S)ave', '(Q)uick Save', '(T)alk', '(L)oad', '(Esc)Quit', '(C)lean', '(R)est'])
    universal.set_command_interpreter(bedroom_interpreter)

bedroom = None
def set_bedroom(bedroomIn):
    global bedroom
    bedroom = bedroomIn

def bedroom_interpreter(keyEvent):
    global bedroom
    global previousMode
    previousMode = rest_mode
    if keyEvent.key == K_c:
        bedroom.clean()
    elif keyEvent.key == K_r:
        print('calling bedroom.sleep')
        bedroom.sleep()
    else:
        town_mode_interpreter(keyEvent, rest_mode)

class Room(universal.RPGObject):
    """
    before_arrival does any necessary processing before entering a room. It is expected to return a value of True or False. If before_arrival returns True, then the
    player is allowed to go there. Otherwise the player is not.
    """
    def __init__(self, name, description="", adjacent=None, characters=None, 
            after_arrival=None, bgMusic=None, before_arrival=None):
        self.name = name
        if bgMusic is None:
            self.bgMusic = music.TOWN
        else:
            self.bgMusic = bgMusic
        if not type(description) is list:
            self.description = [description]
        else:
            self.description = description
        self.adjacent = adjacent
        self.characters = characters
        self.after_arrival = after_arrival
        self.before_arrival = before_arrival
        allRooms[self.name] = self

    def mode(self, sayDescription=True):
        return town_mode(sayDescription)

    def add_characters(self, characters):
        for character in characters:
            self.add_character(character)
    def add_character(self, character):
        if self.characters is None:
            self.characters = {character.get_id():character}
        else:
            self.characters[character.get_id()] = character

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
    def add_adjacent(self, adjacent):
        if self.adjacent is None:
            if type(adjacent) is list:
                self.adjacent = adjacent
                for adj in adjacent:
                    adj.add_adjacent(self)
            else:
                self.adjacent = [adjacent]
                adjacent.add_adjacent(self)
        elif adjacent in self.adjacent:
            return
        elif type(adjacent) is list:
            self.adjacent.extend(adjacent)
            for adj in adjacent:
                adj.add_adjacent(self)
        else:
            self.adjacent.append(adjacent)
            adjacent.add_adjacent(self)

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
        saveText = ['begin_room:', 'room_name='+ universal.SAVE_DELIMITER + self.name]
        if self.characters is not None:
            saveText.append('characters:')
            if person.PC.get_id() in self.characters.keys():
                saveText.append(person.PC._save())
                saveText.extend([self.characters[c]._save() for c in self.characters if c != person.PC.get_id()])
            else:
                saveText.extend([self.characters[c]._save() for c in self.characters])
            saveText.append('end_characters')
        saveText.append('end_room' + '\n')
        return '\n'.join(saveText)

    @staticmethod
    def _load(dataList):
        print('calling load for regular room')
        lineNum = 0
        name = ''
        adjacent = None
        characters = []
        while lineNum < len(dataList):
            line = dataList[lineNum].split(universal.SAVE_DELIMITER)
            if line[0][0] == '%':
                continue
            if line[0] == 'room_name=':
                name = str.strip(' '.join(line[1:]))
            elif str.strip(dataList[lineNum]) == 'characters:':
                personDataList = None
                lineNum += 1
                while str.strip(dataList[lineNum]) != 'end_characters':
                    personDataList = None
                    personType = dataList[lineNum]
                    lineNum += 1
                    while dataList[lineNum] != 'end_' + personType:
                        if personDataList is None:
                            personDataList = [dataList[lineNum]]
                        else:
                            personDataList.append(dataList[lineNum])
                        lineNum += 1
                    lineNum += 1
                    newPerson = person.load_person(personType, personDataList)
                    characters.append(newPerson)
            lineNum += 1
        thisRoom = allRooms[name]
        thisRoom.clear_characters()
        thisRoom.add_characters(characters)
        return thisRoom

class Bedroom(Room):
    def __init__(self, name, description="", adjacent=None, characters=None, before_arrival=None, bgMusic=None, punishment=None, punisher=None, weeklyTasks=None,
            after_arrival=None):
        super(Bedroom, self).__init__(name, description, adjacent, characters, self.after_arrival, bgMusic, before_arrival)
        self.dayNum = 1
        self.dirtiness = 0
        self.numTransgressions = 0
        self.punisher = punisher
        #punishment is the function that should be invoked if the player's space is too dirty.
        self.punishment = punishment
        self.weeklyTasks = weeklyTasks
        self.after_after_arrival = after_arrival
        self.boarding = False

    def mode(self, sayDescription=True):
        return rest_mode(sayDescription)

    def after_arrival(self):
        universal.say_title('Bedroom')
        print('calling after arrival')
        if self.after_after_arrival is not None:
            self.after_after_arrival()
        universal.say(self.description)
        print('boarding:')
        print(self.boarding)
        if self.boarding:
            rest_mode()
        else:
            town_mode()

    def _save(self):
        saveText = super(Bedroom, self)._save()
        saveText = saveText.split('\n')
        saveText.insert(-2, universal.SAVE_DELIMITER.join(['boarding=', str(self.boarding)]))
        return '\n'.join(saveText)

    @staticmethod
    def _load(saveText):
        bRoom = Room._load(saveText)
        for line in saveText:
            line = line.split(universal.SAVE_DELIMITER)
            if line[0] == 'boarding=':
                bRoom.boarding = line[1] == 'True'
        print(bRoom.name)
        print(bRoom.boarding)
        if bRoom.boarding:
            global bedroom
            bedroom = bRoom
        return bRoom

    def sleep(self):
        try:
            #I don't know what this is doing, or why it's here but I'm not going to mess with it.
            self.punisher = self.punisher()
        except TypeError:
            pass
        #This is such a horrible, quick and dirty hack. I really need to make a function that allows one to modify this
        #kind of thing without having to dig into this code, but I'm too lazy. I'll rework this the next time I need to have some episode-specific event trigger on
        #rest.
        print('called sleep')
        try:
            import PotionWars
        except ImportError, e:
            print('-------------------ImportError!--------------------')
            print(e)
            self.clean_check()
        else:
            print('checking episode!')
            if person.PC.currentEpisode.name == PotionWars.episode1.name:
                if 'taking_Carrie_home' in person.PC.keywords:
                    PotionWars.ep1_carrie_sex()
                else:
                    print('calling ep1_catalin')
                    PotionWars.ep1_catalin()
            else:
                self.clean_check()
                universal.say(universal.format_text([[person.PC.name, '''plops down in''', person.hisher(), '''nice bed, and sleeps the night away.''']]), justification=0)
        person.PC.restores()
        self.dayNum += 1
        self.dirtiness += 1
        
    def clean_check(self):
        if self.dayNum % 7 == 0:
            if self.tooDirty():
                self.numTransgressions += 1
                self.punishment()
            else:
                universal.say(universal.format_text([['''"Inspection time," says''', self.punisher.name, '''appearing besides''', person.PC.name + "."],
                    [person.PC.name, '''looks up groggily. "Hmm. Is it Chiday already?"'''],
                    ['''"Yup," says''', self.punisher.name + ".", person.HeShe(), '''walks around''', person.PC.name + "'s", 
                        '''space for a moment, checking the ground underneath the bedding, checking''', person.PC.name + "'s",
                        '''bedding, and studying the floor.'''],
                    [person.HeShe(), '''nods in satisfaction.''', '''"Excellent," says''', punisher.name + "."],
                    [person.PC.name, '''nods. "Can I go to bed now?"'''],
                    ['''"Of course," says''', punisher.name + " with a smile."]]), justification=0)
        if self.dayNum % 7 == 0:
            self.weeklyTasks()

    def tooDirty(self):
        return self.dirtiness > 3

    def clean(self):
        if person.PC.current_health() < person.PC.health() // 2 or person.PC.current_mana() < person.PC.mana() // 2:
            universal.say(universal.format_text([[name(), '''considers taking some time to clean, but plops down on''', person.hisher(), '''bed instead.''', person.HeShe(), 
                '''is too darn tired to clean.''']]), justification=0)
        else:
            universal.say(universal.format_text([[person.PC.name, '''takes some time to do some cleaning.''', person.HeShe(), 
                '''cleans dirty clothing, scrapes the mud off''', person.hisher(), '''boots, washes''', person.hisher(), 
                '''linens, and makes sure''', person.hisher(), '''equipment is in good condition.''']]), justification=0)
            self.dirtiness = 0


def clear_rooms():
    print('calling clear rooms')
    import traceback
    traceback.print_stack()
    for room in allRooms:
        allRooms[room].clear_characters()
offStage = Room('offStage', "If you're seeing this, it means you've reached the end of the content.")
person.set_PC(person.PlayerCharacter("DEFAULT", person.FEMALE))
print('printing PC gender')
print(person.FEMALE)
print(person.PC.gender)
person.set_party(person.Party([person.PC]))
offStage.add_character(person.get_PC())
print(offStage.characters)
print(person.get_PC().get_id())
print(person.get_PC().get_id() in offStage.characters)

def load_initial_room():
    town_mode()

currentRoom = offStage

def set_current_room(room):
    global currentRoom
    currentRoom = room

lastSaveFile = 'pw'
lastQuickSaveFile = ''
loadName = ''
quickSaveNum = 0

def set_initial_room(room):
    global currentRoom
    currentRoom = room

def get_current_room(room):
    return currentRoom


def town_mode_interpreter(keyEvent, previousModeIn=town_mode):
    party = person.get_party()
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
        universal.say('\t'.join(['Name:', 'Health:', 'Mana:\n\t',]), columnNum=3)
        universal.say(party.display_party(), columnNum=3)
        universal.set_command_interpreter(select_character_interpreter)

def select_character_interpreter(keyEvent):
    party = person.get_party()
    if keyEvent.key == K_BACKSPACE:
        previousMode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        per = party.members[num-1]
        per.character_sheet(previousMode)

def confirm_quit(previousModeIn):
    global previousMode
    previousMode = previousModeIn
    universal.set_commands(['Would you like to save before quitting? Y/N', '(Esc)Back'])
    universal.set_command_interpreter(confirm_quit_interpreter)

def confirm_title_screen(previousModeIn):
    global previousMode
    previousMode = previousModeIn
    universal.set_commands(['Would you like to save before returning to the title screen? Y/N', '(Esc)Back'])
    universal.set_command_interpreter(confirm_title_screen_interpreter)

quitting = False
def confirm_quit_interpreter(keyEvent):
    if keyEvent.key == K_y: 
        global quitting
        quitting = True
        save(previousMode)
    elif keyEvent.key == K_n:
        quit()
    elif keyEvent.key == K_ESCAPE:
        previousMode()

showTitleScreen = False
def confirm_title_screen_interpreter(keyEvent):
    if keyEvent.key == K_y: 
        global showTitleScreen
        showTitleScreen = True
        save(previousMode)
    elif keyEvent.key == K_n:
        import titleScreen
        titleScreen.title_screen()
    elif keyEvent.key == K_ESCAPE:
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
        universal.set_commands(['Provide a save name:_', '(#) Select a save file.', '(Esc)Back'])
    else:
        universal.set_commands([' '.join(['Provide a save name:_']), '(#) Select a save file:_', '(Esc)Back'])
    universal.set_command_interpreter(save_interpreter)

numLastInput = False
saveNum = ''
def save_interpreter(keyEvent):
    global saveName, saveNum, numLastInput, previousMode
    playerInput = pygame.key.name(keyEvent.key)
    if keyEvent.key == K_BACKSPACE:
        if numLastInput and saveNum == '':
            saveNum = saveNum[:-1] 
        else:
            saveName = saveName[:-1]
    elif keyEvent.key == K_RETURN:
        if numLastInput:
            try:
                saveName = saveFiles[int(saveNum)-1]
            except IndexError, ValueError:
                return
        confirm_save(saveName)
        return
    elif keyEvent.key == K_ESCAPE:
        if previousMode is not None:
            previousMode()
        else:
            town_mode()
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
            saveNum += playerInput
            numLastInput = True
    elif re.match(re.compile(r'^\w$'), playerInput):
        if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
            saveName += str.capitalize(playerInput)
        else:
            saveName += playerInput
        numLastInput = False
    universal.set_commands([''.join(['Provide a save name:', saveName, '_']), 
        ''.join(['(#) Select a save file:', saveNum, '_']), '(Esc)Back'])


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
print(saveDirectory)
def save_game(saveName, previousModeIn=None, preserveSaveName=True):
    import traceback
    traceback.print_stack()
    global previousMode
    if previousModeIn is not None:
        previousMode = previousModeIn
    if not os.path.exists(saveDirectory):
        os.makedirs(saveDirectory)
    if saveName.split('.')[-1] != 'sav':
        saveName += '.sav'
    saveData = [] 
    saveData.append('willpower_check=' + universal.SAVE_DELIMITER + str(person.get_willpower_check()) + '\n')
    saveData.append('difficulty=' + universal.SAVE_DELIMITER + str(universal.get_difficulty()) + '\n')
    try:
        saveData.append(person.PC.currentEpisode._save() + '\n')
    except AttributeError:
        pass
    print(offStage.characters)
    startRoom = [room for roomName, room in allRooms.iteritems() 
            if room.characters is not None and room.characters is not [] and 
            person.get_PC().get_id() in room.characters][0]
    otherRooms = [room for roomName, room in allRooms.iteritems() 
            if (room.characters is None or not person.PC.get_id() in room.characters)]
    saveData.append(startRoom._save())
    for room in otherRooms: 
        saveData.append(room._save())
    saveData.append(person.get_party()._save() + '\n')
    with open(os.path.join(saveDirectory, saveName), 'w') as saveFile:
        saveFile.write(''.join(saveData))
        saveFile.flush()
    global showTitleScreen
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
def load(returnMode=town_mode):
    global returnTo, loadName, saveFiles
    returnTo = returnMode
    saveFiles = [fileName for fileName in os.listdir('save') if fileName[0] != '.']
    try:
        saveFiles.insert(0, saveFiles.pop(saveFiles.index('quick.sav')))
    except ValueError: 
        pass
    universal.clear_world_view()
    universal.say_title('Load')
    universal.say('\n'.join(universal.numbered_list([sf for sf in saveFiles if sf[0] != '.'])))
    if len(saveFiles) < 10:
        universal.set_commands(['(#) Select a file to load:', '(Esc)Back'])
    else:
        universal.set_commands(['(#) Select a file to load:_', '(Esc)Back'])
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
        loadName = loadName[:-1] 
    elif keyEvent.key == K_RETURN:
        try:
            loadName = saveFiles[int(loadName)-1]
        except (ValueError, IndexError):
            return
        confirm_load()
        return
    elif keyEvent.key == K_ESCAPE:
        returnTo()
        return
    universal.set_commands([''.join(['(#) Select a file to load:', loadName, '_']), '(Esc)Back'])

def confirm_load():
    global loadName
    universal.set_commands([' '.join(['Is', loadName, 'correct? Y/N']), '(Esc)Back'])
    universal.set_command_interpreter(confirm_load_interpreter)

def confirm_load_interpreter(keyEvent):
    if keyEvent.key == K_y:
        load_game()
    elif keyEvent.key == K_n:
        load(returnTo)
        global loadName
        loadName = ''
    elif keyEvent.key == K_ESCAPE:
        returnTo()

#TODO: Rewrite this and save_game using the pickle module.
def load_game(loadNameIn=None, preserveLoadName=True):
    clear_screen()
    loadData = []
    rooms = {}
    currentRoom = None
    global allRooms
    global loadName
    if loadNameIn is not None:
        loadName = loadNameIn
    for room in allRooms:
        allRooms[room].clear_characters()
    try:
        with open(os.path.join(saveDirectory, loadName), 'r') as loadFile:
            loadData = [l.strip() for l in list(loadFile)]
    except IOError:
        universal.say([loadName, 'does not exist!'])
        acknowledge(load, returnTo)
    else:
        loadName = ''
        lineNum = 0
        while lineNum < len(loadData):
            line = loadData[lineNum].split(universal.SAVE_DELIMITER)
            if line[0] == 'willpower_check=':
                flag = int(line[1])
                if flag == 1:
                    person.set_willpower_check(True)
                else:
                    set_willpower_check(False)
            elif line[0] == 'difficulty=':
                universal.set_difficulty(int(line[1]))
            elif line[0] == 'begin_episode':
                lineNum += 1
                episodeData= []
                while loadData[lineNum] != 'end_episode':
                    episodeData.append(loadData[lineNum])
                    lineNum += 1 
                if person.PC is None:
                    person.PC = person.PlayerCharacter('', person.FEMALE)
                person.PC.currentEpisode = episode.Episode._load(episodeData)
            elif line[0] == 'begin_room:':
                roomData = []
                lineNum += 1
                isDungeon = False
                isBedroom = False
                while loadData[lineNum] != 'end_room':
                    if loadData[lineNum].split(universal.SAVE_DELIMITER)[0] == 'dungeon=':
                        isDungeon = True
                    elif loadData[lineNum].split(universal.SAVE_DELIMITER)[0] == 'boarding=':
                        isBedroom = True
                    roomData.append(loadData[lineNum])  
                    lineNum += 1
                if isDungeon:
                    import dungeonmode
                    newRoom = dungeonmode.Dungeon._load(roomData)
                elif isBedroom:
                    newRoom = Bedroom._load(roomData)
                else:
                    newRoom = Room._load(roomData)
                allRooms[newRoom.name] = newRoom
            elif line[0] == 'begin_party:':
                    partyNames = []
                    lineNum += 1
                    while loadData[lineNum] != 'end_party':
                        partyNames.append(str.strip(loadData[lineNum]))
                        lineNum += 1
                    currentRoom = [room for rName, room in allRooms.iteritems() if 
                            room.characters is not None and person.PC.get_id() in 
                            room.characters][0]
                    person.set_party(person.Party([c for cName, c in currentRoom.characters.iteritems() if 
                        cName in partyNames]))
            lineNum += 1
        assert(person.PC.name != '')
        if not preserveLoadName:
            #global loadName
            loadName = ''
        else:
            go(currentRoom)


def select_destination(previousModeIn):
    global adjacentList
    adjacent = currentRoom.adjacent
    if currentRoom.adjacent is not None:
        universal.say('\n'.join([str(i) + '. ' + adj.name for i, adj in zip([j for j in range(1, len(adjacent) + 1)], adjacent)]))
        universal.set_commands(['(#) Select destination', '<==Back'])
    else:
        universal.set_commands(['<==Back'])
    global previousMode
    previousMode = previousModeIn
    universal.set_command_interpreter(select_destination_interpreter)

def select_destination_interpreter(keyEvent, previousMode=town_mode):
    if keyEvent.key == K_BACKSPACE:
        previousMode()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if currentRoom.adjacent is not None and 0 < num and num <= len(currentRoom.adjacent):
            go(currentRoom.adjacent[num-1])

def go(room, party=None, sayDescription=True):
    try:
        if room.before_arrival():
            perform_go(room, party, sayDescription)
    except (TypeError, AttributeError):
        perform_go(room, party, sayDescription)

def perform_go(room, party=None, sayDescription=True):
    global currentRoom
    if party is None:
        party = person.get_party()
    if currentRoom is not None:
        currentRoom.remove_characters(party)
    room.add_characters(party)
    currentRoom = room
    print(currentRoom.characters)
    if currentRoom.after_arrival is None:
        currentRoom.mode(sayDescription)
    else:
        currentRoom.after_arrival()
        #currentRoom.mode()

def talk(previousModeIn):
    party = person.get_party()
    universal.say('Who would you like to speak to?\n')
    talkableCharacters = [c for cName, c in currentRoom.characters.iteritems() if 
            not party.inParty(c)]
    for c in talkableCharacters:
        print(c.printedName)
    universal.say('\n'.join([j + name for j, name in zip(
        [str(i) + '. ' for i in range(1, len(talkableCharacters)+1)],
        [c.printedName for c in talkableCharacters])]))
    universal.set_commands(['(#) Select person', '<==Back'])
    global previousMode
    previousMode = previousModeIn
    universal.set_command_interpreter(talk_interpreter)

def talk_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        previousMode()
    elif keyEvent.key in NUMBER_KEYS:
        chosenNum = int(pygame.key.name(keyEvent.key)) - 1
        talkableCharacters = [c for cName, c in currentRoom.characters.iteritems() if c not in person.get_party().members]
        if 0 <= chosenNum and chosenNum < len(talkableCharacters):
            print('talking to:')
            print(talkableCharacters[chosenNum])
            print(talkableCharacters[chosenNum].litany)
            print(talkableCharacters[chosenNum].defaultLitany)
            conversation.converse_with(talkableCharacters[chosenNum], town_mode)

