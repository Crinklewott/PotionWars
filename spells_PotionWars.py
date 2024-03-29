
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
import combatAction
from combatAction import GRAPPLER_ONLY, ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY, ONLY_WHEN_GRAPPLED, UNAFFECTED, NOT_WHEN_GRAPPLED, WARRIORS_GRAPPLERS, SPELL_SLINGERS, ALL, ALLY, ENEMY
import math
import person as p
from person import BASIC, ADVANCED, EXPERT
import random
import spanking
import statusEffects
import universal
from universal import *
#---------------------------------------------------------------Tier 0----------------------------------------------------------------------
#--------------------------------------------------------------Tier 0 Combat----------------------------------------------------------------
class Firebolt(p.Combat):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 1
    tier = 0
    cost = 3
    name = 'Firebolt'

    def __init__(self, attacker, defenders):
        super(Firebolt, self).__init__(attacker, defenders)
        self.description = 'Flings a small bolt of fire at a single opponent.' 
        self.effectFormula = 'DAMAGE: magic + bonus(magic - enemy.magic)'
        self.numTargets = 1
        self.minDamage = 2 
        self.magicMultiplier = 1
        self.expertise = BASIC

    def effect_statement(self, defender, dam):
        self.effectStatements = [[self.attacker.printedName, 'casts Firebolt at', defender.printedName, 'for', str(dam), 'damage!']]
        return super(Firebolt, self).effect_statement(defender)

    def immune_statement(self, defender):
        return [defender.printedName, 'smirks as the flames dance harmlessly across', defender.hisher(), 'body.']

        

class Icebolt(p.Combat):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    tier = 0
    numTargets = 1
    cost = 4
    name = 'Icebolt'
    def __init__(self, attacker, defenders):
        super(Icebolt, self).__init__(attacker, defenders)
        self.description = 'Flings a small icicle at a single opponent.' 
        self.effectFormula = 'DAMAGE: magic + bonus(1.2 * magic - enemy.magic)'
        self.numTargets = 1
        self.minDamage = 3 
        self.magicMultiplier = 1.2
        self.expertise = ADVANCED
    
    
    def effect_statement(self, defender, dam):
        self.effectStatements = [[self.attacker.printedName, 'casts Icebolt at', defender.printedName, 'for', str(dam), 'damage!']]
        #self.effectStatements = [[self.attacker.name, '\'s fist becomes coated in frost.', He_She(self.attacker), 'snaps', hisher(self.attacker), 'fist forward. An icicle erupts from', hisher(self.attacker), 'fist and strikes', defender.name, 'in the chest.']]
        return super(Icebolt, self).effect_statement(defender)

    def immune_statement(self, defender):
        immuneStatement = [defender.printedName, 'smirks as the icicle shatters harmlessly against', defender.hisher(), 'body.']


class Magicbolt(p.Combat):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 1
    tier = 0
    cost = 5
    name = 'Magicbolt'
    def __init__(self, attacker, defenders):
        super(Magicbolt, self).__init__(attacker, defenders)
        self.description = 'Flings a small bolt of raw magic at a single opponent.' 
        self.effectFormula = 'DAMAGE: magic + bonus(1.4 * magic - enemy.magic)'
        self.numTargets = 1
        self.minDamage = 4
        self.magicMultiplier = 1.4
        self.rawMagic = True
        self.expertise = EXPERT


    def effect_statement(self, defender, dam):
        self.effectStatements = [[self.attacker.printedName, 'casts Magicbolt at', defender.printedName, 'for', str(dam), 'damage!']]
        return super(Magicbolt, self).effect_statement(defender)

    def immune_statement(self, defender):
        return [defender.printedName, 'smirks as the magic dissipates harmlessly against', defender.hisher(), 'body.']

#Note these are "empty" actions for use in displaying and learning spells. When actually casting spells in combat, a new object should be created with the attacker and 
#defender(s) specified.
firebolt = Firebolt(None, None)
icebolt = Icebolt(None, None)
magicbolt = Magicbolt(None, None)
p.allSpells[0] = [(firebolt, icebolt, magicbolt)]
#--------------------------------------------------------------Tier 0 Status----------------------------------------------------------------
class Weaken(p.Status):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 1
    tier = 0
    cost = 1
    statusInflicted = statusEffects.WEAKENED
    name = 'Weaken'
    def __init__(self, attacker, defenders):
        super(Weaken, self).__init__(attacker, defenders)
        self.description = 'Wraps your enemy in a field that interferes with the implicit magic responsible for lending strength to their muscles, making them physically weaker and slower.'
        self.effectFormula = 'EFFECT: -2 penalty to Dexterity and Strength\nDURATION: max(2, resilience - enemy.resilience)'
        self.numTargets = 1
        self.rawMagic = True
        self.statusInflicted = statusEffects.WEAKENED
        self.effectClass = combatAction.WARRIORS_GRAPPLERS
        self.resilienceMultiplier = 1
        self.expertise = ADVANCED
        self.minDuration = 3
        self.magicMultiplier = 1
        self.minProbability = 50
        self.maxProbability = 98

    def effect_statement(self, defender):
        attacker = self.attacker
        #self.effectStatements = [[attacker.name, 'points', hisher(attacker), 'finger at,' defender.name, '. A beam of red light flies from', attacker.name, '\'s fignertip and strikes', defender.name, '. The beam disperses into a cocoon of light that then fuses with', defender.name, '\'s skin.']]
        #self.effectStatements = [[attacker.name, 'points', hisher(attacker), 'finger at', defender.name, '. A beam of red light flies from', attacker.name, '\'s fignertip and strikes', defender.name, '. The beam disperses into a cocoon of light that then fuses with', defender.name, '\'s skin.']]
        self.effectStatements = [[attacker.printedName, 'casts Weaken on', defender.printedName + '!']]
        return super(Weaken, self).effect_statement(defender)

    def immune_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is immune!']

    def failure_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'resists!']

    def success_statement(self, defender):
        return [defender.printedName, 'is weakened!']


