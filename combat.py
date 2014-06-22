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
import items
import person
import music
import combatAction
from combatAction import ALLY, ENEMY
import pygame
import titleScreen
import copy
import random
import statusEffects
import operator
import music
import copy
import townmode
import dungeonmode
import statusEffects

"""
Note: The interpreters all assume that you will only ever face up to 9 enemies at 
once. If you want to face more than 9 enemies, you'll have to modify the interpreters to 
take multi-digit numbers as well (see the save_game interpreter for ideas on how to do that).

Furthermore, I've commented out the code that allows the player and enemies to spank each other in combat. The reason for this is two-fold:
        1. The spankings are kind of boring. They exist in a vaccum, and I can't really write any interesting interaction between the spanker and spankee. Therefore,
        these essentially boil down to trying to find a thousand ways of saying "Person A hit Person B's bottom, and it was sexy." While these types of generic spankings
        could be enjoyable in a game with graphics, in a text-based game they're kind of boring.
        2. It seriously messes with the atmosphere of combat. Combat is treated in the story-proper as a pretty serious, and dangerous thing. Furthermore, there may be
        very dark, and serious moments right before a battle. Being able to spank your opponent is kind of silly in that respect, and detracts from said seriousness.
        Basically, Pandemonium Cycle has become too serious for this kind of mechanic.
"""


#message for indicating status is cleared: [character.name, 'is no longer affected by', status.name, '!']


TITLE_OFFSET = 15
allies = None
origAllies = None
origEnemies = None
afterCombatEvent = None
worldView = None
enemies = None
bg = None
runnable = True
activeAlly = None
chosenActions = []
titleFont = pygame.font.SysFont(universal.FONT_LIST, universal.TITLE_SIZE)
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
def end_fight():
    global allies, enemies, actionsInflicted, actionsEndured, activeAlly, chosenActions 
    allies = None
    enemies = None
    actionsInflicted = {}
    actionsEndured = {}
    activeAlly = None
    chosenActions = []
def fight(enemiesIn, afterCombatEventIn=None, previousModeIn=dungeonmode.dungeon_mode, runnableIn=True, bossFight=False, optionalIn=False, additionalAllies=None, 
        ambushIn=0):
    global afterCombatEvent, activeAlly, worldView, enemies, bg, allies, allySurface, enemySurface, commandSurface, clearScreen, previousMode, origAllies, origEnemies, \
            actionsInflicted, actionsEndured, chosenActions, optional, defeatedEnemies, defeatedAllies
    global ambush
    global boss
    boss = bossFight
    ambush = ambushIn
    enemies = None
    allies = None
    defeatedAllies = []
    defeatedEnemies = []
    optional = optionalIn
    print(enemiesIn)
    print(person.get_party().members)
    print(additionalAllies if additionalAllies is not None else [])
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
    else:
        music.play_music(music.COMBAT)
    if type(enemiesIn) != list:
        enemiesIn = [enemiesIn]
    origEnemies = copy.deepcopy(enemiesIn)
    enemies = person.Party(enemiesIn)
    if additionalAllies is not None:
        allies = person.Party(list(person.get_party().members + additionalAllies))
    else:
        allies = person.Party(list(person.get_party().members))
    for ally in allies:
        ally.chanceIncrease = [0 for i in range(len(ally.chanceIncrease))]
    origAllies = copy.deepcopy(allies.members)
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
    runnable = runnableIn
    activeAlly = allies[0]
    maxAllyLevel = max([sum(ally.get_battle_stats()) for ally in allies]) 
    print([sum(ally.get_battle_stats()) for ally in allies])
    print([ally.get_battle_stats() for ally in allies])
    maxEnemyLevel = max([sum(enemy.get_battle_stats()) for enemy in enemies])
    print('maxAllyLevel: ' + str(maxAllyLevel))
    print('maxEnemyLevel: ' + str(maxEnemyLevel))
    for ally in allies:
        if sum(ally.get_battle_stats()) <= maxEnemyLevel:
            orderResult = ally.order(ally, allies, enemies)
            if orderResult is not '':
                say_delay(orderResult)
                for i in range(0, 5):
                    delaySplit = delay // 5
                    pygame.time.delay(delaySplit)
    for enemy in enemies:
        if sum(enemy.get_battle_stats()) <= maxAllyLevel:
            orderResult = enemy.order(enemy, enemies, allies)
            if orderResult is not '':
                say_delay(orderResult)
                for i in range(0, 5):
                    delaySplit = delay // 5
                    pygame.time.delay(delaySplit)
    if ambush < 0:
        say_delay('The party has been ambushed!')
        ambush = 0
        for i in range(0, 5):
            delaySplit = delay // 5
            pygame.time.delay(delaySplit)
        choose_enemy_actions()
    else:
        if ambush > 0:
            say_delay('The party has ambushed their enemies!')
            for i in range(0, 5):
                delaySplit = delay // 5
                pygame.time.delay(delaySplit)
        display_combat_status()

def end_combat():
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
    commandList = ['(A)ttack', '(C)ast', '(D)efend', '(L)ook']
    if activeAlly.is_grappling():
        commandList.remove('(L)ook')
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
    print('setting commands')   
    print(commandList)  
    set_command_interpreter(battle_interpreter)

def print_enemies(enemies, targetList=None, title='Enemies'):
    screen = get_screen()
    say_title(title, surface=enemySurface)
    flush_text(TITLE_OFFSET)
    pygame.draw.line(enemySurface, LIGHT_GREY, 
            (enemySurface.get_rect().topleft[0], enemySurface.get_rect().topleft[1] + 3), 
            (enemySurface.get_rect().topright[0], enemySurface.get_rect().topleft[1] + 3), 
                7)
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
        universal.say('\t'.join(['', 'Health:', 'Mana:', 'Grappling:\t']), surface=allySurface, columnNum=4)
        universal.say(allies.display_party(ally=activeAlly, targeted=targetList, grappling=True), 
                surface=allySurface, columnNum=4)
    flush_text(TITLE_OFFSET)
    screen.blit(allySurface, enemySurface.get_rect().bottomleft)

