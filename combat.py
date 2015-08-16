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
import items
import person
import positions
import music
import combatAction
from combatAction import ALLY, ENEMY
import pygame
import titleScreen
import copy
import random
import spanking
import statusEffects
import operator
import music
import copy
import townmode
import dungeonmode
import statusEffects
import math
import logging

"""
Note: The interpreters all assume that you will only ever face up to 9 enemies
at
once. If you want to face more than 9 enemies, you'll have to modify the
interpreters to
take multi-digit numbers as well (see the save_game interpreter for ideas on
how to do that).
"""


#message for indicating status is cleared: [character.name, 'is no longer affected by', status.name, '!']


TITLE_OFFSET = 15
allies = None
afterCombatEvent = None
worldView = None
enemies = None
bg = None
runnable = True
activeAlly = None
chosenActions = []
titleFont = pygame.font.SysFont(universal.FONT_LIST_TITLE, universal.TITLE_SIZE)
enemySurface = None
allySurface = None
commandSurface = None
clearScreen = None
previousMode = None
#Maps each character to a list of pairs. Each pair associates an action performed by that character with the effect (damage, a status successfully inflicted, a spanking
#inflicted/reversed, etc).
actionsInflicted = {}
ACTION = 0
EFFECT = 1
#maps each character to a list of pairs. Each pair associates an action performed on the character with the effect on that character (damage received, a status endured,
#a spanking received/reversed etc).
actionsEndured = {}
optional = False
ambush = 0
boss = False
initialAllies = None
initialEnemies = None
randomEncounter = False
coordinates = None
defeatedAllies = []
defeatedEnemies = []
interpreter = None

def is_catfight():
    return interpreter == catfight_interpreter

def end_fight():
    if randomEncounter:
        for enemy in enemies:
            universal.state.remove_character(enemy)
    global allies, enemies, actionsInflicted, actionsEndured, activeAlly, chosenActions, initialAllies, initialEnemies
    allies = None
    enemies = None
    initialAllies = []
    initialEnemies = []
    actionsInflicted = {}
    actionsEndured = {}
    activeAlly = None
    chosenActions = []

def catfight(enemy, after_combat_event_in, previous_mode_in):
    """
    Initiates a catfight between the player, and the passed in enemy.
    Catfights are basically brawls. No real damage is done, and weapons are
    not used. The player will also only have access to certain silly spells
    (not yet implemented)
    :param enemy: The person being fought
    :param after_combat_event_in: The callable event that will occur after
    battle. Usually a function that processes the result.
    :param previous_mode_in: The type of game mode (town or dungeon) that
    the game was in before battle began.
    """
    fight(enemy, after_combat_event_in, previous_mode_in, False, False, True,
          None, 0, False, None, True, [universal.state.player])

def fight(
        enemiesIn, 
        afterCombatEventIn=None,
        previousModeIn=dungeonmode.dungeon_mode, 
        runnableIn=True,
        bossFight=False, 
        optionalIn=False, 
        additionalAllies=None,
        ambushIn=0, 
        randomEncounterIn=False, 
        coordinatesIn=None,
        catfight=False, 
        party=None
):
    # Way too many global variables. This code really needs to be rewritten.
    global afterCombatEvent, activeAlly, worldView, enemies, bg, allies,\
        allySurface, enemySurface, commandSurface, clearScreen, previousMode,\
        actionsInflicted, actionsEndured, chosenActions, optional,\
        defeatedEnemies, defeatedAllies
    global ambush, boss, initialAllies, initialEnemies, randomEncounter, \
        coordinates, interpreter
    randomEncounter = randomEncounterIn
    interpreter = catfight_interpreter if catfight else battle_interpreter
    if randomEncounter:
        assert coordinatesIn
        coordinates = coordinatesIn
    universal.state.enemies = person.Party(enemiesIn)
    allies = party if party else list(universal.state.party)
    universal.state.allies = person.Party(list(allies) + (
        additionalAllies if additionalAllies else []))
    initialEnemies = []
    initialAllies = []
    for ally in universal.state.allies:
        initialAllies.append((ally.get_id(), list(ally.primaryStats),
            dict(ally.statusDict), list(ally.increaseSpellPoints),
            list(ally.increaseStatPoints)))
        ally.humiliationLevel = 0
        ally.staminaDamage = 0
    for enemy in universal.state.enemies:
        initialEnemies.append((enemy.get_id(), list(enemy.primaryStats),
            dict(enemy.statusDict)))
        enemy.humiliationLevel = 0
        enemy.staminaDamage = 0 
    boss = bossFight
    ambush = ambushIn
    enemies = universal.state.enemies
    allies = universal.state.allies
    for enemy in enemies:
        enemy.restores()
    defeatedAllies = []
    defeatedEnemies = []
    #All catfights are optional
    optional = optionalIn or catfight
    try:
        actionsInflicted = {combatant:[] for combatant in enemiesIn + person.get_party().members + (additionalAllies if additionalAllies is not None else [])}
    except TypeError:
        actionsInflicted = {combatant:[] for combatant in [enemiesIn] + person.get_party().members + (additionalAllies if additionalAllies is not None else [])}
    chosenActions = []
    previousMode = previousModeIn
    bg = get_background()
    afterCombatEvent = afterCombatEventIn
    if bossFight:
        music.play_music(music.BOSS)
        for ally in allies:
            orderResult = ally.order(ally, allies, enemies)
            if orderResult != '':
                say_delay(orderResult)
                for i in range(0, 5):
                    delaySplit = delay // 5
                    pygame.time.delay(delaySplit)
    else:
        music.play_music(music.COMBAT)
    #for ally in allies:
    #   ally.chanceIncrease = [0 for i in range(len(ally.chanceIncrease))]
    maxAllyLevel = max([sum(ally.get_battle_stats()) for ally in allies]) 
    maxEnemyLevel = max([sum(enemy.get_battle_stats()) for enemy in enemies])
    for enemy in enemies:
        if sum(enemy.get_battle_stats()) <= maxAllyLevel:
            orderResult = enemy.order(enemy, enemies, allies)
            if orderResult is not '':
                say_delay(orderResult)
                for i in range(0, 5):
                    delaySplit = delay // 5
                    pygame.time.delay(delaySplit)
    actionsEndured = {combatant:[] for combatant in allies + enemies}
    actionsInflicted = {combatant:[] for combatant in allies + enemies}
    if additionalAllies is not None:
        allies.extend(person.Party(additionalAllies))
    worldView  = get_world_view()
    enemySurface = pygame.Surface((worldView.width, worldView.height / 2.5))
    enemySurface.fill(DARK_GREY)
    allySurface = pygame.Surface((enemySurface.get_width(), 
        6 * (1.5 * worldView.height / 2.5) / 7))
    allySurface.fill(DARK_GREY)
    commandSurface = pygame.Surface((allySurface.get_width(), 
        (1.5 * worldView.height / 2.5) / 7))
    commandSurface.fill(DARK_GREY)
    clearScreen = pygame.Surface((worldView.width, worldView.height))
    clearScreen.fill(DARK_GREY)
    global runnable
    runnable = runnableIn and not catfight
    activeAlly = allies[0]
    if ambush < 0:
        say_delay('The party has been ambushed!')
        ambush = 0
        for i in range(0, 5):
            delaySplit = delay // 5
            pygame.time.delay(delaySplit)
        increment_stat_points()    
        choose_enemy_actions()
        start_round([])
    else:
        if ambush > 0:
            say_delay('The party has ambushed their enemies!')
            for i in range(0, 5):
                delaySplit = delay // 5
                pygame.time.delay(delaySplit)
        display_combat_status()

def end_combat():
    end_fight()
    previousMode()

def display_combat_status(targeted=None, printAllies=True, printEnemies=True):
    screen = get_screen()
    screen.blit(clearScreen, worldView)
    if printEnemies:
        print_enemies(enemies)
    else:
        screen.blit(enemySurface, worldView)
    if printAllies:
        print_allies(allies)
    else:
        screen.blit(allySurface, enemySurface.get_rect().bottomleft)
    if optional:
        print_command('Optional')
    #print_command(activeAlly.printedName)
    set_battle_commands()

def set_battle_commands():
    commandList = ['(#Enter)Attack', '(C)ast', '(F#) Quick Spell', '(D)efend', '(L)ook']
    if activeAlly.is_spanking():
        commandList = ['(Enter)Spank', '(S)top Spanking']
    elif activeAlly.is_being_spanked():
        commandList = ['(Enter)Struggle', '(E)ndure']
    elif activeAlly.is_grappling():
        commandList.remove('(L)ook')
        commandList.extend(['(S)pank', '(T)hrow', '(B)reak Grapple']) 
    else:
        commandList.append('(G)rapple')
        if runnable:
            commandList.append('(F)lee')
    commandList.append('<==Back')
    commandList.append('(Esc)To Title')
    set_commands(commandList)   
    set_command_interpreter(battle_interpreter)

def print_enemies(enemies, targetList=None, title='Enemies'):
    screen = get_screen()
    say_title(title, surface=enemySurface)
    flush_text(TITLE_OFFSET)
    pygame.draw.line(enemySurface, LIGHT_GREY, 
            (enemySurface.get_rect().topleft[0], enemySurface.get_rect().topleft[1] + 3), 
            (enemySurface.get_rect().topright[0], enemySurface.get_rect().topleft[1] + 3), 7)
    if isinstance(enemies, basestring):
        universal.say(enemies, surface=enemySurface, columnNum=1)
    else:
        activeEnemies = person.Party([enemy for enemy in enemies if enemy.current_health() > 0])
        universal.say(activeEnemies.display_party(False, targeted=targetList), surface=enemySurface, columnNum=3) 
    flush_text(TITLE_OFFSET)
    screen.blit(enemySurface, worldView)

def print_allies(allies, targetList=None, title='Party'):
    screen = get_screen()
    pygame.draw.line(allySurface, LIGHT_GREY, allySurface.get_rect().topleft, 
            allySurface.get_rect().topright, 10)
    say_title(title, surface=allySurface)
    flush_text(TITLE_OFFSET)
    if isinstance(allies, basestring):
        universal.say(allies, surface=allySurface, columnNum=1)
    else:
        if is_catfight():
            universal.say('\t'.join(['', 'Humiliation:', 'Stamina:', 'Grappling:\n\t']),
                    surface=allySurface, columnNum=4)
        else:
            universal.say('\t'.join(['', 'Health:', 'Mana:',  'Grappling:\n\t']), 
                    surface=allySurface, columnNum=4)
        if is_catfight():
            universal.say(allies.display_catfight(grappling=True), 
                    surface=allySurface, columnNum=4)
        else:
            universal.say(allies.display_party(ally=activeAlly, targeted=targetList, 
                grappling=True), surface=allySurface, columnNum=4)
    flush_text(TITLE_OFFSET)
    screen.blit(allySurface, enemySurface.get_rect().bottomleft)

