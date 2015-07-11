import itemspotionwars
import person as p 
import pwutilities
import townmode
import universal

edgeOfAvaricum = townmode.Room('Edge of Avaricum', "The road is overflowing with people, mostly merchants and farmers bringing their goods to market. Scattered amongst them is a much sadder crowd: Taironan refugees fleeing the strife of the Potion Riots. Many stumble down the road with dead eyes and ragged clothing, hunched under the weight of their children and few precious possessions. Just down the road is the city of Avaricum, the most powerful Carnutian city-state in this region of the One-Thousand-Twenty-Four. Several guards stand on either side of the road studying the people making their way into the Outer City.", bgMusic=pwutilities.VENGADOR, bgMusicName='pwutilities.VENGADOR')


#Note: The room is automatically added to the universal.state.rooms by the Room's constructor.
avaricumSquare = townmode.Room('Avaricum Square', "Avaricum Square is the center of daily life for the commoners living in Avaricum. Men and women (and even a handful of elves) of all shapes and sizes arrive from every direction and leave towards every other. Hawkers wander the crowds, shouting their wares at the top of their lungs. Corner entertainers juggle, dance to silent music, or create little sparkling butterflies with bits of magic. Children sprint around and between the legs of adults. A massive sundial dominates the center of the square.")
avaricumSquare.add_adjacent(edgeOfAvaricum)

shrine = townmode.Room('Shrine', '''Despite the size of the cathedral, the actual place of worship is tiny, no more than a shrine with with four pews, each of which could seat five people if they didn't mind being friendly. At the back of the shrine is an equallly small altar. Sitting on the center of the altar is a brightly painted wooden idol of the Mother. Behind the altar is a straight-backed, armless oaken chair. There is a sign carved into the wood of the vestibule: "Although the Avaricum Cathedral is open to all who seek help in any form, because of the small size of the shrine, only Sisters are allowed to attend the weekly worship."''', bgMusic=pwutilities.CHURCH, bgMusicName="pwutilities.CHURCH")

def shrine_before_arrival():
    if (universal.state.player.currentEpisode == episode1.name and episode.allEpisodes[universal.state.player.currentEpisode].currentSceneIndex == 0 and 
    'second_hand_tragedy' in universal.state.player.keywords):
        universal.say(universal.format_line([name(), 'has no interest in going to the Matirian Church again any time soon.']))
        return False
    elif (universal.state.player.currentEpisode == episode1.name and episode.allEpisodes[universal.state.player.currentEpisode].currentSceneIndex == 2 and 
    'finished_night_on_town' in keywords()):
        universal.say(universal.format_line([name(), '''has nothing more to do in the Shrine.''', HeShe(), '''should probably find a bed.''']), justification=0)
    else:
        return True

shrine.before_arrival = shrine_before_arrival
shrine.add_adjacent(avaricumSquare) 

orphanage = townmode.Room('Orphanage', universal.format_line(["The orphanage is a dizzying maze of twisting hallways. Children sprint through the hallways, gasping and laughing, playing hide and seek, tag, and countless other games. About a dozen Younger Brothers and Sisters in light blue, and students in light grey run after the children. In the center of the orphanage is a large dining hall. Two dozen or so children are crowded around an older woman sitting in the corner telling a story. Sitting in the center of the hall is a woman in her mid forties. She is wearing a dark red robe, which denotes her rank as a Sister of the Spectral Persuasion. She has light brown shoulder-length hair with a hint of grey, and pale skin. Her hair is pulled back into a complex braid. She is of average height, but carries herself with a level of",
                '''confidence and conviction that makes her appear taller. Crows feet spread out from her blue eyes. Her eyes flick all over the dining room, keeping an eye on the children and Younger Brothers and Sisters both. At the same time, she braids the hair of a young girl to match her own.''']), bgMusic=pwutilities.LIGHT_HEARTED, bgMusicName="pwutilities.LIGHT_HEARTED")

