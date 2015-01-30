"""
    Universal.py contains various functions and operations that need to be accessible by every other file in the engine, in particular: 
    1. The say function for displaying text
    2. The set_command_interpreter and get_command_interpreter functions for modifying how the game interprets various keyboard commands.
    3. A quit() command that adds a quit event to the event queue. 
    4. Functions for getting and setting the list of commands to be displayed.

WARNING: Due to fiddling with the name of Carlita (she was Carlita, then Lucilla, then Anastacia, then Carlita again), I've had to add some code to the state object to change Lucilla/Anastacia to Carlita, in order to ensure
that keywords are registering properly for people loading saves from versions where Carly's name was Lucilla.
"""

#NOTE: I've had to add some code to keep save files compatible with the name change of Peter's shop. That code should be deleted before using this engine for future games.
from __future__ import print_function 
import sys, pygame, textrect, abc
import Queue
from pygame.locals import *
import os
import math
import ast

DEBUG = True
SAVE_DELIMITER = '%%%'


STAT_GROWTH_RATE_MULTIPLIER = 10
NUM_TIERS = 10

SELECT_NUMBER_COMMAND = ['(#) Select a number.']
SELECT_NUMBER_BACK_COMMAND = SELECT_NUMBER_COMMAND + ['<==Back']

def resource_path(relative):
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, 'data', relative)

def key_name(keyEvent):
    return pygame.key.name(keyEvent.key)

def response(keyEvent):
    return int(key_name(keyEvent))

author = 'AKA'
programmer = 'AKA'
authorEmailBugs = 'sprpgs@gmail.com+bugs'
programmerEmailBugs = 'sprpgs@gmail.com+bugs'
authorEmail = 'sprpgs@gmail.com'
programmerEmail = authorEmail

NUM_STATS = 9
WARFARE = 0
MAGIC = 1
RESILIENCE = 2
GRAPPLE = 3
STEALTH = 4
HEALTH = 5
MANA = 6
CURRENT_HEALTH = 7
CURRENT_MANA = 8

COMBAT_MAGIC = 9
STATUS_MAGIC = 10
BUFF_MAGIC = 11
SPECTRAL_MAGIC = 12
BALANCED = 13

def stat_name(stat):
    if stat == WARFARE:
        return 'warfare'    
    elif stat == MAGIC:
        return 'magic'
    elif stat == RESILIENCE:
        return 'resilience'
    elif stat == GRAPPLE:
        return 'grapple'
    elif stat == STEALTH:
        return 'stealth'
    elif stat == HEALTH:
        return 'health'
    elif stat == MANA:
        return 'mana'
    elif stat == CURRENT_HEALTH:
        return 'current health'
    elif stat == CURRENT_MANA:
        return 'current mana'

STRENGTH = 0
DEXTERITY = 1
WILLPOWER = 2
TALENT = 3
ALERTNESS = 4

def primary_stat_name(stat):
    print(stat)
    if stat == STRENGTH:
        return 'Strength'    
    elif stat == DEXTERITY:
        return 'Dexterity'
    elif stat == WILLPOWER:
        return 'Willpower'
    elif stat == TALENT:
        return 'Talent'
    elif stat == ALERTNESS:
        return 'Alertness'
    elif stat == HEALTH:
        return 'Health'
    elif stat == MANA:
        return 'Mana'
    elif stat == CURRENT_HEALTH:
        return 'Current Health'
    elif stat == CURRENT_MANA:
        return 'Current Mana'

#This contains a list of list of triples. get_spells()[i] is the list of triples for tier i. Each triple consists of three separate spells: a basic, advanced, and expert
#spell at tier i for each type. Basic and Advanced spells are available to everyone, but they must learn basic before advanced. Expert spells are only available to a 
#character who is specialized in that spell type. Furthermore, characters who are specialized in a spell type get the basic spell for free.
spellsByTier = None
def set_spells(spellList):
    global spellsByTier
    spellsByTier = spellList

def get_spells():
    return spellsByTier

NUMBER_KEYS = [K_0, K_1, K_2, K_3, K_4, K_5, K_6, K_7, K_8, K_9]
FUNCTION_KEYS = [K_F1, K_F2, K_F3, K_F4, K_F5, K_F6, K_F7, K_F8, K_F9, K_F10,  K_F11, K_F12]  

def set_programmer_email(email):
    global programmerEmail
    programmerEmail = email


def set_programmer_email_bugs(email):
    global programmerEmailBugs
    programmerEmailBugs = email

def set_author_email(email):
    global authorEmail
    authorEmail = email

def set_author_email_bugs(email):
    global authorEmailBugs
    authorEmailBugs = email

def get_author_email_bugs():
    return authorEmailBugs

def programmer_email_bugs():
    return programmerEmailBugs

def set_author(name):
    global author
    author = name

def set_programmer(name):
    global programmer
    programmer = name

def get_author():
    return author

def get_programmer():
    return programmer

commands = []
commandInterpreter = None
def set_command_interpreter(ci):
    """
    Allows the user to change the function that processes the key presses. This is particularly valuable for different game modes: i.e. moving through the city versus
    exploring a dungeon versus combat versus conversation.  
    """
    global commandInterpreter
    commandInterpreter = ci

def get_command_interpreter():
    return commandInterpreter