def print_command(command):
    screen = get_screen()
    commandScreenCoord = (enemySurface.get_rect().bottomleft[0], 
            enemySurface.get_rect().bottomleft[1] + allySurface.get_height())
    commandSurface.fill(DARK_GREY)
    screen.blit(commandSurface, commandScreenCoord)
    fontSize = pygame.font.SysFont(FONT_LIST_TITLE, TITLE_SIZE).size(command)
    say_title(command, surface=commandSurface)
    flush_text(13)
    cmdMidTop = commandSurface.get_rect().midtop
    pygame.draw.rect(commandSurface, LIGHT_GREY, 
            pygame.Rect(cmdMidTop[0] - fontSize[0], cmdMidTop[1], fontSize[0] + fontSize[0], fontSize[1] + fontSize[1]), 10) 
    screen.blit(commandSurface, commandScreenCoord)


def catcast():
    raise NotImplementedError()


def catfight_interpreter(keyEvent):
    global chosenActions, activeAlly
    if keyEvent.key == K_BACKSPACE:
        if allies[0] != activeAlly:
            activeAlly = allies[allies.index(activeAlly)-1]
            del chosenActions[-1]
            display_combat_status(printEnemies=False, printAllies=False)
    elif activeAlly.is_spanking():
        if keyEvent.key == K_RETURN:    
            continue_spanking()
        elif keyEvent.key == K_s:
            terminate_spanking()
    elif activeAlly.is_being_spanked():
        if keyEvent.key == K_RETURN:
            struggle()
        elif keyEvent.key == K_e:
            endure()
    elif keyEvent.key == K_RETURN:
        attack(-1)
    elif keyEvent.key in universal.NUMBER_KEYS:
        number = int(universal.key_name(keyEvent)) - 1
        if number < len(enemies):
            attack(number)
    elif keyEvent.key == K_c:
        pass
        #catcast()
    elif keyEvent.key == K_d:
        defend()
    elif activeAlly.is_grappling():
        if keyEvent.key == K_s:
            spank()
        if keyEvent.key == K_t:
            strip()
        elif keyEvent.key == K_b:
            break_grapple()
    elif keyEvent.key == K_g:
        grapple()
    elif keyEvent.key == K_r:
        activeAlly = allies[0]
        chosenActions = []
        display_combat_status(printEnemies=False, printAllies=False)
    elif keyEvent.key == K_l:
        look()

def battle_interpreter(keyEvent):
    global chosenActions, activeAlly
    if keyEvent.key == K_ESCAPE:
        set_commands(['Are you sure you want to quit? (Y/N)'])
        set_command_interpreter(confirm_to_title_interpreter)
    elif keyEvent.key == K_BACKSPACE:
        if allies[0] != activeAlly:
            activeAlly = allies[allies.index(activeAlly)-1]
            del chosenActions[-1]
            display_combat_status(printEnemies=False, printAllies=False)
    elif activeAlly.is_spanking():
        if keyEvent.key == K_RETURN:    
            continue_spanking()
        elif keyEvent.key == K_s:
            terminate_spanking()
    elif activeAlly.is_being_spanked():
        if keyEvent.key == K_RETURN:
            struggle()
        elif keyEvent.key == K_e:
            endure()
    elif keyEvent.key == K_RETURN:
        attack(-1)
    elif keyEvent.key in universal.NUMBER_KEYS:
        number = int(universal.key_name(keyEvent)) - 1
        if number < len(enemies):
            attack(number)
    elif keyEvent.key == K_c:
        cast()
    elif keyEvent.key == K_d:
        defend()
    elif keyEvent.key == K_F1 and activeAlly.quickSpells[0] != None:
        cast(activeAlly.quickSpells[0])
    elif keyEvent.key == K_F2 and activeAlly.quickSpells[1] != None:
        cast(activeAlly.quickSpells[1])
    elif keyEvent.key == K_F3 and activeAlly.quickSpells[2] != None:
        cast(activeAlly.quickSpells[2])
    elif keyEvent.key == K_F4 and activeAlly.quickSpells[3] != None:
        cast(activeAlly.quickSpells[3])
    elif keyEvent.key == K_F5 and activeAlly.quickSpells[4] != None:
        cast(activeAlly.quickSpells[4])
    elif keyEvent.key == K_F6 and activeAlly.quickSpells[5] != None:
        cast(activeAlly.quickSpells[5])
    elif keyEvent.key == K_F7 and activeAlly.quickSpells[6] != None:
        cast(activeAlly.quickSpells[6])
    elif keyEvent.key == K_F8 and activeAlly.quickSpells[7] != None:
        cast(activeAlly.quickSpells[7])
    elif keyEvent.key == K_F9 and activeAlly.quickSpells[8] != None:
        cast(activeAlly.quickSpells[8])
    elif keyEvent.key == K_F10 and activeAlly.quickSpells[9] != None:
        cast(activeAlly.quickSpells[9])
    elif keyEvent.key == K_F11 and activeAlly.quickSpells[10] != None:
        cast(activeAlly.quickSpells[10])
    elif keyEvent.key == K_F12 and activeAlly.quickSpells[11] != None:
        cast(activeAlly.quickSpells[11])
    elif activeAlly.is_grappling():
        if keyEvent.key == K_s:
            spank()
        if keyEvent.key == K_t:
            throw()
        elif keyEvent.key == K_b:
            break_grapple()
    elif keyEvent.key == K_g:
        grapple()
    elif keyEvent.key == K_f and '(F)lee' in get_commands():
        run()
    elif keyEvent.key == K_r:
        activeAlly = allies[0]
        chosenActions = []
        display_combat_status(printEnemies=False, printAllies=False)
    elif keyEvent.key == K_l:
        look()


def not_enough_mana():
    set_commands(["Press Enter to continue"])
    set_command_interpreter(not_enough_mana_interpreter)

def not_enough_mana_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        display_combat_status()

def look():
    set_commands(['(#) Enemy to look at', '<==Back'])
    set_command_interpreter(look_interpreter)

def look_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        commandList = ['(A)ttack', '(C)ast', '(D)efend', '(L)ook']
        if activeAlly.is_grappling():
            #commandList.extend(['(S)pank', '(T)hrow', '(B)reak Grapple']) 
            commandList.extend(['(T)hrow', '(B)reak Grapple']) 
        else:
            commandList.append('(G)rapple')
            if runnable:
                commandList.append('(F)lee')
        commandList.append('(R)eset')
        commandList.append('<==Back')
        commandList.append('(Esc)To Title')
        set_commands(commandList)
        set_command_interpreter(battle_interpreter)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        num -= 1
        if 0 <= num  and num < len(enemies):
            chosenEnemy = [enemy for enemy in enemies if enemy.current_health() > 0][num]
            say_title(chosenEnemy.printedName)
            if isinstance(chosenEnemy.description, basestring):
                print_enemies(chosenEnemy.description)
            else:
                print_enemies('\n'.join(chosenEnemy.description))
            acknowledge(display_combat_status, ()) 


def next_character():
    global activeAlly, chosenTargets
    chosenTargets = []
    print_allies(allies, chosenTargets)
    print_enemies(enemies, chosenTargets)
    activeIndex = allies.index(activeAlly)
    if activeIndex < len(allies) - 1:
        activeAlly = allies[activeIndex+1]
    else:
        display_round_confirmation()

def display_round_confirmation():
    get_screen().blit(get_background(), (0, 0))
    say_title('Confirm Actions')
    for action in chosenActions:
        universal.say(action.confirmation_message() + '\n\n') 
    if universal.state.instant_combat:
        universal.say('Combat messages are printed all at once.')
    else:
        universal.say('There is a delay before printing each combat message.')
    set_commands(['(Enter) Begin Round', '(T)oggle combat delay', '<==Back'])
    set_command_interpreter(begin_round_interpreter)



PRIMARY_POINTS = 2
SECONDARY_POINTS = 1

def increment_stat_points():
    numStats = len(person.allStats)
    global chosenActions
    for action in chosenActions:
        increaseStat = action.attacker.increaseStatPoints
        increaseSpellPoints = action.attacker.increaseSpellPoints
        if action.attacker in allies:
            increaseStat[action.primaryStat] += PRIMARY_POINTS
            try:
                increaseSpellPoints[action.spellType] += action.spell_points()
            except AttributeError:
                continue
            try:
                increaseStat[action.secondaryStat] += SECONDARY_POINTS
            except (AttributeError, TypeError):
                continue
        elif action.attacker in enemies:
            for defender in action.defenders:
                defender.increaseStatPoints[action.primaryStat] += SECONDARY_POINTS
    for ally in allies:
        ally.increaseStatPoints[universal.ALERTNESS] += SECONDARY_POINTS

def begin_round_interpreter(keyEvent):
    global chosenActions, chosenTargets
    if keyEvent.key == K_RETURN:
        global ambush
        if ambush <= 0:
            choose_enemy_actions()
        else:
            ambush = 0
        increment_stat_points()
        start_round(chosenActions)
    elif keyEvent.key == K_t:
        universal.state.instant_combat = not universal.state.instant_combat
        display_round_confirmation()
    elif keyEvent.key == K_BACKSPACE:
        if DEBUG:
            chosenActions = []
        else:
            del chosenActions[-1]
        chosenTargets = []  
        display_combat_status()

def confirm_to_title_interpreter(keyEvent):
    if keyEvent.key == K_y:
        for ally in allies:
            ally.break_grapple()
        end_fight()
        titleScreen.title_screen()
        return
    elif keyEvent.key == K_n:
        display_combat_status(printAllies=False, printEnemies=False)

def combat_acknowledge_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        set_battle_commands()
        print_enemies(enemies)

def attack(target):
    if target < 0:
        target = enemies.index(activeAlly.grapplingPartner) if activeAlly.is_grappling() else 0
    activeAlly.previousTarget = target
    if activeAlly.is_grappling() and target == enemies.index(activeAlly.grapplingPartner):
        if is_catfight():
            chosenActions.append(combatAction.CatAttackACtion(activeAlly, 
                activeAlly.grapplingPartner))
        else:
            chosenActions.append(combatAction.AttackAction(activeAlly, activeAlly.grapplingPartner))
        next_character()
    elif not activeAlly.is_grappling():
        if 0 <= target and target < len(enemies) and enemies[target] in [enemy for enemy in enemies if enemy.current_health() > 0] and not enemies[target].is_grappling():
            if is_catfight():
                chosenActions.append(combatAction.CatAttackAction(activeAlly, enemies[target]))
            else:
                chosenActions.append(combatAction.AttackAction(activeAlly, enemies[target]))
            next_character()
        elif enemies[target].is_grappling():
            print_enemies("Cannot attack a grappled enemy. You might hit your ally!")
            set_commands(["(Enter) Acknowledge"])
            set_command_interpreter(combat_acknowledge_interpreter)

chosenImplement = spanking.hand

def continue_spanking():
    assert activeAlly.is_spanking(), "Active Ally: %s isn't spanking!" % activeAlly.name
    assert activeAlly.is_spanking(activeAlly.grapplingPartner), "Active Ally: %s isn't spanking %s!" % (activeAlly.name, activeAlly.grapplingPartner.name)
    spankee = activeAlly.spankee
    #If we're not grappling, then we must be administering a spectral spanking
    if activeAlly.is_grappling():
        severity = chosenImplement.severity
    else:
        severity = activeAlly.position.severity
    if is_catfight():
        chosenActions.append(combatAction.CatContinueSpankingAction(activeAlly, [spankee], severity))
    else:
        chosenActions.append(combatAction.ContinueSpankingAction(activeAlly, [spankee], severity))
    next_character()

