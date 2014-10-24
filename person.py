""" Copyright 2014 Andrew Russell 

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
import statusEffects
import combatAction
import random
import abc
import episode
import items
import conversation
import operator
from combatAction import GRAPPLER_ONLY, ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY, ONLY_WHEN_GRAPPLED, UNAFFECTED, NOT_WHEN_GRAPPLED, WARRIORS_GRAPPLERS, SPELL_SLINGERS, ALL, ALLY, ENEMY
import inspect
import copy

checkWillpower = True


def flip_willpower_check():
    global checkWillpower
    checkWillpower = not checkWillpower

def set_willpower_check(willpower):
    global checkWillpower
    checkWillpower = willpower > 0


def get_willpower_check():
    return 1 if checkWillpower else 0

"""
COMBAT_MAGIC = 0
BUFF_MAGIC = 1
STATUS_MAGIC = 2
SPECTRAL_MAGIC = 3
ATTACKING = 4
GRAPPLING = 5
BALANCED = 6
"""

TALENT_PER_TIER = 10

allStats = [universal.WARFARE, universal.MAGIC, universal.RESILIENCE, universal.GRAPPLE, universal.STEALTH, universal.HEALTH, universal.MANA, universal.CURRENT_HEALTH, 
        universal.CURRENT_MANA]

allPrimaryStats = [universal.STRENGTH, universal.DEXTERITY, universal.WILLPOWER, universal.TALENT, universal.ALERTNESS, universal.HEALTH, universal.MANA, 
        universal.CURRENT_HEALTH, universal.CURRENT_MANA]

MALE = 0
FEMALE = 1

HEALTH_SCALE = 5
MANA_SCALE = 5

XP_INCREASE_PER_LEVEL = 100

STATUS_OBJ = 0
DURATION = 1
#This is used for saving purposes

def remove_character(person):
    if person.name in universal.state.characters:
        universal.state.characters.remove(person)

universal.state.player = universal.state.player

def get_PC():
    return universal.state.player

def set_PC(playerCharacter):
    universal.state.player = playerCharacter

class InvalidEquipmentError(Exception):
    pass

def stat_name(stat):
    if stat == universal.WARFARE:
        return 'warfare'    
    elif stat == universal.MAGIC:
        return 'magic'
    elif stat == universal.RESILIENCE:
        return 'resilience()'
    elif stat == universal.GRAPPLE:
        return 'grapple'
    elif stat == universal.STEALTH:
        return 'stealth'
    elif stat == universal.HEALTH:
        return 'health'
    elif stat == universal.MANA:
        return 'mana'
    elif stat == universal.CURRENT_HEALTH:
        return 'current health'
    elif stat == universal.CURRENT_MANA:
        return 'current mana'

WEAPON = 0
SHIRT = 1
LOWER_CLOTHING = 2
UNDERWEAR = 3
PAJAMA_TOP = 4
PAJAMA_BOTTOM = 5
NUM_EQUIP_SLOTS = 6
def slot_Name(slot):
    if slot == WEAPON:
        return 'weapon'
    elif slot == SHIRT:
        return 'shirt'
    elif slot == LOWER_CLOTHING:
        return 'lower clothing'
    elif slot == UNDERWEAR:
        return 'underwear'



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

def zeroth_order(unleasher, allies, enemies):
    return ''

def first_order(unleasher, allies, enemies):
    secondOrderEnemies = [enemy for enemy in enemies if enemy.order == second_order]
    if secondOrderEnemies == []:
        for enemy in enemies:
            enemy.inflict_status(statusEffects.build_status(statusEffects.FIRST_ORDER))
        return ' '.join([unleasher.printedName, 'unleashes the First Order.\n\n'])
    else:
        return ' '.join([unleasher.printedName + "'s", 'Order has been blocked.\n\n'])

def second_order(unleasher, allies, enemies):
    firstOrderEnemies = [enemy for enemy in enemies if enemy.order == first_order]
    if firstOrderEnemies == []:
        for ally in allies:
            #print('ally stats before second_order:' + str(ally.statList))
            ally.inflict_status(statusEffects.build_status(statusEffects.SECOND_ORDER))
            #print('ally stats after second_order:' + str(ally.statList))
        return ' '.join([unleasher.printedName, 'unleashes the Second Order.\n\n'])
    else:
        return ' '.join([unleasher.printedName + "'s", 'Order has been blocked.\n\n'])

def third_order(unleasher, allies, enemies):
    fourthOrderEnemies = [enemy for enemy in enemies if enemy.order == fourth_order]
    if fourthOrderEnemies == []:
        for ally in allies:
            ally.inflict_status(statusEffects.build_status(statusEffects.THIRD_ORDER))
        return ' '.join([unleasher.printedName, 'unleashes the Third Order.\n\n'])
    else:
        return ' '.join([unleasher.printedName + "'s", 'Order has been blocked.\n\n'])


def fourth_order(unleasher, allies, enemies):
    thirdOrderEnemies = [enemy for enemy in enemies if enemy.order == third_order]
    if thirdOrderEnemies == []:
        for ally in allies:
            ally.inflict_status(statusEffects.build_status(statusEffects.FOURTH_ORDER))
        return ' '.join([unleasher.printedName, 'unleashes the Fourth Order.\n\n'])
    else:
        return ' '.join([unleasher.printedName + "'s", 'Order has been blocked.\n\n'])


def fifth_order(unleasher, allies, enemies):
    sixthOrderEnemies = [enemy for enemy in enemies if enemy.order == sixth_order]
    if sixthOrderEnemies == []:
        for enemy in enemies:
            enemy.receives_damage(enemy.current_health() // 2)
            enemy.uses_mana(enemy.current_mana() // 2)
        return ' '.join([unleasher.printedName, 'unleashes the Fifth Order.\n\n'])
    else:
        return ' '.join([unleasher.printedName + "'s", 'Order has been blocked.\n\n'])

def sixth_order(unleasher, allies, enemies):
    fifthOrderEnemies = [enemy for enemy in enemies if enemy.order == fifth_order]
    if fifthOrderEnemies == []:
        for ally in allies:
            ally.heals(ally.health())
            ally.restores_mana(ally.mana())
        return ' '.join([unleasher.printedName, 'unleashes the Sixth Order.\n\n'])
    else:
        return ' '.join([unleasher.printedName + "'s", 'Order has been blocked.\n\n'])


def order_function(name):
    """
    Inverse of order_name
    """
    if name == '0':
        return zeroth_order
    elif name == '1':
        return first_order
    elif name == '2':
        return second_order
    elif name == '3':
        return third_order
    elif name == '4':
        return fourth_order
    elif name == '5':
        return fifth_order
    elif name == '6':
        return sixth_order

def order_name(order):
    """
    Inverse of order_function
    """
    if order == zeroth_order:
        return str(0)
    elif order == first_order:
        return str(1)
    elif order == second_order:
        return str(2)
    elif order == third_order:
        return str(3)
    elif order == fourth_order:
        return str(4)
    elif order == fifth_order:
        return str(5)
    elif order == sixth_order:
        return str(6)


def display_person(person):
    if person is None:
        return ' '
    else:
        return person.printedName

BODY_TYPES = ['slim', 'average', 'voluptuous', 'heavyset']


HEIGHTS = ['short', 'average', 'tall', 'huge']


MUSCULATURE = ['soft', 'fit', 'muscular']


HAIR_LENGTH = ['short', 'shoulder-length', 'back-length', 'butt-length']

SHORT_HAIR_STYLE = ['down']
SHOULDER_HAIR_STYLE = SHORT_HAIR_STYLE + ['ponytail', 'braid', 'pigtails', 'bun']
BACK_HAIR_STYLE = SHOULDER_HAIR_STYLE
BUTT_HAIR_STYLE = BACK_HAIR_STYLE


def compute_stat(stat, primaryStats):
    if stat == WARFARE:
        return 2 * primaryStats[universal.STRENGTH] + primaryStats[universal.DEXTERITY]
    elif stat == GRAPPLE:
        return 2 * primaryStats[universal.DEXTERITY] + primaryStats[universal.STRENGTH]
    elif stat == RESILIENCE:
        return 2 * primaryStats[universal.WILLPOWER] + primaryStats[universal.TALENT]
    elif stat == STEALTH:
        return 2 * ALERTNESS
    

class Person(universal.RPGObject): 
    """
        People are complicated.
    """
    def __init__(self, name, gender, defaultLitany, litany, description="", printedName=None, 
            coins=20, specialization=universal.BALANCED, order=zeroth_order, dropChance=0, rawName=None, skinColor='', eyeColor='', hairColor='', hairStyle='', marks=None,
            musculature='', hairLength='', height='', bodyType='', identifier=None): 
        self.name = name
        self.gender = gender
        self.previousTarget = 0
        if type(description) is list:
            print("Found a list!")
            print(description)
            self.description = '\n'.join(description)
        else:
            self.description = description
        print(self.name)
        assert(not isinstance(self.description, list))
        #A mapping from the name of the status, to the actual status, and the duration.     
        self.statusList = {}
        if rawName is None:
            self.rawName = name
        else:
            self.rawName = rawName
        self.spellList = [None for i in range(universal.NUM_TIERS)]
        self.numSmacks = 0
        self.grapplingPartner = None
        self.inventory = []
        self.equipmentList = [None for i in range(NUM_EQUIP_SLOTS)]
        self.equipmentList[WEAPON] = items.emptyWeapon
        self.equipmentList[SHIRT] = items.emptyUpperArmor
        self.equipmentList[LOWER_CLOTHING] = items.emptyLowerArmor
        self.equipmentList[UNDERWEAR] = items.emptyUnderwear
        self.equipmentList[PAJAMA_TOP] = items.emptyPajamaTop
        self.equipmentList[PAJAMA_BOTTOM] = items.emptyPajamaBottom
        self.primaryStats = [1 for i in range(len(allPrimaryStats))]
        #self.statList = [compute_stat(stat, self.primaryStats) for i in range(len(allStats))]
        self.set_default_stats()
        self.level = 1
        self.tier = 0
        self.experience = 0
        self.spellPoints = 3
        self.specialization = None
        self.ignoredSpells = []
        self.spankingPositions = []
        self.combatType = None
        self.litany = litany
        self.defaultLitany = defaultLitany
        self.coins = coins
        self.specialization = specialization
        self.order = order
        #Last four indices are the appropriate spell categories
        self.chanceIncrease = [0 for i in range(len(allPrimaryStats) + NUM_SPELL_CATEGORIES)]
        #We have as many quick spells as we do function keys.
        self.quickSpells = [None for i in range(12)]
        if printedName is None:
            self.printedName = name
        else:
            self.printedName = printedName
        self.emerits = 0
        self.demerits = 0
        #A person who is guarding this person.
        self.guardian = None
        #Only used for leveling up
        self.chosenStat = -1
        self.statPoints = 0
        self.availableStats = None
        self.origStats = None
        self.hairLength = hairLength
        self.bodyType = bodyType
        self.height = height
        self.musculature = musculature
        self.bumStatus = 0
        self.welts = []
        self.skinColor = skinColor
        self.hairColor = hairColor
        self.eyeColor = eyeColor
        self.hairStyle = hairStyle
        self.mainStatDisplay = True
        if marks is None:
            self.marks = []
        else:
            self.marks = marks
        self.identifier = identifier
        universal.state.add_character(self)

    def __getstate__(self):
        state = self.__dict__.copy()
        known_spells = [[] for i in range(universal.NUM_TIERS)]
        #print(self)
        #print("'s spell list!")
        #print(self.spellList)
        state['spellList'] = [[(allSpells[tier].index((get_basic_spell(tier, action_type_to_spell_type(spell.actionType)), 
            get_advanced_spell(tier, action_type_to_spell_type(spell.actionType)), get_expert_spell(tier, action_type_to_spell_type(spell.actionType)))), spell.expertise) 
            for spell in self.spellList[tier]] for tier in range(len(self.spellList)) if self.spellList[tier] is not None]
        quickSpellList = []
        for spell in state['quickSpells']:
            try:
                quickSpellList.append(spell.name)
            except AttributeError:
                pass
        state['quickSpells'] = quickSpellList
        #print("state's spell list!")
        #print(state['spellList'])
        return state

    def __setstate__(self, state):
        #import traceback
        #print(traceback.print_stack())
        #print(state['spellList'])
        state['spellList'] = [[allSpells[tier][index][expertise] for (index, expertise) in state['spellList'][tier]] for tier in range(len(state['spellList']))]
        state['spellList'].extend([None for i in range(universal.NUM_TIERS - len(state['spellList']))])
        state['quickSpells'] = [get_spell(name) for name in state['quickSpells']]
        while len(state['quickSpells']) < 12:
            state['quickSpells'].append(None)

        #While writing text for episode 2, I realized that I should have a separate object for DropSeatPajamas. The following code is a bit of a patch in order to ensure that
        #people who have the drop seat pajamas have an object of the correct type, even if they're loading a save from before I changed the type of the drop seat pajamas (note that there was
        #only one type of drop seat pajama before I made the change. 
        try:
            import itemspotionwars
        except ImportError:
            pass
        else:
            pajamaTop = state['equipmentList'][PAJAMA_TOP]
            if pajamaTop.name == itemspotionwars.dropSeatPJs.name and pajamaTop.armorType != items.DropSeatPajamas.armorType:
                state['equipmentList'][PAJAMA_TOP] = items.DropSeatPajamas(pajamaTop.name, pajamaTop.description, pajamaTop.price)
                state['equipmentList'][PAJAMA_BOTTOM] = state['equipmentList'][PAJAMA_TOP]
                        
        self.__dict__.update(state)
        assert(self.spellList != [])
        #print('done settingt state!')
        #print(self.spellList)
        #print(self)
        self.spellList = state['spellList']


    def add_quick_spell(self, spell):
        try:
            self.quickSpells[self.quickSpells.index(None)] = spell
        except ValueError:
            pass

    def set_quick_spell(self, spell, index):
        try:
            self.quickSpells[index] = spell
        except IndexError:
            return

    def swap_quick_spells(self, index1, index2):
        try:
            self.quickSpells[index1], self.quickSpells[index2] = self.quickSpells[index2], self.quickSpells[index1]
        except IndexError:
            return

    def hair_styles(self):
        if self.hairLength == 'short':
            return SHORT_HAIR_STYLE
        elif self.hairLength == 'shoulder-length':
            return SHOULDER_HAIR_STYLE
        elif self.hairLength == 'back-length':
            return BACK_HAIR_STYLE
        elif self.hairLength == 'butt-length':
            return BUTT_HAIR_STYLE

    def risque(self):
        risqueLevel = sum(equipment.risque for equipment in self.equipmentList if not isinstance(equipment, items.Weapon))
        #If the lower clothing isn't baring, then we can't see the underwear, so its risque level doesn't matter.
        if not self.lower_clothing().baring:
            risqueLevel -= self.underwear().risque

    def _set_weapon(self, weapon):
        self.equipmentList[WEAPON] = weapon

    def _set_shirt(self, shirt):
        self.equipmentList[SHIRT] = shirt

    def _set_lower_clothing(self, lowerClothing):
        self.equipmentList[LOWER_CLOTHING] = lowerClothing

    def _set_underwear(self, underwear):
        self.equipmentList[UNDERWEAR] = underwear

    def _set_pajama_top(self, pajamaTop):
        self.equipmentList[PAJAMA_TOP] = pajamaTop

    def _set_pajama_bottom(self, pajamaBottom):
        self.equipmentList[PAJAMA_BOTTOM] = pajamaBottom

    def bum_adj(self):
        if self.bodyType == 'slim':
            adjList = ['small', 'petite', 'heart-shaped']
        elif self.bodyType == 'average':
            adjList = ['plump', 'round', 'curved']
        elif self.bodyType == 'voluptuous':
            adjList = ['ample', 'curvaceous', 'large']
        elif self.bodyType == 'heavyset':
            adjList = ['fleshy', 'wide', 'expansive']
        return random.choice(adjList)

    def quiver(self):
        if self.musculature == 'soft':
            adjList = ['ripple', 'jump', 'flatten']
        elif self.musculature == 'fit':
            adjList = ['spasm', 'bounce', 'shake']
        elif self.musculature == 'muscular':
            adjList = ['quiver', 'bob', 'shiver']

    def quivering(self):
        if self.musculature == 'soft':
            adjList = ['rippling', 'jumping', 'flattening']
        elif self.musculature == 'fit':
            adjList = ['spasming', 'bouncing', 'shaking']
        elif self.musculature == 'muscular':
            adjList = ['quivering', 'bobbing', 'shivering']

    def is_slim(self):
        return self.bodyType == 'slim'

    def is_average(self):
        return self.bodyType == 'average'

    def is_heavyset(self):
        return self.bodyType == 'heavyset'

    def muscle_adj(self):
        if self.musculature == 'soft':
            adjList = ['jiggly', 'wobbly', 'pillowy']
        elif self.musculature == 'fit':
            adjList = ['firm', 'toned', 'bouncy']
        elif self.musculature == 'muscular':
            adjList = ['hard', 'solid', 'muscular']
        return random.choice(adjList)

    def is_fit(self):
        return self.musculature == 'fit'
    def is_soft(self):
        return self.musculature == 'soft'
    def is_muscular(self):
        return self.musculature == 'muscular'
    
    #HEIGHTS = ['short', 'average', 'tall', 'huge']
    #Height dimensions:
    #short: 5' - 5'4"
    #average: 5' 5" - 5' 9"
    #tall : 5' 10" - 6'"
    #huge : over 6'

    def is_average_or_shorter(self):
        return HEIGHTS.index(self.height) <= HEIGHTS.index('average')

    def is_short(self):
        return HEIGHTS.index(self.height) <= HEIGHTS.index('short')

    def is_tall_or_shorter(self):
        return HEIGHTS.index(self.height) <= HEIGHTS.index('tall')

    def is_huge_or_shorter(self):
        return HEIGHTS.index(self.height) <= HEIGHTS.index('huge')

    def is_short(self):
        return self.height == 'short'

    def is_average(self):
        return self.height == 'average'

    def is_tall(self):
        return self.height == 'tall'

    def is_huge(self):
        return self.height == 'huge'

    def is_short_or_taller(self):
        return self.is_short() or self.is_average() or self.is_tall() or self.is_huge()

    def is_average_or_taller(self):
        return self.is_average() or self.is_tall() or self.is_huge()

    def is_tall_or_taller(self):
        return self.is_tall() or self.is_huge()

    def is_huge_or_taller(self):
        return self.is_huge()


    def dwarfs(self, char):
        return HEIGHTS.index(self.height) - HEIGHTS.index(char.height) >= 3

    def towers_over(self, char):
        return HEIGHTS.index(self.height) - HEIGHTS.index(char.height) >= 2

    def taller_than(self, char):
        return HEIGHTS.index(self.height) - HEIGHTS.index(char.height) >= 1

    def dwarfed_by(self, char):
        return -(HEIGHTS.index(self.height) - HEIGHTS.index(char.height)) >= 3

    def towered_over_by(self, char):
        return - (HEIGHTS.index(self.height) - HEIGHTS.index(char.height)) >= 2

    def shorter_than(self, char):
        return - (HEIGHTS.index(self.height) - HEIGHTS.index(char.height)) >= 1



    #HAIR_LENGTH = ['short', 'shoulder-length', 'back-length', 'butt-length']
    def short_hair(self):
        return self.hairLength == 'short'

    def long_hair(self):
        return self.shoulder_hair() or self.back_hair() or self.butt_hair()

    def shoulder_hair(self):
        return self.hairLength == 'shoulder-length'

    def back_hair(self):
        return self.hairLength == 'back-length'

    def butt_hair(self):
        return self.hairLength == 'butt-length'


    def get_core_stats(self):
        return self.primaryStats[:-2]

    def get_battle_stats(self):
        """Returns all the stats except for health, mana, current health, current mana
        """
        return self.primaryStats[:-4]

    def set_default_stats(self):
        self.set_all_stats(strength=1, dexterity=1, willpower=1, talent=1, alertness=1, health=10, mana=10)

    def set_state(self, original):
        raise NotImplementedError()
        """
        self.name = original.name
        self.gender = original.gender
        self.description = original.description
        self.statusList = original.statusList
        self.numSmacks = original.numSmacks
        self.grapplingPartner = original.grapplingPartner
        self.inventory = original.inventory
        self.equipmentList = original.equipmentList
        self.statList = original.statList
        self.level = original.level
        self.tier = original.tier
        self.experience = original.experience
        self.spellPoints = original.spellPoints
        self.specialization = original.specialization
        self.ignoredSpells = original.ignoredSpells
        self.spankingPositions = original.spankingPositions
        self.combatType = original.combatType
        self.litany = original.litany
        self.defaultLitany = original.defaultLitany
        self.coins = original.coins
        self.specialization = original.specialization
        self.printedName = original.printedName
        self.emerits = original.emerits
        self.demerits = original.demerits
        self.chosenStat = original.chosenStat
        """

    def is_bonus(self, stat):
        if stat == universal.MAGIC and (self.specialization == COMBAT_MAGIC or self.specialization == STATUS_MAGIC or self.specialization == BUFF_MAGIC or 
                self.specialization == SPECTRAL_MAGIC):
            return True
        elif self.specialization == stat:
            return True
        else:
            return False
    def is_penalty(self, stat):
        if self.specialization == universal.WARFARE and stat == universal.MAGIC:
            return True
        elif self.specialization == universal.GRAPPLE and stat == universal.RESILIENCE:
            return True
        elif self.specialization == universal.MAGIC and stat == universal.WARFARE:
            return True
        elif self.specialization == universal.RESILIENCE and stat == universal.GRAPPLE:
            return True
        elif self.specialization == universal.STEALTH and stat == universal.WARFARE:
            return True
        else:
            return False

    def apply_specialization(self, stat, statChance):
        if self.is_bonus(stat):
            return 2 * statChance
        elif self.is_penalty(stat):
            return statChance // 2
        else:
            return statChance


    def get_item(self, num):
        return (self.inventory + self.equipmentList)[num]

    def flattened_spell_list(self):
        spellList = [spells for spells in self.spellList if spells is not None]
        if spellList == []:
            return []
        else:
            return reduce(operator.concat, spellList)

    def knows_spell(self, spell):
        if isinstance(spell, Spell):
            return spell in self.flattened_spell_list()
        else:
            return [knownSpell for knownSpell in self.flattened_spell_list() if isinstance(knownSpell, spell)] != []

    def get_id(self):
        """
        Returns a string that consists of a person's name annotated with their type (in this case person). This is to ensure that id's are distinct, even if the 
        player happens to give their character the same name as another character in the game (because player characters will be appended with 'playerCharacter').
        """
        if self.identifier:
            rawName = self.rawName + str(self.identifier)
        else:
            rawName = self.rawName
        return rawName + ".person"

    def __eq__(self, other):
        """
        A very simple equality that assumes that two characters are the same iff they have the same or they have the same name. Note that this means this will not 
        work for generic enemies, or rather it would view two different instances of generic enemies as the same person.
        """
        try:
            return id(self) == id(other) or self.get_id() == other.get_id()
        except AttributeError:
            return False

    def add_mark(self, mark):
        self.marks.append(mark)

#----------------------------------------------------------------Abstract Methods---------------------------------------------------------------------
    #abstractmethod
    def had_spanking_reversed_by(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement reversed_spanking_of for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def reversed_spanking_of(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement reversed_spanking_of for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def spanked_by(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement spanked_by for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def avoided_spanking_by(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement avoided_spanking_by for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def spanks(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement spanks for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def failed_to_spank(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement failed_to_spank for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))

#-----------------------------------------------------------------End Abstract Methods--------------------------------------------------------------------------

    def take_item(self, item):
        if not item in self.inventory and not item in items.emptyEquipment:
            self.inventory.append(copy.deepcopy(item))

    def drop_item(self, item):
        if not item in self.inventory:
            self.unequip(item)
        try:
            self.inventory.remove(item)
        except ValueError:
            pass

    def set_spanking_positions(self, spankingPositions):
        self.spankingPositions = spankingPositions

    def ignores_spells(self, ignoredSpells):
        self.ignoredSpells = ignoredSpells

    def set_ignored_spells(self, ignoredSpells):
        self.set_ignored_spells = ignoredSpells

    def _set_spell_points(self, spellPoints):
        """
            This should only be used internally, by this person's level up method.
        """
        self.spellPoints = spellPoints

    def has_fighting_style(self, fightingStyle):
        self.fightingStyle = fightingStyle

    def set_fighting_style(self, fightingStyle):
        self.has_fighting_style(fightingStyle)

    def set_specialization(self, specialization):
        self.specialization = specialization

    def is_specialized_in(self, specialization):
        return self.specialization == specialization

    def is_specialized_in_magic(self):
        return (self.is_specialized_in(COMBAT_MAGIC) or self.is_specialized_in(BUFF_MAGIC) or 
                self.is_specialized_in(STATUS_MAGIC) or self.is_specialized_in(SPECTRAL_MAGIC) or self.is_specialized_in(BALANCED))
    
    def set_litany(self, litany):
        self.litany = litany

    def set_level(self, level):
        self.level = level

    def set_gender(self, genderIn):
        self.gender = genderIn

    def set_stat(self, stat, num):
        self.primaryStats[stat] = num

    def set_all_stats(self, strength=None, willpower=None, talent=None, dexterity=None, alertness=None, health=None, mana=None):
        if strength is not None:
            self.primaryStats[universal.STRENGTH] = strength
        if willpower is not None:
            self.primaryStats[universal.WILLPOWER] = willpower
        if talent is not None:
            self.primaryStats[universal.TALENT] = talent
        if dexterity is not None:
            self.primaryStats[universal.DEXTERITY] = dexterity
        if alertness is not None:
            self.primaryStats[universal.ALERTNESS] = alertness
        if health is not None:
            self.primaryStats[universal.HEALTH] = health
        if mana is not None:
            self.primaryStats[universal.MANA] = mana
        if health is not None:
            self.primaryStats[universal.CURRENT_HEALTH] = health
        if mana is not None:
            self.primaryStats[universal.CURRENT_MANA] = mana

    def increase_stat(self, stat, increment):
        self.primaryStats[stat] += increment

    def improve_stat(self, stat, increment):
        #TODO: Change how quickly a person's spell tiers increases.
        self.increase_stat(stat, increment)
        oldTier = self.tier
        self.tier = self.talent() // TALENT_PER_TIER
        if self.tier > oldTier:
            magicSchool = get_spell_index(self.specialization) if self.specialized_in_magic() else -1
            if magicSchool >= 0:
                self.learn_spell(allSpells[self.tier][magicSchool][0])
                universal.say(universal.format_line(['\n' + self.name, 'has learned the', allSpells[self.tier][magicSchool][0].name, 'spell!']))

    def reduce_stat(self, stat, increment): 
        self.decrease_stat(stat, increment)
        tier = self.magic() // TALENT_PER_TIER

    def specialized_in_magic(self):
        return self.specialization == COMBAT_MAGIC or self.specialization == STATUS_MAGIC or self.specialization == BUFF_MAGIC or self.specialization == SPECTRAL_MAGIC

    def increment_stat(self, stat):
        self.increase_stat(stat, 1)

    #def increase_all_stats(self, increment):
    #    self.set_all_stats(warfare + increment, resilience() + increment, magic + increment, grapple + increment, stealth + increment)

    #def decrease_all_stats(self, decrement):
    #    self.increase_all_stats(-decrement)


    def equip(self, equipment): 
        try:
            equipment.equip(self)
        except items.NakedError:
            universal.clear_screen()
            if isinstance(equipment, items.Pajamas):
                universal.say(format_text([[self.name, '''can't go without pajama bottoms. After all,''', heshe(self), '''needs something to cover''', hisher(self), 
                '''bottom for when''', heshe(self), '''wants to leave''', hisher(self), '''room, but doesn't want to get dressed.''']]), justification=0)
            else:
                universal.say(format_text([[self.name, '''realizes with a spike of embarassment that if''', heshe(self), '''equips''', equipment.name + ",", '''then''', 
                    heshe(self), '''will be naked from the waist down.''', HeShe(self), '''decides not to equip''', equipment.name + "."]]), justification=0)
            acknowledge(Person.character_sheet, self)
            raise items.NakedError()
        except AttributeError:
            pass
        else:
            try:
                self.inventory.remove(equipment)
            except ValueError:
                pass


    def unequip(self, equipment, couldBeNaked=True):
        if not equipment in items.emptyEquipment:
            try:
                equipment.unequip(self, couldBeNaked)
            except items.NakedError:
                universal.clear_screen()
                if isinstance(equipment, items.Pajamas):
                    universal.say(format_text([[self.name, '''can't go without pajama bottoms. After all,''', heshe(self), '''needs something to cover''', hisher(self), 
                    '''bottom for when''', heshe(self), '''wants to leave''', hisher(self), '''room, but doesn't want to get dressed.''']]), justification=0)
                else:
                    universal.say(format_text([[self.name, '''realizes with a spike of embarassment that if''', heshe(self), '''equips''', equipment.name + ",", '''then''', 
                        heshe(self), '''will be naked from the waist down.''', HeShe(self), '''decides not to equip''', equipment.name + "."]]), justification=0)
                acknowledge(Person.character_sheet, self)
                raise items.NakedError()


    def display_equipment(self, slot):
        self.viewedSlot = slot
        universal.say(self.equipmentList[self.viewedSlot].display())
        set_commands(['(Enter) Unequip', '<==Back'])
        set_command_interpreter(view_item_interpreter)

    def is_male(self):
        return self.gender == MALE

    def is_female(self):
        return self.gender == FEMALE

    def ignores_spell(self, spell):
        return spell in self.ignoredSpells

    def is_specialized_in_spell_type(self, spellType):
        return self.is_magic_specialist() and self.specialization_type() == spellType

    def specialization_type(self):
        return self.specialization
        if self.specialization == COMBAT_MAGIC:
            return COMBAT
        elif self.specialization == BUFF_MAGIC:
            return BUFF
        elif self.specialization == STATUS_MAGIC:
            return STATUS
        elif self.specialization == SPECTRAL_MAGIC:
            return SPECTRAL
        else:
            return NO_MAGIC

    def increase_all_stats(self, num):
        """
            Note: This method increases all of the character's stats EXCEPT health, mana, current health, and current mana. 
        """
        for stat in range(len(self.primaryStats)):
            if stat != universal.HEALTH and stat != universal.MANA and stat != universal.CURRENT_MANA and stat != universal.CURRENT_HEALTH:
                self.primaryStats[stat] += num


    def decrease_all_stats(self, penalty):
        self.increase_all_stats(0-penalty)

    def decrease_stat(self, stat, num):
        self.increase_stat(stat, 0 - num)

    def receives_damage(self, num):
        self.set_stat(universal.CURRENT_HEALTH, self.current_health() - min(self.current_health(), num))

    def uses_mana(self, num):
        self.set_stat(universal.CURRENT_MANA, self.current_mana() - min(self.current_mana(), num))

    def restores(self):
        self.fully_heals()
        self.fully_restores_mana()
        self.clear_statuses()

    def clear_statuses(self):
        for status in self.statusList.copy():
            self.reverse_status(status)

    def fully_heals(self):
        self.set_stat(universal.CURRENT_HEALTH, self.health())

    def fully_restores_mana(self):
        self.set_stat(universal.CURRENT_MANA, self.mana())

    def heals(self, num):
        """
            Note that heal does not go past a character's maximum health. To bypass this (say through the fortify spell), use the increase_stat method.
        """
        healedAmount = 0
        if self.current_health() + num > self.health():
            #print('fully healing.')
            healedAmount = max(0, self.health() - self.current_health())
            self.fully_heals()
        else:
            self.increase_stat(universal.CURRENT_HEALTH, num)
            #print('partially healing.')
            healedAmount = num
        #print('--------------' + self.name + ' healing---------------')
        #print(str(self.current_health()) + '/' + str(self.health()))
        return healedAmount

    def restores_mana(self, num):
        """
            See heals.
        """
        if self.current_mana() + num > self.mana():
            self.fully_restores_mana()
        else:
            self.increase_stat(universal.CURRENT_MANA, num)

    def reset(self):
        self.set_state(self.origSelf)
        return self

    def reset_stats(self, episode=None, primaryStats=None):
        if primaryStats is None:
            self.default_stats()
        else:
            self.primaryStats = copy.deepcopy(primaryStats) 
        self.tier = self.talent() // TALENT_PER_TIER

    def default_stats(self):
        """
        Override this if we want a particular character to have different default stats.
        """
        self.set_all_stats(1, 1, 1, 1, 1, 15, 10)

    def get_stat(self, stat):
        return int(self.primaryStats[stat])

    def warfare(self):
        value = 2 * self.strength() + self.dexterity()
        for equipment in self.equipmentList:
            value += sum([enchantment.bonus for enchantment in equipment.enchantments if enchantment.stat == universal.WARFARE])
        return value

    def magic(self):
        value = 2 * self.talent() + self.willpower()
        for equipment in self.equipmentList:
            value += sum([enchantment.bonus for enchantment in equipment.enchantments if enchantment.stat == universal.MAGIC])
        return value

    def resilience(self):
        value = 2 * self.willpower() + self.talent()
        for equipment in self.equipmentList:
            value += sum([enchantment.bonus for enchantment in equipment.enchantments if enchantment.stat == universal.RESILIENCE])
        return value

    def grapple(self, person=None):
        """
        If person is none, we want the value of the grapple stat. If person is not None, then we want to start grappling that person.
        """
        if person is not None:
            self.grapplingPartner = person
            person.grapplingPartner = self
        else:
            value = 2 * self.dexterity() + self.strength()
            for equipment in self.equipmentList:
                value += sum([enchantment.bonus for enchantment in equipment.enchantments if enchantment.stat == universal.GRAPPLE])
            return value

    def break_grapple(self):
        gp = self.grapplingPartner
        self.grapplingPartner = None
        if gp is not None:
            gp.grapplingPartner = None

    def stealth(self):
        value = 2 * self.alertness()
        for equipment in self.equipmentList:
            value += sum([enchantment.bonus for enchantment in equipment.enchantments if enchantment.stat == universal.STEALTH])
        return value

    def health(self):
        return int(self.primaryStats[universal.HEALTH])

    def mana(self):
        return int(self.primaryStats[universal.MANA])

    def current_health(self):
        return int(self.primaryStats[universal.CURRENT_HEALTH])

    def current_mana(self):
        return int(self.primaryStats[universal.CURRENT_MANA])

    def stat(self, statIn):
        return int(self.primaryStats[statIn])

    def primary_stat(self, stat):
        return int(self.primaryStats[stat])

    def strength(self):
        return self.primary_stat(universal.STRENGTH)

    def dexterity(self):
        return self.primary_stat(universal.DEXTERITY)

    def willpower(self):
        return self.primary_stat(universal.WILLPOWER)

    def talent(self):
        return self.primary_stat(universal.TALENT)

    def alertness(self):
        return self.primary_stat(universal.ALERTNESS)

    def increase_primary_stat(self, stat, increment=1):
        self.primaryStats[stat] += increment
        self.recompute_stats()

    def equipment(self, slot):
        return self.equipmentList[slot]

    def weapon(self):
        return self.equipmentList[WEAPON]
    def shirt(self):
        return self.equipmentList[SHIRT]
    def lower_clothing(self):
        return self.equipmentList[LOWER_CLOTHING]


    def is_pantsless(self):
        return self.lower_clothing().name == items.emptyLowerArmor.name
    def worn_lower_clothing(self):
        return self.lower_clothing().name if self.lower_clothing() != items.emptyLowerArmor else self.underwear().name

    def lower_clothing_type(self):
        return self.lower_clothing().armorType if self.lower_clothing().name != items.emptyLowerArmor.name else self.lower_clothing().armorType

    def clad_bottom(self, useName=True, pajama=False):
        if pajama:
            return hisher(self) + " " + self.pajama_bottom().name + "-clad bottom"
        else:
            return (hisher(self) + (" " + self.underwear().name + "-clad bottom" if self.underwear() != items.emptyUnderwear else self.lower_clothing_type() + " bottom") 
                    if self.lower_clothing() == items.emptyLowerArmor else "the seat of " + (self.printedName + "'s" if useName else hisher(self)) + " " + 
                    self.lower_clothing_type())

    def clothing_below_the_waist(self):         
        return self.underwear() if self.lower_clothing().name == items.emptyLowerArmor.name else self.lower_clothing()
    
    def underwear(self):
        return self.equipmentList[UNDERWEAR]

    def pajama_top(self):
        return self.equipmentList[PAJAMA_TOP]

    def pajama_bottom(self):
        return self.equipmentList[PAJAMA_BOTTOM]

    def display_main_stats(self):
        if self.mainStatDisplay:
            statList = [': '.join([universal.primary_stat_name(stat), str(statValue)]) for (stat, statValue) in 
                    zip([i for i in range(0, len(self.primaryStats[:-4]))], self.primaryStats)] 
        else:
            statList = []
            statList.append(' '.join(['warfare:', str(self.warfare())]))
            statList.append(' '.join(['grapple:', str(self.grapple())]))
            statList.append(' '.join(['resilience:', str(self.resilience())]))
            statList.append(' '.join(['magic:', str(self.magic())]))
            statList.append(' '.join(['stealth:', str(self.stealth())]))
        statList.append('Health: ' + str(self.primaryStats[-2]) + '/' + str(self.primaryStats[-4]))
        statList.append('Mana: '   + str(self.primaryStats[-1]) + '/' + str(self.primaryStats[-3]))
        return '\n'.join(statList)

    def display_stats(self):
        return self.display_main_stats()
    def display_spells(self, tierNum=None):
        if tierNum is None:
            spellList = []
            for tier in self.spellList:
                if tier is not None:
                    spellList.extend([s.name for s in tier])
            return ', '.join(spellList)
        else:
            tier = self.spellList[tierNum]
            try:
                return '\n'.join([str(n) + '. ' + s.name for (n,s) in zip([i for i in range(1, len(tier)+1)], tier)])
            except TypeError:
                return ' '.join([self.printedName, 'does not know any spells of this tier.'])

    def known_spells(self, tierNum=None):
        if tierNum is None:
            spellList = []
            for tier in self.spellList:
                if tier is not None:
                    spellList.extend([s for s in tier])
            return spellList
        else:
            tier = self.spellList[tierNum]
        return tier

    #The following functions take another person as argument. The first is used when this person failed to spank the arguent.
    #The second is used when the argument failed to spank this person.
    #The third is used when this person spanked the argument.
    #The fourth is used when this person is spanked by the argument.
    #The fifth is used when this person reversed the attempted spanking of the argument
    #The sixth is used when the argument reverses an attempted spanking by this person. 

    def is_magic_specialist(self):
        if (self.specialization == COMBAT_MAGIC or 
            self.specialization == BUFF_MAGIC or 
            self.specialization == SPECTRAL_MAGIC or
            self.specialization == STATUS_MAGIC):
            return True
        else:
            return False

    def magic_modifier(self, inCombat=True):
        return self.magic() + self.iron_modifier(True, inCombat)

    def magic_attack(self, inCombat=True):
        return self.magic_modifier(inCombat)

    def iron_modifier(self, rawMagic, inCombat=True):
        return self.magic_penalty() if rawMagic and inCombat else 0

    def is_grappling(self, opponent=None):
        if opponent is None:
            return self.grapplingPartner is not None
        elif self.grapplingPartner is None:
            return False
        else:
            return self.grapplingPartner == opponent

    def attack_modifier(self):
        if self.is_grappling():
            return self.grapple() + self.attack_penalty()
        else:
            return self.warfare() + self.attack_penalty()

    def attack(self):
        return self.attack()

    def damage(self):
        weaponDamage = random.randrange(self.weapon().minDamage, self.weapon().maxDamage)
        if self.is_grappling():
            weaponDamage += self.weapon().grappleBonus
        else:
            weaponDamage += self.weapon().armslengthBonus
        return self.warfare() + weaponDamage

    def magic_defense(self, rawMagic=False):
        return self.magic() + self.magic_defense_bonus() + (self.magic_penalty() if rawMagic else 0)

    def defense(self):
        if self.is_grappling():
            return self.grapple() + self.defense_bonus()
        else:
            return self.warfare() + self.defense_bonus()

    def magic_penalty(self, rawMagic=True):
        return self.weapon().castingPenalty + self.shirt().castingPenalty + self.lower_clothing().castingPenalty + self.underwear().castingPenalty


    def magic_defense_bonus(self):
        defenseBonus = 0
        if statusEffects.LoweredMagicDefense.name in self.statusList:
            defenseBonus = self.statusList[statusEffects.LoweredMagicDefense.name][0].inflict_status(self)
        if statusEffects.MagicShielded.name in self.statusList: 
            defenseBonus += self.statusList[statusEffects.MagicShielded.name][STATUS_OBJ].inflict_status(self)
        return self.weapon().magicDefense + self.shirt().magicDefense + self.lower_clothing().magicDefense + self.underwear().magicDefense + defenseBonus

    def inflict_status(self, status, originalList=None, newList=None):
        if originalList is not None and newList is not None:
            status.inflict_status(self, originalList, newList)
        else:
            status.inflict_status(self)
        self.statusList[status.name] = [status, status.duration]

    def reverse_status(self, statusName, originalList=None, newList=None):
        if self.is_inflicted_with(statusName):
            if originalList is not None and newList is not None:
                self.statusList[statusName][STATUS_OBJ].reverse_status(self, originalList, newList)
            else:
                self.statusList[statusName][STATUS_OBJ].reverse_status(self)
            del self.statusList[statusName] 

    def is_inflicted_with(self, statusName):
        return statusName in self.statusList.keys()  

    def status_string(self):
        return ';'.join([statusEffects.status_shorthand(statusName) for statusName in self.statusList.keys()])

    def decrement_statuses(self, amount=1):
        expiredStatuses = []
        for statusName in self.statusList.keys():
            self.statusList[statusName][STATUS_OBJ].every_round(self)
            self.statusList[statusName][DURATION] -= amount
            if self.statusList[statusName][DURATION] <= 0:
                expiredStatuses.append(statusName)
        for statusName in expiredStatuses:
            self.reverse_status(statusName)

    def get_status(self, statusName):
        return self.statusList[statusName][STATUS_OBJ]

    def status_names(self):
        return self.statusList.keys()
        
    
    def learn_spell(self, spell):
        print(self.spellList)
        if self.spellList[spell.tier] is None:
            self.spellList[spell.tier] = [spell]
        else:
            if not spell in self.spellList[spell.tier]:
                self.spellList[spell.tier].append(spell)

    def forget_spell(self, spell):
        if spell in self.spellList[spell.tier]:
            self.spellList[spell.tier].remove(spell)

    def clear_spells(self):
        self.spellList = [None for i in range(NUM_TIERS)]

    def spells(self, tierNum=-1):
        spellList = []
        if tierNum == -1:
            for tier in self.spellList:
                if tier is not None:
                    spellList.extend(tier)
        else:
            spellList = self.spellList[tier]
        return spellList


    def attack_penalty(self):
        return self.shirt().attackPenalty + self.lower_clothing().attackPenalty + self.underwear().attackPenalty


    def defense_bonus(self):
        defenseBonus = 0
        if self.is_inflicted_with(statusEffects.LoweredDefense.name):
            defenseBonus = self.statusList[statusEffects.LoweredDefense.name][STATUS_OBJ].inflict_status(self)
        if self.is_inflicted_with(statusEffects.Shielded.name):
            print('defense bonus:')
            print(self.shirt().attackDefense)
            print(self.lower_clothing().attackDefense)
            print(self.underwear().attackDefense)
            print(defenseBonus)
            print(self.statusList)
            print(self.statusList[statusEffects.Shielded.name][STATUS_OBJ])
            print(self.statusList[statusEffects.Shielded.name][STATUS_OBJ].inflict_status(self))
            print(self.statusList[statusEffects.Shielded.name][STATUS_OBJ].inflict_status)
            defenseBonus += self.statusList[statusEffects.Shielded.name][STATUS_OBJ].inflict_status(self)
        return self.shirt().attackDefense + self.lower_clothing().attackDefense + self.underwear().attackDefense + defenseBonus
    

    @staticmethod
    def add_data(data, saveData):
        """
        Given a string containing data about self, appends "Person:" and the data to saveData.
        """
        saveData.extend(["Person Data:", data])

    def save(self):
        """
        Returns a string containing the important data of this character.
        """
        saveData = []
        Person.add_data(self.name.strip(), saveData)
        Person.add_data(str(self.gender), saveData)
        Person.add_data(self.description.strip(), saveData)
        statusList = []
        for statusName, statusTuple in self.statusList.iteritems():
            status, duration = statusTuple
            statusList.extend(["Status:", statusName, status.save()])
        Person.add_data('\n'.join(statusList), saveData)
        Person.add_data(self.rawName.strip(), saveData)
        spellNames = []
        for tier in self.spellList:
            if tier:
                spellNames.append(', '.join([spell.name for spell in tier]))
            else:
                spellNames.append('None')
        Person.add_data('\n'.join(spellNames), saveData) 
        itemList = []
        for item in self.inventory:
            itemList.extend(["Item:", item.name, item.save()])
        Person.add_data('\n'.join(itemList), saveData)
        equipmentList = []
        for equipment in self.equipmentList:
            equipmentList.extend(["Equipment:", equipment.name, equipment.save()])
        Person.add_data('\n'.join(equipmentList), saveData)
        Person.add_data('\n'.join([str(stat) for stat in self.primaryStats]), saveData)
        Person.add_data(str(self.tier), saveData)
        Person.add_data(str(self.specialization), saveData)
        Person.add_data('\n'.join([spell.name for spell in self.ignoredSpells]), saveData)
        Person.add_data(str(self.combatType), saveData) 
        try:
            Person.add_data(str(self.litany.index), saveData)
        except AttributeError:
            Person.add_data(str(self.litany), saveData)
        try:
            Person.add_data(str(self.defaultLitany.index), saveData)
        except AttributeError:
            Person.add_data(str(self.defaultLitany), saveData)
        Person.add_data(str(self.coins), saveData)
        Person.add_data(str(self.specialization), saveData)
        Person.add_data(str(self.order), saveData)
        Person.add_data('\n'.join([spell.name if spell else "None" for spell in self.quickSpells]), saveData)
        Person.add_data(str(self.printedName), saveData)
        Person.add_data(str(self.emerits), saveData)
        Person.add_data(str(self.demerits), saveData)
        Person.add_data(str(self.hairLength), saveData)
        Person.add_data(str(self.bodyType), saveData)
        Person.add_data(str(self.height), saveData)
        Person.add_data(str(self.musculature), saveData)
        Person.add_data(str(self.bumStatus), saveData)
        welts = [welt.strip() for welt in self.welts if welt.strip()]
        if welts:
            Person.add_data('\n'.join(welts), saveData)
        else:
            Person.add_data('', saveData)
        Person.add_data(str(self.skinColor), saveData)
        Person.add_data(str(self.hairColor), saveData)
        Person.add_data(str(self.eyeColor), saveData)
        Person.add_data(str(self.hairStyle), saveData)
        marks = [mark.strip() for mark in self.marks if mark.strip()]
        if marks:
            Person.add_data('\n'.join(self.marks), saveData)
        else:
            Person.add_data('', saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(data, person):
        #Note: First entry in the list is the empty string.
        data = data.strip()
        _, name, gender, description, statuses, rawName, spellNames, inventory, equipmentList, stats, tier, specialization, ignoredSpells, combatType, litany, defaultLitany, coins, specialization, \
                order, quickSpells, printedName, emerits, demerits, hairLength, bodyType, height, musculature, bumStatus, welts, skinColor, hairColor, eyeColor, hairStyle, marks = \
                data.split("Person Data:")
        person.name = name.strip()
        person.description = description.strip()
        person.gender = int(gender.strip())
        person.specialization = int(specialization.strip())
        person.statusList = {}
        if statuses.strip():
            statuses = statuses.split("Status:")
            for status in statuses:
                name, _, statusData = status.partition('\n')
                statusEffect = statusEffects.build_status(name)
                statusEffects.StatusEffect.load(status, statusEffect)
                person.statusList[name] = (statusEffect, statusEffect.duration)
        person.rawName = rawName.strip()
        if spellNames.strip():
            person.clear_spells()
            spellTiers = spellNames.split('\n')
            spellTiers = [spellName.strip() for spellName in spellTiers if spellName.strip()]
            for spells in spellTiers:
                spells = spells.split(',')
                for spellName in spells:
                    spellName = spellName.strip()
                    if spellName != "None":
                        spell = get_spell(spellName)
                        person.learn_spell(spell)
        person.inventory = []
        if inventory.strip():
            inventory = [item.strip() for item in inventory.split("Item:") if item.strip()]
            for itemData in inventory:
                name, _, itemData = itemData.partition('\n')
                items.Item.load(itemData, universal.state.get_item(name))
                person.take_item(universal.state.get_item(name))
        equipmentList = [equipment.strip() for equipment in equipmentList.split("Equipment:") if equipment.strip()]
        person.equipmentList = [items.emptyWeapon, items.emptyUpperArmor, items.emptyLowerArmor, items.emptyUnderwear, items.emptyPajamaTop, items.emptyPajamaBottom]
        for equipmentData in equipmentList:
            name, _, equipmentData = equipmentData.partition('\n')
            items.Item.load(equipmentData, universal.state.get_item(name))
            person.equip(universal.state.get_item(name))
        stats = [stat.strip() for stat in stats.split('\n') if stat.strip()] 
        person.primaryStats = [int(stat.strip()) for stat in stats]
        person.tier = int(tier.strip())
        person.specialization = int(specialization.strip())
        ignoredSpells = [spellName.strip() for spellName in ignoredSpells if spellName.strip()]
        person.ignoredSpells = []
        if ignoredSpells:
            person.ignoredSpells = [get_spell(spellName.strip()) for spellName in ignoredSpells]
        if combatType.strip() != "None":
            person.combatType = int(combatType.strip())
        if litany.strip() != "None":
            person.litany = int(litany.strip())
        person.coins = int(coins.strip())
        if 'zeroth_order' in order:
            person.order = zeroth_order
        elif 'first_order' in order:
            person.order = first_order
        elif 'second_order' in order:
            person.order = second_order
        elif 'third_order' in order:
            person.order = third_order
        elif 'fourth_order' in order:
            person.order = fourth_order
        elif 'fifth_order' in order:
            person.order = fifth_order
        elif 'sixth_order' in order:
            person.order = sixth_order
        else:
            raise Exception(''.join([order, 'is not a valid order, according to the load function for people.']))
        quickSpells = [spellName.strip() for spellName in quickSpells.split('\n') if spellName.strip()]
        person.quickSpells = [None if spellName.strip() == "None" else get_spell(spellName.strip()) for spellName in quickSpells]
        person.printedName = printedName.strip()
        person.emerits = int(emerits.strip())
        person.demerits = int(demerits.strip())
        person.hairLength = hairLength.strip()
        person.bodyType = bodyType.strip()
        person.height = height.strip()
        person.musculature = musculature.strip()
        person.bumStatus = int(bumStatus.strip())
        person.welts = welts.split('\n')
        person.skinColor = skinColor.strip()
        person.hairColor = hairColor.strip()
        person.eyeColor = eyeColor.strip()
        person.hairStyle = hairStyle.strip()
        person.marks = marks.split('\n')

    def character_sheet_spells(self):
        return '\n'.join(['Name: ' + self.name, 'Order: ' + order_name(self.order),  self.display_stats(), 'Spells: ', self.display_spells()])

    def character_sheet(self, mode=None):
        """
            In addition to listing the character's statistics and inventory, this function also sets the commands and command interpreter for studying the character in
            more detail
        """
        global currentMode
        print('character sheet!')
        if mode is not None:
            currentMode = mode
        global currentPerson
        currentPerson = self
        say_title(self.name)
        universal.say('\n'.join(['Order: ' + order_name(self.order), 'Status: ' + self.display_statusList(), 'Defense: ' + str(self.defense()), 
            'Magic Defense: ' + str(self.magic_defense(False)),
            #'Exp to Next Level: ' + str(self.level * XP_INCREASE_PER_LEVEL - self.experience),
            self.display_stats(), '\t']))
        numberedEquipmentList = universal.numbered_list(['Weapon: ' + self.weapon().name, 'Chest: ' + self.shirt().name, 'Legs: ' + self.lower_clothing().name, 
            'Underwear: ' + self.underwear().name, 'Pajama Top: ' + self.pajama_top().name, 'Pajama Bottom: ' + self.pajama_bottom().name])
        universal.say('\n'.join(numberedEquipmentList + [self.display_inventory()]), columnNum=2)
        set_commands(['(A)ppearance','(S)pells', '(E)quip', '(#)View Item', '(T)oggle Stats', '<==Back']) 
        set_command_interpreter(character_viewer_interpreter)

    def display_inventory(self):
        if self.inventory is None:
            return 'Inventory:'
        else:
            return '\n'.join(['', 'Inventory:', ' '.join(str(n) + '. ' + item.name for 
                (n, item) in zip([i for i in range(len(self.equipmentList) + 1, len(self.inventory) + len(self.equipmentList) + 1)], self.inventory))])

    def display_tiers(self, interpreter=None):
        universal.say('Tiers: ' + ', '.join(str(i) for i in range(self.tier + 1)))
        set_commands(['(#)select tier', '<==Back'])
        if interpreter == None:
            print('interpreter is none.')
            set_command_interpreter(display_tiers_interpreter)
        else:
            print('interpreter is not none. interpreter:')
            print(interpreter)
            set_command_interpreter(interpreter)
        print(universal.commandInterpreter)

    def display_statusList(self):
        if self.statusList == {}:
            return 'Healthy'
        else:
            return ', '.join([status + ": " + str(statusDurationPair[DURATION]) for status, statusDurationPair in self.statusList.iteritems()])

    def equip_menu(self):
        set_commands(['(#) Select item to equip:_', '<==Back', '(Esc) Return to menu'])
        global selectedPerson
        selectedPerson = self
        set_command_interpreter(equip_interpreter)

    def appearance(self, printEquipment=False):
        hairStyleDescription = ''
        if self.hairStyle == 'down':
            hairStyleDescription = 'down'
        else:
            hairStyleDescription = 'pulled into'
            if self.hairStyle == 'pigtails':
                hairStyleDescription += ' cute pigtails.'
            else:
                hairStyleDescription += ' '.join(['', 'a', self.hairStyle])
        appearance = [[self.name + "'s", '''skin is a''', self.skinColor + ".", HeShe(self), '''has''', self.eyeColor, '''eyes, and is wearing''', hisher(self),
            self.hairLength + ",", self.hairColor,'''hair''', hairStyleDescription + "."],
            [HeShe(self), '''stands at a fairly''', self.height, '''height.''', HeShe(self), '''has a''', self.musculature + ",", self.bodyType, '''body.''']]
        bumDesc = ' '.join([self.muscle_adj() + ",", self.bum_adj()])
        if self.marks:
            appearance.append(self.marks)
        elif self.bumStatus > 6:
            appearance.append([self.name + "'s", bumDesc, '''bottom is criss-crossed with countless layers of marks and welts. Every inch of''', hisher(), '''bottom is''',
            '''throbbing with raw, burning pain.''', HisHer(), '''walk has been reduced to a pained hobble.'''])
        elif self.bumStatus > 4:
            appearance.append([self.name + "'s", bumDesc, '''bottom is a dark red. Every inch of''', hisher(), '''bum is covered in marks and welts. Every step makes''',
                hisher(), '''bottom buzz with pain, and the thought of sitting makes''', himher(), '''wince.'''])
        elif self.bumStatus > 2:
            appearance.append([self.name + "'s", bumDesc, '''bottom is a deep red. Several welts mar''', hisher(), '''cheeks.''', HeShe(), '''can't sit without wincing''',
                '''and there is a slight stiffness to''', hisher(), '''gait.'''])
        elif self.bumStatus > 0:
            appearance.append([self.name + "'s", bumDesc, '''bottom is a dark pink, interspersed with patches of dark red.''', HisHer(), '''bottom tingles with the''',
                    '''lingering sting of''', hisher(), '''recent spankings. Sitting is best done with great care.'''])
        elif self.bumStatus == 0:
            appearance.append([self.name + "'s", bumDesc, '''bottom is smooth and unmarked.''', HeShe(), '''wonders idly just how long''',
                    '''that will last.'''])
        if printEquipment:
            appearance.append('\n'.join(['Weapon: ' + self.weapon().name, 'Chest: ' + self.shirt().name, 'Legs: ' + self.lower_clothing().name, 
                'Underwear: ' + self.underwear().name]))
        return format_text(appearance)

    def clear_marks(self):
        self.marks = []

    def remove_mark(self):
        self.marks.pop() 

equipNum = ''
selectedPerson = None
def equip_interpreter(keyEvent):
    global equipNum
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if 0 < num and num <= len(selectedPerson.inventory) + len(selectedPerson.equipmentList): 
            if len(selectedPerson.inventory) + len(selectedPerson.equipmentList) < 10:
                num = num - len(selectedPerson.equipmentList) - 1
                try:
                    selectedPerson.equip(selectedPerson.inventory[num])
                except InvalidEquipmentError:
                    universal.say('''That cannot be equipped!''')
                    acknowledge(selectedPerson.equip_menu, ())
                    return
                except IndexError:
                    pass
            else:
                equipNum += pygame.key.name(keyEvent.key)
                set_command_interpreter(['(#) Select input to equip: ' + equipNum + '_', '<==Back', '(Esc) Return to menu'])
            selectedPerson.character_sheet()
            selectedPerson.equip_menu()
    elif keyEvent.key == K_BACKSPACE: 
        if equipNum != '':
            equipNum = equipNum[:-1]
        else:
            selectedPerson.character_sheet(currentMode)
    elif keyEvent.key == K_ESCAPE:
        selectedPerson.character_sheet(currentMode)
    elif keyEvent.key == K_RETURN and equipNum != '':
        num = int(equipNum) - len(selectedPerson.equipmentList) - 1
        if 0 < num and num <= len(selectedPerson.inventory):
            try:
                selectedPerson.equip(selectedPerson.inventory[num])
            except InvalidEquipmentError:
                say('''That cannot be equipped!''')
                acknowledge(selectedPerson.equip_menu, ())
                return
        selectedPerson.character_sheet()
        selectedPerson.equip_menu()

                

class PlayerCharacter(Person):
    """
    In addition to all the information a person usually has, a PlayerCharacter has a list of keywords that track game progression.
    Also the spanking methods have been overriden so that they call the appropriate methods of the other character, i.e. failed_to_spank(self, person) calls 
    person.avoided_spanking_by(self). Note that this SHOULD NOT be done by other characters. If we had two different characters with these functions implemented this way,
    and one got Charmed, and tried to spank the other, we'd get infinite function calls.

    This is only allowed for the player character because there should be only one in any given episode (though there's no reason why there couldn't be more than one across
    the entire game, so long as the two never fight each other).
    """
    def __init__(self, name, gender, description="", currentEpisode=None, order=zeroth_order, nickname=""):
        super(PlayerCharacter, self).__init__(name, gender, None, None, description=description, order=zeroth_order, rawName='$$$universal.state.player$$$', skinColor='rich caramel',
                eyeColor='brown', hairColor='dark brown')
        self.keywords = []
        self.currentEpisode = currentEpisode
        self.numSpankings = 0
        self.numSpankingsGiven = 0
        self.coins = 20
        self.fakeName = ''
        self.nickname = nickname
        self.viewedSlot = None
        self.reputation = 0

    def add_mark(self, mark):
        super(PlayerCharacter, self).add_mark(mark)
        self.numSpankings += 1

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Player Data:", data])

    def save(self):
        saveString = super(PlayerCharacter, self).save()
        saveData = [saveString, "Player Character Only:"]
        print("saving keywords:")
        print(self.keywords)
        PlayerCharacter.add_data('\n'.join(keyword.strip() for keyword in self.keywords if keyword.strip()), saveData)
        PlayerCharacter.add_data(str(self.currentEpisode), saveData)
        import episode
        try:
            PlayerCharacter.add_data(str(episode.allEpisodes[self.currentEpisode].currentSceneIndex), saveData)
        except KeyError:
            PlayerCharacter.add_data('', saveData)
        PlayerCharacter.add_data(str(self.numSpankings), saveData)
        PlayerCharacter.add_data(str(self.numSpankingsGiven), saveData)
        PlayerCharacter.add_data(str(self.fakeName), saveData)
        PlayerCharacter.add_data(str(self.nickname), saveData)
        PlayerCharacter.add_data(str(self.reputation), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(loadData, player):
        personData, _, playerCharacterData = loadData.partition("Player Character Only")
        Person.load(personData, player)
        loadData = playerCharacterData
        _, keywords, currentEpisode, currentSceneIndex, numSpankings, numSpankingsGiven, fakeName, nickname, reputation = loadData.split("Player Data:")
        player.keywords = [keyword.strip() for keyword in keywords.split('\n') if keyword.strip()]
        print("loading keywords")
        print(player.keywords)
        player.currentEpisode = currentEpisode.strip()
        print(player.currentEpisode)
        if player.currentEpisode == "None":
            player.currentEpisode = None
        else:
            episode.allEpisodes[player.currentEpisode].currentSceneIndex = int(currentSceneIndex.strip())
        player.numSpankings = int(numSpankings.strip())
        player.numSpankingsGiven = int(numSpankingsGiven.strip())
        player.fakeName = fakeName.strip()
        player.nickname = nickname.strip()
        player.reputation = int(reputation.strip())




                


    def get_id(self):
        if self.identifier:
            rawName = self.rawName + str(self.identifier)
        else:
            rawName = self.rawName
        return rawName + ".playerCharacter"

    def set_fake_name(self):
        if self.gender == FEMALE:
            self.fakeName = 'Cascada' if self.name == 'Adelina' else 'Adelina'
        elif self.gender == MALE:
            self.fakeName = 'Adriano' if self.name == 'Cesar' else 'Cesar'
    def willpower_check(self, num):
        return checkWillpower and self.willpower() >= num

    def add_keyword(self, keyword):
        if not keyword in self.keywords:
            self.keywords.append(keyword)

    def remove_keyword(self, keyword):
        if keyword in self.keywords:
            self.keywords.remove(keyword)

    def failed_to_spank(self, person):
        person.avoided_spanking_by(self)

    def avoided_spanking_by(self, person):
        person.failed_to_spank(self)

    def spanked_by(self, person):
        person.spanked(self)

    def reversed_spanking_of(self, person):
        person.had_spanking_reversed_by(self)

    def had_spanking_reversed_by(self, person):
        person.reversed_spanking_of(self)
           
    def add_mark(self, mark):
        super(PlayerCharacter, self).add_mark(mark)
        self.numSpankings += 1


    @staticmethod
    def _load(dataList):
        raise NotImplementedError()

def display_tiers_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        currentPerson.character_sheet(currentMode)
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if num <= currentPerson.tier:
            universal.say(currentPerson.display_spells(num))
            set_commands(['(#)view spell', '<==Back'])
            global currentTier
            currentTier = num
            set_command_interpreter(display_spells_interpreter)

currentTier = 0
def display_spells_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        currentPerson.display_tiers()
    elif keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key))
        if  currentPerson.spellList[currentTier] is not None and 0 < num and num <= len(currentPerson.spellList[currentTier]):
            universal.say(currentPerson.spellList[currentTier][num-1].get_description())
            set_commands(['<==Back'])
            set_command_interpreter(return_to_display_spells_interpreter)

def return_to_display_spells_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        universal.say(currentPerson.display_spells(currentTier))
        set_commands(['(#)view spell', '<==Back'])
        set_command_interpreter(display_spells_interpreter)



currentMode = None
currentPerson = None
selectedNum = None
NUM_DIGITS = 3
def character_viewer_interpreter(keyEvent):     
    global equipNum
    global selectedNum
    #set_commands(['(S)pells, (E)quip, (#)View Item, (W)eapon, S(H)irt, (L)ower Clothing, (U)nderwear, <==Back']) 
    if keyEvent.key == K_BACKSPACE and equipNum != '':
        equipNum = equipNum[:-1]
        set_commands(['(A)ppearance','(S)pells', '(E)quip', '(#)View Item:' + equipNum + '_', '(T)oggle Stats', '<==Back']) 
    elif keyEvent.key == K_BACKSPACE:
        currentMode()
    elif keyEvent.key == K_s:
        currentPerson.display_tiers()
    #elif keyEvent.key == K_e:
        #currentPerson.equip_menu()
    elif keyEvent.key in NUMBER_KEYS:
        if len(currentPerson.inventory) + len(currentPerson.equipmentList) < 10:
            print('num items in inventory less than 10!')
            num = int(pygame.key.name(keyEvent.key)) - 1
            allEquipment = currentPerson.equipmentList + currentPerson.inventory
            try:
                universal.say(allEquipment[num].display())
            except IndexError:
                return
            else:
                if num < len(currentPerson.equipmentList):
                    currentPerson.viewedSlot = num
                commandList = []
                if len(currentPerson.equipmentList) <= num and currentPerson.inventory[num - len(currentPerson.equipmentList)].is_equippable():
                    commandList.append('(Enter) Equip')
                    global selectedNum
                    selectedNum = num - len(currentPerson.equipmentList)
                elif num < len(currentPerson.equipmentList): 
                    commandList.append('(Enter) Unequip')
                commandList.append('<==Back')
                set_commands(commandList)
                set_command_interpreter(view_item_interpreter)
        else:
            print('num items in inventory more than ten!')
            if len(equipNum) < NUM_DIGITS:
                equipNum += pygame.key.name(keyEvent.key)
            set_commands(['(A)ppearance','(S)pells', '(E)quip', '(#)View Item:' + equipNum + '_', '(T)oggle Stats', '<==Back']) 
    elif keyEvent.key == K_RETURN and len(currentPerson.equipmentList) + len(currentPerson.inventory) >= 10:
        print('calling return!')
        #This has turned into a nightmare, and really needs to be refactored. I'll do it later. All I want is for the damn thing to work.
        try:
            num = int(equipNum) - 1
        except ValueError:
            print('value error!')
            print(equipNum)
            equipNum = ''
            return
        else:
            print('no value error!')
            equipNum = ''
        commandList = []
        if len(currentPerson.equipmentList) <= num and currentPerson.inventory[num - len(currentPerson.equipmentList)].is_equippable():
            commandList.append('(Enter) Equip')
            selectedNum = num - len(currentPerson.equipmentList)
        elif num < len(currentPerson.equipmentList): 
            commandList.append('(Enter) Unequip')
        print('player input:')
        print(num)
        if num < 0:
            set_commands(['(A)ppearance','(S)pells', '(E)quip', '(#)View Item:' + equipNum + '_', '(T)oggle Stats', '<==Back']) 
            return
        elif num >= len(currentPerson.equipmentList):
            print('number greater than equipment list!')
            num -= len(currentPerson.equipmentList)
            try:
                print(currentPerson.inventory[num].display())
                universal.say(currentPerson.inventory[num].display())
            except IndexError:
                print('index error. inventory len:')
                print(len(currentPerson.inventory))
                print('num:')
                print(num)
                set_commands(['(A)ppearance','(S)pells', '(E)quip', '(#)View Item:' + equipNum + '_', '(T)oggle Stats', '<==Back']) 
                return
        elif num < len(currentPerson.equipmentList):
            currentPerson.viewedSlot = num
            universal.say(currentPerson.equipmentList[num].display())
        commandList.append('<==Back')
        set_commands(commandList)
        set_command_interpreter(view_item_interpreter)
    elif keyEvent.key == K_t:
        currentPerson.mainStatDisplay = not currentPerson.mainStatDisplay
        currentPerson.character_sheet()
    elif keyEvent.key == K_a:
        say(currentPerson.appearance(), justification=0)
        acknowledge(Person.character_sheet, currentPerson)

def view_item_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
        currentPerson.viewedSlot = None
        currentPerson.character_sheet(currentMode)
    elif keyEvent.key == K_RETURN and '(Enter) Unequip' in universal.commands:
        try:
            currentPerson.unequip(currentPerson.equipmentList[currentPerson.viewedSlot])
        except items.NakedError:
            return
        currentPerson.viewedSlot = None
        currentPerson.character_sheet(currentMode)
    elif keyEvent.key == K_RETURN and '(Enter) Equip' in universal.commands:
        global selectedNum
        currentPerson.equip(currentPerson.inventory[selectedNum])
        selectedNum = None
        currentPerson.character_sheet(currentMode)


#-----------------------------------
class Party(universal.RPGObject):
    def __init__(self, members):
        super(Party, self).__init__()
        self.inDungeon = False
        if type(members) is not list:
            self.members = [members]
        else:
            self.members = members

    def __len__(self):
        return self.len()

    def __add__(self, other):
        return self.members + other.members

    def len(self):
        return len(self.members)

    def index(self, member):
        return self.members.index(member)

    def __iter__(self):
        for member in self.members:
            yield member

    def __getitem__(self, key):
        return self.members[key]

    def remove_member(self, member):
        try:
            self.members.remove(member)
        except ValueError:
            pass


    def add_member(self, member):
        if not member in self.members:
            self.members.append(member)

    def remove_members(self, members):
        self.members = [m for m in self.members if m not in members]

    def get_member(self, index):
        return self.members[index]

    def extend(self, newMembers):
        self.members.extend(newMembers.members)

    def inParty(self, person):
        return person in self.members

    def is_defeated(self):
        return len(self.members) == 0

    def _save(self):
        partyNames = ['begin_party:']
        partyNames.extend([p.get_id() for p in self.members])
        partyNames.append('end_party')
        return '\n'.join(partyNames)

    def display_party(self, showHP=True, ally=None, targeted=None, grappling=False):
        allyIndex = -1
        targetedIndices = []
        if ally is not None and ally in self.members:
            allyIndex = self.members.index(ally)
        if targeted is not None:
            targetedIndices = [i for i in [self.index(t) for t in targeted]] 
        #print([member.printedName for member in self])
        #print([member.status_string() for member in self])
        memberNames = [': '.join([member.printedName, member.status_string()]) for member in self]
        if showHP:
            partyTxt = ['\t'.join([target(n, arrow(n, allyIndex), targetedIndices) + '. '
                + memberName, str(member.current_health()) + '/' + str(member.health()), str(member.current_mana()) + '/' + str(member.mana())])
                for (n, member, memberName) in zip([i for i in range(1, len(self.members)+1)], self.members, memberNames)]
            if grappling:
                partyTxt = ['\t'.join([memTxt, display_person(mem.grapplingPartner)]) for (memTxt, mem) in zip(partyTxt, self.members)]
            return '\n\t'.join(partyTxt)
        else:
            return '\t'.join([target(n, arrow(n, allyIndex), targetedIndices) + '. ' + '\n'
                + memberName for (n, member, memberName) in 
                zip([i for i in range(1, len(self.members)+1)], self.members, memberNames)])


    def display(self):
        return display_party(self)


    def avg_stealth(self):
        return sum([member.stealth() for member in self.members]) / len(self)

    def max_stealth(self):
        return max([member.stealth() for member in self.members])

    def median_stealth(self):
        return median([member.stealth() for member in self.members])

def median(listNums):
    return listNums[len(listNums) // 2]

def arrow(n, allyIndex):
    return ' '.join(['->', str(n)]) if n-1 == allyIndex else str(n)

def target(n, strn, targetIndices):
    return ' '.join(['X', strn]) if n-1 in targetIndices else strn

def set_party(partyIn):
    universal.state.party = partyIn

def get_party():
    return universal.state.party


#--------------------------------------Spells----------------------------------------------------------------------
#Looking for the constant NUM_TIERS? Since the person module needs it as well (and this module depends on the person module), NUM_TIERS was defined in universal.py.

NUM_SPELL_TYPES = 4

NO_MAGIC = -1

#This is a list of list of tuples. Each list of tuples is all the spells in that particular tier.
allSpells = [None for i in range(universal.NUM_TIERS)]

def get_spell(name):
    for spellTier in allSpells:
        for spellTuple in spellTier:
            for spell in spellTuple:
                if spell.name == name:
                    return spell
COMBAT_INDEX = 0
STATUS_INDEX = 1
BUFF_INDEX = 2
SPECTRAL_INDEX = 3
def get_spell_index(spellIndex):
    if spellIndex == COMBAT_MAGIC:
        return COMBAT_INDEX
    elif spellIndex == STATUS_MAGIC:
        return STATUS_INDEX
    elif spellIndex == BUFF_MAGIC:
        return BUFF_INDEX
    elif spellIndex == SPECTRAL_MAGIC:
        return SPECTRAL_INDEX
    else:
        raise ValueError(str(i) + 'is not a valid spell school.')

def action_type_to_spell_type(actionType):
    if actionType == 'combat':
        return COMBAT
    elif actionType == 'buff':
        return BUFF
    elif actionType == 'status':
        return STATUS
    elif actionType == 'spectral':
        return SPECTRAL
def get_basic_spell(tierNum, spellType):
    if spellType < 0 or spellType > SPECTRAL:
        raise ValueError(' '.join(['invalid spell type. Excepted a number between 0 and 3, got', str(spellType)]))
    return None if allSpells[tierNum] is None else allSpells[tierNum][spellType][0]

def get_advanced_spell(tierNum, spellType):
    if spellType < 0 or spellType > SPECTRAL:
        raise ValueError(' '.join(['invalid spell type. Excepted a number between 0 and 3, got', str(spellType)]))
    return None if allSpells[tierNum] is None else allSpells[tierNum][spellType][1]

def get_expert_spell(tierNum, spellType):
    if spellType < 0 or spellType > SPECTRAL:
        raise ValueError(' '.join(['invalid spell type. Excepted a number between 0 and 3, got', str(spellType)]))
    return None if allSpells[tierNum] is None else allSpells[tierNum][spellType][2]

def print_spell_type(spellType):
    if spellType == COMBAT:
        return 'Combat'
    elif spellType == BUFF:
        return 'Buff'
    elif spellType == STATUS:
        return 'Status'
    elif spellType == SPECTRAL:
        return 'Spectral'
    else:
        raise ValueError(' '.join(str(spellType), 'is not a spell type.'))

BASIC = 0
ADVANCED = 1
EXPERT = 2

#TODO: Modify the effect functions of our spells to return the same triples as all the other combat actions:
#1. A string describing the results
#2. The list of effects for each defender
#3. The actual action executed (i.e. self).
NUM_SPELL_CATEGORIES = 4
class Spell(combatAction.CombatAction):
    primaryStat = universal.TALENT
    targetType = None
    grappleStatus = None
    effectClass = None
    numTargets = 0
    cost = 0
    """
    Fields from CombatAction:
    grappleStatus = combatAction.GRAPPLER_ONLY
    statusInflicted = None
    effectClass = ALL
    grappleStatus = GRAPPLER_ONLY
    targetType = ALLY
    attacker = None
    defenders = []

    """
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(Spell, self).__init__(attacker, defenders, universal.MAGIC, secondaryStat)
        self.name = None
        self.description = None
        self.effectFormula = None
        self.cost = None
        self.numTargets = None
        self.spellType = None
        self.expertise = None
        #A list of strings that represents a single statement for when a particular enemy is immune to a spell.
        self.immuneStatement = []
        self.rawMagic = False
        self.tier = None
        self.magicMultiplier = None
        self.castableOutsideCombat = False

    def __str__(self):
        return self.name
    
    def _save(self):
        raise NotImplementedError()

    @staticmethod
    def _load(spellName):
        raise NotImplementedError()


    def __eq__(self, other):
        """
        A simple equality test that returns true iff the two spells have the same name.
        """
        if isinstance(other, Spell):
            return self.name == other.name
        else:
            #If we're comparing a spell to a combat action that is not a spell, then we use the equality test for combatActions.
            super(Spell, self).__eq__(other)

    def __neq__(self, other):
        return not self == other

    def outside_combat_effect(self):
        """
        It is assumed that a character removes any iron armor before casting a spell when not in combat, so the iron penalty doesn't apply.
        """
        return self.effect(False)

    @abc.abstractmethod
    def effect(self, inCombat=True, allies=None, enemies=None):
        if inCombat:
            self.attacker.uses_mana(self.cost)
        return
    @abc.abstractmethod
    def immune_statement(self, defender):
        return

    def spell_stats(self):
        return '\n'.join(['NAME: ' + self.name, 'DESCRIPTION: ' + self.description, 'TYPE: ' + print_spell_type(self.spellType), self.effectFormula, 'COST: ' + str(self.cost), 'TARGETS: ' + self.target_string(), 'AFFECTED BY IRON: ' + self.raw_magic_string(), 'CASTABLE WHEN GRAPPLING: ' + self.grappling_string()]) 

    def abbr_spell_stats(self):
        return '\n'.join([self.effectFormula, 'COST: ' + str(self.cost), 'AFFECTED BY IRON: ' + self.raw_magic_string()])

    def get_description(self):
        return self.spell_stats()

    def target_string(self):
        targetString = ''
        if self.numTargets == -1:
            targetString = 'All'
        else:
            targetString = str(self.numTargets)
        if self.targetType == combatAction.ENEMY:
            if self.numTargets == 1:
                targetString += ' enemy'
            else:
                targetString += ' enemies'
        elif self.targetType == combatAction.ALLY:
            if self.numTargets == 1:
                targetString += ' ally'
            else:
                targetString += ' allies'
        return targetString

    def raw_magic_string(self):
        if self.rawMagic:
            return 'yes'
        else:
            return 'no'

    def is_basic(self):
        return self.expertise == BASIC

    def is_advanced(self):
        return self.expertise == ADVANCED

    def is_expert(self):
        return self.expertise == EXPERT

    def basic_form(self):
        if self.is_advanced():
            return [s1 for (s1, s2, s3) in get_spells()[self.tier] if s2 == self][0]
        elif self.is_expert():
            return [s1 for (s1, s2, s3) in get_spells()[self.tier] if s3 == self][0]
        elif self.is_basic():
            return self

    def advanced_form(self):
        if self.is_basic():
            return [s2 for (s1, s2, s3) in get_spells()[self.tier] if s1 == self][0]
        elif self.is_expert():
            return [s2 for (s1, s2, s3) in get_spells()[self.tier] if s3 == self][0]
        elif self.is_advanced():
            return self

    def expert_form(self):
        if self.is_basic():
            return [s3 for (s1, s2, s3) in get_spells()[self.tier] if s1 == self][0]
        elif self.is_advanced():
            return [s3 for (s1, s2, s3) in get_spells()[self.tier] if s2 == self][0]
        elif self.is_expert():
            return self


def available_spells_in_tier(tier, person):
        spellList = get_spells()[tier]
        unrolledSpellList = [s for spellTuple in spellList for s in spellTuple]
        if person.spellList[tier] is None:
            return [s for s in unrolledSpellList if s.is_basic()]
        else:
            return [s for s in unrolledSpellList if s.is_basic() or (s.is_advanced() and s.basic_form() in person.spellList[tier]) or (s.is_expert() and 
                s.advanced_form() in person.spellList[tier] and person.is_specialized_in_spell_type(s.spellType))]

COMBAT = 0
STATUS = 1
BUFF = 2
SPECTRAL = 3

class Combat(Spell):
    targetType = ENEMY
    grappleStatus = None
    effectClass = None
    actionType = 'combat'
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(Combat, self).__init__(attacker, defenders, secondaryStat)
        self.minDamage = None
        #Deprecated. Do not use.
        self.spellType = COMBAT
        self.spellSchool = universal.COMBAT_MAGIC
        self.targetType = combatAction.ENEMY
        self.actionType = 'combat'

    def effect(self, inCombat=True, allies=None, enemies=None):
        super(Combat, self).effect(inCombat, allies, enemies)
        if not inCombat:
            return (['You can\'t cast', self.name, 'outside of combat.'], [], self)
        defenders = self.defenders
        attacker = self.attacker
        damage = 0
        effectString = []
        effects = []
        opponents = enemies if attacker in allies else allies
        currentDefenders = list(defenders)
        for defender in defenders:
            if not defender in opponents:
                availableOpponents = [opp for opp in opponents if opp not in currentDefenders]
                if availableOpponents == []:
                    continue
                else:
                    defender = availableOpponents[random.randrange(0, len(availableOpponents))]
                    currentDefenders.append(defender)
            damage = 0
            if not defender.ignores_spell(self):
                print('-------------------' + self.name + '------------------')
                print('magicMultiplier: ' + str(self.magicMultiplier))
                print('magic_attack: ' + str(attacker.magic_attack()))
                print('magic_defense: ' + str(defender.magic_defense(self.rawMagic)))
                try:
                    damage = random.randint(self.minDamage, self.magicMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic)))
                except ValueError:
                    damage = self.minDamage
                print('damage: ' + str(damage))
            defender.receives_damage(damage)
            effects.append(damage)
            if damage == 0:
                effectString.append(self.immune_string())
            else:
                effectString.append(self.effect_statement(defender, damage))
                if defender.current_health() <= 0:
                    effectString[-1] = '\n'.join([' '.join(effectString[-1]), ' '.join([defender.printedName, 'collapses!'])])
        return (universal.format_text(effectString), effects, self)

class Status(Spell):
    targetType = ENEMY
    grappleStatus = None
    effectClass = None
    statusInflicted = None
    primaryStat = universal.WILLPOWER
    secondaryStat = universal.TALENT
    actionType = 'status'
    def __init__(self, attacker, defenders, secondaryStat=universal.MAGIC):
        super(Status, self).__init__(attacker, defenders, secondaryStat)
        self.statusInflicted = None
        #This way, if we forget to set these values, we'll get an exception.
        self.minDuration = None
        self.magicMultiplier = None
        self.minProbability = None
        self.maxProbability = None
        self.willpowerMultiplier = None
        self.successStatement = []
        self.failureStatement = []
        self.spellType = STATUS #Deprecated. Do not use.
        self.spellSchool = universal.STATUS_MAGIC
        self.targetType = combatAction.ENEMY
        self.primaryStat = Status.primaryStat
        self.actionType = 'status'

    def effect(self, inCombat=True, allies=None, enemies=None):
        super(Status, self).effect(inCombat, allies, enemies)
        if not inCombat:
            return ['You can\'t cast', self.name, 'outside of combat.']
        defenders = self.defenders
        attacker = self.attacker
        resultString = []
        effects = []
        opponents = enemies if attacker in allies else allies
        currentDefenders = list(defenders)
        successProbability = 0
        for defender in defenders:
            if not defender in opponents:
                availableOpponents = [opp for opp in opponents if opp not in currentDefenders]
                if availableOpponents == []:
                    continue
                else:
                    defender = availableOpponents[random.randrange(0, len(availableOpponents))]
                    currentDefenders.append(defender)
            successProbability = self.resilienceMultiplier * (attacker.resilience() - attacker.magic_penalty() - defender.resilience())
            print('casing weaken')
            print("caster's resilience():")
            print(attacker.resilience())
            print("recipient's resilience():")
            print(defender.resilience())
            print('success probability:')
            print(successProbability)
            assert attacker.resilience() is not None, 'attacker has no resilience()'
            assert attacker.magic_penalty() is not None, 'attacker has no magic penalty'
            assert defender.resilience() is not None, 'defender has no resilience()'
            assert defender.magic_defense(self.rawMagic) is not None, 'defender has no magic defense'
            duration = self.magicMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
            resultString.append(self.effect_statement(defender))
            if defender.ignores_spell(self):
                resultString.append(self.immune_statement(defender))
            else:
                if successProbability < self.minProbability:
                    successProbability = self.minProbability
                elif successProbability > self.maxProbability:
                    successProbability = self.maxProbability
                assert successProbability is not None, 'no successProbability, likely because you forgot to set maxProbability.'
                if duration < self.minDuration:
                    duration = self.minDuration
                assert duration is not None, 'no min duration.'
                success = random.randint(1, 100)
                #print('casting' + str(self))
                #print('successProbability:' + str(successProbability))
                #print('success: ' + str(success))
                #print('resilienceMultiplier: ' + str(self.resilienceMultiplier))
                #print('attacker resilience(): ' + str(attacker.resilience()))
                #print('attacker magic penalty: ' + str(attacker.magic_penalty()))
                #print('defender resilience(): ' + str(defender.resilience()))
                #print('defender magic defense: ' + str(defender.magic_defense(self.rawMagic)))
                print('success probability:')
                print(successProbability)
                print('success:')
                print(success)
                print(success <= successProbability)
                if defender.ignores_spell(self):
                    resultString.append(self.immune_statement(defender))
                    effects.append(False)
                elif success <= successProbability:
                    resultString.append(self.success_statement(defender))
                    defender.inflict_status(statusEffects.build_status(self.statusInflicted, duration))
                    effects.append(True)
                else:
                    resultString.append(self.failure_statement(defender))
                    effects.append(False)
        return (universal.format_text(resultString, False), effects, self)

    @abc.abstractmethod
    def failure_statement(self, defender):
        """
            Use this method to gain access to a string that indicates that the spell failed due to chance rather than because the recipient is immune (for the immune 
            statement, define the immune_statement method).
        """
        return

    @abc.abstractmethod
    def success_statement(self, defender):
        """
            Use this method to gain access to a string that indicates that the spell succeeded.
        """
        return

class CharmMagic(Status):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    def effect(self, inCombat=True, allies=None, enemies=None):
        super(CharmMagic, self).effect(inCombat, allies, enemies)
        if not inCombat:
            return ['You can\'t cast', self.name, 'outside of combat.']
        if self.attacker in allies:
            #If the attacker is an ally (meaning in the party) then they're trying to charm an enemy.
            originalList = enemies
            newList = allies
        else:
            originalList = allies
            newList = enemies
        self.attacker.uses_mana(self.cost)
        defenders = self.defenders
        attacker = self.attacker
        resultString = []
        effects = []
        opponents = enemies if attacker in allies else allies
        currentDefenders = list(defenders)
        for defender in defenders:
            if not defender in opponents:
                availableOpponents = [opp for opp in opponents if opp not in currentDefenders]
                if availableOpponents == []:
                    continue
                else:
                    defender = availableOpponents[random.randrange(0, len(availableOpponents))]
                    currentDefenders.append(defender)
            successProbability = self.resilienceMultiplier * (attacker.resilience() - attacker.magic_penalty() - defender.resilience() - defender.magic_defense(self.rawMagic))
            duration = self.magicMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
            if defender.ignores_spell(self):
                resultString.append(self.immune_statement(defender))
            else:
                if successProbability < self.minProbability:
                    successProbability = self.minProbability
                elif successProbability > self.maxProbability:
                    successProbability = self.maxProbability
                if duration < minDuration:
                    duration = minDuration
                success = random.randint(1, 100)
                if person.ignores_spell(self):
                    resultString.append(self.immune_statement(defender))
                    effects.append(False)
                elif success <= successProbability:
                    resultString.append(self.effect_statement(defender))
                    resultString.append('\n')
                    resultString.append(self.success_statement(defender))
                    defender.inflict_status(statusEffects.build_status(self.statusInflicted, duration, originalList, newList))
                    effects.append(True)
                else:
                    resultString.append(self.failure_statement(defender))
                    effects.append(False)
        return (universal.format_text(resultString, False), effects, self)


class Buff(Spell):
    targetType = ALLY
    grappleStatus = None
    effectClass = None
    statusInflicted = None
    actionType = 'buff'
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(Buff, self).__init__(attacker, defenders, secondaryStat)
        self.targetType = combatAction.ALLY
        self.effectClass = None
        self.spellType  = BUFF #Deprecated. Do not use.
        self.spellSchool = universal.BUFF_MAGIC
        self.statusInflicted = None
        self.minDuration = None
        self.actionType = 'buff'
        self.castableOutsideCombat = True

    def effect(self, inCombat=True, allies=None, enemies=None):
        super(Buff, self).effect(inCombat, allies, enemies)
        recipients = self.defenders
        caster = self.attacker
        resultStatement = []
        effects = []
        companions = allies if caster in allies else enemies
        currentRecipients = list(recipients)
        for recipient in recipients:
            if recipient not in companions:
                availableRecipients = [comp for comp in companions if comp not in currentRecipients]
                if len(availableRecipients) == 0:
                    continue
                else:
                    recipient = availableRecipients[random.randrange(0, len(availableRecipients))]
                    availableRecipients.append(recipient)
            if caster != recipient:
                #The iron penalty applies only if we're currently in combat.
                duration = self.magicMultiplier * (caster.magic_attack(inCombat) + recipient.iron_modifier(self.rawMagic, inCombat))
                if duration < minDuration:
                    duration = minDuration
            else:
                #Because the buff spell is being cast on the caster, the magic never actually leaves the person's body, so it isn't affected by the caster's iron.
                duration = self.magicMultiplier * caster.magic_attack(False)
            if self.statusInflicted is not None:
                recipient.inflict_status(statusEffects.build_status(self.statusInflicted, duration))
            resultStatement.append(self.effect_statement(recipient))
            resultStatement.append(self.success_statement(recipient))
            print(resultStatement)
            effects.append(True)
        return (universal.format_text(resultStatement, False), effects, self)

    def success_statement(self, defender):
        """
            Use this method to gain access to a string that indicates that the spell succeeded.
        """
        return

class Healing(Buff):
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(Healing, self).__init__(attacker, defenders, secondaryStat)
        self.minHealedHealth = None
        #If fortify is true, then this healing spell can heal health past the character's maximum health.
        self.fortify = False
        self.fortifyCap = None

    def effect(self, inCombat=True, allies=None, enemies=None):
        #We don't want to invoke the effect function of Buff.
        super(Buff, self).effect(inCombat, allies, enemies)
        recipients = self.defenders
        caster = self.attacker
        resultStatement = []
        effects = []
        companions = []
        if inCombat:
            companions = allies if caster in allies else enemies
        else:
            companions = allies
        currentRecipients = list(recipients)
        for recipient in recipients:
            if recipient not in companions:
                availableRecipients = [comp for comp in companions if comp not in currentRecipients]
                if len(availableRecipients) == 0:
                    continue
                else:
                    recipient = availableRecipients[random.randrange(0, len(availableRecipients))]
                    availableRecipients.append(recipient)
            if recipient == caster:
                healedHealth = self.magicMultiplier * caster.magic_attack(False)
            else:
                healedHealth = self.magicMultiplier * (caster.magic_attack(inCombat) - recipient.iron_modifier(self.rawMagic, inCombat))
            if self.fortify and recipient.current_health() <= recipient.health() and healedHealth <= self.fortifyCap:
                if healedHealth < 0:
                    healedHealth = 1
                recipient.increase_stat(universal.CURRENT_HEALTH, healedHealth)
            else:
                if healedHealth < 0:
                    healedHealth = 1
                healedHealth = recipient.heals(healedHealth)
            resultStatement.append(self.effect_statement(recipient) + [caster.printedName, 'heals', recipient.printedName, 'for', str(healedHealth), 'health!'])
            effects.append(True)
        return (universal.format_text(resultStatement, False), effects, self)

class Resurrection(Healing):
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(Resurrection, self).__init__(attacker, defenders, secondaryStat)
        self.fortify = False
        self.fortifyCap = None

    def effect(self, inCombat=True, allies=None, enemies=None):
        raise NotImplementedError("Need to implement the effect for resurrection spells!")

class Spectral(Spell):
    targetType = None
    grappleStatus = None
    effectClass = None
    actionType = 'spectral'
    """
    Note: Because Spectral spells are so varied, we can't implement a generic effect function. Each spectral spell will have to implement its own.
    """
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(Spectral, self).__init__(attacker, defenders, secondaryStat)
        self.targetType = combatAction.ENEMY
        self.effectClass = None
        self.spellType = SPECTRAL #Deprecated. Do not use.
        self.spellSchool = universal.SPECTRAL_MAGIC
        self.actionType = 'spectral'


class SpectralSpanking(Spectral):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    tier = 0
    numTargets = 1
    statusInflicted = statusEffects.HUMILIATED
    cost = 2
    secondaryStat = universal.RESILIENCE
    def __init__(self, attacker, defenders):
        super(SpectralSpanking, self).__init__(attacker, defenders)
        self.name = 'Spectral Spanking'
        self.cost = SpectralSpanking.cost
        self.grappleStatus = combatAction.GRAPPLER_ONLY
        self.description = 'Conjures \'hands\' of raw magic. One hand grabs the target and lifts them into the air. The other lands a number of swats on the target\'s backside. Once the spanking is done, the first hand lifts the target up, and throws them into the ground. The spanking leaves your opponent distracted and humiliated, giving them a -1 penalty to all stats.'
        self.effectFormula = 'DURATION: 2 | 2 * (resilience - enemy resilience)\nDAMAGE: 1 | (magic - enemy magic),\nSuccess (%): 50 | 35 * (magic - enemy magic) | 95'
        self.numTargets = 1
        self.magicMultiplier = 1
        self.resilienceMultiplier = 2
        self.targetType = combatAction.ENEMY
        self.effectClass = combatAction.ALL
        self.statusInflicted = statusEffects.HUMILIATED
        self.rawMagic = True
        self.tier = SpectralSpanking.tier
        self.expertise = BASIC
        self.maxProbability = 95
        self.minProbability = 50
        self.probModifier = 35
        self.secondaryStat = SpectralSpanking.secondaryStat
        self.minDamage = 2
        self.minDuration = 2


    def effect(self, inCombat=True, allies=None, enemies=None, severity=0):
        """
        Returns a triple:
        1. A string describing what happened
        2. A pair indicating the damage done, and the number of smacks administered.
        3. This action.
        """
        super(SpectralSpanking, self).effect(inCombat, allies, enemies)
        opponents = enemies if self.attacker in allies else opponents
        currentDefenders = list(self.defenders)
        for defender in self.defenders:
            if not defender in opponents:
                availableOpponents = [opp for opp in opponents if opp not in currentDefenders]
                if availableOpponents == []:
                    continue
                else:
                    defender = availableOpponents[random.randrange(0, len(availableOpponents))]
                    currentDefenders.append(defender)
        defender = self.defenders[0]
        attacker = self.attacker
        damage = self.magicMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
        if damage < self.minDamage:
            damage = self.minDamage
        duration = self.resilienceMultiplier * (attacker.resilience() - defender.resilience() - defender.iron_modifier(self.rawMagic) + severity)
        if duration < self.minDuration:
            duration = self.minDuration
        print('spectral spanking duration:')
        print(duration)
        resultStatement = []
        effects = []
        effectString = self.effect_statement(defender)
        #resultStatement.append(self.effect_statement(defender))
        if defender.ignores_spell(self):
            resultStatement.append(self.immune_statement(defender))
            effects.append((0, 0))
        else:
            successProbability = self.probModifier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
            print(successProbability)
            if successProbability < self.minProbability:
                successProbability = self.minProbability
            if successProbability > self.maxProbability:
                successProbability = self.maxProbability
            print('spectral spanking success probability:')
            success = random.randint(1, 100)
            print('success:')
            print(success)
            if success <= successProbability:
                defender.inflict_status(statusEffects.build_status(statusEffects.HUMILIATED, duration=duration))
                defender.receives_damage(damage)
                resultStatement.append(self.success_statement(defender))
                effects.append(damage)
                effectString = effectString + [universal.format_line(self.success_statement(defender)), universal.format_line(['\n\n' + self.attacker.printedName, 'does', str(damage), 'damage to', defender.printedName + "!"])]
                if defender.current_health() <= 0:
                    resultStatement = [effectString  + ['\n' + defender.printedName + ' collapses!']]
                else:
                    resultStatement = [effectString]
            else:
                effects.append((0, 0))
                resultStatement = [self.failure_statement(defender)]
        return (universal.format_text(resultStatement, False), effects, self)

    def effect_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        self.effectStatements = [[A, 'holds up', hisher(attacker), 'hands. Giant ghostly shapes that vaguely resemble hands form above', himher(attacker), '.', 
            HeShe(attacker), 'throws out', hisher(attacker), 'hands in the direction of', D, '. Noticing this,', D, 
            'backs up rapidly and tries to find a way to avoid the spectral hands. Then,', A, 
            '\'s left hand snaps down and closes into a fist. The left ghostly hand snaps down and grabs at the back of', D,'\'s', defender.lower_clothing().name]]
        return super(SpectralSpanking, self).effect_statement(defender) 
    
    def immune_statement(self, defender):
        return ['The hand dissipates as soon as it touches', defender.printedName]

    def failure_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        return [D, 'just barely manages to slip through the hand\'s fingers.', A, 'tries to catch', D, ', but', heshe(defender), 'manages to stay one step ahead of the',
                'ghostly fingers until the hand finally fades.'] if not attacker.is_grappling(defender) else [D, '''pivots, forcing''', A, '''around so that''', A,
                        '''is between''', D, '''and the hand.''', A, '''tries to bring the hand around to grab''', D + ",", '''but''', D, '''manages to keep''', A, 
                        '''in the way until the hand fades.''']

    def success_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        return [A, 'lifts', hisher(attacker), 'hand into the air, and the spectral hand lifts', D, 'off the ground.', D, 'struggles desperately.', A, 'draws back', 
                hisher(attacker), 
                'right hand, and then snaps it forward. In perfect sync, the right spectral hand draws back, and then cracks against', defender.clad_bottom(), '.', D, 
                'yelps as a fiery sting spreads through', hisher(defender), 'bottom. The spectral hand proceeds to give', D, 'a solid spanking, making', D, 
                '\'s bottom bounce vigorously.\nEventually, the right hand fades.', A, 'raises', hisher(attacker), 
                'left hand, and then snaps it down. In response, the left spectral hand raises', D, 'into the air, and then flings', himher(defender), 'into the ground.'] 

#---------------------------------------Gender-specific functions---------------------------
def choose_string(person, male, female):
    return female if person.is_female() else male

def him_her(person=None):
    if person is None:
        person = universal.state.player
    return 'her' if person.is_female() else 'him' 
def his_her(person=None):
    if person is None:
        person = universal.state.player
    return 'her' if person.is_female() else 'his'
def He_She(person=None):
    if person is None:
        person = universal.state.player
    return 'She' if person.is_female() else 'He'

def himher(person=None):
    if person is None:
        person = universal.state.player
    return 'her' if person.is_female() else 'him' 

def HimHer(person=None):
    if person is None:
        person = universal.state.player
    return 'her' if person.is_female() else 'him' 

def hisher(person=None):
    if person is None:
        person = universal.state.player
    return 'her' if person.is_female() else 'his'

def HisHer(person=None):
    if person is None:
        person = universal.state.player
    return 'Her' if person.is_female() else 'His'

def heshe(person=None):
    if person is None:
        person = universal.state.player
    return 'she' if person.is_female() else 'he'

def HeShe(person=None):
    if person is None:
        person = universal.state.player
    return 'She' if person.is_female() else 'He'


def heshell(person=None):
    if person is None:
        person = universal.state.player
    return "she'll" if person.is_female() else "he'll"

def HeShell(person=None):
    if person is None:
        person = universal.state.player
    return "She'll" if person.is_female() else "He'll"

def himselfherself(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'himself', 'herself')

def HimselfHerself(person):
    return choose_string(person, 'Himself', 'Herself')

def mistermiss(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'mister', 'miss')

def MisterMiss(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Mister', 'Miss')

def manwoman(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'man', 'woman')

def ManWoman(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Man', 'Woman')


def menwomen(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'men', 'women')

def MenWomen(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Man', 'Woman')

def hishers(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'his', 'hers')

def HisHers(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'His', 'Hers')

def boygirl(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'boy', 'girl')

def BoyGirl(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Boy', 'Girl')

def manlady(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'man', 'lady')

def ManLady(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Man', 'Lady')

def kingqueen(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'king', 'queen')

def KingQueen(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'King', 'Queen')

def lordlady(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'lord', 'lady')

def LordLady(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Lord', 'Lady')

def brothersister(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'brother', 'sister')

def BrotherSister(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Brother', 'Sister')

def underwearpanties(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'underwear', 'panties')

def UnderwearPanties(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Underwear', 'Panties')

def thisthese(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'this', 'these')

def itthem(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'it', 'them')

def itthey(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'it', 'they')

def isare(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'is', 'are')

def UnderwearPanties(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Underwear', 'Panties')

def pigcow(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'pig', 'cow')
def PigCow(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Pig', 'Cow')

def sirmaam(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'sir', "ma'am")

def SirMaam(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Sir', "Ma'am")

def menwomen(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'men', 'women')


def MenWomen(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Men', 'Women')

def bastardbitch(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'bastard', 'bitch')

def BastardBitch(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Bastard', 'Bitch')

def ladlass(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'lad', 'lass')

def LadLass(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Lad', 'Lass')

def sondaughter(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'son', 'daughter')

def SonDaughter(person=None):
    if person is None:
        person = universal.state.player
    return choose_string(person, 'Son', 'Daughter')


#The following functions are used to simplify the LaTeX to Python translation. 

def muscle_adj(personName):
    return universal.state.get_character(personName).muscle_adj()

def bum_adj(personName):
    return universal.state.get_character(personName).bum_adj()

def quiver(personName):
    return universal.state.player.get_character(personName).quiver()

def quivering(personName):
    return universal.state.player.get_character(personName).quivering()


def stealth(personName):
    return universal.stat.get_character(personName).stealth()

def warfare(personName):
    return universal.stat.get_character(personName).warfare()

def magic(personName):
    return universal.stat.get_character(personName).magic()

def grapple(personName):
    return universal.stat.get_character(personName).grapple()

def resilience(personName):
    return universal.stat.get_character(personName).resilience()


def height_based_msg(person, shortMsg, avgMsg, tallMsg, hugeMsg):
    return universal.msg_selector(person.height, {HEIGHTS[0]:shortMsg, HEIGHTS[1]:avgMsg, HEIGHTS[2]:tallMsg, HEIGHTS[3]:hugeMsg})

def bodytype_based_msg(person, slimMsg, avgMsg, voluptuousMsg, heavysetMsg):
    return universal.msg_selector(person.bodytype, {BODY_TYPES[0]:slimMsg, BODY_TYPES[1]:avgMsg, BODY_TYPES[2]:voluptuousMsg, BODY_TYPES[3]:heavysetMsg})

def musculature_based_msg(person, softMsg, fitMsg, muscularMsg):
    return universal.msg_selector(person.musculature, {MUSCULATURE[0]:softMsg, MUSCULATURE[1]:fitMsg, MUSCULATURE[2]:muscularMsg})


def hair_length_based_msg(person, shortMsg, shoulderMsg, backMsg, buttMsg):
    return universal.msg_selector(person.hairLength, {HAIR_LENGTH[0]:shortMsg, HAIR_LENGTH[1]:shoulderMsg, HAIR_LENGTH[2]:backMsg, HAIR_LENGTH[3]:buttMsg})
