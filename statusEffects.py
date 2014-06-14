
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
import universal
from universal import *
import abc


HUMILIATED = 0
WEAKENED = 1
CHARMED = 2
MAGIC_DISTORTED = 3
SHIELDED = 4
MAGIC_SHIELDED = 5
LOWERED_DEFENSE = 6
LOWERED_MAGIC_DEFENSE = 7
DEFENSE = 8
FIRST_ORDER = 9
SECOND_ORDER = 10
THIRD_ORDER = 11
FOURTH_ORDER = 12

def is_negative(status):
    return status.isNegative

class StatusEffect(universal.RPGObject):
    """
        A status effect is a lingering effect that can inflict a character. Note
        that there are both positive (i.e. an effect that increases a character's
        defense) and negative (i.e. an effect that causes damage every round) 
        effects.
    """
    combatOnly = True
    name = ''

    def __init__(self, name, duration, combatOnly=True, isNegative=True):
        self.duration = duration
        self.name = name
        self.combatOnly = combatOnly
        self.isNegative = True

    @abc.abstractmethod
    def inflict_status(self, person):
        """
        inflictStatus(P) 
        inflicts the status on the person P. Note that some statuses (such as 
        reduceDefense) only affect a secondary skill, not a primary skill. Such
        effects need to return the penalty of the status. If a status affects a 
        primary skill, then the status should modify the primary skill directly,
        and return 0.
        """
        return

    @abc.abstractmethod
    def reverse_status(self, person):
        """
        reverseStatus(P) 
        should remove the status from P's list of status effects, and reverse any
        penalties imposed by the status.
        This should be the reverse of inflict status, so that after the following two calls:
        status.inflictStatus(person)
        status.reverseStatus(person)
        the state of the person should be unchanged
        """
        return

    def every_round(self, person):
        """
        This method gets called at the end of every combat round for every status in a given character's list of statuses. Only override this if you want your status to do 
        something every round.
        """
        return
    def _save(self):
        return '\n'.join(['begin_status', self.name(), str(self.duration), 'end_status']) 

    @staticmethod
    def _load(dataFile):
        effect = str.strip(dataFile[0])
        duration = int(str.strip(dataFile[1]))
        return factory(effect)(duration)

class Humiliated(StatusEffect):
    #The number of smacks that need to be landed to increase the penalty by another point. This can be varied for balancing.
    smacksPerPenaltyPoint = 5
    name = 'Humiliation'
    def __init__(self, duration, numSmacks):
        super(Humiliated, self).__init__(Humiliated.name, duration, True)
        self.penalty = numSmacks // Humiliated.smacksPerPenaltyPoint + 1

    def inflict_status(self, person):
        print(' '.join([person.name, 'before humiliation:']))
        print(person.statList)
        person.decrease_all_stats(self.penalty)
        print(' '.join([person.name, 'after humiliation:']))
        print(person.statList)
        return 0

    def reverse_status(self, person):
        print(' '.join([person.name, 'before reverse humiliation:']))
        print(person.statList)
        person.increase_all_stats(self.penalty)
        print(' '.join([person.name, 'before after humiliation:']))
        print(person.statList)
        return 0

class Weakened(StatusEffect):
    name = 'Weakness'
    def __init__(self, duration):
        super(Weakened, self).__init__(Weakened.name, duration, False)

    def inflict_status(self, person):
        print(' '.join([person.name, 'before weakened:']))
        print(person.statList)
        person.decrease_stat(WARFARE, 3)
        person.decrease_stat(GRAPPLE, 3)
        print(' '.join([person.name, 'after weakened:']))
        print(person.statList)
        return 0

    def reverse_status(self, person):
        print(' '.join([person.name, 'before reverse weakened:']))
        print(person.statList)
        person.increase_stat(WARFARE, 3)
        person.increase_stat(GRAPPLE, 3)
        print(' '.join([person.name, 'after reverse weakened:']))
        print(person.statList)
        return 0

class Shielded(StatusEffect):
    name = 'Shield'
    def __init__(self, duration, defenseBonus=2):
        super(Shielded, self).__init__(Shielded.name, duration, False, isNegative=False)
        self.defenseBonus = defenseBonus

        def inflict_status(self, person):
            return defenseBonus

        def reverse_status(self, person):
            """ 
            Since Shielded doesn't actually do anything to the person, it doesn't need to do anything.
            """
            return 0