class DistortMagic(p.Status):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = SPELL_SLINGERS
    numTargets = 1
    tier = 0
    statusInflicted = statusEffects.MAGIC_DISTORTED
    cost = 1
    name = 'Distort Magic'
    def __init__(self, attacker, defenders):
        super(DistortMagic, self).__init__(attacker, defenders)
        self.description = 'Wraps your enemy in a field that interferes with their ability to cast and protect against spells.'
        self.effectFormula = 'EFFECT: -2 penalty to Talent and Willpower\n DURATION: max(0, resilience - enemy.resilience)'
        self.numTargets = 1
        self.rawMagic = True
        self.statusInflicted = statusEffects.MAGIC_DISTORTED
        self.effectClass = combatAction.SPELL_SLINGERS
        self.resilienceMultiplier = 15
        self.magicMultiplier = 2
        self.expertise = BASIC
        self.maxProbability = 95
        self.minProbability = 50
        self.minDuration = 3


    def effect_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        self.effectStatements = [[A, 'casts Distort Magic on', D + "!"]]
        #self.effectStatements = [[A, 'sweeps', hisher(attacker), 'arm in an arc in front of', himselfherself(attacker), 'as if', p.heshe(attacker),
        #   'were scattering birdseed. Half a dozen small red robs fly from', A, 'and strike', E,'.']]
        return super(DistortMagic, self).effect_statement(defender)

    def immune_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is immune!']

    def failure_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'resists!']

    def success_statement(self, defender):
        return [defender.printedName, 'is distorted!']



class WeakCharm(p.CharmMagic):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 0
    statusInflicted = statusEffects.CHARMED
    cost = 7
    name = 'Weak Charm'
    def __init__(self, attacker, defenders):
        super(WeakCharm, self).__init__(attacker, defenders)
        self.description = 'The weakest of the mind control spells. Even this simple charm spell is so complex, that only a specialist can cast it without permanently damaging the recipient\'s brain. Furthermore, it can only be cast when the caster is grappling an opponent.'
        self.effectFormula = 'EFFECT: Target is forced to fight for their opponents\nSUCCESS CHANCE (%): 20 | 10 * resilience bonus\n DURATION: 4 | 4 *magic bonus'
        self.numTargets = 1
        self.rawMagic = False
        self.statusInflicted = statusEffects.CHARMED
        self.effectClass = combatAction.ALL
        self.expertise = EXPERT
        self.minProbability = 20
        self.resilienceMultiplier = 10
        self.magicMultiplier = 4
        self.minDuration = 4

    def effect_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        self.effectStatements = [[A, 'casts Weak Charm on', D + "!"]]
        return super(WeakCharm, self).effect_statement(defender)

    def immune_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is immune!']

    def failure_statement(self, defender):
        D = defender.printedName
        return [D, 'resists!']

    def success_statement(self, defender):
        return [defender.printedName, 'is charmed!']

weaken = Weaken(None, None)
distortMagic = DistortMagic(None, None)
weakCharm = WeakCharm(None, None)
p.allSpells[0].append((distortMagic, weaken, weakCharm))
#--------------------------------------------------------------Tier 0 Buff----------------------------------------------------------------

class Heal(p.Healing):
    targetType = ALLY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 0
    cost = 2
    name = 'Heal'
    def __init__(self, attacker, defenders):
        super(Heal, self).__init__(attacker, defenders)
        self.fortify = False
        self.numTargets = 1
        self.description = 'Converts mana into health, and infuses the recipient with it.'
        self.effectFormula = 'HEALS: between 1.2 * magic and target\'s health - target\'s current health'
        self.magicMultiplier = 1.2
        self.rawMagic = True
        self.expertise = BASIC

    def effect_statement(self, defender):
        caster = self.attacker
        C = caster.printedName
        D = defender.printedName
        self.effectStatements = [['']]
        return super(Heal, self).effect_statement(defender)

class Fortify(p.Healing):
    targetType = ALLY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 0
    cost = 3
    name = 'Fortify'
    def __init__(self, attacker, defenders):
        super(Fortify, self).__init__(attacker, defenders)
        self.fortify = True
        self.cost = Fortify.cost
        self.numTargets = 1
        self.fortifyCap = 40
        self.description = 'Converts mana into health, and infuses the recipient with it. Note that this spell can heal a character past their maximum health. However, it has no effect if the character\'s current health is already above its maximum. Unfortunately, because of the extra energy needed to infuse a character with extra health, this spell does not heal as many hit points as Heal. It caps out at 40.'
        self.effectFormula = 'HEALS: between magic and 40'
        self.magicMultiplier = 1
        self.rawMagic = True
        self.expertise = ADVANCED


    def effect_statement(self, defender):
        caster = self.attacker
        C = caster.printedName
        D = defender.printedName
        self.effectStatements = [[C, 'casts', self.name, 'on', D + '!\n']]
        #self.effectStatements = [[C, 'takes a deep breath.', He_She(caster), 'breathes out, and sweeps', hisher(caster), 'hands towards', D, '.']]
        return super(Fortify, self).effect_statement(defender)


