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

MAGIC_PER_TIER = 3

allStats = [universal.WARFARE, universal.MAGIC, universal.WILLPOWER, universal.GRAPPLE, universal.STEALTH, universal.HEALTH, universal.MANA, universal.CURRENT_HEALTH, 
        universal.CURRENT_MANA]

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

PC = universal.state.player
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
    elif stat == universal.WILLPOWER:
        return 'willpower'
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
NUM_EQUIP_SLOTS = 4
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
    willpower
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
class Person(universal.RPGObject): 
    """
        People are complicated.
    """
    def __init__(self, name, gender, defaultLitany, litany, description="", printedName=None, 
            coins=20, specialization=universal.BALANCED, order=zeroth_order, dropChance=0, rawName=None): 
        self.name = name
        self.gender = gender
        if type(description) is list:
            self.description = description
        else:
            self.description = [description]
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
        self.statList = [1 for i in range(len(allStats))]
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
        self.chanceIncrease = [0 for i in range(len(allStats) + NUM_SPELL_CATEGORIES)]
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
        universal.state.add_character(self)

    def __getstate__(self):
        originalOrder = self.order
        self.order = order_name(self.order)
        result = self.__dict__.copy()
        self.order = originalOrder
        return result

    def __setstate__(self, dictIn):
        self.__dict__ = dictIn
        self.order = order_function(self.order)

    def get_core_stats(self):
        return self.statList[:-2]

    def get_battle_stats(self):
        """Returns all the stats except for health, mana, current health, current mana
        """
        return self.statList[:-4]

    def set_default_stats(self):
        self.set_all_stats(warfare=1, grapple=1, willpower=1, magic=1, stealth=1, health=10, mana=10)

    def set_state(self, original):
        for attribute in vars(original).keys():
            if attribute != 'origSelf':
                setattr(self, attribute, copy.deepcopy(vars(original)[attribute]))
        """
        self.name = original.name
        self.gender = original.gender
        self.description = original.description
        self.statusList = original.statusList
        self.spellList = original.spellList
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
        elif self.specialization == universal.GRAPPLE and stat == universal.WILLPOWER:
            return True
        elif self.specialization == universal.MAGIC and stat == universal.WARFARE:
            return True
        elif self.specialization == universal.WILLPOWER and stat == universal.GRAPPLE:
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
        return self.rawName + ".person"

    def __eq__(self, other):
        """
        A very simple equality that assumes that two characters are the same iff they have the same or they have the same name. Note that this means this will not 
        work for generic enemies, or rather it would view two different instances of generic enemies as the same person.
        """
        try:
            return id(self) == id(other) or self.get_id() == other.get_id()
        except AttributeError:
            return False

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
        if not item in self.inventory:
            self.inventory.append(item)

    def drop_item(self, item):
        successfulUnequip = True
        if not item in self.inventory:
            successfulUnequip = self.unequip(item)
        try:
            self.inventory.remove(item)
        except ValueError:
            pass
        return successfulUnequip

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
        self.specialization == specialization

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
        self.gender = gender

    def set_stat(self, stat, num):
        self.statList[stat] = num

    def set_all_stats(self, warfare=None, willpower=None, magic=None, grapple=None, stealth=None, health=None, mana=None):
        if warfare is not None:
            self.statList[universal.WARFARE] = warfare
        if willpower is not None:
            self.statList[universal.WILLPOWER] = willpower
        if magic is not None:
            self.statList[universal.MAGIC] = magic
        if grapple is not None:
            self.statList[universal.GRAPPLE] = grapple
        if stealth is not None:
            self.statList[universal.STEALTH] = stealth
        if health is not None:
            self.statList[universal.HEALTH] = health
        if mana is not None:
            self.statList[universal.MANA] = mana
        if health is not None:
            self.statList[universal.CURRENT_HEALTH] = health
        if mana is not None:
            self.statList[universal.CURRENT_MANA] = mana

    def increase_stat(self, stat, increment):
        self.set_stat(stat, self.statList[stat] + increment)

    def improve_stat(self, stat, increment):
        self.increase_stat(stat, increment)
        oldTier = self.tier
        self.tier = self.magic() // MAGIC_PER_TIER
        if self.tier > oldTier:
            magicSchool = get_spell_index(self.specialization) if self.specialized_in_magic() else -1
            if magicSchool >= 0:
                self.learn_spell(allSpells[self.tier][magicSchool][0])
                universal.say(universal.format_line(['\n' + self.name, 'has learned the', allSpells[self.tier][magicSchool][0].name, 'spell!']))

    def reduce_stat(self, stat, increment): 
        decrease_stat(self, stat, increment)
        tier = self.magic() // MAGIC_PER_TIER

    def specialized_in_magic(self):
        return self.specialization == COMBAT_MAGIC or self.specialization == STATUS_MAGIC or self.specialization == BUFF_MAGIC or self.specialization == SPECTRAL_MAGIC

    def increment_stat(self, stat):
        self.increase_stat(stat, 1)

    def increase_all_stats(self, increment):
        self.set_all_stats(warfare + increment, willpower + increment, magic + increment, grapple + increment, stealth + increment)

    def decrease_all_stats(self, decrement):
        self.increase_all_stats(-decrement)


    def equip(self, equipment): 
        oldEquipment = None
        if isinstance(equipment, items.Weapon):
            if self.equipmentList[WEAPON] != items.emptyWeapon:
                oldEquipment = self.equipmentList[WEAPON]
                self.inventory.append(self.equipmentList[WEAPON])
            self.equipmentList[WEAPON] = equipment
        elif isinstance(equipment, items.LowerArmor):
            if self.equipmentList[LOWER_CLOTHING] != items.emptyLowerArmor:
                self.inventory.append(self.equipmentList[LOWER_CLOTHING])
                oldEquipment = self.equipmentList[LOWER_CLOTHING]
            self.equipmentList[LOWER_CLOTHING] = equipment
        elif isinstance(equipment, items.UpperArmor):
            if self.equipmentList[SHIRT] != items.emptyUpperArmor:
                self.inventory.append(self.equipmentList[SHIRT])
                oldEquipment = self.equipmentList[SHIRT]
            self.equipmentList[SHIRT] = equipment
        elif isinstance(equipment, items.Underwear):
            if self.equipmentList[UNDERWEAR] != items.emptyUnderwear:
                self.inventory.append(self.equipmentList[UNDERWEAR])
                oldEquipment = self.equipmentList[UNDERWEAR]
            self.equipmentList[UNDERWEAR] = equipment
        elif isinstance(equipment, items.FullArmor):
            if self.equipmentList[LOWER_CLOTHING] != items.emptyLowerArmor:
                self.inventory.append(self.equipmentList[LOWER_CLOTHING])
                oldEquipment = self.equipmentList[LOWER_CLOTHING]
            self.equipmentList[LOWER_CLOTHING] = equipment
            if self.equipmentList[SHIRT] != items.emptyUpperArmor and not isinstance(self.equipmentList[SHIRT], items.FullArmor):
                self.inventory.append(self.equipmentList[SHIRT])
                oldEquipment = self.equipmentList[SHIRT]
            self.equipmentList[SHIRT] = equipment
        else:
            raise InvalidEquipmentError(' '.join([equipment.name, 'is not equippable.']))
        if equipment in self.inventory:
            self.inventory.remove(equipment)
        equipment.apply_bonuses(self)
        if oldEquipment is not None:
            oldEquipment.remove_bonuses(self)

    def unequip(self, equipment):
        empty = None
        try: 
            equipment == WEAPON
        except AttributeError:
            equipment = self.equipmentList.index(equipment)
        if equipment == WEAPON and self.equipmentList[WEAPON].name != items.emptyWeapon.name:
            empty = items.emptyWeapon
        elif equipment == LOWER_CLOTHING and self.equipmentList[LOWER_CLOTHING].name != items.emptyLowerArmor.name:
            empty = items.emptyLowerArmor
            if self.underwear().name == items.emptyUnderwear.name:
                universal.clear_screen()
                universal.say(universal.format_line([self.printedName, '''begins to remove''', hisher(), self.lower_clothing().name, '''only to realize that''', heshe(),
                    '''is not wearing any underwear. In the interests of modesty,''', heshe(), '''decides to keep''', hisher(), self.lower_clothing().name, '''on.''']))
                acknowledge(self.character_sheet, None)
                return None
        elif equipment == UNDERWEAR and self.equipmentList[UNDERWEAR].name != items.emptyUnderwear.name:
            empty = items.emptyUnderwear
            if self.lower_clothing().name == items.emptyLowerArmor.name:
                universal.clear_screen()
                universal.say(universal.format_line([self.printedName, '''begins to remove''', hisher(), self.underwear().name, '''only to realize that''', heshe(),
                    '''is not wearing any pants. In the interests of modesty,''', heshe(), '''decides to keep''', hisher(), self.underwear().name, '''on.''']))
                acknowledge(self.character_sheet, None)
                return None
        elif equipment == SHIRT and self.equipmentList[SHIRT].name != items.emptyUpperArmor.name:
            empty = items.emptyUpperArmor
        if empty is not None:
            self.inventory.append(self.equipmentList[equipment])
            self.equipmentList[equipment] = empty
        return empty is not None

    def display_equipment(self, slot):
        universal.say(self.equipmentList[slot].display())
        set_commands(['<==Back'])
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
        for stat in range(len(self.statList)):
            if stat != universal.HEALTH and stat != universal.MANA and stat != universal.CURRENT_MANA and stat != universal.CURRENT_HEALTH:
                self.statList[stat] += num


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

    def set_copy(self):
        self.origSelf = copy.deepcopy(self)

    def reset(self):
        self.set_state(self.origSelf)
        return self

    def reset_stats(self, episode=None, statList=None):
        if statList is None:
            self.default_stats()
        else:
            self.statList = copy.deepcopy(statList) 
        self.tier = self.magic() // MAGIC_PER_TIER

    def default_stats(self):
        """
        Override this if we want a particular character to have different default stats.
        """
        self.set_all_stats(1, 1, 1, 1, 1, 15, 10)

    def get_stat(self, stat):
        return int(self.statList[stat])
    def warfare(self):
        return int(self.statList[universal.WARFARE])
    def magic(self):
        return int(self.statList[universal.MAGIC])
    def willpower(self):
        return int(self.statList[universal.WILLPOWER])
    def grapple(self, person=None):
        """
        If person is none, we want the value of the grapple stat. If person is not None, then we want to start grappling that person.
        """
        if person is not None:
            self.grapplingPartner = person
            person.grapplingPartner = self
        else:
            return int(self.statList[universal.GRAPPLE])
    def break_grapple(self):
        gp = self.grapplingPartner
        self.grapplingPartner = None
        if gp is not None:
            gp.grapplingPartner = None

    def stealth(self):
        return int(self.statList[universal.STEALTH])
    def health(self):
        return int(self.statList[universal.HEALTH])
    def mana(self):
        return int(self.statList[universal.MANA])
    def current_health(self):
        return int(self.statList[universal.CURRENT_HEALTH])
    def current_mana(self):
        return int(self.statList[universal.CURRENT_MANA])
    def stat(self, statIn):
        return int(self.statList[statIn])

    def equipment(self, slot):
        return self.equipmentList[slot]

    def weapon(self):
        return self.equipmentList[WEAPON]
    def shirt(self):
        return self.equipmentList[SHIRT]
    def lower_clothing(self):
        return self.equipmentList[LOWER_CLOTHING]

    def worn_lower_clothing(self):
        return self.lower_clothing().name if self.lower_clothing() != items.emptyLowerArmor else self.underwear().name

    def lower_clothing_type(self):
        return self.lower_clothing().armorType if self.lower_clothing().name != items.emptyLowerArmor.name else self.lower_clothing().armorType

    def clad_bottom(self, useName=True):
        return (hisher(self) + (" " + self.underwear().name + "-clad bottom" if self.underwear() != items.emptyUnderwear else self.lower_clothing_type() + " bottom") 
                if self.lower_clothing() == items.emptyLowerArmor else "the seat of " + (self.printedName + "'s" if useName else hisher(self)) + " " + 
                self.lower_clothing_type())

    def clothing_below_the_waist(self):         
        return self.underwear() if self.lower_clothing().name == items.emptyLowerArmor.name else self.lower_clothing()
    
    def underwear(self):
        return self.equipmentList[UNDERWEAR]

    def display_main_stats(self):
        #Don't include health or mana initially
        statList = [': '.join([stat_name(stat), str(statValue)]) for (stat, statValue) in zip([i for i in range(0, len(self.statList)-4)], self.statList)] 
        statList.append('health: ' + str(self.statList[-2]) + '/' + str(self.statList[-4]))
        statList.append('mana: '   + str(self.statList[-1]) + '/' + str(self.statList[-3]))
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

    def magic_defense_modifier(self, rawMagic):
        return self.magic() + self.magic_defense_bonus() + (self.magic_penalty() if rawMagic else 0)

    def defense(self):
        if self.is_grappling():
            return self.grapple() // 2 + self.defense_bonus()
        else:
            return self.warfare() // 2 + self.defense_bonus()

    def magic_penalty(self, rawMagic=True):
        return self.weapon().castingPenalty + self.shirt().castingPenalty + self.lower_clothing().castingPenalty + self.underwear().castingPenalty

    def magic_defense(self, rawMagic):
        return self.magic_defense_modifier(rawMagic)

    def magic_defense_bonus(self):
        defenseBonus = 0
        if statusEffects.LoweredMagicDefense.name in self.statusList:
            defenseBonus = self.statusList[statusEffects.LoweredMagicDefense.name][0].inflict_status(self)
        if statusEffects.MagicShielded.name in self.statusList: 
            print('magic defense bonus:')
            print(self.weapon().magicDefense)
            print(self.shirt().magicDefense)
            print(self.lower_clothing().magicDefense)
            print(self.underwear().magicDefense)
            print(defenseBonus)
            print(self.statusList[statusEffects.MagicShielded.name][STATUS_OBJ])
            print(self.statusList[statusEffects.MagicShielded.name][STATUS_OBJ])
            print(self.statusList[statusEffects.MagicShielded.name][STATUS_OBJ].inflict_status(self))
            print(self.statusList[statusEffects.MagicShielded.name][STATUS_OBJ].inflict_status)
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
    

    def _save(self):
        raise NotImplementedError()
    @staticmethod
    def _load(data, personType='person'):
        raise NotImplementedError()

    def character_sheet_spells(self):
        return '\n'.join(['Name: ' + self.name, 'Order: ' + order_name(self.order),  self.display_stats(), 'Spells: ', self.display_spells()])

    def character_sheet(self, mode=None):
        """
            In addition to listing the character's statistics and inventory, this function also sets the commands and command interpreter for studying the character in
            more detail
        """
        global currentMode
        if mode is not None:
            currentMode = mode
        global currentPerson
        currentPerson = self
        say_title(self.name)
        universal.say('\n'.join(['Order: ' + order_name(self.order), 'Status: ' + self.display_statusList(), 'Defense: ' + str(self.defense()), 
            'Magic Defense: ' + str(self.magic_defense(False)),
            #'Exp to Next Level: ' + str(self.level * XP_INCREASE_PER_LEVEL - self.experience),
            self.display_stats(), '\t']))
        universal.say('\n'.join(['Weapon: ' + self.weapon().name, 'Chest: ' + self.shirt().name, 'Legs: ' + self.lower_clothing().name, 
            'Underwear: ' + self.underwear().name, self.display_inventory()]), columnNum=2)
        set_commands(['(S)pells', '(E)quip', '(#)view item', '(W)eapon', '(C)hest', '(L)egs', '(U)nderwear', '<==Back']) 
        set_command_interpreter(character_viewer_interpreter)

    def display_inventory(self):
        if self.inventory is None:
            return 'Inventory:'
        else:
            return '\n'.join(['', 'Inventory:', ' '.join(str(n) + '. ' + item.name for 
                (n, item) in zip([i for i in range(1, len(self.inventory)+1)], self.inventory))])

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
        set_commands(['(#) Select item to equip:_', 'Unequip (W)eapon', 'Unequip (C)hest', 'Unequip (L)egs', 'Unequip (U)nderwear', '<==Back', '(Esc) Return to menu'])
        global selectedPerson
        selectedPerson = self
        set_command_interpreter(equip_interpreter)


    @staticmethod
    def _get_load_data(loadData, lineNum, endLine):
        data = []
        while loadData[lineNum] != endLine:
            data.append(loadData[lineNum])
            lineNum += 1
        return (data, lineNum)

equipNum = ''
selectedPerson = None
def equip_interpreter(keyEvent):
    global equipNum
    if keyEvent.key in NUMBER_KEYS:
        num = int(pygame.key.name(keyEvent.key)) - 1
        if 0 < num and num <= len(selectedPerson.inventory): 
            if len(selectedPerson.inventory) < 10:
                try:
                    selectedPerson.equip(selectedPerson.inventory[num])
                except InvalidEquipmentError:
                    universal.say('''That cannot be equipped!''')
                    acknowledge(selectedPerson.equip_menu, ())
                    return
            else:
                equipNum += pygame.key.name(playerInput)
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
        num = int(equipNum)
        if 0 < num and num <= len(selectedPerson.inventory):
            try:
                selectedPerson.equip(selectedPerson.inventory[num])
            except InvalidEquipmentError:
                say('''That cannot be equipppe!''')
                acknowledge(selectedPerson.equip_menu, ())
                return
    elif keyEvent.key == K_w:
        result = selectedPerson.unequip(WEAPON)
    elif keyEvent.key == K_c:
        result = selectedPerson.unequip(SHIRT)
    elif keyEvent.key == K_l:
        result = selectedPerson.unequip(LOWER_CLOTHING)
    elif keyEvent.key == K_u:
        result = selectedPerson.unequip(UNDERWEAR)
    try:
        if result is not None:
            selectedPerson.character_sheet()
            selectedPerson.equip_menu()
    except UnboundLocalError:
        pass

                

class PlayerCharacter(Person):
    """
    In addition to all the information a person usually has, a PlayerCharacter has a list of keywords that track game progression.
    Also the spanking methods have been overriden so that they call the appropriate methods of the other character, i.e. failed_to_spank(self, person) calls 
    person.avoided_spanking_by(self). Note that this SHOULD NOT be done by other characters. If we had two different characters with these functions implemented this way,
    and one got Charmed, and tried to spank the other, we'd get infinite function calls.

    This is only allowed for the player character because there should be only one in any given episode (though there's no reason why there couldn't be more than one across
    the entire game, so long as the two never fight each other).
    """
    def __init__(self, name, gender, description="", currentEpisode=None, order=sixth_order, nickname=""):
        super(PlayerCharacter, self).__init__(name, gender, None, None, description=description, order=zeroth_order, rawName='$$$PC$$$')
        self.keywords = []
        self.currentEpisode = currentEpisode
        self.numSpankings = 0
        self.numSpankingsGiven = 0
        self.coins = 20
        self.fakeName = ''
        self.set_copy()
        self.nickname = nickname

    def get_id(self):
        return self.rawName + ".playerCharacter"

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

    def _save(self):
        raise NotImplementedError()

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
partialNum = ''
def character_viewer_interpreter(keyEvent):     
    global partialNum
    #set_commands(['(S)pells, (E)quip, (#)View Item, (W)eapon, S(H)irt, (L)ower Clothing, (U)nderwear, <==Back']) 
    if keyEvent.key == K_BACKSPACE:
        currentMode()
    elif keyEvent.key == K_s:
        currentPerson.display_tiers()
    elif keyEvent.key == K_e:
        currentPerson.equip_menu()
    elif keyEvent.key == K_w:
        currentPerson.display_equipment(WEAPON)
    elif keyEvent.key == K_c:
        currentPerson.display_equipment(SHIRT)
    elif keyEvent.key == K_l:
        currentPerson.display_equipment(LOWER_CLOTHING)
    elif keyEvent.key == K_u:
        currentPerson.display_equipment(UNDERWEAR)
    elif keyEvent.key in NUMBER_KEYS:
        if len(currentPerson.inventory) < 10:
            num = int(pygame.key.name(keyEvent.key))
            if currentPerson.inventory is not None and 0 < num \
            and num <= len(currentPerson.inventory):
                universal.say(currentPerson.inventory[num-1].display())
                set_commands(['<==Back'])
                set_command_interpreter(view_item_interpreter)
        else:
            partialNum += pygame.key.name(keyEvent.key)
    elif keyEvent.key == K_RETURN and len(currentPerson.inventory) >= 10:
        num = int(partialNum)
        universal.say(currentPerson.inventory[num-1].display())
        set_commands(['<==Back'])
        set_command_interpreter(view_item_interpreter)

def view_item_interpreter(keyEvent):
    if keyEvent.key == K_BACKSPACE:
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
        if member in self.members:
            self.members.remove(member)
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
                + memberName, str(member.current_health()) + '/' + str(member.health()), 
                str(member.current_mana()) + '/' + str(member.mana())]) 
                for (n, member, memberName) in zip([i for i in range(1, len(self.members)+1)], self.members, memberNames)]
            if grappling:
                partyTxt = ['\t'.join([memTxt, display_person(mem.grapplingPartner)]) 
                    for (memTxt, mem) in zip(partyTxt, self.members)]
            return '\n'.join(partyTxt)
        else:
            return '\t'.join([target(n, arrow(n, allyIndex), targetedIndices) + '. ' + 
                '\n' + memberName for (n, member, memberName) in 
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

#This is a list of list tuples. Each list of tuples is all the spells in that particular tier.
allSpells = [None for i in range(universal.NUM_TIERS)]
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
    primaryStat = universal.MAGIC
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
                #print('-------------------' + self.name + '------------------')
                #print('magicMultiplier: ' + str(self.magicMultiplier))
                #print('magic_attack: ' + str(attacker.magic_attack()))
                #print('magic_defense: ' + str(attacker.magic_defense(self.rawMagic)))
                damage = self.magicMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
                #print('damage: ' + str(damage))
                if damage < self.minDamage:
                    damage = self.minDamage
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
    secondaryStat = universal.MAGIC
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
            successProbability = self.willpowerMultiplier * (attacker.willpower() - attacker.magic_penalty() - defender.willpower())
            print('casing weaken')
            print("caster's willpower:")
            print(attacker.willpower())
            print("recipient's willpower:")
            print(defender.willpower())
            print('success probability:')
            print(successProbability)
            assert attacker.willpower() is not None, 'attacker has no willpower'
            assert attacker.magic_penalty() is not None, 'attacker has no magic penalty'
            assert defender.willpower() is not None, 'defender has no willpower'
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
                #print('willpowerMultiplier: ' + str(self.willpowerMultiplier))
                #print('attacker willpower: ' + str(attacker.willpower()))
                #print('attacker magic penalty: ' + str(attacker.magic_penalty()))
                #print('defender willpower: ' + str(defender.willpower()))
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
            successProbability = self.willpowerMultiplier * (attacker.willpower() - attacker.magic_penalty() - defender.willpower() - defender.magic_defense(self.rawMagic))
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
    tier = 1
    numTargets = 1
    statusInflicted = statusEffects.HUMILIATED
    cost = 8
    secondaryStat = universal.WILLPOWER
    def __init__(self, attacker, defenders):
        super(SpectralSpanking, self).__init__(attacker, defenders)
        self.name = 'Spectral Spanking'
        self.cost = SpectralSpanking.cost
        self.grappleStatus = combatAction.GRAPPLER_ONLY
        self.description = 'Conjures \'hands\' of raw magic. One hand grabs the target and lifts them into the air. The other lands a number of swats on the target\'s backside. Once the spanking is done, the first hand lifts the target up, and throws them into the ground.'
        self.effectFormula = 'NUMBER OF SMACKS: 5 | 5 * (magic - enemy magic), \nHUMILIATION DURATION: 2 | 2 * (willpower - enemy willpower)\nDAMAGE: 2 | 2 * (magic - enemy magic),\nSuccess (%): 40 | 30 * (magic - enemy magic) | 95'
        self.numTargets = 1
        self.magicMultiplier = 2
        self.smackMultiplier = 5
        self.willpowerMultiplier = 2
        self.targetType = combatAction.ENEMY
        self.effectClass = combatAction.ALL
        self.statusInflicted = statusEffects.HUMILIATED
        self.rawMagic = True
        self.tier = SpectralSpanking.tier
        self.expertise = BASIC
        self.maxProbability = 95
        self.minProbability = 40
        self.probModifier = 30
        self.secondaryStat = SpectralSpanking.secondaryStat
        self.minDamage = 2


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
        numSmacks = self.smackMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
        duration = self.willpowerMultiplier * (attacker.willpower() - defender.willpower() - defender.iron_modifier(self.rawMagic) + severity)
        resultStatement = []
        effects = []
        effectString = self.effect_statement(defender)
        #resultStatement.append(self.effect_statement(defender))
        if defender.ignores_spell(self):
            resultStatement.append(self.immune_statement(defender))
            effects.append((0, 0))
        else:
            successProbability = self.probModifier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))
            if successProbability < self.minProbability:
                successProbability = self.minProbability
            if successProbability > self.maxProbability:
                successProbability = self.maxProbability
            success = random.randint(1, 100)
            if success <= successProbability:
                defender.inflict_status(statusEffects.build_status(statusEffects.HUMILIATED, numSmacks))
                defender.receives_damage(damage)
                resultStatement.append(self.success_statement(defender))
                effects.append((damage, numSmacks))
                effectString = effectString + [universal.format_line(self.success_statement(defender)), universal.format_line(['\n' + self.attacker.printedName, 'does', str(damage), 'damage to', defender.printedName + "!"])]
                if defender.current_health() <= 0:
                    resultStatement = [effectString  + [defender.printedName + ' collapses!']]
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
        person = PC
    return 'her' if person.is_female() else 'him' 
def his_her(person=None):
    if person is None:
        person = PC
    return 'her' if person.is_female() else 'his'
def He_She(person=None):
    if person is None:
        person = PC
    return 'She' if person.is_female() else 'He'

def himher(person=None):
    if person is None:
        person = PC
    return 'her' if person.is_female() else 'him' 

def HimHer(person=None):
    if person is None:
        person = PC
    return 'her' if person.is_female() else 'him' 

def hisher(person=None):
    if person is None:
        person = PC
    return 'her' if person.is_female() else 'his'

def HisHer(person=None):
    if person is None:
        person = PC
    return 'Her' if person.is_female() else 'His'

def heshe(person=None):
    if person is None:
        person = PC
    return 'she' if person.is_female() else 'he'

def HeShe(person=None):
    if person is None:
        person = PC
    return 'She' if person.is_female() else 'He'

def himselfherself(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'himself', 'herself')

def HimselfHerself(person):
    return choose_string(person, 'Himself', 'Herself')

def mistermiss(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'mister', 'miss')

def MisterMiss(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Mister', 'Miss')

def manwoman(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'man', 'woman')

def ManWoman(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Man', 'Woman')


def menwomen(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'men', 'women')

def MenWomen(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Man', 'Woman')

def hishers(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'his', 'hers')

def HisHers(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'His', 'Hers')

def boygirl(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'boy', 'girl')

def BoyGirl(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Boy', 'Girl')

def manlady(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'man', 'lady')

def ManLady(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Man', 'Lady')

def kingqueen(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'king', 'queen')

def KingQueen(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'King', 'Queen')

def lordlady(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'lord', 'lady')

def LordLady(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Lord', 'Lady')

def brothersister(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'brother', 'sister')

def BrotherSister(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Brother', 'Sister')

def underwearpanties(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'underwear', 'panties')

def UnderwearPanties(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Underwear', 'Panties')

def thisthese(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'this', 'these')

def itthem(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'it', 'them')

def itthey(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'it', 'they')

def isare(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'is', 'are')

def UnderwearPanties(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Underwear', 'Panties')

def pigcow(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'pig', 'cow')
def PigCow(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Pig', 'Cow')

def sirmaam(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'sir', "ma'am")

def SirMaam(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Sir', "Ma'am")

def menwomen(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'men', 'women')


def MenWomen(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Men', 'Women')

def bastardbitch(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'bastard', 'bitch')

def BastardBitch(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Bastard', 'Bitch')

def ladlass(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'lad', 'lass')

def LadLass(person=None):
    if person is None:
        person = PC
    return choose_string(person, 'Lad', 'Lass')

