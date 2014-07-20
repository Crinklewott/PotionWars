""" Copyright 2014 Andrew Russell 

This file is part of PotionWars.  PotionWars is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

PotionWars is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with PotionWars.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
import sys
import re
import person
import textrect
import townmode
import universal
from universal import *
import pygame
from pygame.locals import *
import music
import os
import episode
import items
import itemspotionwars
import copy

""" Note: This file will have to be modified if we ever decide to have multiple universal.state.player's. Not quite sure what the best way of handling the case of multiple universal.state.player's is. We'll have
    to see.
"""

gameTitle = ''

TITLE_IMAGE_FILE = None
TITLE_IMAGE_FILE_1 = None
TITLE_IMAGE_FILE_2 = None
TITLE_IMAGE_FILE_3 = None

TITLE_IMAGES = []

def set_title_image(image, extension, numImages):
    "Note: DO NOT provide the extension when providing the path. Provide the extension separately."
    global TITLE_IMAGES
    TITLE_IMAGES.append(image + "." + extension)
    for i in range(1, numImages):
        TITLE_IMAGES.append(image + str(i) + "." + extension)
    print(TITLE_IMAGES)

def title(text):
    global gameTitle
    gameTitle = text

def get_title():
    return gameTitle

gameSubtitle = ''
def subtitle(text):
    global gameSubtitle
    gameSubtitle = text

def get_subtitle():
    return gameSubtitle

firstEpisode = None
OPENING_CRAWL = None

def set_opening_crawl(musicFile, alreadyDecrypted=True):
    global OPENING_CRAWL
    if alreadyDecrypted:
        OPENING_CRAWL = musicFile
    else:
        OPENING_CRAWL = music.decrypt(resource_path(musicFile))

def title_screen_interpreter(keyEvent):
    if keyEvent.key == pygame.K_s:
        request_difficulty()
    elif keyEvent.key == pygame.K_ESCAPE:
        quit()
    elif keyEvent.key == pygame.K_l:
        load_game()
    elif keyEvent.key == pygame.K_a:
        display_acknowledgments()

def display_acknowledgments():
    universal.say_title('Acknowledgments')
    universal.get_screen().blit(universal.get_background(), universal.get_world_view().topleft)
    universal.say(format_text([['Code, Story, Concept: Andrew Russell'], 
        ['Coded in Python using the Pygame engine: pygame.org'],
        ['Images:'],
        ['  title screen image: Rak'],
        #['Sound Effects: Filippo Vicarelli. Downloaded from his website: noiseforfun.com'],
        #['Dungeon step: Click Switch'],
        ['Music: Filippo Vicarelli. Purchased through his website: playonloop.com.'], 
        ['  Opening Crawl/Church theme: Apparition'],
        ['  Title Theme: The Challenge'],
        ['  Episode 1 Titlecard: Bridge over Darkness'],
        ["  Vengador's Theme: Antique Market"],
        ["  Guard's Theme: War Victimis"],
        ['  Avaricum Theme: Spiritual Path'],
        ['  Battle Theme: The Chase'],
        ["  Peaceful Theme(Adventurer's Guild): Jesu"],
        ['  Tense Theme: Hurry Up'],
        ['  Defeated Theme: Graveyard Lord'],
        ["  Peter's Theme: Telekinesis"],
        ["  Carlita's Theme: Goodbye"],
        ["  Maria's Theme : Moonlight"],
        ["  Carrie's Theme: Smart Ideas"],
        ["  Catalin's Theme: Sadistic Game"],
        ["  Roland's Theme: Risky Plan"],
        ["  Elise's Theme: Land of Peace"],
        ]
        ))
    acknowledge(title_screen, None)

def display_title():
    """
    Unused.
    """
    titleImage = pygame.image.load(TITLE_IMAGE_FILE)
    universal.get_screen().blit(titleImage)
    universal.get_screen().flip()
    """
    display_text(get_title() + ":", worldView, worldView.midleft)
    display_text(get_subtitle() + ":", worldView, worldView.midleft)
    """
    

DELAY_INCREMENTS = 100
DELAY_TIME = 8000
DELAY_TIME_SHORT = DELAY_TIME / 2
DELAY_TIME_REALLY_SHORT = DELAY_TIME / 4
DELAY_TIME_LONG = 2 * DELAY_TIME

skip = False
def check_delay():
    for event in pygame.event.get():
        if event.type == KEYUP and event.key == K_RETURN:
            global skip
            skip = True

def delay_really_short():
    count = 0
    while not skip and count < DELAY_TIME_REALLY_SHORT / DELAY_INCREMENTS:
        check_delay()
        pygame.time.delay(DELAY_INCREMENTS)
        count += 1
def delay_short():
    count = 0
    while not skip and count < DELAY_TIME_SHORT / DELAY_INCREMENTS:
        check_delay()
        pygame.time.delay(DELAY_INCREMENTS)
        count += 1

def delay():
    count = 0
    while not skip and count < DELAY_TIME / DELAY_INCREMENTS:
        check_delay()
        pygame.time.delay(DELAY_INCREMENTS)
        count += 1

def delay_long():
    count = 0
    while not skip and count < DELAY_TIME_LONG / DELAY_INCREMENTS:
        check_delay()
        pygame.time.delay(DELAY_INCREMENTS)
        count += 1

def display_crawl():
    if skip:
        universal.say_replace('')
    worldView = universal.get_world_view()
    textRect = universal.get_world_view().copy()
    titleFont = pygame.font.SysFont(universal.FONT_LIST, universal.TITLE_SIZE)
    displayPosition = (worldView.topleft[0], worldView.topleft[1] + 2 * titleFont.get_linesize())
    universal.display_text(universal.get_text_to_display(), textRect, displayPosition, isTitle=False)
    pygame.display.flip()

def opening_crawl():
    #universal.say_replace([
    #"You've been stabbed in the stomach. Your health magic triggers."])
    #display_crawl()
    #delay_short()  
    #universal.say_replace("But there's no damage to repair.")
    #display_crawl()
    #delay_short()
    universal.say_replace(['''Pandemonium Cycle: The Potion Wars is intended for adults only. Spanking and other erotic content depicted are fantasies and intended for''',
    '''adults only. Nothing in this game should be interpreted as''', 
    '''advocating any form of non-consensual spanking or the spanking of minors.''',
    '''\n-Andrew Russell''',
    '''\n\nTo skip the opening crawl (which will begin shortly), press Enter at any time.'''])
    display_crawl()
    delay()
    if not skip:
        music.play_music(OPENING_CRAWL, fadeoutTime=0, wait=True)
    universal.say_replace(["Along the coast of the Medios Sea is a region rife with bickering city-states, known collectively as the 1024. The city-states are inhabited by two broad cultures: the bronze-skinned "
        "Taironans, and the much paler Carnutians."])
    display_crawl()
    delay()
    universal.say_replace(["Magic permeates this world, like oxygen permeates our own. Just as we have adapted to use oxygen, so have they adapted to use magic.",
        "They instinctively use magic to strengthen their bodies, making the average person faster, stronger, and more perceptive than our greatest athletes. Each has a",
        "special store of magic, called health, that allows them to instantly heal serious injuries."])
    display_crawl()
    delay_long()
    universal.say_replace(["However, there is a terrible and feared disease called the Wasting Wail. So long as someone is inflicted with the Wail, their body believes",
    "they are covered in terrible wounds, and tries to heal these nonexistent injuries. Their body heals, and heals, until they have no more health. Then, the body",
    "pulls energy from other places, and continues healing, until either they are lucky, and the disease passes, or if they are unlucky, they die."])
    display_crawl()
    delay_long()
    universal.say_replace(["In the hear 1273, the Wasting Wail descended upon the Taironan city of Bonda. It started in the Merchant District, spread into the slums, and",
    "even touched the nobility. The other cities instituted a strict quarantine, and left Bonda alone to endure the ravages of the plague"])
    display_crawl()
    delay_long()
    universal.say_replace(["But then, a group of Brothers and Sisters from the Matirian Church, a powerful (Carnutian) religion arrived at the gates of Bonda. They",
    "carried with them a new invention: Potions."])
    display_crawl()
    delay()
    universal.say_replace(["These Potions, they claimed, were healers in a bottle. They would keep the plague",
            "victims' energy up long enough for them to recover. Out of sheer desperation, the Bondan king allowed the healers into",
            "the city."])
    display_crawl()
    delay_long()
    universal.say_replace(["The death rate dropped from 40% to 5%. When the plague finally ended, there was",
            "a massive celebration throughout the city. Bonda and Avaricum prepared to enter an everlasting",
            "alliance. The Matirian Brothers and Sisters stopped distributing Potions."])
    display_crawl()
    delay_long()
    universal.say_replace([
            "The earliest recipients of the Potions",
            "sank into a deep depression. They couldn't sleep, they could barely",
            "eat, they shook uncontrollably, and some",
            "suffered severe seizures. Crowds gathered outside the Matirian treatment centers,",
            "but", 
            "the Matirians didn't have enough Potions to handle this new, strange disease.",
            "Some began to accuse the Matirians of holding out. Others claimed that the Potions",
            "were poison, part of an Avaricumite plot to conquer Bonda."])
    display_crawl()
    delay_long()
    universal.say_replace("The crowds turned into mobs.")
    display_crawl()
    delay_short()
    universal.say_replace(["Treatment centers were attacked. Brothers and Sisters viciously beaten. Bondan",
            "fought Bondan, brother against sister, for the precious few remaining Potions.",
            "An Avaricumite army arrived and occupied Bonda, helping the Brothers and Sisters",
            "escape."])
    display_crawl()
    delay_long()
    universal.say_replace("A little over twenty years have passed. Bonda has all but collapsed, and Avaricum teeters on the edge of a")
    display_crawl()
    if not skip:
        music.play_music(music.THEME, DELAY_TIME / 3, wait=True)
    else:
        music.play_music(music.THEME, wait=True)
    #delay_short()

loadingGame = True

def title_screen(episode=None):
    global firstEpisode, loadingGame
    textSurface = None
    titleImage = None
    try:
        titleImage = pygame.image.load(TITLE_IMAGES[0])
        titleImage = pygame.transform.scale(titleImage, (pygame.display.Info().current_w, pygame.display.Info().current_h))
    except IOError:
        textSurface = textrect.render_textrect(get_title(), #+ (":" if get_subtitle() != "" else ""), 
                font, worldView, LIGHT_GREY, DARK_GREY, 1)
    except IndexError:
        textSurface = textrect.render_textrect(get_title(), #+ (":" if get_subtitle() != "" else ""), 
                font, worldView, LIGHT_GREY, DARK_GREY, 1)
    titleImages = []
    if os.path.exists(os.path.join(os.getcwd(), 'save')) and '.init.sav' in os.listdir(os.path.join(os.getcwd(), 'save')):
        #townmode.clear_rooms()
        print('loading .init.sav')
        townmode.previousMode = None
        townmode.load_game('.init.sav', preserveLoadName=False)
    else:
        townmode.save_game('.init.sav', preserveSaveName=False)
    assert(episode is not None or firstEpisode is not None)
    if episode is not None:
        firstEpisode = episode
    screen = universal.get_screen()
    worldView = universal.get_world_view()
    background = universal.get_background()
    screen.fill(universal.DARK_GREY)
    font = pygame.font.SysFont(universal.FONT_LIST, 50)
    wvMidLeft = worldView.midleft
    if loadingGame:
        for i in range(1, len(TITLE_IMAGES)):
            try:
                titleImages.append(pygame.image.load(TITLE_IMAGES[i]))
                titleImages[-1] = pygame.transform.scale(titleImages[-1], (pygame.display.Info().current_w, pygame.display.Info().current_h))
            except IOError:
                continue
        opening_crawl()
        loadingGame = False
    music.play_music(music.THEME)
    universal.set_commands(['(S)tart', '(L)oad', '(A)cknowledgments', '(Esc)Quit'])
    universal.set_command_interpreter(title_screen_interpreter)
    if not skip:
        pygame.time.delay(125)
        for i in range(0, len(titleImages)):
            print('printing image: ' + str(i))
            screen.blit(titleImages[i], worldView.topleft)
            pygame.time.delay(25)
            pygame.display.flip()
    if titleImage is not None:
        screen.blit(titleImage, worldView.topleft)
    else:
        screen.blit(textSurface, worldView.centerleft)
    pygame.display.flip()
    while 1:
        universal.textToDisplay = ''
        universal.titleText = ''
        for event in pygame.event.get():
            if event.type == KEYUP:
                import traceback
                traceback.print_stack()
                return
    #subtitleLocation = (wvMidLeft[0], wvMidLeft[1]+50)
    #textSurface = textrect.render_textrect(get_subtitle(), pygame.font.SysFont(universal.FONT_LIST, 30), worldView, LIGHT_GREY, DARK_GREY, 1)
    #screen.blit(textSurface, subtitleLocation)
    #pygame.display.update()

def request_difficulty():
    universal.say_title('Character Creation')
    universal.get_screen().blit(universal.get_background(), universal.get_world_view().topleft)
    universal.say('Before we get started, we need to pick a difficulty level:\n\n')
    universal.say('HAND: Enemies choose their actions purely at random.\n\n')
    universal.say('STRAP: Enemies choose their actions based on their own statistics, and the skills of their allies. They choose their target at random.\n\n')
    universal.say('CANE: Enemies choose their actions based on their statistics, the skills of their allies and previous rounds. They choose their target based on the effects of previous rounds.')
    universal.set_commands(['(H)and', '(S)trap', '(C)ane', '(Esc)Quit', '<==Back'])
    universal.set_command_interpreter(request_difficulty_interpreter)

def request_difficulty_interpreter(keyEvent):
    validCommand = False
    if keyEvent.key == pygame.K_ESCAPE:
        quit()
    elif keyEvent.key == pygame.K_h:
        universal.set_difficulty(universal.HAND)
        validCommand = True
    elif keyEvent.key == pygame.K_s:
        universal.set_difficulty(universal.STRAP)
        validCommand = True
    elif keyEvent.key == pygame.K_c:
        universal.set_difficulty(universal.CANE)
        validCommand = True
    elif keyEvent.key == pygame.K_BACKSPACE:
        title_screen(firstEpisode)
    if validCommand:
        request_gender()

requestNameString = 'Please provide a name, and hit enter when done. Note: The beginning of your name will be automatically capitalized as you type. To erase, use the backspace. To return to the previous screen, press the Esc key.\n'

partialName = ''
def request_name():
    global partialName, gender
    universal.say(requestNameString)
    universal.set_commands(['Esc'])
    if gender == person.MALE:
        partialName = 'Julian'
    else:
        partialName = 'Juliana'
    universal.say(partialName)
    universal.say('_')
    universal.set_command_interpreter(request_name_interpreter)


def request_name_interpreter(keyEvent):
    global partialName
    if keyEvent.key == K_RETURN:
        universal.state.player = person.PlayerCharacter(partialName, gender)
        person.get_PC().set_all_stats(2, 2, 2, 2, 2, 20, 10)
        person.set_party(person.Party([person.get_PC()]))
        universal.state.player.currentEpisode = firstEpisode.name
        universal.state.player.name = partialName
        universal.state.player.set_fake_name()
        request_nickname()
    elif keyEvent.key == K_ESCAPE:
        partialName = ''
        request_gender()
    else:
        playerInput = pygame.key.name(keyEvent.key)
        if re.match(re.compile(r'^\w$'), playerInput):
            partialName += playerInput
        elif keyEvent.key == K_BACKSPACE:
            partialName = partialName[:-1]
        universal.say(requestNameString)
        partialName = simpleTitleCase(partialName)
        if keyEvent.key == K_SPACE:
            partialName += ' '
        universal.say(partialName)
        universal.say('_')

def request_nickname():
    global partialName
    universal.say('Provide a nickname for your character:\n')
    universal.set_commands(['Esc'])
    print(universal.state.player)
    print(universal.state.player.gender)
    if universal.state.player.is_male():
        partialName = 'Juli'
    elif universal.state.player.is_female():
        partialName = 'Julia'
    universal.say(partialName)
    universal.say('_')
    universal.set_command_interpreter(request_nickname_interpreter)

def request_nickname_interpreter(keyEvent):
    global partialName
    if keyEvent.key == K_RETURN:
        universal.state.player.nickname = partialName
        request_body_type()
    elif keyEvent.key == K_ESCAPE:
        partialName = ''
        request_name()
    else:
        playerInput = pygame.key.name(keyEvent.key)
        if re.match(re.compile(r'^\w$'), playerInput):
            partialName += playerInput
        elif keyEvent.key == K_BACKSPACE:
            partialName = partialName[:-1]
        universal.say('Provide a nickname for your character:\n')
        partialName = simpleTitleCase(partialName)
        if keyEvent.key == K_SPACE:
            partialName += ' '
        universal.say(partialName)
        universal.say('_')

#BODY_TYPES = ['slim', 'average', 'voluptuous', 'heavyset']
def request_body_type():
    universal.say_title('Select Body Type')
    universal.say('\n'.join(universal.numbered_list(person.BODY_TYPES)), justification=0)
    set_command_interpreter(request_body_type_interpreter)
    set_commands(universal.SELECT_NUMBER_BACK_COMMAND)

def request_body_type_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            request_nickname()
        return
    else:
        try:
            universal.state.player.bodyType = person.BODY_TYPES[num]
        except IndexError:
            return
        else:
            request_height()

#HEIGHT = ['short', 'average', 'tall', 'huge']
def request_height():
    NUM_INCHES_IN_FOOT = 12
    NUM_METERS_IN_INCH = .0254
    def inches_to_meters(inches):
        return round(inches * NUM_METERS_IN_INCH, 2)
    universal.say_title('Select Height')
    height = universal.numbered_list([h + ':' for h in person.HEIGHTS])
    increment = NUM_INCHES_IN_FOOT //  len(person.HEIGHTS) 
    heightNums = []
    for i in range(len(height)):
        bottom = 5*12 + increment * i
        top =  5*12 + increment * (i + 1)
        heightNums.append(''.join([str(bottom // NUM_INCHES_IN_FOOT), "'", str(bottom % NUM_INCHES_IN_FOOT), '"', ' (', str(inches_to_meters(bottom)), 'm)', ' - ', 
            str(top // NUM_INCHES_IN_FOOT), "'", str(top % NUM_INCHES_IN_FOOT), '"', ' (', str(inches_to_meters(top)), 'm)']))
    heightNums = '\n'.join(heightNums)
    height = '\n'.join(height)
    print('---------------height------------------')
    print('\n'.join(height))
    universal.say(height + '\t' + heightNums, columnNum=4, justification=0)
    set_commands(universal.SELECT_NUMBER_BACK_COMMAND)
    set_command_interpreter(request_height_interpreter)

def request_height_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            request_body_type()
        return
    else:
        try:
            universal.state.player.height = person.HEIGHTS[num]
        except IndexError:
            return
        else:
            request_musculature()

#MUSCULATURE = ['soft', 'fit', 'muscular']
def request_musculature():
    universal.say_title('Select Musculature')
    musculature = '\n'.join([m + ':' for m in universal.numbered_list(person.MUSCULATURE)])
    musculatureDescr = [
            ' '.join(['', universal.state.player.name, '''has a soft, jiggly body.''']), 
            ' '.join(['', universal.state.player.name, '''has a firm, smooth body.''']), 
            ' '.join(['', universal.state.player.name, '''has a hard, muscled body.'''])
            ]
    musculatureDescr = '\n'.join(musculatureDescr)    
    universal.say(musculature + '\t' + musculatureDescr, justification=0, columnNum=3)
    set_command_interpreter(request_musculature_interpreter)
    set_commands(universal.SELECT_NUMBER_BACK_COMMAND)

def request_musculature_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            request_height()
        return
    else:
        try:
            universal.state.player.musculature = person.MUSCULATURE[num]
        except IndexError:
            return
        else:
            request_hair_length()




#HAIR_LENGTH = ['short', 'shoulder-length', 'back-length', 'butt-length']
def request_hair_length():
    universal.say_title('Select Hair Length')
    universal.say('\n'.join(numbered_list(person.HAIR_LENGTH)), justification=0)
    set_commands(universal.SELECT_NUMBER_BACK_COMMAND)
    set_command_interpreter(request_hair_length_interpreter)

def request_hair_length_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            request_musculature()
        return
    else:
        try:
            universal.state.player.hairLength = person.HAIR_LENGTH[num]
        except IndexError:
            return
        else:
            request_hair_style()

def get_hair_style():
    player = universal.state.player
    if player.hairLength == 'short':
        hairStyle = person.SHORT_HAIR_STYLE
    elif player.hairLength == 'shoulder-length':
        hairStyle = person.SHOULDER_HAIR_STYLE
    elif player.hairLength == 'back-length':
        hairStyle = person.BACK_HAIR_STYLE
    elif player.hairLength == 'butt-length':
        hairStyle = person.BUTT_HAIR_STYLE
    return hairStyle

def request_hair_style():
    universal.say_title('Select Hair Style')
    player = universal.state.player
    universal.say('\n'.join(numbered_list(get_hair_style())), justification=0)
    set_commands(SELECT_NUMBER_BACK_COMMAND)
    set_command_interpreter(request_hair_style_interpreter)

def request_hair_style_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            request_hair_length()
        return
    else:
        try:
            universal.state.player.hairStyle = get_hair_style()[num]
        except IndexError:
            return
        else:
            select_shirt()

#[itemspotionwars.thong, itemspotionwars.lacyUnderwear, itemspotionwars.boyShorts, itemspotionwars.underShorts
shirtList = []
chosenShirt = None
#TODO: Refactor all of this to allow me to set it through the game file rather than in titleScreen.
def select_shirt():
    global shirtList
    universal.say_title('Select Shirt')
    shirtList = [itemspotionwars.vNeckTunic, itemspotionwars.tunic, itemspotionwars.blouse, itemspotionwars.bra, itemspotionwars.blackDress, itemspotionwars.sunDress,
            itemspotionwars.robe, items.emptyUpperArmor]
    universal.say('\n'.join(universal.numbered_list([shirt.name for shirt in shirtList])), justification=0)
    set_commands(universal.SELECT_NUMBER_BACK_COMMAND)
    set_command_interpreter(select_shirt_interpreter)

def select_shirt_interpreter(keyEvent):
    global chosenShirt
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            request_hair_style()
    else:
        try:
            chosenShirt = shirtList[num]
        except IndexError:
            return
        else:
            universal.say(chosenShirt.display())
            set_command_interpreter(confirm_shirt_interpreter)
            set_commands(['(Enter) Equip shirt', '<==Back'])

def confirm_shirt_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        universal.state.player._set_shirt(copy.deepcopy(chosenShirt))
        if isinstance(chosenShirt, items.FullArmor):
            universal.state.player._set_lower_clothing(universal.state.player.shirt())
        else:
            universal.state.player._set_lower_clothing(items.emptyLowerArmor)
        select_lower_clothing()
    elif keyEvent.key == K_BACKSPACE:
        select_shirt()

chosenPants = None
pantsList = []
def select_lower_clothing():
    global pantsList
    print(universal.state.player.lower_clothing().name)
    print(universal.state.player.shirt().name)
    if universal.state.player.lower_clothing() is universal.state.player.shirt():
        select_underwear()
    else:
        universal.say_title('Select Lower Clothing')
        pantsList = [itemspotionwars.shorts, itemspotionwars.shortShorts, itemspotionwars.plainSkirt, itemspotionwars.miniSkirt, itemspotionwars.pencilSkirt,
                items.emptyLowerArmor]
        universal.say('\n'.join(universal.numbered_list([pants.name for pants in pantsList])), justification=0)
        set_commands(universal.SELECT_NUMBER_BACK_COMMAND)
        set_command_interpreter(select_lower_clothing_interpreter)

def select_lower_clothing_interpreter(keyEvent):
    global chosenPants
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            select_shirt()
    else:
        try:
            chosenPants = pantsList[num]
        except IndexError:
            return
        else:
            universal.say(chosenPants.display())
            set_command_interpreter(confirm_lower_clothing_interpreter)
            set_commands([' '.join(['(Enter) Equip', chosenPants.armorType]), '<==Back'])
    
def confirm_lower_clothing_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        universal.state.player._set_lower_clothing(copy.deepcopy(chosenPants))
        select_underwear()
    elif keyEvent.key == K_BACKSPACE:
        select_lower_clothing()

underwearList = []
chosenUnderwear = None

def select_underwear():
    global underwearList
    underwearList = [itemspotionwars.thong, itemspotionwars.lacyUnderwear, itemspotionwars.boyShorts, itemspotionwars.underShorts, itemspotionwars.modestUnderwear,
            items.emptyUnderwear]
    if universal.state.player.lower_clothing() == items.emptyLowerArmor:
        underwearList.remove(items.emptyUnderwear)
    universal.say_title('Select Underwear')        
    universal.say('\n'.join(universal.numbered_list([underwear.name for underwear in underwearList])), justification=0)
    set_commands(SELECT_NUMBER_BACK_COMMAND)
    set_command_interpreter(select_underwear_interpreter)

def select_underwear_interpreter(keyEvent):
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            print('keyError!')
            if universal.state.player.shirt() is universal.state.player.lower_clothing():
                select_shirt()
            else:
                select_lower_clothing()
    else:
        global chosenUnderwear
        try:
            chosenUnderwear = underwearList[num]
        except IndexError:
            return
        else:
            universal.say(chosenUnderwear.display())
            set_commands(['(Enter) Equip underwear', '<==Back'])
            set_command_interpreter(confirm_underwear_interpreter)

def confirm_underwear_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        universal.state.player._set_underwear(copy.deepcopy(chosenUnderwear))
        select_weapon()
    elif keyEvent.key == K_BACKSPACE:
        select_underwear()
  
weaponList = []
chosenWeapon = None
def select_weapon():
    global weaponList
    weaponList = [itemspotionwars.familyDagger, itemspotionwars.familySword, itemspotionwars.familySpear]
    universal.say_title('Request Weapon')
    universal.say('\n'.join(universal.numbered_list([weapon.name for weapon in weaponList])), justification=0)
    set_commands(SELECT_NUMBER_BACK_COMMAND)
    set_command_interpreter(select_weapon_interpreter)

def select_weapon_interpreter(keyEvent):
    global chosenWeapon
    try:
        num = int(universal.key_name(keyEvent)) - 1
    except ValueError:
        if keyEvent.key == K_BACKSPACE:
            select_underwear()
        return
    else:
        try:
            chosenWeapon = weaponList[num]
        except IndexError:
            return
        else:
            universal.say(chosenWeapon.display())
            set_commands(['(Enter) Equip Weapon', '<==Back'])
            set_command_interpreter(confirm_weapon_interpreter)

def confirm_weapon_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        universal.state.player._set_weapon(copy.deepcopy(chosenWeapon))
        final_confirmation()
    elif keyEvent.key == K_BACKSPACE:
        select_weapon()

    

def simpleTitleCase(string):
    """
    A quick and dirty function for doing halfway decent title case.
    """
    stringList = str.split(string)
    newString = None
    for word in stringList:
        if word != 'of' and word != 'and' and word != 'the' and word != 'a' and word != 'an' and word != 'for':
            if newString == None:
                newString = [word.title()]
            else:
                newString.append(word.title())
        else:
            if newString == None:
                newString = [word]
            else:
                newString.append(word)
    if newString:
        return ' '.join(newString)
    else:
        return ''

requestDescriptionString = 'The following is your character\'s background. If you wish, you may add additional text. For example, you can give more details about your character\'s physical appearance. Note that this is purely aesthetic, and will not affect any in-game text. Also, you cannot change your character\'s background. To go back, hit Esc. When done, hit enter.\n\n'
def request_description():
    universal.say(requestDescriptionString)
    universal.say(universal.state.player.description)
    universal.say('_')
    universal.set_command_interpreter(request_description_interpreter)

partialDescription = ''
def request_description_interpreter(keyEvent):
    global partialDescription
    if keyEvent.key == K_RETURN:
        universal.state.player.description = ' '.join([universal.state.player.description, partialDescription])
        final_confirmation()
    elif keyEvent.key == K_ESCAPE:
        partialDescription = ''
        request_name()
    else:
        playerInput = pygame.key.name(keyEvent.key)
        if re.match(re.compile(r'^\w$'), playerInput):
            if pygame.key.get_pressed()[K_LSHIFT] or pygame.key.get_pressed()[K_RSHIFT]:
                partialDescription += str.capitalize(playerInput)
            else:
                partialDescription += playerInput
        elif keyEvent.key == K_PERIOD:
            partialDescription += '.'
        elif keyEvent.key == K_COMMA:
            partialDescription += ','
        elif keyEvent.key == K_LEFTPAREN:
            partialDescription += '('
        elif keyEvent.key == K_RIGHTPAREN:
            partialDescription += ')'
        elif keyEvent.key == K_SEMICOLON:
            partialDescription += ';'
        elif keyEvent.key == K_COLON:
            partialDescription += ':'
        elif keyEvent.key == K_BACKSPACE:
            partialDescription = partialDescription[:-1]
        universal.say(requestDescriptionString)
        if keyEvent.key == K_SPACE:
            partialDescription += ' '
        universal.say(' '.join([universal.state.player.description, partialDescription]))
        universal.say('_')
    

gender = person.MALE
def request_gender():
    universal.say('Please select a gender.') 
    universal.set_commands(['(M)ale', '', '(F)emale', '<==Back', '(Esc)Quit'])
    universal.set_command_interpreter(request_gender_interpreter)

def request_gender_interpreter(keyEvent):
    global gender
    if keyEvent.key == K_m:
        gender = person.MALE
        request_name()
    elif keyEvent.key == K_f:
        gender= person.FEMALE
        request_name()
    elif keyEvent.key == K_BACKSPACE:
        request_difficulty()
    elif keyEvent.key == K_ESCAPE:
        quit()


partialDescription = ''
"""
Stats:
    warfare
    magic
    resilience()
    grapple
    stealth
    health
    mana
    current health
    current mana
