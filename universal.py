"""
    Universal.py contains various functions and operations that need to be accessible by every other file in the engine, in particular: 
    1. The say function for displaying text
    2. The set_command_interpreter and get_command_interpreter functions for modifying how the game interprets various keyboard commands.
    3. A quit() command that adds a quit event to the event queue. 
    4. Functions for getting and setting the list of commands to be displayed.
"""
from __future__ import print_function 
import sys, pygame, textrect, abc
import Queue
from pygame.locals import *
import os

DEBUG = False

NUM_TIERS = 9

def resource_path(relative):
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, 'data', relative)

author = 'AKA'
programmer = 'AKA'
authorEmailBugs = 'sprpgs@gmail.com+bugs'
programmerEmailBugs = 'sprpgs@gmail.com+bugs'
authorEmail = 'sprpgs@gmail.com'
programmerEmail = authorEmail

NUM_STATS = 9
WARFARE = 0
MAGIC = 1
WILLPOWER = 2
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

def set_commands(newCommands):
    """
        Set the commands to be used by the player. Raises a ValueError if the number of commands passed exceeds 9 (the maximum number that can be displayed).
    """
    global commands
    if commands != newCommands:
        clear_commands()
    if not type(newCommands) == list:
        commands = [newCommands]
    elif len(newCommands) > 9:
        raise ValueError('Number of commands cannot exceed 9. Problem commands: ' + ', '.join(newCommands))
    else:
        commands = newCommands

def get_commands():
    return commands

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
    titleFont = pygame.font.SysFont(FONT_LIST, TITLE_SIZE)
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
difficulty = 0
def set_difficulty(diff):
    global difficulty
    difficulty = diff

def get_difficulty():
    return difficulty

#Make sure to confirm font names for Windows and Mac.
FONT_LIST = 'Lucida Grande, Segoe UI, rachana'


BLACK = (0,0,0)
DARK_GREY = (10, 10, 10)
LIGHT_GREY = (200, 200, 200)
WHITE = (250,250,250)
GREEN = (0, 100, 0)
RED = (100, 0, 0)
BLUE = (25, 25, 125)
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
        while columnCount < numSeparateColumns:
            column = columns[columnCount]
            #Need to wrap back around to the first column.
            if columnCount >= numColumnsLocal and columnCount % numColumnsLocal == 0:
                lineNum += 1
            textSurface = None
            if isTitle:
                font = pygame.font.SysFont(FONT_LIST, TITLE_SIZE)
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
                        nextSong = playedMusic.get_nowait()
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
            import traceback
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
                    if event.type == KEYUP and event.key == K_RETURN:
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
        set_commands(previousCommands)
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
        set_screen(pygame.display.set_mode(size))
    else:
        set_screen(pygame.display.set_mode(size, pygame.FULLSCREEN))
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
    if keyEvent.key == K_RETURN:
        if postAcknowledgeArgs == ((),):
            postAcknowledgeFunction()
        else:
            postAcknowledgeFunction(*postAcknowledgeArgs)


class RPGObject(object):
    """
        This is the class that ALL object types in my games should inherit from. It includes two abstract methods: _save and _load. The first is an instance method, the
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
    def _save(self):
        return self.begin_text()
    
    @staticmethod
    def _load(dataList):
        """
            Given a list of strings containing the data about this object, returns a constructed object of the appropriate type with the appropriate state. 
        """
        raise NotImplementedError()

def display_commands():
        commandList = get_commands()
        set_column_number(1)
        global chosenSurface
        chosenSurface = screen
        if commandList != None:
            leftCommandList = commandList[0:len(commandList):3]
            middleCommandList = commandList[1:len(commandList):3]
            rightCommandList = commandList[2:len(commandList):3]    
            if len(commandList) % 3 == 1:
                try:
                    middleCommandList.append(leftCommandList.pop())  
                except AttributeError: 
                    print('The following command is not a list, like it should be: ' + middleCommandList + '. Make sure you wrapped your most recent command in a list.')
                    return
            elif len(commandList) % 3 == 2:
                try:
                    rightCommandList.append(middleCommandList.pop())
                except AttributeError: 
                    print('The following command is not a list, like it should be: ' + rightCommandList + '. Make sure you wrapped your most recent command in a list.')
                    return
            if leftCommandList != None:
                display_text('\n'.join([''] + leftCommandList), leftCommandView, leftCommandView.topleft, justification=1)
            else:
                display_text('', leftCommandView, leftCommandView.topleft)
            if middleCommandList != None:
                display_text('\n'.join([''] + middleCommandList), middleCommandView, middleCommandView.topleft, justification=1)
            else:
                display_text('', middleCommandView, middleCommandView.topleft)
            if rightCommandList != None:    
                display_text('\n'.join([''] + rightCommandList), rightCommandView, rightCommandView.topleft, justification=1)
            else:
                display_text('', rightCommandView, rightCommandView.topleft, justification=1)
        else:
            display_text('', leftCommandView, leftCommandView.topleft, justification=1)
            display_text('', middleCommandView, middleCommandView.topleft, justification=1)
            display_text('', rightCommandView, rightCommandView.topleft, justification=1)


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
    titleFont = pygame.font.SysFont(FONT_LIST, TITLE_SIZE)
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