def terminate_spanking():
    assert activeAlly.is_spanking(), "Active Ally: %s isn't spanking!" % activeAlly.name
    assert activeAlly.is_spanking(activeAlly.grapplingPartner), "Active Ally: %s isn't spanking %s!" % (activeAlly.name, activeAlly.grapplingPartner.name)
    activeAlly.spankee.spankingEnded = True
    activeAlly.terminate_spanking()
    display_combat_status()

def struggle():
    assert activeAlly.is_being_spanked(), "Active Ally: %s isn't being spanked!" % activeAlly.name
    assert activeAlly.is_being_spanked(activeAlly.grapplingPartner), "Active Ally: %s isn't being spanked by %s!" % (activeAlly.name, activeAlly.grapplingPartner.name)
    spanker = activeAlly.spanker
    if is_catfight():
        chosenActions.append(combatAction.StruggleAction(activeAlly, [spanker]))
    else:
        chosenActions.append(combatAction.CatStruggleAction(activeAlly, [spanker]))
    next_character()

def endure():
    assert activeAlly.is_being_spanked(), "Active Ally: %s isn't being spanked!" % activeAlly.name
    assert activeAlly.is_being_spanked(activeAlly.grapplingPartner), "Active Ally: %s isn't being spanked by %s!" % (activeAlly.name, activeAlly.grapplingPartner.name)
    spanker = activeAlly.spanker
    if is_catfight():
        chosenActions.append(combatAction.CatEndureAction(activeAlly, [spanker]))
    else:
        chosenActions.append(combatAction.EndureAction(activeAlly, [spanker]))
    next_character()

def cast(quickSpell=None):
    if quickSpell is not None:
        if (activeAlly.is_grappling() and quickSpell.grappleStatus == combatAction.NOT_WHEN_GRAPPLED) or (not activeAlly.is_grappling() and 
        (quickSpell.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY or quickSpell.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED)):
            return
        global chosenSpell
        chosenSpell = quickSpell
        target_spell()
    else:
        print_command('Tier')
        commandList = [str(i) for i in range(0, activeAlly.tier+1)]
        if len(commandList) < 9:
            commandList.append('<==Back')
        set_commands(commandList)
        set_command_interpreter(cast_interpreter)

def cast_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if 0 <= num and num <= activeAlly.tier and activeAlly.spellList[num] != None:
            select_spell(num)

chosenTier = None
possibleSpells = None
def select_spell(tier):
    global chosenTier
    chosenTier = tier
    """
    Note: This assumes that a character can learn at most 9 spells per tier (2 per type,
    plus a third for their specialization)
    """
    print_command('Spell')
    global possibleSpells
    possibleSpells = [spell for spell in activeAlly.spellList[chosenTier] if activeAlly.current_mana() >= spell.cost]
    if activeAlly.is_grappling():
        possibleSpells = [spell for spell in possibleSpells if spell.grappleStatus != combatAction.NOT_WHEN_GRAPPLED]
    else:
        possibleSpells = [spell for spell in possibleSpells if spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED and 
                spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY]
    commandList = numbered_list([spell.name for spell in possibleSpells if activeAlly.mana() >= spell.cost])
    if len(commandList) < 9:
        commandList.append('<==Back')
    set_commands(commandList)
    set_command_interpreter(select_spell_interpreter)

chosenSpell = None
def select_spell_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(possibleSpells):
            global chosenSpell
            chosenSpell = possibleSpells[num]
            target_spell()

def target_spell():
    #print_command(chosenSpell.name)
    target = 'enemy'
    targets = 'enemies'
    if activeAlly.current_mana() < chosenSpell.cost:
        print_allies(' '.join([activeAlly.name, "does not have enough mana to cast", chosenSpell.name]))
        not_enough_mana()
        return
    if chosenSpell.targetType == ALLY:
        target = 'ally'
        targets = 'allies'
    if chosenSpell.targetType == ENEMY:
        print_allies(chosenSpell.abbr_spell_stats(), title=chosenSpell.name)
    else:
        print_enemies(chosenSpell.abbr_spell_stats(), title=chosenSpell.name)
    if activeAlly.is_grappling() and (chosenSpell.grappleStatus == combatAction.GRAPPLER_ONLY or 
            chosenSpell.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY):
        set_commands(['(Enter) Cast Spell', '<==Back'])
        targetAllies = chosenSpell.targetType == ALLY
        targets = allies if targetAllies else enemies
        printTargets = print_allies if targetAllies else print_enemies
        printTargets(targets, [activeAlly if targetAllies else activeAlly.grapplingPartner])
        #flush_text(TITLE_OFFSET)
    else:
        spell_target_commands()
    set_command_interpreter(target_spell_interpreter)

def spell_target_commands():
    set_commands([' '.join(['(#)', 'Select', str(chosenSpell.numTargets), 
        'targets' if chosenSpell.numTargets > 1 else 'target']), '<==Back', 
        '(Enter) Cast Spell'])

chosenTargets = []

def combat_acknowledge_spell_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        spell_target_commands()
        set_command_interpreter(target_spell_interpreter)

def target_spell_interpreter(keyEvent):
    """
    This assumes that you never face more than 9 enemies, and you never have more than 9
    allies.
    """
    numTargetsChosen = len(chosenTargets)
    targetAllies = chosenSpell.targetType == ALLY
    targets = allies if targetAllies else enemies
    printTargets = print_allies if targetAllies else print_enemies
    targetStr = 'enemy'
    targetStrs = 'enemies'
    global chosenTier
    if targetAllies:
        targetStr = 'ally'
        targetStrs = 'allies'
    if activeAlly.is_grappling():
        if keyEvent.key == K_RETURN:
            if chosenSpell.targetType == ENEMY:
                chosenActions.append(chosenSpell.__class__(activeAlly, activeAlly.grapplingPartner))
            else:
                chosenActions.append(chosenSpell.__class__(activeAlly, activeAlly))
            chosenTier = None
            next_character()
        elif keyEvent.key == K_BACKSPACE:
            if chosenTier is not None:
                print_allies(allies)
                print_enemies(enemies)
                select_spell(chosenTier)
            else:
                display_combat_status(printAllies=True, printEnemies=True)

    else:
        if keyEvent.key == K_BACKSPACE:
            if numTargetsChosen == 0:
                if chosenTier:
                    select_spell(chosenTier)
                else:
                    display_combat_status(printAllies=True, printEnemies=True)
            else:
                chosenTargets.pop()
                printTargets(targets, chosenTargets)
        elif keyEvent.key in NUMBER_KEYS:
            num = int(pygame.key.name(keyEvent.key)) - 1
            if 0 <= num and num < len(targets) and not targets[num] in chosenTargets:
                if chosenSpell.actionType == person.Combat.actionType and targets[num].is_grappling():
                    print_enemies("You cannot target grappled enemies with a combat spell. You might hit your ally!")
                    set_commands(['(Enter) Acknowledge'])
                    set_command_interpreter(combat_acknowledge_spell_interpreter)
                chosenTargets.append(targets[num])
                numTargetsChosen += 1
                printTargets(targets, chosenTargets)
                if chosenSpell.numTargets - numTargetsChosen > 0 and len(enemies) - numTargetsChosen > 0:
                    set_commands([format_line(['(#) Select', str(chosenSpell.numTargets - numTargetsChosen),
                        targetStrs if chosenSpell.numTargets - numTargetsChosen > 1 else targetStr]), 
                        '<==Back', '(Enter)Cast spell'])
                else:
                    chosenActions.append(chosenSpell.__class__(activeAlly, chosenTargets))
                    next_character()
        elif keyEvent.key == K_RETURN and len(chosenTargets) > 0:
            chosenActions.append(chosenSpell.__class__(activeAlly, chosenTargets))
            next_character()

def defend():
    global chosenActions
    if activeAlly.is_grappling():
        chosenActions.append(combatAction.DefendAction(activeAlly, activeAlly))
        next_character()
    else:
        print_command('Defend')
        set_commands(['(#) Select ally', '<==Back'])
        set_command_interpreter(defend_interpreter)

def defend_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(allies) and not allies[num].is_grappling():
            chosenActions.append(combatAction.DefendAction(activeAlly, allies[num]))
            next_character()
        #Note: If the activeAlly is trying to defend himself and he's grappling, then he is automatically made the target of defend as a part of defend()
        elif allies[num].is_grappling():
            print_enemies(["Cannot defend a grappled ally!"])
            set_commands(["(Enter) Acknowledge"])
            set_command_interpreter(combat_acknowledge_interpreter)

possibleTargets = []
def break_grapple():
    global possibleTargets
    if activeAlly.is_grappling():
        chosenActions.append(combatAction.BreakGrappleAction(activeAlly, activeAlly.grapplingPartner))
        next_character()
    else:
        possibleTargets = filter(lambda x : x.is_grappling(), allies)
        if len(possibleTargets) == 0:
            display_combat_status(printAllies=False, printEnemies=False)
        else:
            print_command('Break Grapple')
            set_commands(['(#) Select 1 ally.', '<==Back'])         
            set_command_interpreter(break_grapple_interpreter)

def break_grapple_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(allies) and allies[num].is_grappling():
            chosenActions.append(combatAction.BreakAllysGrappleAction(activeAlly, allies[num])) 
            next_character()

def grapple():
    print_command('Grapple')
    set_commands(['(#) Select 1 enemy.', '<==Back'])
    set_command_interpreter(grapple_interpreter)

def grapple_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(enemies):
            if enemies[num].is_grappling():
                chosenActions.append(combatAction.BreakAllysGrappleAction(activeAlly, enemies[num].grapplingPartner))
            else:
                chosenActions.append(combatAction.GrappleAction(activeAlly, enemies[num]))
        next_character()
def run():
    chosenActions.append(combatAction.RunAction(activeAlly, None))
    next_character()
def spank():
    if activeAlly.grapplingPartner.is_inflicted_with(statusEffects.Humiliated.name):
        print_enemies("Cannot spank an already humiliated enemy.")
        set_commands(["(Enter) Acknowledge"])
        set_command_interpreter(combat_acknowledge_interpreter)
    else:
        positions = activeAlly.grapplingPartner.positions
        print_command('Select Position')
        set_commands([''.join([str(num+1), '. ', pos.name]) for num, pos in enumerate(positions)])
        universal.set_command_interpreter(spank_interpreter)

chosenPos = None
def spank_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(activeAlly.grapplingPartner.positions):
            global chosenPos
            chosenPos = activeAlly.grapplingPartner.positions[num]
            print_allies(chosenPos.display(), title=chosenPos.name)
            set_commands(['(Enter) Use Position', '<==Back'])
            set_command_interpreter(confirm_spanking_interpreter)

def confirm_spanking_interpreter(keyEvent):
    if keyEvent.key == K_RETURN: 
        if is_catfight():
            chosenActions.append(combatAction.CatSpankAction(activeAlly, 
                activeAlly.grapplingPartner, chosenPos))
        else:
            chosenActions.append(combatAction.SpankAction(activeAlly, activeAlly.grapplingPartner, 
                chosenPos))
        next_character()
    elif keyEvent.key == K_BACKSPACE:
        print_allies(allies)
        spank()

