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
import spanking
import statusEffects
import abc
import random
import person
import math
from random import randrange

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
            raise ValueError(' '.join(['' if self.grappleStatus is None else str(self.grappleStatus), 'is not a valid grapple status.']))

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

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: A string indicating what happened, the damage inflicted by the action, and this action.
        """
        defender = self.defenders[0]
        attacker = self.attacker
        opponents = enemies if self.attacker in allies else allies
        if not defender in opponents:
            return AttackAction(attacker, opponents[randrange(0, len(opponents))]).effect(inCombat, allies, enemies)
        resultString = ''
        try:
            if defender.guardian.current_health() == 0:
                defender.guardian = None
        except AttributeError:
            pass
        if defender.guardian:
            self.defenders[0] = defender.guardian
            attackEffect = self.effect(inCombat, allies, enemies)
            defender.guardian = None
            return ('\n'.join([' '.join([defender.guardian.printedName, 'defends', defender.printedName, 'from', attacker.printedName + '!']), attackEffect[0]]), 
                    attackEffect[1], attackEffect[2]) 
        if not defender.guardian:
            attacker = self.attacker
            wa = attacker.weapon()
            wd = defender.weapon()
            attackBonus = wa.attack_bonus(attacker.is_grappling())
            defendBonus = wd.parry_bonus(defender.is_grappling())
            warfareDifference = max(0, attacker.warfare() - defender.warfare())
            bonus = compute_bonus(warfareDifference)
            #attackBonus += attacker.warfare()
            #defendBonus += defender.warfare() // 2
            #assert attacker.attack_penalty() >= 0, '%s attack penalty: %s' % (attacker.name, attacker.attack_penalty())
            #attackBonus += attacker.attack_penalty()
            #defendBonus += defender.attack_penalty()
            success = rand(bonus + attackBonus) 
            failure = rand(defendBonus)
            if failure <= success:
                #damageBonus = attacker.warfare() + wa.attack_bonus(attacker.is_grappling()) - defender.defense()
                dam = max(1, wa.damage(attacker.is_grappling()) + bonus - defender.defense())
                defender.receives_damage(dam)
                damageString = ' '.join([attacker.printedName, 'hits', defender.printedName, 'for', str(dam), 'damage!'])
            else:
                dam = 0
                damageString = ' '.join([attacker.printedName, 'misses', defender.printedName + '!'])
            resultString = '\n'.join([resultString, damageString]) if resultString != '' else damageString
            if defender.current_health() <= 0:
                resultString = '\n'.join([resultString, ' '.join([defender.printedName, 'collapses!'])])
            return (resultString, [dam], self)


class GrappleAction(CombatAction):
    targetType = ENEMY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = SPELL_SLINGERS
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.DEXTERITY
    actionType = 'GrappleAction'
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

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Attacker tries to grapple defender. If attacker is already grappling defender, attacks defender. If attacker is already grappling someone else, attempts to break
        that other grapple.
        Returns a triple of a string, boolean and action: The string contains a printout of the result of the grapple, the boolean is true if the grapple was successful, 
        and false otherwise, the action is the action performed: this action if the grappling was attempted. Otherwise, if something else had to happen (an attack, a 
        different grapple, etc) then it's that action.
        """
        defender = self.defenders[0]
        opponents = enemies if self.attacker in allies else allies
        attacker = self.attacker
        if not defender in opponents:
            return AttackAction(attacker, opponents[randrange(0, len(opponents))]).effect(inCombat, allies, enemies)
        resultString = ''
        if attacker.is_grappling() and not attacker.is_grappling(defender):
            return BreakGrappleAction(attacker, attacker.grapplingPartner).effect(inCombat, allies, enemies)
        elif defender.guardian is not None and not defender.is_grappling(attacker):
            resultString = ' '.join([defender.guardian.printedName, 'defended', defender.printedName, 'from', attacker.printedName + '!'])
            self.defenders = [defender.guardian]
            defender.guardian = None
            grappleEffect = self.effect(inCombat, allies, enemies)
            if grappleEffect[1]:
                #If the attacker is grappling the defender's guardian, the guardian can no longer protect the defender.
                defender.guardian = None
            return ('\n'.join([resultString, grappleEffect[0]]), grappleEffect[1], grappleEffect[2])
        elif attacker.is_grappling(defender):
            return AttackAction(attacker, defender).effect(True, allies, enemies)
        if not defender.guardian:               
            if defender.is_grappling() and not defender.is_grappling(attacker):
                return AttackAction(attacker, defender).effect(inCombat, allies, enemies)
            wa = attacker.weapon()
            wd = defender.weapon()
            bonus = compute_bonus(max(0, attacker.grapple() - defender.grapple()))
            #grappleABonus = wa.grappleAttempt + attacker.grapple() - attacker.attack_penalty()
            #grappleDBonus = wd.grappleAttemptDefense + max(defender.grapple(), defender.warfare()) // 2 - defender.attack_penalty()
            success = rand(CHANCE_RANGE + bonus + wa.grappleAttempt)
            failure = rand(CHANCE_RANGE + wd.grappleAttemptDefense)
            if failure <= success:
                defender.break_grapple()
                attacker.grapple(defender)
                return(' '.join([attacker.printedName, 'grapples', defender.printedName + '!']), [True], self)
            else:
                return(' '.join([attacker.printedName, 'fails to grapple', defender.printedName + '!']), [False], self)


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

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The string indicating the result, true if the break succeeded false otherwise, and itself if the break grapple occured. Otherwise, if the 
        grapple had already been broken, this function returns the result of the attacker defending.
        """
        attacker = self.attacker
        defender = attacker.grapplingPartner
        if defender is None:
            return DefendAction(attacker, attacker).effect(inCombat, allies, enemies)
        if attacker.is_grappling():
            wa = attacker.weapon()
            wd = defender.weapon()
            bonus = compute_bonus(max(0, attacker.grapple() - defender.grapple()))
            #grappleABonus = wa.grappleAttemptDefense + max(attacker.warfare(), attacker.grapple()) - attacker.attack_penalty()
            #grappleDBonus = wd.grapple_bonus() // 2 + defender.grapple() - defender.attack_penalty()
            success = rand(bonus + wa.grapple_bonus())
            failure = rand(wd.grapple_bonus())
            if failure <= success:
                attacker.break_grapple()
                return (' '.join([attacker.printedName, 'breaks the grapple with', defender.printedName + '!']), [True], self)
            else:
                return(' '.join([attacker.printedName, 'fails to break the grapple with', defender.printedName + '!']), [False], self)
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
            
class SpankAction(CombatAction):
    #TODO: Rework with the new spanking mechanic described on my blog.
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    primaryStat = universal.STRENGTH
    secondaryStat = universal.DEXTERITY
    actionType = 'spank'
    def __init__(self, attacker, defenders, position, severity=0):
        super(SpankAction, self).__init__(attacker, defenders, GRAPPLE, SpankAction.secondaryStat)
        self.targetType = ENEMY
        self.grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
        self.effectClass = ALL
        self.statusInflicted = statusEffects.HUMILIATED 
        self.actionType = 'spank'
        self.position = position
        self.severity = severity

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
            Returns a triple: The result of the spanking, a positive number if the spanking was successful, a negative number if the spanking was reversed, and 0 if the 
            spanking failed, and the actual action performed.
        """
        attacker = self.attacker
        defender = self.defenders[0]
        position = self.position
        opponents = enemies if self.attacker in allies else allies
        if not defender in opponents:
            return AttackAction(attacker, opponents[randrange(0, len(opponents))]).effect(inCombat, allies, enemies)
        if attacker.is_grappling(defender):
            wa = attacker.weapon()
            wd = defender.weapon()
            #spankABonus = wa.grapple_bonus() + attacker.grapple() - attacker.attack_penalty()
            #spankDBonus = wd.grapple_bonus() + defender.grapple() - defender.attack_penalty()
            success = rand(compute_bonus(max(0, attacker.grapple() - defender.grapple())) + wa.grapple_bonus())
            failure = rand(wd.grapple_bonus() + self.position.difficulty)
            humiliated = False
            successFlag =  0
            if failure <= success:
                if not defender.is_inflicted_with(statusEffects.Humiliated.name):
                    duration = max(MIN_DURATION, DURATION_MULTIPLIER * rand(compute_bonus(max(0, attacker.resilience() - defender.resilience()))) + self.severity)
                    #This is just a placeholder, until we can implement the multi-round spankings.
                    numSmacks = rand(self.position.maintainability)
                    defender.inflict_status(statusEffects.build_status(statusEffects.HUMILIATED, duration, numSmacks))
                resultString = spanking.spanking_string(attacker, defender, position)
                successFlag = 1
            else:
                success = rand(compute_bonus(max(0, defender.grapple() - attacker.grapple())) + wd.grapple_bonus())
                failure = rand(wa.grapple_bonus())
                if failure <= success:
                    if not attacker.is_inflicted_with(statusEffects.Humiliated.name):
                        duration = max(MIN_DURATION, DURATION_MULTIPLIER * rand(compute_bonus(max(0, defender.resilience() - attacker.resilience()))) + self.severity)
                        numSmacks = rand(self.position.maintainability)
                        attacker.inflict_status(statusEffects.build_status(statusEffects.HUMILIATED, duration, numSmacks))
                    #This will also need to be reworked to use the enemy's spanking strings.
                    resultString = spanking.reversed_spanking(attacker, defender, position)
                    successFlag = -1
                else:
                    #This will also need to be reworked to use the enemy's spanking strings.
                    resultString = spanking.failed_spanking(attacker, defender, position)
                    successFlag = 0
            return (resultString, [successFlag], self)
        else:
            return GrappleAction(attacker, defender).effect(inCombat, allies, enemies)


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

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        The damage done (to both enemies) is between 3% and 10% of the grappled character's health.
        """
        attacker = self.attacker
        grappler = self.defenders[0]
        defender = self.defenders[1]
        damRange = (grappler.health() * .1 if grappler.health() * .1 > 1 else 1, grappler.health() * .1 if grappler.health() * .2 > 1 else 1)
        dam = 0
        dam1 = 0
        opponents = enemies if self.attacker in allies else allies
        if not grappler in opponents:
            return AttackAction(attacker, defender).effect(inCombat, allies, enemies)
        if attacker.is_grappling(grappler):
            wa = attacker.weapon()
            wd = grappler.weapon()
            #grappleABonus = wa.grapple_bonus() + attacker.grapple() - attacker.attack_penalty()
            #grappleGBonus = wg.grapple_bonus() + grappler.grapple() - grappler.attack_penalty()
            bonus = compute_bonus(max(0, attacker.grapple() - defender.grapple()))
            success = rand(bonus + wa.grapple_bonus())
            failure = rand(wd.grapple_bonus())
            if failure <= success:
                #betterStat = attacker.warfare() if attacker.warfare() >= attacker.grapple() else attacker.grapple()
                dam = max(1, int(bonus + damRange[0]))
                grappler.receives_damage(dam)   
                attacker.break_grapple()
                if grappler is defender:
                    resultString = ' '.join([attacker.printedName, 'throws', defender.printedName, 'for', str(dam), 'damage!'])
                    dam1 = dam
                    if grappler.current_health() <= 0:
                        resultString = '\n'.join([resultString, ' '.join([defender.printedName, 'collapses!'])])
                else:
                    if not defender in opponents:
                        defender = opponents[randrange(0, len(opponents))]
                    failure = rand(wd.grapple_bonus())
                    success = rand(bonus + wa.grapple_bonus())
                    if failure <= success:
                        dam1 = max(1, int(math.floor(rand(damRange[1] + attacker.grapple()) + damRange[0] - defender.defense())))
                        defender.receives_damage(dam1)
                        resultString = '\n'.join([' '.join([attacker.printedName, 'throws', grappler.printedName, 'for', str(dam), 'damage!']), 
                            ' '.join([attacker.printedName, 'strikes', defender.printedName, 'for', str(dam), 'damage!'])])
                        if grappler.current_health() <= 0:
                            resultString = '\n'.join([resultString, ' '.join([grappler.printedName, 'collapses!'])])
                        if defender.current_health() <= 0:
                            resultString = '\n'.join([resultString, ' '.join([defender.printedName, 'collapses!'])])
                    else:
                        resultString = ' '.join([attacker.printedName, 'throws', grappler.printedName, 'at', defender.printedName + ',', 'doing', str(dam), 'damage to', 
                            grappler.printedName + ',', 'but missing', defender.printedName + '!'])
                        if grappler.current_health() <= 0:
                            resultString = '\n'.join([resultString, ' '.join([grappler.printedName, 'collapses!'])])
            else:
                resultString = ' '.join([attacker.printedName, 'fails to throw', defender.printedName])
            return (resultString, [dam, dam1], self)    
        else:
            return AttackAction(attacker, grappler).effect(inCombat, allies, enemies)

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
    

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        If we try to break our ally's grapple, only to see that the grapple is already broken, then we defend them.
        """
        defenders = self.defenders
        attacker = self.attacker
        if (attacker in allies and not defenders[0] in allies) or (attacker in enemies and not defenders[0] in enemies):
            return DefendAction(self.attacker, self.attacker).effect(inCombat, allies, enemies)
        wa = attacker.weapon()
        defender = defenders[0].grapplingPartner
        if defender is None:
            return DefendAction(attacker, defenders[0]).effect(inCombat, allies, enemies)
        else:
            wd = defender.weapon()
            #grappleABonus = wa.grapple_bonus() + attacker.grapple() - attacker.attack_penalty()
            #grappleDBonus = wd.grapple_bonus() + defender.grapple() - defender.attack_penalty()
            success = rand(compute_bonus(max(0, attacker.grapple() - defender.grapple())) + wa.grapple_bonus())
            failure = rand(wd.grapple_bonus())
            if failure <= success:
                resultStmt = ' '.join([attacker.printedName, 'breaks', defender.printedName + "'s", '''hold on''', defender.grapplingPartner.printedName + '!'])
                defender.break_grapple()
                attacker.grapple(defender)
            else:
                resultStmt = ' '.join([attacker.printedName, "doesn't break", defender.printedName + "'s", 'hold on', defender.grapplingPartner.printedName + '!'])
            return (resultStmt, [None], self) 