commandColors = []
def set_commands(newCommands, colors=None):
    """
        Set the commands to be used by the player. Also allows the player to set the color of each command. If colors is not given, then the commands default to LIGHT_GREY. Note the colors must be a 
        list, where colors[i] is the color of newCommands[i]. 
        Raises a ValueError if the number of commands passed exceeds 9 (the maximum number that can be displayed).
    """
    global commands 
    global commandColors
    print('commands:')
    print(commands)
    print('colors to be used:')
    print(colors)
    import traceback
    #traceback.print_stack()
    if commands != newCommands:
        clear_commands()
    if not type(newCommands) == list:
        commands = [newCommands]
        if colors and not type(colors) == list:
            commandColors = [colors]
        elif colors:
            commandColors = colors
        else:
            commandColors = [LIGHT_GREY]
    elif len(newCommands) > 9:
        raise ValueError('Number of commands cannot exceed 9. Problem commands: ' + ', '.join(newCommands))
    else:
        commands = newCommands
        #(LIGHT_GREY,) is necessary as opposed to LIGHT_GREY in order to ensure that we get len(commands) copies of LIGHT_GREY, rather than the numbers in the tuple that LIGHT_GREY represents.
        commandColors = colors if colors else [LIGHT_GREY] * len(commands)
    print('commandColors')
    print(commandColors)

def get_commands():
    """
    Returns a pair containing the list of commands, and the list of associated commandColors.
    """
    return commands

def get_command_colors():
    return commandColors

#textToDisplay is a list of 4-tuples. The first element is the text. The second element is the size. The third element is whether or not the text should be italic. The
#fourth element is whether or not the text should be bold.
textToDisplay = ''
TEXT = 0
SIZE = 1
ITALIC = 2
BOLD = 3

DEFAULT_RESOLUTION = (1680, 1050)
DEFAULT_SIZE = 36
#SMALL_SIZE = DEFAULT_SIZE/2
TITLE_SIZE = 42

numColumns = 1

def set_column_number(numColumnsIn):
    global numColumns
    numColumns = numColumnsIn

textJustification = 1
chosenSurface = None
postSayPair = None
playedMusic = Queue.Queue()
TAB = 5 * '        '

def tab(word):
    return ''.join(' ' for i in range(len(TAB) - len(word) % len(TAB)))

def say(text, columnNum=1, justification=1, fontSize=36, italic=False, bold=False, 
        surface=None, music=None):
    """
        TODO:
        Note: At this point, the fontSize, italic, and bold don't do anything. Furthermore, considering the delay between when this function is called, and when the 
        text is actually printed to screen, I'd have to rework these things. Essentially, I'd have to call display text immediately. This would require the user to 
        block all their text to be displayed into one say call. This could lead to problems if there are a variety of different says that are being combined from various
        parts of the code (such as say something that might be happening due to combat or something). This will have to be played with once I get the full engine up and
        running.
    """
    if surface is None:
        surface = screen
    global chosenSurface
    chosenSurface = surface
    global textToDisplay
    global numColumns
    global textJustification
    textJustification = justification
    import traceback
    assert type(numColumns) == int, "%s" % traceback.print_stack()
    numColumns = columnNum
    if type(text) is list:
        textToDisplay += ' '.join(text) 
    else:
        textToDisplay += text
    if music is not None:
        print(music)
        global playedMusic
        try:
            for song in music:
                playedMusic.put(song)
        except TypeError:
            playedMusic.put(music)
        #print('putting a song into playedMusic:')
        #print(music)
        #import traceback
        #traceback.print_stack()
    """
    if textToDisplay:
        textToDisplay.append((text, fontSize, italic, bold))
    else:
        textToDisplay = [(text, fontSize, italic, bold)]
    """


def say_immediate(text, columnNum=1, justification=1, fontSize=36, italic=False, bold=False, 
        surface=None):
    """
        TODO:
        Note: At this point, the fontSize, italic, and bold don't do anything. Furthermore, considering the delay between when this function is called, and when the 
        text is actually printed to screen, I'd have to rework these things. Essentially, I'd have to call display text immediately. This would require the user to 
        block all their text to be displayed into one say call. This could lead to problems if there are a variety of different says that are being combined from various
        parts of the code (such as say something that might be happening due to combat or something). This will have to be played with once I get the full engine up and
        running.
    """
    if surface is None:
        surface = screen
    global chosenSurface
    chosenSurface = surface
    global textToDisplay
    global numColumns
    global textJustification
    textJustification = justification
    numColumns = columnNum
    if type(text) is list:
        textToDisplay += ' '.join(text) 
    else:
        textToDisplay += text
    textRect = worldView.copy()
    titleFont = pygame.font.SysFont(FONT_LIST_TITLE, TITLE_SIZE)
    textRect.height = textRect.height - 2 * titleFont.get_linesize()
    displayPosition = (worldView.topleft[0], worldView.topleft[1] + 2 * titleFont.get_linesize())
    display_text(get_text_to_display(), textRect, displayPosition, isTitle=False)
    clear_text_to_display()
    display_commands()
    pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(commandView.topleft, commandView.size), 5)
    pygame.display.flip()
    """
    if textToDisplay:
        textToDisplay.append((text, fontSize, italic, bold))
    else:
        textToDisplay = [(text, fontSize, italic, bold)]
    """

def say_delay(text, columnNum=1, justification=1, fontSize=36, italic=False, bold=False, surface=None, overwritePrevious=True):
    say(text, columnNum, justification, fontSize, italic, bold, surface)
    flush_text(overwrite=overwritePrevious)

def say_replace(text, columnNum=1, justification=1, fontSize=36, italic=False, bold=False):
    """
    Just like say, except it replaces the old text to be displayed, rather than adding to it.
    """
    global textToDisplay, numColumns, textJustification
    if type(text) is list:
        textToDisplay = ' '.join(text)
    else:
        textToDisplay = text
    numColumns = columnNum
    textJustification = justification

titleText = ''
def get_title_text():
    return titleText