def strip_command(clothing, numCommand):
    return ''.join([str(numCommand), '. ', 'Strip ', clothing.name()])

def strip():
    assert is_catfight()
    print_command('Strip')
    stripCommands = []
    grapplingPartner = activeAlly.grapplingPartner
    if grapplingPartner.wearing_lower_clothing():
        stripCommands.append(strip_command(grapplingPartner.lower_clothing(), len(stripCommands)+1))
    elif grapplingPartner.wearing_underwear():
        stripCommands.append(strip_command(grapplingPartner.underwear(), len(stripCommands)+1))
    #We need to make sure we don't add a command to strip the same garment twice if the 
    #character is wearing a dress or similar full-body outfit.
    if grapplingPartner.wearing_shirt() and not (grapplingPartner.shirt() is 
            grapplingPartner.lower_clothing()):
        stripCommands.append(strip_command(grapplingPartner.shirt(), len(stripCommands)+1))

    set_command_interpreter(strip_interpreter)

def num_strip_commands(grapplingPartner):
    numCommands = 0
    if grapplingPartner.wearing_lower_clothing() or grapplingPartner.wearing_underwear():
        numCommands += 1
    if grapplingPartner.wearing_shirt() and not (grapplingPartner.shirt is 
            grapplingPartner.lower_clothing()):
        numCommands += 1
    return numCommands

def clothing_to_strip(grapplingPartner):
    clothing = []
    if grapplingPartner.wearing_lower_clothing():
        clothing.append(grapplingPartner.lower_clothing())
    elif grapplingPartner.wearing_underwear():
        clothing.append(grapplingPartner.underwear())
    if grapplingPartner.wearing_shirt():
        clothing.append(grapplingPartner.shirt())
    return clothing


def strip_interpreter(keyEvent):
    validCommands = num_strip_commands(activeAlly.grapplingParnter)
    clothing = clothing_to_strip(activeAlly.grapplingPartner)
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    try:
        selectedNum = int(keyEvent.key.name) - 1
    except AttributeError:
        return
    try:
        selectedClothing = clothing[selectedNum]
    except IndexError:
        return
    else:
        chosenActions.append(combatAction.StripAction(activeAlly, [activeAlly.grapplingPartner], 
            selectedClothing))
        next_character()

def throw():
    print_command('Throw')
    set_commands([' '.join(['(#) Select target.']), '<==Back'])
    set_command_interpreter(throw_interpreter)

def throw_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(enemies) and (not enemies[num].is_grappling() or enemies[num].is_grappling(activeAlly)):
            chosenActions.append(combatAction.ThrowAction(activeAlly, [activeAlly.grapplingPartner, enemies[num]]))
            next_character()
        elif enemies[num].is_grappling() and not enemies[num].is_grappling(activeAlly):
            print_enemies("Cannot throw your opponent at another grappled opponent. You might hit your ally!")
            set_commands(["(Enter) Acknowledge"])
            set_command_interpreter(combat_acknowledge_interpreter)

def choose_enemy_actions():
    for enemy in enemies:
        chosenActions.append(select_action(enemy))

def select_action(enemy):
    #if enemy.spankingEnded:
    #    enemy.spankingEnded = False
    #    return combatAction.DefendAction(enemy, [enemy])
    allActions = [combatAction.CatAttackAction] if is_catfight() else [combatAction.AttackAction]
    if enemy.is_spanking():
        #Note: This is a weakness in the AI. An enemy is forced to always administer a spanking, regardless of what's going on. This can make for an easy way of delaying an enemy: Just endure
        #their spanking while your allies take care of the others. However, it may be a wash, simply because this also neutralizes your character, and usually you'll be outnumbered.
        #If the enemy does not have a grappling partner, then she is spanking someone with a spectral spell, which is stored in the position.
        spankee = enemy.grapplingPartner if enemy.grapplingPartner else enemy.position.defenders[0]
        if is_catfight():
            return combatAction.CatContinueSpankingAction(enemy, [spankee], enemy.position)
        else:
            return combatAction.ContinueSpankingAction(enemy, [spankee], enemy.position)
    elif get_difficulty == HAND and enemy.is_being_spanked():
        spanker = enemy.grapplingPartner if enemy.grapplingPartner else enemy.position.attacker
        if random.randrange(2):
            #If the enemy does not have a grappling partner, then she is being spanked by a spectral spell.
            return combatAction.CatEndureAction if is_catfight() else combatAction.EndureAction(
                    enemy, [spanker])
        else:
            return combatAction.CatStruggleAction if is_catfight() else combatAction.StruggleAction(
                    enemy, [spanker])
    elif enemy.is_being_spanked():
        spanker = enemy.grapplingPartner if enemy.grapplingPartner else enemy.position.attacker
        if get_difficulty() == CANE and enemy.grappleDuration == 1:
            return combatAction.CatEndureAction if is_catfight() else combatAction.EndureAction(
                    enemy, [spanker])
        elif get_difficulty() == CANE and enemy.grappleDuration <= enemy.grapple() // combatAction.GRAPPLE_DIVISOR:
            return combatAction.CatStruggleAction if is_catfight() else combatAction.StruggleAction(
                    enemy, [spanker])
        else:
            bestStat = enemy.highest_stat()
            if is_catfight():
                allActions = [combatAction.CatStruggleAction] * (enemy.grapple() + 1) + [
                        combatAction.CatEndureAction] * (bestStat + 1)
            else:
                allActions = [combatAction.StruggleAction] * (enemy.grapple() + 1) +  [
                        combatAction.EndureAction] * (bestStat + 1)
            return allActions[random.randrange(len(allActions))](enemy, [spanker])
    elif enemy.is_grappling():
        if is_catfight():
            allActions.append(combatAction.CatSpankAction)
        elif not enemy.grapplingPartner.is_inflicted_with(statusEffects.Humiliated.name) and universal.state.enemiesCanSpank:
            allActions.append(combatAction.SpankAction)
        if not is_catfight() and enemy.grapple() // 2 <= enemy.grappleDuration:
            allActions.append(combatAction.ThrowAction)
        allActions.append(combatAction.BreakGrappleAction)
        #Currently I don't have any catfight-specific spells implemented.
        if not is_catfight():
            allActions.extend([spell.__class__ for spell in enemy.flattened_spell_list() if spell.grappleStatus != combatAction.NOT_WHEN_GRAPPLED and 
                spell.cost <= enemy.current_mana()])
    else:
        allActions.append(combatAction.GrappleAction)
        if filter(lambda x : x.is_grappling(), enemies) != []:
            allActions.append(combatAction.BreakAllysGrappleAction)
        if not is_catfight():
            allActions.extend([spell.__class__ for spell in enemy.flattened_spell_list() if 
                all([spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY,
                spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED, spell.cost <= 
                enemy.current_mana()])])
    if get_difficulty() == HAND:
        return hand_ai(enemy, allActions)
    elif get_difficulty() == STRAP or get_difficulty() == CANE:
        return strap_cane_ai(enemy)

def hand_ai(enemy, allActions):
    action = allActions[random.randrange(0, len(allActions))]
    defenders = []
    if enemy.is_grappling() and (action.grappleStatus == combatAction.GRAPPLER_ONLY or 
            action.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY):
        defenders = [enemy.grapplingPartner]
    else:
        targetList = list(allies if action.targetType == combatAction.ENEMY else enemies)
        if action.actionType == combatAction.AttackAction.actionType or action.actionType == person.Combat.actionType:
            targetList = [target for target in targetList if not target.is_grappling()]
            if not targetList:
                return hand_ai(enemy, [validAction for validAction in allActions if validAction != action])
        for i in range(0, action.numTargets):
            chosenAlly = targetList.pop(random.randrange(0, len(targetList)))
            defenders.append(chosenAlly)
            if targetList == [] and action == combatAction.ThrowAction:
                defenders.append(defenders[0])
                break
    if action == combatAction.SpankAction:
        assert universal.state.enemiesCanSpank
        action = action(enemy, defenders, enemy.positions[random.randrange(0, len(enemy.positions))])
    else:
        action = action(enemy, defenders)
    return action   

def choose_action_class(enemy, weightedActionClasses, warfareActions, grappleActions, magicActions, companions, availableSpells):
    chosenActionClass = []
    while chosenActionClass == []:
        chosenActionClass = weightedActionClasses[random.randrange(0, len(weightedActionClasses))]
        if chosenActionClass == warfareActions:
            if enemy.is_grappling():
                warfareActions.extend([combatAction.BreakGrappleAction for i in range(max(0, (enemy.warfare() - enemy.grapple())))]) 
                warfareActions.extend([combatAction.AttackAction for i in range(max(0, (enemy.warfare() - enemy.grapple())))]) 
            else:
                warfareActions.extend([combatAction.AttackAction for i in range(max(0, enemy.warfare()))])
        elif chosenActionClass == grappleActions:
            if enemy.is_grappling():
                if not enemy.grapplingPartner.is_inflicted_with(statusEffects.Humiliated.name) and universal.state.enemiesCanSpank:
                    grappleActions.extend([combatAction.SpankAction for i in range(max(1, enemy.grapple()))])
                grappleActions.extend([combatAction.AttackAction for i in range(max(1, enemy.warfare()))])
                if enemy.grapple() <= enemy.grappleDuration // 2:
                    grappleActions.extend([combatAction.ThrowAction for i in range(max(1, enemy.grapple()))])
                else:
                    try:
                        grappleActions.remove(combatAction.ThrowAction)
                    except ValueError:
                        pass
            else:
                grappleActions.extend([combatAction.GrappleAction for i in range(max(1, enemy.grapple()))])
                grappledCompanions = [e for e in companions if e.is_grappling()]
                for companion in grappledCompanions:
                    #The idea here that if this character has a much higher grapple than his ally, then not only is this character good for breaking a grapple, but 
                    #it's likely that his ally has a low grapple, in which case the ally needs all the help he can get.
                    grappleActions.extend([combatAction.BreakAllysGrappleAction for i in range(max(0, enemy.grapple() - companion.grapple()))])
        elif chosenActionClass == magicActions:
            possibleSpells = list(magicActions)
            for spell in possibleSpells:
                try:
                    spell.statusInflicted
                except AttributeError:
                    pass
                else:
                    possibleTargets = [ally for ally in allies if not ally.is_inflicted_with(statusEffects.get_name(spell.statusInflicted))]
                    if possibleTargets == []: #and spell in magicActions:
                        try:
                            magicActions.remove(spell)
                        except ValueError:
                            pass
                    else:
                        magicActions.extend([spell for i in range(spell.tier)])
            if chosenActionClass != []:
                chosenActionClass = weight_healing(magicActions, companions)
            if chosenActionClass != []:
                chosenActionClass = weight_status_buff(enemy, chosenActionClass)
    #We want to guarantee that the magicActions contain only spells when weighting them for the cane difficulty.
    chosenActionClass.extend([combatAction.DefendAction for statName in enemy.status_names() if statusEffects.is_negative(enemy.get_status(statName))])
    return chosenActionClass