#orphanage.add_adjacent(shrine)

hospital = townmode.Room('Hospital', "The hospital is a busy, but somber place. People afflicted with various diseases and injuries (crookedly healed bones appearing to be the most common) sit waiting to be treated. Brothers and Sisters in white walk back and forth, some disappearing into the patient rooms in the back, others speaking with those waiting, still others handing off paperwork to each other. Sitting behind a large desk at the back of the room is a woman about Elise's age. She is wearing the light grey robes of a student, and is hunched over some parchment, her forehead wrinkled in thought.", bgMusic=pwutilities.CHURCH, bgMusicName="pwutilities.CHURCH")

#hospital.add_adjacent(shrine)
hospital.add_adjacent(orphanage)

craftmansCorridor = townmode.Room("Craftman's Corridor", '''The Craftman's Corridor is almost as bustling as the main square, though the people here tend to be better dressed. Shops line the street on both sides, but only three of them are of any interest: the Adventurer's Guild, a smithy, and a tailor. The road continues to the northeast, snakes around the base of the hill upon which the Inner City sits, and eventually leads into the slums on the far eastern side.''') 
        
avaricumSquare.add_adjacent(craftmansCorridor)

wesleyAndAnnesArmorShop = townmode.Room("Wesley and Anne's Smithy", "", bgMusic=pwutilities.PETER, bgMusicName="pwutilities.PETER") 

def update_armor_shop_description():
    wesleyAndAnnesArmorShop.description = universal.format_line(['''The shop consists of a single small room. A counter runs the length of the far wall. The shop consists of a single small room. A counter runs the length of the far wall. Hanging on the left wall are a variety of small metal things: nails, buckles, hinges, locks, horseshoes. The right side contains a few samples of larger tools: a large sickle, and a shovel. What really catches''', universal.state.player.name + "'s", '''attention is a 'suit' of chanmail hanging on the wall above the counter.''', universal.format_line(['''The armor is a two piece affair. The top looks like to be barely big enough to cover (for a sufficiently loose definition of 'cover')''', universal.state.player.name + "'s", '''breasts, while the bottom is a thong. A thong made out of chainmail.''' if universal.state.player.is_female() else '''The armor is a single, small thong, which is made out of chainmail.'''])])