chosenSurface = None
def say_title(text, surface=None):
    """
    Similar to say, except uses a larger font, and draws a line around the text rectangle to set it apart from the in-game text.
    """
    global titleText, chosenSurface
    if surface is not None:
        chosenSurface = surface
    else:
        chosenSurface = screen
    if type(text) is list:
        titleText = ' '.join(text)
    else:
        titleText = text

def get_text_to_display():
    return textToDisplay

def clear_text_to_display():
    global textToDisplay 
    textToDisplay = ''

def quit():
    pygame.event.post(pygame.event.Event(pygame.QUIT))

HAND = 0
STRAP = 1 
CANE = 2
def set_difficulty(diff):
    global state
    state.difficulty = diff

def get_difficulty():
    global state
    return state.difficulty

#Make sure to confirm font names for Windows and Mac.
FONT_LIST = 'Georgia'

FONT_LIST_TITLE = 'Verdana'


BLACK = (0,0,0)
DARK_GREY = (10, 10, 10)
LIGHT_GREY = (200, 200, 200)
WHITE = (250,250,250)
RED = (100, 50, 50)
GREEN = (50, 100, 50)
BLUE = (50, 50, 100)
YELLOW = (100, 100, 50)
SLATE_GREY = (49, 79, 79)

background = None
screen = None

def set_screen(S):
    global screen
    screen = S

def get_screen():
    return screen

def clear_screen():
    global textToDisplay
    print('clearing screen!')
    textToDisplay = ""
    clearScreen = pygame.Surface((worldView.width, worldView.height))
    clearScreen.fill(DARK_GREY)
    screen.blit(clearScreen, worldView)
    clearScreen = pygame.Surface((commandView.width, commandView.height))
    clearScreen.fill(DARK_GREY)
    screen.blit(clearScreen, commandView)
    pygame.display.flip()

def clear_world_view():
    worldView = get_world_view()
    clearScreen = pygame.Surface((worldView.width, worldView.height))
    clearScreen.fill(DARK_GREY)
    get_screen().blit(clearScreen, worldView)
    pygame.display.flip()

def clear_commands():
    global textToDisplay
    clearScreen = pygame.Surface((commandView.width, commandView.height))
    clearScreen.fill(DARK_GREY)
    screen.blit(clearScreen, commandView)
    pygame.display.flip()

def set_background(B):
    global background
    background = B

def get_background():
    return background

