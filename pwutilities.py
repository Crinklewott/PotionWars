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
import conversation
import dungeonmode
import episode
import items
import music
import person
import titleScreen
import townmode
import universal


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
    universal.state.player.remove_keyword(keyword)

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
    townmode.go(townmode.offStage)
    universal.clear_screen()
    if keyEvent.key == universal.K_RETURN:
        townmode.save(episode.end_content_mode)

def to_title_screen_interpreter(keyEvent):
    universal.clear_screen()
    if keyEvent.key == universal.K_RETURN:
        titleScreen.title_screen()

def initialize_default_rooms():
    """
    Sets up the adjacencies of the basic rooms, whose adjacency lists shouldn't be affected: 
    Edge of Avaricum, Avaricum Square, Shrine, Craftman's Corridor, Therese's Tailors, Wesley and 
    Anne's Smithy, Adventurer's Guild, Slums, Maria's Home, along with the associated
    adjacencies.
    """
    edge = universal.state.get_room("Edge of Avaricum")
    square = universal.state.get_room("Avaricum Square")
    shrine = universal.state.get_room("Shrine")
    sofiasClinic = universal.state.get_room("Sofia's Clinic")
    craftmansCorridor = universal.state.get_room("Craftman's Corridor")
    taylors = universal.state.get_room("Therese's Tailors")
    smithy = universal.state.get_room("Wesley and Anne's Smithy")
    guild = universal.state.get_room("Adventurer's Guild")
    slums = universal.state.get_room("Slums")
    mariasHome = universal.state.get_room("Maria's Home")
    kitchen = universal.state.get_room("Kitchen")
    square.add_adjacent(edge)
    square.add_adjacent(shrine)
    square.add_adjacent(craftmansCorridor)
    craftmansCorridor.add_adjacent(guild)
    craftmansCorridor.add_adjacent(slums)
    craftmansCorridor.add_adjacent(smithy)
    craftmansCorridor.add_adjacent(taylors)
    guild.add_adjacent(kitchen)
    if 'boarding_with_Adrian' in keywords():
        slums.add_adjacent(mariasHome)
    elif 'boarding_with_Maria' in keywords():
        slums.add_adjacent(sofiasClinic)


def initialize_default_char_locations():
    """
    Similar to initialize_basic_rooms, this puts those characters who are usually in a particular
    place in that particular place (i.e. Peter in the Smithy, Ildri in the Kitchen).
    """
    ildri = universal.state.get_character("Ildri.person")
    peter = universal.state.get_character("Peter.person")
    carol = universal.state.get_character("Carol.person")
    sofia = universal.state.get_character("Sofia.person")
    kitchen = universal.state.get_room("Kitchen")
    smithy = universal.state.get_room("Wesley and Anne's Smithy")
    taylors = universal.state.get_room("Therese's Tailors")
    enterLeft(ildri, kitchen)
    enterLeft(peter, smithy)
    enterLeft(carol, taylors)


#-------------------------------------Music Files----------------------------------------
CHURCH = music.register(universal.resource_path('05-305-Heresy.mp3'), 'church')
LIGHT_HEARTED = music.register(universal.resource_path(
            '1-07-158-B-White-Elephants_Back-it-Up_Mix.mp3'), 
        'light-hearted')
BRATTY = music.register(universal.resource_path('1-13-173-Who-Left-the-Milk-Out!.mp3', 'bratty')
INTENSE = music.register(universal.resource_path('02-300-B-Liliths-Rage.mp3'), 'intense')
TAIRONAN = music.register(universal.resource_path('1-14-288-Dont-MEss-with-Me.mp3'), 'taironan')
VENGADOR = music.register(universal.resource_path('1-15-289-Heated-Battle.mp3'), 'vengador')
OMINOUS = music.register(universal.resource_path('POL-bridge-over-darkness-long.wav'), 'ominous')
CARLITA = music.register(universal.resource_path('2-02-291-B-Lost.mp3'), 'carlita')
MARIA = music.register(universal.resource_path('2-01-291-A-Never-Forget.mp3'), 'maria')
ROLAND = music.register(universal.resource_path('09-309-Desert-Battle.mp3'), 'roland')
ELISE = music.register(universal.resource_path('POL-land-of-peace-long.wav'), 'elise')
CATALIN = music.register(universal.resource_path('POL-sadistic-game-long.wav'), 'catalin')
CARRIE = music.register(universal.resource_path('1-17-290-My-Friend.wav'), 'carrie')
ALONDRA = music.register(universal.resource_path('POL-moonshine-piano-long.wav'), 'alondra')
ROMANTIC = music.register(universal.resource_path('POL-love-theme-long.wav'), 'romantic')
PETER = music.register(universal.resource_path('POL-telekinesis-long.wav'), 'peter')
TRISTANA = music.register(universal.resource_path('07-307-Wrath.mp3'), 'tristana')
OMINOUS_BUT_INSPIRING = music.register(universal.resource_path('1-15-192-A-Blood-Mambo.mp3'), 
'ominous but inspiring')
JAVIER = OMINOUS_BUT_INSPIRING
DEFEAT = music.register(universal.resource_path('POL-graveyard-lord-long.wav'), 'defeat')
SNEAKY = music.register(universal.resource_path('2-05-293-A-Fire-Drill.mp3'), 'sneaky')
CATFIGHT = COMBAT
TENSION = music.register(universal.resource_path('1-10-162-A-Pre-Boss-Battle-Tension.mp3'), 
    'tension')
OUTCOME_IN_DOUBT = music.register(universal.resource_path('2-06-293-B-This-Is-Not-a-Drill.mp3'),
        'outcome-in-doubt')
COMBAT = OUTCOME_IN_DOUBT
HEROIC = music.register(universal.resource_path('2-07-294-Leviathan.mp3'), 'heroic')
RIGHTEOUS_RAGE = music.register(universal.resource_path('2-11-297-Bloodlust.mp3'), 'righteous rage')

music.set_combat(COMBAT)
music.set_catfight(CATFIGHT)
music.set_boss(HEROIC)
music.set_town(music.register(universal.resource_path('2-08-295-Insidia.mp3')))
music.set_theme(music.register(universal.resource_path('POL-the-challenge-long.wav')))
music.set_defeated(music.register(universal.resource_path('POL-graveyard-lord-long.wav')))
music.set_victory(music.register(universal.resource_path('POL-the-challenge-long.wav')))
titleScreen.set_opening_crawl(CHURCH)

#A dummy character who exists solely to give us someone to talk to for arbitrary conversations. Conversations are incorporated into the dungeons as follows:
maze = person.Person("Maze", person.FEMALE, None, None)

def trigger_event(nodeName, eventTitle):
    """
    Given the name of a conversation node, and the title of the desired dungeon event, begins the
    dungeon event.
    This should be called in every event function that needs to display automatically generated conversation nodes.
    """
    node = conversation.allNodeNames[nodeName]
    global maze
    maze.printedName = eventTitle
    maze.litany = node.index
    conversation.converse_with(maze, dungeonmode.dungeon_mode)


def none():
    """
    A function that just returns None. Used by the defaultdict map events as a factory for squares
    with no events
    """
    return None