def armor_shop_after_arrival():
    wesleyAndAnnesArmorShop = universal.state.get_room("Wesley and Anne's Smithy")
    wesleyAndAnnesArmorShop.description = universal.format_line(['''The shop consists of a single small room. A counter runs the length of the far wall. Hanging on the left wall are a variety of small metal things: nails, buckles, hinges, locks, horseshoes. The right side contains a few samples of larger tools: a large sickle, and a shovel. What really catches''', universal.state.player.name + "'s", '''attention is a 'suit' of chanmail hanging on the wall above the counter.''', universal.format_line(['''The armor is a two piece affair. The top looks like to be barely big enough to cover (for a sufficiently loose definition of 'cover')''', universal.state.player.name + "'s", '''breasts, while the bottom is a thong. A thong made out of chainmail.''' if universal.state.player.is_female() else '''The armor is a single, small thong, which is made out of chainmail.'''])])
    if "visited_blacksmith" not in universal.state.player.keywords:
        wesleyAndAnnesArmorShop.description = (
            universal.format_text([wesleyAndAnnesArmorShop.description, [universal.state.player.name, 
                '''stares at the piece for a few seconds, trying to process''', 
                '''just how or why anyone would ever make something so''', 
                '''patently useless out of valuable steel. Then, remembering''',
                '''a lecture given to''', himher(universal.state.player), 
                '''by Nana about trusting just''', hisher(universal.state.player), '''eyes,''', 
                heshe(universal.state.player), '''studies it with''', hisher(universal.state.player), 
                '''more magical senses.''', HisHer(universal.state.player), 
                '''eyes widen. Useless nothing, the enchantments on that armor''',
                '''make it as protective as mail, and a hundredth as''',
                '''heavy. Whoever made that was cursed good at enchanting''', 
                '''equipment.'''],
                ['''However, there is something odd about the enchantment.''', 
                '''Peering more closely,''', universal.state.player.name, '''realizes that the''', 
                '''strength of the enchantment is based on the force of a blow.''',
                '''If the force being exerted is enough to break skin,''', 
                '''bones, etc. (basically enough to trigger one's health)''', 
                '''then the enchantment springs into full force. If the''',
                '''force of the blow would only cause a little bruising, then''',
                '''the enchantment remains dormant. Basically, the magic would''',
                '''protect''', 
                universal.state.player.name, '''from a spear thrust, but not a spanking. Which''', 
                '''is unfortunate, because if Nana ever caught''', universal.state.player.name, 
                '''wearing such an absurd suit of armor, she'd put the young''',
                '''Taironan over her knee so fast it'd double as the invention''',
                '''of a new haste spell.''']]))
        wesleyAndAnnesArmorShop.description = universal.format_text([wesleyAndAnnesArmorShop.description, 
            ['''The proprietor of the shop hussles out of the backroom.''',
            '''He is also clearly the smith; he's six feet tall, and has more muscles in one arm than''', 
            universal.state.player.name, '''has in''', hisher(universal.state.player), '''entire body. He has light skin,''',
            '''short-cropped''',
            '''dark brown hair, a trimmed beard, and blue eyes. He is wearing''',
            '''a thick leather apron, and a pair of heavily patched trousers.''']])
    wesleyAndAnnesArmorShop.after_arrival = None
    townmode.town_mode()

def armor_shop_before_arrival():
    if 'flirting_with_Peter' in keywords() and universal.state.player.currentEpisode == episode1.name:
        universal.say('''Peter's shop is currently closed.''', justification=0)
        return False
    elif (('refused_to_leave_Peters_shop' in keywords() or 'insulted_Peters_kid' in keywords()) and universal.state.player.currentEpisode != episode1.name and 
        episode.allEpisodes[universal.state.player.currentEpisode].currentSceneIndex != 0):
        universal.say('''Probably wise not to go back just yet.''', justification=0)
        return False
    return True

wesleyAndAnnesArmorShop.before_arrival = armor_shop_before_arrival
wesleyAndAnnesArmorShop.after_arrival = armor_shop_after_arrival
wesleyAndAnnesArmorShop.add_adjacent(craftmansCorridor)

theresesTailors = townmode.Room("Therese's Tailors", "")

def thereses_tailors_after_arrival():
    theresesTailors = universal.state.get_room("Therese's Tailors")
    if 'visited_tailors' not in universal.state.player.keywords:
        theresesTailors.description = universal.format_text([[universal.state.player.name + "'s", '''eyes widen when''', 
            heshe(universal.state.player), '''enters the tailors.''', HeShe(universal.state.player) + "'d", 
            '''expected to find a small, mostly bare shop with a''', 
            '''couple of tailors taking custom orders, and maybe a few pieces of clothing''', 
            '''for demonstration purposes. What''', heshe(universal.state.player), '''finds instead is''',
            '''a large, open room with racks of clothing of all shapes and sizes.''', 
            '''Tunics and trousers hang on racks in the middle of the room. Dresses''',
            '''and skirts line the walls.''', universal.state.player.name, '''even notices in the back''',
            '''what appears to be a display rack for underwear of all sorts.''', 
            '''A variety of people, mostly women, move about the clothing racks.''', 
            '''They riffle through them, occasionally pulling something''', 
            '''off the shelves and holding it against themselves or their''', 
            '''companion.''', universal.state.player.name, '''also notices several people who appear to''',
            '''be workers. They move about the racks, reorganizing, and''',
            '''rehanging clothing, while keeping an eye on the various customers.''',
            '''One in particular, a woman about''', universal.state.player.name + "'s", '''age, watches''',
            universal.state.player.name, '''out of the corner of her eye.'''], 
            ['''The young woman has light brown hair pulled back into a single long''',
                '''braid, and light brown eyes. She is wearing a light red tunic''',
                '''emblazoned on the right chest with a pair of crossed needles, and''',
                '''a matching knee-length skirt.''']])
    else:
        theresesTailors.description = universal.format_line([
            '''Tunics and trousers hang on racks in the middle of the room. Dresses''',
            '''and skirts line the walls.''', universal.state.player.name, '''even notices in the back''',
            '''what appears to be a display rack for underwear of all sorts.''', 
            '''A variety of people, mostly women, move about the clothing racks.''', 
            '''They riffle through them, occasionally pulling something''', 
            '''off the shelves and holding it against themselves or their''', 
            '''companion.''', universal.state.player.name, '''also notices several people who appear to''',
            '''be workers. They move about the racks, reorganizing, and''',
            '''rehanging clothing, while keeping an eye on the various customers.''',
            '''One in particular, a woman about''', universal.state.player.name + "'s", '''age, watches''',
            universal.state.player.name, '''out of the corner of her eye.'''])
    theresesTailors.after_arrival = None
    townmode.town_mode()