def display_text(text, rectIn, position, isTitle=False, justification=None):
    """
    \p to allows the
    user to split text along pages, rather than relying solely on whether there is enough room. This can be particularly useful for things like combat messages.    
    We print the text in columns based on the location of \t. Essentially, each \t indicates that the following text should go in the next column, where the next column
    is current column + 1 % numColumns.  

    Note: Tabbing is really fucked up, and I have no idea how it works anymore. I'd recommend avoiding it, unless you want to fix it or poke your own eyes out.
    TODO: Improve tabbing. Seriously, IMPROVE TABBING! YE GODS IT'S SO HACKY AND HORRIBLE!!!!!

    Meanwhile, \p indicates that the next batch of text should appear on a new screen of text(with an acknowledgment between them) in the appropriate column. Note that 
    we split on pages first, then columns.

    Note that currently this is a little bit unsafe, in that it doesn't check to make sure that there is enough space for all the columns. The number of columns you can
    support depends on how much text you have, and how big the viewing area is, and which you'll have to determine with a bit of experimentation.
    It will automatically generate 
    new pages if the text is too big to fit on a single page.
    """
    #We need to split the rectangle into number of columns pieces, essentially, for displaying the text.
    global chosenSurface
    if chosenSurface is None:
        chosenSurface = screen
    rect = rectIn.copy()
    if isTitle:
        numColumnsLocal = 1
    else:
        numColumnsLocal = numColumns
    if justification is None:
        if isTitle:
            justification = 1
        else:
            rect.width = rect.width - 20
            justification = textJustification
    rect.width = rect.width / numColumnsLocal
    text = text.replace('\m', '\p\m')
    pages = text.split('\p')
    try:
        pages.remove('')
    except ValueError:
        pass
    previousColumnWidth = 0
    previousLineHeight = 0
    pageLength = len(pages)
    pageCount = 0
    #We're using a while loop, because we need to do a bit of loop iteration manipulation to handle dynamically creating new pages of text when there isn't enough
    #room.
    newPage = ''
    previousPageAdditionColumnCount = 0
    while pageCount < pageLength:
        page = pages[pageCount]
        columns = page.split('\t')
        if numColumnsLocal == 1:
            columns[0] = ' '.join(columns)
            del columns[1:]
        columnCount = 0
        numSeparateColumns = len(columns)
        lineNum = 0
        previousCommands = get_commands()
        previousColors = get_command_colors()
        while columnCount < numSeparateColumns:
            column = columns[columnCount]
            #Need to wrap back around to the first column.
            if columnCount >= numColumnsLocal and columnCount % numColumnsLocal == 0:
                lineNum += 1
            textSurface = None
            if isTitle:
                font = pygame.font.SysFont(FONT_LIST_TITLE, TITLE_SIZE)
            else:
                font = pygame.font.SysFont(FONT_LIST, DEFAULT_SIZE)
            #At this point, we just add one line at a time until the whole thing fits, and move the other lines onto a new page. It's ugly as sin, but it gets the job
            #done, and it guarantees that a minimum number of pages is used. In particular, we may want to move the logic for checking if the text is large enough into
            #the except block.
            playMusic = False
            try:
                if '\m' in column:
                    playMusic = True
                    columnNoM = column.replace('\m', '')
                else:
                    columnNoM = column
                textSurface = textrect.render_textrect(columnNoM, font, rect, LIGHT_GREY, DARK_GREY, justification)
            #If there isn't enough room, we need to move this text onto a new page in the appropriate column. We try move them onto the next page one line at a time.
            except textrect.TextRectException, e:
                accumulatedHeight = 0
                finalLines = textrect.get_final_lines(column, font, rect)
                nextPage = ''
                thisPage = ''
                i = 0
                while accumulatedHeight + font.size(finalLines[i])[1] < rect.height:
                    thisPage += '\n' + finalLines[i]
                    i += 1
                    accumulatedHeight += font.size(finalLines[i])[1]
                nextPage = '\n'.join(finalLines[i:])
                thisPage = thisPage.strip()
                nextPage = nextPage.strip()
                #If this is the case, it means our optional font is too big.
                #If we're still working in the same column, then we don't add \t.
                if columnCount % numColumnsLocal == previousPageAdditionColumnCount:
                    if finalLines[-2] == '':
                        newPage = '\n'.join(['', nextPage, newPage])
                    else:
                        newPage = '\n'.join([nextPage, newPage])
                    columns[columnCount] = thisPage
                else:
                    newPage = '\t' + nextPage + newPage
            else:
                if playMusic:
                    import music
                    global playedMusic
                    try:
                        print("Playing music:")
                        nextSong = playedMusic.get_nowait()
                        print(nextSong)
                        music.play_music(nextSong)
                    except Queue.Empty:
                        print("------You tried to add a music flag '\m', but didn't also include some music. Text that generated the exception:------")
                        print(text)
                        print('---------------Music:---------------------')
                        sys.exit(1)
                #if isTitle:
                    #titleRect = textSurface.get_rect().copy()
                if justification == 0:
                    chosenSurface.blit(textSurface, (position[0] + rect.width * (columnCount % numColumnsLocal) + 20, position[1] + (font.get_linesize() * lineNum)))
                    #screen.blit(textSurface, (position[0] + rect.width * (columnCount % numColumnsLocal) + 20, position[1] + (font.get_linesize() * lineNum)))
                else:
                    chosenSurface.blit(textSurface, (position[0] + rect.width * (columnCount % numColumnsLocal), position[1] + (font.get_linesize() * lineNum)))
                previousColumnWidth = font.size(column)[0]
                columnCount += 1
                #If newPage is not empty, it means we had to add a few lines onto a new page. So we insert them now.
                if str.strip(newPage) != '':
                    pages.insert(pageCount+1, newPage)
                    pageLength += 1
                    newPage = ''
        if pageLength > 1 and pageCount < pageLength-1:
            #import traceback
            #traceback.print_stack()
            if DEBUG:
                set_commands(['(Enter) to continue.', '<==Back', '(Esc) Skip'])
            else:
                set_commands(['(Enter) to continue.', '(Esc) Skip'])
            #commandSurface = pygame.Surface((commandView.width, commandView.height))
            pygame.draw.rect(screen, LIGHT_GREY, pygame.Rect(commandView.topleft, commandView.size), 10)
            #commandSurface.fill(DARK_GREY)
            #screen.blit(commandSurface, commandView.topleft)
            display_commands()
            pygame.display.flip()
            acknowledged = False
            while not acknowledged: 
                for event in pygame.event.get():
                    if event.type == KEYUP and (event.key == K_LSUPER or event.key == K_RSUPER):
                        pygame.display.iconify()
                    elif event.type == KEYUP and event.key == K_RETURN:
                        acknowledged = True
                        break
                    elif event.type == KEYUP and event.key == K_BACKSPACE and DEBUG:
                        acknowledged = True
                        del pages[pageCount]
                        pageLength -= 1
                        if pageCount > 0:
                            pageCount -= 2
                        break
                    elif event.type == KEYUP and event.key == K_ESCAPE:
                        acknowledged = True
                        pageCount = pageLength-2
                        global playedMusic
                        playedMusic.queue.clear()
                        break
        set_commands(previousCommands, previousColors)
        pageCount += 1 

worldView = None
commandView = None
leftCommandView = None
rightCommandView = None
middleCommandView = None
size = width, height = 0, 0

def get_world_view():
    return worldView

def get_command_view():
    return commandView

def get_left_command_view():
    return leftCommandView

def get_middle_command_view():
    return middleCommandView

def get_right_command_view():
    return rightCommandView

def set_world_view(wv):
    global worldView
    worldView = wv

def set_command_view(cv):
    global commandView
    commandView = cv

game_name = ''
def set_name(new_name):
    global game_name
    game_name = new_name

def get_name():
    return game_name

def init_game():
    global worldView
    global commandView
    global leftCommandView
    global rightCommandView
    global middleCommandView
    global DEFAULT_SIZE, TITLE_SIZE
    width, height = pygame.display.Info().current_w, pygame.display.Info().current_h
    import math
    #using whichever scale is smaller to scale the font size, ensuring that the text will fit where it's supposed to.
    heightScale = (height * 1.0) / DEFAULT_RESOLUTION[1]
    widthScale = (width * 1.0) / DEFAULT_RESOLUTION[0]
    scale = heightScale if heightScale < widthScale else widthScale
    DEFAULT_SIZE = int(math.floor(DEFAULT_SIZE * scale))
    TITLE_SIZE = int(math.floor(TITLE_SIZE * scale))
    pygame.display.set_caption(get_name())
    if DEBUG:
        set_screen(pygame.display.set_mode((1920, 1080)))
    else:
        set_screen(pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE))
    #set_screen(pygame.display.set_mode(size))
    # Fill background
    set_background(pygame.Surface(get_screen().get_size()))
    set_background(get_background().convert())
    background = get_background()
    background.fill((10, 10, 10))