def print_command(command):
    screen = get_screen()
    commandScreenCoord = (enemySurface.get_rect().bottomleft[0], 
            enemySurface.get_rect().bottomleft[1] + allySurface.get_height())
    commandSurface.fill(DARK_GREY)
    screen.blit(commandSurface, commandScreenCoord)
    fontSize = pygame.font.SysFont(FONT_LIST, TITLE_SIZE).size(command)
    say_title(command, surface=commandSurface)
    flush_text(13)
    cmdMidTop = commandSurface.get_rect().midtop
    pygame.draw.rect(commandSurface, LIGHT_GREY, 
            pygame.Rect(cmdMidTop[0] - fontSize[0], cmdMidTop[1], fontSize[0] + fontSize[0], fontSize[1] + fontSize[1]), 10) 
    screen.blit(commandSurface, commandScreenCoord)

def battle_interpreter(keyEvent):
    global chosenActions, activeAlly
    if keyEvent.key == K_ESCAPE:
        set_commands(['Are you sure you want to quit? (Y/N)'])
        set_command_interpreter(confirm_to_title_interpreter)
    elif keyEvent.key == '<==Back':
        if allies[0] != activeAlly:
            activeAlly = allies[allies.index(activeAlly)-1]
            del chosenActions[-1]
            display_combat_status(printEnemies=False, printAllies=False)
    elif keyEvent.key == K_a:
        attack()
    elif keyEvent.key == K_c:
        cast()
    elif keyEvent.key == K_d:
        defend()
    elif activeAlly.is_grappling():
        #if keyEvent.key == K_s:
            #spank()
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
        get_screen().blit(get_background(), (0, 0))
        say_title('Confirm Actions')
        for action in chosenActions:
            universal.say(print_action(action) + '\n\n') 
        set_commands(['Begin round(Y/N)?'])
        set_command_interpreter(begin_round_interpreter)


def print_action(action):
    defenders = ', '.join([d.printedName for d in action.defenders if d is not None])
    attacker = action.attacker.printedName
    if isinstance(action, combatAction.AttackAction):
        return ' '.join([attacker, 'will attack', defenders + '.'])
    elif isinstance(action, combatAction.ThrowAction):
        return ' '.join([attacker, 'will throw', action.defenders[0].printedName, 'at', 
                action.defenders[1].printedName + '.'])
    elif isinstance(action, combatAction.GrappleAction):
        return ' '.join([attacker, 'will grapple', defenders + '.'])
    elif isinstance(action, combatAction.DefendAction):
        return ' '.join([attacker, 'will defend', defenders + '.'])
    elif isinstance(action, combatAction.RunAction):
        return ' '.join([attacker, 'will try to flee.'])
    elif isinstance(action, combatAction.BreakGrappleAction):
        return ' '.join([attacker, 'will attempt to stop grappling', defenders + '.'])
    elif isinstance(action, combatAction.SpankAction):
        return ' '.join([attacker, 'will spank', defenders, 'in the', action.position.name, 'position.'])
    elif isinstance(action, combatAction.BreakAllysGrappleAction):
        return ' '.join([attacker, 'will break', defenders + "'s", 'grapple.'])
    elif isinstance(action, person.Spell):
        return ' '.join([attacker, 'will cast', action.name, 'on', defenders + '.'])

def increase_stat_chance():
    numStats = len(person.allStats)
    global chosenActions
    for action in chosenActions:
        increaseStat = action.attacker.chanceIncrease
        if action.attacker in allies:
                increaseStat[action.primaryStat] += 8 if increaseStat[action.primaryStat] < 16 else 4
                try:
                    increaseStat[action.spellType] += 8 if increaseStat[action.spellType] < 16 else 4
                except AttributeError:
                    continue
                try:
                    increaseStat[action.secondaryStat] += 4 if increaseStat[action.secondaryStat] == 0 else 2
                except AttributeError:
                    continue
        elif action.attacker in enemies:
            print('----------------defenders of action: ' + str(action) + '-------------------')
            print(action.defenders)
            for defender in action.defenders:
                defender.chanceIncrease[action.primaryStat] += 2
                try:    
                    increaseStat[action.secondaryStat] += 1
                except AttributeError:
                    continue

def begin_round_interpreter(keyEvent):
    global chosenActions, chosenTargets
    if keyEvent.key == K_y:
        global ambush
        if ambush <= 0:
            choose_enemy_actions()
        else:
            ambush = 0
        increase_stat_chance()
        start_round(chosenActions)
    elif keyEvent.key == K_n:
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
    elif keyEvent.key == K_n:
        display_combat_status(printAllies=False, printEnemies=False)


def attack():
    print_command('Attack')
    if activeAlly.is_grappling():
        set_commands(['(Enter) Attack grappling partner.', '<==Back'])
    else:
        set_commands(['(#) Select target.'])
    set_command_interpreter(attack_interpreter)

def attack_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif activeAlly.is_grappling() and keyEvent.key == K_RETURN:
        chosenActions.append(combatAction.AttackAction(activeAlly, activeAlly.grapplingPartner))
        next_character()
    elif not activeAlly.is_grappling() and keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(enemies) and enemies[num] in [enemy for enemy in enemies if enemy.current_health() > 0]:
            chosenActions.append(combatAction.AttackAction(activeAlly, enemies[num]))
            next_character()

def cast():
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
        set_commands([' '.join(['(#)', 'Select', str(chosenSpell.numTargets), 
            targets if chosenSpell.numTargets > 1 else target]), '<==Back', 
            '(Enter) Cast Spell'])
    set_command_interpreter(target_spell_interpreter)

