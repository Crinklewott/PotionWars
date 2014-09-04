import universal
import music
import titleScreen


def enterLeft(character, room):
    offStage = universal.state.get_room('offStage')
    offStage.remove_character(character)
    room.add_character(character)

def exitLeft(character, room):
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