theresesTailors.after_arrival = thereses_tailors_after_arrival  
theresesTailors.add_adjacent(craftmansCorridor)

slums = townmode.Room("Slums", ' '.join(['''The roads have been churned into mud by''',
        '''the steps of hundreds, perhaps even thousands, of feet. The wooden''',
        '''buildings seem''', 
        '''to sag beneath the weight of age and creeper vines. Men, women,''',
        '''and children mill about. They're dressed in worn, holey clothing''',
        '''at best, rags at worst. Most chat congenially amongst themselves''', 
        '''while repairing clothing, cleaning clothing, or cooking a meal.''', 
        '''However,''', universal.state.player.name, '''also notices more than a few women''', 
        '''wearing clothing fitted to emphasize certain bits of their anatomy.''',
        '''They chat and laugh amongst themselves, while flashing inviting''',
        '''smiles at any men that may walk by. Periodically, one of them will''',
        '''disengage from the group, and take a brief stroll.''',
        '''Beggars huddle against the crumbling buildings, crude bowls sitting''',
        '''on the ground in front of them.''']), bgMusic=pwutilities.VENGADOR, 
        bgMusicName="pwutilities.VENGADOR")

def marias_home_before_arrival():
    if not 'Marias_home' in keywords():
        universal.say(universal.format_text([['''While''', name(), '''would like to find Maria's home,''', heshe(), '''has no idea where it is.''']]), justification=0)
        return False
    elif 'grudge_against_Maria' in keywords() and universal.state.player.currentEpisode == episode1.name:
        universal.say(universal.format_text([[name(), '''has no interest in speaking to Maria right now.''']]), justification=0)
        return False
    return True


def marias_home_after_arrival():
    universal.say_title("Maria's Home")
    maria = universal.state.get_character('Maria.person')
    mariasHome = universal.state.get_room("Maria's Home")
    if mariasHome.has(maria) and universal.state.player.currentEpisode == episode1.name:
        mariasHome.description = format_text([mariasHomeDesc, ['''Maria is hunched over the small firepit, making some stew. She glances up as''', name(), 
            '''enters.''']])
    if 'boarding_with_Maria' in keywords() and universal.state.player.currentEpisode == episode1.name:
        mariasHome.description = universal.format_text([['''Maria lives in a dinky little room with barely enough room for two people to lie down comfortably. The''',
    '''floor is packed dirt, and the old wooden walls sag, seeming on the verge of collapse at any moment. A small, stone-circled firepit sits in the''',
    '''center, just below a small hole in the ceiling. A small collection of wooden bowls, plates, and  skewers lie next to the pit. A pile of ragged''',
    '''blankets is crumpled up in the corner. A few additional blankets are spread out next to the firepit.''']])
        if 'Elise_shows_you_around' in keywords():
            mariasHome.description = universal.format_text([mariasHome.description, ['''There is a small note written in the dirt. It reads:''',
    '''"Went for a walk. Your blankets are spread out next to the pit. We'll look for a better place tomorrow. Maria"''']])
        mariasHome.description = format_text([mariasHome.description, [''' If''', name(), '''wishes,''', heshe(), 
            '''can Rest, and put an end to this seemingly neverending day.''']])
    if mariasHome.boarding:
        townmode.rest_mode(mariasHome)
    else:
        townmode.town_mode()