class SuperFortify(p.Healing):
    targetType = ALLY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 0
    cost = 4
    name = 'Super Fortify'
    def __init__(self, attacker, defenders):
        super(SuperFortify, self).__init__(attacker, defenders)
        self.fortify = True
        self.fortifyCap = 50
        self.numTargets = 1
        self.description = 'Converts mana into health, and infuses the recipient with it. Note that this spell can heal a character past their maximum health. However, it has no effect if the character\'s current health is already above its maximum. Furthermore, it is just as powerful as Heal. However, it is also slightly more expensive than Fortify. It caps out at 45.'
        self.effectFormula = 'HEALS: 2*magic | 50'
        self.magicMultiplier = 2
        self.rawMagic = True
        self.expertise = EXPERT


    def effect_statement(self, defender):
        caster = self.attacker
        C = caster.printedName
        D = defender.printedName
        self.effectStatements = [[C, 'casts', self.name, 'on', D + '!']]
        #self.effectStatements = [[C, 'takes a deep breath.', He_She(caster), 'breathes out, and sweeps', hisher(caster), 'hands towards', D, '.']]
        return super(SuperFortify, self).effect_statement(defender)

heal = Heal(None, None)
fortify = Fortify(None, None)
superFortify = SuperFortify(None, None)
p.allSpells[0].append((heal, fortify, superFortify))

#-------------------------------------------------------------------------Tier 0 Spectral--------------------------------------------------------------



class SpectralPush(p.Spectral):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 1
    cost = 2
    name = 'Spectral Push'
    def __init__(self, attacker, defenders):
        super(SpectralPush, self).__init__(attacker, defenders)
        self.targetType = combatAction.ENEMY
        self.rawMagic = True
        self.numTargets = 1
        self.effectClass = combatAction.WARRIORS_GRAPPLERS
        self.minDamage = 1
        self.successMultiplier = 40
        self.minProbability = 40
        self.maxProbability = 95
        self.magicMultiplier = 2
        self.expertise = BASIC
        self.description = 'Unleashes a battering ram of raw magical power into an enemy\'s body, potentially flinging them backwards several feet. Has a chance of breaking a grapple. The greater the caster\'s magic compared to the target, the better the chance.'
        self.effectFormula = 'DAMAGE: 1 | 2 * magic bonus\nSUCCESS CHANCE (%): 40 | 40*magic bonus'

    def effect(self, inCombat=True, allies=None, enemies=None):
        """
        Returns a triple:
        1. A string describing the result
        2. A pair containing the damage done and whether or not the grapple was successfully broken
        3. This action
        """
        super(SpectralPush, self).effect(inCombat)
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker = self.attacker
        if not attacker.is_grappling():
            attacker.increase_stat(universal.MANA, self.cost)
            return combatAction.DefendAction(attacker, attacker)
        opponents = enemies if self.attacker in allies else allies
        effects = []
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
        damage = max(self.minDamage, self.attacker.magic_attack() - defender.magic_defense(self.rawMagic))
        successProbability = min(self.maxProbability, max(self.minProbability, self.successMultiplier * (self.attacker.magic_attack() - defender.magic_defense(self.rawMagic))))
        success = random.randint(1, 100)
        resultStatement = []
        resultStatement.append(self.effect_statement(defender, damage))
        if defender.ignores_spell(self):
            resultStatement.append(self.immune_statement(defender))
            effects.append((0, False))
        elif success <= successProbability:
            self.attacker.break_grapple()
            defender.receives_damage(damage)
            effects.append((damage, True))
            resultStatement.append(self.success_statement(defender))
        else:
            defender.receives_damage(damage)
            resultStatement.append(self.failure_statement(defender))
            effects.append((damage, False))
        if defender.current_health() <= 0:
            resultStatement[-1] = ['\n'.join([resultStatement[-1][0], ' '.join([defender.printedName, 'collapses!'])])]
        return (universal.format_text(resultStatement, False), effects, self)


    def effect_statement(self, defender, dam):
        A = self.attacker.printedName
        attacker = self.attacker
        D = defender.printedName
        self.effectStatements = [[A, 'casts Spectral Push on', D, 'for', str(dam), 'damage!']]
        #self.effectStatements = [['With a primal screen,', A, 'arches', hisher(attacker), 'back, then snaps forward,', hisher(attacker), 'hands snap out in front of', him_her(attacker), '. A battering ram of pure magic erupts from', A, '\'s body and slams into', D, '.']]
        return super(SpectralPush, self).effect_statement(defender)

    def success_statement(self, defender):
        A = self.attacker.printedName
        attacker = self.attacker
        D = defender.printedName
        return ['Grapple broken!']

    def immune_statement(self, defender):
        return [defender.printedName, 'is immune!']

    def failure_statement(self, defender):
        return ['Grapple not broken!']

