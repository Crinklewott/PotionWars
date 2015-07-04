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
import abc
import items
import spanking
import statusEffects
import math
import person
import positions
import random
from random import randrange
import types
import universal
from universal import *

GRAPPLER_ONLY = 0
ONLY_WHEN_GRAPPLED = 1
UNAFFECTED = 2
ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY = 3
NOT_WHEN_GRAPPLED = 4

WARRIORS_GRAPPLERS = 0
SPELL_SLINGERS = 1
ALL = 2

ALLY = 0
ENEMY = 1
MIN_SMACKS = 5
SMACKS_MULTIPLIER = 1
DURATION_MULTIPLIER = 2
MIN_DURATION = 3

RESULT = 0
EFFECTS = 1
ACTION = 2

#Chance range is used for providing a range for random number generation when performing the attack, defend, grappling, etc. calculations. 
#Increasing this would lessen the impact of the modifiers, decreasing it would increase the impact.
CHANCE_RANGE = 5
def rand(bonus=0):
    #If we do this, then the bonus will have a HUGE impact, because it essentially moves your random number range up. So if your bonus is greater than the other 
    #character's maximum role, then you're guaranteed to succeed. In other words, a specialist will dominate in his specialty, but will get dominated everywhere else,
    #whereas a jack-of-all-trades will hold his own everywhere. Which is pretty much what we want. It also means that even a bonus of +1 will have a significant impact.
    return (random.random() * CHANCE_RANGE) + bonus

ACTION_INDEX = 2
def executed_action(actionEffect):
    return actionEffect[ACTION_INDEX]

STRING_INDEX = 0
def result_string(actionEffect):
    return actionEffect[STRING_INDEX]

EFFECT_INDEX = 1
def effects(actionEffect):
    return actionEffect[EFFECT_INDEX]

class CombatAction(universal.RPGObject):
    #effectStatements is a list of list of strings. Each list of strings in effectString is a single effect statement (split into a list to allow use of his_her, the
    #character name, etc.
    targetType = None
    grappleStatus = None
    effectClass = None
    numTargets = None
    actionType = 'Combat'
    def __init__(self, attacker, defenders, primaryStat, secondaryStat):
        if type(defenders) != list:
            defenders = [defenders]
        self.attacker = attacker
        self.defenders = defenders
        self.effectClass = None
        self.effectStatements = []
        self.grappleStatus = None
        self.targetType = None
        self.primaryStat = primaryStat
        self.secondaryStat = secondaryStat

    def confirmation_message(self):
        raise NotImplementedError()

    def display_defenders(self):
        return ', '.join([defender.printedName for defender in self.defenders])

    def __repr__(self):
        result = []
        if self.attacker:
            result.append("%%%%%%%%%%%")
        result.extend(["\n---------------", self.__class__.__name__, "-------------"])
        for variable, value in vars(self).iteritems():
            if type(value) != 'instancemethod':
                result.append(variable + ": " + repr(value))
        if self.attacker:
            result.append("%%%%%%%%%%")
        return '\n'.join(result)

    def __eq__(self, other):
        """
        A simple equality test that returns true iff the two actions have the same name.
        """
        return self is other

    @abc.abstractmethod
    def effect_statement(self, defender):
        """
        A short hand for randomly picking one of the effect statements of this action. Note that this function returns a random string from this object's effectStatements
        list. However, the effectStatements still need to be defined. Furthermore, because the effect statements only apply to one defender at a time, they can't be 
        defined right away. So they need to be defined in the concrete version of this method, and then you can invoke this abstract version to get a random choice.
        It's not the most elegant implementation ever, and I may come back someday and rework it.
        """
        return random.choice(self.effectStatements)

    @abc.abstractmethod
    def effect(self, allies=None, enemies=None, inCombat=True):
        """
            effect describes the impact of this action when performed by the attacker on the defender(s). It modifies the attacker and defender(s) directly as necessary,
            and returns a string describing what happened.
            The function should return a triple:
            1. The string describing the result of the action.
            2. A list of effects, one for each defender (if there is only one defender, then this should be a singleton list. If the action does not affect a defender in
            a tangible manner, such
            as in the case of a character defending another character, it should return [])
            3. The action performed. Note that this may be this action, or it may be a different action if the original action no longer makes sense. For example, if your
            character attempts to grapple an enemy, but that enemy successfully grapples your character first, then your character will default to attacking).
        """
        return

    def being_spanked(self):
        if self.attacker.involved_in_spanking():
            return ('', [None], CombatAction(self.attacker, self.defenders, self.primaryStat, self.secondaryStat))
        else:
            return None

    def _save(self):
        raise NotImplementedError()

    def grappling_string(self):
        target = 'Grappler only' if self.targetType == ENEMY else 'Caster only'
        if self.grappleStatus == GRAPPLER_ONLY:
            return '\n'.join(['Yes', 'TARGETS WHEN GRAPPLING: ' + target])
        elif self.grappleStatus == ONLY_WHEN_GRAPPLED:
            return '\n'.join(['Only when grappled', 'TARGETS WHEN GRAPPLING: Anyone'])
        elif self.grappleStatus == UNAFFECTED:
            return '\n'.join(['Yes', 'TARGETS WHEN GRAPPLING: Anyone'])
        elif self.grappleStatus == ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY:
            return '\n'.join(['Only when grappled', 'TARGETS WHEN GRAPPLING: ' + target])
        elif self.grappleStatus == NOT_WHEN_GRAPPLED:
            return '\n'.join(['No.'])
        else:
            raise ValueError(' '.join(['' if self.grappleStatus is None else str(self.grappleStatus), 'is not a valid grapple status. CombatAction:', str(self.grappleStatus)]))

    def target_type_string(self):
        if self.targetType == ALLY:
            return 'Ally'
        elif self.targetType == ENEMY:
            return 'Enemy'