mariasHomeDesc = universal.format_line(['''Maria lives in a dinky little room with barely enough room for two people to lie down comfortably. The''',
    '''floor is packed dirt, and the old wooden walls sag, seeming on the verge of collapse at any moment. A small, stone-circled firepit sits in the''',
    '''center, just below a small hole in the ceiling. A small collection of wooden bowls, plates, and  skewers lie next to the pit. A pile of ragged''',
    '''blankets is crumpled up in the corner.'''])
mariasHome = townmode.Bedroom("Maria's Home", description=mariasHomeDesc, bgMusic=pwutilities.TAIRONAN, bgMusicName="pwutilities.TAIRONAN", 
        before_arrival=marias_home_before_arrival, after_arrival=marias_home_after_arrival)


class AdventurersGuild(townmode.Room):
    def get_description(self):
        adventurersGuild = universal.state.get_room("Adventurer's Guild")
        if 'visited_adventurers_guild' not in universal.state.player.keywords:
            universal.state.player.add_keyword('visited_adventurers_guild')
            adventurersGuild.description = universal.format_text([['''The main room of the guild is very''',
'''large, well-lit and exceptionally clean. Chairs line the walls, while in the center are about half a dozen round tables that could sit about six''',
'''people each. About four very rough people sit at the central table. They are dirty, unkempt, and every one of them is armed. They all give''', universal.state.player.name, '''a wary look before returning to a game of craps. Each roll is accompanied by boisterous laughter and vicious swearing in half a dozen different languages.'''], 
['''At the far end of the room is a long, thick wooden counter. Standing behind the counter is an impeccably clean, immaculately''',
'''dressed, middle-aged man. He waves''', universal.state.player.name, '''forward. There is a door set into the corner of the northern wall, flush against the end of the counter.''']])
        elif universal.state.player.currentEpisode == episode1.name and 'first_dungeon_done' in keywords():
            adventurersGuild.description = universal.format_text([['''The main room is empty, save for Adrian at the back. The tables have all been split in two or more pieces, and the chairs are shattered. The''',
            '''counter at the back has been split down the middle, with both ends sloping downwards. The floor is covered in shredded, and ground up parchment.''']])
        else:
            adventurersGuild.description = universal.format_text([['''The main room of the guild is very''',
'''large, well-lit and exceptionally clean. Chairs line the walls, while in the center are about half a dozen round tables that could sit about six''',
'''people each. About four very rough people sit at the central table. They are dirty, unkempt, and every one of them is armed. They all give''', universal.state.player.name, '''a wary look before returning to a large game of dice. Each roll is accompanied by boisterous laughter and vicious swearing in half a dozen different languages.''']]) 
        return adventurersGuild.description

adventurersGuild = AdventurersGuild("Adventurer's Guild", bgMusic=pwutilities.LIGHT_HEARTED)
adventurersGuild.add_adjacent(craftmansCorridor)
infirmary = townmode.Room("Infirmary", description=universal.format_line(['''A large, open room filled with cots, and the sharp, irritating smell of poultices, alcohol,''',
'''and other medical supplies.''']), bgMusic=pwutilities.LIGHT_HEARTED, bgMusicName="pwutilities.LIGHT_HEARTED")