class SpectralPull(p.Spectral):
    targetType = ENEMY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = SPELL_SLINGERS
    numTargets = 1
    tier = SpectralPush.tier
    cost = 3
    name = 'Spectral Pull'
    def __init__(self, attacker, defenders):
        super(SpectralPull, self).__init__(attacker, defenders)
        self.targetType = combatAction.ENEMY
        self.rawMagic = True
        self.effectClass = combatAction.ALL
        self.minDamage = 1
        self.magicMultiplier = 2
        self.successMultiplier = 40
        self.numTargets = 1
        self.minProbability = 40
        self.maxProbability = 95
        self.description = 'Wraps the target in a cord of pure magic. In addition to disrupting the target\'s health, the cord can be used to yank the target into a grapple. The chances of successfully grappling the target depends on the relative levels of the caster\'s and target\'s magic.'
        self.effectFormula = 'DAMAGE: 1 | 2 * magic bonus\nSUCCESS CHANCE (%): 40 | 40 *magic bonus | 95'
        self.expertise = ADVANCED


    def effect(self, allies=None, enemies=None, inCombat=True):
        """
        Returns a triple:
        1. A string describing the result
        2. A pair containing the damage done and whether or not the grapple was successfully broken
        3. This action
        """
        super(SpectralPull, self).effect(inCombat)
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker  = self.attacker
        defenders = self.defenders
        opponents = enemies if attacker in allies else allies
        currentDefenders = list(defenders)
        effects = []
        for defender in defenders:
            if not defender in opponents:
                availableOpponents = [opp for opp in opponents if opp not in currentDefenders]
                if availableOpponents == []:
                    continue
                else:
                    defender = availableOpponents[random.randrange(0, len(availableOpponents))]
                    currentDefenders.append(defender)
        defender = defenders[0]
        damage = max(self.minDamage, attacker.magic_attack() - defender.magic_defense(self.rawMagic))
        successProbability = min(self.maxProbability, max(self.minProbability, self.successMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))))
        success = random.randint(1, 100)
        resultStatement = []
        damageStatement = [attacker.printedName, 'does', damage, 'damage to', defender.printedName]
        resultStatement.append(self.effect_statement(defender, damage))
        if defender.ignores_spell(self):
            resultStatement.extend(self.immune_statement(defender, damage))
            effects.append((0, False))
        elif success <= successProbability:
            self.attacker.grapple(defender)
            defender.grapple(attacker)
            defender.receives_damage(damage)
            resultStatement.extend(self.success_statement(defender))
            effects.append((damage, True))
        else:
            defender.receives_damage(damage)
            resultStatement.extend(self.failure_statement(defender))
            effects.append((damage, False))
        if defender.current_health() <= 0:
            resultStatement[-1] = '\n'.join([resultStatement[-1], ' '.join([defender.printedName, 'collapses!'])])
        return (universal.format_text(resultStatement, False), effects, self)

    def effect_statement(self, defender, dam):
        A = self.attacker.printedName
        attacker = self.attacker
        D = defender.printedName
        self.effectStatements = [format_line([A, 'casts Spectral Pull on', D, 'for', str(dam), 'damage!'])]
        return super(SpectralPull, self).effect_statement(defender)

    def success_statement(self, defender):
        A = self.attacker.printedName
        attacker = self.attacker
        D = defender.printedName
        return [[A, 'grapples', D, '.']]

    def immune_statement(self, defender):
        return [[defender.printedName, 'is immune!']]

    def failure_statement(self, defender):
        return [[defender.printedName, 'is not grappled!']]


class SpectralShove(p.Spectral):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = SpectralPush.tier
    cost = 4
    name = 'Spectral Shove'
    def __init__(self, attacker, defenders):
        super(SpectralShove, self).__init__(attacker, defenders)
        self.targetType = combatAction.ENEMY
        self.rawMagic = True
        self.effectClass = combatAction.WARRIORS_GRAPPLERS
        self.minDamage = 2
        self.magicMultiplier = 2
        self.numTargets = 1
        self.successMultiplier = 50
        self.minProbability = 50
        self.expertise = EXPERT
        self.maxProbability = 100
        self.description = 'A spectral specialist has spent years studying sophisticated techniques for more efficiently and powerfully shaping raw magical energy. Their hard work pays off in the ability to cast spectral shove. Spectral shove is twice as powerful as spectral push, has a significantly higher chance of breaking a grapple, and is cheaper to boot.'
        self.effectFormula = 'DAMAGE: 2 | 4* magic bonus\nSUCCESS CHANCE (%): 50 | 50*magic bonus | 95'



    def effect(self, inCombat=True, allies=None, enemies=None):
        super(SpectralShove, self).effect(inCombat)
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        attacker = self.attacker
        if not attacker.is_grappling():
            attacker.increase_stat(universal.MANA, self.cost)
            return combatAction.DefendAction(attacker, attacker)
        defenders = self.defenders
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
        defender = self.defenders[0]
        damage = max(self.minDamage, attacker.magic_attack() - defender.magic_defense(self.rawMagic))
        successProbability = min(self.maxProbability, max(self.minProbability, self.successMultiplier * (attacker.magic_attack() - defender.magic_defense(self.rawMagic))))
        success = random.randint(1, 100)
        resultStatement = []
        effects = []
        damageStatement = [attacker.printedName, 'does', damage, 'damage to', defender.printedName]
        resultStatement.append(self.effect_statement(defender, damage))
        if defender.ignores_spell(self):
            resultStatement.extend(self.immune_statement(defender))
            effects.append((0, False))
        elif success <= successProbability:
            self.attacker.break_grapple()
            defender.receives_damage(damage)
            resultStatement.extend(self.success_statement(defender))
            effects.append((damage, True))
        else:
            defender.receives_damage(damage)
            resultStatement.extend(self.failure_statement(defender))
            effects.append((damage, False))
        if defender.current_health() <= 0:
            resultStatement[-1] = '\n'.join([resultStatement[-1], ' '.join([defender.printedName, 'collapses!'])])
        return (universal.format_text(resultStatement, False), effects, self)

    def effect_statement(self, defender, dam):
        A = self.attacker.printedName
        attacker = self.attacker
        D = defender.printedName
        self.effectStatements = [format_line([A, 'casts Spectral Shove on', D, 'for', str(dam), 'damage!'])]
        return format_line([A, 'casts Spectral Shove on', D, 'for', str(dam), 'damage!'])

    def success_statement(self, defender):
        A = self.attacker.printedName
        attacker = self.attacker
        D = defender.printedName
        return [['Grapple broken!']]

    def immune_statement(self, defender):
        return [[defender.printedName, 'is immune!']]

    def failure_statement(self, defender):
        return [['Grapple not broken!']]

            

