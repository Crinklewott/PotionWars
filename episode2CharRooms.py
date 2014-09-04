import universal
import person
import items
import itemspotionwars
import textCommandsMusic
import townmode

ildri = None
kitchen = None
deidre = None
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
    global ildri, deidre
    try:
        ildri = universal.state.get_character('Ildri')
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
        deidre = universal.state.get_character('Deidre')
    except KeyError:
        deidre = person.Person('Deidre', person.FEMALE, None, None, ''.join(["A tall, slender woman with frizzy, shoulder-length blonde hair pulled back into a bun. She has piercing blue eyes, and",
            "carries herself with rod-straight posture. A black beret sits on top of her head."]), specialization=universal.STATUS_MAGIC, order=person.first_order, skinColor="peach", eyeColor="blue",
            hairColor="blonde", hairLength="shoulder-length", hairStyle="bun", height="tall", bodyType="slim")


       


def build_rooms():
    global kitchen
    try:
        kitchen = universal.state.get_room('Kitchen')
    except KeyError:
        kitchen = townmode.Room("Kitchen", ' '.join(["The kitchen is a rather large room with two long, waist-high counters running through the middle. Along the sides of the walls are a few small",
            "tables and",
            "stools. A pair of massive hearths sit at the far end, a pair of turnspit megapnosauri are lying next to the hearth. Their heads come up, and they gurgle happily as", 
            universal.state.player.name,
            "enters. There is a large hole in the south wall. The hole has been braced with several hastily carved timbers, and a few thick furs have been draped over it, so that",
            "customers can't peer directly into the back of the guild. A pair of high windows sit on the western wall on either side of the hearth."]), universal.state.get_room("Adventurer's Guild"),
            None, None, textCommandsMusic.LIGHT_HEARTED, None)