"""
This number determines how fast the bonuses for having a high stat drop off.
Consider an attacker A and a defender D. And suppose A is attacking D.
Then, A gains a 1 point bonus to his attack and damage for the first POINT_DROP_OFF points A has in warfare above D. 
The next POINT_DROP_OFF points give A a .75 bonus per point (rounded down).
The next POINT_DROP_OFF points give A a .5 bonus per point (rounded down).
The next POINT_DROP_OFF points give A a .25 bonus per point (rounded down).
After that, A stops receiving bonuses to his attack and damage.
"""
POINT_DROP_OFF = 5
"""
This affects how quickly the bonuses for points outlined above decrease. For every five points, the multiplier bonus per point decreases by MULTIPLIER_DECREASE. Increasing this value will
reduce the bonuses for having higher stats, while decreasing it will increase the bonuses. This combined with POINT_DROP_OFF can be used to tweak the bonuses.
"""
MULTIPLIER_DECREASE = .25

def compute_bonus(difference):
    """
    Computes the bonus the initiator of an action receives for having higher stats than her opponents.
    """
    remainder = difference % POINT_DROP_OFF
    bonusLevels = difference // POINT_DROP_OFF             
    multiplier = 1.0
    bonus = 0
    while bonusLevels > 0:
        bonus += int(math.floor(POINT_DROP_OFF * multiplier))
        multiplier -= MULTIPLIER_DECREASE
        bonusLevels -= 1
    if remainder:
        bonus += int(math.floor(remainder * multiplier))
    return bonus