spectralPush = SpectralPush(None, None)
spectralPull = SpectralPull(None, None)
spectralShove = SpectralShove(None, None)
p.allSpells[1] = [(spectralPush, spectralPush, spectralPush)]

#---------------------------------------------------------Tier 1-------------------------------------------------------------------------------
#---------------------------------------------------------Tier 1 Combat Spells-------------------------------------------------------------------------------
class Lightningbolt(p.Combat):
    targetType = ENEMY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 3
    tier = 1
    cost = 6
    name = 'Lightningbolt'
    def __init__(self, attacker, defenders):
        super(Lightningbolt, self).__init__(attacker, defenders)
        self.description = 'Unleashes a trio of lightning bolts from the caster\'s fingertips. Does as much damage as firebolt, but affects up to 3 enemies at once. Unfortunately, casting this spell while grappling would hurt the caster as much as the target, so it can\'t be cast when the caster is grappling.' 
        self.effectFormula = 'DAMAGE: 2 -> 2 * magic bonus'
        self.numTargets = 3
        self.minDamage = 2 
        self.magicMultiplier = 2
        self.expertise = BASIC

    def effect_statement(self, defender, dam):
        self.effectStatements = [[self.attacker.printedName, 'electrocutes', defender.printedName, 'for', str(dam), 'damage!']]
            #self.effectStatements = [[self.attacker.name, 'holds up', hisher(attacker), 'hands, fingers extended. An arc of lightning snaps from', self.attacker.name, '\'s fingertips and slams into', defender.name, '.']]
        return super(Lightningbolt, self).effect_statement(defender)

    def immune_statement(self, defender):
        return [defender.printedName, 'stands calmly while the lightning dances harmlessly across', defender.hisher(), 'body.']




class Thunderbolt(p.Combat):
    targetType = ENEMY
    grappleStatus = NOT_WHEN_GRAPPLED
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 3
    tier = 1
    cost = 8
    name = 'Thunderbolt'
    def __init__(self, attacker, defenders):
        super(Thunderbolt, self).__init__(attacker, defenders)
        self.description = 'A more powerful version of Lightningbolt. Does as much damage as Icebolt to up to 3 enemies.' 
        self.effectFormula = 'DAMAGE: 3 -> 3 * magic bonus'
        self.numTargets = 3
        self.minDamage = 3 
        self.magicMultiplier = 3
        self.expertise = ADVANCED


    def effect_statement(self, defender, dam):
        self.effectStatements = [[self.attacker.printedName, 'electrocutes', defender.printedName, 'for', str(dam), 'damage!']]
        #   self.effectStatements = [[self.attacker.printedName, 'holds up', hisher(attacker), 'hands, fingers extended. Twin bolts of lightning snap from', self.attacker.printedName, '\'s fingertips and slam into', defender.printedName, '.']]
        return super(Thunderbolt, self).effect_statement(defender)

    def immune_statement(self, defender):
        return [defender.printedName, 'stands calmly while the lightning dances harmlessly across', defender.hisher(), 'body.']


class Magicstrike(p.Combat):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 3
    tier = 1
    cost = 7
    name = 'Magic Strike'
    def __init__(self, attacker, defenders):
        super(Magicstrike, self).__init__(attacker, defenders)
        self.description = 'What the average spellcaster can do with lightning, a specialist can do with far more powerful (but volatile) raw magical energy. In addition to being more powerful and more efficient then Thunderbolt, this spell can be cast when grappled. Unfortunately, iron provides protection against this spell.' 
        self.effectFormula = 'DAMAGE: 4 -> 4 * magic bonus'
        self.numTargets = 3
        self.minDamage = 4 
        self.magicMultiplier = 4
        self.expertise = EXPERT
        self.rawMagic = True

    def effect_statement(self, defender, dam):
        self.effectStatements = [[self.attacker.printedName, 'unleashes a barrage of raw magic into', defender.printedName, 'for', str(dam), 'damage!']]
            #self.effectStatements = [[self.attacker.printedName, 'holds up', hisher(attacker), 'hands, fingers extended. Twin bolts of lightning snap from', self.attacker.printedName, '\'s fingertips and slam into', defender.printedName, '.']]
        return super(Magicstrike, self).effect_statement(defender)

    def immune_statement(self, defender):
        return [defender.printedName, 'stands calmly while the magical energy disperses harmlessly across', defender.hisher(), 'body.']