def strap_cane_ai(enemy):
    """
    If we're using the strap difficulty, then targeting is random, and action choice depends only 
    on what a character is good at.
    """
    #This allows us to use this ai for any computer controlled allies of the player as well.
    companions = enemies if enemy in enemies else allies
    opponents = allies if enemy in enemies else enemies
    availableSpells = []
    if is_catfight():
        warfareActions = [combatAction.CatAttackAction]
    else:
        warfareActions = [combatAction.AttackAction]
    #If our enemy is not grappling and he/she is wielding a dagger, then he/she wants to try to grapple as soon as possible, because a dagger is basically useless when
    #not grappling.
    if enemy.is_grappling():
        if is_catfight():
            grappleActions = [combatAction.CatAttackAction, combatAction.StripAction,
                    combatAction.CatSpankAction]
        elif get_difficulty() == STRAP or (get_difficulty() == CANE and 
                enemy.weapon().weaponType == items.Sword.weaponType):
            warfareActions.append(combatAction.BreakGrappleAction)
            #If half an enemy's grapple is less than the amount of grapple left, then she can't throw her enemy, so she doesn't even bother.
            if enemy.grapple() // 2 < enemy.grappleDuration:
                grappleActions = [combatAction.AttackAction]
            else:
                grappleActions = [combatAction.ThrowAction, combatAction.AttackAction]
                if universal.state.enemiesCanSpank:
                    grappleActions.append(combatAction.SpankAction)
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Knife.weaponType:
            grappleActions = [combatAction.ThrowAction, combatAction.AttackAction]
        #If the character is using a spear, then they are at a serious disadvantage when grappling, 
        #and they need to break out of it ASAP.
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Spear.weaponType: 
            warfareActions = [combatAction.BreakGrappleAction]
            grappleActions = [combatAction.BreakGrappleAction]
        if not is_catfight():
            availableSpells = [spell for spell in enemy.flattened_spell_list() if 
                    all([spell.grappleStatus != combatAction.NOT_WHEN_GRAPPLED, 
                        enemy.current_mana() >= spell.cost])]
    else:
        if is_catfight():
            warfareActions = [combatAction.CatAttackAction]
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Knife.weaponType:
            warfareActions = []
        if is_catfight():
            grappleActions = [combatAction.GrappleAction]
        elif get_difficulty() == STRAP or (get_difficulty() == CANE and (
            enemy.weapon().weaponType == items.Sword.weaponType or 
            enemy.weapon().weaponType == items.Knife.weaponType)):
            grappleActions = [combatAction.GrappleAction]
        #If your enemy is wielding a spear, the last thing they want is to try to grapple you.
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Spear.weaponType: 
            grappleActions = []
        if [comp for comp in companions if comp.is_grappling() and comp != enemy] != []:
            grappleActions.append(combatAction.BreakAllysGrappleAction)
        if not is_catfight():
            availableSpells = [spell for spell in enemy.flattened_spell_list() if 
                    all([spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED,
                    spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY,
                    enemy.current_mana() >= spell.cost])]
    magicActions = list(availableSpells)

    #We have one reference to each action type for every value in a character's stat + 1 so that every class appears.
    weightedActionClasses = [warfareActions for i in range(max(1, enemy.warfare()))] + [grappleActions for i in range(max(1, enemy.grapple()))]
    if magicActions != []:
        weightedActionClasses += [magicActions for i in range(max(1, enemy.magic()))]
    if get_difficulty() == CANE:
        #For now, this does nothing. Not sure if we want to do anything to perform additional weighting on the classes for cane difficulty.
        weightedActionClasses = weight_classes_cane(weightedActionClasses)
    #If an action class doesn't have anything, we certainly don't want to use it!
    weightedActionClasses = [actionClass for actionClass in weightedActionClasses if actionClass]
    if get_difficulty() == CANE:
        return cane_ai(enemy, weightedActionClasses, warfareActions, grappleActions, magicActions, 
                companions, availableSpells)
    elif get_difficulty() == STRAP:
        return strap_ai(enemy, weightedActionClasses, warfareActions, grappleActions, magicActions, 
                companions, opponents, availableSpells)

def cane_ai(enemy, weightedActionClasses, warfareActions, grappleActions, magicActions, companions, availableSpells):
    chosenActionClass = choose_action_class(enemy, weightedActionClasses, warfareActions, grappleActions, magicActions, companions, availableSpells)
    originalChosenActionClass = list(chosenActionClass)
    assert originalChosenActionClass
    defenders = []
    while defenders == []:
        try:
            chosenAction = chosenActionClass.pop(random.randrange(len(chosenActionClass)))
        except ValueError:
                weightedActionClasses = [actionClass for actionClass in weightedActionClasses if 
                        actionClass != originalChosenActionClass]
                chosenActionClass = weightedActionClasses.pop(random.randrange(len(
                    weightedActionClasses)))
        assert chosenAction, "Chosen Action is None! ChosenAction class: %s" % str(
                chosenActionClass)
        defenders = select_targets(chosenAction, enemy)
    if chosenAction.actionType == combatAction.SpankAction.actionType:
        assert is_catfight() or universal.state.enemiesCanSpank
        return chosenAction(enemy, defenders, random.choice(list(positions.allPositions.values())))
    try:
        return chosenAction(enemy, defenders)
    except TypeError:
        chosenAction = copy.deepcopy(chosenAction)
        chosenAction.attacker = enemy
        chosenAction.defenders = defenders
        return chosenAction