"""
statPoints = 3

def final_confirmation():
    print(universal.state.player.spellList)
    universal.state.player.learn_spell(person.allSpells[0][0][0])
    universal.state.player.learn_spell(person.allSpells[0][1][0])
    universal.state.player.learn_spell(person.allSpells[0][2][0])
    universal.state.player.learn_spell(person.allSpells[0][3][0])
    spells = [person.allSpells[0][0][0], person.allSpells[0][1][0], person.allSpells[0][2][0], person.allSpells[0][3][0]]
    for i in range(len(spells)):
        universal.state.player.quickSpells[i] = spells[i]
    universal.say(universal.state.player.appearance(True), justification=0)
    #print(universal.state.player.character_sheet_spells())
    universal.set_commands(['(Enter) Begin Game', '<==Back', '(Esc) To Title Screen'])
    universal.set_command_interpreter(final_confirmation_interpreter)

def final_confirmation_interpreter(keyEvent):
    #universal.state.player = person.get_PC()
    if keyEvent.key == K_RETURN:
        universal.state.player.currentEpisode = firstEpisode.name
        episode.allEpisodes[universal.state.player.currentEpisode].currentSceneIndex = 0
        #episode.set_post_title_card(townmode.save_game, ['.init', townmode.town_mode, False])
        episode.allEpisodes[universal.state.player.currentEpisode].start_episode(False)
        townmode.saveName = ''
    elif keyEvent.key == K_BACKSPACE:
        select_weapon()
    elif keyEvent.key == K_ESCAPE:
        global spellPoints
        global statPoints
        spellPoints = 3
        statPoints = 3
        #universal.state.player.clear_spells()
        #universal.state.player.reset_stats()
        title_screen(firstEpisode)
        universal.set_command_interpreter(title_screen_interpreter)
        universal.set_commands(['(S)tart', '(L)oad', '(Esc)Quit'])


        
def load_game():
    universal.say_title('Load Game')
    universal.get_screen().blit(universal.get_background(), universal.get_world_view().topleft)
    townmode.load(title_screen)