lightningBolt = Lightningbolt(None, None) 
thunderBolt = Thunderbolt(None, None) 
magicStrike = Magicstrike(None, None)
p.allSpells[1].append((lightningBolt, thunderBolt, magicStrike))
#---------------------------------------------------------Tier 1 Status Spells-------------------------------------------------------------------------------
class MassWeaken(p.Status):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 3
    tier = 1
    statusInflicted = statusEffects.WEAKENED
    cost = 4
    name = 'Mass Weaken'

    def __init__(self, attacker, defenders):
        super(MassWeaken, self).__init__(attacker, defenders)
        self.description = 'Wraps up to 3 enemies in a field that interferes with the implicit magic responsible for lending strength to their muscles, making them physically weaker and slower.'
        self.effectFormula = 'EFFECT: -2 penalty to Strength and Dexterity\nSUCCESS CHANCE (%): 30 | 15 * resilience bonus | 98 \nDURATION: 3 | magic bonus'
        self.resilienceMultiplier = 15
        self.numTargets = 3
        self.rawMagic = True
        self.statusInflicted = statusEffects.WEAKENED
        self.effectClass = combatAction.WARRIORS_GRAPPLERS
        self.expertise = BASIC
        self.magicMultiplier = 1
        self.minDuration = 2
        self.minProbability = 30
        self.maxProbability = 98


    def effect_statement(self, defender):
        attacker = self.attacker
        self.effectStatements = ([[attacker.printedName, 'casts Mass Weaken on', defender.printedName + "!"]])
        """
        self.effectStatements = ([[attacker.name, 'points', hisher(attacker), 'finger at', defender.name, '. A beam of red light flies from ', attacker.name, 
            '\'s fignertip and strikes', defender.name, '. The beam disperses into a cocoon of light that then fuses with', defender.name, '\'s skin.']])
        """
        return super(MassWeaken, self).effect_statement(defender)

    def immune_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is immune!']

    def failure_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'resists!']

    def success_statement(self, defender):
        return [defender.printedName, 'is weakened!']


class MassDistortMagic(p.Status):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = SPELL_SLINGERS
    numTargets = 3
    tier = 1
    statusInflicted = statusEffects.MAGIC_DISTORTED
    cost = 4
    name = 'Mass Distort Magic'
    def __init__(self, attacker, defenders):
        super(MassDistortMagic, self).__init__(attacker, defenders)
        self.description = 'Wraps up to 3 enemies in a field that interfers with their ability to cast and protect against spells.'
        self.effectFormula = 'EFFECT: -2 penalty to Talent and Willpower\nSUCCESS CHANCE (%): 40 | 15 * resilience bonus | 95\n DURATION: 3 | 2 *magic bonus'
        self.numTargets = 3
        self.rawMagic = True
        self.magicMultiplier = 2
        self.statusInflicted = statusEffects.MAGIC_DISTORTED
        self.effectClass = combatAction.SPELL_SLINGERS
        self.resilienceMultiplier = 15
        self.expertise = ADVANCED
        self.maxProbability = 95
        self.minProbability = 40

    
    def effect_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        self.effectStatements = [[A, 'casts Mass Distort Magic on', D + "!"]]
        #self.effectStatements = [[A, 'sweeps', hisher(attacker), 'arm in an arc in front of', himselfherself(attacker), 'as if', p.heshe(attacker),
        #   'were scattering birdseed. Half a dozen small red robs fly from', A, 'and strike', E,'.']]
        return super(MassDistortMagic, self).effect_statement(defender)

    def immune_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is immune!']

    def failure_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'has resisted the Mass Distort Magic spell!']

    def success_statement(self, defender):
        return [defender.printedName, 'is distorted!']

class Charm(p.CharmMagic):
    targetType = ENEMY
    grappleStatus = ONLY_WHEN_GRAPPLED_GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 1
    statusInflicted = statusEffects.CHARMED
    cost = 7
    name = 'Charm'
    def __init__(self, attacker, defenders):
        super(Charm, self).__init__(attacker, defenders)
        self.description = 'A more powerful version of Weak Charm. Charm has a higher chance of success and lasts longer.'
        self.effectFormula = 'EFFECT: Target is forced to fight for their enemies.\nSUCCESS CHANCE (%): 30 | 20 * resilience bonus | 95 \n DURATION: 4 | 4 *magic bonus'
        self.numTargets = 1
        self.rawMagic = False
        self.statusInflicted = statusEffects.CHARMED
        self.effectClass = combatAction.ALL
        self.expertise = EXPERT
        self.minProbability = 20
        self.resilienceMultiplier = 20

    def effect_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        self.effectStatements = [[A, 'casts Charm on', D + "!"]]
        #self.effectStatements = [[A, 'grabs', D, '\'s chin, and forces', him_her(defender), 'to look in', hisher(attacker), 'eyes.', His-Her(attacker), 'eyes swirl through a hypnotic whirl of colors.']]
        return super(Charm, self).effect_statement(defender)

    def immune_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is immune!']

    def success_statement(self, defender):
        A = self.attacker.printedName
        D = defender.printedName
        return [D, 'is charmed!']

    def failure_statement(self, defender):
        D = defender.printedName
        return [D, 'resists!']

massWeaken = MassWeaken(None, None) 
massDistortMagic = MassDistortMagic(None, None) 
charm = Charm(None, None)
p.allSpells[1].append((massWeaken, massDistortMagic, charm))
#---------------------------------------------------------Tier 1 Buff Spells-------------------------------------------------------------------------------
class Shield(p.Buff):
    targetType = ALLY
    grappleStatus = GRAPPLER_ONLY
    effectClass = SPELL_SLINGERS
    numTargets = 1
    tier = 1
    statusInflicted = statusEffects.SHIELDED
    cost = 3
    name = 'Shield'
    def __init__(self, attacker, defenders):
        super(Shield, self).__init__(attacker, defenders)
        self.description = 'Wraps an ally in a magical shield that protects them from physical attacks.'
        self.effectFormula = 'EFFECT: +2 defense\nDURATION: magic'
        self.rawMagic = True
        self.expertise = BASIC
        self.magicMultiplier = 1
        self.statusInflicted = statusEffects.SHIELDED
        self.minDuration = 1
        self.numTargets = 1
        self.effectClass = combatAction.SPELL_SLINGERS


    def effect_statement(self, defender):
        caster = self.attacker
        C = caster.printedName
        D = defender.printedName
        #self.effectStatements = [format_line([C, 'casts Shield on', D + "!"])]
        return format_line([C, 'casts Shield on', D + "!"])
        #self.effectStatements = [[C, 'presses hisher(caster) fist against', hisher(caster), 'chest. Then,', p.heshe(caster), 'holds out', hisher(caster), 'hand towards', D, 
        #',palm up. A curtain of magic flows from', hisher(caster), 'palm and wraps itself around', D, '.\n', D, 'is protected from physical attacks!']]
        #return super(Shield, self).effect_statement(defender)

    def success_statement(self, defender):
        return [defender.printedName, 'is protected!']