class AttackAction(CombatAction):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = SPELL_SLINGERS
    numTargets = 1
    primaryStat = universal.DEXTERITY
    secondaryStat = universal.STRENGTH
    actionType = 'attack'

    def __init__(self, attacker, defenders):
        super(AttackAction, self).__init__(attacker, defenders, universal.WARFARE, AttackAction.secondaryStat)
        self.targetType = ENEMY
    #Spell slingers tend to have lower defense, so attacks are more effective.
        self.effectClass = SPELL_SLINGERS
        self.grappleStatus = GRAPPLER_ONLY
        self.actionType = 'attack'
        self.primaryStat = AttackAction.primaryStat
        self.secondaryStat = AttackAction.secondaryStat

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will attack', self.display_defenders() + '.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: A string indicating what happened, the damage inflicted by the action, and this action.
        """
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        defender = self.defenders[0]
        attacker = self.attacker
        opponents = enemies if attacker in allies else allies
        if defender.is_grappling() and not attacker.is_grappling(defender):
            opponents.remove(defender)
            if opponents:
                return AttackAction(attacker, [opponents[random.randrange(len(opponents))]]).effect(inCombat, allies, enemies)
            else:
                return DefendAction(attacker, [attacker]).effect(inCombat, allies, enemies)
        opponents = enemies if self.attacker in allies else allies
        if not defender in opponents:
            return AttackAction(attacker, opponents[randrange(0, len(opponents))]).effect(inCombat, allies, enemies)
        defender.guardians = [guardian for guardian in defender.guardians if guardian.current_health() > 0]
        if defender.guardians:
            #If the defender is being guarded, then we use the first guardian instead of the current defender. 
            guardian = defender.guardians.pop()
            self.defenders = [guardian]
            attackEffect = self.effect(inCombat, allies, enemies)
            return ('\n'.join([' '.join([guardian.printedName, 'defends', defender.printedName, 
                'from', attacker.printedName + '!']), attackEffect[0]]), attackEffect[1], 
                attackEffect[2]) 
        else:
            dam = self.calculate_damage(attacker, defender)
            self.inflict_damage(defender, dam)
            resultString = self.display_result(attacker, defender, dam)
            return (resultString, [dam], self)

    def calculate_damage(self, attacker, defender):
        return compute_damage(attacker.warfare(), attacker.warfare() + attacker.attack() - 
                (defender.warfare() + defender.defense())) 

    def display_result(self, attacker, defender, damage):
        resultString = ' '.join([attacker.printedName, 'hits', defender.printedName, 
            'for', str(damage), 'damage!'])
        if defender.current_health() <= 0:
            resultString = '\n'.join([resultString, ' '.join([defender.printedName, 'collapses!'])])
        return resultString

    def inflict_damage(self, defender, dam):
        defender.receives_damage(dam)



MINIMUM_NEGATIVE_DAMAGE = -5
DIVISION_CONSTANT = 10
MAX_BONUS = 5
def compute_damage(attWarfare, warfareDiff):
    """
    Given the attacker's warfare, and the difference between the attacker's attack and defender's defense, computes the damage administered by the attacker.
    """
    assert MINIMUM_NEGATIVE_DAMAGE < 0 < MAX_BONUS, "MINIMUM NEGATIVE DAMAGE: %d not negative or MAX_BONUS: %d not positive." % (MINIMUM_NEGATIVE_DAMAGE, MAX_BONUS)
    assert DIVISION_CONSTANT != 0, "DIVISION_CONSTANT cannot be zero."
    #return max(1, attWarfare + warfareDiff)
    if MINIMUM_NEGATIVE_DAMAGE <= warfareDiff <= MAX_BONUS:
        return attWarfare + int(math.trunc(warfareDiff / DIVISION_CONSTANT * attWarfare))
    elif warfareDiff < MINIMUM_NEGATIVE_DAMAGE:
        return max(1, compute_damage(attWarfare, warfareDiff + 1) - 1)
    else:
        return 1 + compute_damage(attWarfare, warfareDiff - 1)


class GrappleAction(CombatAction):
    targetType = ENEMY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = SPELL_SLINGERS
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.DEXTERITY
    actionType = 'GrappleAction'
    GRAPPLE_DURATION_DIVISOR = 1
    def __init__(self, attacker, defenders, enemyInitiated=False):
        super(GrappleAction, self).__init__(attacker, defenders, GRAPPLE, GrappleAction.secondaryStat)
        self.targetType = ENEMY
        #Spell slingers can have their effectiveness grossly decreased by being grappled.
        self.effectClass = SPELL_SLINGERS
        self.primaryStat = GrappleAction.primaryStat
        self.secondaryStat = GrappleAction.secondaryStat
        self.grappleStatus = NOT_WHEN_GRAPPLED
        self.enemyInitiated = enemyInitiated
        self.actionType = 'GrappleAction'

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will grapple', self.display_defenders() + '.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Attacker tries to grapple defender. If attacker is already grappling defender, attacks defender. If attacker is already grappling someone else, attempts to break
        that other grapple.
        Returns a triple of a string, a list containing an int and the action: The string contains a printout of the result of the grapple, the number of rounds the characters will be grappling, 
        the action is the action performed: this action if the grappling was attempted. Otherwise, if something else had to happen (an attack, a 
        different grapple, etc) then it's that action.
        """
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        defender = self.defenders[0]
        opponents = enemies if self.attacker in allies else allies
        attacker = self.attacker
        if not defender in opponents:
            return AttackAction(attacker, opponents[randrange(0, len(opponents))]).effect(inCombat, allies, enemies)
        resultString = ''
        defender.guardians = [guardian for guardian in defender.guardians if guardian.current_health() > 0]
        if attacker.is_grappling() and not attacker.is_grappling(defender):
            return BreakGrappleAction(attacker, attacker.grapplingPartner).effect(inCombat, allies, enemies)
        elif defender.guardians and not defender.is_grappling(attacker):
            guardian = defender.guardians.pop()
            resultString = ' '.join([guardian.printedName, 'defends', defender.printedName, 'from', attacker.printedName + '!'])
            self.defenders = [guardian]
            grappleEffect = self.effect(inCombat, allies, enemies)
            return ('\n'.join([resultString, grappleEffect[0]]), grappleEffect[1], grappleEffect[2])
        elif attacker.is_grappling(defender):
            return AttackAction(attacker, defender).effect(True, allies, enemies)
        if not defender.guardians:               
            if defender.is_grappling() and not defender.is_grappling(attacker):
                return AttackAction(attacker, defender).effect(inCombat, allies, enemies)
            else:
                duration = compute_damage(attacker.grapple(), attacker.grapple() - defender.grapple()) // self.GRAPPLE_DURATION_DIVISOR
                if duration <= 1:
                    duration = 0
                    return (' '.join([attacker.printedName, 'cannot grapple' ,defender.printedName + '!']), [duration], self)
                else:
                    defender.break_grapple()
                    attacker.grapple(defender, duration)
                    return (' '.join([attacker.printedName, 'grapples', defender.printedName + '!']), [duration], self)


GRAPPLE_DIVISOR = 2

