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
import dungeonmode
import episode
import items
import itemspotionwars
import pwutilities
import music
import person
import spells_PotionWars
import townmode
import universal

ildri = None
kitchen = None
deidre = None
alondra = None
sofiasClinic = None
    #def __init__(self, name, gender, defaultLitany, litany, description="", printedName=None, 
    #        coins=20, specialization=universal.BALANCED, order=zeroth_order, dropChance=0, rawName=None, skinColor='', eyeColor='', hairColor='', hairStyle='', marks=None,
    #        musculature='', hairLength='', height='', bodyType=''): 
#BODY_TYPES = ['slim', 'average', 'voluptuous', 'heavyset']


#HEIGHTS = ['short', 'average', 'tall', 'huge']


#MUSCULATURE = ['soft', 'fit', 'muscular']


#HAIR_LENGTH = ['short', 'shoulder-length', 'back-length', 'butt-length']

#SHORT_HAIR_STYLE = ['down']
#SHOULDER_HAIR_STYLE = SHORT_HAIR_STYLE + ['ponytail', 'braid', 'pigtail', 'bun']
def build_chars():
    pass

try:
    ildri = universal.state.get_character('Ildri.person')
except KeyError:
    ildri = person.Person('Ildri', person.FEMALE, None, None, ' '.join(["Ildri is a towering, muscular, golden-haired, and fair-skinned woman. She looks to be about the same age as Adrian. She is",
        "wearing an apron, a",
        "short-sleeve tunic, a pair of wool trousers, and a heavy pair of boots. Her long blonde hair is pulled back into a single thick braid."]), skinColor="peach", eyeColor="blue", 
        hairColor="blonde", hairStyle="braid", musculature="muscular", hairLength="back-length", height="huge", bodyType="voluptuous")
else:
    ildri.description = ' '.join(["Ildri is a towering, muscular, golden-haired, and fair-skinned woman. She looks to be about the same age as Adrian. She is",
        "wearing an apron, a",
        "short-sleeve tunic, a pair of wool trousers, and a heavy pair of boots. Her long blonde hair is pulled back into a single thick braid."])
    ildri.skinColor = 'peach'
    ildri.eyeColor = 'blue'
    ildri.hairColor = 'blonde'
    ildri.hairStyle = 'braid'
    ildri.musculature = 'muscular'
    ildri.hairLength = 'back-length'
    ildri.height = 'huge'
    ildri.bodyType = 'voluptuous'
try: 
    deidre = universal.state.get_character('Deidre.person')
except KeyError:
    deidre = person.Person('Deidre', person.FEMALE, None, None, ''.join(["A tall, slender woman with frizzy, shoulder-length blonde hair pulled back into a bun. She has piercing blue eyes, and",
        " carries herself with rod-straight posture. A black beret sits on top of her head."]), specialization=universal.STATUS_MAGIC, order=person.first_order, skinColor="peach", eyeColor="blue",
        hairColor="blonde", hairLength="shoulder-length", hairStyle="bun", height="tall", bodyType="slim", musculature="fit")
try:
    alondra = universal.state.get_character('Alondra.person')
except KeyError:
    alondra = person.Person('Alondra', person.FEMALE, None, None, ''.join(['''Alondra is a Taironan woman with rich, dark caramel skin, . She is a little on the short side of average.''',
        '''She has shoulder-length hair black hair, and relatively small, dark brown eyes. In contrast to her height, her breasts are a little on the large side of average.''',
        '''She has a round, protruding bottom that rolls enticingly when she walks.''']), specialization=universal.SPEED, order=person.second_order, skinColor="caramel", eyeColor="brown",
        hairColor="black", hairLength="shoulder-length", hairStyle="down", height="average", bodyType="voluptuous", musculature="soft")
    alondra.set_all_stats(strength=2, willpower=2, talent=3, dexterity=1, alertness=4, health=23, mana=18)

if alondra.is_naked():
    alondra.take_item(itemspotionwars.alondrasSkirt)
    alondra.equip(itemspotionwars.alondrasSkirt)
    alondra.take_item(itemspotionwars.alondrasVNeckTunic)
    alondra.equip(itemspotionwars.alondrasVNeckTunic)
    alondra.equip(itemspotionwars.alondrasChemise)
    alondra.equip(itemspotionwars.boyShorts)
    alondra.take_item(itemspotionwars.dagger)
    alondra.equip(itemspotionwars.dagger)

alondra.learn_spell(spells_PotionWars.heal)
alondra.learn_spell(spells_PotionWars.fortify)

