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
import universal
import music
import titleScreen


def enterLeft(character, room):
    if character is universal.state.player:
        universal.state.location = room
    offStage = universal.state.get_room('offStage')
    offStage.remove_character(character)
    room.add_character(character)

def exitLeft(character, room):
    if character is universal.state.player:
        universal.state.location = room
    offStage = universal.state.get_room('offStage')
    room.remove_character(character)
    offStage.add_character(character)

def name():
    return universal.state.player.name

def nickname():
    return universal.state.player.nickname

def names():
    return name() + "'s"

def add_keyword(keyword):
    universal.state.player.add_keyword(keyword)

def remove_keyword(keyword):
    try:
        keywords().remove(keyword)
    except ValueError:
        return

def keywords():
    return universal.state.player.keywords

def one_in_keywords(keywordList):
    return reduce(lambda x, y : x or y, [x in keywords() for x in keywordList])

def many_in_keywords(keywordList):
    return len([x for x in keywordList if x in keywords()]) > 1

def skirt_or_dress(lowerClothing=None):
    if lowerClothing is None:
        lowerClothing = universal.state.player.clothing_below_the_waist()
    return lowerClothing.armorType == items.Skirt.armorType or lowerClothing.armorType == items.Dress.armorType

def skirt_or_pants(lowerClothing=None):
    if lowerClothing is None:
        lowerClothing = universal.state.player.clothing_below_the_waist()
    return lowerClothing.armorType == items.Skirt.armorType or lowerClothing.armorType == items.Pants.armorType

def pants(lowerClothing=None):
    if lowerClothing is None:
        lowerClothing = universal.state.player.clothing_below_the_waist()
    return lowerClothing.armorType == items.Pants.armorType

def skirt(lowerClothing=None):
    if lowerClothing is None:
        lowerClothing = universal.state.player.clothing_below_the_waist()
    return lowerClothing.armorType == items.Skirt.armorType

def dress(lowerClothing=None):
    if lowerClothing is None:
        lowerClothing = universal.state.player.clothing_below_the_waist()
    return lowerClothing.armorType == items.Dress.armorType

def wearing_underwear():
    return universal.state.player.underwear().name != items.emptyUnderwear.name

def inventory():
    return universal.state.player.inventory

def increment_spankings_taken():
    universal.state.player.bumStatus += 1
    universal.state.player.numSpankings += 1

def bummarks(character, mark):
    try:
        character.bumStatus += 1
        character.numSpankings += 1
    except AttributeError:
        pass
    character.marks.append(mark)
    #Necessary because I'm too fucking lazy to do anything special with bummarks to have it not show up in a join. So, it just returns an empty string.
    return ""

def stage_directions(stageDirections):
    """
    For now, this function just returns the empty string (allowing us to treat stage directions as comments. Invisible to the game. However, this could potentially be used for in-game commentary. Assuming people were interested,
    and we came up with a good way of distinguishing it from the game proper.
    """
    return ""
    

def increment_spankings_given():
    universal.state.player.numSpankingsGiven += 1

def lower_clothing():
    return universal.state.player.lower_clothing()
def underwear():
    return universal.state.player.underwear()
def shirt():
    return universal.state.player.shirt()
def weapon():
    return universal.state.player.weapon()

def no_pants():
    return universal.state.player.lower_clothing().name == items.emptyLowerArmor.name

def no_underwear():
    return universal.state.player.underwear().name == items.emptyUnderwear.name

def baring_underwear():
    return universal.state.player.underwear().baring

def wearing_pants():
    return universal.state.player.lower_clothing().armorType == items.Pants.armorType or universal.state.player.lower_clothing().armorType == items.Shorts.armorType

def wearing_skirt():
    return universal.state.player.lower_clothing().armorType == items.Skirt.armorType

def wearing_dress():
    return universal.state.player.lower_clothing().armorType == items.Dress.armorType

def wearing_skirt_or_pants():
    return wearing_pants() or wearing_skirt()

def wearing_skirt_or_dress():
    return wearing_skirt() or wearing_dress()

def wearing_skirt_or_dress_or_pants():
    return wearing_skirt() or wearing_dress() or wearing_pants()

def no_shirt():
    return universal.state.player.shirt().name == items.emptyUpperArmor.name

def end_content_interpreter(keyEvent):    
    townmode.go(offStage)
    clear_screen()
    if keyEvent.key == K_RETURN:
        townmode.save(end_content_mode)


#-------------------------------------Music Files----------------------------------------
CHURCH = music.decrypt(universal.resource_path('POL-apparition-long.wav'), 'church')
GUARDS = music.decrypt(universal.resource_path('POL-war-victims-long.wav'), 'guards')
TAIRONAN = music.decrypt(universal.resource_path('POL-holy-forest-long.wav'), 'taironan')
LIGHT_HEARTED = music.decrypt(universal.resource_path('POL-jesu-long.wav'), 'light-hearted')
INTENSE = music.decrypt(universal.resource_path('POL-hurry-up-long.wav'), 'intense')
SADISTIC_GAME = music.decrypt(universal.resource_path('POL-sadistic-game-long.wav'), 'sadistic_game')
VENGADOR = music.decrypt(universal.resource_path('POL-antique-market-long.wav'), 'vengador')
OMINOUS = music.decrypt(universal.resource_path('POL-bridge-over-darkness-long.wav'), 'ominous')
CARLITA = music.decrypt(universal.resource_path('POL-goodbye-long.wav'), 'carlita')
MARIA = music.decrypt(universal.resource_path('POL-moonlight-long.wav'), 'maria')
ROLAND = music.decrypt(universal.resource_path('POL-risky-plan-long.wav'), 'roland')
ELISE = music.decrypt(universal.resource_path('POL-land-of-peace-long.wav'), 'elise')
CATALIN = music.decrypt(universal.resource_path('POL-sadistic-game-long.wav'), 'catalin')
CARRIE = music.decrypt(universal.resource_path('POL-smart-ideas-long.wav'), 'carrie')
ALONDRA = music.decrypt(universal.resource_path('POL-moonshine-piano-long.wav'), 'alondra')
ROMANTIC = music.decrypt(universal.resource_path('POL-love-theme-long.wav'), 'romantic')
PETER = music.decrypt(universal.resource_path('POL-telekinesis-long.wav'), 'peter')
COMBAT = music.decrypt(universal.resource_path('POL-chase-long.wav'), 'combat')
DEFEAT = music.decrypt(universal.resource_path('POL-graveyard-lord-long.wav'), 'defeat')
music.set_combat(universal.resource_path('POL-chase-long.wav'))
music.set_boss(universal.resource_path('POL-last-duel-long.wav'))
music.set_town(universal.resource_path('POL-spiritual-path-long.wav'))
music.set_theme(universal.resource_path('POL-the-challenge-long.wav'))
music.set_defeated(universal.resource_path('POL-graveyard-lord-long.wav'))
music.set_victory(universal.resource_path('POL-the-challenge-long.wav'))
titleScreen.set_opening_crawl(CHURCH)