class BreakGrappleAction(CombatAction):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.DEXTERITY
    actionType = 'breakGrappleAction'
    def __init__(self, attacker, defenders):
        super(BreakGrappleAction, self).__init__(attacker, defenders, GRAPPLE, BreakGrappleAction.secondaryStat)
        self.targetType = ENEMY
        self.primaryStat = BreakGrappleAction.primaryStat
        self.grappleStatus = ONLY_WHEN_GRAPPLED
        self.effectClass = ALL
        self.actionType = 'breakGrappleAction'

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will attempt to stop grappling', self.display_defenders() + 
            '.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The string indicating the result, true if the break succeeded false otherwise, and itself if the break grapple occured. Otherwise, if the 
        grapple had already been broken, this function returns the result of the attacker defending.
        """
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker = self.attacker
        defender = attacker.grapplingPartner
        if defender is None:
            return DefendAction(attacker, attacker).effect(inCombat, allies, enemies)
        if attacker.is_grappling():
            attacker.reduce_grapple_duration(attacker.grapple() // GRAPPLE_DIVISOR)
            defender.reduce_grapple_duration(attacker.grapple() // GRAPPLE_DIVISOR)
            assert attacker.grapple_duration() == defender.grapple_duration(), "%s grapple duration: %d, %s grapple duration: %d" % (attacker.name, attacker.grappleDuration, defender.name, 
                    defender.grappleDuration)
            if attacker.grapple_duration():
                return(' '.join([attacker.printedName, 'loosens', defender.printedName + "'s", "hold on", person.himher(attacker) + '!']), [False], self)
            else:
                attacker.break_grapple()
                return (' '.join([attacker.printedName, 'breaks the grapple with', defender.printedName + '!']), [True], self)
        else:
            return DefendAction(attacker, attacker).effect(inCombat, allies, enemies)

class RunAction(CombatAction):
    targetType = ALLY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = ALL
    numTargets = 0
    primaryStat = universal.ALERTNESS
    actionType = 'run'
    def __init__(self, attacker, defenders, secondaryStat=None):
        super(RunAction, self).__init__(attacker, defenders, universal.SPEED, secondaryStat)
        self.targetType = ALLY
        self.grappleStatus = NOT_WHEN_GRAPPLED
        self.primaryStat = RunAction.primaryStat
        self.effectClass = ALL
        self.actionType = 'run'

    def effect(self, inCombat=True, allies=None, enemies=None):
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        avgEnemyStealth = 0
        minEnemyStealth = 9000
        attacker = self.attacker
        for enemy in enemies:
            avgEnemyStealth += enemy.speed()
            if enemy.speed() < minEnemyStealth:
                minEnemyStealth = enemy.speed()
        avgEnemyStealth /= len(enemies)
        success = rand(compute_bonus(max(0, attacker.speed() - avgEnemyStealth)))
        failure = rand()
        if failure <= success:
            return (' '.join(['The party has successfully fled.']), [True], self)
        else:
            return(' '.join(['The party has failed to flee.']), [False], self)
            
    def confirmation_message(self):
        return ' '.join([self.attacker, 'will try to flee.'])

class SpankAction(CombatAction):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.WILLPOWER
    actionType = 'spank'
    REVERSAL_CHANCE = 20
    MIN_SPANKING_DURATION = 2
    MIN_HUMILIATED_DURATION = 2
    DIVISOR = 10
    def __init__(self, attacker, defenders, position, severity=0):
        super(SpankAction, self).__init__(attacker, defenders, GRAPPLE, SpankAction.secondaryStat)
        self.targetType = ENEMY
        self.grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
        self.effectClass = ALL
        self.statusInflicted = statusEffects.HUMILIATED 
        self.actionType = 'spank'
        self.position = position
        self.severity = severity
        self.minDuration = 2

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will start spanking', self.display_defenders(), '.'])

    def administer_spanking(self, inCombat, allies, enemies):
        spanker, spankee = self.attacker, self.defenders[0]
        spankerGrapple, spankeeGrapple = spanker.grapple(), spankee.grapple()
        spankerResilience, spankeeResilience = spanker.resilience(), spankee.resilience()
        resultStringFunction = spanking.spanking_string
        durationMultiplier = 1
        if random.randrange(100) < self.REVERSAL_CHANCE and universal.state.enemiesCanSpank:
            spankee, spanker = spanker, spankee
            durationMultiplier = -1
            #Reversals suck. They use whichever combination of grapples and willpowers that most benefits the new spanker, and hurts the new spankee! 
            spankerGrapple, spankeeGrapple = max(spanker.grapple(), spankee.grapple()), min(spanker.grapple(), spankee.grapple())
            spankerResilience, spankeeResilience = max(spanker.resilience(), spankee.resilience()), min(spanker.resilience(), spankee.resilience())
            resultStringFunction = spanking.reversed_spanking
        resultString = resultStringFunction(spanker, spankee, self.position)
        grappleBonus = int(math.trunc((self.position.maintainability / self.DIVISOR) * spankerGrapple))
        durationBonus = int(math.trunc((self.position.humiliating / self.DIVISOR) * spankerGrapple))
        spankingDuration =  durationMultiplier * max(self.MIN_SPANKING_DURATION, spankerGrapple - spankeeGrapple) + grappleBonus
        if durationMultiplier > 0 and spankingDuration < self.minDuration:
            spankingDuration = self.minDuration
        elif durationMultiplier < 0 and spankingDuration > -self.minDuration:
            spankingDuration =  -self.minDuration
        assert durationMultiplier > 0 or spankingDuration < 0, "Duration Multiplier: %d spankingDuration: %d" % (durationMultiplier, spankingDuration)
        spanker.begin_spanking(spankee, self.position, spankingDuration if spankingDuration > 0 else -spankingDuration)
        spankee.begin_spanked_by(spanker, self.position, spanker.grappleDuration)
        duration = max(self.MIN_HUMILIATED_DURATION, spankerResilience - spankeeResilience) + durationBonus
        if spankee.is_inflicted_with(statusEffects.Humiliated.name):
            spanker.spankeeAlreadyHumiliated = True
        else:
            spankee.inflict_status(statusEffects.build_status(statusEffects.Humiliated.name,
                duration))
            spanker.spankeeAlreadyHumiliated = False
        assert spankingDuration
        return (resultString, [spankingDuration], self, spanker, spankee)

    def attack_action(self, inCombat, allies, enemies):
        return AttackAction(self.attacker, self.defenders)

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
            Returns a triple: The result of the spanking, the duration if the 
            spanking was successful, the negative duration if the spanking was reversed, and the actual action performed.
        """
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker = self.attacker
        defender = self.defenders[0]
        position = self.position
        opponents = enemies if self.attacker in allies else allies
        if not defender in opponents:
            return DefendAction(attacker, opponents[randrange(0, len(opponents))]).effect(inCombat, allies, enemies)
        if attacker.is_grappling(defender):
            return self.administer_spanking(inCombat, allies, enemies)
        elif attacker.graple() > defender.grapple():
            return GrappleAction(attacker, defender).effect(inCombat, allies, enemies)
        else:
            return self.attack_action(inCombat, allies, enemies).effect(inCombat, allies, enemies)