chosenTargets = []
spellIncrease = 10
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
    if targetAllies:
        targetStr = 'ally'
        targetStrs = 'allies'
    if activeAlly.is_grappling():
        if keyEvent.key == K_RETURN:
            if chosenSpell.targetType == ENEMY:
                chosenActions.append(chosenSpell.__class__(activeAlly, activeAlly.grapplingPartner))
                activeAlly.chanceIncrease[chosenSpell.spellSchool] += spellIncrease
            else:
                chosenActions.append(chosenSpell.__class__(activeAlly, activeAlly))
                activeAlly.chanceIncrease[chosenSpell.spellSchool] += spellIncrease
            next_character()
        elif keyEvent.key == K_BACKSPACE:
            print_allies(allies)
            print_enemies(enemies)
            select_spell(chosenTier)
    else:
        print('targeting.')
        if keyEvent.key == K_BACKSPACE:
            print('reducing targets.')
            if numTargetsChosen == 0:
                print('numTargetsChosen is 0')
                print_allies(allies)
                print_enemies(enemies)
                select_spell(chosenTier)
            else:
                print('removing target')
                print(chosenTargets)
                chosenTargets.pop()
                printTargets(targets, chosenTargets)
                print('chosenTarget removed.')
                print(chosenTargets)
        elif keyEvent.key in NUMBER_KEYS:
            num = int(pygame.key.name(keyEvent.key)) - 1
            if 0 <= num and num < len(targets) and not targets[num] in chosenTargets:
                print('targeting enemy. targets remaining:' + str(chosenTargets))
                chosenTargets.append(targets[num])
                numTargetsChosen += 1
                printTargets(targets, chosenTargets)
                print('chosenSpell.numTargets - numTargetsChosen: ' +  str(chosenSpell.numTargets - numTargetsChosen))
                print('len(enemies) - numTargetsChosen: ' +  str(len(enemies) - numTargetsChosen))
                if chosenSpell.numTargets - numTargetsChosen > 0 and len(enemies) - numTargetsChosen > 0:
                    print('setting commands:' + str([format_line(['(#) Select', str(chosenSpell.numTargets - numTargetsChosen),
                        targetStrs if chosenSpell.numTargets - numTargetsChosen > 1 else targetStr]), 
                        '<==Back', '(Enter)Cast spell']))
                    set_commands([format_line(['(#) Select', str(chosenSpell.numTargets - numTargetsChosen),
                        targetStrs if chosenSpell.numTargets - numTargetsChosen > 1 else targetStr]), 
                        '<==Back', '(Enter)Cast spell'])
                else:
                    #set_commands([' '.join(['Cast', chosenSpell.name + '?(Y/N)'])])
                    #set_command_interpreter(confirm_cast_interpreter)
                    chosenActions.append(chosenSpell.__class__(activeAlly, chosenTargets))
                    activeAlly.chanceIncrease[chosenSpell.spellSchool] += spellIncrease
                    next_character()
        elif keyEvent.key == K_RETURN and len(chosenTargets) > 0:
            chosenActions.append(chosenSpell.__class__(activeAlly, chosenTargets))
            activeAlly.chanceIncrease[chosenSpell.spellSchool] += spellIncrease
            next_character()

"""
def confirm_cast_interpreter(keyEvent):
    global chosenActions, chosenTargets
    if keyEvent.key == K_y:
        chosenActions.append(chosenSpell.__class__(activeAlly, chosenTargets))
        next_character()
    elif keyEvent.key == K_n:
        chosenTargets.pop()
        if chosenSpell.targetType == ALLY:
            print_allies(allies, chosenTargets)
        else:
            print_enemies(enemies, chosenTargets)
        target_spell()
"""

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
        if 0 <= num and num < len(allies):
            chosenActions.append(combatAction.DefendAction(activeAlly, allies[num]))
            next_character()

possibleTargets = []
def break_grapple():
    global possibleTargets
    print(activeAlly.is_grappling())
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
    print_command('Position')
    set_commands(numbered_list([p.name for p in activeAlly.grapplingPartner.spankingPositions]) + ['<==Back'])
    set_command_interpreter(spank_interpreter)

chosenPos = None
def spank_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num <= len(activeAlly.grapplingPartner.spankingPositions):
            global chosenPos
            chosenPos = activeAlly.grapplingPartner.spankingPositions[num]
            say_title(chosenPos.name, surface=allySurface)
            print_allies(chosenPos.display())
            set_commands(['Use this position? (Y/N)'])
            set_command_interpreter(confirm_spanking_interpreter)

def confirm_spanking_interpreter(keyEvent):
    if keyEvent.key == K_y: 
        chosenActions.append(combatAction.SpankAction(activeAlly, activeAlly.grapplingPartner, chosenPos))
        next_character()
    elif keyEvent.key == K_n:
        print_allies(allies)
        spank()

def throw():
    print_command('Throw')
    set_commands([' '.join(['(#) Select target.']), '<==Back'])
    set_command_interpreter(throw_interpreter)

def throw_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        display_combat_status(printAllies=False, printEnemies=False)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 <= num and num < len(enemies):
            chosenActions.append(combatAction.ThrowAction(activeAlly, [activeAlly.grapplingPartner, enemies[num]]))
            next_character()

def choose_enemy_actions():
    for enemy in enemies:
        chosenActions.append(select_action(enemy))

def select_action(enemy):
    allActions = [combatAction.AttackAction]#, combatAction.DefendAction]
    if enemy.is_grappling():
        #allActions.extend([combatAction.SpankAction, combatAction.ThrowAction, combatAction.BreakGrappleAction])
        allActions.extend([combatAction.ThrowAction, combatAction.BreakGrappleAction])
        allActions.extend([spell.__class__ for spell in enemy.flattened_spell_list() if spell.grappleStatus != combatAction.NOT_WHEN_GRAPPLED and 
            spell.cost <= enemy.current_mana()])
    else:
        allActions.append(combatAction.GrappleAction)
        if filter(lambda x : x.is_grappling(), enemies) != []:
            allActions.append(combatAction.BreakAllysGrappleAction)
        allActions.extend([spell.__class__ for spell in enemy.flattened_spell_list() if spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY and 
            spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED and spell.cost <= enemy.current_mana()])
    if get_difficulty() == HAND:
        return hand_ai(enemy, allActions)
    elif get_difficulty() == STRAP or get_difficulty() == CANE:
        return strap_cane_ai(enemy)