class MagicShielded(StatusEffect):
    name = 'Magic Shield'
    def __init__(self, duration, defenseBonus=4):
        super(MagicShielded, self).__init__(MagicShielded.name, duration, False, isNegative=False)
        self.defenseBonus = defenseBonus

        def inflict_status(self, person):
            return defenseBonus

        def reverse_status(self, person):
            """ 
            Since MagicShielded doesn't actually do anything to the person, it doesn't need to do anything.
            """
            return 0


class MagicDistorted(StatusEffect):
    name = 'Magic Distorted'
    def __init__(self, duration, defenseBonus=4):
        super(MagicDistorted, self).__init__(MagicDistorted.name, duration, False)

    def inflict_status(self, person):
        person.decrease_stat(MAGIC, 3)
        return 0

    def reverse_status(self, person):
        person.increase_stat(MAGIC, 3)
        return 0

class Charmed(StatusEffect):
    name = 'Charmed'
    #Note: Technically charmed is negative, however we want the character to actively attack the party when charmed, rather than just defending.
    def __init__(self, duration, originalList, newList):
        super(Charmed, self).__init__(self, Charmed.name, duration, False, isNegative=False)
        self.allies = originalList
        self.enemies = newList

    def inflict_status(self, person):
        """
        Note: Charmed is rather unique, because it doesn't affect the character. Rather, it moves the character between the ally and enemy lists. Therefore, in order
        to activate the effect of charm, the combat engine needs to call inflict_charm and pass it the ally and enemy lists.
        """
        self.inflict_charm(person, self.allies, self.enemies)
        return 0

    def reverse_status(self, person):
        """
        See inflict status
        """
        self.reverse_charm(person, self.allies, self.enemies)
        return 0

    def inflict_charm(self, person, originalList, newList):
        """
            Moves the indicated person from originalList into newList.
        """
        for n in range(len(originalList)):
            if id(originalList[n]) == id(person):
                del originalList[n]
                break   
        newList.append(person)

    def reverse_charm(self, person, originalList, newList):
        """
        Same as inflict_charm, except it moves from the newList to the originalList.
        So if we call
        inflict_charm(person, allies, enemies)
        reverse_charm(person, allies, enemies)
        """
        self.inflict_charm(person, newList, originalList)

class LoweredDefense(StatusEffect):
    name = 'Lowered Defense'
    def __init__(self, duration, defensePenalty=4):
        super(LoweredDefense, self).__init__(LoweredDefense.name, duration, False)
        self.defensePenalty = 4

    def inflict_status(self, person):
        return self.defensePenalty

    def reverse_status(self, person):
        return 0

class LoweredMagicDefense(StatusEffect):
    name = 'Lowered Magic Defense'
    def __init__(self, duration, defensePenalty=4):
        super(LoweredDefense, self).__init__(LoweredDefense.name, duration, False)
        self.defensePenalty = 4

    def inflict_status(self, person):
        return self.defensePenalty

    def reverse_status(self, person):
        return 0

class DefendStatus(StatusEffect):
    combatOnly = True
    name = 'Defending'

    def __init__(self, duration):
        super(DefendStatus, self).__init__(DefendStatus.name, duration, isNegative=False)
    def inflict_status(self, p):
        """
        When a character is defending, they get a +3 bonus to warfare, grapple, willpower, and magic, to help them defend against enemy attacks.
        Note: This does not apply when a character is defending another character. This only works when a character is defending themselves.
        """
        print('inflicting defense status.')
        print('stats before defense:')
        print(p.statList)
        p.set_stat(WARFARE, p.warfare() + 3)
        p.set_stat(GRAPPLE, p.grapple() + 3)
        p.set_stat(WILLPOWER, p.willpower() + 3)
        p.set_stat(MAGIC, p.magic() + 3)
        print('stats after defense:')
        print(p.statList)
        return

    def reverse_status(self, p):
        print('reversing defense status.')
        print('stats before reversing defense:')
        print(p.statList)
        p.set_stat(WARFARE, p.warfare() - 3)
        p.set_stat(GRAPPLE, p.grapple() - 3)
        p.set_stat(WILLPOWER, p.willpower() - 3)
        p.set_stat(MAGIC, p.magic() - 3)
        print('stats after reversing defense:')
        print(p.statList)
        return

class FirstOrder(StatusEffect):
    combatOnly = True
    name = 'First Order'
    def __init__(self):
        super(FirstOrder, self).__init__(FirstOrder.name, 99, isNegative=True)

    def inflict_status(self, p):
        p.decrease_all_stats(1)

    def reverse_status(self, p):
        p.increase_all_stats(1)

