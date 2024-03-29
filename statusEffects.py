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
STRIKE_TRUE = 13
STRIKE_POOR = 14

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
        self.isNegative = isNegative

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
        pass

    def every_round(self, person):
        """
        This method gets called at the end of every combat round for every status in a given character's list of statuses. Only override this if you want your status to do 
        something every round.
        """
        return
    def save(self):
        return '\n'.join(["Status Data:", self.name, str(self.duration)]) 

    @staticmethod
    def load(statusData, status):
        _, name, duration = (data.strip() for data in statusData.split('\n') if data.strip())
        status.name = name
        status.duration = duration

    @staticmethod
    def _load(dataFile):
        effect = str.strip(dataFile[0])
        duration = int(str.strip(dataFile[1]))
        return build_status(effect)(duration)

class Humiliated(StatusEffect):
    #The number of smacks that need to be landed to increase the penalty by another point. This can be varied for balancing.
    smacksPerPenaltyPoint = 1
    name = 'Humiliation'
    def __init__(self, duration):
        super(Humiliated, self).__init__(Humiliated.name, duration, True)
        self.penaltyPerRound = 1
        self.inflictedStat = None
        self.rounds = 1

    def increase_status(self, person, severity=0):
        person.decrease_stat(self.inflictedStat, self.penaltyPerRound + severity)
        self.rounds += 1
        return 0

    def inflict_status(self, person):
        if person.is_inflicted_with(self.name):
            return
        if self.inflictedStat is None:
            self.inflictedStat = person.highest_stat()
        person.decrease_stat(self.inflictedStat, self.penaltyPerRound * self.rounds)

    def reverse_status(self, person):
        person.increase_stat(self.inflictedStat, self.penaltyPerRound * self.rounds)
        return 0

class Weakened(StatusEffect):
    name = 'Weakness'
    penalty = 2
    def __init__(self, duration, penalty=None):
        super(Weakened, self).__init__(Weakened.name, duration, False)
        self.penalty = penalty
        if penalty is None:
            self.penalty = Weakened.penalty
        else:
            self.penalty = penalty

    def inflict_status(self, person):
        if person.is_inflicted_with(self.name):
            return
        print(person.primaryStats)
        person.decrease_stat(universal.STRENGTH, self.penalty)
        person.decrease_stat(universal.DEXTERITY, self.penalty)
        print(person.primaryStats)
        return 0

    def reverse_status(self, person):
        person.increase_stat(universal.STRENGTH, self.penalty)
        person.increase_stat(universal.DEXTERITY, self.penalty)
        return 0

class Shielded(StatusEffect):
    name = 'Shield'
    defenseBonus = 10
    def __init__(self, duration, defenseBonus=None):
        super(Shielded, self).__init__(Shielded.name, duration, False, isNegative=False)
        if defenseBonus is None:
            self.defenseBonus = Shielded.defenseBonus
        else:
            self.defenseBonus = defenseBonus

    def inflict_status(self, person):
        if person.is_inflicted_with(self.name):
            return
        assert(self.defenseBonus is not None)
        return self.defenseBonus

    def reverse_status(self, person):
        """ 
        Since Shielded doesn't actually do anything to the person, it doesn't need to do anything.
        """
        return 0

class MagicShielded(StatusEffect):
    name = 'Magic Shield'
    defenseBonus = 10
    def __init__(self, duration, defenseBonus=None):
        super(MagicShielded, self).__init__(MagicShielded.name, duration, False, isNegative=False)
        if defenseBonus is None:
            self.defenseBonus = MagicShielded.defenseBonus
        else:
            self.defenseBonus = defenseBonus

    def inflict_status(self, person):
        if person.is_inflicted_with(self.name):
            return
        assert(self.defenseBonus is not None)
        return self.defenseBonus

    def reverse_status(self, person):
        """ 
        Since MagicShielded doesn't actually do anything to the person, it doesn't need to do anything.
        """
        return 0

class MagicDistorted(StatusEffect):
    name = 'Magic Distorted'
    penalty = 2
    def __init__(self, duration, penalty=None):
        super(MagicDistorted, self).__init__(MagicDistorted.name, duration, False)
        if penalty is None:
            self.penalty = MagicDistorted.penalty
        else:
            self.penalty = penalty

    def inflict_status(self, person):
        if person.is_inflicted_with(self.name):
            return
        print(person.primaryStats)
        person.decrease_stat(universal.TALENT, self.penalty)
        person.decrease_stat(universal.WILLPOWER, self.penalty)
        print(person.primaryStats)
        return 0

    def reverse_status(self, person):
        person.increase_stat(universal.TALENT, self.penalty)
        person.increase_stat(universal.WILLPOWER, self.penalty)
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
        if person.is_inflicted_with(self.name):
            return
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
    def __init__(self, duration, defensePenalty=10):
        super(LoweredDefense, self).__init__(LoweredDefense.name, duration, False)
        self.defensePenalty = 10

    def inflict_status(self, person):
        return self.defensePenalty

    def reverse_status(self, person):
        return 0

