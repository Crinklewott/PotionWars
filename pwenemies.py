
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
    def __init__(self, name, gender, defaultLitany, description="", printedName=None, coins=20, specialization=universal.BALANCED, dropChance=3):
        """
        Drop chance determines the chances that this character will drop a piece of equipment.
        """
        super(Enemy, self).__init__(name, gender, defaultLitany, defaultLitany, description, printedName, coins, specialization)
        self.dropChance = dropChance
        self.printedName = self.printedName + (' (M)' if self.is_male() else ' (F)')
        self.equip(items.emptyWeapon)
        self.equip(items.emptyLowerArmor)
        self.equip(items.emptyUpperArmor)
        self.equip(items.emptyUnderwear)

    def drop(self):
        "TODO: Implement"
        pass

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
    def had_spanking_reversed_by(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement reversed_spanking_of for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def reversed_spanking_of(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement reversed_spanking_of for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def avoided_spanking_by(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement avoided_spanking_by for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def failed_to_spank(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement failed_to_spank for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def spanks(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement spanks for', self.name, 'please send them an e-mail at', 
            get_author_email_bugs()]))
    #abstractmethod
    def spanked_by(self, person, position):
        raise NotImplementedError(' '.join(['Uh-Oh! Looks like', author, 'forgot to implement spanked_by for', self.name, 'please send them an e-mail at', 
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
    def __init__(self, gender, level=0):
        super(VengadorWarrior, self).__init__('Vengador Warrior', gender, None, specialization=universal.WARFARE)
        self.level = level
        self.equip(copy.copy(itemspotionwars.leatherCuirass))
        self.equip(copy.copy(itemspotionwars.trousers))
        self.equip(copy.copy(itemspotionwars.warspear))
        self.description = universal.format_line(['''A tall, broad-shouldered''', person.manwoman(self) + ".", person.HeShe(self), '''is wielding a''', self.weapon().name, 
        '''and is wearing''', self.shirt().name, '''and''', self.lower_clothing().name + "."])
        self.set_all_stats(warfare=3, grapple=0, willpower=0, magic=0, health=10, mana=0, stealth=1)
        self.spankingPositions = [positions.headBetweenLegs, positions.frontalOverLap]

    def default_stats(self):
        self.set_all_stats(warfare=2, grapple=0, stealth=1, willpower=1, magic=0, health=18, mana=0)

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
        if universal.state.player.willpower() > self.willpower():
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

    def had_spanking_reversed_by(self, person, position):
        return self.spanking_reversal_text(self, person, position)

    def reversed_spanking_of(self, person, position):
        return self.spanking_reversal_text(person, self, position) 

    def spanking_reversal_text(self, T, B, P):
        if P == positions.frontalOverLap:
            return format_text([[T.name, '''grabs''', B.name + "'s", '''hair, and tries to sweep''', person.hisher(B), '''feet out from under''', person.himher(B) + ".", 
            '''However,''', B.name, '''catches''', T.namde + "'s", '''foot, and with a heave, throws''', T.name, '''on''', person.hisher(T), '''back.''', T.name, '''lets''',
            '''go of''', B.name + "'s", '''hair,''', person.hisher(T), '''hands snapping back to catch''', himselfherself(T) + ".", person.HeShe(T), '''rolls onto''', 
            person.hisher(T), '''hands and knees, but before''', person.heshe(T), '''can stand,''', B.name, '''grabs''', person.hisher(T), '''feet and yanks them''', 
             '''out from under''', person.himher(T), + ".", person.HeShe(B), '''drags''', T.name, '''backwards, and over''', person.hisher(B), '''lap, angling''', T.name, 
             '''so that''', T.name + "'s", '''bottom is nestled under''', B.name + "'s", '''forearm.'''],
            [B.name, '''begins vigorously peppering''', T.name + "'s", '''backside.''', T.name, '''squirms and kicks, pounding inefectually at''', B.name + "'s", '''back.''',
            B.name, '''responds by spanking''', T.name, '''harder, generating a particular vicious bout of kicking. Finally,''', T.name, '''manages to (through luck more''',
            '''than anything) smash an elbow into the bottom of''', B.name + "'s", '''armpit.''', B.name, '''cries out, and''', person.hisher(B), 
            '''grip loosens enough for''',
            T.name, '''to slip out and scramble back to''', person.hisher(T), '''feet, gingerly rubbing''', person.hisher(T), '''bottom.''']])
        elif P == positions.headBetweenLegs:
            return format_text([[T.name, '''wraps''', person.hisher(T), '''fingers around''', B.name + "'s", '''neck, and pulls''', person.himher(B), '''down, forcing''', 
            person.himher(B), '''to bend over.''', B.name, '''grabs the backs of''', T.name + "'s", '''knees, and yanks them out from underneath''', T.name + ",",
            '''knocking''', T.name, '''to the ground.''', 
            B.name, '''wraps''', person.hisher(B), '''arm around''', T.name + "'s", '''calves, and lifts''', person.hisher(T), '''legs up perpendicular to the ground,''',
            '''exposing''', T.name + "'s", '''bottom.''', T.name + ",", '''cries out in protest, and tries to wiggle free, but''', B.name + "'s", '''hold is firm.'''],
            [ 
                B.name, '''gives''', T.name, '''a hard thrashing, setting''', T.name + "'s", '''butt aflame. Eventually,''', T.name, '''manages to''',
                '''throw''', person.himselfherself(T), '''backwards, going into a backward roll and springing to''', person.hisher(T), '''feet.''']]) 
            
    def spanked_by(self, person, position):
        return self.spanking_text(person, self, position)

    def spanking_text(self, spanker, spankee, position):
        T = spanker
        B = spankee
        if position == positions.frontalOverLap:
            return format_text([[T.name, '''grabs''', B.name + "'s", '''hair, and sweeps''', person.hisher(B), '''feet out from under''', person.himher(B), '''knocking''', 
                person.himher(B), '''to''', person.hisher(B), '''knees.''', T.name, '''drops down onto''', person.hisher(T), '''heels, and yanks''', B.name, '''across''', person.hisher(T), 
                '''lap, angled so that''', B.name, '''is facing backwards, and''', person.hisher(B), '''bottom is nestled in the crook of''', T.name + "'s", '''arm.''', T.name, 
                '''begins sharply spanking''', B.name + "'s", '''vulnerable bottom,''', person.hisher(T), '''hand rapidly alternating between cheeks.''', B.name, '''grunts and''',
                '''jerks beneath the barrage,''', person.hisher(B), '''legs scrambling for purchase.'''],
            ['''Finally,''', B.name, '''manages to wrench''', person.himselfherself(B), '''free, rolls away, and jumps to''', person.hisher(B), '''feet.''']])
        elif position == positions.headBetweenLegs:
            return format_text([[T.name, '''wraps''', person.hisher(T), '''fingers around''', B.name + "'s", '''neck, and pulls''', person.himher(B), '''down, forcing''', 
            person.himher(B), '''to bend over.''', person.HeShe(T), '''locks''', person.hisher(T), '''legs around''', B.name + "'s", '''neck firmly enough to hold''', 
            person.himher(B), '''but not hard enough to cut off''', person.hisher(B), '''air.'''], 
            [T.name, '''leans over''', B.name + "'s", '''hunched back, and begins rapidly spanking''', B.name + "'s", '''large bottom.'''],
            [B.name, '''twists and grunts beneath the barrage, clutching at''', T.name + "'s", '''calves, and trying to knock''', person.himher(T), '''over. In response,''',
                T.name, '''starts spanking''', B.name, '''harder and faster, eliciting the occasional yelp from the Vengador.'''],
            ['''Finally, with a herculean effort,''', B.name,'''manages to straighten, throwing''', T.name, '''on''', person.hisher(T), '''back.''', T.name, 
                '''quickly rolls''', '''back to''', person.hisher(T), '''feet and grabs''', B.name, '''before''', B.name, '''can retaliate properly.''']])

    def spanks(self, person, position):
        return self.spanking_text(self, person, position)

    def avoided_spanking_by(self, person, position):
        return self.spank_miss_text(person, self, position)


    def spank_miss_text(self, T, B, position):
        if position == positions.frontalOverLap:
            return format_text([[T.name, '''grabs''', B.name, '''by the hair, and tries to haul''', person.himher(B), '''down. But''', B.name, '''thwacks''', T.name, 
            '''on the inside of the elbow, and breaks''', T.name + "'s", '''grip.''']])
        elif position == positions.headBetweenLegs:
            return format_text([[T.name, '''wraps''', person.hisher(T), '''fingers around the back of''', B.name + "'s", '''neck, and tries to yank''', person.himher(B), 
            '''over. However,''', B.name, '''slips''', person.hisher(B), '''arms between''', T.name + "'s", '''and forces them apart.''']])
    def failed_to_spank(self, person, position):
        return self.spank_miss_text(self, person, position)

class VengadorSpellslinger(Enemy):
    def __init__(self, gender, level=0):
        super(VengadorSpellslinger, self).__init__('Vengador', gender, None, specialization=universal.COMBAT_MAGIC)
        self.level = level
        self.set_all_stats(warfare=0, grapple=1, willpower=1, magic=3, health=7, mana=10, stealth=0)
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
        self.spankingPositions = [positions.overOneKnee, positions.waistBetweenLegs]

    def default_stats(self):
        self.set_all_stats(warfare=0, grapple=1, stealth=0, willpower=1, magic=2, health=7, mana=10)

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
        if universal.state.player.willpower() > self.willpower():
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
            insurgentText = format_text([insurgentText, [name(), '''curses under''', person.hisher(universal.state.player), '''breath, and gives''', hisher(self), '''hand a shake.''', 
                self.name(), '''considers giving the stubborn Taironan a bare bottom spanking. But the sounds of battle return to''', name() + "'s", '''years, a harsh''',
                '''reminder that time is of the essence.''', name(), '''steps away from''', person.hisher(universal.state.player), '''beaten opponent, and plans''', person.hisher(self), 
                '''next move.''']])
        return insurgentText

    def had_spanking_reversed_by(self, person, position):
        return self.spanking_reversal_text(self, person, position)

    def spanking_reversal_text(self, T, B, P):
        if T.lower_clothing().armorType == items.emptyLowerArmor.armorType:
            lc = T.underwear()
        else:
            lc = T.lower_clothing()
        if P == positions.overOneKnee:
            return format_text([[T.name, '''bends over slightly and barrels shoulder first into''', B.name + ".", B.name, '''pivots at the last minute.''', person.HeShe(B),
            '''grabs''', T.name + "'s", '''shoulders, goes down on one knee, and yanks''', T.name, '''over''', person.hisher(B), '''thigh.''', B.name, items.liftlower(lc),
            T.name + "'s", lc.name + ",", '''exposing''', (format_line([T.name + "'s", T.underwear().name]) if lc.armorType != items.Underwear.armorType else 
                "bare bottom") + "."],
            [T.name, '''reaches back and tries to shield''', person.hisher(T), '''exposed bottom, but''', B.name, '''easily catches''', person.hisher(T), '''arm and pins''',
            '''it to''', person.hisher(T), '''back.''', B.name, '''begins thrashing''', T.name + "'s", items.bottom_without_lower_clothing(T), '''with gusto.''', T.name, 
            '''yelps and kicks frantically.''', person.HisHer(T), '''bottom wiggles around on''', B.name + "'s", '''thigh in a futile effort to escape '''
            '''the sharp slaps. Before too long,''', B.name, '''gives''', T.name, '''a shove, sending''', person.himher(T), '''rolling across the ground.''', T.name, 
            '''scrambles back to''', person.hisher(T), '''feet, while at the same time fixing''', person.hisher(T), '''clothing.''']])
        elif P == positions.waistBetweenLegs:
            return format_text([[T.name, '''tries to sweep''', B.name + "'s", '''feet out from under''', person.himher(B), + ".", '''But''', B.name, '''catches''', T.name + 
                "'s", '''foot with''', person.hisher(B), '''own leg. The two combatants sway precariously for a moment, then with a sudden heave,''', B.name, '''pushes''',
                T.name + "'s", '''leg out wide, throwing''', T.name, '''off-balance. Then,''', B.name, '''grabs''', T.name + "'s", '''shoulders, and yanks''', 
                person.himher(T), '''into a bent over position, and gives''', person.himher(T), '''a hard shove.''', T.name, '''falls onto''', person.hisher(T), 
                '''hands and knees.''', B.name, '''straddles''', T.name + ",", '''locking''', person.hisher(B), '''legs around''', T.name + "'s", '''waist and holding''',
                person.himher(T), '''in position.''', B.name, items.liftlower(lc), T.name + "'s", lc.name + ",", '''revealing''', T.name + "'s", 
                (T.underwear() if lc.armorType != items.Underwear.armorType else 'bare bottom') + ".", '''After leaning over slightly, and resting''', person.hisher(B),
                '''hand on''', T.name + "'s", '''hip,''', B.name, '''raises''', person.hisher(B), '''other hand, and starts a quick, painful chastisement of''', 
                T.name + "'s", items.bottom_without_lower_clothing(T) + ".", T.name, '''squeaks, more in embarassment than pain (at first), and thrashes around''',
                '''desperately. Unfortunately, all''', person.heshe(T), '''manages to do is is make''', person.hisher(T), '''bottom jerk back and forth, providing a more''',
                '''difficult target. Annoyed,''', B.name, '''picks up the pace of the spanking, administering a string of hard and fast slaps that quickly makes''', T.name,
                '''yowl.'''],
                '''Eventually,''', T.name, '''manages to slip free, and scrambles to''', person.hisher(T), '''feet, adjusting''', person.hisher(T), '''clothing as''',
                person.heshe(T), '''does so.'''])
        else:
            return format_line(['''Looks like the reversal of position''', P.name, '''for the Vengador enemy hasn't been given any text. Please let''', author, '''know''',
            '''with an e-mail to''', authorEmailBugs + ".", '''Make sure to tell them which enemy, which dungeon and which position triggered this error.'''])

    def reversed_spanking_of(self, person, position):
        return self.spanking_reversal_text(person, self, position)

    #abstractmethod
    def spanked_by(self, person, position):
        return self.spanking_text(person, self, position)

    def spanking_text(self, T, B, P):
        if B.lower_clothing() == items.emptyLowerArmor:
            lc = B.underwear()      
        else:
            lc = B.lower_clothing()
        if P == positions.overOneKnee:
            return format_text([[T.name, '''bends over slightly and barrels shoulder first into''', B.name + ".", B.name, '''stumbles backwards several steps.''', 
                T.name, '''pivots around to''', B.name + "'s", '''side, goes down on one knee, and hauls''', B.name, '''over''', person.hisher(T), '''thigh, bringing''', 
                person.hisher(B), '''large bottom''' if isinstance(B, VengadorSpellslinger) else "bottom", '''into view.''', T.name, items.liftlower(lc), B.name + "'s",
                lc.name + ",", '''revealing a''', format_line(['''large, round, soft''', items.bottom_without_lower_clothing(B) + "."]) if 
                isinstance(B, VengadorSpellslinger) 
                else items.bottom_without_lower_clothing(B) + "."],
            [B.name, '''squawks in surprise and reaches back to try and shield''', person.hisher(B), '''bum.'''],
            [T.name, '''grabs''', B.name + "'s", '''arm and pins it to''', person.hisher(B), '''back. Then''', T.name, '''begins ruthlessly thrashing''', B.name + "'s", 
                format_line(['''soft''', items.bottom_without_lower_clothing(B) + "."]) if isinstance(B, VengadorSpellslinger) 
                else items.bottom_without_lower_clothing(B) + "."],
            [B.name + "'s", '''bottom bounces and ripples beneath''', T.name + "'s", '''hard hand.''', person.HeShe(B), '''kicks and flails, pounding the ground with the''',
                '''flat of''', person.hisher(B), '''free hand, and drumming''', person.hisher(B), '''toes into the ground.'''],
            ['''Finally,''', T.name, '''rolls''', B.name, '''off''', person.hisher(T), '''knee.''', B.name, '''crawls away frantically, quickly fixing''', person.hisher(B),
            '''clothing. Then''', T.name, '''grabs''', person.himher(B) + ",", '''and the struggle resumes.''']])
        elif P == positions.waistBetweenLegs:
            return format_text([[T.name, '''sweeps''', B.name + "'s", '''legs out from under''', person.himher(B) + ",", '''knocking''', person.himher(B), '''to''', 
                person.hisher(B), '''knees. Then,''', T.name, '''grabs''', B.name, '''by the shoulders and steps back, yanking''', B.name, '''forward and down.''', B.name,
                '''yelps, and''', person.hisher(B), '''hands snap out to catch''', person.himselfherself(B) + ".", '''Before''', B.name, '''can retaliate,''', T.name, 
                '''straddles''', person.himher(B) + ",", '''and clamps''', person.hisher(T), '''legs securely around''', B.name + "'s", '''waist.'''],
            [T.name, '''leans over and''', items.liftlower(lc), B.name + "'s", lc.name + ",", '''revealing a''', format_line(['''large, round, soft''', 
                items.bottom_without_lower_clothing(B)]) if isinstance(B, VengadorSpellslinger) else items.bottom_without_lower_clothing(B)],
            [B.name, '''yelps and bucks between''', T.name + "'s", '''legs, accomplishing nothing but making''', person.hisher(B), items.bottom_without_lower_clothing(B),
                '''bob.'''],
            [T.name, '''lifts''', person.hisher(T), '''hand and snaps it down against''', B.name + "'s", '''right cheek.''', B.name, '''yelps, and tries to straighten.''',
                '''For a second, the two combatants sway dangerously. Then,''', T.name, '''shifts''', person.hisher(T), '''foot forward slightly, giving''', 
                person.himselfherself(T), '''a bit more stability.''', person.HeShe(T), '''reaches back with''', person.hisher(T), '''non-spanking hand, and pushes on''',
                B.name + "'s", '''shoulder-blades, forcing''', person.himher(B), '''back down onto''', person.hisher(B), '''elbows. Then,''', T.name, '''returns''', 
                person.hisher(T), '''attention back to''', B.name + "'s", '''exposed bottom.''', B.name + "'s", '''bottom sways and jerks beneath the hard slaps, jiggling''',
                '''mightily beneath the merciless barrage.''', person.HeShe(B), '''pounds''', person.hisher(B), '''feet against the ground, and squeals in pain.'''],
            ['''Finally,''', B.name, '''manages to reach back and grab''', T.name + "'s", '''ankle. With a mighty heave,''', B.name, '''throws''', T.name, '''off-balance,''',
                '''giving''', person.himher(B), '''just enough room to scramble out from between''', T.name + "'s", '''legs.''', person.HeShe(B), '''quickly fixes''', 
                person.hisher(B), '''clothing.''']])
        else:
            return format_line(['''Looks like the position''', P.name, '''for the Vengador enemy hasn't been given any text. Please let''', author, '''know with an e-mail''',
            '''to''', authorEmailBugs + ".", '''Make sure to tell them which enemy, which dungeon and which position triggered this error.'''])

        def spanks(self, person, position):
            return self.spanking_text(self, person, position)
    #abstractmethod
    def spanking_missed_text(self, T, B, P):
        if P == positions.overOneKnee:
            return format_line([T.name, '''bends over slightly and tries to barrel shoulder first into''', B.name + ".", '''But''', B.name, '''manages to catch''', 
            T.name + "'s", '''shoulder, and shoves''', person.himher(T), '''backwards before''', T.name, '''could get a good grip on''', B.name + "."])
        elif P == positions.waistBetweenLegs:
            return format_line([T.name, '''tries to sweep''', B.name + "'s", '''legs out from underneath''', person.himher(B) + ",", '''but''', B.name + "'s", 
            '''own leg snaps out and catches''', T.name + "'s", '''on the side of the calf. The two combatants sway precariously for a moment, before''', T.name, 
            '''withdraws.'''])

    def avoided_spanking_by(self, person, position):
        return self.spanking_missed_text(person, self, position)
    def failed_to_spank(self, person, position):
        return self.spanking_missed_text(self, person, position)

class VengadorScout(Enemy):
    def __init__(self, gender, level=0):
        super(VengadorScout, self).__init__('Vengador Scout', gender, None, specialization=person.GRAPPLE)
        self.level = level
        self.equip(copy.copy(itemspotionwars.tunic))
        self.equip(copy.copy(itemspotionwars.trousers))
        self.equip(copy.copy(itemspotionwars.dagger))
        self.description = format_line(['''A short, thin Taironan''', person.manwoman(self), '''dresssed in a''', self.shirt().name + "," ''' and''', 
            self.lower_clothing().name + ".", person.HeShe(self), '''carries a''', self.weapon().name + "."])
        self.set_all_stats(warfare=1, grapple=3, willpower=2, magic=1, health=7, mana=7, stealth=2)
        self.spankingPositions = [positions.diaper, positions.underarm]
        self.learn_spell(spells_PotionWars.heal)
        self.learn_spell(spells_PotionWars.weaken)
        self.learn_spell(spells_PotionWars.fortify)

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


    def reversal_spanking_text(self, spanker, spankee, position):
        T = spanker
        B = spankee
        P = position
        if P == positions.underarm:
            return format_text([[T.name, '''rams''', person.hisher(T), '''knee into''', B.name + "'s", '''gut, causing''', B.name, '''to hunch in pain,''', T.name, 
            '''wraps''', person.hisher(T), '''arm around''', B.name + "'s", '''waist. But then''', B.name, '''snakes''', person.hisher(B), '''own arm around''', 
            T.name + "'s", '''waist, sweeps''', T.name + "'s", '''feet out from under''', person.himher(T) + "," '''and bends''', T.name, '''over''', person.hisher(B), 
            '''hip.'''],
            [B.name, '''grabs''', T.name + "'s", T.clothing_below_the_waist().name, '''and''', items.lowerlift(T.clothing_below_the_waist()),
            items.itthem(T.clothing_below_the_waist()), '''exposing''', T.name + "'s", T.underwear().name + ".",  B.name, '''starts to give''', T.name, 
            '''a hard spanking.''',
                T.name + "'s", T.clad_bottom(), '''jiggles beneath the barrage, and it isn't long before''', T.name, '''is bobbing and kicking in''', B.name + "'s", 
                '''merciless grip.'''],
            ['''Eventually,''', T.name, '''manages to land a solid punch to the back of''', B.name + "'s", '''knee.''', B.name + "'s", '''leg buckles, and''', 
            person.heshe(B), '''loses''', person.hisher(B), '''balance. This gives''', T.name, '''just the opening''', person.heshe(T), '''needs to wiggle free.''', 
            person.HeShe(T),
            spanking.restore_lower_lift(T.clothing_below_the_waist()), person.hisher(T), T.clothing_below_the_waist().name, '''back over''', person.hisher(T), 
            '''smarting bottom.''']])
        elif P == positions.diaper:
            return format_text([[T.name, '''crouches slightly, and goes for''', B.name + "'s", '''legs.''', B.name, '''shuffles backward a few steps, and''', 
                person.hisher(B), '''hands lance out to catch''', T.name + "'s", '''shoulders.''', B.name, '''gives a hard downward shove on''', T.name + "'s", 
                '''shoulders, forcing''', T.name, '''to bend over so far that''', T.name, '''has to catch''', person.himselfherself(T), '''with''', person.hisher(T), 
                '''hands.''', B.name, '''wraps''', person.hisher(B), '''thighs around''', T.name + "'s", '''neck, and lands a sharp slap to''', T.name + "'s", 
                '''vulnerable, upthrust bottom.''', T.name, '''grunts, grabs''', B.name + "'s", '''calves and tries to force them apart enough to slip free.''',
                B.name, '''holds firm, however, and begins spanking''', T.name + "'s", '''bottom.'''],
            ['''The spanking is hard and fast, and before long''', T.name + "'s", '''bottom is jerking back and forth, and''', T.name, '''is yowling and stomping''', 
                person.hisher(T), '''feet. Eventually,''', person.heshe(T), '''manages to force''', B.name + "'s", '''legs apart enough for''', person.hisher(T), 
                '''head to slip free.''', T.name, '''scrambles backwards, while''', B.name, '''fixes''', person.hisher(B), '''stance, and prepares for''', T.name + "'s",
                '''retaliation.''']])
    def had_spanking_reversed_by(self, person, position):
        return self.reversal_spanking_text(self, person, position)
    #abstractmethod
    def reversed_spanking_of(self, person, position):
        return self.reversal_spanking_text(person, self, position)
    #abstractmethod

    def spanking_miss_text(self, spanker, spankee, position):
        T = spanker;
        B = spankee; 
        if position == positions.underarm:
            return format_text([[T.name, '''rams''', person.hisher(T), '''knee into''', B.name + "'s", '''gut.''', B.name, '''hunches in pain, bending over slightly.''',
            T.name, '''tries to wrap''', person.hisher(T), '''arm around''', B.name + "'s", '''back, but''', B.name, '''rams''', person.hisher(B), '''elbow''',
            '''into''', T.name + "'s", '''armpit.''', T.name, '''cries out in pain, and stumbles back a few steps, clutching at''', person.hisher(T), '''armpit. This''',
            '''gives''', B.name, '''the time''', person.heshe(T), '''needs to catch regain''', person.hisher(B), '''footing.''']])
        elif position == positions.diaper:
            return format_line([T.name, '''grabs''', B.name + "'s", '''legs.''', B.name, '''smashes''', person.hisher(B), '''knee into''', T.name + "'s", '''nose, and''',
            T.name, '''stumbles backward.'''])

    def avoided_spanking_by(self, person, position):
        return self.spanking_miss_text(person, self, position)
    #abstractmethod
    def failed_to_spank(self, person, position):
        return self.spanking_miss_text(self, person, position)

    def spanking_text(self, spanker, spankee, position):
        T = spanker
        B = spankee
        P = position
        if P == positions.underarm:
            return format_text([[T.name, '''rams''', person.hisher(T), '''knee into''', B.name + "'s", '''gut.''', B.name, '''hunches in pain, bending over slightly, and''',
                T.name, '''wraps''', person.hisher(T), '''arm around''', B.name + "'s", '''back.''', person.HeShe(T), '''bends''', B.name, '''over''', person.hisher(T), 
                '''hip.''', T.name, '''gives''', B.name + "'s", '''bottom a light rub, and then proceeds to give it a good hiding.'''],
                [B.name, '''twists and kicks desperately in''', T.name + "'s", '''grip, but''', T.name, '''only tightens''', person.hisher(T), '''grip, and increases the''',
                '''speed and force of''', person.hisher(T), '''smacks.''', B.name, '''starts to yelp, and''', person.hisher(B), '''squirming becomes so bad, that''',
                person.heshe(B), '''manages to break free.''', person.HeShe(B), '''scrambles away, rubbing''', person.hisher(B), '''smarting bottom and cursing.''']])
        elif P == positions.diaper:
            return format_text([[T.name, '''grabs''', B.name + "'s", '''legs and heaves, throwing''', B.name, '''flat on''', person.hisher(B), '''back.''', T.name, 
            '''pushes''', B.name + "'s", '''legs back over''', person.hisher(B), '''head, and crouches down next to''', B.name + "'s", '''vulnerable bottom.''', T.name, 
            '''raises''', person.hisher(T), '''hand.''', B.name, '''wiggles and claws at the ground, desperately trying to drag''', person.himselfherself(B), '''away, but''',
            T.name, '''holds''', person.himher(B), '''fast. Then,''', T.name + "'s", '''hand crashes into''', B.name + "'s", '''bottom.''', '''The bottom ripples beneath''',
            '''the impact, and''', B.name, '''yowls.''', T.name, '''raises''', person.hisher(T), '''hand and spanks''', B.name, '''again. And again, and again, and again,''',
            '''seemingly with no sign of stopping.'''],
            [B.name, '''writhes around on the ground, howling and carrying on, while''', T.name, '''thrashes''', person.hisher(B), '''bottom. Eventually,''', B.name, 
            '''manages to heave''', person.hisher(B), '''upper body up enough to grab''', T.name + "'s", '''arm and break''', T.name + "'s", '''grip on''', person.hisher(B),
            '''legs.''', B.name, '''rolls onto''', person.hisher(B), '''side and scrambles back to''', person.hisher(B), '''feet.''']])
        
    #abstractmethod
    def spanks(self, person, position):
        return self.spanking_text(self, person, position)
    #abstractmethod
    def spanked_by(self, person, position):
        return self.spanking_text(person, self, position)