#We have two rectangles: The rectangle containing the world-view, and the rectangle containing the commands.
    worldView = Rect(background.get_rect().left, background.get_rect().top, background.get_rect().width, 4*background.get_rect().height/5)
    commandView = Rect(worldView.left, worldView.bottom, worldView.width, 1*background.get_rect().height/5)
#We break the commandView into 3 sub-squares. 
    font = pygame.font.SysFont(FONT_LIST, DEFAULT_SIZE)
    leftCommandView = Rect(commandView.left+5, commandView.top+5, commandView.width/3, commandView.height)
    middleCommandView = Rect(leftCommandView.right, commandView.top+5, commandView.width/3, commandView.height) 
    rightCommandView = Rect(middleCommandView.right, commandView.top+5, commandView.width/3-10, commandView.height) 
    #pygame.draw.rect(background, (250, 250, 250), commandView, 5)

postAcknowledgeFunction = None
postAcknowledgeArgs = None
def acknowledge(function, *args):
    global postAcknowledgeFunction
    global postAcknowledgeArgs
    postAcknowledgeFunction = function
    postAcknowledgeArgs = args
    set_command_interpreter(acknowledge_interpreter)
    set_commands(['(Enter) to continue.'])

def acknowledge_interpreter(keyEvent):
    print(postAcknowledgeFunction)
    print(postAcknowledgeArgs)
    if keyEvent.key == K_RETURN:
        if postAcknowledgeArgs == ((),):
            postAcknowledgeFunction()
        else:
            postAcknowledgeFunction(*postAcknowledgeArgs)


class RPGObject(object):
    """
        This is the class that ALL object types in my games should inherit from. It includes two abstract methods: save and load. The first is an instance method, the
        second is a class method.
    """

    beginLabel = 'begin:'
    endText = 'end'
    endLabel = 'end'
    
    @staticmethod
    def construct_end_text(className):
        if className.find('<class') >= 0:
            return ' '.join([RPGObject.endLabel, className])
        else:
            return ' '.join([RPGObject.endLabel, '<class', className + '>'])
    
    @staticmethod
    def construct_begin_text(className):
        return ' '.join([RPGObject.beginLabel, className])

    def begin_text(self):
        return ' '.join([RPGObject.beginLabel, str(type(self))])

    def end_text(self):
        return ' '.join([RPGObject.endLabel, str(type(self))])

    @abc.abstractmethod
    def save(self):
        """
        Returns a string containing the data of this object. Each data element is on a separate line.
        """
        raise NotImplementedError
    
    @staticmethod
    def load(dataList, obj):
        """
            Given a list of strings, containing the data about this object, and the current version of the object, updates the object to the appropriate state. 
        """
        raise NotImplementedError()