def hand_ai(enemy, allActions):
    action = allActions[random.randrange(0, len(allActions))]
    defenders = []
    if enemy.is_grappling() and (action.grappleStatus == combatAction.GRAPPLER_ONLY or action.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY):
        defenders = [enemy.grapplingPartner]
    else:
        targetList = list(allies if action.targetType == combatAction.ENEMY else enemies)
        for i in range(0, action.numTargets):
            chosenAlly = targetList.pop(random.randrange(0, len(targetList)))
            defenders.append(chosenAlly)
            if targetList == [] and action == combatAction.ThrowAction:
                defenders.append(defenders[0])
                break
    if action == combatAction.SpankAction:
        randIndex = random.randrange(0, len(enemy.spankingPositions))
        action = combatAction.SpankAction(enemy, defenders, enemy.spankingPositions[randIndex])
    else:
        action = action(enemy, defenders)
    return action   

def strap_cane_ai(enemy):
    """
    If we're using the strap difficulty, then targeting is random, and action choice depends only on what a character is good at.
    """
        #This allows us to use this ai for any computer controlled allies of the player as well.
    companions = enemies if enemy in enemies else allies
    opponents = allies if enemy in enemies else enemies
    warfareActions = [combatAction.AttackAction]
    #If our enemy is not grappling and he/she is wielding a dagger, then he/she wants to try to grapple as soon as possible, because a dagger is basically useless when
    #not grappling.
    if enemy.is_grappling():
        if get_difficulty() == STRAP or (get_difficulty() == CANE and enemy.weapon().weaponType == items.Sword.weaponType):
            warfareActions.append(combatAction.BreakGrappleAction)
            grappleActions = [combatAction.ThrowAction, combatAction.AttackAction]#, combatAction.DefendAction]
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Knife.weaponType:
            #warfareActions.append(combatAction.BreakGrappleAction)
            grappleActions = [combatAction.ThrowAction, combatAction.AttackAction]#, combatAction.DefendAction]
        #If the character is using a spear, then they are at a serious disadvantage when grappling, and they need to break out of it ASAP.
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Spear.weaponType: 
            warfareActions = [combatAction.BreakGrappleAction]
            grappleActions = [combatAction.BreakGrappleAction]
        availableSpells = [spell for spell in enemy.flattened_spell_list() if spell.grappleStatus != combatAction.NOT_WHEN_GRAPPLED and enemy.current_mana() >= spell.cost]
    else:
        if get_difficulty() == CANE and enemy.weapon().weaponType == items.Knife.weaponType:
            warfareActions = []
        if get_difficulty() == STRAP or (get_difficulty() == CANE and (enemy.weapon().weaponType == items.Sword.weaponType or 
            enemy.weapon().weaponType == items.Knife.weaponType)):
            grappleActions = [combatAction.GrappleAction]
        #If your enemy is wielding a spear, the last thing they want is to try to grapple you.
        elif get_difficulty() == CANE and enemy.weapon().weaponType == items.Spear.weaponType: 
            grappleActions = []
        if [comp for comp in companions if comp.is_grappling() and comp != enemy] != []:
            grappleActions.append(combatAction.BreakAllysGrappleAction)
        availableSpells = [spell for spell in enemy.flattened_spell_list() if spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED and 
                spell.grappleStatus != combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY and enemy.current_mana() >= spell.cost]

    magicActions = list(availableSpells)

    #We have one reference to each action type for every value in a character's stat + 1 so that every class appears.
    weightedActionClasses = [warfareActions for i in range(max(1, enemy.warfare()))] + [grappleActions for i in range(max(1, enemy.grapple()))]
    if magicActions != []:
        weightedActionClasses += [magicActions for i in range(max(1, enemy.magic()))]
    if get_difficulty() == CANE:
        #For now, this does nothing. Not sure if we want to do anything to perform additional weighting on the classes for cane difficulty.
        weightedActionClasses = weight_classes_cane(weightedActionClasses)
    chosenActionClass = []
    while chosenActionClass == []:
        chosenActionClass = weightedActionClasses[random.randrange(0, len(weightedActionClasses))]
        if chosenActionClass == warfareActions:
            if enemy.is_grappling():
                warfareActions.extend([combatAction.BreakGrappleAction for i in range(max(0, enemy.warfare() - enemy.grapple()))]) 
            else:
                warfareActions.extend([combatAction.AttackAction for i in range(max(0, enemy.warfare()))])
            #warfareActions.extend([combatAction.DefendAction for statName in enemy.status_names() if statusEffects.is_negative(enemy.get_status(statName))])
        elif chosenActionClass == grappleActions:
            if enemy.is_grappling():
                #if not enemy.grapplingPartner.is_inflicted_with(statusEffects.Humiliated.name):
                    #grappleActions.extend([combatAction.SpankAction for i in range(max(1, enemy.grapple()))])
                grappleActions.extend([combatAction.AttackAction for i in range(max(1, enemy.warfare()))])
                grappleActions.extend([combatAction.ThrowAction for i in range(max(1, enemy.grapple()))])
            else:
                grappleActions.extend([combatAction.GrappleAction for i in range(max(1, enemy.grapple()))])
                grappledCompanions = [e for e in companions if e.is_grappling()]
                for companion in grappledCompanions:
                    #The idea here that if this character has a much higher grapple than his ally, then not only is this character good for breaking a grapple, but 
                    #it's likely that his ally has a low grapple, in which case the ally needs all the help he can get.
                    grappleActions.extend([combatAction.BreakAllysGrappleAction for i in range(max(0, enemy.grapple() - companion.grapple()))])
            #grappleActions.extend([combatAction.DefendAction for statName in enemy.status_names() if statusEffects.is_negative(enemy.get_status(statName))])
        elif chosenActionClass == magicActions:
            for spell in availableSpells:
                if hasattr(spell, 'statusInflicted'):
                    inflictedAllies = [ally for ally in allies if not ally.is_inflicted_with(statusEffects.get_name(spell.statusInflicted))]
                    if inflictedAllies == [] and spell in magicActions:
                        magicActions.remove(spell)
                    else:
                        magicActions.extend([spell for i in range(spell.tier)])
            if chosenActionClass != []:
                chosenActionClass = weight_healing(magicActions, companions)
                print('chosenActionClass:')
                print(chosenActionClass)
            if chosenActionClass != []:
                chosenActionClass = weight_status_buff(enemy, chosenActionClass)
    #We want to guarantee that the magicActions contain only spells when weighting them for the cane difficulty.
    chosenActionClass.extend([combatAction.DefendAction for statName in enemy.status_names() if statusEffects.is_negative(enemy.get_status(statName))])
    chosenAction = chosenActionClass[random.randrange(0, len(chosenActionClass))]
    print(chosenActionClass)
    print('chosenActionClass:')
    print(chosenActionClass)
    if get_difficulty() == CANE:
        defenders = []
        while defenders == []:
            if chosenActionClass == []:
                return strap_cane_ai(enemy)
            chosenAction = chosenActionClass.pop(random.randrange(0, len(chosenActionClass)))
            defenders = select_targets(chosenAction, enemy)
            chosenActionClass = [actionClass for actionClass in chosenActionClass if actionClass.actionType != chosenAction.actionType]
        #Note: The below won't actually happen, because I've commented out the code that allows the player and the enemy to use the SpankAction.
        if chosenAction == combatAction.SpankAction:
            posDifficulty = [pos.difficulty + pos.reversability - pos.maintainability for pos in enemy.spankingPositions]
            posAndDiff = zip(enemy.spankingPositions, posDifficulty)
            minDiff = float("inf")
            easiestPos = 0
            for pos, difficulty in posAndDiff:
                if difficulty < minDiff:
                    minDiff = difficulty
                    easiestPos = pos
            weightedPos = [easiestPos]
            #list of pairs containing the position and the result, which is a number of smacks. If positive, the spanking worked. If zero it didn't, if negative, it 
            #got reversed
            pastPositions = [(effect[0].position, effect[1]) for effect in actionsEndured[defenders[0]] if isinstance(effect[0], combatAction.SpankAction)]
            for pos, difficulty in posAndDiff:
                weightedPos.extend([pos for i in range(min(0, enemy.grapple() - difficulty))]) 
                weightedPos.extend([pos for i in range(len([position for (position, result) in pastPositions if position == pos and result > 0]))])
            return chosenAction(enemy, defenders, weightedPos[random.randrange(0, len(weightedPos))])
        try:
            return chosenAction(enemy, defenders)
        except TypeError:
            chosenAction = copy.deepcopy(chosenAction)
            chosenAction.attacker = enemy
            chosenAction.defenders = defenders
            return chosenAction
    #We may wish to add additional difficulties in the future.
    elif get_difficulty() == STRAP:
        defenders = []
        activeCompanions = [comp for comp in companions if comp.current_health() > 0]
        activeOpponents = [opp for opp in opponents if opp.current_health() > 0]
        if chosenAction == combatAction.ThrowAction:
            defenders.append(enemy.grapplingPartner)
            activeOpponents = [opp for opp in activeOpponents if opp != enemy.grapplingPartner]
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
                    defendTargets.extend([companion for statName in companion.status_names() if statusEffects.is_negative(companion.get_status(statName))])
                    #We want to defend the magic users above all else.
                    defendTargets.extend([companion for i in range(max(0, companion.magic()) // 3)])
                    defendTargets.extend([companion for i in range(companion.health() - companion.current_health()) if companion.current_health() <= avg_damage(opponents)])
                if len(defendTargets) > 0:
                    defenders.append(defendTargets[random.randrange(0, len(defendTargets))])    
                else:
                    defenders.append(enemy)
        else:
            #The code above for weighting the spells, and spankings, guarantees that this list will not be empty, assuming that the only actions that inflict statuses 
            #are spells, spankings, and defend.
            if hasattr(chosenAction, 'statusInflicted'):
                activeOpponents = [opp for opp in activeOpponents if not opp.is_inflicted_with(statusEffects.get_name(chosenAction.statusInflicted))] 
            assert(activeOpponents != [])
            for i in range(chosenAction.numTargets):
                defenders.append(activeOpponents.pop(random.randrange(0, len(activeOpponents))))
                if activeOpponents == []:
                    break
        if chosenAction == combatAction.SpankAction:
            posDifficulty = [pos.difficulty + pos.reversability - pos.maintainability for pos in enemy.spankingPositions]
            posAndDiff = zip(enemy.spankingPositions, posDifficulty)
            minDiff = 9000
            easiestPos = 0
            for pos, difficulty in posAndDiff:
                if difficulty < minDiff:
                    minDiff = difficulty
                    easiestPos = pos
            weightedPos = [easiestPos]
            for pos, difficulty in posAndDiff:
                weightedPos.extend([pos for i in range(min(0, enemy.grapple() - difficulty))]) 
            return chosenAction(enemy, defenders, weightedPos[random.randrange(0, len(weightedPos))])
        else:
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
            for attacker in filter(lambda x : x in opponents, actionsInflicted.keys()):
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
    targets = [opp for opp in opponents if opp.current_health() > 0] if chosenAction.targetType == combatAction.ENEMY else \
              [comp for comp in companions if comp.current_health() > 0]
    try:
        if chosenAction.combatType == combatAction.GrappleAction.actionType or chosenAction.combatType == combatAction.BreakAllysGrappleAction.combatType:
            targets = [t for t in targets if not chosenActions_have_target_action(chosenAction, t)]
    except AttributeError:
        pass
    if targets == []:
        return []
    isCombat = isinstance(chosenAction, person.Combat) or isinstance(chosenAction, combatAction.AttackAction) or isinstance(chosenAction, combatAction.ThrowAction)
    isStatus = isinstance(chosenAction, person.Status)
    isHealing = isinstance(chosenAction, person.Buff)
    isBuff = isinstance(chosenAction, person.Buff) and not isHealing
    isSpectral = isinstance(chosenAction, person.Spectral)
    targetsEndured = {key:actionPair for (key, actionPair) in actionsEndured.iteritems() if key in targets}
    if enemy.is_grappling() and (chosenAction.targetType == combatAction.GRAPPLER_ONLY or chosenAction.targetType == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY):
        return [enemy.grapplingPartner] if chosenAction.targetType == combatAction.ENEMY else [enemy]
    if chosenAction == combatAction.DefendAction:
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
    elif chosenAction == combatAction.SpankAction:
        return [enemy.grapplingPartner]
    elif chosenAction == combatAction.GrappleAction:
        targets = [target for target in targets if not target.is_grappling()]
        for target in targets:
            targets.extend([target for i in range(0, len([effect for (action, effect) in actionsEndured[target] if action == combatAction.GrappleAction]))])
    elif chosenAction == combatAction.BreakGrappleAction:
        return [enemy.grapplingPartner]
    elif chosenAction == combatAction.BreakAllysGrappleAction:
        targets = [target for target in targets if target.is_grappling() and target.grapple() < enemy.grapple()]
        for target in list(targets):
            #The idea here that if this character has a much higher grapple than his ally, then not only is this character good for breaking a grapple, but 
            #it's likely that his ally has a low grapple, in which case the ally needs all the help he can get.
            targets.extend([target for i in range(enemy.grapple() - target.grapple())])
    elif isCombat:
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
            targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted) and (target.is_specialized_in(person.ATTACKING) or 
                target.is_specialized_in(person.GRAPPLING) or target.is_specialized_in(person.BALANCED))]
        elif chosenAction.effectClass == combatAction.SPELL_SLINGERS:
            targets = [target for target in targets if not target.is_inflicted_with(chosenAction.statusInflicted) and (target.is_specialized_in_magic() or 
                target.is_specialized_in(person.BALANCED))]
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
    elif chosenAction == combatAction.DefendAction:
        targets.append(enemy)
        for target in list(targets):
            #We want to defend the magic users above all else.
            targets.extend([target for i in range(max(0, target.magic()) // 3)])
            targets.extend([target for i in range(target.health() - companion.current_health()) if target.current_health() <= max_damage(opponents)])
        if len(defendTargets) > 0:
            defenders.append(defendTargets[random.randrange(0, len(defendTargets))])    
        else:
            defenders.append(enemy)
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
    print('calling weight_healing')
    print(actionClass)
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
    print('done weighting for healing.')
    print(actionClass)
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
            actEndured = [action for action in actionsEndured[comp] if isinstance(combatAction.executed_action(action), type(chosenAction))]
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
RANDOM_ORDER_MULTIPLIER = 2
def start_round(chosenActions):
    global actionResults, resultIndex, delay
    delay = COMBAT_DELAY
    actionResults = []
    resultIndex = 0
    #First, we shuffle the actions.
    #We order the actions based on the stat that each action depends on. For example, a character with a high warfare attacking is going to go first than a character with
    #a low grapple who is grappling. Because we shuffled the actions first, there's no guarantee on who goes first if two characters have the same values for the 
    #primary stat of their action.
    defendActions = [action for action in chosenActions if isinstance(action, combatAction.DefendAction)]
    nonDefendActions = [action for action in chosenActions if action not in defendActions]
    random.shuffle(nonDefendActions)
    #nonDefendActions.sort(key=lambda x : x.attacker.stat(x.primaryStat) + random.randrange(0, RANDOM_ORDER_MULTIPLIER))
    #We push all the defend actions to the beginning, so that every defending character is guaranteed to defend at the beginning.
    chosenActions = defendActions + sorted(nonDefendActions, key=lambda x : x.attacker.stat(x.primaryStat) + random.randrange(0, RANDOM_ORDER_MULTIPLIER), reverse=True) 
    for action in chosenActions:
        activeAllies = [ally for ally in allies if ally.current_health() > 0]
        activeEnemies = [enemy for enemy in enemies if enemy.current_health() > 0]
        if len(activeAllies) == 0 or len(activeEnemies) == 0:
            break
        attacker = action.attacker
        if attacker in activeAllies or attacker in activeEnemies:
            if attacker.is_grappling() and action.grappleStatus == combatAction.GRAPPLER_ONLY or action.grappleStatus == combatAction.ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY:
                action.defenders = [attacker.grapplingPartner]
            elif attacker.is_grappling() and action.grappleStatus == combatAction.NOT_WHEN_GRAPPLED:
                action = combatAction.DefendAction(attacker, [attacker])
            actionEffect = action.effect(inCombat=True, allies=activeAllies, enemies=activeEnemies)
            count = 0
            print(action)
            if actionEffect[combatAction.ACTION].actionType == combatAction.RunAction.actionType and actionEffect[1][0]:
                end_combat()
                return
            else:
                try:    
                    actionsInflicted[action.attacker].append((combatAction.executed_action(actionEffect), combatAction.effects(actionEffect)))
                except KeyError, e:
                    print(actionsInflicted)
                    raise KeyError(str(e))
                defenders = combatAction.executed_action(actionEffect).defenders
                attacker = combatAction.executed_action(actionEffect).attacker
                for defender, effect in zip(defenders, combatAction.effects(actionEffect)):
                    if defender is not None:
                        actionsEndured[defender].append((combatAction.executed_action(actionEffect), effect))
                        if defender.current_health() <= 0:
                            defender.break_grapple()
                    if not (action.attacker, action.defenders, combatAction.result_string(actionEffect), 
                        isinstance(combatAction.executed_action(actionEffect), combatAction.SpankAction) or 
                        isinstance(combatAction.executed_action(actionEffect), person.SpectralSpanking)) in actionResults:
                            actionResults.append((action.attacker, action.defenders, combatAction.result_string(actionEffect), 
                                isinstance(combatAction.executed_action(actionEffect), combatAction.SpankAction) or 
                                isinstance(combatAction.executed_action(actionEffect), person.SpectralSpanking)))
    print_round_results()

resultIndex = 0
COMBAT_DELAY = 1000
delay = COMBAT_DELAY
def print_round_results():
    set_commands([('None')])
    global resultIndex
    if resultIndex == len(actionResults):
        end_round()
    else:
        actionResult = actionResults[resultIndex]
        say_title('Combat!')
        actionResultSplit = [actionResult[2]] if actionResult[3] else actionResult[2].split('\n')
        for result in actionResultSplit:
            if result.strip() == '':
                continue
            print('result: ' + result)
            if actionResult[3]:
                say_delay(result + "\n", overwritePrevious=True)
            else:
                say_delay(result + "\n", overwritePrevious=False)
            if len(actionResultSplit) > 1 and actionResultSplit[-1] != result:
                pass
                for i in range(0, 5):
                    delaySplit = delay // 5
                    pygame.time.delay(delaySplit)
        resultIndex += 1
        if actionResult[3]:
        #If the action is a spanking, then we need to give the player plenty of time to enjoy it. 
            acknowledge(print_round_results, ())
            #print_round_results()
        else:
            for i in range(0, 5):
            #This is so that we can respond faster to the user pressing the enter key. 
                delaySplit = delay // 5
                pygame.time.delay(delaySplit)
            print_round_results()

defeatedAllies = []
defeatedEnemies = []
def end_round():
    global allies, enemies, chosenActions, actionResults, defeatedAllies, defeatedEnemies
    activeAllies = [ally for ally in allies if ally.current_health() > 0]
    defeatedAllies.extend([ally for ally in allies if ally.current_health() <= 0])
    allies = person.Party(activeAllies)
    activeEnemies = [enemy for enemy in enemies if enemy.current_health() > 0]
    defeatedEnemies.extend([enemy for enemy in enemies if enemy.current_health() <= 0])
    enemies = person.Party(activeEnemies)
    for ally in activeAllies:
        ally.decrement_statuses()
    for enemy in activeEnemies:
        enemy.decrement_statuses()
    if len(activeAllies) == 0 : game_over()
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
    universal.say('You have been defeated! Would you like to try again? (Y/N)\n\n')
    if optional:
        universal.say('Note that winning this fight is optional. Saying "no" will NOT give you a game over.')
    else:
        universal.say('Note that you need to win this fight to continue the game. If you say "no" you will return to the title screen.')
    set_commands(['(Y)es', '(N)o'])
    set_command_interpreter(game_over_interpreter)

def game_over_interpreter(keyEvent):
    if keyEvent.key == K_y:
        global allies, enemies, chosenActions, actionResults, actionsEndured, actionsInflicted, defeatedAllies, defeatedEnemies, origEnemies, origAllies
        enemies.members += defeatedEnemies
        allies.members += defeatedAllies
        defeatedAllies = []
        defeatedEnemies = []
        enemies = person.Party(copy.deepcopy(origEnemies))
        #enemies[i].set_state(origEnemies[i])
        #allies[i].set_state(origAllies[i])
        allies = person.Party(copy.deepcopy(origAllies))
        person.set_party(allies)
        for i in range(len(allies)):
            allies[i].chanceIncrease = [0 for j in range(len(allies[i].chanceIncrease))]
        chosenActions = []
        actionResults = []
        print('allies and enemies:')
        print(allies)
        print(enemies)
        print(allies + enemies)
        actionsEndured = {combatant:[] for combatant in enemies + allies}
        actionsInflicted = {combatant:[] for combatant in enemies + allies}
        print('actionsEndured : ' + str(actionsEndured))
        print('actionsInflicted : ' + str(actionsInflicted))
        display_combat_status()
        global activeAlly
        activeAlly = allies[0]
        if boss:
            music.play_music(music.BOSS)
        else:
            music.play_music(music.COMBAT)
    elif keyEvent.key == K_n:
        if optional:
            print(allies.members)
            print([ally for ally in allies if ally.current_health() <= 0])
            print(enemies.members)
            print([enemy for enemy in enemies if enemy.current_health() <= 0])
            afterCombatEvent([ally for ally in allies if ally.current_health() <= 0] + defeatedAllies, 
                    [enemy for enemy in enemies if enemy.current_health() <= 0] + defeatedEnemies, False)
            allies.members += defeatedAllies    
        else:
            end_fight()
            titleScreen.title_screen()
        return


def victory():
    """
    Note: If there is an afterCombatEvent, then that function will have to transtition the player into the appropriate mode. We can't do it here, because the 
    after combat event may require player input, in which case the game would immediately go into the previous mode before the player can actually give any input to the
    after combat event.
    """
    clear_screen()
    global allies, defeatedAllies, enemies, defeatedEnemies
    allies.members += defeatedAllies
    enemies.members += defeatedEnemies
    activeAllies = [ally for ally in allies if ally.current_health() > 0]
    activeEnemies = [enemy for enemy in enemies if enemy.current_health() > 0]
    for enemy in enemies:
        enemy.restores()
    clear_screen()
    say_title('Victory!')
    universal.say(format_line([person.PC.name, 'has defeated', person.hisher(), 'enemies.\n']))
    music.play_music(music.VICTORY)
    for ally in allies:
        ally.break_grapple()
    improve_characters(afterCombatEvent, activeAllies, activeEnemies, True)
    end_fight()
    """
    global enemies, chosenActions, actionResults, actionsEndured, actionsInflicted
    enemies = person.Party(origEnemies)
    enemies.add_member(enemies.members.pop().reset_stats())
    chosenActions = []
    actionResults = []
    actionsEndured = {combatant:[] for combatant in enemies + allies}
    actionsInflicted = {combatant:[] for combatant in enemies + allies}
    display_combat_status()
    """

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

HIGH_STAT_PENALTY = .25
def improve_characters(afterCombatEvent, activeAllies, activeEnemies, victorious):
    """
    Takes as argument the function that should be invoked after leveling up is complete.
    """
    experience = []
    #for i in range(len(enemies)):
        #print(enemies[i].statList)
    maxStats = [max([enemy.get_stat(i) for enemy in enemies]) for i in range(person.NUM_STATS)]
    #print(maxStats)
    for ally in allies:
        #print('chanceIncrease for ' + ally.name)
        #print(ally.chanceIncrease)
        ally.chanceIncrease[HEALTH] += 25 + max(ally.chanceIncrease[WARFARE], ally.chanceIncrease[GRAPPLE]) // 2
        ally.chanceIncrease[MANA] += 25 + ally.chanceIncrease[MAGIC] // 2
        ally.chanceIncrease[STEALTH] += 5
        for i in range(len(ally.chanceIncrease)):
        #We give a bonus 20% bonus to increasing the stat for every 5 points that a character is below the enemy' stat. This allows characters to more easily
        #climb out of a hole. Note that you do need to use an action that relies on this stat at least once for the benefit to be of use.
            if i < COMBAT_MAGIC:
                ally.chanceIncrease[i] += (20 * ((maxStats[i] - ally.get_stat(i)) // 5)) if ally.chanceIncrease[i] > 0 and maxStats[i] > ally.get_stat(i) else 0 
                ally.chanceIncrease[i] = ally.apply_specialization(i, ally.chanceIncrease[i])
                if ally.get_stat(i) >= maxStats[i] + specialization_bonus(ally, i):
                    ally.chanceIncrease[i] *= HIGH_STAT_PENALTY
                #print('chanceIncrease for ' + ally.name + ' after end of combat bonuses.') 
                #print(ally.chanceIncrease)
            try:
                print('stat:' + person.stat_name(i)) 
                print(ally.chanceIncrease[i])
            except TypeError:
                print('spell school: ' + str(i))
            #If your character already has a significantly higher stat than your opponent, the chances of increasing that stat drop off drastically
            statChance = ally.chanceIncrease[i] + (100 if universal.DEBUG else 0)
            #print('chance to increase:' + str(statChance))
            success = random.randint(1, 100)
            #print('success:' + str(success))
            #print(success <= statChance)
            gainedPoint = False
            print('success:' + str(success))
            print('statChance: ' + str(statChance))
            if success <= statChance:
                if i < COMBAT_MAGIC:
                    #print(maxStats[i])
                    #print(ally.get_stat(i))
                    #print(specialization_bonus(ally, i))
                    gainedPoint = True
                    print('increasing stat: ' + person.stat_name(i))
                    gain = 1
                    if i != HEALTH and i != MANA and i != CURRENT_HEALTH and i != CURRENT_MANA:
                        ally.increase_stat(i, 1)
                    elif i != CURRENT_HEALTH and i != CURRENT_MANA:
                        gain = random.randint(1, 10)    
                        print(ally)
                        print(person.PC)
                        ally.improve_stat(i, gain)
                    if i != CURRENT_HEALTH and i != CURRENT_MANA:
                        universal.say(format_line([ally.name, 'has gained', str(gain), person.stat_name(i) + '.\n']))
                else:
                    #print('learning a spell.')
                    learn_spell(ally, i)
    if afterCombatEvent is not None:
        acknowledge(afterCombatEvent, defeatedAllies, defeatedEnemies, victorious)
    else:
        acknowledge(previousMode)

def learn_spell(ally, spellSchool):
    spellIndex = person.get_spell_index(spellSchool)
    unknownSpells = []
    for i in range(0, ally.tier+1):
        #Need to learn basic before you can learn advanced before you can learn specialized. Can only learn specialized if you are specialized in this particular type of
        #magic.
        #print('spell information')
        #print(person.allSpells)
        #print(i)
        #print(spellIndex)
        #print(ally.tier)
        print(i)
        try:
            if not ally.knows_spell(person.allSpells[i][spellIndex][0]):
                #We weight the spells based on their tier level. Spells that have tier 0 have 1 weight, spells of tier 1 have 2 weight and so on. This increases the chances
                #of a character learning a more powerful spell sooner.
                unknownSpells.append(person.allSpells[i][spellIndex][0])    
            elif not ally.knows_spell(person.allSpells[i][spellIndex][1]):
                unknownSpells.append(person.allSpells[i][spellIndex][1])    
            elif ally.specialization == spellSchool and not ally.knows_spell(Person.allSpells[i][spellIndex][2]):
                unknownSpells.append(person.allSpells[i][spellIndex][2])    
        except TypeError:
            continue
    if len(unknownSpells) > 0:
        learnedSpell = unknownSpells[random.randint(0, len(unknownSpells)-1)]
        ally.learn_spell(learnedSpell)
        universal.say(format_line([ally.name, 'has learned the spell', learnedSpell.name + '!\n']))
        

""" 
def add_experience(experience, afterCombatEvent, activeAllies, activeEnemies, victorious):
    #print('calling add_experience')
    assert len(allies) == len(experience), 'allies and experience should be the same length.'
    for i in range(len(experience) - 1):
        print('adding experience to: ' + str(i) + " ally.")
        allies[i].add_experience(experience[i])
    if afterCombatEvent is None:
        afterCombatEvent = previousMode
    print('adding experience to last ally.')
    allies[-1].add_experience(experience[-1], afterCombatEvent, activeAllies, activeEnemies, victorious)
"""


def print_round_results_interpreter(keyEvent):
    if keyEvent.key == K_RETURN:
        global delay
        delay = 0