def strap_ai(enemy, weightedActionClasses, warfareActions, grappleActions, magicActions, 
        companions, opponents, availableSpells):
    defenders = []
    activeCompanions = [comp for comp in companions if comp.current_health() > 0]
    activeOpponents = [opp for opp in opponents if opp.current_health() > 0]
    chosenActionClass = choose_action_class(enemy, weightedActionClasses, warfareActions, 
            grappleActions, magicActions, companions, availableSpells)
    originalChosenActionClass = list(chosenActionClass)
    chosenAction = chosenActionClass.pop(random.randrange(0, len(chosenActionClass)))
    if chosenAction == combatAction.ThrowAction:
        defenders.append(enemy.grapplingPartner)
        activeOpponents = [opp for opp in activeOpponents if opp != enemy.grapplingPartner and 
                not opp.is_grappling()]
        if activeOpponents == []:
            defenders.append(enemy.grapplingPartner)
        else:
            defenders.append(activeOpponents[random.randrange(0, len(activeOpponents))])
    elif chosenAction == combatAction.DefendAction:
        if enemy.is_grappling():
            defenders = [enemy]
        else:
            activeCompanions.append(enemy)
            defendTargets = [comp for comp in activeCompanions if not comp.is_grappling()]
            for companion in activeCompanions:
                defendTargets.extend([companion for statName in companion.status_names() if 
                    statusEffects.is_negative(companion.get_status(statName))])
                #We want to defend the magic users above all else.
                defendTargets.extend([companion for i in range(max(0, companion.magic()) // 3)])
                defendTargets.extend([companion for i in range(companion.health() - 
                    companion.current_health()) if companion.current_health() <= 
                    avg_damage(opponents)])
            if len(defendTargets) > 0:
                defenders.append(defendTargets[random.randrange(0, len(defendTargets))])    
            else:
                defenders.append(enemy)
    else:
        if chosenAction.actionType == combatAction.AttackAction.actionType or (
                chosenAction.actionType == person.Combat.actionType):
            activeOpponents = [opp for opp in activeOpponents if not opp.is_grappling()] 
            if not activeOpponents:
               return strap_ai(enemy, [actionClass for actionClass in weightedActionClasses if 
                   actionClass != originalChosenActionClass], warfareActions, grappleActions, 
                   magicActions, companions, opponents, availableSpells)
        #The code above for weighting the spells, and spankings, guarantees that this list will not be empty, assuming that the only actions that inflict statuses 
        #are spells, spankings, and defend.
        if hasattr(chosenAction, 'statusInflicted'):
            activeOpponents = [opp for opp in activeOpponents if not opp.is_inflicted_with(statusEffects.get_name(chosenAction.statusInflicted))] 
        assert(activeOpponents != [])
        for i in range(chosenAction.numTargets):
            defenders.append(activeOpponents.pop(random.randrange(0, len(activeOpponents))))
            if activeOpponents == []:
                break
    if chosenAction.actionType == combatAction.SpankAction.actionType:
        assert is_catfight() or universal.state.enemiesCanSpank
        return chosenAction(enemy, defenders, positions.allPositions.values()[random.randrange(0, len(positions.allPositions))])
    try:
        return chosenAction(enemy, defenders)
    except TypeError:
        chosenAction = copy.deepcopy(chosenAction)
        chosenAction.attacker = enemy
        chosenAction.defenders = defenders
        return chosenAction

def weight_classes_cane(actionClasses):
    """
    For now this function does nothing. However, in the future, a method of using the previous round results to weight the classes themselves may occur to me. Not so sure,
    though.
    """
    return actionClasses

def weight_status_buff(enemy, chosenActionClass):
    """
    The only additional weighting that this performs is on the action classes is on buff, and status magic. Each buff spell gets an additional weight for every character in
    who does not already have that buff, and based on the number of times a particular action that that buff protects again has appeared in the past. Meanwhile, status
    magic is also weighted by the number of possible targets who don't have the status, not including those who are immune. It also weights the status attacks based on
    the previous attacks of the opponents. So a spell like weaken is more likely to be cast if there are a lot of attacks and grapples, etc.

    Note: May also want to weight combat spells based on their average damage. We'll have to see.

    Note: The status magic weighting is only performed with difficulty of cane, since it requires looking at past history, which only happens in the cane difficulty.
    """
    companions = enemies if enemy in enemies else allies
    opponents = allies if enemy in enemies else enemies
    if isinstance(chosenActionClass[0], person.Spell):
        attackGrappleBuff = [action for action in chosenActionClass if isinstance(action, person.Buff) and not isinstance(action, person.Healing) and 
                action.targetType == combatAction.WARRIORS_GRAPPLERS]
        spellBuff = [action for action in chosenActionClass if isinstance(action, person.Buff) and not isinstance(action, person.Healing) and 
                action.targetType == combatAction.SPELL_SLINGERS]
        allBuff = [action for action in chosenActionClass if isinstance(action, person.Buff) and not isinstance(action, person.Healing) and 
                action.targetType == combatAction.ALL]
        attackGrappleComps = [comp for comp in companions if comp.is_specialized_in(WARFARE) or comp.is_specialized_in(GRAPPLE) or
            comp.is_specialized_in(BALANCED)]
        spellComps = [comp for comp in companions if comp.is_specialized_in_magic()]
        chosenActionClass.extend([buff for buff in attackGrappleBuff for comp in attackGrappleComps if not comp.is_inflicted_with(buff.statusInflicted)])
        chosenActionClass.extend([buff for buff in spellBuff for comp in spellComps if not comp.is_inflicted_with(buff.statusInflicted)])
        #Here we're counting the balanced characters twice, but whatever. Buff magic that affects everyone is still really good, so it's a good thing to cast.
        chosenActionClass.extend([buff for buff in allBuff for comp in attackGrappleComps + spellComps if not comp.is_inflicted_with(buff.statusInflicted)])
        if get_difficulty() == CANE:
            attackGrappleStatus = [action for action in chosenActionClass if hasattr(action, 'statusInflicted') and action.targetType == combatAction.WARRIORS_GRAPPLERS]
            spellStatus = [action for action in chosenActionClass if hasattr(action, 'statusInflicted') and action.targetType == combatAction.SPELL_SLINGERS]
            allStatus = [action for action in chosenActionClass if hasattr(action, 'statusInflicted') and action.targetType == combatAction.ALL]
            attackActions = []
            spellActions = []
            for attacker in (att for att in actionsInflicted.keys() if att in opponents):
                attackActions.extend([actionPair for actionPair in actionsInflicted[attacker] if (isinstance(actionPair[ACTION], combatAction.AttackAction) or 
                    isinstance(actionPair[ACTION], combatAction.GrappleAction) or isinstance(actionPair[ACTION], combatAction.ThrowAction) or
                    isinstance(actionPair[ACTION], combatAction.BreakAllysGrappleAction))])
                spellActions.extend([actionPair for actionPair in actionsInflicted[attacker] if isinstance(actionPair[ACTION], person.Spell)]) 

            chosenActionClass.extend([status for status in attackGrappleStatus for actionPair in attackActions])
            chosenActionClass.extend([status for status in spellBuff for actionPair in spellActions])
            chosenActionClass.extend([status for status in allStatus for actionPair in attackActions + spellActions])
    return chosenActionClass

def chosenActions_have_target_action(chosenAction, target):
    try:
        aType = chosenAction.actionType
    except AttributeError:
        return False
    for action in [a for a in chosenActions if hasattr(a, 'actionType') and a.actionType == aType]: 
        if target in action.defenders:
            return True
    return False

    
def select_targets(chosenAction, enemy):
    opponents = allies if enemy in enemies else enemies
    companions = enemies if enemy in enemies else allies
    targets = opponents if chosenAction.targetType == combatAction.ENEMY else companions
    if is_catfight():
        targets = [target for target in targets if target.current_humiliation() < 
                target.humiliation()]
    else:
        targets = [target for target in targets if target.current_health() > 0]
    try:
        if chosenAction.combatType == combatAction.GrappleAction.actionType or chosenAction.combatType == combatAction.BreakAllysGrappleAction.actionType:
            targets = [t for t in targets if not chosenActions_have_target_action(chosenAction, t)]
    except AttributeError:
        pass
    if not targets:
        return targets
    isCombat = any([chosenAction.actionType == person.Combat.actionType, 
        chosenAction.actionType == combatAction.AttackAction.actionType,
        chosenAction.actionType == combatAction.ThrowAction])
    isStatus = chosenAction.actionType == person.Status.actionType
    isHealing = chosenAction.actionType == person.Buff.actionType
    isBuff = chosenAction.actionType == person.Buff.actionType
    isSpectral = chosenAction.actionType == person.Spectral.actionType
    targetsEndured = {key:actionPair for (key, actionPair) in actionsEndured.iteritems() if key in targets}
    if enemy.is_grappling() and (chosenAction.targetType == combatAction.GRAPPLER_ONLY or chosenAction.targetType == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY):
        return [enemy.grapplingPartner] if chosenAction.targetType == combatAction.ENEMY else [enemy]
    if chosenAction.actionType == combatAction.DefendAction.actionType:
        targets.append(enemy)
        defendTargets = [comp for comp in targets if not comp.is_grappling()]
        defendTargets.extend([enemy for statName in enemy.status_names() if statusEffects.is_negative(enemy.get_status(statName))])
        for companion in companions:
            #We want to defend the magic users above all else.
            defendTargets.extend([companion for i in range(max(0, companion.magic()) // 3)])
            defendTargets.extend([companion for i in range(companion.health() - companion.current_health()) if companion.current_health() <= max_damage(companions)])
        defenders = []
        if len(defendTargets) > 0:
            defenders.append(defendTargets[random.randrange(0, len(defendTargets))])    
        else:
            defenders.append(enemy)
        return defenders
    elif chosenAction.actionType == combatAction.SpankAction.actionType:
        assert is_catfight() or universal.state.enemiesCanSpank
        return [enemy.grapplingPartner]
    elif chosenAction.actionType == combatAction.GrappleAction.actionType:
        targets = [target for target in targets if not target.is_grappling()]
        for target in targets:
            try:
                maxGrappleDuration = max([effect[0] for (action, effect) in actionsEndured[target] if action == combatAction.GrappleAction])
            except ValueError:
                maxGrappleDuration = 0
            targets.extend([target for i in range(maxGrappleDuration)])
    elif chosenAction.actionType == combatAction.BreakGrappleAction.actionType:
        return [enemy.grapplingPartner]
    elif chosenAction.actionType == combatAction.StripAction.actionType:
        assert is_catfight()
        return [enemy.grapplingPartner]
    elif chosenAction.actionType == combatAction.BreakAllysGrappleAction.actionType:
        targets = [target for target in targets if target.is_grappling() and target.grapple() < enemy.grapple()]
        for target in list(targets):
            #Note we're only looking at grappled targets with a lower grapple. Therefore, if there's a high grapple duration, the target is at a disadvantage and needs to be freed.
            targets.extend([target for i in range(target.grappleDuration)])
    elif isCombat:
        if not enemy.is_grappling():
            targets = [target for target in targets if not target.is_grappling()]
            if not targets:
                return targets
        avgdam = avg_damage(targets, chosenAction)
        #we'll be modifying the original targets list
        for target in list(targets):
            avgDamEndured = avg_damage_endured(target, chosenAction)
            #Here, we want to focus our attacks on enemies that take more damage from attacks, i.e. enemies with an average damage endured higher than the average for
            #this particular attack
            targets.extend([target for i in range(max(1, avgDamEndured - avgdam))])
    elif isStatus:
        targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted)]
        for target in list(targets):
            statusEndured = [action[1] for action in actionsEndured[target] if isinstance(action[0], type(chosenAction))]
            numSuccesses = 0
            for status in statusEndured:
                #Status is either a boolean, or a tuple containing the damage done, and a boolean indicating that the attack successfully inflicted the status
                if type(status) == type(True) and status:
                    numSuccesses += 1
                elif type(status) == type(()) and status[1]:
                    numSuccesses += 1
            targets.extend([target for i in range(numSuccesses)])
    elif isHealing:
        targets = [target for target in targets if target.current_health() <= max_damage(opponents) and target.health() > target.current_health()]
        for target in list(targets):
            targets.extend([target for i in range(target.health() - target.current_health())])
    elif isBuff:
        if chosenAction.effectClass == combatAction.WARRIORS_GRAPPLERS:
            targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted) and (target.is_specialized_in(universal.WARFARE) or 
                target.is_specialized_in(universal.GRAPPLE) or target.is_specialized_in(universal.BALANCED))]
        elif chosenAction.effectClass == combatAction.SPELL_SLINGERS:
            targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted) and (target.is_specialized_in_magic() or 
                target.is_specialized_in(universal.BALANCED))]
        elif chosenAction.effectClass == combatAction.ALL:
            targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted)]
    elif isSpectral:
        if hasattr(chosenAction, 'statusInflicted'):
            targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted)]
            for target in list(targets):
                statusEndured = [action[1] for action in actionsEndured[target] if isinstance(action[0], type(chosenAction))]
                numSuccesses = 0
                for status in statusEndured:
                    #Status is either a boolean, or a tuple containing the damage done, and a boolean indicating that the attack successfully inflicted the status
                    if type(status) == type(True) and status:
                        numSuccesses += 1
                    elif type(status) == type(()) and status[1]:
                        numSuccesses += 1
                targets.extend([target for i in range(numSuccesses)])
        avgdam = avg_damage(targets, chosenAction)
        for target in list(targets):
            avgDamEndured = avg_damage_endured(target, chosenAction)
            targets.extend([target for i in range(max(1, avgDamEndured - avgdam))])
    defenders = []
    if chosenAction == combatAction.ThrowAction:
        defenders.append(enemy.grapplingPartner)
        defenders.append(targets[random.randrange(0, len(targets))])
    else:
        for i in range(chosenAction.numTargets):
            if len(targets) == 0:
                break
            defenders.append(targets.pop(random.randrange(0, len(targets))))
            targets = [target for target in targets if target != defenders[-1]]
    return defenders                
                
                        
def avg_damage_endured(target, action=None):
    if action is None:
        effects = [endured for endured in actionsEndured[target]]
    else:
        effects = [endured for endured in actionsEndured[target] if isinstance(endured[0], type(action))]
    avgDam = 0
    count = 0
    for effect in effects:
        #The effect may be either a number or a tuple containing a number and a status, or it might not be an effect that does damage 
        try:
            avgDam += effect
        except TypeError:
            try:
                avgDam += effect[0]
            except:
                continue
            else:
                count += 1
        else:
            count += 1
    return int(avgDam) // count if count > 0 else 0

#TODO: Once we add a spell for "resurrecting" characters with zero hitpoints, need to modify this function to handle that.
def weight_healing(actionClass, companions):
    healingSpells = [spell for spell in actionClass if isinstance(spell, person.Healing)]
    activeCompanions = [comp for comp in companions if comp.current_health() > 0]
    if [spell for spell in actionClass if isinstance(spell, person.Resurrection)] != []:
            raise NotImplementedError("Our enemies can now use resurrection spells. We need to write code to allow their AI to deal with it.")
    if healingSpells == []:
        return actionClass
    elif get_difficulty() == STRAP:
        avgDam = avg_damage(companions)
        hurting = [comp for comp in companions if comp.current_health() <= avgDam and comp.health() - comp.current_health() > 0]
    elif get_difficulty() == CANE:
        maxDam = max_damage(companions)
        hurting = [comp for comp in companions if comp.current_health() <= maxDam and comp.health() - comp.current_health() > 0]
    if hurting == []:
        #If none of our allies need healing, we don't bother casting any healing magic.
        actionClass = [action for action in actionClass if not isinstance(action, person.Healing)]
    else:
        actionClass.extend([spell for i in range(len(hurting)) for spell in healingSpells])
    return actionClass

ACTION = 0
EFFECT = 1
def avg_damage(companions, chosenAction=None):
    actEndured = []
    if chosenAction is None:
        for comp in companions:
            actEndured.extend([action for action in actionsEndured[comp]])
    else:
        for comp in companions:
            actEndured.extend([action for action in actionsEndured[comp] if isinstance(action[0], type(chosenAction))])
    avgDam = 0
    count = 0
    for action in actEndured:
        #The effects could either be a list of numbers (such as with combat spells, or attacks) or a list of tuples containing damage and a status inflicted (such as 
        #with spectral spells.
        try:
            for i in range(action[0].numTargets):
                avgDam += combatAction.effects(action)[i]   
                count += 1
        except TypeError:
            try:
                for i in range(action[0].numTargets):
                    avgDam += combatAction.effects(action)[i][0]
                    count += 1
            except TypeError:
                continue
    return avgDam / count if count > 0 else 0