def display_commands():
        commandSurface = pygame.Surface((commandView.width, commandView.height))
        LEFT_MARGIN = commandView.width // 10
        cmdList = get_commands()
        cmdColors = get_command_colors()
        global chosenSurface
        chosenSurface = screen
        font = pygame.font.SysFont(FONT_LIST, DEFAULT_SIZE)
        accumulatedHeight = 0
        if cmdList:
            leftCommandList = cmdList[0:len(cmdList):3]
            leftCommandColors = cmdColors[0:len(cmdColors):3]
            middleCommandList = cmdList[1:len(cmdList):3]
            middleCommandColors = cmdColors[1:len(cmdColors):3]
            rightCommandList = cmdList[2:len(cmdList):3]    
            rightCommandColors = cmdColors[2:len(cmdColors):3]    
            if len(cmdList) % 3 == 1:
                try:
                    middleCommandList.append(leftCommandList.pop())  
                except AttributeError: 
                    print('The following command is not a list, like it should be: ' + middleCommandList + '. Make sure you wrapped your most recent command in a list.')
                    return
                else:
                    try:
                        middleCommandColors.append(leftCommandColors.pop())
                    except AttributeError:
                        print('The following color is not a list, like it should be: ' + str(middleCommandColors) + '. Make sure you wrapped your most recent command in a list.')
                        return
            elif len(cmdList) % 3 == 2:
                try:
                    rightCommandList.append(middleCommandList.pop())
                except AttributeError: 
                    print('The following command is not a list, like it should be: ' + rightCommandList + '. Make sure you wrapped your most recent command in a list.')
                    return
                else:
                    try:
                        rightCommandColors.append(middleCommandColors.pop())
                    except AttributeError:
                        print('The following color is not a list, like it should be: ' + str(rightCommandColors) + '. Make sure you wrapped your most recent command in a list.')
                        return
            lenLongestList = max(len(leftCommandList), len(rightCommandList), len(middleCommandList))
            if leftCommandList:
                position = (LEFT_MARGIN, font.size(leftCommandList[0])[1])
                for command, color in zip(leftCommandList, leftCommandColors):
                    if color == LIGHT_GREY:
                        font.set_bold(False)
                    else:
                        font.set_bold(True)
                    textSurface = font.render(command, True, color, BLACK)
                    commandSurface.blit(textSurface, position)
                    position = (position[0], position[1] + int(math.floor(font.size(command)[1] * 3 / lenLongestList)))
            if middleCommandList:
                position = (LEFT_MARGIN + commandView.width // 3, font.size(middleCommandList[0])[1])
                for command, color in zip(middleCommandList, middleCommandColors):
                    textSurface = font.render(command, True, color, BLACK)
                    commandSurface.blit(textSurface, position)
                    position = (position[0], position[1] + int(math.floor(font.size(command)[1] * 3 / lenLongestList)))
            if rightCommandList:    
                position = (LEFT_MARGIN + 2 * commandView.width // 3, font.size(rightCommandList[0])[1])
                for command, color in zip(rightCommandList, rightCommandColors):
                    textSurface = font.render(command, True, color, BLACK)
                    commandSurface.blit(textSurface, position)
                    position = (position[0], position[1] + int(math.floor(font.size(command)[1] * 3 / lenLongestList)))
            screen.blit(commandSurface, commandView.topleft)
            #else:
                #display_text('', rightCommandView, rightCommandView.topleft, justification=1)
        #else:
            #textSurface = textrect.render_textrect(columnNoM, font, rect, LIGHT_GREY, DARK_GREY, justification)
            #display_text('', leftCommandView, leftCommandView.topleft, justification=1)
            #display_text('', middleCommandView, middleCommandView.topleft, justification=1)
            #display_text('', rightCommandView, rightCommandView.topleft, justification=1)


def format_line(text):
    """
    Given a list of text, returns the text joined using a space as a separator. Meant to be shorthand.
    """
    return ' '.join(text)

def format_text(text, doubleSpaced=True):
    """
    Given a list of (lists of) text, returns the text joined using '\n\n' as a separator. Note that any lists of text that are contained in text are joined using a space.
    So the list ['Hi!', ['I am', 'a list!'], 'Good-bye!'] would be returned as a single string of the form:
    Hi!

    I am a list!

    Good-Bye!
    """
    textList = []
    try:
        for line in text:
            if type(line) is list:
                textList.append(' '.join(line))
            else:
                textList.append(line)
    except TypeError, e:
        print(e)
        print(text)
        sys.exit()
    return '\n\n'.join(textList) if doubleSpaced else '\n'.join(textList)


def format_text_translate(text):
    """
    Given a list of (lists of) text, returns the text joined using '' as a separator. Note that any lists of text that are contained in text are joined using a space.
    Used by the translated python code in order to provide better control over when we get paragraph separators.
    """
    textList = []
    try:
        for line in text:
            if type(line) is list:
                textList.append(' '.join(line))
            else:
                textList.append(line)
    except TypeError, e:
        print(e)
        print(text)
        sys.exit()
    return ''.join(textList)

def format_text_no_space(text, doubleSpaced=True):
    """
    Given a list of (lists of) text, returns the text joined using '\n\n' as a separator. Note that any lists of text that are contained in text are joined without a space.
    So,
    the list ['Hi!', ['I am', 'a list!'], 'Good-bye!'] would be returned as a single string of the form:
    Hi!

    Iamalist!

    Good-Bye!

    This is typically used by the auto-generated code, because it's easier to replace latex commands without worrying about context.
    """
    textList = []
    try:
        for line in text:
            if type(line) is list:
                textList.append(''.join(line))
            else:
                textList.append(line)
    except TypeError, e:
        print(e)
        print(text)
        sys.exit()
    return '\n\n'.join(textList) if doubleSpaced else '\n'.join(textList)

def quit_interpreter(keyEvent):
    """
    A simple interpreter whose only command is for quitting. Useful for debugging.
    """
    if keyEvent.key == K_ESCAPE:
       quit()

def flush_text(titleOffset=None, overwrite=True):
    global chosenSurface
    """
    Prints the text currently stored in the textToDisplay variable to the screen immediately,
    as opposed to waiting until the results of the player's commands have been processed.
    """
    textRect = worldView.copy()
    titleFont = pygame.font.SysFont(FONT_LIST_TITLE, TITLE_SIZE)
    textRect.height = textRect.height - 2 * titleFont.get_linesize()
    displayPosition = (chosenSurface.get_rect().topleft[0], 
            chosenSurface.get_rect().topleft[1] + 2 * titleFont.get_linesize())
    if titleOffset is None:
        titlePos = (chosenSurface.get_rect().topleft[0], 
                chosenSurface.get_rect().topleft[1] + titleFont.get_linesize())
    else:
        titlePos = (chosenSurface.get_rect().topleft[0], 
                chosenSurface.get_rect().topleft[1] + titleOffset) 
    if titleText != '':
        display_text(get_title_text(), chosenSurface.get_rect(), titlePos, isTitle=True) 
    if textToDisplay != '':
        display_text(get_text_to_display(), textRect, displayPosition, isTitle=False)
    display_commands()
    commandSurface = pygame.Surface((commandView.width, commandView.height))
    #screen.blit(commandSurface, commandView.topleft)
    pygame.display.flip()
    if overwrite:
        clear_text_to_display()

def s(number):
    """"
    Successor function. Easier way of writing number + 1.
    """
    return number + 1

def numbered_list(l):
    """
    Given a list l = [e_1, e_2, e_3, ..., e_n], this returns a list of strings of the form
    ["1. e_1", "2. e_2", "3. e_3", ..., "n. e_n"]
    """
    return ['. '.join([str(i), e]) for (i, e) in zip([i for i in range(1, len(l)+1)], l)] 

import sets


class State(object):
    def __init__(self):
        self.player = None
        self.bedroom = None
        self.party = None
        self.enemies = None
        self.allies = None
        self.location = None
        self.characters = {}
        self.rooms = {}
        self.items = {}
        self.difficulty = None
        self.init_scene = None
        self.instant_combat = True
        self.reset = None
        #A list of triples containing the coordinates of one-time encounters that have been cleared. This is automatically emptied at the end of each episode.
        self.clearedSquares = []

    def save(self, saveFile):
        saveData = []
        saveData.append("State Data:")
        saveData.append(self.player.save())
        saveData.append("State Data:")
        for name, char in self.characters.iteritems():
            if not char is self.player:
                saveData.append("Character:")
                saveData.append(name)
                saveData.append(char.save())
        saveData.append("State Data:")
        for name, room in self.rooms.iteritems():
            saveData.append("Room:")
            saveData.append(name)
            saveData.append(room.save())
        saveData.append("State Data:")
        saveData.append(self.bedroom.name if self.bedroom else "None")
        saveData.append("State Data:")
        saveData.extend(member.get_id() for member in self.party)
        saveData.append("State Data:")
        saveData.append(self.location.name)
        saveData.append("State Data:")
        for name, item in self.items.iteritems():
            saveData.append("Item:")
            saveData.append(name)
            saveData.append(item.save())
        saveData.append("State Data:")
        saveData.append(str(self.difficulty))
        saveData.append("State Data:")
        for coordinate in self.clearedSquares:
            saveData.append("Square:")
            saveData.append(str(coordinate))
        saveFile.write('\n'.join(saveData))

    def load(self, loadFile):
        import episode, person, townmode, items 
        try:
            import itemspotionwars
        except ImportError:
            pass
        fileData = '\n'.join(loadFile.readlines())
        #Note: The first entry in the list is just the empty string.
        try:
            _, player, characters, rooms, bedroom, party, location, itemList, difficulty, clearedSquares = fileData.split('State Data:')
        except ValueError:
            _, player, characters, rooms, bedroom, party, location, itemList, difficulty = fileData.split('State Data:')
            clearedSquares = ''
        person.PlayerCharacter.load(player, self.player)   
        if self.player.currentEpisode:
            currentEpisode = episode.allEpisodes[self.player.currentEpisode]
            currentEpisode.init()
            currentScene = currentEpisode.scenes[currentEpisode.currentSceneIndex]
            currentScene.startScene(True)
        characters = [charData.strip() for charData in characters.split("Character:") if charData.strip()]
        for charData in characters:
           name, _, charData = charData.partition('\n')
           if name.strip().lower() == 'lucilla' or name.strip().lower() == 'anastacia':
               name = "Carlita"
           try:
               person.Person.load(charData, self.characters[name.strip() + '.person'])
           except KeyError:
               try:
                   person.Person.load(charData, self.characters[name.strip() + '.playerCharacter'])
               except KeyError:
                   pass
        rooms = [roomData.strip() for roomData in rooms.split("Room:") if roomData.strip()]
        for roomData in rooms:
           name, _, roomData = roomData.partition('\n')
           try:
               townmode.Room.load(roomData, self.rooms[name])
           except KeyError, e:
               townmode.Room.load(roomData, self._backwards_compatibility_room_names(name, e))
        if bedroom.strip() != "None":
            self.bedroom = self.rooms[bedroom.strip()] 
        party = party.strip().split('\n')
        party = [name.strip() for name in party if name.strip()]
        self.party = person.Party([self.player if memberName == self.player.get_id() else self.characters[memberName] for memberName in party])
        self.location = self.rooms[location.strip()]
        itemList = [itemName.strip() for itemName in itemList.split("Item:") if itemName.strip()]
        hasQualityDagger = False
        for itemData in itemList:
            name, _, itemData = itemData.partition('\n')
            try:
                items.Item.load(itemData, self.items[name])
            except KeyError:
                pass
        try:
            self.difficulty = int(difficulty.strip())
        except ValueError:
            self.difficulty = None
        clearedSquares = [square for square in clearedSquares.split('Square:') if square.split()]
        self.clearedSquares = []
        print(clearedSquares)
        for square in clearedSquares:
            if square:
                self.clearedSquares.append(ast.literal_eval(square))

    def _backwards_compatibility_items(self, item):
        #NOTE: This function needs to be eliminated before using this code for other games. This exists solely for reasons of backwards compatibility for Potion Wars.
        import itemspotionwars
        try:
            itemName = item.name
        except AttributeError:
            itemName = item
        if itemName == 'leather cuirass':
            #&&& Working on replacing leather cuirass with a gem. We'll also need to replace qualityDagger with the player's weapon at some point, in case the player decided to sell off their family weapon.
            say_immediate(format_text([["Due to changes to the armor system, the leather cuirass no longer exists. Instead, you will receive an enhancement gem (if you haven't received one already for having the quality dagger) that Peter at Wesley and Anne's",
            "Smithy can forge into your weapon, and Carol at Therese's Tailors can",
            "forge into your clothing. You will also receive 20 coins, enough to purchase a clothing item of your choice to cover your rather exposed chest."],
            ["Hit Enter to continue loading your game."]]))
            if not itemspotionwars.attackGem in self.player.inventory:
                self.player.take_item(itemspotionwars.attackGem)
            acknowledged = False
            while not acknowledged:
                for event in pygame.event.get():
                    if event.type == KEYUP and event.key == K_RETURN:
                        acknowledged = True
                        break
            self.player.coins += 20
        elif itemName == 'quality dagger':
            if not itemspotionwars.attackGem in self.player.inventory:
                self.player.take_item(itemspotionwars.attackGem)
            say_immediate(format_text([["Due to changes to the weapon system, the quality dagger no longer exists. Instead, you will receive an enhancement gem (if you haven't received one already for having the leather cuirass) that Peter at Wesley and Anne's",
            "Smithy can forge into your weapon, and Carol at Therese's Tailors can forge into your clothing."]]))
            if all(map(lambda x : x not in self.player.inventory, [itemspotionwars.familyDagger, itemspotionwars.familySword, itemspotionwars.familySpear])):
                say_immediate(format_text([['''It appears that you got rid of your starting weapon in favor of the quality dagger. Since the family weapons are rather unique, you'll now be given the option of selecting a new family weapon, just like at''',
                    '''the''','''beginning''', '''of the game. Please make your choice:'''], ['''1. Family Dagger'''], ['''2. Family Sword'''], ['''3. Family Spear''']]))
                choiceMade = False
                while not choiceMade:
                    for event in pygame.event.get():
                        if event.type == KEYUP:
                            if event.key == K_1:
                                self.player.take_item(itemspotionwars.familyDagger)
                                choiceMade = True
                                break
                            elif event.key == K_2:
                                self.player.take_item(itemspotionwars.familySword)
                                choiceMade = True
                                break
                            elif event.key == K_3:
                                self.player.take_item(itemspotionwars.familySpear)
                                choiceMade = True
                                break
            else:
                universal.say_immediate("Hit Enter to continue loading your game.")
                if not itemspotionwars.attackGem in self.player.inventory:
                    self.player.take_item(itemspotionwars.attackGem)
                acknowledged = False
                while not acknowledged:
                    for event in pygame.event.get():
                        if event.type == KEYUP and event.key == K_RETURN:
                            acknowledged = True
                            break

    def clear_one_time_encounters(self):
        self.clearedSquares = []

    def clear_encounter(self, coordinate):
        self.clearedSquares.append(coordinate)

    def is_clear(self, coordinate):
        return coordinate in self.clearedSquares

    def set_init_scene(self, init_scene):
        self.init_scene = init_scene

    def __setstate__(self, state):
        self.__dict__ = state
        #Forces the version of the location stored in the state, and the version in the rooms function to agree.
        self.location = self.rooms[self.location.name]
        #Quick and dirty hack because I'm too fucking lazy to modify my save file. Note: Write save interpreter!
        #if not self.bedroom:
            #self.bedroom = self.get_room("Maria's Home")
        if not 'instant_combat' in state: 
            self.instant_combat = True
        try:
            self.init_scene()
        except TypeError:
            pass

    """
        def add_position(self, position):
            self.positions[position.name] = position

        def remove_position(self, position):
            try:
                del positions[position.name]
            except KeyError:
                return


        def add_scene(self, scene):
            self.scenes[scene.name] = scene

        def remove_scene(self, scene):
            try:
                self.scenes.remove(scene)
            except KeyError:
                return

        def add_episode(self, episode):
            self.episodes[episode.name] = episode

        def remove_episode(self, episode):
            try:
                del self.episodes[episode.name]
            except KeyError:
                return

    """

    def add_item(self, item):
        self.items[item.name] = item

    def get_item(self, itemName):
        return self.items[itemName]

    def remove_item(self, item):
        try:
            del self.items[item.name]
        except KeyError:
            return

    def add_room(self, room):
        self.rooms[room.name] = room

    def remove_room(self, room):
        try:
            del self.rooms[room.name]
        except KeyError:
            return

    def get_room(self, room):
        try:
            return self.rooms[room.name]
        except AttributeError:
            try:
                return self.rooms[room]
            except KeyError, e:
                return self._backwards_compatibility_room_names(room, e)
        except KeyError, e:
                return self._backwards_compatibility_room_names(room, e)

    def _backwards_compatibility_room_names(self, room, e):
        """
            NOTE: This is here to keep save files compatible with the change in the name of Peter's shop. This should be deleted before using this engine for future games.
        """
        try:
            roomName = room.name
        except AttributeError:
            roomName = room
        if roomName == "Wesley and Anne's Weapons and Armor":
            return self.rooms["Wesley and Anne's Smithy"]
        elif roomName == "offStage":
            #Hacking away and I don't care!
            import townmode
            return townmode.offStage
        elif roomName == "Wesley and Anne's Smithy":
            return self.rooms["Wesley and Anne's Weapons and Armor"]
        else:
            raise e

    def add_character(self, character):
        self.characters[character.get_id()] = character

    def replace_character(self, character):
        self.add_character(character)

    def remove_character(self, character):
        try:
            del self.characters[character.get_id()]
        except KeyError:
            return

    def get_character(self, character):
        """
        Returns a particular character from the state. There are several ways of obtaining a character:
        1. Pass a character object containing the same id (name.person if the character is an NPC, name.playerCharacter if the the character is a PC)
        2. Pass name.person (if seeking an NPC) and name.playerCharacter (if seeking a PC).
        3. Pass "name." Then, the function will first try to find a player character with that name, then an NPC. This is because we generally know a priori when we want to obtain a particular NPC, but we can't hard-code the
        player's name, because we don't know the player's name yet.
        """
        print(self.characters)
        try:
            return self.characters[character.get_id()]
        except AttributeError:
            try:
                return self.characters[character]
            except KeyError:
                try:
                    return self.characters[''.join([character, '.playerCharacter'])]
                except KeyError:
                    try:
                        return self.characters[''.join([character, '.person'])]
                    except KeyError, e:
                        return self._backwards_compatibility_person_names(character, e)

    def _backwards_compatibility_person_names(self, character, e):
        try:
            characterName = character.get_id()
        except AttributeError:
            characterName = character
        if characterName == "Lucilla.person": 
            try:
                character =  self.get_character("Edita.person")
            except KeyError:
                character =  self.get_character("Lucilla.person")
        elif characterName == "Carlita.person":
            try:
                character =  self.get_character("Edita.person")
            except KeyError:
                character =  self.get_character("Lucilla.person")
        else:
            raise e


state = State()

def set_state(stateIn):
   global state
   state = stateIn

def set_initial_room(room):
    global state
    state.location = room

def set_state(stateIn):
    global state
    state = stateIn

def cond(condition, ifTrue, ifFalse):
    return ifTrue if condition else ifFalse

def msg_selector(attribute, msgMap):
    return msgMap[attribute]