class ContinueSpankingAction(CombatAction):
    targetType = ALLY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.WILLPOWER
    actionType = 'continue spanking'
    def __init__(self, attacker, defenders, position, severity=0):
        super(ContinueSpankingAction, self).__init__(attacker, defenders, GRAPPLE, SpankAction.secondaryStat)
        self.severity = severity

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will continue to spank', self.display_defenders() + '.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The result string, a list containing a single bool indicating whether or not successfully decremented the stat point, and this action
        """
        spankingEffect = self.being_spanked()
        attacker = self.attacker
        defender = self.defenders[0]
        #Counteracts the decrement in duration of the humiliated status at the end of the round. We want the effective duration of humiliated to only go down after the 
        #spanking.
        #defender.increment_status_duration(statusEffects.Humiliated.name)
        humiliatedStatus = defender.get_status(statusEffects.Humiliated.name)
        if not attacker.is_spanking():
            return DefendAction(attacker, [attacker]).effect(inCombat, allies, enemies) 
        if attacker.spankeeAlreadyHumiliated:
            decrementedStat = False
            defender.enduring = False
        elif defender.enduring:
            severity = self.severity - 1
            if severity:
                humiliatedStatus.increase_status(defender, severity)
                decrementedStat = True
            else:
                defender.enduring = False
                decrementedStat = False
        else:
            humiliatedStatus.increase_status(defender)
            decrementedStat = True
        #If our "position" is not in the map of all spanking positions, then our position is actually a spell.
        if attacker.position.name in positions.allPositions:
            resultString = spanking.continue_spanking(self.attacker, defender, self.attacker.position)
        else:
            resultString = attacker.position.round_statement(defender)
        assert defender.is_inflicted_with(statusEffects.Humiliated.name), "Somehow, defender: %s is not afflicted with humiliated!" % defender.name
        return (resultString, [decrementedStat], self)


class StruggleAction(CombatAction):
    targetType = ALLY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.WILLPOWER
    actionType = 'struggle'
    def __init__(self, attacker, defenders):
        super(StruggleAction, self).__init__(attacker, defenders, GRAPPLE, SpankAction.secondaryStat)

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will struggle against the spanking.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The result string, a list containing nothing, and this action
        """
        spankingEffect = self.being_spanked()
        defender = self.defenders[0]
        attacker = self.attacker
        if not attacker.is_being_spanked():
            return DefendAction(attacker, [attacker]).effect(inCombat, allies, enemies)
        attacker.reduce_grapple_duration(attacker.grapple() // 2)
        defender.reduce_grapple_duration(attacker.grapple() // 2)
        assert attacker.grapple_duration() == attacker.spanker.grapple_duration(), "Attacker: %s Duration: %d ; Defender: %s ; Grappler: %s ; Duration : %d" % (attacker.name, 
                attacker.grapple_duration(), attacker.grapplingPartner.name, defender.name, defender.grapple_duration())
        return (' '.join([attacker.printedName, "struggles against", defender.printedName + "'s", "iron grip!"]), [None], self)

class EndureAction(CombatAction):
    targetType = ALLY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.WILLPOWER
    actionType = 'struggle'
    def __init__(self, attacker, defenders):
        super(EndureAction, self).__init__(attacker, defenders, GRAPPLE, SpankAction.secondaryStat)

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will endure the spanking.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The result string, a list containing nothing, and this action
        """
        attacker = self.attacker
        if not attacker.is_being_spanked():
            return DefendAction(attacker, [attacker]).effect(inCombat, allies, enemies)
        attacker.enduring = True
        return (' '.join([attacker.printedName, "endures", self.defenders[0].printedName + "'s", "stinging blows!"]), [None], self)


class ThrowAction(CombatAction):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED
    effectClass = ALL
    numTargets = 2
    primaryStat = universal.DEXTERITY
    secondaryStat = universal.STRENGTH
    actionType = 'throw'
    def __init__(self, attacker, defenders):
        super(ThrowAction, self).__init__(attacker, defenders, GRAPPLE, ThrowAction.secondaryStat)
        self.targetType = ENEMY
        self.primaryStat = ThrowAction.primaryStat
        self.secondaryStat = ThrowAction.secondaryStat
        self.grappleStatus = ONLY_WHEN_GRAPPLED
        self.effectClass = ALL
        self.actionType = 'throw'

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will throw', self.defenders[0].printedName, 
            'at', self.defenders[1].printedName + '.'])
            

    def effect(self, inCombat=True, allies=None, enemies=None):
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker = self.attacker
        grappler = self.defenders[0]
        defender = self.defenders[1]
        opponents = enemies if attacker in allies else allies
        if defender.is_grappling() and not attacker.is_grappling(defender):
            opponentsCopy = list(opponents)
            opponentsCopy.remove(defender)
            #This should always hold true, because if worst comes to worst, the defender can just be the grappler.
            assert len(opponentsCopy) >= 1
            newTarget = opponentsCopy[random.randrange(len(opponentsCopy))]
            while newTarget.is_grappling() and not attacker.is_grappling(newTarget):
                newTarget = opponentsCopy.pop(random.randrange(len(opponentsCopy)))
            defender = newTarget
        damage = attacker.warfare() if attacker.warfare() > attacker.grapple() else attacker.grapple()
        opponents = enemies if self.attacker in allies else allies
        if not grappler in opponents:
            return AttackAction(attacker, defender).effect(inCombat, allies, enemies)
        elif attacker.is_grappling(grappler):
            if attacker.grapple_duration() <= attacker.grapple() // 2:
                grappler.receives_damage(damage)   
                attacker.break_grapple()
                if grappler is defender:
                    resultString = ' '.join([attacker.printedName, 'throws', defender.printedName, 'for', str(damage), 'damage!'])
                    if grappler.current_health() <= 0:
                        resultString = '\n'.join([resultString, ' '.join([defender.printedName, 'collapses!'])])
                else:
                    if not defender in opponents:
                        defender = opponents[randrange(0, len(opponents))]
                    defender.receives_damage(damage)
                    resultString = '\n'.join([' '.join([attacker.printedName, 'throws', grappler.printedName, 'for', str(damage), 'damage!']), 
                        ' '.join([attacker.printedName, 'strikes', defender.printedName, 'for', str(damage), 'damage!'])])
                    if grappler.current_health() <= 0:
                        resultString = '\n'.join([resultString, ' '.join([grappler.printedName, 'collapses!'])])
                    if defender.current_health() <= 0:
                        resultString = '\n'.join([resultString, ' '.join([defender.printedName, 'collapses!'])])
            else:
                damage = 0
                resultString = ' '.join([attacker.printedName, 'cannot yet throw', defender.printedName + "!"])
            return (resultString, [damage, damage], self)    
        else:
            return AttackAction(attacker, defender).effect(inCombat, allies, enemies)

class BreakAllysGrappleAction(CombatAction):
    targetType = ALLY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = SPELL_SLINGERS
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.DEXTERITY
    actionType = 'breakAllysGrappleAction'
    def __init__(self, attacker, defenders):
        super(BreakAllysGrappleAction, self).__init__(attacker, defenders, GRAPPLE, BreakGrappleAction.secondaryStat)
        self.targetType = ALLY
        self.primaryStat = BreakAllysGrappleAction.primaryStat
        self.grappleStatus = NOT_WHEN_GRAPPLED
        #Need to make sure to break the grapple if it's one of your spell slingers that's been grappled.
        self.effectClass = SPELL_SLINGERS
        self.actionType = 'breakAllysGrappleAction'

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will break', self.defenders[0].printedName + "'s", 
            'grapple.'])
    

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        If we try to break our ally's grapple, only to see that the grapple is already broken, then we defend them.
        """
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        defenders = self.defenders
        attacker = self.attacker
        if (attacker in allies and not defenders[0] in allies) or (attacker in enemies and not defenders[0] in enemies):
            return DefendAction(self.attacker, self.attacker).effect(inCombat, allies, enemies)
        ally, allysGrappler = defenders[0], defenders[0].grapplingPartner
        if allysGrappler is None:
            return DefendAction(attacker, defenders[0]).effect(inCombat, allies, enemies)
        else:
            ally.reduce_grapple_duration(attacker.grapple() // GRAPPLE_DIVISOR)
            allysGrappler.reduce_grapple_duration(attacker.grapple() // GRAPPLE_DIVISOR)
            if ally.grapple_duration():
                resultStmt = ' '.join([attacker.printedName, "loosens", allysGrappler.printedName + "'s", 'hold on', ally.printedName + '!'])
            else:
                resultStmt = ' '.join([attacker.printedName, 'breaks', allysGrappler.printedName + "'s", '''hold on''', ally.printedName + '!'])
                allysGrappler.break_grapple()
            return (resultStmt, [None], self) 


class DefendAction(CombatAction):
    targetType = ALLY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = SPELL_SLINGERS
    numTargets = 1
    primaryStat = universal.ALERTNESS
    secondaryStat = universal.WILLPOWER
    actionType = 'defend'
    def __init__(self, attacker, defenders):
        super(DefendAction, self).__init__(attacker, defenders, DefendAction.primaryStat, 
                DefendAction.secondaryStat)
        self.targetType = ALLY
        self.grappleStatus = GRAPPLER_ONLY
        self.primaryStat = DefendAction.primaryStat
        #Want to make sure to defend your spell slingers
        self.effectClass = SPELL_SLINGERS
        self.actionType = 'defend'

    def confirmation_message(self):
        return ' '.join([self.attacker, 'will defend', self.display_defenders() + '.'])

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The result, [None], this action.
        The reason this returns a triple rather than a double, is so that we don't have to do anything special with the defend action in the combat code.
        """
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker = self.attacker
        defender = self.defenders[0]
        if attacker == defender:
            attacker.inflict_status(statusEffects.DefendStatus(1))
            return (' '.join([attacker.printedName, 'defends', person.himselfherself(attacker) + '!']), [None], self)
        else:
            companions = allies if attacker in allies else enemies
            if defender not in companions:
                return DefendAction(attacker, attacker).effect(inCombat, allies, enemies)
            defender.guardians.append(attacker)
            return (' '.join([attacker.printedName, 'defends', defender.printedName + '!']), [None], self)




#--------------------------------Catfight actions---------------------------

class CatSpankAction(SpankAction):
    noPantsBonus = 5
    noPantiesBonus = 5

    def __init__(self, attacker, defenders, position, severity=0):
        super(CatSpankAction, self).__init__(attacker, defenders, position, severity)

    def attack_action(self, inCombat, allies, enemies):
        return CatAttackAction(self.attacker, self.defenders)

    def administer_spanking(self, inCombat, allies, enemies):
        spanker, spankee = self.attacker, self.defenders[0]
        if spankee.guardians:
            guardian = spankee.guardians.pop()
            (resultString, effects, action) = CatSpankAction(spanker, 
                    [guardian], self.position, self.severity).effect(inCombat, allies, enemies)
            resultString = ' '.join([guardian.printedName, 'defends', spankee.printedName + 
                '!\n']) + resultString
            return (resultString, effects, action)

        spankerBonus = sum([spanker.musculature_bonus(), spanker.body_type_bonus(), 
            spanker.size_bonus()])
        spankerRandomModifier = spanker.strength() + spanker.current_stamina()
        spankeeBonus = sum([spankee.musculature_bonus(), spankee.body_type_bonus(), 
            spankee.size_bonus()])
        spankeeRandomModifier = spankee.strength() + spankee.current_stamina()

        def generate_spankee_threshhold():
            return rand(spankeeRandomModifier) - spankee.hair_penalty() + spankeeBonus

        def generate_spanker_threshhold():
            return rand(spankerRandomModifier) - spanker.hair_penalty() + spankerBonus

        wasSuccessful = generate_spankee_threshhold() <= generate_spanker_threshhold()
        resultString = ''

        if not wasSuccessful and generate_spankee_threshhold() >= generate_spanker_threshhold():
            spanker, spankee = spankee, spanker
            spankerBonus, spankeeBonus = spankeeBonus, spankerBonus
            spankerThreshhold = generate_spanker_threshhold()
            spankeeThreshhold = generate_spankee_threshhold()
            wasSuccessful = rand(spankeeThreshhold) <= rand(spankerThreshhold)
            resultString = spanker.reversed_by(spankee, self.position)
        elif wasSuccessful:
            resultString = spanker.spanks(spankee, self.position)

        if not wasSuccessful:
            return (' '.join(spanker.failed_spanking(spankee, self.position)), [0], self)
        else:
            spankingDuration = compute_damage(spanker.grapple(), 
                    spankee.grapple())
            spankingDuration += sum([spankerBonus, 
                spanker.current_stamina(), 
                -spanker.hair_penalty(),
                -spankeeBonus, 
                spankee.hair_penalty(), 
                -spankee.current_stamina()]) 
            spanker.begin_spanking(spankee, self.position, spankingDuration)

            resilienceDamage = compute_damage(spanker.warfare(), spankee.warfare())
            humiliationDamage = compute_damage(spanker.resilience(), spankee.resilience())
            resilienceDamage += spankerBonus - spankeeBonus
            defender = self.defenders[0]
            if not defender.wearing_lower_clothing():
                humiliationDamage += self.noPantsBonus 
                resilienceDamage += self.noPantsBonus
            if not defender.wearing_underwear() or defender.underwear().baring():
                humiliationDamage += self.noPantiesBonus
                resilienceDamage += self.noPantsBonus

            spankee.receives_stamina_damage(resilienceDamage)
            spankee.receives_humiliation_damage(humiliationDamage)
            if spankee.current_humiliation() >= spankee.humiliation():
                resultString += ''.join(['\n', spankee.printedName, ' surrenders!'])
        return (resultString, [spankingDuration], self)

class CatAttackAction(AttackAction):

    def inflict_damage(self, defender, dam): 
        defender.receives_stamina_damage(dam)

    def display_result(self, attacker, defender, damage):
        possible_strings = [
                ' '.join([attacker.printedName, "bitch slaps", defender.printedName +"!"]),
                ' '.join([attacker.printedName, "rakes", defender.printedName, "with", 
                        attacker.hisher(), "nails!"]),
                ' '.join([attacker.printedName, "grabs", defender.grab_hair_message(), 
                        "and gives a vicious tug!"]),
                ' '.join([attacker.printedName, "punches", defender.printedName, "in the",
                    "boob!" if defender.is_female() else "chest!"]),
                ' '.join([attacker.printedName, "pokes", defender.printedName, "in the eye!"]),
                ' '.join([attacker.printedName, "punches", defender.printedName, "in the belly!"]),
                ' '.join([attacker.printedName, "smacks", defender.printedName, 
                        "hard on the ass!"]),
                ' '.join([attacker.printedName, "digs", attacker.hisher(), "nails into",
                    defender.printedName + "'s", "forearm!"])
        ]
        return random.choice(possible_strings)

class StripAction(CombatAction):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.DEXTERITY
    actionType = 'strip'

    def __init__(self, attacker, defenders, clothingTypeToStrip):
        """
        clothingTypeToStrip is the integer representing a clothing type. The types can be 
        found in person.py. Search for "SHIRT =".
        """
        self.attacker = attacker
        self.defenders = defenders
        self.clothingTypeToStrip = clothingTypeToStrip

    def get_clothing_to_strip(self, target):
        """
        If the target is still wearing the clothingToStrip, we just return the clothingToStrip.
        If however the target is not wearing the clothingToStrip, then we find some clothing
        to strip. If the target is completely naked, we return None.
        """
        if target.wearing(self.clothingToStrip):
            return self.clothingToStrip
        elif target.wearing(person.SHIRT):
            return person.SHIRT
        elif target.wearing(person.LOWER_CLOTHING):
            return person.LOWER_CLOTHING
        elif target.wearing(person.UNDERWEAR):
            return person.UNDERWEAR

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: A string indicating what happened, a list containing a single
        number: 1 if the strip was successful, 0 if not, -1 if reversed, and this action.
        """
        attacker = self.attacker
        defender = self.defenders[0]
        if not attacker.is_grappling(): 
            return attacker.CatAttackAction(attacker, self.defenders).effect(inCombat, allies, 
                    enemies)
        elif not attacker.is_grappling(defender):
            newTarget = attacker.grapplingPartner
            newClothingToStrip = self.get_clothing_to_strip(newTarget)
            if newClothingToStrip is None:
                return attacker.CatAttackAction(attacker, [newTarget]).effect(inCombat, allies,
                        enemies)
            else:
                return StripAction(attacker, [newTarget], newClothingToStrip).effect(
                        inCombat, allies, enemies)
        else:
            def strip_threshhold(character):
                return sum([rand(character.strength() + 
                    character.dexterity() // 2 + character.willpower() // 2), 
                    character.current_stamina(),
                    character.size_bonus(), character.hair_penalty(), 
                    character.musculature_bonus(), character.body_type_bonus()])
            stripper, stripee = attacker, defender
            successNum = 1
            if strip_threshhold(stripper) < strip_threshhold(stripee):
                #If the stripper fails twice, things get reversed.
                if strip_threshhold(stripper) < strip_threshhold(stripee):
                    stripper, stripee = stripee, stripper
                    self.clothingToStrip = self.get_clothing_to_strip(stripee)
                    successNum = -1
                else:
                    resultString = ' '.join([stripper.printedName, "fails to rip off", 
                        stripee.printedName + "'s", stripee.equipment(self.clothingToStrip) + "!"])
                    return (resultString, [0], self)
            resultString = self.stripping_string(stripper, stripee)  
            stripee.unequip(stripee.equipment(self.clothingToStrip), couldBeNaked=True)
            stripee.receives_humiliation_damage(max(1, (stripee.humiliation - 
                stripee.current_humiliation()) // 4))
            return (resultString, [-1], self)

    def stripping_string(self, stripper, stripee):
        clothing = stripee.equipment(self.clothingToStrip)
        if items.is_shirt(clothing):
            return self.shirt_stripping(stripper, stripee)
        elif items.is_underwear(clothing):
            return self.underwear_stripping(stripper, stripee)
        elif items.is_lower_clothing(clothing):
            return self.lower_clothing_stripping(stripper, stripee)
        else:
            raise ValueError(' '.join([clothing.name, "is not clothing, and cannot be stripped"]))

    def confirmation_message(self):
        return ' '.join([self.attacker.printedName, "will strip off", 
            self.defenders[0].printedName + "'s", 
            self.defenders[0].equipment[self.clothingTypeToStrip].name + "."])
                
    def shirt_stripping(self, stripper, stripee):
        stripperName = stripper.printedName
        stripeeName = stripee.printedName
        shirtName = stripee.shirt().name
        possibleStrings = [
                ' '.join([stripperName, "grabs the back of", stripeeName + "'s", shirtName, 
                    "and tugs.", stripeeName, "hunches over,", stripee.hisher(), "arms flailing",
                    "wildly. The two sway, and the", shirtName, "inches its way up", 
                    stripeeName + "'s", "back, briefly gets tangled in", stripee.hisher(),
                    "hair and arms, then snaps off.", stripeeName, "blushes furiously, while",
                    stripperName, "waves the shirt over", stripper.hisher(), "head, and flings",
                    "it into a corner."])
        ]
        return random.choice(possibleStrings)