class SecondOrder(StatusEffect):
    combatOnly = True
    name = 'Second Order'
    def __init__(self):
        super(SecondOrder, self).__init__(SecondOrder.name, 99, isNegative=False)

    def inflict_status(self, p):
        p.increase_all_stats(1)

    def reverse_status(self, p):
        p.decrease_all_stats(1)

class ThirdOrder(StatusEffect):
    combatOnly = True
    name = 'Third Order'
    def __init__(self):
        super(ThirdOrder, self).__init__(ThirdOrder.name, 10, isNegative=True)

    def inflict_status(self, p):
        pass

    def reverse_status(self, p):
        pass

    def every_round(self, person):
        """
        This method gets called at the end of every combat round for every status in a given character's list of statuses. Only override this if you want your status to do 
        something every round.
        """
        person.receives_damage(person.health() // 5)

class FourthOrder(StatusEffect):
    combatOnly = True
    name = 'Fourth Order'
    def __init__(self):
        super(FourthOrder, self).__init__(FourthOrder.name, 10, isNegative=False)

    def inflict_status(self, p):
        pass

    def reverse_status(self, p):
        pass

    def every_round(self, person):
        """
        This method gets called at the end of every combat round for every status in a given character's list of statuses. Only override this if you want your status to do 
        something every round.
        """
        person.heals(person.health() // 5)

def status_shorthand(statusName):
    if statusName == Humiliated.name:
        return 'H'
    elif statusName == Weakened.name:
        return 'W'
    elif statusName == Shielded.name:
        return 'S'
    elif statusName == MagicShielded.name:
        return 'MS'
    elif statusName == DefendStatus.name:
        return 'D'
    elif statusName == LoweredDefense.name:
        return 'LD'
    elif statusName == LoweredMagicDefense.name:
        return 'LMD'
    elif statusName == MagicDistorted.name:
        return 'MD'
    elif statusName == Charmed.name:
        return 'C'
    elif statusName == FirstOrder.name:
        return '1'
    elif statusName == SecondOrder.name:
        return '2'
    elif statusName == ThirdOrder.name:
        return '3'
    elif statusName == FourthOrder.name:
        return '4'

def get_name(status):
    if status == HUMILIATED:
        return Humiliated.name
    elif status == WEAKENED:
        return Weakened.name
    elif status == MAGIC_DISTORTED:
        return MagicDistorted.name
    elif status == SHIELDED:
        return Shielded.name
    elif status == MAGIC_SHIELDED:
        return MagicShielded.name
    elif status == LOWERED_DEFENSE:
        return LoweredDefense.name
    elif status == LOWERED_MAGIC_DEFENSE:
        return LoweredMagicDefense.name
    elif status == CHARMED:
        return Charmed.name
    elif status == FIRST_ORDER:
        return FirstOrder.name
    elif status == SECOND_ORDER:
        return SecondOrder.name
    elif status == THIRD_ORDER:
        return ThirdOrder.name
    elif status == FOURTH_ORDER:
        return FourthOrder.name

def build_status(status, duration=0, numSmacks=0, allies=None, enemies=None):
    """
        A factory function. Given an enum representing a status, returns the associated status. Raises a ValueError if the passed integer does not correspond to a particular
        status. Note: The numSmacks argument should only be used for the Humiliated status, since the severity of that status depends on how many blows the spanker managed
        to land on the spankee.
    """
    if status == HUMILIATED:
        return Humiliated(duration, numSmacks)
    elif status == WEAKENED:
        return Weakened(duration)
    elif status == MAGIC_DISTORTED:
        return MagicDistorted(duration)
    elif status == SHIELDED:
        return Shielded(duration)
    elif status == MAGIC_SHIELDED:
        return MagicShielded(duration)
    elif status == LOWERED_DEFENSE:
        return LoweredDefense(duration)
    elif status == LOWERED_MAGIC_DEFENSE:
        return LoweredMagicDefense(duration)
    elif status == CHARMED:
        return Charmed(duration, allies, enemies)
    elif status == FIRST_ORDER:
        return FirstOrder()
    elif status == SECOND_ORDER:
        return SecondOrder()
    elif status == THIRD_ORDER:
        return ThirdOrder()
    elif status == FOURTH_ORDER:
        return FourthOrder()
    else:
        if status == None:
            raise ValueError(' '.join(['None is not a status effect.'])) 
        else:
            raise ValueError(' '.join([str(status), 'is not a status effect.'])) 


    def __init__(self, duration):
        super(LoweredDefense, self).__init__(LoweredDefense.name, duration, False)