try:
    sofia = universal.state.get_character("Sofia.person")
except KeyError:
    sofia = person.Person("Sofia", person.FEMALE, None, None, ''.join(['''Sofia is a middle-aged Taironan woman with moderately dark skin. She is short and thin, with graying shoulder-length''',
        '''hair. She is wearing a plain cotton dress.''']))

try:
    airell = universal.state.get_character("Airell.person")
except KeyError:
    airell = person.Person("Airell", person.MALE, None, None, ''.join(['''A slouching,''',
                '''exceptionally pale man with out of control red hair and a big bushy red''',
                '''beard that extends all the way down to his chest.''']))



def build_rooms():
    pass

try:
    kitchen = universal.state.get_room('Kitchen')
except KeyError:
    kitchen = townmode.Room("Kitchen", 
            ' '.join(["The kitchen is a rather large room with two long, waist-high counters running through the middle. Along the sides of the walls are a few small",
        "tables and",
        "stools. A pair of massive hearths sit at the far end, and a pair of turnspit dogs are lying next to the hearth. Their heads come up, and their tails thump against the ground as the Taironan", 
        "enters. There is a large hole in the south wall. The hole has been braced with several hastily carved timbers, and a few thick furs have been draped over it, so that",
        "customers can't peer directly into the back of the guild. A pair of high windows sit on the western wall on either side of the hearth."]), [universal.state.get_room("Adventurer's Guild")],
        None, None, pwutilities.LIGHT_HEARTED, "pwutilities.LIGHT_HEARTED", None)

try:
    sofiasClinic = universal.state.get_room("Sofia's Clinic")
except KeyError:
    sofiasClinic = townmode.Room("Sofia's Clinic", ' '.join(["The 'clinic' is nothing more than a long, dark, low-ceilinged room crammed with piles of ragged blankets. Immersed in the piles of",
        "blankets are dozens of Taironans, all in different states of duress. Most of them are shivering quietly, or sleeping fitfully. Some are moaning, and shifting. A few are crying, and shaking",
        "violently. There is even one man who is being wrestled back into his blankets, while screaming incoherently in an unrecognizable dialect. No more than",
        "half a dozen helpers, mostly women, are moving amongst the clinic's patients."]), [], None, None, pwutilities.TAIRONAN, "pwutilities.TAIRONAN", 
        None)

try:
    adriansOffice = universal.state.get_room("Adrian's Office")
except KeyError:
    adriansOffice = townmode.Room("Adrian's Office", ' '.join(["A spartan place consisting only of a large desk, and several chairs. A long, whippy cane hangs on the wall above Adrian's chair.",
        "Despite being his 'office,' Adrian rarely uses it. He generally prefers to be out in the main room working behind the counter. He only uses his office when he wants to have a private",
        "conversation, typically while negotiating with clients."]), [], None, None, pwutilities.LIGHT_HEARTED, "pwutilities.LIGHT_HEARTED", None)


    #               0     1     2     3     4     5     6     7     8     9    10    11    12    13    14    15    16    17    18    19
