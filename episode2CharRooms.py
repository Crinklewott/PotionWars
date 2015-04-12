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
import person
import items
import itemspotionwars
import textCommandsMusic
import townmode
import episode
import music

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

try:
    sofia = universal.state.get_character("Sofia.person")
except KeyError:
    sofia = person.Person("Sofia", person.FEMALE, None, None, ''.join(['''Sofia is a middle-aged Taironan woman with moderately dark skin. She is short and thin, with graying shoulder-length''',
        '''hair. She is wearing a plain cotton dress.''']))




def build_rooms():
    pass

try:
    kitchen = universal.state.get_room('Kitchen')
except KeyError:
    kitchen = townmode.Room("Kitchen", 
            ' '.join(["The kitchen is a rather large room with two long, waist-high counters running through the middle. Along the sides of the walls are a few small",
        "tables and",
        "stools. A pair of massive hearths sit at the far end, a pair of turnspit dogs are lying next to the hearth. Their heads come up, and their tails thump against the ground as the Taironan", 
        "enters. There is a large hole in the south wall. The hole has been braced with several hastily carved timbers, and a few thick furs have been draped over it, so that",
        "customers can't peer directly into the back of the guild. A pair of high windows sit on the western wall on either side of the hearth."]), [universal.state.get_room("Adventurer's Guild")],
        None, None, textCommandsMusic.LIGHT_HEARTED, "textCommandsMusic.LIGHT_HEARTED", None)

try:
    sofiasClinic = universal.state.get_room("Sofia's Clinic")
except KeyError:
    sofiasClinic = townmode.Room("Sofia's Clinic", ' '.join(["The 'clinic' is nothing more than a long, dark, low-ceilinged room crammed with piles of ragged blankets. Immersed in the piles of",
        "blankets are dozens of Taironans, all in different states of duress. Most of them are shivering quietly, or sleeping fitfully. Some are moaning, and shifting. A few are crying, and shaking",
        "violently. There is even one man who is being wrestled back into his blankets, while screaming incoherently in an unrecognizable dialect. No more than",
        "half a dozen helpers, mostly women, are moving amongst the clinic's patients."]), [], None, None, textCommandsMusic.TAIRONAN, "textCommandsMusic.TAIRONAN", 
        None)

try:
    adriansOffice = universal.state.get_room("Adrian's Office")
except KeyError:
    adriansOffice = townmode.Room("Adrian's Office", ' '.join(["A spartan place consisting only of a large desk, and several chairs. A long, whippy cane hangs on the wall above Adrian's chair.",
        "Despite being his 'office,' Adrian rarely uses it. He generally prefers to be out in the main room working behind the counter. He only uses his office when he wants to have a private",
        "conversation, typically while negotiating with clients."]), [], None, None, textCommandsMusic.LIGHT_HEARTED, "textCommandsMusic.LIGHT_HEARTED", None)

def start_scene_1_episode_3(loading=False): 
    universal.say("Next Time on Pandemonium Cycle: The Potion Wars")
    music.play_music(music.THEME)
    universal.say(["Roland and Elise are getting married, and", textCommandsMusic.name(), "is asked to escort Elise to the Lowen Monastery for the wedding. But things get a little bit complicated when an old enemy of Roland's",
    "ambushes them!"])
    universal.set_commands("Press Enter t osave")
    universal.set_command_interpreter(textCommandsMusic.end_content_interpreter)

def end_scene_1_episode3():
        pass

def start_scene_2_episode_2(loading=False):
    universal.say("You've reached the end of the current content. Hope you've enjoyed playing it. If you have any comments or criticisms, please either post on my website spankingrpgs.com, or send me an e-mail at sprpgs@gmail.com. Once the next scene is posted, you'll be able to enjoy by loading a save from just before this scene. Thanks!")
    universal.set_commands('Press Enter to go back to the title screen')
    universal.set_command_interpreter(textCommandsMusic.to_title_screen_interpreter)
episode2Scene2 = episode.Scene('Episode 2 Scene 2', start_scene_2_episode_2, None)

episode3Scene1 = episode.Scene("Episode 3 Scene 1", start_scene_1_episode_3, end_scene_1_episode3)
episode3 = episode.Episode(3, 'No Good Deed', scenes=[episode3Scene1])