class MagicShield(p.Buff):
    targetType = ALLY
    grappleStatus = GRAPPLER_ONLY
    effectClass = WARRIORS_GRAPPLERS
    numTargets = 1
    tier = 1
    statusInflicted = statusEffects.MAGIC_SHIELDED
    cost = 3
    name = 'Magic Shield'
    def __init__(self, attacker, defenders):
        super(MagicShield, self).__init__(attacker, defenders)
        self.description = 'Wraps an ally in a magical shield that protects them from magical attacks.'
        self.effectFormula = 'EFFECT: +2 magic defense\nDURATION: magic'
        self.magicMultiplier = 1
        self.rawMagic = True
        self.statusInflicted = statusEffects.MAGIC_SHIELDED
        self.minDuration = 1
        self.numTargets = 1
        self.effectClass = combatAction.WARRIORS_GRAPPLERS
        self.expertise = ADVANCED

    def effect_statement(self, defender):
        caster = self.attacker
        C = caster.printedName
        D = defender.printedName
        self.effectStatements = [[C, 'casts Magic Shield on', D + '!']]
        #self.effectStatements = [[C, 'presses hisher(caster) fist against', hisher(caster), 'chest. Then,', p.heshe(caster), 'holds out', hisher(caster), 'hand towards', D, 
        #',palm up. A curtain of magic flows from', hisher(caster), 'palm and wraps itself around', D, '.\n', D, 'is protected from magical attacks!']]
        return super(MagicShield, self).effect_statement(defender)

    def success_statement(self, defender):
        return [defender.printedName, 'is protected!']

class SuperShield(p.Buff):
    targetType = ALLY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = 1
    statusInflicted = statusEffects.SHIELDED
    cost = 3
    name = 'Super Shield'
    def __init__(self, attacker, defenders):
        super(SuperShield, self).__init__(attacker, defenders)
        self.description = 'Wraps an ally in a magical shield that protects them from physical and magical attacks.'
        self.effectFormula = 'EFFECT: +2 defense, +2 magic defense\nDURATION: magic'
        self.magicMultiplier = 1
        self.rawMagic = True
        self.statusInflicted = statusEffects.SHIELDED
        self.minDuration = 1
        self.numTargets = 1
        self.effectClass = combatAction.ALL
        self.expertise = EXPERT

    def effect_statement(self, defender):
        caster = self.attacker
        C = caster.printedName
        D = defender.printedName
        self.effectStatements = [[C, 'casts Super Shield on', D + "!"]]
        #self.effectStatements = [[C, 'presses hisher(caster) fist against', hisher(caster), 'chest. Then,', p.heshe(caster), 'holds out', hisher(caster), 'hand towards', D, 
        #',palm up. A curtain of magic flows from', hisher(caster), 'palm and wraps itself around', D, '.\n', D, 'is protected from physical and magical attacks!']]
        return super(SuperShield, self).effect_statement(defender)


    def effect(self, inCombat=True, allies=None, enemies=None):
        super(SuperShield, self).effect(inCombat)
        spankingEffect = self.being_spanked()
        if spankingEffect:
            return spankingEffect
        recipient = self.defenders[0]
        caster = self.attacker
        resultStatement = []
        if caster != recipient:
            #The iron penalty applies only if we're currently in combat.
            duration = self.magicMultiplier * (caster.magic_attack(inCombat) + recipient.iron_modifier(self.rawMagic, inCombat))
        else:
            #Because the buff spell is being cast on the caster, the magic never actually leaves the person's body, so it isn't affected by the caster's iron.
            duration = self.magicMultiplier * caster.magic_attack(False)
        recipient.inflict_status(statusEffects.build_status(statusEffects.SHIELDED, duration))
        recipient.inflict_status(statusEffects.build_status(statusEffects.MAGIC_SHIELDED, duration))
        resultStatement.extend(self.effect_statement(recipient))
        resultStatement.append('\n')
        resultStatement.extend(self.success_statement(recipient))
        return resultStatement

    def success_statement(self, defender):
        return [defender.printedName, 'is protected!']


shield = Shield(None, None) 
magicShield = MagicShield(None, None) 
superShield = SuperShield(None, None)
p.allSpells[1].append((shield, magicShield, superShield))

#---------------------------------------------------------Tier 1 Spectral Spells-------------------------------------------------------------------------------