def max_damage(companions, chosenAction=None):
    actEndured = []
    if chosenAction is None:
        for comp in companions:
            actEndured.extend([action for action in actionsEndured[comp]])
    else:
        for comp in companions:
            actEndured = [action for action in actionsEndured[comp] if isinstance(


                combatAction.executed_action(action), type(chosenAction))]
    maxDam = 0
    for action in actEndured:
        try:
            for i in range(action[0].numTargets):
                if maxDam < combatAction.effects(action)[i]:
                    maxDam = combatAction.effects(action)[i]
        except TypeError:
            try:
                for i in range(action[0].numTargets):
                    if maxDam < combatAction.effects(action)[i][0]:
                        maxDam = combatAction.effects(action)[i][0]
            except TypeError:
                continue
    return maxDam


actionResults = []
def start_round(chosenActions):
    global actionResults, resultIndex, delay
    delay = COMBAT_DELAY
    actionResults = []
    resultIndex = 0
    for ally in allies:
        if ally.is_grappling():
            ally.increaseStatPoints[universal.STRENGTH] += 2
    def actions_sort_key(action):
        return action.attacker.stat(action.primaryStat) // 2 + action.attacker.alertness()
    #We order the actions based on the stat that each action depends on. For example, a character with a high warfare attacking is more likely to go first than a 
    #character with
    #a low grapple who is grappling. Because we shuffled the actions first, there's no guarantee on who goes first if two characters have the same values for the 
    #primary stat of their action.
    defendActions = [action for action in chosenActions if isinstance(action, combatAction.DefendAction)]
    #Next, we grab all characters who are grappling
    alreadyGrappling = sorted([action for action in chosenActions if action.attacker.is_grappling() and not action in defendActions], key=actions_sort_key, reverse=True)
    #Then, all characters casting spells (spells don't have a range limit, so they can be let off really fast)
    chosenActions = [action for action in chosenActions if not action in alreadyGrappling and not action in defendActions]
    spellActions = sorted([action for action in chosenActions if person.is_spell(action)])
    #Then all characters attacking with spears
    if is_catfight():
        knieActions = sorted([action for action in chosenActions if action.actionType == 
            combatAction.AttackAction.actionType], key=actions_sort_key, reverse=True)
        spearAttacks = []
        swordAttacks = []
    else:
        knifeAttacks = sorted([action for action in chosenActions if 
            action.attacker.weapon().weaponType == items.Knife.weaponType and action.actionType == 
            combatAction.AttackAction.actionType], key=actions_sort_key, reverse=True)
        spearAttacks = sorted([action for action in chosenActions if 
            action.attacker.weapon().weaponType == items.Spear.weaponType and action.actionType == 
            combatAction.AttackAction.actionType], key=actions_sort_key, reverse=True)
        #Then all characters attacking with swords
        swordAttacks = sorted([action for action in chosenActions if 
            action.attacker.weapon().weaponType == items.Sword.weaponType and 
            action.actionType == combatAction.AttackAction.actionType], key=actions_sort_key, 
            reverse=True)
    spankActions = sorted([action for action in chosenActions if 
        action.attacker.weapon().weaponType == items.Knife.weaponType and action.actionType == 
        combatAction.SpankAction.actionType], key=actions_sort_key, reverse=True)
    grappleTypes = [combatAction.GrappleAction.actionType, 
            combatAction.BreakAllysGrappleAction.actionType]
    grappleActions = sorted([action for action in chosenActions if action.actionType in grappleTypes], key=actions_sort_key, reverse=True)
    tiers = defendActions + alreadyGrappling + spellActions + spearAttacks + swordAttacks + knifeAttacks + spankActions + grappleActions
    #TODO: Need to grab all the other actions, not in any of the above
    allOtherActions = [action for action in chosenActions if action not in tiers]
    #We push all the defend actions to the beginning, so that every defending character is guaranteed to defend at the beginning.
    chosenActions = tiers + sorted(allOtherActions, key=actions_sort_key, reverse=True) 
    #If there are any duplicates, i.e. the above lists are not disjoint, this will fail.
    assert len(chosenActions) == len(set(chosenActions)), "There is a duplicated action:%s" % str(chosenActions) 
    for index in range(len(chosenActions)):
        action = chosenActions[index]
        errorLog = logging.getLogger("errors")
        errorLog.setLevel(logging.INFO)
        errorLog.addHandler(logging.FileHandler("errors.log"))
        errorLog.info(repr(action))
        if action is None:
            continue
        activeAllies = [ally for ally in allies if ally.current_health() > 0]
        activeEnemies = [enemy for enemy in enemies if enemy.current_health() > 0]
        if len(activeAllies) == 0 or len(activeEnemies) == 0:
            break
        assert action is not None, "Action is None when it isn't supposed to be!"
        attacker = action.attacker
        if attacker in activeAllies or attacker in activeEnemies:
            if attacker.is_grappling() and action.grappleStatus == combatAction.GRAPPLER_ONLY or action.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY:
                action.defenders = [attacker.grapplingPartner]
            elif attacker.is_grappling() and action.grappleStatus == combatAction.NOT_WHEN_GRAPPLED:
                action = combatAction.DefendAction(attacker, [attacker])
            actionEffect = action.effect(inCombat=True, allies=activeAllies, enemies=activeEnemies)
            count = 0
            if actionEffect[combatAction.ACTION].actionType == combatAction.RunAction.actionType and actionEffect[1][0]:
                end_combat()
                return
            else:
                try:    
                    actionsInflicted[action.attacker].append((
                                                             combatAction.executed_action(
                                                                 actionEffect), combatAction.effects(actionEffect)))
                except KeyError, e:
                    raise KeyError(str(e))
                defenders = combatAction.executed_action(actionEffect).defenders
                attacker = combatAction.executed_action(actionEffect).attacker
                print(actionEffect[0])
                for defender, effect in zip(defenders, combatAction.effects(actionEffect)):
                    if defender is not None:
                        actionsEndured[defender].append((
                                                        combatAction.executed_action(
                                                            actionEffect), effect))
                        if defender.current_health() <= 0:
                            if defender.is_grappling():
                                defender.break_grapple()
                            if defender.involved_in_spanking():
                                defender.terminate_spanking()
                            #A defeated character can't guard anyone.
                            for char in activeEnemies:
                                try:
                                    char.guardians.remove(defender)
                                except ValueError:
                                    pass
                            #A defeated character can't do anything.
                            for index2 in range(len(chosenActions)):
                                action2 = chosenActions[index2]
                                if action2 and action2.attacker == defender:
                                    chosenActions[index2] = None
                    isSpanking = isinstance(
                        combatAction.executed_action(actionEffect), combatAction.SpankAction)
                    isSpellSpanking = isinstance(
                        combatAction.executed_action(actionEffect), person.SpectralSpanking)
                    isSpanking = isSpanking or isSpellSpanking
                    if not (
                    combatAction.action_result_string(actionEffect), isSpanking) in actionResults:
                            actionResults.append((
                                                 combatAction.action_result_string(
                                                     actionEffect), isSpanking))
    decrement_grappling()
    print_round_results()

def decrement_grappling():
    for ally in allies:
        if ally.is_grappling():
            ally.reduce_grapple_duration(1)
            ally.grapplingPartner.reduce_grapple_duration(1)
            assert ally.grapple_duration() == ally.grapplingPartner.grapple_duration(), "Ally: %s ; grapple duration: %d, Enemy: %s ; grapple duration: %d" % (ally.name, ally.grapple_duration(),
                    ally.grapplingPartner.name, ally.grapplingPartner.grapple_duration())
            if not ally.grapple_duration():
                grapplingPartner = ally.grapplingPartner
                if ally.involved_in_spanking():
                    spankee = ally if ally.is_being_spanked() else grapplingPartner
                    spanker = ally if ally.is_spanking() else grapplingPartner
                    assert spanker != spankee, "Somehow, spanker: %s is spanking themselves!" % spanker.printedName
                    spanker.terminate_spanking()
                    actionResults.append((' '.join([spankee.printedName, "breaks free of", spanker.printedName + "'s", "punishing grip!"]), False))
                else:
                    ally.break_grapple()
                    actionResults.append(((' '.join([ally.printedName, "and", grapplingPartner.printedName, "break apart!"]), False)))
        #If this happens, it means someone is administering a spectral spanking.
        elif ally.involved_in_spanking():
            assert ally.spanker or ally.spankee, "Ally: %s is being spanked, but doesn't have a spanker!" % ally.name
            spanker = ally if ally.spankee else ally.spanker
            spankee = ally if ally.spanker else ally.spankee
            assert spanker != spankee, "Somehow, spanker: %s is spanking themselves!" % spanker.printedName
            spanker.reduce_grapple_duration(1)
            spankee.reduce_grapple_duration(1)
            assert spanker.grapple_duration() == spankee.grapple_duration(), "Spanker: %s ; grapple duration: %d, Spankee: %s ; grapple duration: %d" % (spanker.name, 
                    spanker.grapple_duration(), spankee.name, spankee.grapple_duration())
            if not spanker.grapple_duration():
                actionResults.append((spanker.position.end_statement(spankee), False))
                spanker.terminate_spanking()

resultIndex = 0
COMBAT_DELAY = 1000
delay = COMBAT_DELAY
ACTION_STRING = 0
IS_SPANKING = 1
def print_round_results():
    set_commands([('None')])
    global resultIndex
    if resultIndex == len(actionResults):
        if universal.state.instant_combat:
            universal.acknowledge(end_round, ())
        else:
            end_round()
    else:
        actionResult = actionResults[resultIndex]
        say_title('Combat!')
        actionResultSplit = [actionResult[ACTION_STRING]] if actionResult[IS_SPANKING] else actionResult[ACTION_STRING].split('\n')
        for result in actionResultSplit:
            if result.strip() == '':
                continue
            if universal.state.instant_combat:
                universal.say(result + '\n')
            else:
                if actionResult[1]:
                    universal.say_delay(result + "\n", overwritePrevious=True)
                else:
                    universal.say_delay(result + "\n", overwritePrevious=False)
                if len(actionResultSplit) > 1 and actionResultSplit[-1] != result:
                    pass
                    for i in range(0, 5):
                        delaySplit = delay // 5
                        pygame.time.delay(delaySplit)
        resultIndex += 1
        if actionResult[1] and not universal.state.instant_combat:
        #If the action is a spanking, then we need to give the player plenty of time to enjoy it. 
            acknowledge(print_round_results, ())
            #print_round_results()
        else:
            if not universal.state.instant_combat:
                for i in range(0, 5):
                #This is so that we can respond faster to the user pressing the enter key. 
                    delaySplit = delay // 5
                    pygame.time.delay(delaySplit)
            print_round_results()