class DefendAction(CombatAction):
    targetType = ALLY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = SPELL_SLINGERS
    numTargets = 1
    primaryStat = universal.WILLPOWER
    secondaryStat = universal.DEXTERITY
    actionType = 'defend'
    def __init__(self, attacker, defenders):
        super(DefendAction, self).__init__(attacker, defenders, RESILIENCE, DefendAction.secondaryStat)
        self.targetType = ALLY
        self.grappleStatus = GRAPPLER_ONLY
        self.primaryStat = DefendAction.primaryStat
        #Want to make sure to defend your spell slingers
        self.effectClass = SPELL_SLINGERS
        self.actionType = 'defend'

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple: The result, [None], this action.
        The reason this returns a triple rather than a double, is so that we don't have to do anything special with the defend action in the combat code.
        """
        attacker = self.attacker
        defender = self.defenders[0]
        if attacker == defender:
            attacker.inflict_status(statusEffects.DefendStatus(1))
            return (' '.join([attacker.printedName, 'defends', person.himselfherself(attacker) + '!']), [None], self)
        else:
            companions = allies if attacker in allies else enemies
            if defender not in companions:
                return DefendAction(attacker, attacker).effect(inCombat, allies, enemies)
            defender.guardian = attacker
            return (' '.join([attacker.printedName, 'defends', defender.printedName + '!']), [None], self)