class SpectralStrapping(p.SpectralSpanking):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = p.SpectralSpanking.tier
    statusInflicted = statusEffects.HUMILIATED
    cost = 16
    severity = spanking.LEATHER_STRAP_SEVERITY
    name = 'Spectral Strapping'
    def __init__(self, attacker, defenders):
        super(SpectralStrapping, self).__init__(attacker, defenders)
        self.description = 'Conjures a \'hand\' and \'strap\' made of raw magic. The hand grabs the target and lifts them into the air. The strap lands a number of swats on the target\'s backside. Once the spanking is done, the hand lifts the target up, and throws them into the ground. For each round that the strapping continues, the caster uses 2 mana.'
        self.effectFormula = 'SPANKING DURATION: talent + bonus(1.2 * talent - enemy.talent)\nHUMILIATION DURATION: 1.4 * resilience - enemy.resilience\nDAMAGE: 1.2 * talent'
        self.numTargets = 1
        self.magicMultiplier = 1.2
        self.resilienceMultiplier = 1.4
        self.targetType = combatAction.ENEMY
        self.effectClass = combatAction.ALL
        self.statusInflicted = statusEffects.HUMILIATED
        self.rawMagic = True
        self.expertise = ADVANCED
        self.probModifier = 19
        self.minProbability = 37
        self.maxProbability = 96
        self.minDamage = 2
        
    def effect(self, inCombat=True, allies=None, enemies=None):
        return super(SpectralStrapping, self).effect(inCombat, allies, enemies)

    def effect_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        self.effectStatements = [[A, 'flings', p.hisher(attacker), 'hand out at', D + ".", 'A faintly glowing rope flies from', p.hisher(attacker), 'palm and wraps itself',
            'around', D + ".", A, 'snaps', p.hisher(attacker), 'arm back, spinning', D, 'around so that', D, 'is facing away from', A + "."]] 
        return super(SpectralStrapping, self).effect_statement(defender)    
    
    def success_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        return [A, 'snaps the cord taught, smirking as', p.heshe(attacker), 'watches', D, 'squirm.', p.HeShe(attacker), 'draws', p.hisher(attacker), 'free hand back.', 
                'A long, spectral strap forms in', p.hisher(attacker), 'hand.', A, 'swings', 
                p.hisher(attacker), 'arm through the air and snaps the strap against', D + "'s", 
                defender.bum_adj(), 'bottom.', D, 
                'stiffens and squeaks as a sharp sting spreads across', p.hisher(defender), 
                defender.quivering(), 'bottom.'] 

    def round_statement(self, defender):     
        attacker = self.attacker
        resultStatement = ' '.join(["The spectral strap snaps repeatedly against", defender.printedName + "'s", defender.quivering() + ",", "rapidly reddening bottom.", defender.HeShe(), 
            "kicks and flails,", defender.hisher(), "face an even brighter red than", defender.hisher(), defender.muscle_adj(), "bottom."])
        if attacker.current_mana():
            attacker.decrease_stat(universal.CURRENT_MANA, 2)
            return resultStatement
        else:
            return '\n\n'.join([resultStatement, self.end_statement(defender)])

        
class SpectralCaning(p.SpectralSpanking):
    targetType = ENEMY
    grappleStatus = GRAPPLER_ONLY
    effectClass = ALL
    numTargets = 1
    tier = p.SpectralSpanking.tier
    statusInflicted = statusEffects.HUMILIATED
    effectClass = combatAction.ALL
    cost = 32
    severity = spanking.CANE_SEVERITY
    name = 'Spectral Caning'
    def __init__(self, attacker, defenders):
        super(SpectralCaning, self).__init__(attacker, defenders)
        self.description = 'Conjures a \'hand\' and \'cane\' made of raw magic. The hand grabs the target and lifts them into the air. The cane lands a number of swats on the target\'s backside. Once the caning is done, the hand lifts the target up, and throws them into the ground. However, for every round that the spanking continues, the caster uses 3 mana.'
        self.effectFormula = 'SPANKING DURATION: talent + bonus(1.4 * talent - enemy.talent)\nHUMILIATION DURATION: 1.6 * resilience - enemy.resilience\nDAMAGE: 1.2 * talent'
        self.numTargets = 1
        self.magicMultiplier = 1.4
        self.smackMultiplier = 5
        self.expertise = EXPERT
        self.resilienceMultiplier = 1.6
        self.targetType = combatAction.ENEMY
        self.effectClass = combatAction.ALL
        self.statusInflicted = statusEffects.HUMILIATED
        self.rawMagic = True
        self.probModifier = 20
        self.minProbability = 40
        self.maxProbability = 97
        self.minDamage = 2


    def effect(self, inCombat=True, allies=None, enemies=None):
        return super(SpectralCaning, self).effect(inCombat, allies, enemies)

    def success_statement(self, defender):
        attacker = self.attacker
        A = attacker.printedName
        D = defender.printedName
        return [A, 'snaps the cord taught, smirking as', p.heshe(attacker), 'watches', D, 'squirm.', 
                p.HeShe(attacker), 'draws', p.hisher(attacker), 'free hand back.', 
                'A long, thin, whippy cane forms in', p.hisher(attacker), 'hand.', A, 'whips', 
                p.hisher(attacker), 'arm through the air and cuts the cane against', D + "'s", 
                defender.bum_adj(), 'bottom.', D, 
                'squeals as a deep line of fire spreads across', p.hisher(defender), 
                defender.quivering(), 'bottom.'] 

    def round_statement(self, defender):
        attacker = self.attacker
        resultStatement = ' '.join([attacker.printedName, 'flicks', attacker.hisher(), 'wrist. In response, the cane whizzes through the air and snaps against', 
            defender.printedName + "'s", 
            defender.bum_adj(), "bottom.", defender.printedName, "shrieks as a long, thin welt forms across", defender.hisher(), defender.muscle_adj(), "cheeks."])
        if attacker.current_mana():
            attacker.decrease_stat(universal.CURRENT_MANA, 3)
            return resultStatement
        else:
            return '\n\n'.join([resultStatement, self.end_statement(defender)])

        
spectralSpanking = p.SpectralSpanking(None, None) 
spectralStrapping = SpectralStrapping(None, None) 
spectralCaning = SpectralCaning(None, None)
p.allSpells[p.SpectralSpanking.tier].append((spectralSpanking, spectralStrapping, spectralCaning))
universal.set_spells(p.allSpells)