def ildri_or_adrian():
    adrian = universal.state.get_character('Adrian.person')
    ildri = universal.state.get_character('Ildri.person')
    return ildri if universal.state.player.is_female() else adrian
               
def guild_bedroom_before_arrival():
    if 'boarding_with_Adrian' not in keywords():
        universal.say(universal.format_text[[name(), '''isn't currently living in the Guild.''']])
        return False
    return True

def guild_bedroom_after_arrival():
    guildBedroom = universal.state.get_room('Bedroom')
    thisEpisode = episode.allEpisodes[universal.state.player.currentEpisode]  
    if universal.state.player.currentEpisode == episode1.name and thisEpisode.currentSceneIndex == 2:
        alondraSleeping = '''Alondra, the girl Vengador Ildri shielded from the city guard, is already curled up in one of the beds, soundly asleep.'''
        if not alondraSleeping  in guildBedroom.description:
            guildBedroom.description = universal.format_text([guildBedroom.description, alondraSleeping])
        if not universal.format_line(['''If''', name(), '''wishes,''', heshe(), '''can rest, and put an end to this seemingly neverending day.''']) in guildBedroom.description:
            guildBedroom.description = universal.format_text([guildBedroom.description, ['''If''', name(), '''wishes,''', heshe(), 
                '''can rest, and put an end to this seemingly neverending day.''']])
        if 'Elise_shows_you_around' in pwutilities.keywords() and universal.state.player.currentEpisode == episode1.name and not ("should go meet Elise at the Shrine" in 
                guildBedroom.description):
            guildBedroom.description = universal.format_text([guildBedroom.description, ['''If''', name(), '''hasn't already,''', p.heshe(), 
                '''should go meet Elise at the Shrine. After all,''', p.heshe(), '''shouldn't keep her waiting!''']])
    if guildBedroom.boarding:
        townmode.rest_mode(guildBedroom)
    else:
        townmode.town_mode()

guildBedroom = townmode.Bedroom("Bedroom", description=universal.format_line(['''A small, bare room containing four beds in two stacks of two. The beds are feather-beds, complete with pillows and a few blankets. Adrian's''',
'''obscene''',
    '''wealth continues to boggle the brain.''']), bgMusic=pwutilities.LIGHT_HEARTED, bgMusicName="pwutilities.LIGHT_HEARTED", 
    punisher=ildri_or_adrian, before_arrival=guild_bedroom_before_arrival, after_arrival=guild_bedroom_after_arrival)



carol = p.Person('Carol', p.FEMALE, None, None, universal.format_line(['''A woman in her''', 
        '''mid-twenties. She has light brown hair pulled back into a single''',
        '''long braid, and light brown eyes. She is wearing a light red''', 
        '''tunic''',
        '''emblazoned on the right chest with a pair of crossed needles, and''',
        '''a matching knee-length skirt.''']), printedName='Shopclerk')

carolInventory = [itemspotionwars.thong, itemspotionwars.lacyUnderwear, itemspotionwars.boyShorts, itemspotionwars.underShorts, itemspotionwars.shorts, 
    itemspotionwars.shortShorts, itemspotionwars.plainSkirt, itemspotionwars.miniSkirt, itemspotionwars.blackDress, itemspotionwars.sunDress, itemspotionwars.vNeckTunic, 
    itemspotionwars.pencilSkirt, itemspotionwars.blouse, itemspotionwars.largeShirt, itemspotionwars.pinkPajamaShirt, itemspotionwars.pinkPajamaPants, 
    itemspotionwars.bluePajamaShirt, itemspotionwars.bluePajamaPants, 
    itemspotionwars.flowerPrintShirt, itemspotionwars.blueVest, 
    itemspotionwars.flowerPrintTrousers, itemspotionwars.blueShorts, 
    itemspotionwars.flowerPrintDress, itemspotionwars.pinkDress]

carol.inventory = carolInventory