slumsLevel1Map = (
                 ( "___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___","___", "_"),
                 ("|   ","___","___","   ","___"," .,","   ","___","___","___",".,", "___","___","___","___","___","___","___","___","   ","|" ), #19
                 ("|   ","|.,",";.,","|  ","|.,",";__","|  ","|__",";  ","___","   ","___","   ",";__","|.,",";.,",";.,",";__","|.,","|  ","|" ), #18
                 ("|   ","|.,",";.,","|  ","|__","|.,","   ","|__",";  ",";__","|  ",";__","|  ",";__","|.,",";__",";__","|  ","|__",";  ","|" ), #17
                 ("|   ","|.,",";.,","|  ",";__","|__","|  ","|__",";__",";__","|.,",";__","|__",";__","|__","___","   ","___","   ","___","|" ), #16 
                 ("|   ",";.,",";.,","|  ",";__","|.,","   ","___","___","   ","___","___","|__",";  ","||.,",";.","|  ",";.,","|  ","|.,","|" ), #15
                 ("|   ","|.,",";.,","|  ","|.,",";.,","|  ","|  ","   ","|  ","|__",";__",";__","   ","|.,",";.,",";  ","|__","|  ",";__","|" ), #14
                 ("|   ","|.,",";.,","|  ","|.,",";.,","|  ","|  ","   ","|  ","|  ","   ","   ","|  ","|__",";__","|  ",";__","|  ",";.,","|" ), #13
                 ("|   ","|.,",";.,","|  ","|__",";.,","|  ",";  ","   ","|  ",";  ","   ","   ","|__","___","   ","   ","   ","   ","|__","|" ), #12
                 ("|   ","|__",";__",";__","., ","|__","|  ","|__","___","|  ",";  ","   ","   ","|__",";__",";  ","   ","., ","   ",";.,","|" ), #11
                 ("|   ","   ","   ","|.,",";.,",";.,","|  ","|.,","|.,","|.,","|__","___","___","|__","   ","., ","., ",";.,",";.,","|__","|" ), #10
                 ("|   ","___","   ","|.,",";.,",";.,","|  ","|.,",";__",";__",";__",";__",";__","|__",";  ","|__","|__",";__",";__","|.,","|" ), #9
                 ("|___","|  ","|  ","|.,",";.,",";.,","|  ","|.,","|  ","   ","   ","   ","   ","., ","., ","___","., ","___","   ",";.,","|" ), #8
                 ("|___","___","|  ","|__",";__",";__","|  ","|__","|  ","   ","   ","   ","   ","|__","|__","|__",";__",";__","|., ","|__","|" ), #7
                 ("|   ","   ","   ","___","___","___","___","___","   ","   ","   ","   ","   ","., ","___","., ","   ","___","|__","|.,","|" ), #6
                 ("|   ","., ","   ","|  ","   ","   ","   ","|__",";  ","   ","   ","   ","   ","|.,",";.,","|.,","|  ",";__","|.,",";.,","|" ), #5
                 ("|   ","|.,","|  ","|  ","   ","   ","   ","|__",";  ","___","___","___","   ","|__","|__","|__","|  ","., ",";__",";__","|" ), #4
                 ("|   ","|.,","|  ","|  ","   ","   ","   ","|__",";  ","|.,",";.,",";.,",";.,",";.,","|  ","|.,","|  ","|__","   ","|.,","|" ), #3
                 ("|   ","|.,","|.,","|  ","   ","   ","   ","___",";  ","|__",";__",";.,",";__",";__","|  ",";.,",";__","|.,",";__",";.,","|" ), #2
                 ("|   ","|__",";__","|__","___","___","___","|.,","|  ","___","___","___","   ",";__",";__","|  ","|.,","|.,","|.,","|  ","|" ), #1  
                 ("|s__","___","___","___","___","___","___","___","___",";__","___","___","|__","___","___","___","___","___","___","___","|" )  #0
                 )

slumsLevel1Events = (
                   #0    1    2   3     4   5    6    7     8   9    10   11   12   13  14    15   16   17   18   19
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #19
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #18
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #17
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #16
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #15
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #14
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #13
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #12
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #11
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #10
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #9
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #8
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #7
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #6
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #5
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #4
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #3
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #2
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #1
                 (None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None), #0
                 )

slumEvents = [slumsLevel1Events]
allegriasDomain = dungeonmode.Dungeon("Allegria's Domain", [slumsLevel1Map], slumEvents, bgMusic=pwutilities.TAIRONAN,
        enemies=None)

def start_scene_1_episode_3(loading=False): 
    universal.say("Next Time on Pandemonium Cycle: The Potion Wars")
    music.play_music(music.THEME)
    universal.say(["Roland and Elise are getting married, and", pwutilities.name(), "is asked to escort Elise to the Lowen Monastery for the wedding. But things get a little bit complicated when an old enemy of Roland's",
    "ambushes them!"])
    universal.set_commands("Press Enter t osave")
    universal.set_command_interpreter(pwutilities.end_content_interpreter)

def end_scene_1_episode3():
        pass


def start_scene_2_episode_2(loading=False):
    universal.say("You've reached the end of the current content. Hope you've enjoyed playing it. If you have any comments or criticisms, please either post on my website spankingrpgs.com, or send me an e-mail at sprpgs@gmail.com. Once the next scene is posted, you'll be able to enjoy by loading a save from just before this scene. Thanks!", justification=0)
    universal.set_commands('Press Enter to go back to the title screen')
    universal.set_command_interpreter(pwutilities.to_title_screen_interpreter)
episode2Scene2 = episode.Scene('Episode 2 Scene 2', start_scene_2_episode_2, None)

episode3Scene1 = episode.Scene("Episode 3 Scene 1", start_scene_1_episode_3, end_scene_1_episode3)
episode3 = episode.Episode(3, 'No Good Deed', scenes=[episode3Scene1])



