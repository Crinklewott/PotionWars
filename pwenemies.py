""" Copyright 2014-2015 Andrew Russell

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
import person
import itemspotionwars
import copy
import spells_PotionWars
import positions
import items
import spanking


def name():
    return universal.state.player.name

class Enemy(person.Person):
    def __init__(self, name, gender, defaultLitany, description="", printedName=None, coins=20, specialization=universal.BALANCED, dropChance=3, musculature='', 
            bodyType='', height='', hairLength='', hairStyle='', eyeColor='', skinColor='', order=person.zeroth_order, identifier=None):
        """
        Drop chance determines the chances that this character will drop a piece of equipment.
        """
        super(Enemy, self).__init__(name, gender, defaultLitany, defaultLitany, description, printedName, coins, specialization, order, musculature=musculature,
                bodyType=bodyType, height=height, hairLength=hairLength, hairStyle=hairStyle, eyeColor=eyeColor, skinColor=skinColor, identifier=identifier)
        self.dropChance = dropChance
        self.printedName = self.printedName + (' (M)' if self.is_male() else ' (F)')
        self.equip(items.emptyWeapon)
        self.equip(items.emptyLowerArmor)
        self.equip(items.emptyUpperArmor)
        self.equip(items.emptyUnderwear)
        self.positions = [positions.overTheKnee, positions.standing, positions.onTheGround]
        self.spankingFunctions = {
                positions.overTheKnee: (self.otk_intro, self.otk_round, self.otk_failure, self.otk_reversal),
                positions.standing: (self.standing_intro, self.standing_round, self.standing_failure, self.standing_reversal),
                positions.onTheGround: (self.on_the_ground_intro, self.on_the_ground_round, self.on_the_ground_failure, self.on_the_ground_reversal)
            }

        self.firstRound = True

    def spanks(self, bottom, position):
        return self.spankingFunctions[position][0](self, bottom)

    def spanked_by(self, top, position):
        return self.spankingFunctions[position][0](top, self)

    def reverses(self, top, position):
        return self.spankingFunctions[position][-1](top, self)

    def reversed_by(self, bottom, position):
        return self.spankingFunctions[position][-1](self, bottom)

    def failed(self, bottom, position):
        return self.spankingFunctions[position][-2](self, bottom)

    def blocks(self, top, position):
        return self.spankingFunctions[position][-2](top, self)


    def otk_intro(self, top, bottom):
        raise NotImplementedError()

    def otk_round(self, top, bottom):
        raise NotImplementedError()

    def otk_failure(self, top, bottom):
        raise NotImplementedError()

    def otk_reversal(self, top, bottom):
        raise NotImplementedError()

    def standing_intro(self, top, bottom):
        raise NotImplementedError()

    def standing_round(self, top, bottom):
        raise NotImplementedError()

    def standing_failure(self, top, bottom):
        raise NotImplementedError()

    def standing_reversal(self, top, bottom):
        raise NotImplementedError()

    def on_the_ground_intro(self, top, bottom):
        raise NotImplementedError()

    def on_the_ground_round(self, top, bottom):
        raise NotImplementedError()

    def on_the_ground_failure(self, top, bottom):
        raise NotImplementedError()

    def on_the_ground_reversal(self, top, bottom):
        raise NotImplementedError()

    def end_spanking(self, top, bottom):
        self.firstRound = True
        return universal.format_line(['''Finally, with a mighty effort,''', bottom.printedName, '''manages to wriggle''', bottom.himselfherself(), '''free of''', top.printedName + "'s", 
        '''merciless grasp.''', bottom.HeShe(), '''scrambles away from''', top.printedName, '''clutching at''', bottom.hisher(), '''burning bottom with one hand, while snatching up''', 
        bottom.hisher(), '''dropped weapon with the other.'''])

    def drop(self):
        "TODO: Implement"
        raise NotImplementedError()

    def level_up(self, level):
        """
        Used for scaling. Level up to the specified level.
        TODO: Implement
        """
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement level_up for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))

    def post_combat_spanking(self): 
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement post_combat_spanking for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))

    def __eq__(self, other):    
        """
        For enemies, reduce equality to seeing if they point to the same object. This is necessary because two different generic enemies may not have the same name.
        """
        return self is other

#--------------------------Introduced in Episode 1----------------------------------------------------
class VengadorWarrior(Enemy):
    #def __init__(self, name, gender, defaultLitany, description="", printedName=None, 
            #coins=20, specialization=BALANCED)
    def __init__(self, gender, level=0, identifier=None):
        super(VengadorWarrior, self).__init__('Vengador Warrior', gender, None, specialization=universal.DEXTERITY, bodyType='voluptuous', musculature='muscular', 
                height='tall', identifier=identifier)
        self.level = level
        #self.equip(copy.copy(itemspotionwars.leatherCuirass))
        self.equip(copy.copy(itemspotionwars.tunic))
        self.equip(copy.copy(itemspotionwars.trousers))
        self.equip(copy.copy(itemspotionwars.warspear))
        self.description = universal.format_line(['''A tall, broad-shouldered''', person.manwoman(self) + ".", person.HeShe(self), '''is wielding a''', self.weapon().name, 
        '''and is wearing''', self.shirt().name, '''and''', self.lower_clothing().name + "."])
        self.set_all_stats(strength=1, dexterity=2, willpower=0, talent=0, health=12, mana=0, alertness=1)

    def otk_intro(self, top, bottom):
        if self is top:
            spankingText = universal.format_text([['''The Vengador Warrior rushes''', bottom.printedName, '''in a burst of speed that belies''', top.hisher(), '''size, and jabs''', bottom.printedName, 
                '''in the stomach with''', top.hisher(), '''spear. As''', bottom.printedName, '''hunches forward, the warrior crouches and yanks''', bottom.printedName, 
                '''across''', 
                top.hisher(), '''lap, while wrapping one of''', top.hisher(), '''arms around''', bottom.printedName + "'s", '''midsection.'''],
                ['''Straddling the crouching warrior's lap,''', bottom.printedName, '''is helpless as the Vengador Warrior administers a thorough, if short, spanking to''', bottom.hisher(), 
                '''plump, unblocked bottom. The whole thing happens so quickly, that''', top.printedName, '''is able to cover the Taironan's entire ass in peppering swats before''', bottom.heshe(),
                '''can even begin to fight back.''']])
        else: 
            spankingText = universal.format_text([[top.printedName, '''rushes the Vengador Warrior in a burst of speed, and jabs the warrior in the stomach with the butt of''', 
                top.hisher(),
                top.weapon().name + ".", '''As the Vengador Warrior involuntarily bends forward,''', top.name, '''goes into a crouch, and throws the Vengador Warrior across''', person.hisher(), 
                '''lap. Then,''', top.heshe(), '''wraps one of''', top.hisher(), '''arms around the fighter's midsection.'''],
                ['''Straddling''', top.printedName + "'s", '''lap, the warrior finds''', bottom.himselfherself(), '''completely helpless as''', top.printedName, '''administers a thorough, if short,''',
                    '''spanking to''', bottom.hisher(), '''shapely, unblocked bottom.''', '''The whole thing happens so quickly, that''', top.printedName, 
                    '''is able to cover the Taironan's''', bottom.bum_adj(), '''ass in peppering swats before''', bottom.heshe(), '''can even begin to fight back.''']])
        return spankingText

    def standing_intro(self, top, bottom):
        if self is top:
            spankingText = universal.format_text([['''The dark-skinned warrior surprises''', bottom.printedName, '''by striking low with the butt of''', top.hisher(), '''spear, rather than at the''',
            '''torso with the tip.''',
                '''The solid wood crashes into''', bottom.printedName + "'s", '''legs and knocks''', bottom.hisher(), '''feet out from under''', bottom.himher() + ".", 
                bottom.printedName, '''lands hard on''', bottom.hisher(), '''knees. The Vengador Warrior wastes no time in leaping forward, roughly grabbing''', bottom.printedName + "'s", 
                '''shoulders and thrusting''', bottom.hisher(), '''head between the warrior's calves.''', bottom.printedName, '''extends''', bottom.hisher(), '''legs in an attempt to''',
                '''stand up, but with''', bottom.hisher(), '''head hopelessly locked in a tight grip,''', bottom.heshe(), '''only makes''', bottom.hisher(), '''own''', bottom.bum_adj(), 
                '''bottom a tempting target for the Vengador Warrior.'''],
                ['''Pleased with''', top.himselfherself() + ",", '''the Vengador Warrior clutches''', bottom.printedName + "'s", bottom.lower_clothing().name, '''tightly with one hand and begins to''',
                '''whale on''', bottom.hisher(), bottom.muscle_adj(), '''wriggling butt with the other.''']])
        else:
            spankingText = universal.format_text([[top.printedName, '''distracts the dark-skinned warrior with a flurry of swings and thrusts that draw the Vengador Warrior's attention above''', 
                top.printedName + "'s", '''head.''', top.printedName, '''then sweeps the warrior's feet out from underneath''', bottom.himher() + ".", '''The Vengador Warrior lands hard on''', 
                bottom.hisher(), '''knees.''', top.printedName, '''then roughly grabs the warrior's shoulders and thrusts the warrior's head between''', top.hisher(), '''calves. The warrior''',
                '''extends''', bottom.hisher(), '''legs in an attempt to stand up, but with''', bottom.hisher(), '''head hopelessly locked in a tight grip,''', bottom.heshe(), '''only makes''',
                 bottom.hisher(), '''own tight bottom a tempting target for''', top.printedName + "."],
                 ['''Pleased with the success of''', top.hisher(), '''fanciful moves,''', top.printedName, '''clutches''', bottom.printedName + "'s", '''trousers tightly with one hand, and begins''',
                 '''to whale on''', bottom.hisher(), '''round butt with the other.''']])
        return spankingText

    def on_the_ground_intro(self, top, bottom):
        if self is top:
            spankingText = universal.format_text([['''Suddenly, the Vengador Warrior unleashes a desperate attack at''', bottom.printedName + "'s", '''head.''', bottom.printedName, 
            '''dodges the spear thrust. The warrior snaps the spear down, and sweeps''', bottom.printedName + "'s", '''legs out from underneath''', bottom.himher() + ",", '''and''', bottom.printedName,
            '''lands hard on''', bottom.hisher(), '''face. Before''', bottom.printedName, '''can get back up, the Vengador Warrior sits down on the middle of''', bottom.printedName + "'s", 
            '''back and begins drumming''', bottom.printedName + "'s", '''bottom with both hands. Facedown, and with''', bottom.hisher(), '''arms pinned uselessly between the Warrior's legs, and''',
            bottom.hisher(), '''own torso,''', bottom.printedName, '''can do nothing but wait for a chance to escape, while''', bottom.heshe(), '''drums''', bottom.hisher(), '''toes onto the floor''',
            '''in pain and humiliation.''']])
        else: 
            spankingText = universal.format_text([['''Suddenly,''', top.printedName, '''lunges forward in a seemingly desperate attack aimed at''', bottom.printedName + "'s", '''head. The warrior''',
                '''dodges the''', top.weapon().weaponType, '''strike, only to discover the attack was feint, when''', top.printedName, '''suddenly shifts''', top.hisher(), '''weight, and knocks''', 
                bottom.hisher(), '''legs knocked out from under''', bottom.himher() + ".", '''As the Vengador Warrior hits the ground facefirst,''', top.printedName, '''sits down on the middle of''',
                '''the''',
                 '''warrior's back and begins to drum''', bottom.hisher(), '''bottom with both hands. Facedown, and with''', bottom.hisher(), '''arms pinned uselessly between''', top.printedName + 
                 "'s", '''legs and''', bottom.hisher(), '''own sides, the Vengador can do nothing but wait for a chance to escape, and drum''', bottom.hisher(), 
                 '''toes against the floor in pain.''']]) 
        return spankingText

    def otk_continuing(self, top, bottom):
        if self is top:
            return universal.format_text([[bottom.printedName, '''struggles against the broad-shouldered warrior, but with''', bottom.hisher(), '''arm around the''', bottom.heroheroine() + "'s",
            '''waist, the''',
                '''Vengador has all the leverage. That doesn't stop''', bottom.PrintedName, '''from thrusting''', bottom.hisher(), '''legs upward between stinging full-armed swats, but the warrior''',
                '''sees what the heroine is up to and, with a "Tsk, tsk, none of that!" directs''', top.hisher(), '''attention to''', bottom.printedName + "'s.", bottom.printedName, '''howls''', 
                bottom.hisher(), '''displeasure and drums''', bottom.hisher(), '''fists against the stone floor as the warrior's solid hand batters''', bottom.hisher(), '''thighs and sit spots.''']])
        else: 
            return universal.format_text([['''The broad-shouldered warrior struggles against''', top.printedName + "'s", '''grip, but with''', bottom.hisher(), '''arm around the warrior's''',
                '''waist, the''', top.heroheroine(), '''has all the leverage. That doesn't stop the Vengador Warrior from trying to put''', bottom.hisher(), '''strength to use by thrusting''', 
                bottom.hisher(),
                '''legs upward between stinging full-armed swats, but''', top.printedName, '''sees what the fighter is up to and, with an admonishing click of''', top.hisher(), '''tongue, directs''',
                top.hisher(), '''attention to the warrior's thighs. The''', bottom.manwoman(), '''howls''', bottom.hisher(), '''displeasure and drums''', bottom.hisher(), '''fists against the stone''',
                '''floor as''', top.printedName + "'s", '''solid hand batters''', bottom.hisher(), '''thighs and sit spots.''']])

    def standing_continuing(self, top, bottom):
        if self is top:
            return universal.format_text([[bottom.printedName, '''continues''', bottom.hisher(), '''struggle to escape from the Vengador Warrior's grip, but''', bottom.hisher(), '''head is securely''',
                '''stuck between the Vengador Warrior's muscled thighs. A wave of embarrassment rolls over''', bottom.himher(), '''as''', bottom.heshe(), '''feels the warrior's hard spanks heat up''',
                bottom.hisher(), '''up-thrust, weaving,''', bottom.bum_adj(), '''bottom.''']])
        else:
            return universal.format_text([['''The Vengador Warrior continues''', bottom.hisher(), '''struggle to escape''', top.printedName + "'s", '''grip, but''', bottom.hisher(), '''head is''',
                '''securely stuck between the''', top.heroheroine() + "'s", top.muscle_adj(), '''thighs. If anything,''', bottom.hisher(), '''struggles only spur''', top.printedName, 
                '''on to harder''',
                '''and harder smacks, making''', bottom.hisher(), bottom.muscle_adj(), '''bottom bounce.''']])

    def on_the_ground_continuing(self, top, bottom):
        if self is top:
            return universal.format_text([['''The Vengador Warrior has brightened''', bottom.printedName + "'s", '''ass beneath''', bottom.lower_clothing().name, ' '.join(['''and''', 
                bottom.underwear().name + ","])  if bottom.wearing_underwear() else ',', '''and none of''', bottom.printedName + "'s", '''squirming seems ready to change the situation. The Vengador''',
                '''concentrates on''', bottom.printedName + "'s", '''thighs and sit spots, eliciting both wails and pleas from''', top.hisher(), '''victim.''']])
        else:
            return universal.format_text([[top.printedName, '''continues to mercilessly batter the Vengador Warrior's''', bottom.bum_adj(), '''bottom, and none of the warrior's squirming seems''',
                '''poised to change the situation.''', top.printedName, '''concentrates on the Vengador's thighs and sit spots, eliciting both wails and pleas from''', top.hisher(), '''victim.''']])

    def otk_reversal(self, top, bottom):
        return universal.format_text([[self.otk_intro(top, bottom)], ['''However, while''', top.printedName, '''continues to redden''', bottom.printedName + "'s" '''behind,''', bottom.printedName, 
            '''musters all''', bottom.hisher(), '''lower-body strength into a grab-and-twist with''', bottom.printedName + "'s", '''thighs and hips, twisting both the Taironans around and''',
            '''onto the floor. The surprised''', '''warrior''' if self is top else top.heroheroine(), '''is slow to respond, and is still lying on''', top.hisher(), 
            '''stomach when a now-crouching''', bottom.printedName, '''grabs the waistband''',
            '''of''', top.hisher(), '''trousers and yanks the helpless warrior onto''', bottom.hisher(), '''lap.''', bottom.printedName, '''begins pelting the warrior's squirming bottom with''',
            '''a vengeance.''', top.printedName, '''has no hope of freeing''', top.himselfherself(), '''and finds''', top.himselfherself(), '''primarily preoccupied with trying to keep''', 
            top.hisher(), top.lower_clothing().name, top.lower_clothing().updown() + "."]])

    def standing_reversal(self, top, bottom):
        return universal.format_text([[self.standing_intro(top, bottom)], ['''Then,''', bottom.heroheroine() + "'s", '''strong hands grip''', top.printedName, '''firmly around the ankles.''',
            bottom.printedName, '''pulls''', bottom.hisher(), '''hands forward, forcing''', top.printedName, '''to topple backward, and land on''', top.hisher(), '''behind.''', bottom.printedName,
            '''pulls''', bottom.himselfherself(), '''to''', bottom.hisher(), '''full height and wastes no time in grasping''', top.printedName, '''and shoving''', top.hisher(), '''head between''',
            bottom.hisher(), '''legs.''', bottom.printedName, ' '.join(['''spies the waistband of''', top.printedName + "'s", top.underwear().name, ' '.join(['''peeking out from above''', 
                top.hisher(), 
                top.hisher(), top.lower_clothing().name]) if top.wearing_lower_clothing() else '', '''and clutches it tightly.''']) if top.wearing_underwear() else 
            ' '.join(['''grabs the back of''', top.printedName + "'s", top.lower_clothing.name + "."]),
                    ['''Then,''', bottom.printedName, '''lifts''', top.printedName + "'s", '''bottom up by to hip level.''', top.printedName, '''curses and kicks, but that doesn't stop''',
                        bottom.printedNamep, '''from putting''', top.printedName, '''in the same vulnerable position in which''', top.heshe(), '''had tried to place''', bottom.printedName + ".",
                        '''With''', top.hisher(), '''head locked tightly between''', bottom.printedName + "'s", '''calves, the warrior can do little more than wriggle''', top.hisher(), 
                        '''bottom as''', bottom.printedName, '''assaults it with stinging spanks, turning it the same color as the humiliated''', top.printedName + "'s", '''face.''']]])
        
    def on_the_ground_reversal(self, top, bottom):
        return format_text([[self.on_the_ground_intro(top, bottom)], [top.printedName, '''But then,''', bottom.printedName, '''flips''', bottom.hisher(), '''hips over, and slings one of''', 
            top.printedName + "'s", '''legs away from''', top.hisher(), '''body. The other combatant lands on all fours but isn't there for long, because''', bottom.printedName, '''quickly sits on''',
            top.hisher(), '''back with enough force to slam''', top.himher(), '''to the floor.''', bottom.printedName, '''begins''', bottom.hisher(), '''spanking revenge by focusing all of''', 
            bottom.hisher(), '''swats on one cheek, leaving''', top.printedName, '''writhing under the relentless punishment.''']])

    def default_stats(self):
        self.set_all_stats(strength=1, dexterity=3, willpower=0, talent=0, health=15, mana=0, alertness=1)

    def otk_failure(self, top, bottom):
        return universal.format_text([[top.printedName, '''rushes''', bottom.printedName, '''in a burst of speed, swinging the butt of''', top.hisher(), '''weapon at''', bottom.printedName + "'s",
            '''face.''', bottom.printedName, '''deflects the weapon with''', bottom.hisher(), '''own weapon and swats''', top.printedName + "'s", '''thigh as they dance apart.''']])

    def standing_failure(self, top, bottom):
        return universal.format_text([[top.printedName, '''spins''', top.hisher(), top.weapon().name, '''in an effort to distract''', bottom.printedName, '''from''', top.hisher(), '''true target:''',
            bottom.printedName + "'s", '''shins. However,''', bottom.printedName, '''sees''', top.printedName + "'s", '''feet heading toward''', bottom.hisher(), '''legs. The warrior knocks them''',
            ''''aside with''', ' '.join(['''the shaft of''', bottom.hisher(), '''spear and quickly brings it back around to crack against''', top.printedName + "'s", top.bum_adj(), '''behind.''']) if
            top.weapon().weaponType == items.Spear.weaponType else ' '.join(['''the blade of''', bottom.hisher(), '''weapon. Then''', bottom.heshe(), '''snaps''', bottom.hisher(), 
                bottom.weapon().name,  
            '''back around, and cracks the flat of the blade against,''', top.printedName + "'s", top.bum_adj(), '''bottom.''']),
                top.printedName, '''jumps and yelps, while one of''', top.hisher(), '''hands involuntarily flies back to''', top.muscle_adj(), '''round bottom in an attempt to rub away the sting.''']])

    def on_the_ground_failure(self, top, bottom):
        return universal.format_text([[top.printedName, '''puts all''', top.hisher(), '''strength into a desperate strike, or so it seems.''', bottom.printedName, '''reads the true intention of''',
            top.hisher(), '''attack, and when the warrior's leg sweep comes, kicks''', bottom.hisher(), '''foot out of the way with such force that''', top.printedName, 
            '''wobbles, dangerously close''',
            '''to toppling.''', bottom.printedName, '''takes advantage of the brief window of vulnerability to land a solid swat to the embarrassed fighter's backside before readying''', 
            bottom.himselfherself(),''' for''', bottom.hisher(), '''next move.''']])

    def post_combat_spanking(self):
        bottomAdj = "large, smooth, round" if self.is_female() else "large, rather hairy"
        warriorText = format_text([['''The warrior staggers, and falls to one knee,''', person.hisher(self), '''weapon slipping from''', person.hisher(self), '''fingers.'''],
        [universal.state.player.name, '''approaches''', person.himher(self) + ',', '''kicking''', person.hisher(self), '''weapon out of reach.'''],
        ['''"Why are the insurgents attacking the guild? Who is leading the attack?" asks''', universal.state.player.name + "."],
        ['''The warrior spits at''', universal.state.player.name + "'s", '''face. Well, tries to. It's less spit, and more drool. Losing all your health will do that to you.'''],
        ['''"Right then."''', universal.state.player.name, '''goes down on one knee, grabs the warrior's shoulders, and hauls''', person.himher(self), '''over''', person.hisher(), 
            '''thigh.'''],
        ['''The warrior laughs. "You don't really think a spanking is going to make me reveal anything, do you?"'''],
        ['''"Well, worst case is you get a much needed punishment," says''', universal.state.player.name + ".", person.HeShe(), '''hooks''', person.hisher(), '''fingers in''', 
            '''the warrior's trousers, and slides them down to''', person.hisher(self), '''ankles, baring a''', bottomAdj, '''bottom. The warrior bears''', 
            person.hisher(self), '''undressing stoically.''', name(), '''flexes''', person.hisher(), '''fingers, and gets ready to break said stoicism.'''],
        [name(), '''begins smacking the young''', person.manwoman(self) + "'s", '''bottom, setting a fast and furious pace.''', person.HisHer(self), '''bottom quickly''',
            '''reddens, and''', person.heshe(self), '''begins to squirm a little. Still, the warrior remains stubbornly silent.''', '''So,''', name(), '''shifts''', 
            person.hisher(), '''attention to the warrior's sitspots, and the sensitive crease where bottom meets thigh.'''],
            ['''A few grunts slip past the warrior's lips, and''', person.hisher(self), '''fingers start to curl.'''],
        ['''"Had enough?" asks''', name() + ",", '''massaging''', person.hisher(), '''palm. The warrior's bottom is hard and muscled, and spanking it hurts''', name() + "'s",
            '''hand far more than it has any right to!'''],
        [person.HeShe(self), '''laughs. "Please. Ana's reminder taps hurt more than this."'''],
        ['''For a second,''', name(), '''hesitates, and studies the red, angry looking bottom.''']])
        if universal.state.player.resilience() > self.resilience():
            warriorText = format_text([warriorText, [name(), '''steels''', person.himselfherself() + ".", person.HeShe(), '''slips off''', person.hisher(), '''pack, and pulls''',
                '''out''', person.hisher(), '''wooden spoon.'''],
            ['''"Right then."''', name(), '''taps the spoon against the''', person.manwoman(self) + "'s", '''bottom. "Let's see if I can change that attitude."'''],
            [name(), '''raises the spoon above''', person.hisher(), '''head, and whips it down against the warrior's bottom.'''],
            ['''The warrior gives a strangled cry, and''', person.hisher(self), '''body jerks against''', name() + "'s", '''thigh.'''],
            [name(), '''works the spoon vigorously, spreading a stinging burn across the Vengador's bottom. At first, the Vengador bears the spoon with''',
                '''the same stoicism as''', name() + "'s", '''hand. Then,''', name(), '''lands a particularly stinging smack to''', person.hisher(self), '''sitspot, and''',
                '''the dam breaks.''', person.HeShe(self), '''starts kicking and flailing,''', person.hisher(self), '''red bottom wiggling around on''', name() + "'s", 
                '''thigh.'''],
            ['''"Ok, ok," cries the insurgent. "Stop, stop, please I've had enough!"'''],
            ['''"Why are you attacking the guild?" asks''', name() + "."],
            ['''"Everyone knows Adrian has a stockpile of weapons he uses to outfit his adventurers," says the insurgent. "Only the military and guard armories have more,''',
                '''but those are much more heavily guarded."'''],
            ['''"Who is that woman out there leading the attack?" asks''', name() + "."],
            ['''"I don't know," says the''', person.manwoman(self) + "."],
            [name(), '''gives''', person.himher(self), '''a hard smack with the spoon.'''],
            ['''"It's true, it's true!" wails the insurgent, kicking''', person.hisher(self), '''legs. "I only joined a few months ago. I was trained by Ana."'''],
            ['''"Whose Ana?" asks''', name() + "."],
            ['''"A Taironan woman. I think she's from Bonda," says the warrior. "She was in charge of recruiting and training us."'''],
            ['''"Well, she didn't do a very good job," mutters''', name() + "."],
            ['''"Not like she had a lot of time," snaps the warrior. "Besides there were a lot of us."'''],
            [name(), '''frowns, and pushes the warrior off''', person.hisher(), '''thigh.'''],
            ['''It would appear that''', name() + "'s", '''arrived in Avaricum just in time for things to get interesting. Joy.''']])
            universal.state.player.add_keyword('learned_Vengadores_are_escalating')
        else:
            warriorText = format_text([warriorText, [name(), '''rubs''', person.hisher(), '''hand, and considers the warrior's blazing bottom, and''',
            person.hisher(), '''stoicism. Then,''', name(), '''decides that''', person.heshe(), '''doesn't have anymore time to waste, and shoves the warrior off''',
            person.hisher(), '''knee.'''],
            ['''"You're not worth it," says''', name() + ",", '''standing and brushing off''', person.hisher(), '''hands.'''],
            [name(), '''notices the warrior smirk as''', person.heshe(self), '''pulls up''', person.hisher(self), '''trousers.''', name(), '''turns away from''', 
            person.himher(self) + ".", '''Smirk or not,''', person.heshe(self), '''was still too weak to attack''', name(), '''again.''']])
        return warriorText


class VengadorSpellslinger(Enemy): 

    def __init__(self, gender, level=0, identifier=None):
        super(VengadorSpellslinger, self).__init__('Vengador', gender, None, specialization=universal.COMBAT_MAGIC, bodyType='voluptuous', height='short', musculature='soft', identifier=identifier)
        self.level = level
        self.set_all_stats(strength=0, dexterity=1, willpower=2, talent=2, health=6, mana=10, alertness=0)
        if gender == person.FEMALE:
            self.equip(copy.copy(itemspotionwars.wornDress))
        else:
            self.equip(copy.copy(itemspotionwars.wornRobe))
        self.equip(copy.copy(itemspotionwars.staff))
        self.description = universal.format_line(['''A short Taironan''', person.manwoman(self), '''dressed in a''', 
            self.lower_clothing().name + ".", person.HeShe(self), '''carries a''', self.weapon().name + "."])
        self.learn_spell(spells_PotionWars.firebolt)
        self.learn_spell(spells_PotionWars.icebolt)
        self.learn_spell(spells_PotionWars.magicbolt)
        self.positions = [positions.overTheKnee, positions.standing, positions.onTheGround]

    def default_stats(self):
        self.set_all_stats(strength=0, dexterity=1, willpower=2, talent=4, health=8, mana=10, alertness=0)

    def otk_intro(self, top, bottom):
        return  universal.format_text([[top.printedName, '''dodges''', bottom.printedName + "'s", '''attack and grabs''', bottom.himher(), '''by the shoulders.''', top.HeShe(), 
            '''lunges forward''',
            '''and bends''', bottom.printedName, '''over''', top.hisher(), '''outthrust knee. The whole thing happens so quickly that''', bottom.printedName + "'s", '''bottom is being fiercely''',
            '''swatted''',
            '''before''', bottom.heshe(), '''even understands what's happening.''']])

    def otk_round(self, top, bottom):
        return universal.format_text([[top.printedName, '''manages to keep''', top.hisher(), '''position, but several of''', top.hisher(), '''blows are deflected by''', bottom.printedName + "'s",
            '''flailing hand. But then,''', top.printedName, '''catches and secures the hand and pins it to the small of the''', bottom.heroheroine() + "'s", '''back. Now with even more control,''', 
            top.printedName, '''makes''', bottom.printedName, '''pay for''', bottom.hisher(), '''struggles by delivering a series of swats to the lower curve of''', bottom.hisher(), 
            '''plump globes, prompting ineffectual kicking and threats of vengeance.''']])

    def otk_failure(self, top, bottom):
        if self is top:
            return universal.format_text([[self.otk_intro(top, bottom)], ['''But''', bottom.printedName, '''quickly becomes fed up with the embarrassment of being hauled over the Vengador's knee''',
                '''like a naughty''', bottom.boygirl(), '''and throws''', bottom.himselfherself(), '''up, then down.''', top.HisHer(), 
                '''attention absorbed by the discipline''', top.heshe(), '''has started to mete out,''',
                '''the spellslinger is caught off guard and fails to brace''', top.himselfherself(), '''before the''', bottom.heroheroine(), '''crashes down on top of''', top.himher() + ".", 
                '''By the time''', top.printedName, '''recovers from the shock,''', top.hisher(), '''opponent is back on''', bottom.hisher(), '''feet and gripping''', bottom.hisher(), 
                bottom.weapon().weaponType, '''with one hand. The pose would, perhaps, be more intimidating if''', bottom.printedName + "'s", '''other hand weren't massaging''',
                '''a smarting bottom.''']])
        else:
            return universal.format_text([[self.otk_intro(top, bottom)], ['''Suddenly''', bottom.printedName, '''throws''', bottom.himselfherself(), '''up, then down.''', top.HisHer(), 
                '''attention absorbed by the discipline''', top.heshe(), '''has started to mete out,''',
                top.printedName, '''is caught off guard and fails to brace''', top.himselfherself(), '''before the spellslinger crashes back down on top of''', top.himher() + ".", 
                '''By the time''', top.printedName, '''recovers from the shock,''', top.hisher(), '''opponent is back on''', bottom.hisher(), '''feet and gripping''', bottom.hisher(), 
                bottom.weapon().weaponType, '''with one hand. The pose would, perhaps, be more intimidating if''', bottom.printedName + "'s", '''other hand weren't massaging''',
                '''a smarting bottom.''']])

    def otk_reversal(self, top, bottom):
        if self is top:
            return universal.format_text([[self.otk_intro(top, bottom)],['''Despite''', bottom.HisHer(), '''bottom already starting to burn,''', bottom.printedName, '''decides to relax''', 
                bottom.hisher(), '''body and wait until the Vengador lets''', top.hisher(), '''guard down. A few punishing swats later,''', bottom.printedName, '''twists''', bottom.hisher(), 
                '''body with all''', bottom.hisher(), '''might, rolling''', top.printedName, '''to the side and off balance. Foisting the struggling slinger across''', bottom.hisher(), 
                '''own knee,''', bottom.printedName, '''begins spanking''', top.printedName + "'s", '''wriggling bottom, returning''', top.printedName, '''favor.''']])
        else:
            return universal.format_text([[self.otk_intro(top, bottom)], [bottom.printedName, '''relaxes, submitting''', bottom.himselfherself(), '''to the punishment.''', '''Upon seeing the''',
                '''spanked''', bottom.manwoman(), '''relax''', bottom.hisher(), '''body,''', top.printedName, '''lets''', top.hisher(), '''guard down, that''',  top.heshe() + "'s", '''actually''',
                '''teaching the invader a stern lesson. But then, the Vengador twists''', bottom.hisher(), '''body with all''', bottom.hisher(), '''might, knocking''', top.printedName, '''on''',
                top.hisher(), '''side.''', bottom.printedName, '''hits the ground, and rolls into a lunge position. Then,''', bottom.heshe(), '''grabs''', top.printedName, '''and foists the''',
                '''struggling''', top.heroheroine(), '''across''', bottom.hisher(), '''own knee. Then, the slinger begins returning the spanks to''', top.printedName + "'s", '''wriggling bottom.''']])

    def standing_intro(self, top, bottom):
        return universal.format_text([[bottom.printedName + "'s", '''opponent fakes an attack with''', top.hisher(), '''staff, then quickly grabs''', top.printedName + "'s", '''shoulders,''',
            '''and forces''', bottom.himher(), '''onto''', bottom.hisher(), '''hands and knees.''', top.printedName, '''straddles''', bottom.printedName + "'s", '''waist, and tightens''', 
            top.hisher(), '''legs around''', bottom.printedName() + "'s", '''torso. Then,''', top.heshe(), '''bends over and begins swatting''', bottom.printedName + "'s", '''behind.''',
            bottom.printedName, '''swipes''', bottom.hisher(), '''hands to either side, but is unable to grab anything''', ' '.join(['''but the slinger's''', top.clothing_below_the_waist().name,])
            if self is top else '''of use''', '''as''', bottom.hisher(), '''ass is set ablaze.''']])

    def standing_round(self, top, bottom):
        if self is top:
            spankingText = universal.format_text([[bottom.printedName, '''continues to struggle against''', top.printedName + "'s", '''relentless spanking but only manages to get''', bottom.hisher(), 
                '''fingers firmly tangled in the folds of the slinger's robe.''']]) 
            if bottom.wearing_pants_or_shorts() or bottom.is_pantsless():
                spankingText = universal.format_text([[spankingText], ['''Smirking,''', top.printedName, '''yanks on''', bottom.printedName + "'s", 
                    bottom.clothing_below_the_waist().name, '''giving''' if self.firstRound else '''deepening''', bottom.printedName + "'s", '''wedgie.'''], ['''Then,''', top.printedname, 
                        '''delivers six full-bodied smacks to each''','''of the''', bottom.heroheroine() + "'s", bottom.bum_adj(), '''cheeks,''', bottom.printedname, 
                            '''helplessly howling all the''', '''while.''']])
                self.firstRound = False
            elif self.firstRound:
                self.firstRound = False
                spankingText = universal.format_text([[spankingText], ['''Smirking,''', top.printedName, '''flips up''', bottom.printedName + "'s", 
                        bottom.lower_clothing().name, '''exposing''', bottom.hisher(), bottom.underwear().name + "."], ['''Then,''', top.printedname, '''delivers six full-bodied smacks to each''',
                            '''of the''', bottom.heroheroine() + "'s", bottom.bum_adj(), '''cheeks,''', bottom.printedname, 
                            '''helplessly howling all the''', '''while.''']]) 
            else:
                spankingText = universal.format_text([[spankingText], [top.printedName, '''wales on''', bottom.printedName + "'s", ' '.join(['''naked,''', bottom.bum_adj(), 
                    '''ass,''']) if not bottom.wearing_underwear() else ' '.join([bottom.underwear().name + "-clad", '''ass,'''])], ['''While''', bottom.printedName, '''wails in pain and''',
                        '''humiliation.''']]) 
        else:
            if self.firstRound:
                self.firstRound = False
                return universal.format_text([[bottom.printedName, '''continues to struggle against''', top.printedName + "'s", 
                    '''relentless spanking but only manages to claw the unforgiving floor.''',
                    '''Smirking,''', top.printed, '''pulls up the slinger's''', bottom.lower_clothing().armorType, '''to reveal a shapely bare bottom.''', top.HeShe(), 
                    '''delivers six full-bodied smacks to each of the slinger's''',  bottom.bum_adj(), '''cheeks before moving on to''', bottom.hisher(), '''sit spots, the Vengador helplessly''',
                    '''howling all the while.''']])
            else:
                return universal.format_text([[bottom.printedName, '''claws the unforgiving floor, while''',
                    top.printedName, 
                    '''delivers full-bodied smack after full-bodied smack to each of the slinger's''',  bottom.muscle_adj(), '''cheeks before moving on to''', bottom.hisher(), '''sit spots,''',
                    '''the Vengador helplessly howling all the while.''']])
        return spankingText

    def standing_failure(self, top, bottom):
        if self is top:
            return universal.format_text([[self.standing_intro(top, bottom)], ['''Anxious to continue the spanking,''', top.printedName, '''begins taking off the''', bottom.heroheroine + "'s", 
                bottom.clothing_below_the_waist() + ".", '''Seeing a chance to escape,''', bottom.printedName, '''surges upward and breaks the slinger's hold on''', bottom.himher() + ".", 
                '''Pushing''', top.printedName, '''back''', bottom.printedName, '''hurriedly readjusts''', bottom.hisher(), '''clothing, then falls into''', bottom.hisher(), '''combat stance.''']])
        else:
            return universal.format_text([[self.standing_intro(top, bottom)], ['''Then, ''',  top.printedName, '''begins bunching up the hem of the slinger's''', bottom.lower_clothing().name, 
            '''in an attempt to lift it over''', bottom.hisher(), '''round ass. Seeing a chance to escape, the Vengador surges upward and breaks the''', top.heroheroine() + "'s", '''hold on''', 
            bottom.himher() + ".", '''Pushing''', top.printedName, '''back, the Vengador hurriedly readjusts''', bottom.hisher(), '''clothing as best she can.''']])

    def standing_reversal(self, top, bottom):
        if self is top:
            return universal.format_text([[self.standing_intro(top, bottom)], ['''The red-faced and reddening-bottomed''', bottom.heroheroine, '''keeps swiping''', bottom.hisher(), 
            '''hands through the air in an attempt to better snag''', top.printedName + "'s", '''clothing. Fortunately for''', bottom.printedName + ",", '''the cascading''', 
            top.lower_clothing().name, '''is easy to find, and''',
            '''that gives''', bottom.himher(), '''purchase enough to break free of''', top.printedName + "'s", '''legs. In one swift motion,''', bottom.printedName, '''stands, ggrasps the slinger's''',
            '''shoulders, and forces''', top.himher(), '''down on all fours. Quickly straddling''', top.hisher(), '''waist in the same fashion the Vengador had done to''', bottom.himher(), + ",", 
            top.printedName, '''bends over and rapidly delivers swats to the slinger's''', top.muscle_adj(), '''derriere.''']])
        else:
            return universal.format_text([[self.standing_intro(top, bottom)], ['''The red-faced and reddening-bottomed slinger keeps swiping''', bottom.hisher(), '''hands through the air in''',
                '''an attempt to grab''', top.printedName + "'s", '''clothing. Instead,''', bottom.heshe(), '''manages to grab the''', top.heroheroine() + "'s", '''ankle. This gives''', 
                bottom.himher(), '''purchase enough to break free of''', top.printedName + "'s", '''legs. In one swift motion, the Vengador grasps''', top.printedName + "'s", '''shoulders as''',
                bottom.heshe(), '''stands and forces''', top.printedName, '''down on all fours. Quickly straddling''', top.hisher(), '''waist in the same fashion''', top.printedName, 
                '''had done to''', bottom.himher() + ",", '''the spellcaster bends over and rapidly delivers swats to the''', top.heroheroine() + "'s", top.muscle_adj(), '''derriere.''']])

    def on_the_ground_intro(self, top, bottom):
        if self is top:
            return universal.format_text([[top.printedName, '''feigns casting a spell, causing''', bottom.printedName, '''to surge forward in an attempt to stop it. The slinger is expecting this,''',
                '''however, and just before the''', bottom.heroheroine(), '''is upon''', top.himerh() + ",", top.printedName, '''shoves the butt of''', top.hisehr(), top.weapon().name, 
                '''into''', bottom.printedName + "'s", '''chest hard enough to knock''', bottom.himher(), '''flat on''', bottom.hisher(), '''back. The slinger then grabs the feet of the surprised''',
                bottom.heroheroine(), '''and lifts them straight up, perpendicular to''', bottom.hisher(), '''torso. Locking''', top.hisher(), '''left arm around''', bottom.printedName, 
                '''thighs, the Vengador assaults''', bottom.hisher(), bottom.bum_adj(), '''bottom with full-armed swats as''', bottom.printedName, '''ineffectually squirms and squeals.''']])
        else:
            return universal.format_text([[top.printedName, '''feigns casting a spell, causing''', bottom.printedName, '''to rush''', top.himher(), '''in an attempt to stop it.''', top.printedName,
                '''is expecting this, however, and just before the slinger is upon''', top.himher() + ",", '''the''', top.heroheroine(), '''shoves''', top.printedName + "'s", '''chest with both''',
                '''hands, knocking''', bottom.himher(), '''flat on''', bottom.hisher(), '''back. The adventurer then grabs the feet of the surprised spellcaster and lifts them straight up,''',
                '''perpendicular to''', bottom.hisher(), '''torso.'''],
                ['''The Vengador's robe slides down to the small of''', bottom.hisher(), '''back, exposing a shapely pair of coffee-colored legs and a full, bare bottom. Locking''', top.hisher(), 
                    '''left arm around the Vengador's thighs,''', top.printedName, '''assaults the spellcaster's''', bottom.muscle_adj(), '''behind with full-armed swats, while the slinger''',
                    '''squirms and squeals.''']])

    def on_the_ground_round(self, top, bottom):
        if self is top:
            return universal.format_text([[bottom.printedName, '''tries to sit up in an effort to grab''', top.printedName + ".", '''Alas,''', bottom.heshe() + "'s", '''unable to get into a''',
                '''full sitting position, and the slinger pushes''', bottom.himher(), '''back down with''', top.hisher(), '''foot, never breaking''', top.hisher(), '''tight grip on the''',
                bottom.heroheroine + "'s", '''legs. If anything, the slinger grips''', bottom.printedName + "'s", '''thighs even tighter as''', top.heshe(), '''pushes''', top.hisher(), 
                '''foot snugly underneath the''', bottom.heroheroine() + "'s", '''chin. Immobile,''', bottom.printedName, '''is helpless to prevent a renewed barrage of swats to''', bottom.hisher(),
                '''stinging cheeks.''']]) 
        else:
            raise NotImplementedError()

    def on_the_ground_failure(self, top, bottom):
        if self is top:
            return universal.format_text([[self.on_the_ground_intro(top, bottom)], ['''Flailing''', bottom.hisher(), '''arms,''', bottom.printedName, '''is able to grab''', top.printedName + "'s", 
            '''flowing''', top.lower_clothing().name, '''and pull''', bottom.himselfherself(), '''up enough to grab the slinger's waist. With a bit of effort, the''', bottom.heroheroine(), 
            '''shoves''', bottom.hisher(), '''assailant forward, knocking''', top.printedName, '''off balance long enough for''', bottom.printedName, '''to regain''', bottom.printedName + "'s", 
            '''feet.''']])
        else:
            raise NotImplementedError()

    def on_the_ground_reversal(self, top, bottom):
        if self is top:
            return universal.format_text([[self.on_the_ground_intro(top, bottom)], [top.printedName, '''is in such a hurry to punish''', bottom.printedName, '''that''', top.heshe(), 
            '''fails to completely secure''', top.hisher(), '''victim's legs.''', bottom.printedName, '''is quick to notice this oversight and swings''', bottom.himselfherself(), '''legs back''',
            '''over''', bottom.hisher(), '''own head, throwing''', bottom.himselfherself(), '''into a roll. As''', bottom.heshe(), '''comes up from''', bottom.hisher(), '''roll, the''', 
            bottom.heroheroine(), '''sweeps the surprised Vengador's legs out from under''', top.himher(), '''and knocks''', top.himher(), '''flat on''', bottom.hisher(), '''back.''', 
            '''With a wicked grin,''', bottom.printedName, '''lifts the helpless slinger's legs up with one hand, and as soon as gravity bunches''', top.hisher(), top.lower_clothing().armorType, 
            '''around''', top.hisher(), '''waist,''', bottom.printedName + "'s", '''hand cracks against the Vengador's tightly pantied bottom with an avenging fury.''']])
        else:
            raise NotImplementedError()

    def post_combat_spanking(self):
        insurgentText = format_text([['''The Vengador leans against a nearby wall, breathing heavily.''', person.HeShe(self), '''tries to stumble away from''', name() + ",",
            '''leaning on the wall for support.''', name(), '''steps up next to''', person.himher(self), '''and presses a hand to the wall on either side of''', 
            person.himher(self) + "."],
        ['''"Who taught you how to use magic like that?" asks''', name() + "."],
        ['''"Nobody," says the Vengador. "I'm self-"'''],
        [name(), '''grabs''', person.himher(self), '''by the shoulders, spins''', person.himher(self), '''around, and presses''', person.hisher(self), '''upper body''',
            '''against the wall, so that''', person.hisher(self), '''bottom juts out slightly.''', name(), '''smacks the seat of the Vengador's''', 
            self.lower_clothing().name + "."],
        ['''"You're either lying, or the most gifted spellslinger since Ada herself," says''', name() + ".", name(), '''lands another hard slap to''', person.hisher(self), 
            '''bum. "Now. Who. Taught. You?"'''],
        ['''"Nobody-oww!" The Vengador wiggles and squeals as''', name(), '''starts to spank''', person.hisher(self), '''soft bottom.''', name(), '''doesn't stop until''', 
            person.hisher(universal.state.player), '''hand is good and sore.'''],
        ['''"Now, tell me," says''', name() + "."],
        ['''"No!" says the insurgent.''']])
        if universal.state.player.resilience() > self.resilience():
            if self.gender == person.FEMALE:
                bumAdj = "large, round, light brown"
            else:
                bumAdj = "light brown, surprisingly smooth"
            insurgentText = format_text([insurgentText, ['''"Fine."''', name(), '''grabs the back of''', person.hisher(self), self.lower_clothing().name + ",", 
                '''and lifts''','''it up past''', self.name + "'s", '''waist, revealing a bare,''', bumAdj, '''bottom.'''],
                ['''The Vengador squeals in indignity and kicks weakly at''', name() + ".", '''"No, stop, not on the bare!"'''],
                [name(), '''pins the''', self.lower_clothing().name, '''to the Vengador's back with''', person.hisher(universal.state.player), '''left hand. "Tell me the name of the person who''',
                    '''trained you."'''],
                ['''The insurgent doesn't say anything.'''],
                ['''"Fine."''', name(), '''strikes the insurgent's ample, soft, right butt cheek.''', person.HisHer(self), '''cheek bounces beneath the slap. Then''', name(),
                    '''slaps the left cheek. Then right, then left, then right again.'''],
                ['''Pretty soon, the Vengador's entire bottom is bouncing and rippling beneath''', name() + "'s", '''hard, merciless hand. The Vendgaodr's hips sway''',
                    '''desperately back and forth, trying in vain to dodge''', name() + "'s", '''hard slaps.''', person.HeShe(self), '''kicks''', person.hisher(self), 
                    '''feet and weakly pounds the wall.''', person.HeShe(self), '''tries to escape, but''', person.hisher(self), '''efforts are weak and ineffectual, and''',
                    '''all they earn''', person.himher(self), '''are a few sharp slaps to''', person.hisher(self),  '''thighs.'''],
                ['''"Ok, ok," wails the Vengador. "Please, please stop I'll tell you, I'll tell you!"'''],
                ['''"Well?" says''', name() + ",", '''landing a sharp slap to''', person.hisher(self), ''' very red bottom. "Out with it!"'''],
                ['''"Her name is Sierra," says the vengador through''', person.hisher(self), '''tears. "She works for one of the Slum Ladies, Zulimar. Specializies in''',
                    '''combat magic. She helped train all of us before this attack."'''],
                [name(), '''steps away from the wimpering Taironan, and''', person.heshe(self), '''promptly collapses into a crouch, rubbing''', person.hisher(self), 
                '''throbbing bottom.''', name(), '''looks around, and plots''', person.hisher(self), '''next move.''']])
        else:
            insurgentText = format_text([insurgentText, [name(), '''curses under''', person.hisher(universal.state.player), '''breath, and gives''', person.hisher(self), '''hand a shake.''', 
                self.name(), '''considers giving the stubborn Taironan a bare bottom spanking. But the sounds of battle return to''', name() + "'s", '''years, a harsh''',
                '''reminder that time is of the essence.''', name(), '''steps away from''', person.hisher(universal.state.player), '''beaten opponent, and plans''', person.hisher(self), 
                '''next move.''']])
        return insurgentText


class VengadorScout(Enemy):
    def __init__(self, gender, level=0, identifier=None):
        super(VengadorScout, self).__init__('Vengador Scout', gender, None, specialization=person.STRENGTH, bodyType='slim', height='average', musculature='fit', identifier=identifier)
        self.level = level
        self.equip(copy.copy(itemspotionwars.tunic))
        self.equip(copy.copy(itemspotionwars.trousers))
        self.equip(copy.copy(itemspotionwars.dagger))
        self.description = format_line(['''A short, thin Taironan''', person.manwoman(self), '''dresssed in a''', self.shirt().name + "," ''' and''', 
            self.lower_clothing().name + ".", person.HeShe(self), '''carries a''', self.weapon().name + "."])
        self.set_all_stats(strength=3, dexterity=1, willpower=2, talent=1, health=9, mana=7, alertness=2)
        self.positions = [positions.overTheKnee, positions.standing, positions.onTheGround]
        self.learn_spell(spells_PotionWars.heal)
        self.learn_spell(spells_PotionWars.weaken)
        self.learn_spell(spells_PotionWars.fortify)

    def otk_intro(self, top, bottom):
        return universal.format_text([[bottom.printedName, '''tries to drive''', top.printedName, '''to''', top.hisher(), '''knees, but''', top.printedName, '''uses''', top.hisher(), 
        '''superior grappling experience to roll with the shove, using''', bottom.printedName + "'s", '''own momentum to force''', bottom.himher(), '''into an awkward, bent over posture.''',
        ''' Sitting down on''', bottom.hisher(), '''heels, the''', top.height, '''scout''' if self is top else top.heroheroine(), '''pulls the''', 
        ''.join([bottom.heroheroine(), "'s"]) if self is top else '''scout's''', '''body over''', top.hisher(), '''knee and into a position with which''',
        '''naughty boys and girls have great familiarity.''', bottom.printedName, '''writhes as''', top.printedName + "'s", '''strong smacks begin to rain down on''', 
        bottom.hisher(), bottom.muscle_adj(), 
        '''behind, but the grappler has''', top.hisher(), '''victim right where''', top.heshe(), '''wants''', bottom.himher() + "."]])

    def otk_round(self, top, bottom):
        if self.firstRound:
            self.firstRound = False
            return universal.format_text([[bottom.printedName, '''kicks and squirms under the punishing hand of''', top.printedName + ".", '''Flinging one of''', bottom.hisher(), 
            '''hands around behind''', bottom.himher(), + ",", '''the''', bottom.heroheroine() if self is top else "scout", '''manages to slap''', bottom.hisher(), 
            '''accoster across the face. The''', '''scout''' if self is top else bottom.heroheroine(), '''retaliates by twisting''',
            bottom.printedName + "'s", '''arm around and pinning it to the small of''', bottom.hisher(), '''back. Free to spank unhindered,''', top.printedName, '''thoroughly heats''', 
            bottom.printedName + "'s", 
            '''exposed bottom.''' if bottom.clothing_below_the_waist().is_baring() else ' '.join(['''through''',  bottom.hisher(), bottom.clothing_below_the_waist().tightness, 
            bottom.clothing_below_the_waist().armorType + "."])]])
        else:
            return universal.format_text([[bottom.printedName, '''kicks and squirms under the punishing hand of''', top.printedName + ".", '''Every attempt to wrench''', bottom.hisher(), 
                '''wrist free ends in failure, and a particularly vicious stream of slaps as''', top.printedName, '''thoroughly heats''', bottom.printedName + "'s", 
            '''exposed bottom.''' if bottom.clothing_below_the_waist().is_baring() else ' '.join(['''through''',  bottom.hisher(), bottom.clothing_below_the_waist().tightness, 
            bottom.clothing_below_the_waist().armorType + "."])]])

    def otk_failure(self, top, bottom):
        return universal.format_text([[bottom.printedName, '''tries to drive''', top.printedName, '''to''', top.hisher(), '''knees, but''', top.printedName, '''uses''', top.hisher(), 
        '''superior grappling experience to try roll with the shove, using''', bottom.printedName + "'s", '''own momentum to force''', bottom.himher(), '''into an awkward, bent over posture.''',
        '''But then''', top.heshe(), '''gets roughly shouldered by the quick-thinking''', bottom.printedName + ".", '''Knocked to the ground, the Taironan somehow manages to regain''', 
        top.hisher(), '''feet before''', top.heshe(), '''is impaled by a''', bottom.weapon().weaponType, '''thrust from''', bottom.printedName + "."]])

    def otk_reversal(self, top, bottom):
        return universal.format_text([[bottom.printedName, '''tries to drive''', top.printedName, '''to''', top.hisher(), '''knees, but''', top.printedName, '''uses''', top.hisher(), 
        '''superior grappling experience to roll with the shove, using''', bottom.printedName + "'s", '''own momentum to try to force''', bottom.himher(), 
        '''into an awkward, bent over posture.''', top.printedName, '''is taken aback when''', bottom.printedName, '''spins around in a flash and bends the''', top.height, 
        '''scout''' if self is top else top.heroheroine(), '''across''',
        bottom.hisher(), '''lap.''',  '''"Over the knee, really? I've had too much experience with this position for the likes of you to hold me in it!"''' if self is top else 
        ' '.join(['''"Time to give you a taste of your own medicine."'''])],
        ['''With that, the''', bottom.heroheroine() if self is top else '''scout''', '''begins smacking the''', '''scout's''' if self is top else top.heroheroine() + "'s", top.bum_adj() + ",", 
            top.muscle_adj(), '''bottom with a fury.''']])

    def standing_intro(self, top, bottom):
        return universal.format_text([['''The wily''', top.printedName, '''ducks a mighty''', '''swing''' if bottom.weapon().weaponType == items.Sword.weaponType else '''thrust''',  
            '''from''', bottom.printedName + "'s", bottom.weapon().name, '''and wraps''', top.hisher(), '''arm around the other Taironan's waist. The''', 
            '''scout''' if self is top else bottom.heroheroine(), '''simultaneously''',
            '''presses against the small''',
            '''of''', bottom.printedName + "'s", '''back with''', top.hisher(), '''elbow, and lifts the''', bottom.heroheroine() + "'s", '''hips to give''', top.himher(),
            '''a target. Bent over in such an awkward fashion,''', bottom.printedName, '''can do nothing but endure several stinging spanks from''', bottom.hisher(), 
            '''surprisingly strong grappler.''']])

    def standing_round(self, top, bottom):
        if self is top:
            if self.firstRound:
                self.firstRound = False
                return universal.format_text([[bottom.printedName, '''curses''', bottom.himselfherself(), '''for letting the Vengador Scout get the upper hand on''', bottom.himher() + ".", 
                    '''Though''', bottom.heshe(), '''remains on''', bottom.hisher(), '''feet, it matters little, as''', bottom.hisher(), '''back is arched sufficiently to present an attractively''',
                    bottom.bum_adj(), '''target for the scout. The spanker, meanwhile cackles maliciously, clearly enjoying the thorough reddening''', top.heshe(), '''is giving''', 
                    bottom.printedName + "'s", bottom.muscle_adj(), '''bottom.''', '''Then,''', top.HeShe(), '''grabs the''', bottom.clothing_below_the_waist().waistband_hem(), '''of''', 
                    bottom.printedName + "'s", bottom.clothing_below_the_waist().tightness, bottom.clothing_below_the_waist().name + ".", bottom.printedName, '''shrieks in protest, but that''',
                    '''doesn't stop''', top.printedName, '''from''', ' ' .join(['''pushing''', bottom.printedName + "'s", bottom.clothing_below_the_waist().name, '''to the tops of''', 
                        bottom.hisher(), '''thighs,''']) if bottom.clothing_below_the_waist().liftlower() == "lower" else ' '.join([
                            '''pulling''' if bottom.clothing_below_the_waist().tightness == 'tight' else '''flipping''', bottom.printedName + "'s", bottom.clothing_below_the_waist().name, 
                            '''up  and over the small of''', bottom.hisher(), '''back,''']), '''fully exposing''', bottom.printedName + "'s", 
                        '''bare bottom.''' if bottom.clothing_below_the_waist().armorType == items.Underwear.armorType else bottom.underwear().name + "."],
                        [bottom.printedName, '''squeals and kicks as''', top.printedName, '''begins gleefully slapping''', bottom.hisher(), 
                            '''bare cheeks''' if not bottom.wearing_lower_clothing() or bottom.underwear().is_baring() else ' '.join(['''cheeks over the thin cloth of''', bottom.hisher(), 
                                bottom.underwear().name])]])
            else:
                return universal.format_text([[bottom.printedName, '''squeals, curses and kicks as''', top.printedName, '''continues energetically smacking''', bottom.printedName + "'s", 
                    bottom.bum_adj(), '''bottom,''', bottom.hisher(), '''lowered''' if not bottom.wearing_lower_clothing() else '', bottom.underwear().name, '''doing'''
                    '''absolutely''' if bottom.underwear().is_baring() or not bottom.wearing_lower_clothing() else '''almost''', '''nothing to protect''', bottom.hisher(),
                    bottom.quivering(), '''cheeks.''']])
        else:
            return universal.format_text([[bottom.printedName, '''curses violently as''', top.printedName, '''continues thrashing''', bottom.hisher(), '''vulnerable bottom.''', 
                '''Though''', bottom.heshe(), '''remains on''', bottom.hisher(), '''feet, it matters little, as''', bottom.hisher(), '''back is arched sufficiently to present an attractively''',
                bottom.bum_adj(), '''target for the''', '''scout.''' if self is top else top.heroheroine() + ".", 
                '''Then,''', top.HeShe(), '''grabs the''', bottom.clothing_below_the_waist().waistband_hem(), '''of''', 
                bottom.printedName + "'s", bottom.clothing_below_the_waist().tightness, bottom.clothing_below_the_waist().name + ".", bottom.printedName, '''shrieks in protest, but that''',
                '''doesn't stop''', top.printedName, '''from''', ' ' .join(['''pushing''', bottom.printedName + "'s", bottom.clothing_below_the_waist().name, '''to the tops of''', 
                    bottom.hisher(), '''thighs,''']) if bottom.clothing_below_the_waist().liftlower() == "lower" else ' '.join([
                        '''pulling''' if bottom.clothing_below_the_waist().tightness == 'tight' else '''flipping''', bottom.printedName + "'s", bottom.clothing_below_the_waist().name, 
                        '''up  and over the small of''', bottom.hisher(), '''back,''']), '''fully exposing''', bottom.printedName + "'s", 
                    '''bare bottom.''' if bottom.clothing_below_the_waist().armorType == items.Underwear.armorType else bottom.underwear().name + "."],
                    [bottom.printedName, '''squeals and kicks as''', top.printedName, '''begins gleefully slapping''', bottom.hisher(), 
                        '''bare cheeks''' if not bottom.wearing_lower_clothing() or bottom.underwear().is_baring() else ' '.join(['''cheeks over the thin cloth of''', bottom.hisher(), 
                            bottom.underwear().name])]])

    def standing_failure(self, top, bottom):
        return universal.format_text([['''The wily''', top.printedName, '''ducks a mighty''', '''swing''' if bottom.weapon().weaponType == items.Sword.weaponType else '''thrust''',  
            '''from''', bottom.printedName + "'s", bottom.weapon().name, '''and wraps''', top.hisher(), '''arm around the''', ''.join([bottom.heroheroine(), "'s"]) if self is top else '''scout's''', 
            '''waist. The''', '''scout''' if self is top else top.heroheroine(), '''simultaneously''',
            '''presses against the small''',
            '''of''', bottom.printedName + "'s", '''back with''', top.hisher(), '''elbow, and lifts the other Taironan's hips up enough to give''', top.himher(),
            '''a target. However,''', bottom.printedName, '''is able to plant''', bottom.hisher(), '''feet, and with a mighty shove, drives''', bottom.hisher(), '''torso up with enough force''',
            '''to throw''', top.printedName, '''off balance, breaking free of the other's grip.''',
            '''The''', bottom.heroheroine(), '''rights''', bottom.himselfherself() + ",", '''and''', '''glowers at the''', top.height, '''scout.''']])

    def standing_reversal(self, top, bottom):
        return universal.format_text([['''The wily''', top.printedName, '''ducks a mighty swing from''', bottom.printedName + "'s", bottom.weapon().weaponType, '''and wraps''', top.hisher(), 
            '''arm around the other Taironan's waist.''', bottom.printedName, '''reacts quickly, however, and encircles the hips of''', bottom.hisher(), '''opponent with''',
            bottom.hisher(), '''own arm. The two sway for a moment, as each tries to force the other to bend over. However,''', bottom.printedName, '''manages to gain the upper hand, and forces''',
            top.printedName, '''to bend over and arch''', top.hisher(), '''back. With''', bottom.printedName + "'s", '''elbow pressing down on''', 
            top.hisher(), '''back,''', top.printedName, '''can offer no resistance to the heavy rise and fall of the other's punishing hand.''']])

    def on_the_ground_intro(self, top, bottom):
        return universal.format_text([[top.printedName, '''suddenly snaps the hilt of''', top.hisher(), top.weapon().weaponType, '''up under''', bottom.printedName + "'s", '''chin, briefly dazing''',
            bottom.printedName + ".", '''Before''', bottom.printedName, '''can recover,''', top.printedName, '''rams''', top.hisher(), '''knee between''', bottom.printedName + "'s", '''legs, then''',
            '''throws''', bottom.himher(), '''facefirst into the ground.''', top.printedName, '''falls to''', top.hisher(), '''knees, one hand closing around the back of''', bottom.printedName + "'s",
            '''face and pushing it into the ground. Then,''', top.heshe(), '''begins peppering''', bottom.printedName + "'s", bottom.muscle_adj(), '''bottom with quick, stinging slaps, while''',
            bottom.printedName, '''screams and kicks against the floor.''']])

    def on_the_ground_round(self, top, bottom):
        return universal.format_text([[bottom.printedName, '''tugs vainly at''', top.printedName + "'s", '''hand, kicks''', bottom.hisher(), '''legs, and bucks''', bottom.hisher(), '''hips.''',
            '''None if it accomplishes much of anything except annoying''', top.printedName + ",", '''who makes''', top.hisher(), '''annoyance clear with a bevy hard slaps to''', 
            bottom.clad_bottom() + ",", '''making''', bottom.printedName, '''kick and buck all the more frantically.''']])


    def on_the_ground_failure(self, top, bottom):
        return universal.format_text([[top.printedName, '''suddenly snaps the hilt of''', top.hisher(), top.weapon().weaponType, '''up under''', bottom.printedName + "'s", '''chin. But''', 
            bottom.printedName, '''manages to jerk''', bottom.hisher(), '''head backward, taking nothing more than a glancing blow to''', bottom.hisher(), '''chin.''']])

    def on_the_ground_reversal(self, top, bottom):
        return universal.format_text([[top.printedName, '''suddenly snaps the hilt of''', top.hisher(), top.weapon().weaponType, '''up under''', bottom.printedName + "'s", 
            '''chin, briefly dazing''',
        bottom.printedName + ".", '''Then,''', top.printedName, '''tries to ram''', top.hisher(), '''knee between''', bottom.printedName + "'s", '''legs. However, it becomes clear that''', 
        bottom.printedName, '''was playing possum when''', bottom.heshe(), '''grabs''', top.printedName + "'s", '''knee and throws''', top.himher(), '''onto''', top.hisher(), '''back. The back''',
        '''of''', top.printedName + "'s", '''head smacks against the hard floor, and for a second''', top.heshe(), '''is dazed. In that second,''', bottom.printedName, '''drops to''', 
        bottom.hisher(), '''knees and rolls''', top.printedName,
        '''onto''', top.hisher(), '''front.''', bottom.printedName, '''grabs''', top.printedName + "'s", '''hair with one hand, and shoves''', top.hisher(),
        '''face it into the ground. Then,''', bottom.heshe(), '''begins peppering''', top.printedName + "'s", bottom.muscle_adj(), '''bottom with quick, stinging slaps, while''',
        top.printedName, '''screams and kicks against the floor.''']])

    def post_combat_spanking(self): 
        return format_text([['''The young''', person.manwoman(self), '''is on''', person.hisher(self), '''hands and knees, breathing heavily, and shaking slightly.'''],
        [name(), '''approaches the insurgent, and gives''', person.himher(self), '''a sharp slap on the bottom. The''', person.manwoman(self), 
            '''yelps, and tries to crawl away,''',
        '''but''', person.hisher(self), '''arms give out, and''', person.heshe(self), '''collapses.'''],
        ['''"So what's your job?" asks''', name() + "."],
        ['''The insurgent doesn't respond. Instead''', person.heshe(self), '''struggles back onto''', person.hisher(self), '''hands and knees, and starts to crawl away''',
            '''again.''',
        name(), '''kneels down next to''', person.himher(self), '''and presses against the middle of''', person.hisher(self), '''back, pushing''', person.hisher(self), 
        '''chest and face into the ground.''', name(), '''gives''', person.hisher(self), '''upthrust bottom a warning rub. "Will you answer my question, or do I need to''',
        '''yank these trousers down and paddle your bottom?"'''],
        ['''"Or you could, you know, stop fighting your own people, and instead help us," says the scout angrily, turning''', person.hisher(self), '''head and glaring at''',
            name() + "."],
    [name(), '''sighs. "Not this again."''', person.HeShe(), '''gives''', self.name, '''a pair of swift, hard slaps, one to each cheek. The insurgent squirms a little,''',
        '''but manages to keep quiet. "Try again."'''],
    ['''"I'm a scout," mutters the insurgent.'''],
    ['''"Oh good. I'm new here, and don't know much about the back of the guild," says''', name() + ".", '''"How about you tell me what I can expect?"'''],
    ['''The scout doesn't say anything.'''],
    [name(), '''grabs the waistband of the''', person.manwoman(self) + "'s", '''trousers, and pulls them down to''', person.hisher(self) + "'s", '''knees, revealing a''',
        '''small, but firm bare bottom.'''],
    [name(), '''pulls''', person.hisher(), '''wooden spoon out of''', person.hisher(), '''pack, and taps it lightly against the''', person.manwoman(self) + "'s", 
        '''bottom.''', name(), '''smirks a little when the scout tenses . "Last chance."'''],
    '''"Oh come on, you aren't seriously going to spank me are you?" says the scout. "Do you really thing a sore bottom is going to make me talk?"''',
    ['''"Actually, it can be surprisingly effective," says''', name() + ",", '''rubbing the''', person.manwoman(self) + "'s", '''bottom with the spoon. "It's weird.''',
    '''Regular torture just encourages the torturee to lie to make the pain stop. But for some reason, a spanking prompts the spankee to tell the truth. Maybe our truth''',
    '''centers are in our bottoms, and a spanking stimulates them?"'''],
    ['''"That makes absolutely no sense," says the insurgent.'''],
    ['''"Yes, well, whatever." The spoon whips through the air and cracks against the insurgent's bottom. The insurgent yelps, and''', person.hisher(self), '''hips jerk''',
    '''forward under the impact. "Whatever the reason, it is most effective, as you shall soon see."''', name(), '''works the spoon furiously, giving the''', 
    '''scout's bottom a thorough hiding.'''],
    ['''The scout bawls and thrashes beneath the bombardment,''', person.hisher(self), '''bitty bottom bouncing beneath the spoon's stinging slaps.'''],
    '''"Ok, ok," yelps the scout at last. "I'll tell you, I'll tell you, just please stop spanking me!"''',
    ['''"I'm listening."''', name(), '''rubs the flat of the spoon against the scout's tender bottom.'''],
    ['''"There are eight rooms," mutters the scout. "On the first floor is a kitchen, a clinic, a dining room and the training room for Adrian's combat trainer, a man''',
        '''named Morey. Apparently, the cook is a retired adventurer whose even quicker to whip out her spatula than you are to whip out that horrible spoon. There's a''',
        '''healer in the clinic. The dining room doesn't have much of interest. On the second floor are the grapple training room, the magic training room and the stealth''',
        '''training room. The stealth room is a maze, but I don't know much more. Our people who have gone in there, haven't come back out again. The armory is where''',
        '''Adrian stores all of his equipment. There are currently two Taironans in there right now, directing our acquisitions, a warslinger, and a warrior. Either one''',
        '''of them would wipe the floor with you."'''],
    ['''Wonderful.'''],
    [name(), '''forces a smile. "There, what'd I tell you? Totally effective."'''],
    ['''The scout grumbles something under''', person.hisher(self), '''breath, and reaches back to lift up''', person.hisher(self), '''trousers.'''],
    [name(), '''stands, and considers''', person.hisher(), '''next move.''']])


        
    #abstractmethod