class LoweredMagicDefense(StatusEffect):
    name = 'Lowered Magic Defense'
    def __init__(self, duration, defensePenalty=10):
        super(LoweredMagicDefense, self).__init__(LoweredDefense.name, duration, False)
        self.defensePenalty = 10

    def inflict_status(self, person):
        return self.defensePenalty

    def reverse_status(self, person):
        return 0

class DefendStatus(StatusEffect):
    combatOnly = True
    name = 'Defending'
    BONUS = 2

    def __init__(self, duration):
        super(DefendStatus, self).__init__(DefendStatus.name, duration, isNegative=False)

    def inflict_status(self, person):
        """
        When a character is defending, they get a +BONUS bonus to strength, dexterity, willpower, and talent, to help them defend against enemy attacks.
        Note: This does not apply when a character is defending another character. This only works when a character is defending themselves.
        """
        if person.is_inflicted_with(self.name):
            return
        person.set_stat(universal.STRENGTH, person.strength() + self.BONUS)
        person.set_stat(universal.DEXTERITY, person.dexterity() + self.BONUS)
        person.set_stat(universal.WILLPOWER, person.willpower() + self.BONUS)
        person.set_stat(universal.TALENT, person.talent() + self.BONUS)

    def reverse_status(self, p):
        p.set_stat(universal.STRENGTH, p.strength() - self.BONUS)
        p.set_stat(universal.DEXTERITY, p.dexterity() - self.BONUS)
        p.set_stat(universal.WILLPOWER, p.willpower() - self.BONUS)
        p.set_stat(universal.TALENT, p.talent() - self.BONUS)


class StrikePoor(StatusEffect):
    name = 'Strike Poor'
    def __init__(self, duration, damagePenalty=10):
        super(StrikePoor, self).__init__(StrikePoor.name, duration, False, isNegative=False)
        self.damagePenalty = damagePenalty

    def inflict_status(self, person):
        assert self.damagePenalty is not None
        return self.damagePenalty

    def reverse_status(self, person):
        """ 
        Since StrikePoor doesn't actually do anything to the person, it doesn't need to do anything.
        """
        return 0

class StrikeTrue(StatusEffect): 
    name = 'Strike True'
    def __init__(self, duration, damageBonus=10):
        super(StrikeTrue, self).__init__(StrikeTrue.name, duration, False, isNegative=False)
        self.damageBonus = damageBonus

    def inflict_status(self, person):
        assert self.damageBonus is not None
        return self.damageBonus

    def reverse_status(self, person):
        """ 
        Since StrikeTrue doesn't actually do anything to the person, it doesn't need to do anything.
        """
        return 0


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
    elif statusName == StrikeTrue.name:
        return 'ST'
    elif statusName == StrikePoor.name:
        return 'SP'
    else:
        raise ValueError(' '.join([statusName, "does not have a shorthand associated with it."]))

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

def build_status(status, duration=0, allies=None, enemies=None):
    """
        A factory function. Given an enum representing a status, returns the associated status. Raises a ValueError if the passed integer does not correspond to a particular
        status. Note: The numSmacks argument should only be used for the Humiliated status, since the severity of that status depends on how many blows the spanker managed
        to land on the spankee.

        status can also be the status' name.
    """
    if status == HUMILIATED or status == Humiliated.name:
        return Humiliated(duration)
    elif status == WEAKENED or status == Weakened.name:
        return Weakened(duration)
    elif status == MAGIC_DISTORTED or status == MagicDistorted.name:
        return MagicDistorted(duration)
    elif status == SHIELDED or status == Shielded.name:
        return Shielded(duration)
    elif status == MAGIC_SHIELDED or status == MagicShielded.name:
        return MagicShielded(duration)
    elif status == LOWERED_DEFENSE or status == LoweredDefense.name:
        return LoweredDefense(duration)
    elif status == LOWERED_MAGIC_DEFENSE or status == LoweredMagicDefense.name:
        return LoweredMagicDefense(duration)
    elif status == CHARMED or status == Charmed.name:
        return Charmed(duration, allies, enemies)
    elif status == FIRST_ORDER or status == FirstOrder.name:
        return FirstOrder()
    elif status == SECOND_ORDER or status == SecondOrder.name:
        return SecondOrder()
    elif status == THIRD_ORDER or status == ThirdOrder.name:
        return ThirdOrder()
    elif status == FOURTH_ORDER or status == FourthOrder.name:
        return FourthOrder()
    elif status == STRIKE_TRUE or status == StrikeTrue.name:
        return StrikeTrue(duration)
    elif status == STRIKE_POOR or status == StrikeTrue.name:
        return StrikePoor(duration)
    else:
        if status == None:
            raise ValueError(' '.join(['None is not a status effect.'])) 
        else:
            raise ValueError(' '.join([str(status), 'is not a status effect.'])) 