def end_round():
    global allies, enemies, chosenActions, actionResults, defeatedAllies, defeatedEnemies
    if is_catfight():
        activeAllies = [ally for ally in allies if ally.current_humiliation() < ally.humiliation()]
        defeatedAllies.extend([ally for ally in allies if ally.current_humiliation() >= 
            ally.humiliation()])
    else:
        activeAllies = [ally for ally in allies if ally.current_health() > 0]
        defeatedAllies.extend([ally for ally in allies if ally.current_health() <= 0])
    allies = person.Party(activeAllies)
    if is_catfight():
        activeEnemies = [enemy for enemy in enemies if enemy.current_humiliation() < 
                enemy.humiliation()]
        defeatedEnemies.extend([enemy for enemy in enemies if enemy.current_humiliation() >= 
            enemy.humiliation()])
    else:
        activeEnemies = [enemy for enemy in enemies if enemy.current_health() > 0]
        defeatedEnemies.extend([enemy for enemy in enemies if enemy.current_health() <= 0])
    enemies = person.Party(activeEnemies)
    for ally in allies:
        ally.decrement_statuses()
    for enemy in enemies:
        enemy.decrement_statuses()
    if len(activeAllies) == 0 : 
        game_over()
    elif len(activeEnemies) == 0:
        victory()
    else:
        chosenActions = []
        actionResults = []
        display_combat_status()

def game_over():
    music.play_music(music.DEFEATED)
    clear_screen()
    say_title('Game over!')
    universal.say('You have been defeated! Would you like to try again?\n\n')
    if optional:
        universal.say('Note that winning this fight is optional. Saying "no" will NOT give you a game over.')
    else:
        universal.say('Note that you need to win this fight to continue the game. If you say "no" you will return to the title screen.')
    set_commands(["(Enter) Try Again", "(Esc) Don't try again"])
    set_command_interpreter(game_over_interpreter)

def game_over_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        global allies, enemies, chosenActions, actionResults, actionsEndured, actionsInflicted, defeatedAllies, defeatedEnemies
        #universal.set_state(copy.deepcopy(initialState))
        for charid, primaryStats, statusDict, spellPoints, statPoints in initialAllies:
            character = universal.state.get_character(charid)
            character.primaryStats = list(primaryStats)
            character.statusDict = dict(statusDict)
            character.increaseSpellPoints = list(spellPoints)
            character.increaseStatPoints = list(statPoints)
            character.break_grapple()
        for charid, primaryStats, statusDict in initialEnemies:
            character = universal.state.get_character(charid)
            character.primaryStats = list(primaryStats)
            character.statusDict = dict(statusDict)
            character.break_grapple()
        allies = universal.state.allies
        enemies = universal.state.enemies
        defeatedEnemies = []
        defeatedAllies = []
        actionsEndured = {combatant:[] for combatant in enemies + allies}
        actionsInflicted = {combatant:[] for combatant in enemies + allies}
        chosenActions = []
        display_combat_status()
        global activeAlly
        activeAlly = allies[0]
        if boss:
            music.play_music(music.BOSS)
        elif is_catfight():
            music.play_music(music.CATFIGHT)
        else:
            music.play_music(music.COMBAT)
    elif keyEvent.key == K_ESCAPE:
        if optional:
            try:
                #defeatedAllies = allies.members + defeatedAllies
                #defeatedEnemies = [enemy for enemy in enemies if enemy.current_health() <= 0] + defeatedEnemies
                improve_characters(False, afterCombatEvent)
            except TypeError:
                pass
            #allies = universal.state.allies
            end_fight()
            #allies.members += defeatedAllies    
        else:
            end_fight()
            universal.state.enemies = None
            universal.state.allies = None
            titleScreen.title_screen()
        return


def victory():
    """
    Note: If there is an afterCombatEvent, then that function will have to transtition the player into the appropriate mode. We can't do it here, because the 
    after combat event may require player input, in which case the game would immediately go into the previous mode before the player can actually give any input to the
    after combat event.
    """
    clear_screen()
    global coordinates
    if randomEncounter:
        universal.state.clear_encounter(coordinates)
        coordinates = None
    global allies, defeatedAllies, enemies, defeatedEnemies
    allies.members += defeatedAllies
    enemies.members += defeatedEnemies
    universal.state.allies = None
    universal.state.enemies = None
    activeAllies = [ally for ally in allies if ally.current_health() > 0]
    activeEnemies = [enemy for enemy in enemies if enemy.current_health() > 0]
    for enemy in enemies:
        enemy.restores()
    clear_screen()
    say_title('Victory!')
    universal.say(format_line([universal.state.player.name, 'has defeated', person.hisher(), 'enemies.\n']))
    music.play_music(music.VICTORY)
    for ally in allies:
        ally.break_grapple()
    improve_characters(True, afterCombatEvent)
    end_fight()

BASE_XP = 15
XP_RATE = 5

def specialization_bonus(ally, i):
    if ally.is_bonus(i):
        bonus = 4 * person.HEALTH_SCALE if i == HEALTH or i == MANA else 4
    elif ally.is_penalty(i):
        bonus = -1 * person.HEALTH_SCALE if i == HEALTH or i == MANA else -1
    else:
        bonus = 3 * person.HEALTH_SCALE if i == HEALTH or i == MANA else 3
    return bonus

HIGH_STAT_PENALTY = .1
BASE_HEALTH_INCREASE = 8
def improve_characters(victorious, afterCombatEvent=None):
    """
    Takes as argument the function that should be invoked after leveling up is complete.
    """
    if is_catfight():
        if afterCombatEvent is not None:
            acknowledge(afterCombatEvent, defeatedAllies, defeatedEnemies,
                        victorious)
        else:
            acknowledge(previousMode)
        return
    #Characters can gain stat points even if they are knocked out.
    for ally in allies.members + defeatedAllies:
        #We temporarily remove the ally's status effects, so that they don't interfere with stat gain.
        #TODO: Similarly remove the effect of bonuses.
        allyStatuses = ally.get_statuses()
        ally.clear_statuses()
        for i in range(len(ally.increaseStatPoints)):
            statPoints = ally.increaseStatPoints[i]
            stat = ally.stat(i) if i == universal.HEALTH else ally.stat(i) * universal.STAT_GROWTH_RATE_MULTIPLIER 
            spells = [universal.COMBAT_MAGIC, universal.STATUS_MAGIC, universal.BUFF_MAGIC, universal.SPECTRAL_MAGIC]
            specialtyModifier = 1
            if ally.is_specialized_in(i) or (i == universal.TALENT and ally.specialization in spells):
                specialtyModifier = .5
            elif ally.is_weak_in(i):
                specialtyModifier = 2
            gain = 0
            manaGain = 0
            threshhold = int(math.floor(stat * specialtyModifier))
            while threshhold <= statPoints:
                if i == universal.HEALTH:
                    gain += BASE_HEALTH_INCREASE + min(5, (statPoints - threshhold))
                    ally.improve_stat(i, gain)
                    ally.increaseStatPoints[i] = 0
                else:
                    stat = ally.stat(i) * universal.STAT_GROWTH_RATE_MULTIPLIER
                spells = [universal.COMBAT_MAGIC, universal.STATUS_MAGIC, universal.BUFF_MAGIC, 
                        universal.SPECTRAL_MAGIC]
                specialtyModifier = 1
                if ally.is_specialized_in(i) or (i == universal.TALENT and ally.specialization in 
                        spells):
                    specialtyModifier = .5
                elif ally.is_weak_in(i):
                    specialtyModifier = 2
                gain = 0
                manaGain = 0
                while int(math.floor(stat * specialtyModifier)) <= statPoints:
                    if i == universal.HEALTH:
                        gain += int(math.ceil(stat * HEALTH_MULTIPLIER))
                        ally.improve_stat(i, gain)
                        ally.increaseStatPoints[i] = 0
                    else:
                        gain += 1
                        ally.improve_stat(i, 1)
                        if i == universal.TALENT:
                            manaGain += 3
                            ally.improve_stat(person.MANA, manaGain)
                        ally.increaseStatPoints[i] -= stat 
                    statPoints = ally.increaseStatPoints[i]
                    stat = ally.stat(i) * universal.STAT_GROWTH_RATE_MULTIPLIER
                if gain:
                    universal.say(format_line([ally.name, 'has gained', str(gain), 
                        person.primary_stat_name(i) + '.\n']))
                if manaGain:
                    universal.say(format_line([ally.name, 'has gained', str(manaGain), 'Mana.\n']))
            for i in range(len(ally.increaseSpellPoints)): 
                #Note: This is much MUCH simpler than what we will actually allow. This simply checks if the player has 5 spell points, and then has the player learn the advanced spell if the player 
                #doesn't already know it.
                #This is only a stop-gap measure. The actual learning spell mechanic will be much more complicated, but I don't want to implement that until I've built a proper GUI.
                statThreshhold = (ally.tier*universal.STAT_GROWTH_RATE_MULTIPLIER if ally.tier else 
                        person.TIER_0_SPELL_POINTS)
                if ally.increaseSpellPoints[i] >= statThreshhold and not ally.knows_spell(
                                person.allSpells[0][i][1]):
                    learn_spell(ally, i+universal.COMBAT_MAGIC)
                    ally.increaseSpellPoints[i] -= ally.tier*universal.STAT_GROWTH_RATE_MULTIPLIER if ally.tier else person.TIER_0_SPELL_POINTS
            #Now that we're done increasing stats, we can reinflict any lingering statuses
            for statusName in allyStatuses:
                status = allyStatuses[statusName][0]
                status.duration = allyStatuses[statusName][1]
                ally.inflict_status(status)
    if afterCombatEvent is not None:
        acknowledge(afterCombatEvent, defeatedAllies, defeatedEnemies, victorious)
    else:
        acknowledge(previousMode)

def learn_spell(ally, spellSchool):
    """
    TODO: Currently, the spells learned are random within a given school. However, this needs to be modified to give the player a choice. I'll implement for a choice as a part of episode 3, when I rework the GUI. Don't want to add too much more to the
    GUI until I've reworked it.
    """
    spellIndex = person.get_spell_index(spellSchool)
    unknownSpells = []
    for i in range(0, ally.tier+1):
        #Need to learn basic before you can learn advanced before you can learn specialized. Can only learn specialized if you are specialized in this particular type of
        #magic.
        try:
            if not ally.knows_spell(person.allSpells[i][spellIndex][0]):
                #We weight the spells based on their tier level. Spells that have tier 0 have 1 weight, spells of tier 1 have 2 weight and so on. This increases the chances
                #of a character learning a more powerful spell sooner.
                unknownSpells.append(person.allSpells[i][spellIndex][0])    
            elif not ally.knows_spell(person.allSpells[i][spellIndex][1]):
                unknownSpells.append(person.allSpells[i][spellIndex][1])    
            elif ally.specialization == spellSchool and not ally.knows_spell(person.allSpells[i][spellIndex][2]):
                unknownSpells.append(person.allSpells[i][spellIndex][2])    
        except TypeError:
            continue
    if len(unknownSpells) > 0:
        learnedSpell = unknownSpells[random.randint(0, len(unknownSpells)-1)]
        ally.learn_spell(learnedSpell)
        ally.add_quick_spell(learnedSpell)
        universal.say(format_line([ally.name, 'has learned the spell', learnedSpell.name + '!\n']))
    else:
        ally.increaseSpellPoints[i-universal.COMBAT_MAGIC] = ally.tier * universal.STAT_GROWTH_RATE_MULTIPLIER if ally.tier else person.TIER_0_SPELL_POINTS
        

