import universal
import textCommandsMusic
import person
import items
import pwenemies
import dungeonmode
import itemspotionwars
import random
import conversation
import episode
import townmode
from episode2CharRooms import *
def start_scene_1_episode_2(loading=False):
    pass
    guild = universal.state.get_room("Adventurer's Guild")
    deidre = universal.state.get_character("Deidre.person")
    ildri = universal.state.get_character("Ildri.person")
    alondra = universal.state.get_character("Alondra.person")
    kitchen = universal.state.get_room("Kitchen")
    bedroom = universal.state.get_room("Bedroom")
    universal.state.player.restores()
    if not loading:
        textCommandsMusic.enterLeft(ildri, kitchen)
        textCommandsMusic.enterLeft(alondra, kitchen)
        textCommandsMusic.enterLeft(deidre, guild)
        textCommandsMusic.enterLeft(universal.state.player, bedroom)
    def bedroom_leaving():
        if not 'ep2LeftBedroom' in textCommandsMusic.keywords():
            universal.say( 
            universal.format_text([['''While passing Adrian's office,''', person.heshe(), '''picks up the''',
                '''sharp thwack of a paddling.''', person.HeShe(), '''hesitates, and presses''', person.hisher(), '''ear against the door.''', person.HeShe(), '''can just make out voices. Sounds like''',
                '''Paloma and Adrian.'''],
                ['''"But it was an emergency!" wails Paloma.'''],
                ['''"Please. An emergency is when someone is dying. Yours is the only coffin that was nearly occupied." A series of bangs burst from the office, and Paloma wails.'''],
                [textCommandsMusic.name(), '''winces in sympathy, but continues on to the kitchen.''']]))
            textCommandsMusic.add_keyword('ep2LeftBedroom') 
    bedroom.leaving = bedroom_leaving
    def guild_before_arrival():
        if 'hadBreakfast' in textCommandsMusic.keywords():
            return True
        else:
            universal.say(universal.format_text([[textCommandsMusic.names(), '''stomach rumbles. The succulent smell of baking bread wafts out of the nearby kitchen, making''', textCommandsMusic.names(),
            '''mouth water. Hmm. Nana always did say a proper adventurer starts every day on a full stomach.''']]))
            return False
    guild.before_arrival = guild_before_arrival

    universal.state.set_init_scene(init_episode_2_scene_1)
    init_episode_2_scene_1()
    universal.state.player.litany = conversation.allNodes[327]
    conversation.converse_with(universal.state.player, townmode.town_mode)
    universal.state.get_character("Ildri.person").litany = conversation.allNodes[332]
def init_episode_2_scene_1():
    ep2_wakeup = conversation.Node(327)
    def ep2_wakeup_quip_function():

        
        ep2_wakeup.quip = universal.format_text_translate([['''''']])
        ep2_wakeup.children = []
        ep2_wakeup.playerComments = []

        if "boarding_with_Adrian" in textCommandsMusic.keywords():
            ep2_wakeup.children = ep2_guild_wake_up.children
            conversation.say_node(ep2_guild_wake_up.index)
        elif "boarding_with_Maria" in textCommandsMusic.keywords():
            ep2_wakeup.children = ep2_marias_wake_up.children
            conversation.say_node(ep2_marias_wake_up.index)

    ep2_wakeup.quip_function = ep2_wakeup_quip_function
    ep2_guild_wake_up = conversation.Node(328)
    def ep2_guild_wake_up_quip_function():

        townmode.go(universal.state.get_room("Bedroom"), sayDescription=False)
        
        
        
        ep2_guild_wake_up.quip = universal.format_text_translate([['''''']])
        ep2_guild_wake_up.children = []
        ep2_guild_wake_up.playerComments = []

        if "extrovert" in textCommandsMusic.keywords():
            ep2_guild_wake_up.children = ep2_guild_wake_up_extrovert.children
            conversation.say_node(ep2_guild_wake_up_extrovert.index)
        elif True:
            ep2_guild_wake_up.children = ep2_guild_wake_up_introvert.children
            conversation.say_node(ep2_guild_wake_up_introvert.index)

    ep2_guild_wake_up.quip_function = ep2_guild_wake_up_quip_function
    ep2_guild_wake_up_extrovert = conversation.Node(329)
    def ep2_guild_wake_up_extrovert_quip_function():

        universal.state.player.receives_damage(1)
        
        
        
        ep2_guild_wake_up_extrovert.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' groans, and rubs ''', person.hisher(), ''' throbbing forehead. ''', person.HeShe(), ''' rolls onto ''', person.hisher(), ''' side, and slowly cracks an eye open. ''', person.HisHer(), ''' headache spikes as a bit of early morning sunlight strikes ''', person.hisher(), ''' eyes. ''', person.HeShe(), ''' starts to pull the blanket over ''', person.hisher(), ''' head, but then ''', person.hisher(), ''' stomach heaves. ''', person.HeShe(), ''' frantically rolls off the side of the bed, and lunges for a nearby bucket.'''],
['\n\n' + '''Alas, ''', person.heshe(), ''' is not quite fast enough.'''],
['\n\n' + '''Stupid Carrie, and her stupid "Let's party tonight!"'''],
['\n\n' + '''Then, ''', universal.state.player.name, ''' feels a surge of energy, and the headache, nausea, and general bleariness vanish. ''', person.HeShe(), ''' winces. Hungover enough to trigger ''', person.hisher(), ''' health? Good thing Nana isn't around.'''],
['\n\n' + universal.state.player.name, ''' crawls towards a nearby bucket of water (which ''', person.heshe(), ''' kept for just such emergencies) and a worn rag, and starts cleaning.''']])
        ep2_guild_wake_up_extrovert.children = [ep2_ventilate, ep2_extrovert_to_kitchen]
        ep2_guild_wake_up_extrovert.playerComments = ['''Remember to open the windows in an effort to ventilate the place.''','''Forget to open the windows.''']

        

    ep2_guild_wake_up_extrovert.quip_function = ep2_guild_wake_up_extrovert_quip_function
    ep2_ventilate = conversation.Node(330)
    def ep2_ventilate_quip_function():

        
        ep2_ventilate.quip = universal.format_text_translate([['\n\n' + '''But first, ''', person.heshe(), ''' opens the window in an effort to ventilate the place a little. ''', person.HeShe(), ''' breaths in the cool spring air wafting in through the window, silently grateful for the charms Airell's placed on the windows of the guild to keep thieves out. Then, ''', person.heshe(), ''' gets to work.''']])
        ep2_ventilate.children = []
        ep2_ventilate.playerComments = []

        ep2_ventilate.children = ep2_extrovert_to_kitchen.children
        conversation.say_node(ep2_extrovert_to_kitchen.index)

    ep2_ventilate.quip_function = ep2_ventilate_quip_function
    ep2_extrovert_to_kitchen = conversation.Node(331)
    def ep2_extrovert_to_kitchen_quip_function():

        ep2_extrovert_to_kitchen.quip = universal.format_text_translate([['\n\n' + '''Having finished cleaning up after ''', person.himselfherself(), ''', ''', universal.state.player.name, ''' gets changed. Perhaps the kitchen for some breakfast? Or ''', person.heshe(), ''' could always wander about town, and see what people are up to.''']])
        ep2_extrovert_to_kitchen.children = []
        ep2_extrovert_to_kitchen.playerComments = []

        

    ep2_extrovert_to_kitchen.quip_function = ep2_extrovert_to_kitchen_quip_function
    ep2_talk_to_Ildri = conversation.Node(332)
    def ep2_talk_to_Ildri_quip_function():

        
        ep2_talk_to_Ildri.quip = universal.format_text_translate([['''''']])
        ep2_talk_to_Ildri.children = []
        ep2_talk_to_Ildri.playerComments = []

        if 'extrovert' in textCommandsMusic.keywords():
            ep2_talk_to_Ildri.children = ep2_talk_to_Ildri_extrovert.children
            conversation.say_node(ep2_talk_to_Ildri_extrovert.index)
        elif True:
            ep2_talk_to_Ildri.children = ep2_talk_to_Ildri_introvert.children
            conversation.say_node(ep2_talk_to_Ildri_introvert.index)

    ep2_talk_to_Ildri.quip_function = ep2_talk_to_Ildri_quip_function
    ep2_talk_to_Ildri_extrovert = conversation.Node(333)
    def ep2_talk_to_Ildri_extrovert_quip_function():

        ep2_talk_to_Ildri_extrovert.quip = universal.format_text_translate([['\n\n' + '''Ildri and Alondra are standing at the counter, kneading several piles of dough. Ildri glances over her shoulder at ''', universal.state.player.name, '''. She wipes her hands on her apron, then turns and puts them on her hips. "Well, well. Look whose finally up. Late to bed, late to rise hmm?"'''],
['\n\n' + universal.state.player.name, ''' winces. "I didn't wake you when I got home, did I?"'''],
['\n\n' + '''"Oh, you'd have known if you'd woken me, trust me," says Ildri. She flashes ''', universal.state.player.name, ''' a smile, then glances over her shoulder at Alondra, who is starting to move her dough onto a baking pan.''']])
        ep2_talk_to_Ildri_extrovert.children = []
        ep2_talk_to_Ildri_extrovert.playerComments = []

        ep2_talk_to_Ildri_extrovert.children = ep2_guild_wake_up_extrovert_continue.children
        conversation.say_node(ep2_guild_wake_up_extrovert_continue.index)

    ep2_talk_to_Ildri_extrovert.quip_function = ep2_talk_to_Ildri_extrovert_quip_function
    ep2_guild_wake_up_extrovert_continue = conversation.Node(334)
    def ep2_guild_wake_up_extrovert_continue_quip_function():

        
        ep2_guild_wake_up_extrovert_continue.quip = universal.format_text_translate([['\n\n' + '''She gasps, and spins to face Alondra. "What are you doing, girl? You put that in the oven, half the loaf will be burned, and the other hardly cooked."'''],
['\n\n' + '''Alondra eeps, and quickly pulls the bread off the sheet. "Sorry, sorry. I just, you're so fast-"'''],
['\n\n' + '''"Of course I'm fast," says Ildri. "I've been doing this since before you were born. Now, do it right. I'd rather one good loaf from you than half a dozen bad."'''],
['\n\n' + '''"Yes ma'am, sorry ma'am," says Alondra quickly, her face turning red.'''],
['\n\n' + '''Ildri pats Alondra on the shoulder. "Ah, don't worry about it. Spot-checking is why I'm here."'''],
['\n\n' + '''"Erm, breakfast?" asks ''', universal.state.player.name, '''.'''],
['\n\n' + '''Ildri jerks her head towards a small platter on the far end of the counter. "Some biscuits and fiddleheads, and a bit of old iguanodon jerky. Also a pitcher of water, sanitized by Paloma before her meeting with Adrian."'''],
['\n\n' + universal.state.player.name, ''' starts to nod, then stops and clutches ''', person.hisher(), ''' head.'''],
['\n\n' + '''"Ohh, you'd better not throw up in my kitchen," says Ildri, her eyes narrowing.'''],
['\n\n' + '''"You didn't throw up in our room again, did you?" asks Alondra sharply.'''],
['\n\n' + '''"I cleaned up after myself," mutters ''', universal.state.player.name, ''' defensively.'''],
['\n\n' + '''Alondra throws her hands into the air. "Dios de la Madre! Did you at least remember to open the door and window, so the wretched room could air out a little?"'''],
['\n\n' + universal.state.player.name, ''' winces. "Not so loud."'''],
['\n\n' + '''"Answer the cursed question," says Alondra, putting her hands on her hips.''']])
        ep2_guild_wake_up_extrovert_continue.children = []
        ep2_guild_wake_up_extrovert_continue.playerComments = []

        if 'ventilatedRoom' in textCommandsMusic.keywords():
            ep2_guild_wake_up_extrovert_continue.children = ep2_ventilated_room.children
            conversation.say_node(ep2_ventilated_room.index)
        elif True:
            ep2_guild_wake_up_extrovert_continue.children = ep2_forgot_to_ventilate_room.children
            conversation.say_node(ep2_forgot_to_ventilate_room.index)

    ep2_guild_wake_up_extrovert_continue.quip_function = ep2_guild_wake_up_extrovert_continue_quip_function
    ep2_ventilated_room = conversation.Node(335)
    def ep2_ventilated_room_quip_function():

        
        
        ep2_ventilated_room.quip = universal.format_text_translate([['\n\n' + '''"Yes, I did," says ''', universal.state.player.name, ''' irritably. "Because I clean up my messes, thank you very much. Now let me eat in peace."'''],
['\n\n' + '''Alondra's lips twist. "How can you afford to drink like that anyway? Weren't you complaining the other day about how broke you are? Maybe you wouldn't be so cursed poor if you weren't throwing all your coins at supersaur piss."'''],
['\n\n' + '''"Leave the ''', person.manwoman(), ''' be," says Ildri. "How ''', person.heshe(), ''' spends ''', person.hisher(), ''' money is ''', person.hisher(), ''' business."'''],
['\n\n' + '''"Not when it affects my living space," mutters Alondra.'''],
['\n\n' + universal.state.player.name, ''' rolls ''', person.hisher(), ''' eyes, and stuffs a biscuit into ''', person.hisher(), ''' mouth. "Oh come on. Even smelling faintly of vomit, it's an improvement over your old home, I'm sure."'''],
['\n\n' + '''For a moment, Alondra looks annoyed. Then she shrugs, and smiles sardonically. "That's true, I guess. Wouldn't put up with Ildri and her spatula otherwise."'''],
['\n\n' + '''Ildri raises an eyebrow, but doesn't say anything as she pulls another handful of dough out of a massive bowl on the counter.''']])
        ep2_ventilated_room.children = []
        ep2_ventilated_room.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_ventilated_room.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_ventilated_room.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_ventilated_room.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_ventilated_room.quip_function = ep2_ventilated_room_quip_function
    ep2_forgot_to_ventilate_room = conversation.Node(336)
    def ep2_forgot_to_ventilate_room_quip_function():

        
        ep2_forgot_to_ventilate_room.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' smiles uneasily. "Heh heh heh. Oops?"'''],
['\n\n' + '''Alondra's jaw clenches. ''', universal.state.player.name, ''' is pretty sure ''', person.heshe(), ''' can hear the other Taironan's teeth grind together. "Ildri, may I be excused for about a quarter-glass? I need to explain proper roommate etiquette to my roommate."'''],
['\n\n' + '''Ildri glances at the bread dough laid out on the counter. "Well, I guess I could spare you for a few minutes. But don't take too long."'''],
['\n\n' + '''"Wouldn't dream of it," says Alondra. She grabs ''', universal.state.player.name, "'s", ''' arm. "Come along, you."''']])
        ep2_forgot_to_ventilate_room.children = [ep2_ventilate_meek, ep2_ventilate_resist]
        ep2_forgot_to_ventilate_room.playerComments = ['''Follow meekly.''','''Resist mightily.''']

        

    ep2_forgot_to_ventilate_room.quip_function = ep2_forgot_to_ventilate_room_quip_function
    ep2_ventilate_meek = conversation.Node(337)
    def ep2_ventilate_meek_quip_function():

        
        
        ep2_ventilate_meek.quip = universal.format_text_translate([['\n\n' + '''"I'm sorry," says ''', universal.state.player.name, ''' quietly, as Alondra pulls ''', person.himher(), ''' back towards their room. "I just forgot."'''],
['\n\n' + '''"Perfectly understandable," says Alondra. "All the more reason to give you a little incentive to remember."''']])
        ep2_ventilate_meek.children = [ep2_ventilate_backrub, ep2_ventilate_maam, ep2_ventilate_but]
        ep2_ventilate_meek.playerComments = ['''"Like a backrub whenever I remember?"''','''"Yes ma'am."''','''"But...but..."''']

        

    ep2_ventilate_meek.quip_function = ep2_ventilate_meek_quip_function
    ep2_ventilate_backrub = conversation.Node(338)
    def ep2_ventilate_backrub_quip_function():

        ep2_ventilate_backrub.quip = universal.format_text_translate([['\n\n' + '''''', universal.format_line(['''Alondra pauses outside their door. She glances back at ''', universal.state.player.name, ''', a small smile tugging at her lips. "Not what I had in mind, but I'll think about it. Nothing wrong with using the carrot and the stick."''']) if universal.state.player.is_female() else universal.format_line(['''"No."''']), '''''']])
        ep2_ventilate_backrub.children = []
        ep2_ventilate_backrub.playerComments = []

        ep2_ventilate_backrub.children = ep2_ventilate_meek_enter_room.children
        conversation.say_node(ep2_ventilate_meek_enter_room.index)

    ep2_ventilate_backrub.quip_function = ep2_ventilate_backrub_quip_function
    ep2_ventilate_meek_enter_room = conversation.Node(339)
    def ep2_ventilate_meek_enter_room_quip_function():

        
        ep2_ventilate_meek_enter_room.quip = universal.format_text_translate([['\n\n' + '''Alondra pushes the door open. She reels backward. "Amor de la Madre, it smells awful in here."'''],
['\n\n' + universal.state.player.name, ''' sniffs. "I don't think it smells that bad."'''],
['\n\n' + '''"Open the cursed window," says Alondra, pushing ''', universal.state.player.name, ''' towards the window.'''],
['\n\n' + universal.state.player.name, ''' hurries over and unlatches the window, then pushes it open. A cool spring breeze wafts into the room and spreads throughout the room. ''', universal.state.player.name, ''' takes a deep breath of the fresh air. ''', universal.state.player.name, ''' grimaces. Now ''', person.heshe(), ''' thinks city air is fresh. So maybe it did smell that bad.'''],
['\n\n' + person.HeShe(), ''' turns back around, to see Alondra sitting on the edge of her bed, a large bone hairbrush in her right hand. ''', universal.state.player.name, ''' starts gnawing on ''', person.hisher(), ''' lower lip. "Come on Ali-"'''],
['\n\n' + '''"Do you remember what I said the last time you forgot to air out the room?" asks Alondra sharply.'''],
['\n\n' + '''"You said you'd paddle me with your hairbrush if I forgot again," says ''', universal.state.player.name, ''' quietly, fiddling anxiously with ''', universal.format_line(['''a lock of hair''']) if universal.state.player.long_hair() else universal.format_line(['''a loose thread in ''', person.hisher(), ''' ''', universal.state.player.shirt().name, '''''']), '''.'''],
['\n\n' + '''"And what did you do?" Alondra begins to lightly tap the hairbrush against her thigh.'''],
['\n\n' + '''"I forgot to air out our room," mumbles ''', universal.state.player.name, ''', looking down at ''', person.hisher(), ''' shifting feet.'''],
['\n\n' + '''"So what do you think is going to happen now?" asks Alondra.'''],
['\n\n' + '''"You're going to paddle me," says ''', universal.state.player.name, ''' softly, ''', person.hisher(), ''' bottom clenching anxiously.'''],
['\n\n' + '''"What was that? I couldn't hear you."'''],
['\n\n' + '''"You're going to paddle me," says ''', universal.state.player.name, ''' in a louder voice.'''],
['\n\n' + '''"But I can't do that if you're over there, now can I?"'''],
['\n\n' + '''"No."'''],
['\n\n' + '''"Then maybe you should come over here."'''],
['\n\n' + universal.state.player.name, ''' bites down on ''', person.hisher(), ''' lip, and gives Alondra a pleading look. "I really am sorry."'''],
['\n\n' + '''Alondra's face is still as stone. "Young ''', person.manlady(), ''', you will not like it if I have to bring you over here. Now come here, and turn yourself over my knee."'''],
['\n\n' + universal.state.player.name, ''' swallows. ''', universal.format_line(['''Alondra is (at least relative to ''', universal.state.player.name, ''') plenty big as it is. Her stern disappointment only seems to make her bigger.''']) if not universal.state.player.is_taller_than(alondra) else universal.format_line(['''Despite ''', person.hisher(), ''' greater height, ''', universal.state.player.name, ''' can't help but feel small and ashamed before Alondra's stern disappointment.''']), ''' With uneasy steps, ''', person.heshe(), ''' approaches Alondra, then bends over her lap, resting ''', person.hisher(), ''' torso and legs on the edge of the bed''', universal.format_line([''', ''', person.hisher(), ''' long legs dangling over the end of the bed.''']) if universal.state.player.is_tall_or_taller() else universal.format_line(['''.''']), ''' Alondra shifts backward a few inches, and pulls ''', universal.state.player.name, ''' more fully onto the bed.'''],
['\n\n' + universal.format_line(['''Herp derp. Then, she grabs the waistband of ''', universal.state.player.name, "'s", ''' ''', universal.state.player.pajama_bottom().name, ''' and pushes them down to ''', universal.state.player.name, "'s", ''' knees, exposing ''', person.hisher(), ''' ''', universal.state.player.bum_adj(), ''', ''', universal.state.player.muscle_adj(), ''', bare bottom.''']) if universal.state.player.pajama_bottom().armorType == items.PajamaPants.armorType else universal.format_line(['''''']), ''''''],
[universal.format_line(['''Then, she undoes the little bone buttons holding up ''', universal.state.player.name, "'s", ''' drop seat, and flips it back, exposing ''', universal.state.player.name, "'s", ''' ''', universal.state.player.bum_adj(), ''', ''', universal.state.player.muscle_adj(), ''', bare bottom.''']) if universal.state.player.pajama_bottom().armorType == items.DropSeatPajamas.armorType else universal.format_line(['''Then, she grabs the hem of ''', universal.state.player.name, "'s", ''' ''', universal.state.player.pajama_top().name, ''', and pushes it up over ''', universal.state.player.name, "'s", ''' hips, exposing ''', person.hisher(), ''' exposing ''', universal.state.player.name, "'s", ''' ''', universal.state.player.bum_adj(), ''', ''', universal.state.player.muscle_adj(), ''', bare bottom.''']), ''''''],
['\n\n' + universal.state.player.name, ''' gnaws anxiously on a fingernail, as a cool spring breeze wafts across ''', person.hisher(), ''' bare cheeks. "Does it have to be-"'''],
['\n\n' + '''"Spankings are most effective on the bare," says Alondra matter-of-factly. "And I intend to make this as effective as possible."'''],
['\n\n' + universal.state.player.name, ''' squirms nervously. "Don't spank too hard, OK?"'''],
['\n\n' + '''"I'll spank as hard as I need to," says Alondra. ''', universal.format_line(['''She gives ''', universal.state.player.name, "'s", ''' bottom a comforting rub. "And no harder."''']) if universal.state.player.is_female() else universal.format_line(['''''']), ''''''],
['\n\n' + '''Then, an oval of cool bone taps lightly against ''', universal.state.player.name, "'s", ''' ''', universal.state.player.muscle_adj(), ''' right cheek. ''', person.HisHer(), ''' toes curl, and ''', person.hisher(), ''' fingers dig into Alondra's blanket. ''', person.HeShe(), ''' buries ''', person.hisher(), ''' face in ''', person.hisher(), ''' forearm, and waits for the first blow to descend.'''],
['\n\n' + '''Thwack!'''],
['\n\n' + '''The heavy bone impacts ''', universal.state.player.name, "'s", ''' right cheek with a deep, fierce sting. ''', universal.state.player.name, "'s", ''' feet twitch, and ''', person.hisher(), ''' fingers tighten their grip on Alondra's blanket. Then, the hairbrush cracks against ''', universal.state.player.name, "'s", ''' left cheek. Then the hairbrush wallops ''', universal.state.player.name, "'s", ''' right cheek, just below the first strike. Then a fourth blow lands just above the second. ''', universal.state.player.name, ''' bites down on ''', person.hisher(), ''' lower lip, and whimpers at the building sting.'''],
['\n\n' + '''Alondra lands a rapid one-two-three-four to ''', universal.state.player.name, "'s", ''' vulnerable, sensitive, ''', universal.state.player.muscle_adj(), ''' cheeks. ''', universal.state.player.name, ''' whines, and rocks ''', person.hisher(), ''' body. ''', person.HisHer(), ''' legs slide across the bedspread, while ''', person.hisher(), ''' hips wiggle across Alondra's strong thighs. ''', person.HeShe(), ''' laces ''', person.hisher(), ''' fingers through ''', person.hisher(), ''' hair, and tugs lightly on ''', person.hisher(), ''' own hair in a desperate attempt to find something, anything to distract ''', person.himselfherself(), ''' from the building heat in ''', person.hisher(), ''' poor cheeks. Another half a dozen descend upon ''', person.hisher(), ''' exposed, ''', universal.state.player.bum_adj(), ''', ''', universal.state.player.quivering(), ''' cheeks. ''', universal.state.player.name, ''' squirms and whines through every one, but manages to keep ''', person.himselfherself(), ''' largely in control. There is a small pause, and ''', universal.state.player.name, ''' takes a deep breath. Maybe ''', person.heshe(), ''' can-'''],
['\n\n' + '''The hairbrush collides with ''', universal.state.player.name, "'s", ''' left sit-spot.'''],
['\n\n' + universal.state.player.name, ''' throws ''', person.hisher(), ''' head into the air and howls. ''', person.HisHer(), ''' feet lance up, and press as close to ''', person.hisher(), ''' bottom as they can get.'''],
['\n\n' + '''"Put your feet down," says Alondra, pushing ''', universal.state.player.name, "'s", ''' feet back onto the bed. "And control yourself."'''],
['\n\n' + '''"You're hitting me with a hunk of bone," cries ''', universal.state.player.name, '''. "How can you expect me to control myself?"'''],
['\n\n' + '''The hairbrush smacks ''', universal.state.player.name, "'s", ''' right sitspot, and once more, a howl bursts from ''', universal.state.player.name, "'s", ''' lips, while ''', person.hisher(), ''' legs jump up to shield ''', person.hisher(), ''' bottom.'''],
['\n\n' + '''"I said keep your feet down," says Alondra, pushing ''', universal.state.player.name, "'s", ''' feet back onto the bed. She leans forward slightly, and resumes attacking the swell of ''', universal.state.player.name, "'s", ''' bottom. However, with almost every blow, ''', universal.state.player.name, "'s", ''' feet are back up, blocking the path of the hairbrush.'''],
['\n\n' + '''Alondra growls in frustration. She shifts a little, so that she is sitting at an angle relative to the bed. She yanks ''', universal.state.player.name, "'s", ''' torso forward, and shoves ''', person.hisher(), ''' legs off the bed. Then, Alondra hikes up her own skirt to give herself some flexibility, and hooks her leg around ''', universal.state.player.name, "'s", '''. She then resumes the paddling with gusto.'''],
['\n\n' + universal.state.player.name, ''' begins to buck and flail beneath the heavy, rapid blows. ''', person.HeShe(), ''' pounds ''', person.hisher(), ''' fists into the bed, and drums ''', person.hisher(), ''' toes against the floor. ''', universal.format_line(['''Thanks to ''', universal.state.player.name, "'s", ''' greater size and strength, Alondra has a terrible time holding ''', person.himher(), ''' down. After practically every blow, Alondra has to readjust her grip, and rewrap her leg around ''', universal.state.player.name, "'s", '''. She continues gamely on, however, her hairbrush only barely slowing, and soon ''', universal.state.player.name, ''' stops struggling and meekly takes the spanking.''']) if universal.state.player.taller_than(alondra) else universal.format_line(['''''']), ''''''],
['''''', universal.format_line(['''Despite ''', person.hisher(), ''' carrying on, Alondra easily holds ''', universal.state.player.name, ''' securely pinned, and the cadence of her blows is completely unaffected by ''', universal.state.player.name, "'s", ''' flailing.''']) if alondra.taller_than(universal.state.player) else universal.format_line(['''Though the two are the same size, ''', universal.state.player.name, ''' has the slight edge in raw strength. As such, ''', universal.state.player.name, ''' periodically manages to flail half out of Alondra's grip, forcing the young woman to readjust her grip every few blows. The Taironan continues gamely on, and soon ''', universal.state.player.name, ''' stops struggling, and meekly takes the rest of the spanking.''']), ''''''],
['\n\n' + '''Alondra takes a deep breath, and sets the brush down on the bed. She rests her hand lightly on ''', universal.state.player.name, "'s", ''' blazing bottom. "Do you think I like living someplace that smells like a sick room?"'''],
['\n\n' + universal.state.player.name, ''' buries ''', person.hisher(), ''' face into the bed, and sobs wretchedly.'''],
['\n\n' + '''"''', universal.state.player.nickname, ''', answer my question," says Alondra.'''],
['\n\n' + '''"No," mumbles ''', universal.state.player.name, ''' against the bed.'''],
['\n\n' + '''"No what?"'''],
['\n\n' + '''"No you don't like living in a sick room," says ''', universal.state.player.name, ''', rubbing ''', person.hisher(), ''' face against Alondra's sheets.'''],
['\n\n' + '''"Do you think I like living with someone who comes fumbling in, in the deepest, most godless hours of the night cursing and groaning, and thumping around before finally going to sleep?" asks Alondra, as she slowly rubs away some of the sting in ''', universal.state.player.name, "'s", ''' bottom.'''],
['\n\n' + '''"No." ''', universal.state.player.name, ''' takes a few deep breaths, and struggles to get ''', person.himselfherself(), ''' under control.'''],
['\n\n' + '''"Then why do you keep doing it?"'''],
['\n\n' + '''"I don't mean to," whines ''', universal.state.player.name, '''. "Just, Carrie and I lose track of time and-"'''],
['\n\n' + '''"So should I come and get you?" asks Alondra softly. "Shall I show up at the bar, and tell everyone that you need to come home, because it's your bedtime?"'''],
['\n\n' + universal.state.player.name, "'s", ''' eyes widen. "You wouldn't. I'm not a child."'''],
['\n\n' + '''"You have a choice. Either you decide to come home at a reasonable hour, you stay sober enough so that you can enter quietly, you spend the night with your friend Carrie, or I treat you like a child, with bedtime and everything." says Alondra.'''],
['\n\n' + universal.state.player.name, ''' gnaws uneasily on ''', person.hisher(), ''' lip. "This whole curfew thing, would I get spanked when you come and get me?"'''],
['\n\n' + '''"Only if you lie about where you'lll be drinking, or you kick up a fuss when it's time to go," says Alondra.'''],
['\n\n' + '''Hmm. On the one hand, a curfew would be exceptionally embarassing. On the other, knowing Carrie, ''', universal.state.player.name, ''' would probably wind up getting home super late and plenty drunk most of the time, and the thought of starting each such morning with a splitting headache, and a throbbing bottom is not particularly appealing. To say nothing of the disservice ''', person.heshe(), ''''d be paying to Alondra. Plus, even after she becomes a sister, Carrie has no plans of moving out of the Church dormitories, and the Church tends to frown on students (and Sisters) bringing people home without prior approval.''']])
        ep2_ventilate_meek_enter_room.children = [ep2_alondra_curfew, ep2_alondra_no_curfew]
        ep2_ventilate_meek_enter_room.playerComments = ['''"Erm, let's go for the curfew."''','''"I'll try not to disturb you, I promise."''']

        

    ep2_ventilate_meek_enter_room.quip_function = ep2_ventilate_meek_enter_room_quip_function
    ep2_alondra_curfew = conversation.Node(340)
    def ep2_alondra_curfew_quip_function():

        
        
        
        ep2_alondra_curfew.quip = universal.format_text_translate([['\n\n' + '''"That's rather unexpected, but OK," says Alondra. "Curfew it is then. I should warn you though, you make a fuss when I come to collect you, I will spank you right then and there, in front of La Madre and everybody. Understand?"'''],
['\n\n' + '''"Yes," says ''', universal.state.player.name, ''' uneasily. "I kind of figured as much."'''],
['\n\n' + '''"Good."''']])
        ep2_alondra_curfew.children = []
        ep2_alondra_curfew.playerComments = []

        if universal.state.player.is_female():
            ep2_alondra_curfew.children = ep2_alondra_rub.children
            conversation.say_node(ep2_alondra_rub.index)
        elif True:
            ep2_alondra_curfew.children = ep2_alondra_spanking_done.children
            conversation.say_node(ep2_alondra_spanking_done.index)

    ep2_alondra_curfew.quip_function = ep2_alondra_curfew_quip_function
    ep2_alondra_rub = conversation.Node(341)
    def ep2_alondra_rub_quip_function():

        
        
        ep2_alondra_rub.quip = universal.format_text_translate([['\n\n' + '''Silence settles over the two, except for ''', universal.state.player.name, "'s", ''' occasional sniffling. Alondra begins to gently rub ''', universal.state.player.name, "'s", ''' blazing bottom, her warm, callused, yet soothing hands easing away the sting.''']])
        ep2_alondra_rub.children = [ep2_alondra_rubbing_attracted, ep2_alondra_rubbing_not_attracted, ep2_alondra_rubbing_denied]
        ep2_alondra_rub.playerComments = ['''React with a spike of attraction.''','''Enjoy the rubbing, but don't feel attracted to Alondra.''','''Rudely tell her to stop, and get up.''']

        

    ep2_alondra_rub.quip_function = ep2_alondra_rub_quip_function
    ep2_alondra_rubbing_attracted = conversation.Node(342)
    def ep2_alondra_rubbing_attracted_quip_function():

        
        
        ep2_alondra_rubbing_attracted.quip = universal.format_text_translate([['\n\n' + '''A ''', universal.format_line(['''strange''']) if 'lesbian_in_denial' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''' tingle races across ''', universal.state.player.name, "'s", ''' skin, starting at the quivering flesh beneath Alondra's gentle fingertips, and ending a few inches further down, nestling happily between ''', universal.state.player.name, "'s", ''' legs. Suddenly, ''', person.heshe(), ''' becomes acutely conscious of the warm, strong, bare leg wrapped around ''', person.hisher(), ''' thighs, holding ''', person.himher(), ''' pinned with a strange, firm gentleness. ''', person.HeShe(), ''' can feel a soothing warmth radiating from the leg pressed against ''', universal.state.player.name, "'s", ''' lower belly, Alondra's skirt hiked up so far by the awkward position, that if ''', universal.state.player.name, ''' shifts a little, ''', person.heshe(), ''' can feel ''', person.hisher(), ''' belly rub against Alondra's upper thigh.'''],
['\n\n' + '''Alondra's right hand begin to gently knead ''', universal.state.player.name, "'s", ''' exposed bum, while her left hand rubs slow circles on the small of ''', universal.state.player.name, "'s", ''' back.'''],
['\n\n' + '''"I'm sorry that I had to spank you like that," says Alondra quietly. "I wanted it to be over just as badly as you did."'''],
['\n\n' + '''"You know, you didn't have to spank me," says ''', universal.state.player.name, ''', ''', person.hisher(), ''' hips shifting a little bit beneath Alondra's soothing massage.'''],
['\n\n' + '''"Hah! We've tried that for the past month! And how many times did you listen to my requests to not come barelling through here like a drunken sauropod in the middle of the night?"'''],
['\n\n' + '''"Most nights," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Don't get cheeky with me," says Alondra, lightly slapping ''', universal.state.player.name, "'s", ''' right cheek. "How many times on the nights when you actaully went out?"'''],
['\n\n' + '''"I dunno," mutters ''', universal.state.player.name, ''', wiggling ''', person.hisher(), ''' hips. "They all kinda ran together."'''],
['\n\n' + '''"Hmm. I'm sure," says Alondra, her voice trailing off. She begins rubbing small, but ever widening circles across ''', universal.state.player.name, "'s", ''' hot globes. "Does that feel better?"'''],
['\n\n' + '''"Yes," says ''', universal.state.player.name, ''', pushing ''', person.hisher(), ''' hips up into Alondra's hand, ''', person.hisher(), ''' lower stomach tightening. "Much better."'''],
['\n\n' + '''"I just want us to get along, you know?" says Alondra. "I want our disagreements to be out in the open, as exposed as your ''', universal.format_line(['''cute little''']) if ((universal.state.player.bodyType == 'slim' and universal.state.player.is_average_or_shorter()) or (universal.state.player.bodyType == 'average' and universal.state.player.is_average_or_shorter()) or (universal.state.player.bodyType == 'average' and universal.state.player.is_short_or_shorter())) else universal.format_line(['''bouncy''']), ''' bottom, and dealt with directly."''']])
        ep2_alondra_rubbing_attracted.children = []
        ep2_alondra_rubbing_attracted.playerComments = []

        if 'lesbian_in_denial' in textCommandsMusic.keywords():
            ep2_alondra_rubbing_attracted.children = ep2_alondra_rubbing_attracted_denial.children
            conversation.say_node(ep2_alondra_rubbing_attracted_denial.index)
        elif True:
            ep2_alondra_rubbing_attracted.children = ep2_alondra_rubbing_attracted_acceptance.children
            conversation.say_node(ep2_alondra_rubbing_attracted_acceptance.index)

    ep2_alondra_rubbing_attracted.quip_function = ep2_alondra_rubbing_attracted_quip_function
    ep2_alondra_rubbing_attracted_denial = conversation.Node(343)
    def ep2_alondra_rubbing_attracted_denial_quip_function():

        
        
        ep2_alondra_rubbing_attracted_denial.quip = universal.format_text_translate([['\n\n' + '''"You know, I think we should probably get going," says ''', universal.state.player.name, ''' quickly. ''', person.HeShe(), ''' scrambles off of Alondra's lap, and ''', items.lowerslifts(universal.state.player.lower_clothing()), ''' ''', person.hisher(), ''' ''', universal.state.player.pajama_bottom().name, ''' back over ''', person.hisher(), ''' sore bottom. ''', person.HeShe(), ''' laughs uneasily. "Lots to do, you know?"'''],
['\n\n' + '''"Well, alright," says Alondra, a bit of disappointment in her voice. She stands, and gives ''', universal.state.player.name, ''' an awkward smile. "After you?"'''],
['\n\n' + '''"Umm, sure," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''The two make their way back to the kitchen, and ''', universal.state.player.name, ''' dives into the breakfast laid out on one of the nearby counters. ''', person.HeShe(), ''' gives ''', person.hisher(), ''' bottom an uneasy rub with one hand, while stuffing ''', person.hisher(), ''' face with the other. ''', person.HeShe(), ''' glances surreptitiously at Alondra a few times, before focusing intensely on ''', person.hisher(), ''' food.''']])
        ep2_alondra_rubbing_attracted_denial.children = []
        ep2_alondra_rubbing_attracted_denial.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_alondra_rubbing_attracted_denial.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_rubbing_attracted_denial.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_rubbing_attracted_denial.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_rubbing_attracted_denial.quip_function = ep2_alondra_rubbing_attracted_denial_quip_function
    ep2_alondra_rubbing_attracted_acceptance = conversation.Node(344)
    def ep2_alondra_rubbing_attracted_acceptance_quip_function():

        ep2_alondra_rubbing_attracted_acceptance.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' drags ''', person.hisher(), ''' body back a few inches, until ''', person.hisher(), ''' hip is pressed against Alondra's belly. "Hope you don't mind. Felt kind of unstable, you know?"'''],
['\n\n' + '''"Umm," says Alondra. Her rubbing slows a little, before picking up again. "No, no not at all. Not at all. Feeling comfortable?"'''],
['\n\n' + '''"As comfortable as I can be," says ''', universal.state.player.name, ''', rocking ''', person.hisher(), ''' hips a little bit. "All things considered. You? Your leg seems to be in kind of an awkward position."'''],
['\n\n' + '''"Err, yes." Alondra lets her leg slide down to ''', universal.state.player.name, "'s", ''' calves. "Yes, I suppose, you know, I guess it was. That feels much better though. Hope it's not too uncomfortable for you."'''],
['\n\n' + universal.state.player.name, ''' shrugs.''']])
        ep2_alondra_rubbing_attracted_acceptance.children = []
        ep2_alondra_rubbing_attracted_acceptance.playerComments = []

        ep2_alondra_rubbing_attracted_acceptance.children = ep2_alondra_spanking_done.children
        conversation.say_node(ep2_alondra_spanking_done.index)

    ep2_alondra_rubbing_attracted_acceptance.quip_function = ep2_alondra_rubbing_attracted_acceptance_quip_function
    ep2_alondra_rubbing_not_attracted = conversation.Node(345)
    def ep2_alondra_rubbing_not_attracted_quip_function():

        ep2_alondra_rubbing_not_attracted.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' can't help but sigh a little as the worst of the burn fades.'''],
['\n\n' + '''"You have to believe, I hated doing that," says Alondra. "I don't like spanking anybody, least of all my friends. But I just can't take it anymore. I have a right to a proper night's sleep, don't you think?"'''],
['\n\n' + universal.state.player.name, ''' nods. "Yeah. I'm sorry."'''],
['\n\n' + '''Alondra sighs. "So am I. Let's try to avoid a repeat of this, yes?"'''],
['\n\n' + '''"Sounds like a plan to me," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Great." Alondra rubs ''', universal.state.player.name, "'s", ''' bottom a little bit longer.''']])
        ep2_alondra_rubbing_not_attracted.children = []
        ep2_alondra_rubbing_not_attracted.playerComments = []

        ep2_alondra_rubbing_not_attracted.children = ep2_alondra_spanking_done.children
        conversation.say_node(ep2_alondra_spanking_done.index)

    ep2_alondra_rubbing_not_attracted.quip_function = ep2_alondra_rubbing_not_attracted_quip_function
    ep2_alondra_rubbing_denied = conversation.Node(346)
    def ep2_alondra_rubbing_denied_quip_function():

        
        
        ep2_alondra_rubbing_denied.quip = universal.format_text_translate([['\n\n' + '''"What are you doing?" asks ''', universal.state.player.name, ''' sharply.'''],
['\n\n' + '''"I..." Alondra sounds a bit shocked. "I was just rubbing some of the sting away-"'''],
['\n\n' + '''"Well, don't," says ''', universal.state.player.name, ''', clambering to ''', person.hisher(), ''' feet. "I've spent enough time across your lap today, thanks."'''],
['\n\n' + '''"Sorry," says Alondra. "I just thought-"'''],
['\n\n' + '''"That I'd like comfort from my punisher? Thanks, but no thanks." ''', universal.state.player.name, ''' fixes ''', person.hisher(), ''' pajamas, then storms out of the room, and back to the kitchen.'''],
['\n\n' + person.HeShe(), ''' is halfway through breakfast, before Alondra returns, looking a bit haggard. She glances briefly at ''', universal.state.player.name, ''' before turning her attention to helping Ildri.''']])
        ep2_alondra_rubbing_denied.children = []
        ep2_alondra_rubbing_denied.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_alondra_rubbing_denied.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_rubbing_denied.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_rubbing_denied.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_rubbing_denied.quip_function = ep2_alondra_rubbing_denied_quip_function
    ep2_ventilate_resist = conversation.Node(347)
    def ep2_ventilate_resist_quip_function():

        
        ep2_ventilate_resist.quip = universal.format_text_translate([['\n\n' + '''"No," cries ''', universal.state.player.name, '''. ''', person.HeShe(), ''' digs ''', person.hisher(), ''' heels into the ground, and pulls back against Alondra's grip. "Let go of me!"'''],
['\n\n' + '''"Oh come on, ''', universal.state.player.name, '''! You're acting like a child," says Alondra impatiently. She grabs ''', universal.state.player.name, "'s", ''' arm with both hands, and tries to haul ''', person.himher(), ''' towards their room. "I mean, I shouldn't even have to do this. Is thirty seconds of consideration for your roommate really too much to ask?"'''],
['\n\n' + '''"Oh please," says ''', universal.state.player.name, '''. "We live in the middle of a city! Our room smells downright fresh compared to most of the city."'''],
['\n\n' + '''"That's like saying an Allosaur is small compared to a Supersaur," growls Alondra. "It doesn't matter, because an Allosaur is still freaking huge! Now come on, or so help me-"'''],
['\n\n' + '''"This is absurd." ''', universal.state.player.name, ''' raps the heel of ''', person.hisher(), ''' hand against Alondra's funny bone.'''],
['\n\n' + '''Alondra yelps, releases ''', universal.state.player.name, "'s", ''' arm and pulls her own arm in tight against her chest. "Hey, what in La Madre's name-"'''],
['\n\n' + '''"You are not spanking me," says ''', universal.state.player.name, ''' in a low dangerous voice, pointing one finger menacingly at Alondra. "And if you're thinking of trying to make me, remember I've been learning how to fight since I was barely old enough to walk. I can and will kick your ass."'''],
['\n\n' + '''"Look, come on ''', universal.state.player.nickname, ''', don't be a jerk-"'''],
['\n\n' + '''"I'm the jerk?" cries ''', universal.state.player.name, '''. "You're the one who wants to paddle me because you don't like my cleaning routine-"'''],
['\n\n' + '''"This isn't about that," cries Alondra. "This is about you being a self-centered asshole. At least once a week for the past month, you've stumbled into our room in the middle of the night, clattering about like a sauropod in a porceliain shop. Then the next morning you bitch and whine, because I have to get up at the crack of dawn so your breakfast can be ready by the time you drag your hung-over, lazy ass out of bed. Half the time, you threw up in the middle of the night, so our room stinks to high heaven, and a couple of times, you didn't even bother to clean it! I've warned you, I've begged you, I've pleaded with you, and still you keep doing it. Well, I'm sick of it! I'm sick of lying in bed with my pillow over my head, praying you don't throw up. I'm sick of toptoeing around you every morning, because even the sound of a falling feather will set you off, and I won't put up with it anymore. You start showing me a fraction of the consideration I've been trying to show you, or I will paddle your ass everyday for the rest of your wretched life! Madre, I shouldn't have to make that threat. You're supposed to be an adult. Start acting like it!"''']])
        ep2_ventilate_resist.children = [ep2_ventilate_resist_continue, ep2_ventilate_resist_contrite]
        ep2_ventilate_resist.playerComments = ['''"Or, you could pull that pole out of your ass, and come join us. You know, actually have some fun every now and then? Then, maybe you'll stop being a whiny little brat."''','''"You're right. I've been a jerk. I'm sorry."''']

        

    ep2_ventilate_resist.quip_function = ep2_ventilate_resist_quip_function
    ep2_ventilate_resist_continue = conversation.Node(348)
    def ep2_ventilate_resist_continue_quip_function():

        
        ep2_ventilate_resist_continue.quip = universal.format_text_translate([['\n\n' + '''"I've heard enough," says Ildri, walking up and smacking ''', universal.state.player.name, ''' hard on the ass. "The only one being a brat here is you. Now, you will go with Alondra, and you will take your paddling, or I will give you a thrashing that'll make whatever Alondra has planned look like a lover's caress."'''],
['\n\n' + universal.state.player.name, ''' eyes Ildri's thick, muscled arms, then glances at Alondra's much more slender limbs. ''', person.HeShe(), ''' tosses ''', person.hisher(), ''' head imperiously. "Fine. But if you think-"'''],
['\n\n' + '''"Yeah, yeah whatever." Alondra grabs ''', universal.state.player.name, "'s", ''' arm and gives ''', person.himher(), ''' a sharp tug in the direction of the kitchen's exit. "Let's get this over with."'''],
['\n\n' + universal.state.player.name, ''' allows Alondra to pull ''', person.himher(), ''' into their room. Alondra lets go of ''', universal.state.player.name, "'s", ''' wrist, and approaches the small chest at the foot of her bed. After a few seconds of rooting around, she comes up with a large, white bone hairbrush. She sits down on the bed, and glares at ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Over my knee," says Alondra imperiously.''']])
        ep2_ventilate_resist_continue.children = [ep2_ventilate_resist_comply, ep2_ventilate_resist_fight]
        ep2_ventilate_resist_continue.playerComments = ['''Comply reluctantly.''','''Turn the tables, and give Alondra a lesson in roommate etiquette.''']

        

    ep2_ventilate_resist_continue.quip_function = ep2_ventilate_resist_continue_quip_function
    ep2_ventilate_resist_fight = conversation.Node(349)
    def ep2_ventilate_resist_fight_quip_function():

        
        
        textCommandsMusic.increment_spankings_given()
        
        
        
        ep2_ventilate_resist_fight.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' crosses ''', person.hisher(), ''' arms and smirks. "Yeah? Says who?"'''],
['\n\n' + '''Alondra grinds her teeth together. "Stop being so cursed unreasonable! Just get-"'''],
['\n\n' + '''"Look whose talking," says ''', universal.state.player.name, '''. "You're the one making a mountain out of a hillock."'''],
['\n\n' + '''"I'm done arguing with you." Alondra stands up and grabs ''', universal.state.player.name, "'s", ''' arm. "Now get that ''', universal.format_line(['''fat''']) if universal.state.player.bodyType == 'voluptuous' or universal.state.player.bodyType == 'heavyset' else universal.format_line(['''scrawny''']), ''' ass of yours over my knee!"'''],
['\n\n' + universal.state.player.name, ''' wrenches ''', person.hisher(), ''' arm free, grabs Alondra's wrist, and yanks the woman forward. As Alondra slams into ''', person.himher(), ''', ''', person.heshe(), ''' grabs Alondra around the shoulders, pivots into a lunge position, and yanks the young woman across ''', person.hisher(), ''' knee.'''],
['\n\n' + '''"''', universal.state.player.name, ''', let me up this instant," cries Alondra, drumming her feet against the ground. She tries to break free, but ''', universal.state.player.name, ''' is not only stronger than her, but also much more skilled, and holds the struggling girl easily. "When I tell Ildri-"'''],
['\n\n' + '''"Yeah, yeah, yeah, hide behind Ildri's apron strings." ''', universal.state.player.name, ''' picks up Alondra's dropped hairbrush, and flips up Alondra's skirt, exposing a pair of lacy blue panties that cover the top third of her curvy bottom, and not much else. "Nice panties. Buy them with your first payment?"'''],
['\n\n' + '''Alondra snarls, and bucks savagely against ''', universal.state.player.name, "'s", ''' thigh. She reaches back and tries to slap ''', universal.state.player.name, ''' across the face, but ''', universal.state.player.name, ''' catches her wrist, and pins it against her lower back.'''],
['\n\n' + universal.state.player.name, ''' lands a vicious blow to Alondra's right cheek. The heavy sound of bone to flesh reverberates through the air. Alondra's fleshy cheek flattens and bounces beneath the blow. Her hips jump, and her feet scrabble against the wooden floor. A sharp cry bursts from her lips.'''],
['\n\n' + '''"I won't warn you again," says Alondra. "Let go-oww!"'''],
['\n\n' + universal.state.player.name, ''' smashes the heavy hairbrush against the fleshy center of Alondra's left buttock.'''],
['\n\n' + '''"I mean it," says Alonda savagely, twisting in ''', universal.state.player.name, "'s", ''' grip. She tries to shove forward with her feet, but ''', universal.state.player.name, ''' wraps ''', person.hisher(), ''' arm around Alondra's waist, and pulls her tight against ''', person.hisher(), ''' torso. "Let me go or I'll start screaming for Ildri!"'''],
['\n\n' + '''"Fight your own battles, you cursed coward," says ''', universal.state.player.name, '''. ''', person.HeShe(), ''' begins rapidly battering Alondra's exposed cheeks. Alondra's large bottom writhes and bounces. She tries to jab her pinned elbow into ''', universal.state.player.name, "'s", ''' gut, but the angle is weird, and she doesn't have much leverage. The only effect is that ''', universal.state.player.name, ''' begins hitting harder.'''],
['\n\n' + '''"Ildri!" wails Alondra, bucking and writhing in ''', universal.state.player.name, "'s", ''' grip. "Ildri help me!"'''],
['\n\n' + universal.state.player.name, ''' starts paddling Alondra faster. ''', person.HeShe(), ''' tries to cover Alondra's mouth with ''', person.hisher(), ''' hand, but the girl is squirming so badly, ''', universal.state.player.name, ''' needs ''', person.hisher(), ''' full arm to keep the girl pinned across ''', person.hisher(), ''' thigh.'''],
['\n\n' + '''Then the door bursts open, and Alondra stands in the doorway, with her hands on her large hips. ''', universal.state.player.name, ''' can notice a few curious faces peaking over Ildri's shoulder, and between her torso and arms.'''],
['\n\n' + '''The cook takes the whole scene in at a glance, and her expression darkens dangerously. She steps into the room, and closes the door. "You will let go of Alondra, and you will let go of her now."'''],
['\n\n' + universal.state.player.name, ''' gives Ildri a defiant glare, and cracks the hairbrush against Alondra's right sitspot, eliciting a very satisfying wail from the other girl.'''],
['\n\n' + '''Ildri steps forward and grabs ''', universal.state.player.name, "'s", ''' wrist in a painfully tight grip. "I am so sick of this. Alondra and I have breakfast to cook. We cannot waste time forcing you to take a spanking that you shouldn't need to begin with!"'''],
['\n\n' + '''"If I don't need it, then why are you so insistent of giving it to me?" asks ''', universal.state.player.name, ''', trying (and failing) to free ''', person.hisher(), ''' wrist.'''],
['\n\n' + '''"Don't you dare get cheeky with me you little brat." She grabs ''', universal.state.player.name, "'s", ''' other hand, and starts to peel it away from Alondra. "You do need it. You need it badly. But you shouldn't! Mother's love, my children were more considerate than you when they were five. And five year-olds are demons."'''],
['\n\n' + '''"Let go of me," says ''', universal.state.player.name, ''', trying to twist free of Ildri's grip. Unfortunately, ''', universal.state.player.name, "'s", ''' struggles would have been more effective against a stone wall, and soon Ildri is holding ''', universal.state.player.name, ''' with ''', person.hisher(), ''' forearms folded and pinned securely against ''', person.hisher(), ''' back. ''', universal.state.player.name, ''' twists savagely.'''],
['\n\n' + '''"You keep that up, and you're going to break your arms," says Ildri.'''],
['\n\n' + '''"Bah. My health can handle it," spits ''', universal.state.player.name, '''.'''],
['\n\n' + '''Ildri wraps her left arm around ''', universal.state.player.name, "'s", ''' shoulders, and pulls ''', person.himher(), ''' tight against Ildri's chest, robbing ''', universal.state.player.name, ''' of the flexibility needed to twist.'''],
['\n\n' + '''Meanwhile, Alondra has regained her feet, and is fixing her skirt. She winces when the course wool falls back down across her stinging bottom, before crouching and picking up the hairbrush. "Thank you Ildri. I tried to hold ''', person.himher(), ''' but-"'''],
['\n\n' + '''"I know dear," says Ildri. "That's the problem with adventurers. Professional fighters are hard as stone to spank when they're acting like immature brats."'''],
['\n\n' + '''"So how are we going to do this?" asks Alondra, locking glares with ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Simple." Ildri drags ''', universal.state.player.name, ''' towards the bed, and sits down on the edge of the bed. She hauls ''', universal.state.player.name, "'s", ''' struggling form across her lap. ''', universal.state.player.name, ''' starts cursing viciously, but Ildri simply claps her right hand over the ''', person.boygirl(), ''''s mouth with one hand, while holding ''', person.himher(), ''' pinned against her thighs with the other.'''],
['\n\n' + '''Alondra steps up next to ''', universal.state.player.name, "'s", ''' proferred bottom.'''],
['\n\n' + '''Ildri releases her hold on ''', universal.state.player.name, "'s", ''' mouth, and \liftslowers{''', universal.state.player.pajama_top().name, '''} ''', universal.state.player.name, "'s", ''' ''', universal.format_line(['''the dropseat of ''', universal.state.player.name, "'s", ''' pajamas''']) if universal.state.player.pajama_bottom().armorType == items.DropSeatPajamas.armorType else universal.format_line(['''''', universal.state.player.pajama_bottom().name, '''''']), ''', bringing ''', universal.state.player.name, "'s", ''' tense, ''', universal.state.player.bum_adj(), ''', bare cheeks into the morning light. "Give it to ''', person.himher(), ''' good, Ali."'''],
['\n\n' + '''"This is so unfair!" wails ''', universal.state.player.name, ''', pounding ''', person.hisher(), ''' fist against Ildri's thigh.'''],
['\n\n' + '''"Oh yes," says Alondra, cracking her hairbrush against the swell of ''', universal.state.player.name, "'s", ''' left cheek, making full use of her standing leverage. "Totally unfair. Nothing's more unfair than being called to task for your self-centered crap."'''],
['\n\n' + universal.state.player.name, ''' gives Alondra the finger.'''],
['\n\n' + '''Alondra laughs. "What are you trying to accomplish here? What do you think is the outcome is going to me of spanking me, and then flipping me off? I have Ildri on my side, someone who can clearly hold you like you're a child. Your naked ass is completely exposed and vulnerable, and I have a heavy hairbrush in my hand. I mean, if you want a harder spanking, you just have to ask."'''],
['\n\n' + universal.state.player.name, ''' crosses ''', person.hisher(), ''' arms and glares.'''],
['\n\n' + '''Alondra shrugs. "Whatever."'''],
['\n\n' + '''Alondra draws her arm back, leans forward slightly, and cracks the hairbrush against ''', universal.state.player.name, "'s", ''' right cheek. ''', universal.state.player.name, ''' grunts a little, and grinds ''', person.hisher(), ''' teeth together against the sharp sting. Alondra begins a slow, hard, steady paddling. She alternates between cheeks, and each blow lands someplace new, quickly spreading an even sting across the entirety of ''', universal.state.player.name, "'s", ''' bottom. ''', universal.state.player.name, ''' grunts, and twitches through the blows. ''', person.HeShe(), ''' glares resolutely at the stupid window, while gripping Ildri's ankle. ''', person.HeShe(), ''' takes deep breaths between each blow, and forces ''', person.hisher(), ''' bottom to relax.'''],
['\n\n' + '''When every inch of ''', universal.state.player.name, "'s", ''' bottom is stinging, Alondra rubs the hairbrush against ''', universal.state.player.name, "'s", ''' right cheek. "Right, now that the warm up's done, let's really get started."'''],
['\n\n' + universal.state.player.name, "'s", ''' eyes widen. Warm up? What-'''],
['\n\n' + '''THWACK!'''],
['\n\n' + '''A fountain of stinging pain centered in ''', person.hisher(), ''' right sitspot cascades across ''', universal.state.player.name, "'s", ''' bottom. A squeal grows and dies in ''', person.hisher(), ''' throat, ''', person.hisher(), ''' clenched jaw the only thing keeping it contained. ''', person.HeShe(), ''' twitches on Ildri's lap, and ''', person.hisher(), ''' fingers spasmatically tighten on her ankle.'''],
['\n\n' + '''"Think ''', person.heshe(), ''' felt that one," says Ildri, patting the small of ''', universal.state.player.name, "'s", ''' back.'''],
['\n\n' + '''"Good," says Alondra. "Because ''', person.heshe(), ''''s got a lot just like that coming."'''],
['\n\n' + '''THWACK! THWACK! THWACK!'''],
['\n\n' + '''The heavy hairbrush bites mercilessly into ''', universal.state.player.name, "'s", ''' ''', universal.state.player.muscle_adj(), ''' cheeks. At first, ''', universal.state.player.name, ''' barely manages to keep ''', person.hisher(), ''' reactions to a few squirms, and some grunts. But as the blows keep coming, the squirms turn into wiggling, then flailing. ''', person.HisHer(), ''' grunts turn into squeals, then wails. ''', person.HeShe(), ''' bucks and thrashes. ''', person.HeShe(), ''' drums ''', person.hisher(), ''' toes painfully into the floor. ''', person.HisHer(), ''' nails dig into Ildri's ankle, while ''', person.hisher(), ''' other fist pounds against her the dirt. Tears form in ''', person.hisher(), ''' eyes.'''],
['\n\n' + '''"Don't you ever do that again," says Alondra as she wallops ''', universal.state.player.name, "'s", ''' ass. "When you earn yourself a spanking, then by La Madre, you are going to bend over and take your spanking! You are not to ever, ever again try to spank your punisher. Do you understand me?"'''],
['\n\n' + '''"Get buried," spits ''', universal.state.player.name, ''' through ''', person.hisher(), ''' budding sobs.'''],
['\n\n' + '''Alondra gives Ildri a helpless look, who gives a small nod. Alondra grimaces uneasily, but then takes on an expression of stone. She leans forward, and plants her hand between ''', universal.state.player.name, "'s", ''' shoulder blades. "I really don't want to do this, but since you insist on being so pointlessly stubborn..."'''],
['\n\n' + '''Alondra lands half a dozen hard, fast blows to the peak of ''', universal.state.player.name, "'s", ''' right cheek. ''', universal.state.player.name, ''' howls, and ''', person.hisher(), ''' flailing reaches new peaks. Then, Alondra shifts her attention to ''', person.hisher(), ''' left cheek, and the flailing intensifies. Tears flow freely down ''', person.hisher(), ''' face, and ''', person.hisher(), ''' howls are interrupted by sobs.'''],
['\n\n' + '''Still, Alondra continues to smack ''', universal.state.player.name, "'s", ''' cheeks, hitting ''', person.himher(), ''' almost as hard as before, but twice as fast. ''', person.HisHer(), ''' flailing becomes so bad, that Ildri has to hook one leg over ''', universal.state.player.name, "'s", ''' legs, and lean on ''', person.hisher(), ''' back to hold ''', person.himher(), ''' down.'''],
['\n\n' + '''Then, ''', universal.state.player.name, ''' becomes too exhausted to continue, and ''', person.heshe(), ''' stops. ''', person.HeShe(), ''' slumps across Ildri's lap, and sobs brokenly.'''],
['\n\n' + '''Alondra stops. She gnaws uneasily on her lower lip, as her eyes dance between the blisters on ''', universal.state.player.name, "'s", ''' bottom, and ''', universal.state.player.name, "'s", ''' defeated posture. She glances at Ildri. "Did I-"'''],
['\n\n' + '''"No," says Ildri. She rubs ''', universal.state.player.name, "'s", ''' back. "''', person.HeShe(), ''' earned every smack. But it's over now."'''],
['\n\n' + '''Ildri helps ''', universal.state.player.name, ''' get off her lap, and lays ''', person.himher(), ''' down on ''', person.hisher(), ''' facedown on ''', person.hisher(), ''' bed. "I need to get back to the kitchen. I'll give you about a quarter-glass, Alondra, but then I'll need you as well."'''],
['\n\n' + universal.state.player.name, ''' buries ''', person.hisher(), ''' face in ''', person.hisher(), ''' pillow, and sobs while one hand gingerly strokes ''', person.hisher(), ''' blazing bottom.'''],
['\n\n' + '''Alondra sits down on the edge of the bed, and begins to rub small circles on ''', universal.state.player.name, "'s", ''' back. "I'm sorry that I had to do that. But what did you expect? You've been treating me like dirt for the past month-Well, no that's excessive. But the point is, you haven't shown much concern for me, or what I need. I've been twisting and turning to accomodate you, and you haven't so much as looked in my direction. That's unfair, and you know it."'''],
['\n\n' + universal.state.player.name, ''' doesn't respond.''']])
        ep2_ventilate_resist_fight.children = []
        ep2_ventilate_resist_fight.playerComments = []

        if universal.state.player.is_female():
            ep2_ventilate_resist_fight.children = ep2_ventilate_resist_fight_comfort_female.children
            conversation.say_node(ep2_ventilate_resist_fight_comfort_female.index)
        elif True:
            ep2_ventilate_resist_fight.children = ep2_ventilate_resist_fight_comfort_male.children
            conversation.say_node(ep2_ventilate_resist_fight_comfort_male.index)

    ep2_ventilate_resist_fight.quip_function = ep2_ventilate_resist_fight_quip_function
    ep2_ventilate_resist_fight_comfort_female = conversation.Node(350)
    def ep2_ventilate_resist_fight_comfort_female_quip_function():

        
        
        ep2_ventilate_resist_fight_comfort_female.quip = universal.format_text_translate([['\n\n' + '''Alondra lies down next to ''', universal.state.player.name, ''', and pulls ''', person.himher(), ''' close.''']])
        ep2_ventilate_resist_fight_comfort_female.children = [ep2_alondra_ventilate_resist_fight_comfort_female_attraction, ep2_alondra_ventilate_resist_fight_comfort_female_comfort, ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort]
        ep2_ventilate_resist_fight_comfort_female.playerComments = ['''Melt into Alondra's embrace, and take comfort from her warmth.''','''Take comfort in Alondra's hold.''','''Refuse her comfort.''']

        

    ep2_ventilate_resist_fight_comfort_female.quip_function = ep2_ventilate_resist_fight_comfort_female_quip_function
    ep2_alondra_ventilate_resist_fight_comfort_female_attraction = conversation.Node(351)
    def ep2_alondra_ventilate_resist_fight_comfort_female_attraction_quip_function():

        
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' wiggles a bit closer to Alondra. ''', person.HeShe(), ''' buries ''', person.hisher(), ''' face in Alondra's shoulder, sobbing mightily. Alondra wraps her arms around ''', universal.state.player.name, '''. She presses one hand lightly against the back of ''', universal.state.player.name, "'s", ''' head, and the other against ''', person.hisher(), ''' back. She rests her cheek against the top of ''', universal.state.player.name, "'s", ''' head.'''],
['\n\n' + '''"I'm sorry," mumbles ''', universal.state.player.name, '''. "I'm sorry, I'm sorry."'''],
['\n\n' + '''"Hush," says Alondra gently. "Hush, hush. It's all over. You're forgiven. It's as if it never happened."'''],
['\n\n' + universal.state.player.name, ''' wraps ''', person.hisher(), ''' arms around Alondra's waist, and pulls ''', person.himselfherself(), ''' tight against the other woman's soft, warm frame. A tingle shoots through ''', person.hisher(), ''' body, wherever it comes in contact with Alondra's, especially around the hips, and chest. Alondra shifts her position a little, and one of her smooth, curvy legs travels a few inches up one of ''', universal.state.player.name, "'s", ''', warm skin rubbing sensuously against warm skin.'''],
['\n\n' + '''Her hand travels slowly, inexorably down ''', universal.state.player.name, "'s", ''' back, until her fingers are resting feather-light against ''', universal.state.player.name, "'s", ''' blistered bottom. Slowly, her fingers trace faint, barely perceptiple lines of sensation across ''', universal.state.player.name, "'s", ''' ravaged cheeks. ''', universal.state.player.name, ''' sighs, and ''', person.hisher(), ''' back arches slightly. Growing bolder, Alondra's palm begins to caress the tender cheeks, her slightly rough, yet soothingly soft, hands moving slowly up and down, rubbing away the worst of the sting and replacing it with faint tingles.'''],
['\n\n' + '''A faint moan slips from ''', universal.state.player.name, "'s", ''' lips.''']])
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction.children = []
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction.playerComments = []

        if 'lesbian_in_denial' in textCommandsMusic.keywords():
            ep2_alondra_ventilate_resist_fight_comfort_female_attraction.children = ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial.children
            conversation.say_node(ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial.index)
        elif True:
            ep2_alondra_ventilate_resist_fight_comfort_female_attraction.children = ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan.children
            conversation.say_node(ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan.index)

    ep2_alondra_ventilate_resist_fight_comfort_female_attraction.quip_function = ep2_alondra_ventilate_resist_fight_comfort_female_attraction_quip_function
    ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial = conversation.Node(352)
    def ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial_quip_function():

        
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial.quip = universal.format_text_translate([['\n\n' + '''The moan jerks ''', universal.state.player.name, ''' out of the same fog clogging ''', person.hisher(), ''' mind. ''', person.HeShe(), ''' pushes away Alondra's grasp, and pushes ''', person.himselfherself(), ''' to ''', person.hisher(), ''' hands and knees.'''],
['\n\n' + '''"''', universal.state.player.nickname, '''?" says Alondra hesitantly. "What's wrong?"'''],
['\n\n' + '''"Nothing," says ''', universal.state.player.name, ''' quickly, staring down at ''', person.hisher(), ''' bed. "I just, I think maybe, we've got a day, and stuff you know? Things to do. Food to cook, guilds to repair. You know. Stuff. And I should really get changed. Lost most of the morning already, don't want to lose the afternoon. Things to do. Could you, umm, get up, so I can to my clothing?"'''],
['\n\n' + '''"Are you feeling better?" asks Alondra.'''],
['\n\n' + '''"Much better," says ''', universal.state.player.name, ''' quickly, quickly covering ''', person.himselfherself(), '''. ''', person.HeShe(), ''' quickly pulls out ''', person.hisher(), ''' day clothing, and begins getting changed, ''', person.hisher(), ''' back turned to Alondra. As ''', person.heshe(), ''' is pulling on ''', person.hisher(), ''' ''', universal.format_line(['''''', universal.state.player.underwear().name, '''''']) if universal.state.player.wearing_underwear() else universal.format_line(['''''', universal.state.player.lower_clothing().name, '''''']), ''', ''', person.heshe(), ''' notices that there is a bit of dewy dampness between ''', person.hisher(), ''' legs. ''', person.HeShe(), ''' pauses for a moment, then quickly finishes getting changed.'''],
['\n\n' + '''"I see," says Alondra. Her voice has a strange element of resignation. "Well, we still need to talk about what we're going to do to fix the problem."'''],
['\n\n' + '''"What?"'''],
['\n\n' + '''"Oh come on. I didn't spank you because I enjoy it, I spanked you because you needed to learn just how inconsiderate you were being. Now that we've gotten that out of the way, we need to figure out what to do so that we don't have to repeat this little session."'''],
['\n\n' + universal.state.player.name, ''' gives ''', person.hisher(), ''' bottom a rub, and turns to face Alondra. "I'm all for not repeating this."'''],
['\n\n' + '''"Umm, anyway. I figure we have two options. One, we institute a curfew, in which I come and get you after a certain amount of time. Obviously, for this to work you'll have to come with me without a fuss, and you'll have to tell me where you plan on going each night so that I can find you. Or two, you can keep yourself sober enough to stay quiet when you get home, and to not throw up all over the floor, and then crawl into bed."'''],
['\n\n' + '''"I see," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"And I should warn you, if you take the first option, but try to resist, I will take my hairbrush to your ass. Similarly if you take the second option, but come home like you always have after a night out. So it's up to you. Can you remember not to disburb me, or will you need help?"'''],
['\n\n' + universal.state.player.name, ''' uneasily eyes Alondra's hairbrush (currently resting on Alondra's bed) as ''', person.heshe(), ''' considers ''', person.hisher(), ''' options.''']])
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial.children = [ep2_alondra_curfew, ep2_alondra_no_curfew]
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial.playerComments = ['''"Erm, let's go for the curfew."''','''"I'll try not to disturb you, I promise."''']

        

    ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial.quip_function = ep2_alondra_ventilate_resist_fight_comfort_female_attraction_lesbian_denial_quip_function
    ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan = conversation.Node(353)
    def ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan_quip_function():

        
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan.quip = universal.format_text_translate([['\n\n' + '''"Feeling better?" asks Alondra, her warm breath rolling across the outer-edges of ''', universal.state.player.name, "'s", ''' ear.'''],
['\n\n' + '''"Little bit," murmurs ''', universal.state.player.name, ''', rubbing ''', person.hisher(), ''' face against Alondra's shoulder, tightening ''', person.hisher(), ''' hold around Alondra's waist, and drawing ''', person.hisher(), ''' leg a few inches further up Alondra's.'''],
['\n\n' + '''"I'm glad," says Alondra quietly. "I was worried that maybe you'd start hating me, or something."'''],
['\n\n' + '''"You want me to hate you, you'll have to spank me without good reason," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"I'll keep that in mind." Alondra gives ''', universal.state.player.name, "'s", ''' bottom a light pat, and then disentangles herself. "Anyway, I should probably get going. Ildri's going to start getting a bit impatient."'''],
['\n\n' + '''"OK," says ''', universal.state.player.name, ''', trying to hide ''', person.hisher(), ''' disappointment.'''],
['\n\n' + '''"You should probably come and have some breakfast," says Alondra. "And we need to discuss how we're going to solve this."'''],
['\n\n' + '''"What do you mean?" asks ''', universal.state.player.name, ''', as ''', person.heshe(), ''' starts rooting through the chest at the foot of ''', person.hisher(), ''' bed for ''', person.hisher(), ''' day clothing.'''],
['\n\n' + '''"Umm, you know you could cover yourself," says Alondra, her face darkening.'''],
['\n\n' + '''"Oh come on. I'm about to get changed," says ''', universal.state.player.name, '''. "Besides it's not like you haven't already seen it all, considering what just happened."'''],
['\n\n' + '''"I suppose," says Alondra. "Anyway, I didn't spank you because I enjoy it, I spanked you because you needed to learn just how inconsiderate you were being. Now that we've gotten that out of the way, we need to figure out what to do so that we don't have to repeat this little session."'''],
['\n\n' + universal.state.player.name, ''' glances over ''', person.hisher(), ''' shoulder at Alondra's hairbrush (currently sitting on top of Alondra's bed). "Yes. I'm all for not getting thwacked by that hairbrush again anytime soon."'''],
['\n\n' + '''"And I don't want to thwack you with it," says Alondra. "So, I'm thinking we have two options. One, we institute a curfew, in which I come and get you after a certain amount of time. Obviously, for this to work you'll have to come with me without a fuss, and you'll have to tell me where you plan on going each night so that I can find you. Or two, you can keep yourself sober enough to stay quiet when you get home, and to not throw up all over the floor, and then crawl into bed."''']])
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan.children = [ep2_alondra_curfew, ep2_alondra_no_curfew]
        ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan.playerComments = ['''"Erm, let's go for the curfew."''','''"I'll try not to disturb you, I promise."''']

        

    ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan.quip_function = ep2_alondra_ventilate_resist_fight_comfort_female_attraction_moan_quip_function
    ep2_alondra_ventilate_resist_fight_comfort_female_comfort = conversation.Node(354)
    def ep2_alondra_ventilate_resist_fight_comfort_female_comfort_quip_function():

        
        ep2_alondra_ventilate_resist_fight_comfort_female_comfort.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' shifts a little bit closer to Alondra, and buries ''', person.hisher(), ''' face in Alondra's shoulder. "I'm sorry, Ali. I don't know what I was thinking."'''],
['\n\n' + '''"Hush." Alondra holds ''', universal.state.player.name, ''' tight, and rocks gently, her fingers gently stroking the back of ''', universal.state.player.name, "'s", ''' head. "Hush, it's all right. You just lost your temper, is all."'''],
['\n\n' + '''"You gave me a curse of a spanking for 'just losing my temper,'" says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Well, you were pretty far out of line," says Alondra. "And I lost my temper too. I don't care what Ildri said, I shouldn't have spanked you that hard."'''],
['\n\n' + '''"I can get behind that," says ''', universal.state.player.name, ''' with a faint, sob-wracked laugh.'''],
['\n\n' + '''"Anyway, we do need to talk about what we can do to better accomodate the both of us," says Alondra. "I don't want to rob you of your fun, but at the same time I can't deal with your late night disturbances. To say nothing of your hangovers. Plus, it's just scary. I mean, what if you throw up in your sleep, and I don't hear it, and you end up drowning in it, or something?"'''],
['\n\n' + '''"Oh come on," says ''', universal.state.player.name, '''. "I don't get anywhere near that drunk. I'm not that stupid."'''],
['\n\n' + '''"OK, OK, sorry," says Alondra. "But anyway, I figure we have two options. One, we institute a curfew, in which I come and get you after a certain amount of time. Obviously, for this to work you'll have to come with me without a fuss, and you'll have to tell me where you plan on going each night so that I can find you. Or two, you can keep yourself sober enough to stay quiet when you get home, and to not throw up all over the floor, and then crawl into bed."'''],
['\n\n' + '''"I see," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"And I should warn you, if you take the first option, but try to resist, I will take my hairbrush to your ass. Similarly if you take the second option, but come home like you always have after a night out. So it's up to you. Can you remember not to disburb me, or will you need help?"''']])
        ep2_alondra_ventilate_resist_fight_comfort_female_comfort.children = [ep2_alondra_curfew, ep2_alondra_no_curfew]
        ep2_alondra_ventilate_resist_fight_comfort_female_comfort.playerComments = ['''"Erm, let's go for the curfew."''','''"I'll try not to disturb you, I promise."''']

        

    ep2_alondra_ventilate_resist_fight_comfort_female_comfort.quip_function = ep2_alondra_ventilate_resist_fight_comfort_female_comfort_quip_function
    ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort = conversation.Node(355)
    def ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort_quip_function():

        
        
        ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' pulls sharply away from Alondra's hug.'''],
['\n\n' + '''"Come on, ''', universal.state.player.nickname, '''. Don't be like that," says Alondra, a hint of pleading in her voice.'''],
['\n\n' + '''"Fuck off," mutters ''', universal.state.player.name, ''' into ''', person.hisher(), ''' pillow.'''],
['\n\n' + '''"But-"'''],
['\n\n' + '''"I said fuck off!" snaps ''', universal.state.player.name, ''', glaring at Alondra.'''],
['\n\n' + '''Alondra shrinks from the glare. She nods. "OK. I'm going."'''],
['\n\n' + '''Alondra slips out of the bed and walks to the door. She pauses and looks back at ''', universal.state.player.name, '''. "You know, I didn't like spanking anymore than you liked being spanked."'''],
['\n\n' + universal.state.player.name, ''' buries ''', person.hisher(), ''' face in ''', person.hisher(), ''' pillow and ignores her.'''],
['\n\n' + '''The door opens and closes.'''],
['\n\n' + universal.state.player.name, ''' curls up into a fetal position, and cries miserably for a while longer. Stupid Alondra. Stupid Ildri. Should have lived with Maria. She has it right, getting her own place. Then she doesn't have to put up with Ildri's tyranny. Should have just let the Vengadores steal everything.'''],
['\n\n' + universal.state.player.name, "'s", ''' thoughts flit across the past month or so, ''', person.hisher(), ''' numerous late nights, and really bad hangovers. Maybe ''', person.heshe(), ''' had been a bit inconsiderate. And in retrospect, spanking Alondra had been a terrible idea. Not quite sure what ''', person.heshe(), ''' was thinking. Didn't exactly help the whole "inconsiderate" thing either.'''],
['\n\n' + '''Eventually, ''', universal.state.player.name, ''' wipes ''', person.hisher(), ''' face and clambers out of bed. ''', person.HeShe(), ''' very carefully gets dressed, hissing in pain as ''', person.heshe(), ''' pulls on ''', person.hisher(), ''' ''', universal.format_line(['''''', universal.state.player.underwear().name, '''''']) if universal.state.player.wearing_underwear() else universal.format_line(['''''']), ''''''],
['''''', universal.format_line([''', and''']) if universal.state.player().wearing_skirt_or_dress_or_pants() and universal.state.player.wearing_underwear() else universal.format_line(['''''']), ''''''],
['''''', universal.format_line(['''''', universal.state.player.lower_clothing().name, '''''']) if universal.state.player.wearing_skirt_or_dress_or_pants() else universal.format_line(['''''']), '''.'''],
['\n\n' + person.HeShe(), ''' makes ''', person.hisher(), ''' way slowly into the kitchen, and makes a beeline for several trays of food at the end of one of the kitchen counters. ''', person.HeShe(), ''' quickly digs in, being careful not to look at either Alondra or Ildri. The awkward silence in the kitchen is broken only by the clatter of cooking, and the whuffs of the two spit-Coelophysii lying next to the ovens.''']])
        ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.children = []
        ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort.quip_function = ep2_alondra_ventilate_resist_fight_comfort_female_refuse_comfort_quip_function
    ep2_ventilate_resist_fight_comfort_male = conversation.Node(356)
    def ep2_ventilate_resist_fight_comfort_male_quip_function():

        
        
        ep2_ventilate_resist_fight_comfort_male.quip = universal.format_text_translate([['\n\n' + '''Alondra sighs. She sits in silent for few minutes, tenderly rubbing ''', universal.state.player.name, "'s", ''' back, while ''', person.heshe(), ''' sobs into ''', person.hisher(), ''' blankets. Once ''', universal.state.player.name, "'s", ''' crying quiets some, she stands. "Look, I need to get back into the kitchen, OK? Make sure to come and get something to eat."'''],
['\n\n' + '''Eventually, ''', universal.state.player.name, ''' slides out of bed, and gets changed. Then, ''', person.heshe(), ''' makes his way to the kitchen for some breakfast.'''],
['\n\n' + person.HeShe(), ''' avoids looking at either Alondra or Ildri as he digs into the pile of food set aside on one of the counters for adventurers to pick through.'''],
['\n\n' + '''''', universal.format_line(['''Ildri throws a disapproving look at ''', universal.state.player.name, "'s", ''' exposed cheeks. "You better get those cheeks covered by the time your bum heals, or I'll blister it all over again."''']) if universal.lower_clothing().baring and universal.state.player.underwear().baring else universal.format_line(['''''']), ''''''],
['\n\n' + '''''', universal.format_line(['''''', universal.state.player.name, ''' throws Ildri a quick look, and nods, ''', person.hisher(), ''' hand reaching back to touch ''', person.hisher(), ''' blazing bottom.''']) if universal.lower_clothing().baring and universal.state.player.underwear().baring else universal.format_line(['''''']), ''''''],
['\n\n' + '''Once he reaches the food, ''', universal.state.player.name, ''' eats without saying anything, the awkward silence in the kitchen broken only by the clatter of cooking, and the whuffs of the two spit-Coelophysii lying next to the ovens.''']])
        ep2_ventilate_resist_fight_comfort_male.children = []
        ep2_ventilate_resist_fight_comfort_male.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_ventilate_resist_fight_comfort_male.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_ventilate_resist_fight_comfort_male.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_ventilate_resist_fight_comfort_male.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_ventilate_resist_fight_comfort_male.quip_function = ep2_ventilate_resist_fight_comfort_male_quip_function
    ep2_ventilate_resist_comply = conversation.Node(357)
    def ep2_ventilate_resist_comply_quip_function():

        ep2_ventilate_resist_comply.quip = universal.format_text_translate([['''''']])
        ep2_ventilate_resist_comply.children = []
        ep2_ventilate_resist_comply.playerComments = []

        

    ep2_ventilate_resist_comply.quip_function = ep2_ventilate_resist_comply_quip_function
    ep2_ventilate_resist_contrite = conversation.Node(358)
    def ep2_ventilate_resist_contrite_quip_function():

        
        
        ep2_ventilate_resist_contrite.quip = universal.format_text_translate([['\n\n' + '''For a moment her expression softens. But then, with visible effort Alondra's face hardens, and she puts her fists on her hips. "If you really mean that, you'll come along and take your paddling like an adult."'''],
['\n\n' + universal.state.player.name, ''' nods, though ''', person.hisher(), ''' bottom clenches anxiously. "Alright. And I really am sorry. I guess, I just wasn't thinking. I never meant to make your life miserable."'''],
['\n\n' + '''"Well, miserable's a bit of a strong word," says Alondra. She flashes ''', universal.state.player.name, ''' a smile as she leads the way back to their room. "Frustrating's probably a bit more accurate."'''],
['\n\n' + '''"I'll try to remember to be more considerate in the future," says ''', universal.state.player.name, ''', meekly following after the other Taironan.'''],
['\n\n' + '''"Oh I'm sure," says Alondra. "Especially after the incentive I've got planned."''']])
        ep2_ventilate_resist_contrite.children = [ep2_ventilate_backrub, ep2_ventilate_maam, ep2_ventilate_but]
        ep2_ventilate_resist_contrite.playerComments = ['''"Like a backrub, whenever I remember?"''','''"Yes ma'am."''','''"But...but..."''']

        

    ep2_ventilate_resist_contrite.quip_function = ep2_ventilate_resist_contrite_quip_function
    ep2_alondra_spanking_done = conversation.Node(359)
    def ep2_alondra_spanking_done_quip_function():

        
        
        
        ep2_alondra_spanking_done.quip = universal.format_text_translate([['\n\n' + '''"Anyway, up you go," says Alondra, helping ''', universal.state.player.name, ''' clamber off her lap. "Get yourself covered, and then come on. You need breakfast, and I need to get back to work."'''],
['\n\n' + universal.state.player.name, ''' nods, and does as ordered. Soon, the two are back in the kitchen, Alondra busying herself with a pile of dough, while ''', universal.state.player.name, ''' munches ''', person.hisher(), ''' food with one hand, and rubs ''', person.hisher(), ''' stinging bottom with the other.''']])
        ep2_alondra_spanking_done.children = []
        ep2_alondra_spanking_done.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_alondra_spanking_done.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_spanking_done.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_spanking_done.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_spanking_done.quip_function = ep2_alondra_spanking_done_quip_function
    ep2_alondra_no_curfew = conversation.Node(360)
    def ep2_alondra_no_curfew_quip_function():

        
        ep2_alondra_no_curfew.quip = universal.format_text_translate([['\n\n' + '''"You'd better not, or you and the Squealer are going to get very well acquainted," says Alondra.'''],
['\n\n' + '''"The what?" says ''', universal.state.player.name, ''' twisting around to look at Alondra.'''],
['\n\n' + '''"Do you like it?" asks Alondra, smiling cheerfully. "Just came up with it. Name comes from the sound you make when I smack you with it."'''],
['\n\n' + '''"I didn't squeal," mutters ''', universal.state.player.name, '''.'''],
['\n\n' + '''"You squealed like an eighteen year old getting ''', person.hisher(), ''' first spanking," says Alondra. "You've gotta be what, early twenties by now? Figure you'd be used to it."'''],
['\n\n' + '''"Oh yes," says ''', universal.state.player.name, ''' sarcastically. "And what are you? Early to mid twenties? Yet, Ildri still seems more than capable of making you shriek and kick."'''],
['\n\n' + '''"Yeah, but that's Ildri," says Alondra. "She hits like a sauropod."'''],
['\n\n' + universal.state.player.name, ''' grumbles under ''', person.hisher(), ''' breath.''']])
        ep2_alondra_no_curfew.children = []
        ep2_alondra_no_curfew.playerComments = []

        if universal.state.player.is_female():
            ep2_alondra_no_curfew.children = ep2_alondra_rub.children
            conversation.say_node(ep2_alondra_rub.index)
        elif True:
            ep2_alondra_no_curfew.children = ep2_alondra_spanking_done.children
            conversation.say_node(ep2_alondra_spanking_done.index)

    ep2_alondra_no_curfew.quip_function = ep2_alondra_no_curfew_quip_function
    ep2_ventilate_maam = conversation.Node(361)
    def ep2_ventilate_maam_quip_function():

        ep2_ventilate_maam.quip = universal.format_text_translate([['\n\n' + '''Alondra nods in satisfaction as she stops outside their room. "Glad to see you're accepting this. I can't stand it when people don't take responsibility."''']])
        ep2_ventilate_maam.children = []
        ep2_ventilate_maam.playerComments = []

        ep2_ventilate_maam.children = ep2_ventilate_meek_enter_room.children
        conversation.say_node(ep2_ventilate_meek_enter_room.index)

    ep2_ventilate_maam.quip_function = ep2_ventilate_maam_quip_function
    ep2_ventilate_but = conversation.Node(362)
    def ep2_ventilate_but_quip_function():

        ep2_ventilate_but.quip = universal.format_text_translate([['\n\n' + '''"No buts," says Alondra sharply, stopping outside their door. She turns and lands a sharp smack to ''', universal.state.player.name, "'s", ''' bottom. "We are going to go in there, you are going to open the windows, and then you'll take what's coming to you, and you'll take it like an adult. Understand?"'''],
['\n\n' + universal.state.player.name, ''' nods, gnawing anxiously at a fingernail.''']])
        ep2_ventilate_but.children = []
        ep2_ventilate_but.playerComments = []

        ep2_ventilate_but.children = ep2_ventilate_meek_enter_room.children
        conversation.say_node(ep2_ventilate_meek_enter_room.index)

    ep2_ventilate_but.quip_function = ep2_ventilate_but_quip_function
    ep2_talk_about_teaching = conversation.Node(363)
    def ep2_talk_about_teaching_quip_function():

        
        ep2_talk_about_teaching.quip = universal.format_text_translate([['\n\n' + '''"You teaching Anne today?" asks Ildri as she watches Alondra pound dough.'''],
['\n\n' + universal.state.player.name, ''' nods, but doesn't look up from ''', person.hisher(), ''' food.'''],
['\n\n' + '''"How's that going?" asks Alondra.''']])
        ep2_talk_about_teaching.children = [ep2_enjoy_teaching, ep2_frustrated_teaching]
        ep2_talk_about_teaching.playerComments = ['''"Pretty good, actually. Just the other day, I helped her create a swirl of sparkles, and send them dancing across a large shrub behind the smithy. Madre, she was so excited!"''','''"Amor de la Madre, it's hard. She doesn't understand the simplest of concepts, and she'll try for all of five seconds before giving up and pouting, or worse throwing a tantrum. It doesn't help that I have to running to Peter anytime she acts up. I swear, sometimes I just want to give her a good hard swat or two."''']

        

    ep2_talk_about_teaching.quip_function = ep2_talk_about_teaching_quip_function
    ep2_enjoy_teaching = conversation.Node(364)
    def ep2_enjoy_teaching_quip_function():

        ep2_enjoy_teaching.quip = universal.format_text_translate([['\n\n' + '''"Awesome," says Alondra, grinning widely. "How well-behaved is she?"'''],
['\n\n' + universal.state.player.name, ''' shrugs. "As well behaved as any five year old. She has her good days and bad."'''],
['\n\n' + '''Alondra winces. "Hope she's better behaved than some of my siblings. They're royal terrors. Drove me crazy before... I mean, well-"'''],
['\n\n' + '''Alondra's voice trails off lamely, and an awkward silence descends on the kitchen.'''],
['\n\n' + '''"Anyway," says ''', universal.state.player.name, '''. "I should probably get going. Don't want to keep Peter waiting."'''],
['\n\n' + '''"Have fun," says Ildri, patting Alondra on the shoulder, and flashing ''', universal.state.player.name, ''' a smile.''']])
        ep2_enjoy_teaching.children = []
        ep2_enjoy_teaching.playerComments = []

        ep2_enjoy_teaching.children = ep2_enter_guild.children
        conversation.say_node(ep2_enter_guild.index)

    ep2_enjoy_teaching.quip_function = ep2_enjoy_teaching_quip_function
    ep2_frustrated_teaching = conversation.Node(365)
    def ep2_frustrated_teaching_quip_function():

        ep2_frustrated_teaching.quip = universal.format_text_translate([['\n\n' + '''Ildri gives ''', universal.state.player.name, ''' a stern look. "Now don't go thinking that. Girl's too young to be swatted."'''],
['\n\n' + '''"I never said I would," mutters ''', universal.state.player.name, '''. "Just wish I had some power to discipline her."'''],
['\n\n' + '''"Well, you be careful all the same. The more you think about it, the more comfortable you get with the idea," says Ildri. "The more comfortable you get with it, the more likely you'll lose your temper and actually do it."'''],
['\n\n' + '''"Stegosaur shit," mutters ''', universal.state.player.name, '''. "There's a huge gap between thinking and doing."'''],
['\n\n' + '''"Just giving a friendly warning." Ildri's lips contort into a sardonic twist. "Trust me, children push your patience to the breaking point and beyond, and in the heat of the moment it's very easy to do something you'll regret."'''],
['\n\n' + '''"Anyway," says ''', universal.state.player.name, ''' curtly, briskly cleaning up after ''', person.himselfherself(), ''' and making ''', person.hisher(), ''' way towards the hole in the wall. "I need to be going. Thanks for the breakfast."'''],
['\n\n' + '''"Young ''', person.manlady(), ''' if you try to use that hole as a door, I will turn your bottom redder than a maiden's cheeks on her wedding night," says Ildri sharply.'''],
['\n\n' + universal.state.player.name, ''' freezes, then quickly pivots and walks to the door. "What are you talking about? I wasn't going to go through the hole in the wall. I was just, you know, stretching my legs a little."'''],
['\n\n' + '''"Of course," says Ildri, giving ''', universal.state.player.name, ''' a skeptical look. "Also, did you forget you're still wearing your pajamas? You're not going to go out without getting dressed, are you?"'''],
['\n\n' + universal.state.player.name, ''' smiles innocently as ''', person.heshe(), ''' slips through the door. "There, you see? Going through the hole makes no sense. So obviously, I was just stretching my legs. Anyway, see you later. Good luck on the bread Ali."''']])
        ep2_frustrated_teaching.children = []
        ep2_frustrated_teaching.playerComments = []

        ep2_frustrated_teaching.children = ep2_enter_guild.children
        conversation.say_node(ep2_enter_guild.index)

    ep2_frustrated_teaching.quip_function = ep2_frustrated_teaching_quip_function
    ep2_unplanned_day = conversation.Node(366)
    def ep2_unplanned_day_quip_function():

        
        ep2_unplanned_day.quip = universal.format_text_translate([['\n\n' + '''"So what are your plans for today?" asks Ildri idly, as she watches Alondra work with that pesky lump of dough.'''],
['\n\n' + universal.state.player.name, ''' shrugs. "Dunno. Probably end up helping repair the guild, but I might take a look around, first."''']])
        ep2_unplanned_day.children = []
        ep2_unplanned_day.playerComments = []

        if 'grudge_against_Maria' in textCommandsMusic.keywords():
            ep2_unplanned_day.children = ep2_guild_ildri_talk_to_maria_grudge.children
            conversation.say_node(ep2_guild_ildri_talk_to_maria_grudge.index)
        elif True:
            ep2_unplanned_day.children = ep2_guild_ildri_talk_to_maria.children
            conversation.say_node(ep2_guild_ildri_talk_to_maria.index)

    ep2_unplanned_day.quip_function = ep2_unplanned_day_quip_function
    ep2_guild_ildri_talk_to_maria_grudge = conversation.Node(367)
    def ep2_guild_ildri_talk_to_maria_grudge_quip_function():

        ep2_guild_ildri_talk_to_maria_grudge.quip = universal.format_text_translate([['\n\n' + '''"You know, you really should talk to-"'''],
['\n\n' + '''"No."'''],
['\n\n' + '''Ildri scowls. "You don't even know what I'm going to ask."'''],
['\n\n' + '''"Yes I do," says ''', universal.state.player.name, ''', glaring down at ''', person.hisher(), ''' breakfast. "You want me to talk to Maria. I have no interest."'''],
['\n\n' + '''Ildri throws her hands in the air (nearly cracking Alondra in the face in the process). "It's been a month you silly ''', person.boygirl(), '''! What could she have possibly done that was so terrible?"'''],
['\n\n' + '''"None of your business."'''],
['\n\n' + '''Ildri growls in disgust. "I swear, I oughta paddle you raw."'''],
['\n\n' + '''"So why don't you?" shoots back ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Because it wouldn't do any good," says Ildri bitterly, turning her attention back to her cooking. "I can't spank some stupid grudge out of you, would that I could."'''],
['\n\n' + '''"It's not stupid," mutters ''', universal.state.player.name, ''', glaring down at the remnants of ''', person.hisher(), ''' food.'''],
['\n\n' + '''"You know what? I really don't care. Just let me know if you want to help us repair the guild," says Ildri. "I'm sure I can find something to keep you busy."'''],
['\n\n' + '''"Fine."''']])
        ep2_guild_ildri_talk_to_maria_grudge.children = []
        ep2_guild_ildri_talk_to_maria_grudge.playerComments = []

        ep2_guild_ildri_talk_to_maria_grudge.children = ep2_enter_guild.children
        conversation.say_node(ep2_enter_guild.index)

    ep2_guild_ildri_talk_to_maria_grudge.quip_function = ep2_guild_ildri_talk_to_maria_grudge_quip_function
    ep2_guild_ildri_talk_to_maria = conversation.Node(368)
    def ep2_guild_ildri_talk_to_maria_quip_function():

        ep2_guild_ildri_talk_to_maria.quip = universal.format_text_translate([['\n\n' + '''"Well, if you find some time, drop by Maria's place and see how she's doing," says Ildri. "I don't see much of her these days, and frankly I'm a little worried."'''],
['\n\n' + universal.state.player.name, ''' shrugs. "I might. She doesn't seem to spend much time at home, though."'''],
['\n\n' + '''"Well, if you do see her, tell her we miss her," says Ildri, shifting Alondra to the side and reworking the mass of dough. "And let me know if you'd like to help repair the guild. I'm sure I can find something to keep you busy."'''],
['\n\n' + universal.state.player.name, ''' cleans up ''', person.hisher(), ''' breakfast. "Anyway, I'm going to get going. See you two later."'''],
['\n\n' + '''"See you," says Alondra, flashing ''', universal.state.player.name, ''' a smile.''']])
        ep2_guild_ildri_talk_to_maria.children = []
        ep2_guild_ildri_talk_to_maria.playerComments = []

        ep2_guild_ildri_talk_to_maria.children = ep2_enter_guild.children
        conversation.say_node(ep2_enter_guild.index)

    ep2_guild_ildri_talk_to_maria.quip_function = ep2_guild_ildri_talk_to_maria_quip_function
    ep2_enter_guild = conversation.Node(369)
    def ep2_enter_guild_quip_function():

        ep2_enter_guild.quip = universal.format_text_translate([['\n\n' + '''Her clear blue eyes briefly lock with ''', universal.state.player.name, "'s", ''', and her lips quirk up into a smirk. Then, she returns her gaze to the rest of the room.''']])
        ep2_enter_guild.children = []
        ep2_enter_guild.playerComments = []

        

    ep2_enter_guild.quip_function = ep2_enter_guild_quip_function
    ep2_guild_wake_up_introvert = conversation.Node(370)
    def ep2_guild_wake_up_introvert_quip_function():

        
        ep2_guild_wake_up_introvert.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, "'s", ''' eyes flutter open. A bit of early morning sunshine is shining in through the window. ''', person.HeShe(), ''' stretches for a moment, then rolls out of bed.'''],
['\n\n' + '''Alondra is already sitting on her bed, pulling on her boots. "Morning sleepyhead. Ready for another exciting day as an adventurer in Avernum?"'''],
['\n\n' + universal.state.player.name, ''' grunts. "Oh yes. Another day playing at carpentry while waiting for an actual adventuring job. I swear, if something doesn't happen soon, I might join the Vengadores. Just for something to do."'''],
['\n\n' + '''Alondra's smile fades. "Please don't say that. Don't even joke about it."'''],
['\n\n' + '''"Right," says ''', universal.state.player.name, ''', changing out of ''', person.hisher(), ''' pajamas, and into ''', person.hisher(), ''' day clothing. "Sorry."'''],
['\n\n' + '''Alondra shrugs, running a thick, wide bone hairbrush through her hair. "Not a big deal."''']])
        ep2_guild_wake_up_introvert.children = []
        ep2_guild_wake_up_introvert.playerComments = []

        if universal.state.player.long_hair():
            ep2_guild_wake_up_introvert.children = ep2_alondra_borrow_brush.children
            conversation.say_node(ep2_alondra_borrow_brush.index)
        elif True:
            ep2_guild_wake_up_introvert.children = ep2_alondra_walk_to_kitchen.children
            conversation.say_node(ep2_alondra_walk_to_kitchen.index)

    ep2_guild_wake_up_introvert.quip_function = ep2_guild_wake_up_introvert_quip_function
    ep2_alondra_borrow_brush = conversation.Node(371)
    def ep2_alondra_borrow_brush_quip_function():

        
        ep2_alondra_borrow_brush.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' eyes Alondra's hairbrush, running ''', person.hisher(), ''' fingers through ''', person.hisher(), ''' own unruly hair. "So, think I could borrow that?"'''],
['\n\n' + '''Alondra ''', universal.format_line(['''eyes ''', universal.state.player.name, ''', a slight smile on her lips.''']) if universal.state.player.is_female() else universal.format_line(['''eyes ''', universal.state.player.name, ''' warily.''']), ''' "I don't know. This brush is a family heirloom, you know. Can't just loan it out to anybody."'''],
['\n\n' + '''"Aww, come on, Ali," says ''', universal.state.player.name, ''', tuggging futiley at a knot. "My hair's a complete mess, and my brush broke yesterday. You can trust me, I swear."''']])
        ep2_alondra_borrow_brush.children = []
        ep2_alondra_borrow_brush.playerComments = []

        if universal.state.player.is_female():
            ep2_alondra_borrow_brush.children = ep2_alondra_brush_hair.children
            conversation.say_node(ep2_alondra_brush_hair.index)
        elif True:
            ep2_alondra_borrow_brush.children = ep2_alondra_lets_you_borrow_brush_male.children
            conversation.say_node(ep2_alondra_lets_you_borrow_brush_male.index)

    ep2_alondra_borrow_brush.quip_function = ep2_alondra_borrow_brush_quip_function
    ep2_alondra_brush_hair = conversation.Node(372)
    def ep2_alondra_brush_hair_quip_function():

        
        ep2_alondra_brush_hair.quip = universal.format_text_translate([['\n\n' + '''Alondra's slight smile widens into a playful grin. "I trust nobody. You want your hair brushed? Then, I've got to do it."'''],
['\n\n' + universal.state.player.name, ''' rolls ''', person.hisher(), ''' eyes. "Fine. You big jerk."'''],
['\n\n' + '''"Who you calling big?" asks Alondra. She walks over to ''', universal.state.player.name, ''', and gives ''', person.himher(), ''' a playful swat on the thigh.'''],
['\n\n' + '''"Only in the figurative sense, of course," says ''', universal.state.player.name, ''', grinning.'''],
['\n\n' + '''"Of course." Alondra crawls onto the bed, and sits on her heels behind ''', universal.state.player.name, '''. Her legs brush against ''', universal.state.player.name, "'s", ''' hips, as she scootches forward to better get at the other Taironan's tangled hair.''']])
        ep2_alondra_brush_hair.children = [ep2_attracted_to_alondra, ep2_not_attracted_to_alondra]
        ep2_alondra_brush_hair.playerComments = ['''Feel a flutter in your belly at Alondra's contact.''','''React neutrally to Alondra's contact.''']

        

    ep2_alondra_brush_hair.quip_function = ep2_alondra_brush_hair_quip_function
    ep2_attracted_to_alondra = conversation.Node(373)
    def ep2_attracted_to_alondra_quip_function():

        
        
        ep2_attracted_to_alondra.quip = universal.format_text_translate([['\n\n' + '''As Alondra brushes ''', person.hisher(), ''' hair, ''', universal.state.player.name, ''' becomes acutely aware of the other woman's closeness. As Alondra shifts in the brushing, ''', universal.state.player.name, ''' can feel the other Taironan's generous breasts brush up against ''', person.hisher(), ''' back, leaving a tingling fire across ''', universal.state.player.name, "'s", ''' skin, even through the thin cloth of ''', person.hisher(), ''' pajamas. Alondra's knee-length wool skirt has hiked itself about a third up her thighs, leaving bare skin touching ever so lightly against ''', universal.state.player.name, "'s", ''' hips. ''', universal.state.player.name, "'s", ''' stomach tightens, and ''', person.heshe(), ''' shifts ''', person.hisher(), ''' legs slightly, pressing them a hair more against Alondra's.'''],
['\n\n' + '''"You have very nice hair," says Alondra. Her hairbrush runs into a knot. "Stubborn hair. But nice hair."'''],
['\n\n' + '''She starts sharply tugging on the hairbrush, trying to force it past the knot.'''],
['\n\n' + '''"Oww!" yelps ''', universal.state.player.name, ''', reaching back to grab her hair. "Careful."'''],
['\n\n' + '''"Oh, hush," says Alondra, guiding ''', universal.state.player.name, "'s", ''' hands away. "Seriously, if you can take getting stabbed, you can take a rough hairbrushing."'''],
['\n\n' + '''"Just because I've felt worse, doesn't mean it's pleasant," mutters ''', universal.state.player.name, ''' petulantly.'''],
['\n\n' + '''"You are such a whiner," says Alondra gently, as her hairbrush finally breaks through the knot. She pauses, and runs her free fingers through ''', universal.state.player.name, "'s", ''' hair, her fingers lightly brushing the back of ''', person.hisher(), ''' neck. "There, that wasn't so bad was it?"''']])
        ep2_attracted_to_alondra.children = []
        ep2_attracted_to_alondra.playerComments = []

        if 'lesbian_in_denial' in textCommandsMusic.keywords():
            ep2_attracted_to_alondra.children = ep2_alondra_denial.children
            conversation.say_node(ep2_alondra_denial.index)
        elif True:
            ep2_attracted_to_alondra.children = ep2_alondra_enjoy.children
            conversation.say_node(ep2_alondra_enjoy.index)

    ep2_attracted_to_alondra.quip_function = ep2_attracted_to_alondra_quip_function
    ep2_alondra_denial = conversation.Node(374)
    def ep2_alondra_denial_quip_function():

        ep2_alondra_denial.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, "'s", ''' heartrate skyrockets at Alondra's light touch. ''', person.HeShe(), ''' can feel ''', person.hisher(), ''' friend lean forward a little, to put a bit more 'oomph' in her strokes, her breasts now very lightly pressing against ''', universal.state.player.name, "'s", ''' back, instead of merely brushing against it. ''', universal.state.player.name, ''' swears ''', person.heshe(), ''' can feel Alondra's bare thighs tighten ever so slightly against ''', person.hisher(), ''' hips.'''],
['\n\n' + '''"You know," says ''', universal.state.player.name, ''', leaning forward suddenly (and nearly yanking the hairbrush from Alondra's grasp). "I think that's enough."'''],
['\n\n' + '''"What?" says Alondra, looking a bit uneasy. "But, your hair's still riddled with knots."'''],
['\n\n' + '''"Yeah, but this is a great improvement already," says ''', universal.state.player.name, '''. "And you know, it's going to get all sweaty and messy anyway, probably, right? So, no need to put a lot of effort into it, you know. Cause it'd just, you know, get messy again."'''],
['\n\n' + '''"But-"'''],
['\n\n' + '''There's a slight knock on the door.'''],
['\n\n' + '''"Alondra, hurry up!" calls Ildri's voice. "We got a bunch of hungry adventurers on the verge of waking up, and I need your help making them breakfast!"'''],
['\n\n' + '''"Yes ma'am," says Alondra, scurrying off the bed. She slips her hairbrush into a small satchel, and pulls the satchel over her head. "Coming, coming."'''],
['\n\n' + '''Alondra quickly runs out, leaving ''', universal.state.player.name, ''' alone in their room.'''],
['\n\n' + universal.state.player.name, ''' takes a deep breath, and runs a hand through ''', person.hisher(), ''' gnarled hair.'''],
['\n\n' + '''That was weird. Must have some weird hair brushing fetish. ''', universal.format_line(['''Maybe Peter'd be interested in brushing ''', person.hisher(), ''' hair? ''', universal.state.player.name, ''' thinks about it for a moment, but just can't seem to muster up the same reaction ''', person.heshe(), ''' had when it was Alondra. ''', person.HeShe(), ''' quickly pushes the thought from ''', person.hisher(), ''' head, and focuses on the rest of ''', person.hisher(), ''' day.''']) if 'flirting_with_Peter' in textCommandsMusic.keywords() else universal.format_line(['''Right. That's it exactly. Just need to find the right man, who'd be willing to brush her hair. Yes. Of course. Easy peasy.''']), ''''''],
['\n\n' + '''Some breakfast sounds really good.''']])
        ep2_alondra_denial.children = []
        ep2_alondra_denial.playerComments = []

        

    ep2_alondra_denial.quip_function = ep2_alondra_denial_quip_function
    ep2_alondra_enjoy = conversation.Node(375)
    def ep2_alondra_enjoy_quip_function():

        
        ep2_alondra_enjoy.quip = universal.format_text_translate([['\n\n' + '''"Oh, it was terrible," says ''', universal.state.player.name, ''', a smile playing across ''', person.hisher(), ''' lips. ''', person.HeShe(), ''' leans back a little, reveling in the warm softness of Alondra's chest against ''', person.hisher(), ''' back. "Worst pain ever."'''],
['\n\n' + '''"Cheeky brat," says Alondra playfully. She gives ''', universal.state.player.name, ''' a slight push forward. "But lean forward a little. Can't get at your hair from this angle."''']])
        ep2_alondra_enjoy.children = [ep2_alondra_flirt, ep2_alondra_lean_forward]
        ep2_alondra_enjoy.playerComments = ['''"No. I don't want to."''','''Lean forward''']

        

    ep2_alondra_enjoy.quip_function = ep2_alondra_enjoy_quip_function
    ep2_alondra_flirt = conversation.Node(376)
    def ep2_alondra_flirt_quip_function():

        
        ep2_alondra_flirt.quip = universal.format_text_translate([['\n\n' + '''"Oh really?" asks Alondra quietly, her hot breath tickling ''', universal.state.player.name, "'s", ''' ear. Her fingers begin to dance across ''', universal.state.player.name, "'s", ''' sides, sending squirmy lines of fire shooting through ''', person.hisher(), ''' skin. "You better lean forward right now, or I'll have to choice but to punish you."'''],
['\n\n' + universal.state.player.name, ''' turns her head, and flashes a mischievous grin, then leans backward.'''],
['\n\n' + '''"Ohh, that does it." Alondra drops the hairbrush. The fingers of one hand slip up and begin dancing lightly across the skin of ''', universal.state.player.name, "'s", ''' neck, while the fingers of the other start crawling across ''', universal.state.player.name, "'s", ''' stomach.'''],
['\n\n' + universal.state.player.name, ''' squirms, and giggles at the tingling bolts racing across ''', person.hisher(), ''' skin. ''', person.HisHer(), ''' ''', universal.state.player.muscle_adj(), ''' bottom pushes back against Alondra's groin, ''', person.hisher(), ''' swaying hips rubbing ''', person.hisher(), ''' ''', universal.state.player.bum_adj(), ''' cheeks against Alondra's warmth. ''', person.HisHer(), ''' torso writhes beneath Alondra's tickling, mashing Alondra's cushiony breasts against ''', person.hisher(), ''' back.'''],
['\n\n' + person.HeShe(), ''' can feel the rapid rise and fall Alondra's breathing, the soft scrape of the other woman's shapely legs against ''', person.hisher(), ''' own. ''', person.HeShe(), ''' can even feel the rapid thud of the other woman's heartbeat. Or maybe that's ''', person.hisher(), ''' own.'''],
['\n\n' + '''"Surrender," hisses Alondra into ''', universal.state.player.name, "'s", ''' ear, the hand tickling ''', universal.state.player.name, "'s", ''' neck slips down, and starts tickling ''', person.hisher(), ''' armpit.'''],
['\n\n' + '''"Never," breathes ''', universal.state.player.name, ''', ''', person.hisher(), ''' squirming intensifying.'''],
['\n\n' + '''"Then you leave me no choice." Alondra wraps one arm around ''', universal.state.player.name, "'s", ''' waist. With the other (and her legs), she heaves herself slightly off the bed, and spins around, essentially rolling on top of ''', universal.state.player.name, ''' in place.'''],
['\n\n' + universal.state.player.name, ''' gasps, as Alondra's warm softness is replaced with the bed. Instead, ''', person.heshe(), ''' finds ''', person.himselfherself(), ''' looking up at Alondra's cheerily determined face. Alondra straddles ''', universal.state.player.name, ''', locking her legs around ''', universal.state.player.name, "'s", ''' hips.'''],
['\n\n' + '''"You know," says ''', universal.state.player.name, ''' breathlessly. "Can't comb my hair from there."'''],
['\n\n' + '''"Who said I was going to comb your hair?" Alondra leans forward slightly, and begins mercilessly tickling ''', universal.state.player.name, "'s", ''' sides. She grins wolfishly.'''],
['\n\n' + universal.state.player.name, ''' squeals and giggles, her body writhing ever more desperately beneath Alondra's intensifying tickling.'''],
['\n\n' + '''Finally, ''', universal.state.player.name, ''' can't take it anymore. "Ok, ok, I surrender!"'''],
['\n\n' + '''"Are you going to let me comb your hair properly?" asks Alondra.'''],
['\n\n' + '''"Yes, yes," gasps ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Are you sorry for not letting me comb your hair?" asks Alondra.'''],
['\n\n' + '''"Yes, yes I'm sorry. I won't do it again."'''],
['\n\n' + '''"Liar." Alondra gives ''', universal.state.player.name, ''' one last tickle.'''],
['\n\n' + universal.state.player.name, ''' pouts. "I'm not a liar, I swear."'''],
['\n\n' + '''Before Alondra can respond, a loud knock comes at the door.'''],
['\n\n' + '''"Alondra, hurry up!" calls Ildri's from outside the door. "We got a guild full of adventurers on the verge of waking up, and they'll be expecting breakfast!"'''],
['\n\n' + '''Alondra sighs sadly. "Duty calls."'''],
['\n\n' + '''"Indeed. Isn't life full of hardship?" says ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Cheeky brat," says Alondra, swinging herself off of ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Alondra, don't make me come in there," calls Ildri sternly.'''],
['\n\n' + '''"Coming, coming," says Alondra, straightening her clothing, and hair. She flashes ''', universal.state.player.name, ''' a smile. "Your hair's still a mess. Feel free to use my comb to finish it up."''']])
        ep2_alondra_flirt.children = []
        ep2_alondra_flirt.playerComments = []

        ep2_alondra_flirt.children = ep2_alondra_lets_you_borrow_brush.children
        conversation.say_node(ep2_alondra_lets_you_borrow_brush.index)

    ep2_alondra_flirt.quip_function = ep2_alondra_flirt_quip_function
    ep2_not_attracted_to_alondra = conversation.Node(377)
    def ep2_not_attracted_to_alondra_quip_function():

        ep2_not_attracted_to_alondra.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' sighs, and relaxes. ''', person.HeShe(), ''' winces a few times, when Alondra encounters a particularly stubborn knot, but the feeling is generally soothing.'''],
['\n\n' + universal.state.player.name, ''' finds ''', person.himselfherself(), ''' going back years and years, to a few fragmented memories of ''', person.hisher(), ''' mother combing ''', person.hisher(), ''' hair, and humming gently. It was part of their evening ritual. Every night, mother would comb her hair, then she'd comb ''', universal.state.player.name, "'s", ''', before putting ''', person.himher(), ''' to bed.'''],
['\n\n' + '''Least, until those men came.'''],
['\n\n' + universal.state.player.name, ''' shudders.'''],
['\n\n' + '''"Sorry," says Alondra, tugging the brush through a particularly stubborn knot. "Your hair's stubborn enough to put a rough tree fern to shame."'''],
['\n\n' + '''"Oh, it's not that it's...nevermind."'''],
['\n\n' + '''A knock comes at the door. "Alondra are you up? We've got a bunch of adventurers on the verge of waking, and they're gonna be hungry."'''],
['\n\n' + '''"Yes, Ildri," calls Alondra. She sighs with a hint of sadness as she crawls off the bed. She tosses the hairbrush on the bed. "Here, your hair's still a mess. Just put it back on my bed when you're done alright?"''']])
        ep2_not_attracted_to_alondra.children = []
        ep2_not_attracted_to_alondra.playerComments = []

        ep2_not_attracted_to_alondra.children = ep2_alondra_lets_you_borrow_brush.children
        conversation.say_node(ep2_alondra_lets_you_borrow_brush.index)

    ep2_not_attracted_to_alondra.quip_function = ep2_not_attracted_to_alondra_quip_function
    ep2_alondra_lean_forward = conversation.Node(378)
    def ep2_alondra_lean_forward_quip_function():

        ep2_alondra_lean_forward.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' leans forward obligingly. ''', person.HeShe(), ''' feels a bit of disappointment when ''', person.hisher(), ''' back get out of range of Alondra's breasts. Feeling a touch petulant, ''', universal.state.player.name, ''' rests an elbow on Alondra's thigh, and puts ''', person.hisher(), ''' chin in ''', person.hisher(), ''' hand.'''],
['\n\n' + '''"Hey!" yelps Alondra. "Get that bony-ass elbow off my leg."'''],
['\n\n' + '''"My elbow is not bony," says ''', universal.state.player.name, ''' indignantly, pushing ''', person.hisher(), ''' elbow a bit deeper into Alondra's thigh.'''],
['\n\n' + '''Alondra yelps, and pulls her thigh away from ''', universal.state.player.name, "'s", ''' arm (smacking her other thigh against ''', universal.state.player.name, "'s", ''' in the process). "Are you kidding? It's ''', universal.format_line(['''even bonier than the rest of you!"''']) if universal.state.player.bodyType == 'slim' or universal.state.player.bodyType == 'average' else universal.format_line(['''the boniest cursed piece of bone in the history of boniness!"'''])],
['\n\n' + universal.format_line(['''"I am not bony!"''']) if universal.state.player.bodyType == 'slim' or universal.state.player.bodyType == 'average' else universal.format_line(['''"It is not!"''']), ''' cries ''', universal.state.player.name, '''.'''],
['\n\n' + universal.format_line(['''"Are you kidding? You are the Mistress of Bones. Bony McBonemistress, that's you," says Alondra with a playful grin.''']) if universal.state.player.bodyType == 'slim' or universal.state.player.bodyType == 'average' else universal.format_line(['''"It is so!" shoots back Alondra, grinning playfully.'''])],
['\n\n' + '''"Ooh, I'll show you bony." ''', universal.state.player.name, ''' spins around, and pushes Alondra onto her back. ''', person.HeShe(), ''' locks ''', person.hisher(), ''' legs around Alondra's waist, and begins mercilessly tickling the other Taironan.'''],
['\n\n' + '''Alondra squeals, and starts squirming, her curvy hips rubbing and grinding against ''', universal.state.player.name, "'s", ''' groin. ''', universal.state.player.name, "'s", ''' lower stomach tightens, and a warm tingle spreads throughout ''', person.hisher(), ''' lower regions.'''],
['\n\n' + '''"Careful," says Alondra breathlessly. "You keep this up, and you'll awaken the Tickle Monster."'''],
['\n\n' + '''"Are you kidding?" says ''', universal.state.player.name, ''', ''', person.hisher(), ''' fingers dancing across Alondra' flat belly, and smooth sides. The woman's tunic begins to ride up, and ''', universal.state.player.name, "'s", ''' fingers take advantage of the exposure, skittering across the woman's bare flesh. "That Monster has already awoken, and it is I!"'''],
['\n\n' + '''Alondra giggles at ''', universal.state.player.name, "'s", ''' touch. "I warned you. Can't be held responsible for what happens next."'''],
['\n\n' + '''Alondra wraps her arms around ''', universal.state.player.name, "'s", ''' torso, and yanks the ''', person.manwoman(), ''' tight against her body. ''', universal.state.player.name, ''' gasps as Alondra's generous bosom mashes against ''', universal.state.player.name, "'s", ''' ''', universal.format_line(['''much smaller chest''']) if universal.state.player.bodyType == 'slim' else universal.format_line([''''''])],
[universal.format_line(['''slightly smaller chest''']) if universal.state.player.bodyType == 'average' else universal.format_line([''''''])],
[universal.format_line(['''equally large breasts''']) if universal.state.player.bodyType == 'voluptuous' else universal.format_line(['''even larger chest''']), '''. A shock races through ''', universal.state.player.name, "'s", ''' body, as Alondra's hot curves press up against ''', person.hisher(), ''' own.'''],
['\n\n' + '''Then, Alondra rolls, around on top of ''', universal.state.player.name, '''. The two teeter on the edge of the bed, but a bit of scooching, brings them back onto the bed, and suddenly their positions are reversed.'''],
['\n\n' + '''Now, ''', universal.state.player.name, ''' is lying helplessly on the bed, while Alondra towers over ''', person.himher(), ''', her soft thighs locked around ''', universal.state.player.name, "'s", ''' ''', universal.format_line(['''slender''']) if universal.state.bodyType == 'slim' else universal.format_line([''''''])],
[universal.format_line(['''slightly flared''']) if universal.state.body.bodyType == 'average' else universal.format_line([''''''])],
[universal.format_line(['''curvaceous''']) if universal.state.bodyType == 'voluptuous' else universal.format_line(['''generous''']), ''' hips.'''],
['\n\n' + '''Alondra flicks her head, tossing some hair out of her face. She grins wolfishly down at ''', universal.state.player.name, '''. "Brace yourself, ''', person.boygirl(), '''. Alondra's vengeance is at hand!"'''],
['\n\n' + '''"OOh, I'm so scared," says ''', universal.state.player.name, ''', widening ''', person.hisher(), ''' eyes in mock terror. "What are you gonna do? Tickle me to death?"'''],
['\n\n' + '''Alondra puts her hand to her chest in mock shock. "How could have possibly known that? Are you psychic?"'''],
['\n\n' + '''"Better believe it." ''', universal.state.player.name, ''' puts ''', person.hisher(), ''' fingers to ''', person.hisher(), ''' forehead. "Now watch as I make you get off and apologize!"'''],
['\n\n' + '''"Not if I have anything to say about it!" Alondra leans forward, and starts racing her fingers up and down ''', universal.state.player.name, "'s", ''' side. ''', universal.state.player.name, ''' yelps, and her hands snap down to try to push away Alondra's.'''],
['\n\n' + '''Alondra catches ''', universal.state.player.name, "'s", ''' wrists, and pins them against the other Taironan's chest. "Silly girl. You cannot stop me!"'''],
['\n\n' + '''Alondra's free hand begins roaming across ''', universal.state.player.name, "'s", ''' belly, sides, and even up into ''', person.hisher(), ''' armpits, expertly seeking out all of ''', universal.state.player.name, "'s", ''' most ticklish spots.'''],
['\n\n' + universal.state.player.name, ''' giggles, and yelps, ''', person.hisher(), ''' body writhing beneath Alondra's, ''', person.hisher(), ''' breath coming in ever more rapid gasps.'''],
['\n\n' + '''"Say you're sorry for jabbing me with your elbow," says Alondra, as her fingers find a particularly sensitive spot that sends ''', universal.state.player.name, ''' into fits.'''],
['\n\n' + '''"I'm sorry, I'm sorry," gasps ''', universal.state.player.name, ''', trying half-heartedly to break ''', person.hisher(), ''' hands free of Alondra's grip.'''],
['\n\n' + '''"Sorry for what?" asks Alondra, her fingers racing down ''', universal.state.player.name, "'s", ''' side and walking feather-light across ''', universal.state.player.name, "'s", ''' belly, just above the belly button.'''],
['\n\n' + '''"Sorry for jabbing you with my elbow," breaths ''', universal.state.player.name, '''.'''],
['\n\n' + '''"And?"'''],
['\n\n' + '''"And for tickling you," says ''', universal.state.player.name, '''. She giggles, and squirms a bit harder. "I won't do it again, I promise."'''],
['\n\n' + '''"Liar," says Alondra. "I don't think you've learned your lesson at all."'''],
['\n\n' + '''Then, a pounding comes at the door. "Alondra are you up? You better be up! We've got hungry adventurers on the verge of waking up!"'''],
['\n\n' + '''Alondra sighs in disappointment. "Alas, duty calls."'''],
['\n\n' + '''"I'd like three Othnielosaurus eggs, sunny side up with a side of bread, and a few strips of iguanadon jerky," says ''', universal.state.player.name, ''', smirking.'''],
['\n\n' + '''"You'll get what we feed you," says Alondra, clambering off of ''', universal.state.player.name, '''. "And you'll like it."'''],
['\n\n' + universal.state.player.name, ''' sticks out ''', person.hisher(), ''' tongue at Alondra, who sticks out her tongue right back.'''],
['\n\n' + '''"Alondra, don't make me come in there," says Ildri through the door.'''],
['\n\n' + '''"Coming, coming," says Alondra quickly. Her eyes light on the hairbrush, resting on the bed next to ''', universal.state.player.name, "'s", ''' head. "Your hair's still a mess. Feel free to use the hairbrush. Just, put it back when you're done, alright?"''']])
        ep2_alondra_lean_forward.children = []
        ep2_alondra_lean_forward.playerComments = []

        ep2_alondra_lean_forward.children = ep2_alondra_lets_you_borrow_brush.children
        conversation.say_node(ep2_alondra_lets_you_borrow_brush.index)

    ep2_alondra_lean_forward.quip_function = ep2_alondra_lean_forward_quip_function
    ep2_alondra_lets_you_borrow_brush_male = conversation.Node(379)
    def ep2_alondra_lets_you_borrow_brush_male_quip_function():

        ep2_alondra_lets_you_borrow_brush_male.quip = universal.format_text_translate([['\n\n' + '''"Well, I guess you can borrow it," says Alondra, tossing the brush in ''', universal.state.player.name, "'s", ''' direction. "Just put it back on my bed when you're done. Now, if you'll excuse me, I need to join Ildri in the kitchen, before she gets impatient."''']])
        ep2_alondra_lets_you_borrow_brush_male.children = []
        ep2_alondra_lets_you_borrow_brush_male.playerComments = []

        ep2_alondra_lets_you_borrow_brush_male.children = ep2_alondra_lets_you_borrow_brush.children
        conversation.say_node(ep2_alondra_lets_you_borrow_brush.index)

    ep2_alondra_lets_you_borrow_brush_male.quip_function = ep2_alondra_lets_you_borrow_brush_male_quip_function
    ep2_alondra_lets_you_borrow_brush = conversation.Node(380)
    def ep2_alondra_lets_you_borrow_brush_quip_function():

        ep2_alondra_lets_you_borrow_brush.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' takes the brush and watches as Alondra leaves. What follows is a truly epic battle that will be sung about for ages. Many strands of hair nobly gave their lives in the name of ''', universal.state.player.name, ''' not looking like a crazy hobo, but in the end their sacrifices were not in vain.'''],
['\n\n' + '''When ''', person.heshe(), ''' finally finishes, ''', universal.state.player.name, ''' rubs ''', person.hisher(), ''' head, wincing a little. "Note to self: Get more cooperative hair."'''],
['\n\n' + universal.state.player.name, ''' puts the brush back on the bed. What next? Maybe some breakfast. ''', universal.state.player.name, "'s", ''' stomach gurgles. Yes, breakfast definitely sounds good.''']])
        ep2_alondra_lets_you_borrow_brush.children = []
        ep2_alondra_lets_you_borrow_brush.playerComments = []

        

    ep2_alondra_lets_you_borrow_brush.quip_function = ep2_alondra_lets_you_borrow_brush_quip_function
    ep2_alondra_walk_to_kitchen = conversation.Node(381)
    def ep2_alondra_walk_to_kitchen_quip_function():

        
        ep2_alondra_walk_to_kitchen.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' and Alondra leave their room, and start walking down the hallway towards the kitchen. On the way, they bump into Paloma, the healer. The healer's hair is a bit of a mess, and she is leaning a little on the wall as she walks.'''],
['\n\n' + '''"Paloma, you're out of bed!" says Alondra, stepping forward and giving Paloma a hug. "How you feeling?"'''],
['\n\n' + '''Paloma smiles. "Much better. Still a bit weak, but I can get up, and I can spend more than five minutes cleaning. I was even able to make it through a third of Mai's maze the other day. Even the most trivial of spellslinging makes my head throb, but I'm getting there."'''],
['\n\n' + '''"Where you off to now?" asks Alondra.'''],
['\n\n' + '''Paloma glances past the two, towards the slightly open door of Adrian's office. She blanches. "I um, have a meeting with Adrian. About taking excessive risk."'''],
['\n\n' + '''"Do you think he's going to-"'''],
['\n\n' + '''"Considering how furious he was when I finally crawled away from death's door?" Paloma swallows uneasily, and reaches back to rub her large bottom. "Almost certainly."'''],
['\n\n' + '''"What because you overexerted yourself during the attack?" asks ''', universal.state.player.name, ''' angrily. "That's absurd! I never would have made it to the armory without your help."'''],
['\n\n' + '''"And you maybe kept them from stealing one or two pieces of equipment," says Paloma, grimacing. "By spellslinging myself nearly to death, we caught a few extra Vengadores, and kept a few extra pieces of equipment. Not exactly worth my life."'''],
['\n\n' + '''"And what, almost dying wasn't punishment enough?" asks ''', universal.state.player.name, ''' sarcastically.'''],
['\n\n' + '''Paloma shrugs. "Look, I don't know how the meeting will go, just let me by so I can get it over with, alright?"'''],
['\n\n' + '''"Ok. Sorry," says ''', universal.state.player.name, ''', stepping to the side.'''],
['\n\n' + '''Paloma pats ''', universal.state.player.name, ''' on the shoulder as she walks past.'''],
['\n\n' + '''Alondra and ''', universal.state.player.name, ''' continue their way into the kitchen.'''],
['\n\n' + '''While Alondra joins Ildri at the counter to start making bread, ''', universal.state.player.name, ''' dives into the first round of bread, eggs and jerky prepared by Ildri before she came to get Alondra.'''],
['\n\n' + '''"Morning, ''', universal.state.player.name, '''," says Ildri, flashing the young ''', person.manwoman(), ''' a smile.''']])
        ep2_alondra_walk_to_kitchen.children = []
        ep2_alondra_walk_to_kitchen.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_alondra_walk_to_kitchen.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif True:
            ep2_alondra_walk_to_kitchen.children = ep2_ildri_greeting.children
            conversation.say_node(ep2_ildri_greeting.index)

    ep2_alondra_walk_to_kitchen.quip_function = ep2_alondra_walk_to_kitchen_quip_function
    ep2_ildri_indecent = conversation.Node(382)
    def ep2_ildri_indecent_quip_function():

        
        ep2_ildri_indecent.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' returns the smile as ''', person.heshe(), ''' passes Ildri on the way to the nearby, savory-smelling breakfast.'''],
['\n\n' + '''However, as ''', universal.state.player.name, ''' walks past her, Ildri's hand snaps out and catches ''', universal.state.player.name, ''' around the arm.'''],
['\n\n' + '''"Hey, what are you doing?" cries ''', universal.state.player.name, ''', twisting and looking at Ildri.'''],
['\n\n' + '''Ildri doesn't respond immediately. Instead, she just glares down at the bare, ''', universal.state.player.bum_adj(), ''' cheeks bursting free of ''', universal.state.player.name, "'s", ''' tiny ''', universal.state.player.underwear().name, '''.''']])
        ep2_ildri_indecent.children = []
        ep2_ildri_indecent.playerComments = []

        if 'Ildri_no_pants' in textCommandsMusic.keywords():
            ep2_ildri_indecent.children = ep2_no_pants_punishment.children
            conversation.say_node(ep2_no_pants_punishment.index)
        elif True:
            ep2_ildri_indecent.children = ep2_no_pants.children
            conversation.say_node(ep2_no_pants.index)

    ep2_ildri_indecent.quip_function = ep2_ildri_indecent_quip_function
    ep2_no_pants = conversation.Node(383)
    def ep2_no_pants_quip_function():

        
        
        ep2_no_pants.quip = universal.format_text_translate([['\n\n' + '''Ildri turns her gaze from ''', universal.state.player.name, "'s", ''' exposed bum, to ''', person.hisher(), ''' face. "You're not seriously planning on going out like that, are you?"''']])
        ep2_no_pants.children = [ep2_ildri_bare_backpedal, ep2_ildri_bare, ep2_ildri_bare_rude]
        ep2_no_pants.playerComments = ['''"What? No, of course not! I just you know, forgot to put on some pants. Happens to the best of us you know? In fact, I think I'll go put some pants on right now."''','''"Well, yeah. All the most famous women adventurers run around with their bottoms hanging out. Like Red Sonia, or Emma the White Cheeked."''','''"You're cursed right. And if you don't like it, you can just shut up."''']

        

    ep2_no_pants.quip_function = ep2_no_pants_quip_function
    ep2_ildri_bare_backpedal = conversation.Node(384)
    def ep2_ildri_bare_backpedal_quip_function():

        acceptableClothing = [item for item in universal.state.player.inventory if items.is_lower_clothing(item)]
        acceptableClothing = [item for item in acceptableClothing if not item.armorType == items.Underwear.armorType or not item.baring]
        
        
        
        ep2_ildri_bare_backpedal.quip = universal.format_text_translate([['\n\n' + '''"Yes," says Ildri flatly. "You do that."'''],
['\n\n' + universal.state.player.name, ''' turns and scurries back into ''', person.hisher(), ''' bedroom, and begins frantically looking for something, anything that would cover ''', person.hisher(), ''' ass.''']])
        ep2_ildri_bare_backpedal.children = []
        ep2_ildri_bare_backpedal.playerComments = []

        if acceptableClothing == []:
            ep2_ildri_bare_backpedal.children = ep2_no_acceptable_clothing.children
            conversation.say_node(ep2_no_acceptable_clothing.index)
        elif True:
            ep2_ildri_bare_backpedal.children = ep2_acceptable_clothing.children
            conversation.say_node(ep2_acceptable_clothing.index)

    ep2_ildri_bare_backpedal.quip_function = ep2_ildri_bare_backpedal_quip_function
    ep2_no_acceptable_clothing = conversation.Node(385)
    def ep2_no_acceptable_clothing_quip_function():

        
        
        ep2_no_acceptable_clothing.quip = universal.format_text_translate([['\n\n' + '''Crap. Crap crap. Crap crap crap crap. Crap crap. Crap. How could ''', person.heshe(), ''' possibly not have any clothing at all that actually covers ''', person.hisher(), ''' ass? How???'''],
['\n\n' + '''Oh man, Ildri's going to beat ''', person.hisher(), ''' ass 'till glows in the dark. Then ''', person.heshe(), ''''s going to be walking down the street with a freshly spanked bottom hanging out, yelling to all the world "I've been a naughty ''', person.boygirl(), '''!" Not cool. Not cool.'''],
['\n\n' + '''Thought ''', person.heshe(), ''' owned a pair of trousers at least. Did ''', person.heshe(), ''' get sell ''', person.hisher(), ''' trousers or something? Why did ''', person.heshe(), ''' do that? Why???'''],
['\n\n' + '''Wait. When did ''', person.heshe(), ''' do that, and how did Ildri not notice ''', person.himher(), ''' wearing ass-baring clothing before?'''],
['\n\n' + '''Oh. Right. ''', person.HeShe(), ''' sold one pair of pants. Then ''', person.heshe(), ''' had to scrounge up some money to buy them back when Alondra warned ''', person.himher(), ''' that Ildri would spank ''', person.himher(), ''' so hard ''', person.heshe(), ''''d skip black and go right to blue. Then that pair of trousers got damaged yesterday when they got caught on an exposed nail.'''],
['\n\n' + '''Ok. Don't panic. No panicking. This is a strictly no panic zone.'''],
['\n\n' + universal.state.player.name, "'s", ''' takes one last desperate look, and lights on three options. The first is the blanket on ''', person.hisher(), ''' bed. The second are the ragged remnants of ''', universal.state.player.name, "'s", ''' old trousers, currently hiding beneath ''', person.hisher(), ''' bed. The third is the small chest where Alondra keeps her spare clothing.''']])
        ep2_no_acceptable_clothing.children = [ep2_bedsheet, ep2_salvage_trousers, ep2_borrow_skirt]
        ep2_no_acceptable_clothing.playerComments = ['''Just wrap the blanket around yourself, and hope Ildri has mercy.''','''See if you can salvage the trousers''','''Borrow one of Alondra's skirts. It's an emergency after all. Surely she won't mind.''']

        

    ep2_no_acceptable_clothing.quip_function = ep2_no_acceptable_clothing_quip_function
    ep2_bedsheet = conversation.Node(386)
    def ep2_bedsheet_quip_function():

        itemspotionwars.alondrasSkirt.risque += 1 if universal.state.player.height == "tall" else 0
        itemspotionwars.alondrasSkirt.risque += 2 if universal.state.player.height == "huge" else 0
        
        
        itemspotionwars.alondrasSkirt.risque += 1 if universal.state.player.bodyType == "average" else 0
        itemspotionwars.alondrasSkirt.risque += 2 if universal.state.player.bodyType == "heavyset" else 0
        
        
        universal.state.player.take_item(itemspotionwars.alondrasSkirt)
        universal.state.player.equip(itemspotionwars.alondrasSkirt)
        
        
        
        ep2_bedsheet.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' pulls ''', person.hisher(), ''' blanket off the bed, and wraps it around ''', person.hisher(), ''' waist as an impromptu skirt. Half the cursed thing drags across the ground, and ''', person.heshe(), ''' can't go more than three steps without tripping over it, but it covers ''', person.himher(), ''' by golly!'''],
['\n\n' + '''Holding ''', person.hisher(), ''' head high, ''', universal.state.player.name, ''' marches, trips, and stumbles back into the kitchen, and proudly presents ''', person.himselfherself(), '''.'''],
['\n\n' + '''Ildri takes one look at ''', universal.state.player.name, ''', and bursts out laughing. "Don't tell me, that pair of pants you ruined yesterday were your last pair."'''],
['\n\n' + '''"It wasn't my fault," mutters ''', universal.state.player.name, ''', fidling with ''', person.hisher(), ''' "dress." "I didn't put that nail there."'''],
['\n\n' + '''Alondra frowns. "Actually, I'm pretty sure-"'''],
['\n\n' + '''"No!" says ''', universal.state.player.name, ''' quickly. "I wouldn't have just left it hanging out in pants ripping range. I mean, who would do such a silly thing as pound in a nail before all the wood was in position?"'''],
['\n\n' + '''"A Taironan ''', person.manwoman(), ''' with a hammer and a grim determination to make use of it?" says Alondra.'''],
['\n\n' + '''"Right. Not me," says ''', universal.state.player.name, '''.'''],
['\n\n' + '''Alondra rolls her eyes. "Whatever. You want to borrow one of my skirts?"'''],
['\n\n' + '''"Is that all you have?" asks ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Don't like trousers," says Alondra. "No airflow. Now come on. Let's get some real clothes on you."'''],
['\n\n' + '''A bit later, ''', universal.state.player.name, ''' is dressed in one of Alondra's skirts. ''', universal.format_line(['''While on Alondra, the skirt extends to a little bit past the knees, ''', universal.state.player.name, ''' is shorter, so the skirt goes about halfway down ''', person.hisher(), ''' shins.''']) if universal.state.player.height == "small" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''Fortunately, Alondra and ''', universal.state.player.name, ''' are roughly the same height, so the skirt extends down to a little past ''', universal.state.player.name, "'s", ''' knees, like it does on Alondra.''']) if universal.state.player.height == "average" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''''', universal.state.player.name, ''' is quite a bit taller than Alondra, so the skirt stops several inches shy of ''', universal.state.player.name, "'s", ''' knees, about two-thirds down ''', person.hisher(), ''' thighs.''']) if universal.state.player.height == "tall" else universal.format_line(['''Unfortunately, ''', universal.state.player.name, ''' is much taller than Alondra, so rather than extending to ''', person.hisher(), ''' knees, the skirt stops at best halfway down ''', person.hisher(), ''' thighs.''']), ''''''],
['\n\n' + '''Meanwhile, ''', universal.format_line(['''''', universal.state.player.name, ''' has much slimmer hips than Alondra, so the two had to track down a bit of string to tie around ''', universal.state.player.name, "'s", ''' waist, to keep the skirt from falling down.''']) if universal.state.bodyType == "slim" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''the skirt hangs a little low on ''', universal.state.player.name, "'s", ''' hips, because ''', person.hisher(), ''' hips are a little bit slimmer than Alondra's.''']) if universal.state.bodyType == "average" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''''', universal.state.player.name, ''' and Alondra have comparable hip shapes, so the skirt hangs fairly naturally, neither too loose nor too tight.''']) if universal.state.bodyType == "voluptuous" else universal.format_line(['''''', universal.state.player.name, ''' has much wider than Alondra's, forcing the skirt to cling to ''', universal.state.player.name, "'s", ''' hips much more tightly than it does to Alondra.''']), ''''''],
['\n\n' + '''"That will do," says Ildri. "Though you might want to purchase some proper clothing for yourself."'''],
['\n\n' + '''"I'll keep that in mind," says ''', universal.state.player.name, '''.''']])
        ep2_bedsheet.children = []
        ep2_bedsheet.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_bedsheet.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_bedsheet.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_bedsheet.quip_function = ep2_bedsheet_quip_function
    ep2_borrow_skirt = conversation.Node(387)
    def ep2_borrow_skirt_quip_function():

        itemspotionwars.alondrasSkirt.risque += 1 if universal.state.player.height == "tall" else 0
        itemspotionwars.alondrasSkirt.risque += 2 if universal.state.player.height == "huge" else 0
        
        
        itemspotionwars.alondrasSkirt.risque += 1 if universal.state.player.bodyType == "average" else 0
        itemspotionwars.alondrasSkirt.risque += 2 if universal.state.player.bodyType == "heavyset" else 0
        
        
        
        
        ep2_borrow_skirt.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' roots through Alondra's trunk, and pulls out a skirt that looks good. Alondra probably isn't going to be particularly happy, but surely she'll understand.'''],
['\n\n' + '''A bit later, ''', universal.state.player.name, ''' is dressed in one of Alondra's skirts. ''', universal.format_line(['''While on Alondra, the skirt extends to a little bit past the knees, ''', universal.state.player.name, ''' is shorter, so the skirt goes about halfway down ''', person.hisher(), ''' shins.''']) if universal.state.player.height == "small" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''Fortunately, Alondra and ''', universal.state.player.name, ''' are roughly the same height, so the skirt extends down to a little past ''', universal.state.player.name, "'s", ''' knees, like it does on Alondra.''']) if universal.state.player.height == "average" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''''', universal.state.player.name, ''' is quite a bit taller than Alondra, so the skirt stops several inches shy of ''', universal.state.player.name, "'s", ''' knees, about two-thirds down ''', person.hisher(), ''' thighs.''']) if universal.state.player.height == "tall" else universal.format_line(['''Unfortunately, ''', universal.state.player.name, ''' is much taller than Alondra, so rather than extending to ''', person.hisher(), ''' knees, the skirt stops at best halfway down ''', person.hisher(), ''' thighs.''']), ''''''],
['\n\n' + '''Meanwhile, ''', universal.format_line(['''''', universal.state.player.name, ''' has much slimmer hips than Alondra, so ''', universal.state.player.name, ''' to track down a bit of string to tie around ''', universal.state.player.name, "'s", ''' waist, to keep the skirt from falling down.''']) if universal.state.bodyType == "slim" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''the skirt hangs a little low on ''', universal.state.player.name, "'s", ''' hips, because ''', person.hisher(), ''' hips are a little bit slimmer than Alondra's.''']) if universal.state.bodyType == "average" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''''', universal.state.player.name, ''' and Alondra have comparable hip shapes, so the skirt hangs fairly naturally, neither too loose nor too tight.''']) if universal.state.bodyType == "voluptuous" else universal.format_line(['''''', universal.state.player.name, ''' has much wider than Alondra's, forcing the skirt to cling to ''', universal.state.player.name, "'s", ''' hips much more tightly than it does to Alondra.''']), ''''''],
['\n\n' + universal.state.player.name, ''' takes a deep breath, and makes ''', person.hisher(), ''' way back out into the kitchen.'''],
['\n\n' + '''Alondra glances at ''', universal.state.player.name, ''', and her eyes widen. "Is that one of my skirts?"'''],
['\n\n' + '''"Yeah, sorry I-"'''],
['\n\n' + '''"What the fuck?" cries Alondra.'''],
['\n\n' + universal.state.player.name, ''' blinks, and rocks back a step. "But I don't have anything-"'''],
['\n\n' + '''"So you thought it was OK to just go rooting through my stuff?" snaps Alondra, stepping up to ''', universal.state.player.name, ''' and glares ''', universal.format_line(['''down''']) if alondra.taller_than(universal.state.player) else universal.format_line(['''up''']), ''' at ''', universal.state.player.name, ''', with her fists on her hips. "You didn't think to maybe come out here and ask? You just figured 'Hey Alondra, actually bothers to cover her ass. I'm sure she won't mind if I go rooting through her private stuff without her permission. I mean, it's not like she expects me to respect her privacy or anything.' Well guess what dumbass! I do!"''']])
        ep2_borrow_skirt.children = [ep2_borrow_skirt_explain, ep2_borrow_skirt_apologize, ep2_borrow_skirt_angry]
        ep2_borrow_skirt.playerComments = ['''"But I was afraid Ildri would spank me if-"''','''"I'm sorry. I just thought it wouldn't be a big deal. I was wrong."''','''"Well there's no need to be a bitch about it. Amor de la Madre, all I did was borrow a skirt. It's not that big a deal."''']

        

    ep2_borrow_skirt.quip_function = ep2_borrow_skirt_quip_function
    ep2_borrow_skirt_explain = conversation.Node(388)
    def ep2_borrow_skirt_explain_quip_function():

        
        ep2_borrow_skirt_explain.quip = universal.format_text_translate([['\n\n' + '''"Alondra..." begins Ildri.'''],
['\n\n' + '''"Oh come on," says Alondra, throwing her arms into the air, either ignoring or not hearing Ildri. "Ildri's strict, but she's not unfair. She'd have let you explain, and then you could have borrowed something from me with my permission, and it wouldn't have been a big deal! Madre, you've been living under her roof for a month. You should know this by now."''']])
        ep2_borrow_skirt_explain.children = [ep2_borrow_skirt_apologize, ep2_borrow_skirt_angry]
        ep2_borrow_skirt_explain.playerComments = ['''"I'm sorry, I'm sorry."''','''"Look, get out of my face! Madre, you're acting like a complete bitch. It's just a skirt!"''']

        

    ep2_borrow_skirt_explain.quip_function = ep2_borrow_skirt_explain_quip_function
    ep2_borrow_skirt_apologize = conversation.Node(389)
    def ep2_borrow_skirt_apologize_quip_function():

        
        ep2_borrow_skirt_apologize.quip = universal.format_text_translate([['\n\n' + '''Alondra's glare fades into a look of mild chagrin, then a bit of shame. "I'm sorry too. I guess I can understand your concern, and it really isn't a big deal. Sorry for going off on you like that. Privacy's important to me, is all."'''],
['\n\n' + '''"I noticed," says ''', universal.state.player.name, ''' with an uneasy laugh.'''],
['\n\n' + '''"Feel free to hang onto the skirt, for now," says Alondra. "Though you might want to get yourself some proper clothing at some point."'''],
['\n\n' + '''"Yeah," says ''', universal.state.player.name]])
        ep2_borrow_skirt_apologize.children = []
        ep2_borrow_skirt_apologize.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_borrow_skirt_apologize.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_borrow_skirt_apologize.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_borrow_skirt_apologize.quip_function = ep2_borrow_skirt_apologize_quip_function
    ep2_borrow_skirt_angry = conversation.Node(390)
    def ep2_borrow_skirt_angry_quip_function():

        
        
        ep2_borrow_skirt_angry.quip = universal.format_text_translate([['\n\n' + '''"You stole one of my skirts!" snarls Alondra. "How is that not a big deal?"'''],
['\n\n' + '''"I didn't steal it," shoots back ''', universal.state.player.name, '''. "I just borrowed it without asking. But I have every plan of giving it back."'''],
['\n\n' + '''"Calm down you two," says Ildri, stepping towards the bickering pair.'''],
['\n\n' + '''"Stegosaur shit," spits Alondra. "Borrowing without asking is the exact definition of stealing!"'''],
['\n\n' + '''"No, when you steal something you have no intention of giving it back," shouts ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Both of you-" says Ildri, her voice rising.'''],
['\n\n' + '''"Says the thief so ''', person.heshe(), ''' can sleep at night," says Alondra.'''],
['\n\n' + '''"Are you calling me a thief?"'''],
['\n\n' + '''"You two need to stop," says Ildri, stepping between the two, and putting one hand against each chest.'''],
['\n\n' + '''"If the shoe fits, wear it!"'''],
['\n\n' + '''"Well, you're one to talk you Madre-cursed terrorist!"'''],
['\n\n' + '''Alondra's eyes narrow. "Shut up."'''],
['\n\n' + '''"Or what? You gonna bring in all your terrorist friends? Gonna attack the guild again?"'''],
['\n\n' + '''"Stop calling me that!"'''],
['\n\n' + '''"If the shoe fits, wear it!"'''],
['\n\n' + '''Alondra dodges past Ildri's hand and jumps on top of ''', universal.state.player.name, '''. "I'm going to beat your ass so hard a summer breeze will make you scream!"'''],
['\n\n' + universal.state.player.name, ''' grabs a fistful of Alondra's hair, and pivots, tossing Alondra against a nearby counter. "Hah! Says the kitchen girl, can't even bake a loaf of bread. You even know how to hold a knife?"'''],
['\n\n' + '''"That. Is. ENOUGH!" Ildri grabs ''', universal.state.player.name, ''', and drags ''', person.himher(), ''' backwards a few steps.'''],
['\n\n' + '''"Let go of me," snarls ''', universal.state.player.name, ''', flailing futiely in Ildri's grip. "I'm going to kick her ass!"'''],
['\n\n' + '''"I don't think so," says Ildri sharply, landing three sharp blows to ''', universal.state.player.name, "'s", ''' skirt-clad bottom, then grabbing ''', universal.state.player.name, "'s", ''' ear in a twisting pinch.'''],
['\n\n' + '''"Oww!" yelps ''', universal.state.player.name, '''. ''', person.HeShe(), ''' is forced ''', universal.format_line(['''up onto ''', person.hisher(), ''' toes''']) if ildri.taller_than(universal.state.player) else universal.format_line(['''into an awkward hunch''']), ''' by Ildri's painful grip.'''],
['\n\n' + '''"Having fun, ''', universal.state.player.nickname, '''?" asks Alondra with a smirk as she regains her feet.'''],
['\n\n' + '''Ildri lances forward and grabs Alondra's ear in a twisting pinch.'''],
['\n\n' + '''"Oww!" yelps Alondra, her smirk vanishing.'''],
['\n\n' + '''"Your behavior, both of you, is completely inappropriate," says Ildri through gritted teeth, tightening the twist on their ears. "When I'm done with the two of you..."'''],
['\n\n' + '''"By why are you spanking me?" whines Alondra. She points at ''', universal.state.player.name, '''. "I didn't do anything. It was all ''', person.hisher(), ''' fault!"'''],
['\n\n' + '''"Madre's ass it is," says ''', universal.state.player.name, ''', reaching around Ildri smacking Alondra. "You're the one who overreacted!"'''],
['\n\n' + '''"Oww! ''', universal.format_line(['''Bitch!''']) if universal.state.player.is_female() else universal.format_line(['''Asshole!''']), '''" Alondra returns the smack with one of her own.'''],
['\n\n' + '''Ildri growls. She marches the two ''', universal.format_line(['''girls''']) if universal.state.player.is_female() else universal.format_line(['''Taironans''']), ''' over the bench. Then she sits down, and hauls the both of them across her large thighs, Alondra pressed against her torso, and ''', universal.state.player.name, ''' pressed against Alondra. Despite their rapidly worsening predicament, the two girls continue to shove and slap at each other.'''],
['\n\n' + '''With two brusque motions, Ildri yanks up ''', universal.state.player.name, "'s", ''' and Alondra's skirts, exposing a pair of brown, barely clad bottoms. ''', universal.state.player.name, "'s", ''' round cheeks are practically bursting out of ''', person.hisher(), ''' teeny tiny ''', universal.state.player.underwear().name, '''. Alondra's protruding, curvy, bottom is straining against an almost-as-small pair of dark blue lace panties, that leave more than half of her jiggly bottom bare. Their naked legs grind against each other, while the two shove and slap at each other.'''],
['\n\n' + '''Ildri raises her large, callused hand, and lands a quick one-two to the exposed, naughty behinds of the two brats across her lap, sending all four round globes bouncing.'''],
['\n\n' + '''The two yelp, and they finally stop slapping at each other.'''],
['\n\n' + '''Ildri raises her hand a third time, and smashes it against Alondra's right cheek, and ''', universal.state.player.name, "'s", ''' left cheek. The two brats squeal and squirm simultaneously.'''],
['\n\n' + '''"Wait, wait Ildri I'm sorry," says Alondra, craning around to look at Ildri with wide, pleading eyes. "I didn't mean it, please-oww!"'''],
['\n\n' + '''Ildri's hand smashes against Alondra's left cheek, her face a thunderstorm. The girl's hips jump, and press hard against ''', universal.state.player.name, "'s", ''', while her kicking right leg gets entangled in ''', universal.state.player.name, "'s", ''' left.''']])
        ep2_borrow_skirt_angry.children = [ep2_ildri_double_spanking_apologize, ep2_ildri_double_spanking_unapologetic]
        ep2_borrow_skirt_angry.playerComments = ['''"Me too! I'm really really sorry, please don't spank us!"''','''"Hmmph. I'm not. You're a bitch, and a spanking isn't going to change that''']

        

    ep2_borrow_skirt_angry.quip_function = ep2_borrow_skirt_angry_quip_function
    ep2_ildri_double_spanking_apologize = conversation.Node(391)
    def ep2_ildri_double_spanking_apologize_quip_function():

        
        
        ep2_ildri_double_spanking_apologize.quip = universal.format_text_translate([['\n\n' + '''"Glad to hear it," says Ildri sharply. "Now, let's make sure you mean it."'''],
['\n\n' + '''"Wait, wait we do mean it, we do! Please don't-oww!" cries the two ''', universal.format_line(['''girls''']) if universal.state.player.is_female() else universal.format_line(['''Taironans''']), '''. Their protests are interrupted by another hard blow to Alondra's right cheek and ''', universal.state.player.name, "'s", ''' left.'''],
['\n\n' + '''Ildri's hand rises and falls, rises and falls. It thwacks sensitive sitspots, and quivering globes. It pushes away kicking legs. Sometimes it alternates between cheeks, and other times cracks against the same spot until the chastised owner is begging Ildri to spank somewhere else, anywhere else! Then, it smacks a thigh, before turning its attention to the other pair of orbs.'''],
['\n\n' + '''"I am ashamed of you two," says Ildri. She lands half a dozen quick blows to Alondra's left sitspot, then half a dozen quick blows to ''', universal.state.player.name, "'s", ''' right.'''],
['\n\n' + '''The two yelp, and cling to each other, all animosity forgotten in a desperate need for comfort, any comfort at all!'''],
['\n\n' + '''"Alondra." Ildri's voice is as sharp as the slap to the middle of Alondra's right cheek. "What were you thinking?"'''],
['\n\n' + '''"''', person.HeShe(), ''' had no right to just take one of my skirts without asking," sniffles Alondra.'''],
['\n\n' + '''"No, but it's not like ''', person.heshe(), ''' had any intention of keeping it," says Ildri. She slaps Alondra's left cheek. "So calling ''', person.himher(), ''' a thief was completely inappropriate, don't you think?"'''],
['\n\n' + '''"Yes ma'am," says Alondra glumly.'''],
['\n\n' + '''Ildri slaps the middle of Alondra's bottom, right across her crack. "Are you saying that because you mean it, or because you don't want to be spanked anymore?"'''],
['\n\n' + '''"I mean it, ma'am," mutters Alondra bitterly.'''],
['\n\n' + '''"I don't believe you." Ildri grabs Alondra's tiny panties, and tugs them down to the girl's knees.'''],
['\n\n' + '''"No, not my panties!" Alondra kicks. Her hands fly back to grab her panties (nearly whacking ''', universal.state.player.name, ''' in the face in the process). "They're not protecting me anyway!"'''],
['\n\n' + '''"Alondra, you will let go, and you will let go now," says Ildri in a tone that demands obediance.'''],
['\n\n' + '''The young woman whimpers, but forces her fingers to disentangle from her underwear. She brings her hands back around to dangle in front of her.'''],
['\n\n' + '''''', universal.format_line(['''On a whim, ''', universal.state.player.name, ''' reaches over, and takes Alondra's hand in her own. ''', person.HeShe(), ''' flashes Alondra a comforting smile through ''', person.hisher(), ''' tears. Alondra looks slightly bewildered for a moment, then returns the smile.''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''She nervously interlaces her fingers together, waiting for the spanking the resume.''']), ''''''],
['\n\n' + '''There is a sharp slap, and Alondra cries out. Her hot thigh presses against ''', universal.state.player.name, "'s", ''', while her ''', universal.format_line(['''grip on ''', universal.state.player.name, "'s", ''' hand tightens.''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''interlaced fingers tighten.''']), ''''''],
['\n\n' + '''A long staccato of cracks assault ''', universal.state.player.name, "'s", ''' ears. Alondra whimpers, yelps and cries. Her hips buck and grind, bumping repeatedly against ''', universal.state.player.name, "'s", '''''', universal.format_line([''', each bump sending a small jolt through ''', universal.state.player.name, "'s", ''' body.''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''.''']), ''''''],
['\n\n' + '''"Now," says Ildri, rubbing her hand across ''', universal.state.player.name, "'s", ''' stinging bum. "Let's talk about your behavior, ''', universal.state.player.name, ''' of Chengue."'''],
['\n\n' + '''"Yes ma'am," mutters ''', universal.state.player.name, '''.'''],
['\n\n' + '''Ildri lands a hard smack to ''', universal.state.player.name, "'s", ''' right sitspot. "Care to explain your actions?"'''],
['\n\n' + '''"I was scared," mutters ''', universal.state.player.name, '''. "I didn't have any pants or anything, and I was worried you'd spank me if I came out without wearing anything."'''],
['\n\n' + '''Ildri sighs. "Well, I'm sorry I've made you feel that way. I try not to be unreasonable, I promise. Now, what about what you said to Alondra?"'''],
['\n\n' + universal.state.player.name, ''' shifts on Ildri's lap. "She called me a thief. What did you expect?"'''],
['\n\n' + '''"I expected you to act like a mature adult," says Ildri. "I expected you to hold onto your temper, and apologize for not asking permission. If Alondra contined to make a big deal about it, then I would deal with it. Not you. Understand?"'''],
['\n\n' + '''"Why do you get to punish her and not me?" mutters ''', universal.state.player.name, '''. "I'm the one she wronged."'''],
['\n\n' + '''"Because I'm not emotionally invested in the argument," says Ildri. "Alondra hasn't attacked me, so I'm less likely to go overboard in punishing her. You, feeling hurt and insulted by her accusations, would be much more likely to spank her too hard, or too long. Understand?"'''],
['\n\n' + '''"Oh come on!" cries ''', universal.state.player.name, ''', squirming in Ildri's grip. "That didn't stop you from spanking her when she did attack you. Remember the raid?"'''],
['\n\n' + '''"That's because there was no neutral third party, not unless I wanted to hand her over the guards, and I wasn't sure I wanted to do that just yet," says Ildri. She grabs the waistband of ''', universal.state.player.name, "'s", ''' teeny ''', universal.state.player.underwear().name, ''' and tugs \itthem{universal.state.player.underwear()} down to ''', universal.state.player.name, "'s", '''. "Now hush and take the rest of your spanking."'''],
['\n\n' + universal.state.player.name, ''' groans. ''', person.HeShe(), ''' reflexively clenches ''', person.hisher(), ''' bottom, and squeezes ''', person.hisher(), ''' thighs together, as ''', person.heshe(), ''' feels the bits of fabric slide over the swell of ''', person.hisher(), ''' cheeks, and down ''', person.hisher(), ''' legs.'''],
['\n\n' + '''Then there is a sharp crack, and another wave of pain washes across ''', universal.state.player.name, "'s", ''' bottom.'''],
['\n\n' + '''This latest onslaught of pain becomes too much, and ''', universal.state.player.name, ''' starts to cry. ''', person.HisHer(), ''' naked hips squirm desperately, rubbing against the rough wool of Ildri's trousers, and pressing against Alondra's warm hip. ''', person.HisHer(), ''' legs kick in time with Ildri's heavy blows. ''', person.HisHer(), ''' right hand grabs Ildri's ankle in a deathgrip, while ''', universal.format_line(['''''', person.hisher(), ''' left hand tightens its death grip on Alondra's right.''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''balls into a fist and starts to flail wildly. Alondra grabs ''', universal.state.player.name, "'s", ''' flailing hand, and closes her fingers around it.''']), ''' Alondra's touch is small comfort in the face of the waves of pain cascading from Ildri's heavy blows out across ''', person.hisher(), ''' bottom. But it's comfort nonetheless, and ''', universal.state.player.name, ''' clings to it like a shipwrecked sailor in a storm clings to a bit of driftwood.'''],
['\n\n' + '''"Alright," says Ildri at last. She begins to gently rub some of the sting from first ''', universal.state.player.name, "'s", ''', then Alondra's bottoms. "Alondra, what have we learned?"'''],
['\n\n' + '''"Not to overreact ma'am," says Alondra, sniffling. "Also not to fight with ''', universal.state.player.name, '''."'''],
['\n\n' + '''"And ''', universal.state.player.name, '''?" asks Ildri.'''],
['\n\n' + '''"To trust you to listen to my explanation first, to ask for permission, and also not overreact," says ''', universal.state.player.name, ''', wiping some of the tears from ''', person.hisher(), ''' face. "And not to fight with Alondra."'''],
['\n\n' + '''"Good." Ildri gently pulls the panties of her two spankees back up over their respective bottoms. "Both of you get up."'''],
['\n\n' + '''The two clamber off of Ildri's lap, sorrowfully rubbing their bottoms.'''],
['\n\n' + '''"Keep those skirts up. ''', universal.state.player.name, ''', you're going to spend a half-glass in the corner with your bottom on display. Alondra, I need your help, so I can't have you standing in the corner-"'''],
['\n\n' + universal.state.player.name, "'s", ''' eyes widen. "But that's not-"'''],
['\n\n' + '''"Let me finish," says Ildri curtly. She pulls a small pin out of the red sash she keeps wrapped around her waist. "Turn around Alondra. I'm going to pin your skirt up. You're going to help me cook with your bottom exposed."'''],
['\n\n' + '''Alondra's lips thin, and her eyes narrow. Still, she turns around, and lifts her skirt back up. She also stomps her foot.'''],
['\n\n' + '''Ildri gives the girl's right cheek a warning slap. "Don't you give me any attitude. You've wasted enough of my time already."'''],
['\n\n' + '''Alondra huffs.'''],
['\n\n' + '''When Ildri finishes pinning Alondra's skirt up, she gives the girl's bum another slap. Then, she points towards the northwest corner near the ovens. "''', universal.state.player.name, ''', into the corner. Alondra, come on. We've got bread to bake."'''],
['\n\n' + universal.state.player.name, ''' shuffles into the specified corner. One of the turnspit-Coelophysis cocks its head at ''', universal.state.player.name, ''', then snifs at ''', person.hisher(), ''' exposed ass, its cold nose bumping against ''', universal.state.player.name, "'s", ''' sensitive cheeks.'''],
['\n\n' + '''"Hey!" cries ''', universal.state.player.name, ''', hopping away from the small theropod. "Cut it out!"'''],
['\n\n' + '''"Leave the poor ''', person.boygirl(), ''' be," says Ildri, walking over and lightly smacking the dinosaur on the top of head. "''', person.HeShe(), ''''s been through enough already, this morning."'''],
['\n\n' + '''The dinosaur gurgles.'''],
['\n\n' + '''"Yes, yes I know, you just want some attention," says Ildri with exasperated affection. She scratches the Coelophysis at the point where the scales of its jaw start to give way to short, feathery fur. "Now go lie down next to your sister."'''],
['\n\n' + '''The theropod hums, and curls up in front of the ovens as ordered.'''],
['\n\n' + universal.state.player.name, ''' buries ''', person.hisher(), ''' nose in the corner, obediently holding ''', person.hisher(), ''' borrowed skirt up around ''', person.hisher(), ''' waist.'''],
['\n\n' + '''Over the next half-hour, adventurers filter in and out, snatching up breakfast before going on with their days. A few make a few comments about the two chastised Taironans, but most ignore them. Ildri's strictness is well known, and adventurers aren't exactly the rule-following type, so most have found themselves in the exact same situation at least once.''']])
        ep2_ildri_double_spanking_apologize.children = []
        ep2_ildri_double_spanking_apologize.playerComments = []

        if 'talk_with_Mai' in textCommandsMusic.keywords() and 'talk_with_Airell' in textCommandsMusic.keywords() and 'talk_with_Morey' and 'talk_with_Cosima' in textCommandsMusic.keywords():
            ep2_ildri_double_spanking_apologize.children = ep2_morey_appointment.children
            conversation.say_node(ep2_morey_appointment.index)
        elif True:
            ep2_ildri_double_spanking_apologize.children = ep2_corner_musing.children
            conversation.say_node(ep2_corner_musing.index)

    ep2_ildri_double_spanking_apologize.quip_function = ep2_ildri_double_spanking_apologize_quip_function
    ep2_morey_appointment = conversation.Node(392)
    def ep2_morey_appointment_quip_function():

        ep2_morey_appointment.quip = universal.format_text_translate([['\n\n' + '''At one point, ''', universal.state.player.name, ''' hears Morey and Airell entering.'''],
['\n\n' + '''"Bah!" roars Airell. "Your ignorance is outshined only by your stupidity. A Saurion could no more cast magic than I could regrow my left toe. Why, Reginald just dispersed a treatise that documents an entire year's living with one of the largest tribes in Gondwana. Their 'magic' is superstitious nonsense that has as much an effect as praying to my beard."'''],
['\n\n' + '''"Oh come on. How could he have possibly known they were the largest tribe in Gondwana?" asks Morey. "No explorer I've heard of has managed to cross the Barrier Desert. Who knows what's on the other side. Besides, it doesn't matter how big it is, it's still just one tribe. Not every Saurion is the same."'''],
['\n\n' + '''"Bah," says Airell again, though with slightly more reservation.'''],
['\n\n' + '''"Curse it, ''', universal.state.player.name, '''," says Morey in exasperation. "Why did you get yourself spanked by Ildri? We have a meeting today, remember? About your foolishness during the Vengador attack?"'''],
['\n\n' + '''"Of course I remember," mutters ''', universal.state.player.name, ''', glaring fiercely at the wall. Total lie. ''', person.HeShe(), ''''d completely forgotten about it.'''],
['\n\n' + '''"Then why did you-"'''],
['\n\n' + '''"None of your business," says ''', universal.state.player.name, ''' sharply.'''],
['\n\n' + '''"Hate spanking bruised bottoms," mutters Morey. "Always makes me feel like a jerk. More of a jerk."'''],
['\n\n' + '''"Bah. You're too soft," says Airell. "It'll just drive the lesson home."'''],
['\n\n' + '''"You two leave ''', universal.state.player.name, ''' be," says Ildri. "Cornertime is not talking time."'''],
['\n\n' + '''"Well, ''', universal.state.player.name, ''', if you want, you can wait a bit," says Morey. "Until your bottom heals. Or we can get it over with today. It's up to you."'''],
['\n\n' + '''"I said-" begins Ildri.'''],
['\n\n' + '''"I know, I know," says Morey. "Sorry. Just wanted to-"'''],
['\n\n' + '''"Yeah, yeah. Here have some breakfast," says Ildri.'''],
['\n\n' + '''"Yes ma'am."'''],
['\n\n' + '''"Too soft, you ask me," grumbles Airell.'''],
['\n\n' + '''"No one asked you," says Morey.''']])
        ep2_morey_appointment.children = []
        ep2_morey_appointment.playerComments = []

        ep2_morey_appointment.children = ep2_corner_musing.children
        conversation.say_node(ep2_corner_musing.index)

    ep2_morey_appointment.quip_function = ep2_morey_appointment_quip_function
    ep2_corner_musing = conversation.Node(393)
    def ep2_corner_musing_quip_function():

        
        ep2_corner_musing.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' leans ''', person.hisher(), ''' head against the wall, and shifts ''', person.hisher(), ''' feet, wincing at the cries of protest from ''', person.hisher(), ''' bottom.'''],
['\n\n' + '''''', universal.format_line(['''Not that a tender bottom is anything new. This whole month has been a barrel of bun beating fun.''']) if 'talk_with_Morey' in textCommandsMusic.keywords() or 'talk_with_Airell' in textCommandsMusic.keywords() or 'talk_with_Mai' in textCommandsMusic.keywords() or 'talk_with_Cosima' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['\n\n' + '''''', universal.format_line(['''Like ''', person.hisher(), ''' session with Airell. Held in mid-air by a spectral hand, while the loud-mouthed slinger switched ''', person.hisher(), ''' bare bottom. Then, when it was done he had the nerve to make ''', universal.state.player.name, ''' thank him for the switching. Ass.''']) if 'talk_with_Airell' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['\n\n' + '''''', universal.format_line(['''Mai decided to make their session into a cat and mouse game. She made ''', universal.state.player.name, ''' run through her little maze, while the elf hunted ''', person.himher(), '''. If ''', universal.state.player.name, ''' could evade her for a quarter of a glass, ''', person.heshe(), ''' got out of the spanking. Of course, ''', person.heshe(), ''' didn't even last a tenth. Brat even did this obnoxious victory gloat dance thing, before tying ''', universal.state.player.name, ''' up and whipping ''', person.himher(), ''' with a riding crop.''']) if 'talk_with_Mai' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['\n\n' + '''''', universal.format_line(['''Cosima decided their session would double as some grappling training. They'd grapple. Cosima would overpower ''', universal.state.player.name, '''. Cosima would then paddle ''', universal.state.player.name, ''', while lecturing ''', person.himher(), ''' on all the things ''', person.heshe(), ''' did wrong. Rinse and repeat until ''', universal.state.player.name, ''' could barely walk.''']) if 'talk_with_Cosima' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['\n\n' + '''''', universal.format_line(['''And now, ''', person.heshe(), ''' has a session with Morey. La Madre only knows what Morey will make ''', person.himher(), ''' endure. Least this wretched month is finally, finally almost over.''']) if 'talk_with_Morey' in textCommandsMusic.keywords() and 'talk_with_Airell' in textCommandsMusic.keywords() and 'talk_with_Mai' in textCommandsMusic.keywords() and 'talk_with_Cosima' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['''''', universal.format_line(['''At least ''', person.hisher(), ''' session with Morey was fairly normal. A lecture and a tawsing. Granted, tawses suck, but at least it was straightforward and over relatively quickly.''']) if 'talk_with_Morey' in textCommandsMusic.keywords() else universal.format_line(['''''']), '''''']])
        ep2_corner_musing.children = []
        ep2_corner_musing.playerComments = []

        if 'attractedToAlondra' in textCommandsMusic.keywords():
            ep2_corner_musing.children = ep2_peeking_at_alondra.children
            conversation.say_node(ep2_peeking_at_alondra.index)
        elif True:
            ep2_corner_musing.children = ep2_corner_time_end.children
            conversation.say_node(ep2_corner_time_end.index)

    ep2_corner_musing.quip_function = ep2_corner_musing_quip_function
    ep2_peeking_at_alondra = conversation.Node(394)
    def ep2_peeking_at_alondra_quip_function():

        ep2_peeking_at_alondra.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' shifts ''', person.hisher(), ''' stance a second time. Madre, ''', person.hisher(), ''' bottom hurt. Stupid Ildri. Stupid Alondra.'''],
['\n\n' + '''Least Alondra's bottom is hanging out too. ''', universal.state.player.name, ''' barely contains a giggle as ''', person.heshe(), ''' thinks of Alondra limping around the kitchen, her marked bottom hanging out for all to see.'''],
['\n\n' + '''Her round, jiggly, protruding bottom...'''],
['\n\n' + universal.state.player.name, ''' squeezes ''', person.hisher(), ''' legs together. ''', person.HeShe(), ''''d gotten a glimpse of Alondra's panties when Ildri was spanking them. They'd been so delightfully tiny, yet at the same time covering up just enough to give ''', universal.state.player.name, ''' a thrill of mystery. A desire to peel them back and see what they hid...'''],
['\n\n' + '''''', universal.format_line(['''''', universal.state.player.name, ''' jerks ''', person.himselfherself(), ''' out of the budding fantasy. That spanking must have really raddled ''', person.himher(), '''. No way ''', person.heshe(), ''' could be interested in Alondra. Alondra's a girl.''']) if 'lesbian_in_denial' in textCommandsMusic.keywords() else universal.format_line(['''A desire to lead Alondra back to their room, Ildri's protests be cursed. To lay Alondra down on her bed, and pull those panties down, bringing the full swell of her round, bobbing cheeks into view. To cast a simple little charm to cool ''', universal.state.player.name, "'s", ''' hand off, and then gently rub ''', person.hisher(), ''' hand across Alondra's hot, abused flesh. To watch Alondra jump a little and then squirm at the cooling touch.''']), ''''''],
['\n\n' + universal.state.player.name, ''' glances over ''', person.hisher(), ''' shoulder, scanning for Alondra. Alondra has paused in the middle of pounding some dough, and is looking at ''', universal.state.player.name, "'s", ''' mostly naked bottom. Alondra notices ''', universal.state.player.name, ''' noticing her, and blushes. She turns her attention back to her pile of mashed dough.'''],
['\n\n' + '''''', universal.format_line(['''''', universal.state.player.name, ''' bites ''', person.hisher(), ''' lip and shifts uneasily, feeling a strange combination of elation and unease. Probably just misinterpreted Alondra's stare. She probably was just glancing up to see how ''', universal.state.player.name, ''' was doing, and ''', universal.state.player.name, ''' just happen to see her during her brief look up. Besides, Alondra shouldn't be interested in ''', person.himher(), ''' anyway.''']) if 'lesbian_in_denial' in textCommandsMusic.keywords() else universal.format_line(['''''', universal.state.player.name, ''' gnaws on ''', person.hisher(), ''' lip, and can't deny a small, elated grin. That was oggling. Alondra was totally oggling ''', person.himher(), '''. But could ''', universal.state.player.name, ''' be sure? Maybe it was just a quick glance, that ''', universal.state.player.name, ''' happened to see.''']), ''''''],
['\n\n' + universal.state.player.name, ''' glances back over ''', person.hisher(), ''' shoulder at Alondra. Alondra is paying careful attention to her food preparation, but ''', universal.state.player.name, ''' does catch her furtively glancing in ''', universal.state.player.name, "'s", ''' direction, before quickly looking away.'''],
['\n\n' + '''''', universal.format_line(['''''', universal.state.player.name, ''' stares resolutely at the corner, determined to feel uncomfortable about Alondra's gaze. Just like ''', person.heshe(), ''' is supposed to feel.''']) if 'lesbian_in_denial' in textCommandsMusic.keywords() else universal.format_line(['''''', universal.state.player.name, "'s", ''' grin widens, and ''', person.heshe(), ''' can't help but lean forward ever so slightly, and wiggle ''', person.hisher(), ''' hips a little.''']), ''''''],
['\n\n' + universal.state.player.name, ''' glances over ''', person.hisher(), ''' shoulder one last time, and this time sees Alondra with her back turned to ''', universal.state.player.name, ''', in the middle of grabbing something off the opposite counter. ''', universal.state.player.name, "'s", ''' eyes lance to Alondra's exposed bottom, the thin lacy blue panties, the two-thirds exposed cheeks, the stingy looking marks that just beg to be gently rubbed until the sting goes away.'''],
['\n\n' + universal.state.player.name, ''' feels a jolt between ''', person.hisher(), ''' legs, that spreads to ''', person.hisher(), ''' fingers and toes. ''', universal.format_line(['''''', universal.state.player.name, ''' spins ''', person.hisher(), ''' head back around and glares at the wall, feeling more than a little dirty.''']) if 'lesbian_in_denial' in textCommandsMusic.keywords() else universal.format_line(['''''', universal.state.player.name, "'s", ''' mouth opens slightly, and ''', person.hisher(), ''' fingers tighten on ''', person.hisher(), ''' skirt. Alondra turns back around and her eyes meet ''', universal.state.player.name, "'s", '''. ''', universal.state.player.name, ''' blushes, and ''', person.hisher(), ''' mouth snaps shut. The side of Alondra's mouth quirks, and she flashes ''', universal.state.player.name, ''' a wink. ''', universal.state.player.name, ''' grins back at Alondra, then turns back around to face the wall, before Ildri catches them.''']), '''''']])
        ep2_peeking_at_alondra.children = []
        ep2_peeking_at_alondra.playerComments = []

        ep2_peeking_at_alondra.children = ep2_corner_time_end.children
        conversation.say_node(ep2_corner_time_end.index)

    ep2_peeking_at_alondra.quip_function = ep2_peeking_at_alondra_quip_function
    ep2_corner_time_end = conversation.Node(395)
    def ep2_corner_time_end_quip_function():

        
        ep2_corner_time_end.quip = universal.format_text_translate([['\n\n' + '''"Alright," says Ildri at last. "Time's up. You get some breakfast, and go on with your day, ''', universal.state.player.name, '''. Alondra, we've got work to do."'''],
['\n\n' + universal.state.player.name, ''' lets the skirt drop back around ''', person.hisher(), ''' tender bottom, and turns around to face Alondra and Ildri.'''],
['\n\n' + '''The look of relief on Alondra's is face is palpable as Ildri removes the small pin, and lets Alondra's skirt drop back over her bottom. The relief is quickly replaced by a flash of pain when the rough skirt rubs against her tender bruises.'''],
['\n\n' + '''"You should probably get yourself some proper clothing," says Ildri, pointing at ''', universal.state.player.name, '''. "So you can return Alondra's skirt."'''],
['\n\n' + '''''', universal.format_line(['''"It's alright, I don't mind," says Alondra, shrugging. She flashes ''', universal.state.player.name, ''' a grin. "Besides, ''', person.heshe(), ''' looks kinda cute in it."''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''"Indeed," says Alondra giving ''', universal.state.player.name, ''' a stern look. "Skirts don't exactly grow on trees."''']), ''''''],
['\n\n' + '''''', universal.format_line(['''"Be that as it may," says Ildri. "You should still get yourself some of your own clothing."''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''Ildri nods.''']), ''''''],
['\n\n' + '''"I'll look into it as soon as I can afford it, I promise," says ''', universal.state.player.name, '''. ''', person.HeShe(), ''' makes ''', person.hisher(), ''' way to the breakfast set aside at one of one of the counters, and starts digging in.''']])
        ep2_corner_time_end.children = []
        ep2_corner_time_end.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_corner_time_end.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_corner_time_end.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_corner_time_end.quip_function = ep2_corner_time_end_quip_function
    ep2_ildri_double_spanking_unapologetic = conversation.Node(396)
    def ep2_ildri_double_spanking_unapologetic_quip_function():

        
        
        ep2_ildri_double_spanking_unapologetic.quip = universal.format_text_translate([['\n\n' + '''"''', universal.state.player.name, '''!" cries Alondra, sounding hurt.'''],
['\n\n' + '''WHAMWHAMWHAMWHAMWHAM!'''],
['\n\n' + universal.state.player.name, ''' unleashes a long, high-pitched howl as Ildri's hand smashes repeatedly into ''', person.hisher(), ''' bottom.'''],
['\n\n' + '''"You cruel, insolent little brat," hisses Ildri, her hand smacking every inch of ''', universal.state.player.name, "'s", ''' ''', universal.state.player.bum_adj(), ''', ''', universal.state.player.quivering(), ''', naked cheeks.'''],
['\n\n' + '''"Doesn't matter how hard you spank-oww!" cries ''', universal.state.player.name, ''', kicking ''', person.hisher(), ''' legs. "I still won't be sorry-yaaah!"'''],
['\n\n' + '''"Bold words," says Ildri over ''', universal.state.player.name, "'s", ''' carrying on. "Let's test that."'''],
['\n\n' + '''If anything, Ildri's hand begins to rise and fall even faster. ''', universal.state.player.name, "'s", ''' ''', universal.state.player.muscle_adj(), ''' globes ''', universal.state.player.quiver(), ''' wildly beneath the bombardment, and an all-consuming sting burns across them. Ildri's hard, callused hand ranges across every inch of ''', universal.state.player.name, "'s", ''' ''', universal.state.player.bum_adj(), ''' flesh, until ''', person.hisher(), ''' entire bottom is a white-hot mass of pain.'''],
['\n\n' + universal.state.player.name, ''' kicks and bucks. Cries of pain burst from ''', person.hisher(), ''' lips with every blow. ''', person.HisHer(), ''' hips squirm frantically, pushing Alondra against Ildri's torso, and nearly sending ''', universal.state.player.name, ''' sprawling off of Ildri's knee. Ildri has to pause periodically to readjust ''', universal.state.player.name, "'s", ''' position. On the one hand, the slight pauses are like manna from heaven. On the other, they seem to make the (inevitably) resumed spanking all the more painful.'''],
['\n\n' + '''Ildri even begins sharply slapping ''', universal.state.player.name, "'s", ''' bare thighs, making the chastised ''', person.boygirl(), ''' squeal and squirm even harder.'''],
['\n\n' + '''The thigh-slapping proves too much. "OK, OK I'm sorry, I'm sorry! Alondra's not a bitch! I'm suh, suh, sorreee!"'''],
['\n\n' + '''Ildri stops, her breath coming in deep, rapid pants. "You'd better be sorry. Now, let's get on with your punishment."'''],
['\n\n' + '''"What?" cries ''', universal.state.player.name, '''. ''', person.HeShe(), ''' reaches back to clutch ''', person.hisher(), ''' scalding cheeks. "But I thought-"'''],
['\n\n' + '''"That was for being an unrepetent little brat," says Ildri, rubbing ''', universal.state.player.name, "'s", ''' bruised, tender cheeks. "Now, I can start punishing you two for insulting and fighting each other over something so cursed pointless."'''],
['\n\n' + universal.state.player.name, ''' moans, and starts to cry. "Please, Ildri, I can't take anymore. Please no more!"''']])
        ep2_ildri_double_spanking_unapologetic.children = []
        ep2_ildri_double_spanking_unapologetic.playerComments = []

        ep2_ildri_double_spanking_unapologetic.children = ep2_ildri_double_spanking_apologize.children
        conversation.say_node(ep2_ildri_double_spanking_apologize.index)

    ep2_ildri_double_spanking_unapologetic.quip_function = ep2_ildri_double_spanking_unapologetic_quip_function
    ep2_salvage_trousers = conversation.Node(397)
    def ep2_salvage_trousers_quip_function():

        universal.state.player.take_item(itemspotionwars.cutoffShorts)
        universal.state.player.equip(itemspotionwars.cutoffShorts)
        
        
        
        ep2_salvage_trousers.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' pulls out the knife ''', person.heshe(), ''' uses for non-combat activities, and pulls ''', person.hisher(), ''' trousers out from underneath the bed. One leg has been split in half, but fortunately, the most important part of the pants (the part that covers ''', person.hisher(), ''' ass and crotch) are intact. ''', universal.state.player.name, ''' quickly saws off the trouser legs. Unfortunately, the one leg was so badly damaged, that ''', person.heshe(), ''' had no choice but to saw off the entire leg, leaving ''', person.himher(), ''' with a very short pair of rather ragged shorts. ''', person.HeShe(), ''' pulled on the shorts, and gave ''', person.himselfherself(), ''' a quick look and feel-over. OK, so the ass is covered (barely). Also, the pants were kind of tight, and cuttong off the legs doesn't have any impact on tightness. But the ass is covered. So long as ''', person.heshe(), ''' doesn't bend over. Better make sure to only bend over when Ildri isn't looking.'''],
['\n\n' + universal.state.player.name, ''' takes a deep breath, then returns to the kitchen.'''],
['\n\n' + '''Ildri glances at ''', universal.state.player.name, "'s", ''' new attire, and her eyebrows go up. "You know, you could have just worn the pants."'''],
['\n\n' + '''"One leg was ruined," says ''', universal.state.player.name, ''', shrugging. "Can't very well wear one-legged trousers, now can I?"'''],
['\n\n' + '''"Well, I'm sure you could have borrowed something from Alondra," says Ildri. She glances over ''', universal.state.player.name, '''. ''', universal.format_line(['''"Assuming you could it fit. ''']) if universal.state.player.towers_over(alondra) or alondra.towers_over(universal.state.player) else universal.format_line(['''"''']), '''Right, Ali?"''']])
        ep2_salvage_trousers.children = []
        ep2_salvage_trousers.playerComments = []

        if universal.state.player.is_female():
            ep2_salvage_trousers.children = ep2_alondra_stares.children
            conversation.say_node(ep2_alondra_stares.index)
        elif True:
            ep2_salvage_trousers.children = ep2_alondra_if_you_wanted_to_wear_a_skirt.children
            conversation.say_node(ep2_alondra_if_you_wanted_to_wear_a_skirt.index)

    ep2_salvage_trousers.quip_function = ep2_salvage_trousers_quip_function
    ep2_alondra_stares = conversation.Node(398)
    def ep2_alondra_stares_quip_function():

        
        ep2_alondra_stares.quip = universal.format_text_translate([['\n\n' + '''"Hmm?" says Alondra, her eyes briefly flicking to Ildri, before returning to ''', universal.state.player.name, "'s", ''' bare legs.'''],
['\n\n' + '''Ildri rolls her eyes, and gives Alondra a light swat on the bottom. "Stop staring. You'll make ''', person.himher(), ''' uncomfortable."'''],
['\n\n' + '''Alondra blushes, and her eyes turn back to Ildri. "I don't know what you're talking about."'''],
['\n\n' + '''"Sure you don't. Anyway, I said ''', person.heshe(), ''' could probably borrow a skirt or something from you, yes?" says Ildri.'''],
['\n\n' + '''"Oh, I don't know," says Alondra, her eyes turning back to ''', universal.state.player.name, "'s", ''' form. "Different body shapes and all. My skirts are kinda, you know. Made for me."'''],
['\n\n' + universal.format_line(['''"You two have the same body type, and are the same size," says Ildri.''']) if universal.state.player.bodyType == alondra.bodyType and universal.state.player.height == alondra.height else universal.format_line([''''''])],
['\n\n' + universal.format_line(['''"Uh-huh," says Alondra.''']) if universal.state.player.bodyType == alondra.bodyType and universal.state.player.height == alondra.height else universal.format_line([''''''])],
['\n\n' + '''Ildri rolls her eyes, and gives ''', universal.state.player.name, ''' one more look over. "Well, I guess getting you adventurers to cover your asses is a feat enough for one day. Now go get something to eat. There's some breakfast on the far counter."'''],
['\n\n' + universal.state.player.name, ''' nods gratefully as ''', person.hisher(), ''' stomach grumbles demandingly. ''', person.HeShe(), ''' makes ''', person.hisher(), ''' way to the food and digs in gleefully.''']])
        ep2_alondra_stares.children = []
        ep2_alondra_stares.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_stares.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_stares.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_stares.quip_function = ep2_alondra_stares_quip_function
    ep2_alondra_angry_denial = conversation.Node(399)
    def ep2_alondra_angry_denial_quip_function():

        ep2_alondra_angry_denial.quip = universal.format_text_translate([['\n\n' + '''"No one says you were dear," says Ildri, patting ''', universal.state.player.name, ''' on the shoulder, and giving Alondra a warning glare.'''],
['\n\n' + '''"No, of course not," says Alondra stiffly. She turns back to her pile of dough. "Ildri, we gonna you know, get back to the whole cooking thing?"'''],
['\n\n' + '''"Indeed," says Ildri. "Get some breakfast, ''', universal.state.player.name, '''."'''],
['\n\n' + universal.state.player.name, ''' doesn't need to be told twice. ''', person.HeShe(), ''' makes a beeline''']])
        ep2_alondra_angry_denial.children = []
        ep2_alondra_angry_denial.playerComments = []

        

    ep2_alondra_angry_denial.quip_function = ep2_alondra_angry_denial_quip_function
    ep2_alondra_if_you_wanted_to_wear_a_skirt = conversation.Node(400)
    def ep2_alondra_if_you_wanted_to_wear_a_skirt_quip_function():

        
        ep2_alondra_if_you_wanted_to_wear_a_skirt.quip = universal.format_text_translate([['\n\n' + '''"Assuming you don't mind wearing a skirt," says Alondra, flashing a grin at ''', universal.state.player.name, '''.''']])
        ep2_alondra_if_you_wanted_to_wear_a_skirt.children = [ep2_alondra_refuse_skirt, ep2_alondra_accept_skirt]
        ep2_alondra_if_you_wanted_to_wear_a_skirt.playerComments = ['''"I'm good, thanks."''','''"Sure. Gotta be more comfortable than these."''']

        

    ep2_alondra_if_you_wanted_to_wear_a_skirt.quip_function = ep2_alondra_if_you_wanted_to_wear_a_skirt_quip_function
    ep2_alondra_refuse_skirt = conversation.Node(401)
    def ep2_alondra_refuse_skirt_quip_function():

        
        ep2_alondra_refuse_skirt.quip = universal.format_text_translate([['\n\n' + '''"Right, well there's some food over there," says Ildri, pointing. "Go get something to eat."'''],
['\n\n' + universal.state.player.name, ''' nods eagerly, and makes a beeline for breakfast.''']])
        ep2_alondra_refuse_skirt.children = []
        ep2_alondra_refuse_skirt.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_refuse_skirt.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_refuse_skirt.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_refuse_skirt.quip_function = ep2_alondra_refuse_skirt_quip_function
    ep2_alondra_accept_skirt = conversation.Node(402)
    def ep2_alondra_accept_skirt_quip_function():

        itemspotionwars.alondrasSkirt.risque += 1 if universal.state.player.height == "tall" else 0
        itemspotionwars.alondrasSkirt.risque += 2 if universal.state.player.height == "huge" else 0
        
        
        itemspotionwars.alondrasSkirt.risque += 1 if universal.state.player.bodyType == "average" else 0
        itemspotionwars.alondrasSkirt.risque += 2 if universal.state.player.bodyType == "heavyset" else 0
        
        
        universal.state.player.take_item(itemspotionwars.alondrasSkirt)
        universal.state.player.equip(itemspotionwars.alondrasSkirt)
        
        
        
        ep2_alondra_accept_skirt.quip = universal.format_text_translate([['\n\n' + '''"Alright. Come along," says Alondra, grabbing ''', universal.state.player.name, "'s", ''' wrist and leading ''', person.himher(), ''' back to their shared room.'''],
['\n\n' + '''A bit later, ''', universal.state.player.name, ''' is dressed in one of Alondra's skirts. ''', universal.format_line(['''While on Alondra, the skirt extends to a little bit past the knees, ''', universal.state.player.name, ''' is shorter, so the skirt goes about halfway down ''', person.hisher(), ''' shins.''']) if universal.state.player.height == "small" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''Fortunately, Alondra and ''', universal.state.player.name, ''' are roughly the same height, so the skirt extends down to a little past ''', universal.state.player.name, "'s", ''' knees, like it does on Alondra.''']) if universal.state.player.height == "average" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''''', universal.state.player.name, ''' is quite a bit taller than Alondra, so the skirt stops several inches shy of ''', universal.state.player.name, "'s", ''' knees, about two-thirds down ''', person.hisher(), ''' thighs.''']) if universal.state.player.height == "tall" else universal.format_line(['''Unfortunately, ''', universal.state.player.name, ''' is much taller than Alondra, so rather than extending to ''', person.hisher(), ''' knees, the skirt stops at best halfway down ''', person.hisher(), ''' thighs.''']), ''''''],
['\n\n' + '''Meanwhile, ''', universal.format_line(['''''', universal.state.player.name, ''' has much slimmer hips than Alondra, so the two had to track down a bit of string to tie around ''', universal.state.player.name, "'s", ''' waist, to keep the skirt from falling down.''']) if universal.state.bodyType == "slim" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''the skirt hangs a little low on ''', universal.state.player.name, "'s", ''' hips, because ''', person.hisher(), ''' hips are a little bit slimmer than Alondra's.''']) if universal.state.bodyType == "average" else universal.format_line(['''''']), ''''''],
[universal.format_line(['''''', universal.state.player.name, ''' and Alondra have comparable hip shapes, so the skirt hangs fairly naturally, neither too loose nor too tight.''']) if universal.state.bodyType == "voluptuous" else universal.format_line(['''''', universal.state.player.name, ''' has much wider than Alondra's, forcing the skirt to cling to ''', universal.state.player.name, "'s", ''' hips much more tightly than it does to Alondra.''']), ''''''],
['\n\n' + '''"That will do," says Ildri. "Though you might want to purchase some proper clothing for yourself."'''],
['\n\n' + '''"I'll keep that in mind," says ''', universal.state.player.name, '''.''']])
        ep2_alondra_accept_skirt.children = []
        ep2_alondra_accept_skirt.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_accept_skirt.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_accept_skirt.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_accept_skirt.quip_function = ep2_alondra_accept_skirt_quip_function
    ep2_ildri_bare = conversation.Node(403)
    def ep2_ildri_bare_quip_function():

        
        ep2_ildri_bare.quip = universal.format_text_translate([['\n\n' + '''Ildri raises an eyebrow. "And you're idolizing them because..."''']])
        ep2_ildri_bare.children = [ep2_ildri_sexy_idols, ep2_ildri_hate_sewing]
        ep2_ildri_bare.playerComments = ['''"Because they're sexy!"''','''"I'm not really idolizing them. I just hate constantly fixing my clothing."''']

        

    ep2_ildri_bare.quip_function = ep2_ildri_bare_quip_function
    ep2_ildri_sexy_idols = conversation.Node(404)
    def ep2_ildri_sexy_idols_quip_function():

        
        ep2_ildri_sexy_idols.quip = universal.format_text_translate([['''''']])
        ep2_ildri_sexy_idols.children = []
        ep2_ildri_sexy_idols.playerComments = []

        if universal.state.player.is_female():
            ep2_ildri_sexy_idols.children = ep2_ildri_sexy_idols_female.children
            conversation.say_node(ep2_ildri_sexy_idols_female.index)
        elif True:
            ep2_ildri_sexy_idols.children = ep2_ildri_sexy_idols_male.children
            conversation.say_node(ep2_ildri_sexy_idols_male.index)

    ep2_ildri_sexy_idols.quip_function = ep2_ildri_sexy_idols_quip_function
    ep2_ildri_sexy_idols_female = conversation.Node(405)
    def ep2_ildri_sexy_idols_female_quip_function():

        
        
        ep2_ildri_sexy_idols_female.quip = universal.format_text_translate([['\n\n' + '''Alondra's eyes widen. "Really?"''']])
        ep2_ildri_sexy_idols_female.children = [ep2_alondra_sexy_compliment, ep2_alondra_appreciate, ep2_ildri_hate_sewing_dissapointment]
        ep2_ildri_sexy_idols_female.playerComments = ['''"Better believe it. 'Course, they're not as sexy as you."''','''"Sure. I appreciate a gorgeous female body as much as the next person."''','''"Nah, I'm just kidding. In all seriousness, it's just because I hate having to constantly fix my clothing. So long as you got health, skin heals instantly. Leather or cotton, not so much."''']

        

    ep2_ildri_sexy_idols_female.quip_function = ep2_ildri_sexy_idols_female_quip_function
    ep2_ildri_sexy_idols_male = conversation.Node(406)
    def ep2_ildri_sexy_idols_male_quip_function():

        
        
        ep2_ildri_sexy_idols_male.quip = universal.format_text_translate([['\n\n' + '''Ildri rolls her eyes. "You know, some people believe it's sexier when you don't just let everything hang out."'''],
['\n\n' + '''"Well, they're weird," says ''', universal.state.player.name, '''. ''', person.HeShe(), ''' crosses ''', person.hisher(), ''' arms over ''', person.hisher(), ''' chest. "And probably boring."'''],
['\n\n' + '''"Time to get boring then," says Ildri. She points with her spatula at the door. "Now, get that naked ass of yours back to your room, and get it covered, before I give you a reason other than modesty to cover yourself."''']])
        ep2_ildri_sexy_idols_male.children = [ep2_ildri_sexy_idols_cover_ass, ep2_ildri_sexy_idols_immature, ep2_ildri_bare_rude]
        ep2_ildri_sexy_idols_male.playerComments = ['''"Yes ma'am."''','''"No. I don't want to, and you can't make me."''','''"Yeah? Says you and what army?"''']

        

    ep2_ildri_sexy_idols_male.quip_function = ep2_ildri_sexy_idols_male_quip_function
    ep2_alondra_sexy_compliment = conversation.Node(407)
    def ep2_alondra_sexy_compliment_quip_function():

        
        
        ep2_alondra_sexy_compliment.quip = universal.format_text_translate([['\n\n' + '''Alondra blushes furiously, and a broad, beautiful smile breaks across her face. "Oh, well, thank you."'''],
['\n\n' + '''A small smile tugs at Ildris' lips. That doesn't keep her from reaching around and gives ''', universal.state.player.name, "'s", ''' bum a light smack, however. "Seduce my kitchen girl on her own time. Now go and cover your bottom, before I tan your hide."''']])
        ep2_alondra_sexy_compliment.children = [ep2_ildri_sexy_idols_cover_ass_bounce, ep2_ildri_sexy_idols_immature, ep2_ildri_bare_rude]
        ep2_alondra_sexy_compliment.playerComments = ['''"Yes ma'am."''','''"No. I don't want to, and you can't make me."''','''"Yeah? Says you and what army?"''']

        

    ep2_alondra_sexy_compliment.quip_function = ep2_alondra_sexy_compliment_quip_function
    ep2_ildri_sexy_idols_cover_ass_bounce = conversation.Node(408)
    def ep2_ildri_sexy_idols_cover_ass_bounce_quip_function():

        ep2_ildri_sexy_idols_cover_ass_bounce.quip = universal.format_text_translate([['\n\n' + '''As ''', universal.state.player.name, ''' goes to leave, ''', person.heshe(), ''' glances over ''', person.hisher(), ''' shoulder at Alondra, and gives ''', person.hisher(), ''' bare cheeks a quick wiggle, throwing Alondra a wink as ''', person.heshe(), ''' does so. Alondra's blush deepens, then deepens even more when Ildri's hand comes around and gives ''', universal.state.player.name, ''' another, harder smack, making ''', universal.state.player.name, "'s", ''' right cheek bounce.'''],
['\n\n' + universal.state.player.name, ''' eeps cutely, and hops forward a few steps.'''],
['\n\n' + '''"I said, stop seducing my kitchen girl, and go get changed," says Ildri sharply.''']])
        ep2_ildri_sexy_idols_cover_ass_bounce.children = []
        ep2_ildri_sexy_idols_cover_ass_bounce.playerComments = []

        ep2_ildri_sexy_idols_cover_ass_bounce.children = ep2_ildri_sexy_idols_cover_ass.children
        conversation.say_node(ep2_ildri_sexy_idols_cover_ass.index)

    ep2_ildri_sexy_idols_cover_ass_bounce.quip_function = ep2_ildri_sexy_idols_cover_ass_bounce_quip_function
    ep2_alondra_appreciate = conversation.Node(409)
    def ep2_alondra_appreciate_quip_function():

        
        
        ep2_alondra_appreciate.quip = universal.format_text_translate([['\n\n' + '''Alondra stares at ''', universal.state.player.name, ''' for a moment, apparently taken a bit aback by ''', universal.state.player.name, "'s", ''' bluntness.'''],
['\n\n' + '''"I don't care what you appreciate our how much," says Ildri. "You get that naked bum of yours back to your room, and you get it covered before I cover it in bruises. Understand?"''']])
        ep2_alondra_appreciate.children = [ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce, ep2_ildri_sexy_idols_immature, ep2_ildri_bare_rude]
        ep2_alondra_appreciate.playerComments = ['''"Yes ma'am."''','''"No. I don't want to, and you can't make me."''','''"Yeah? Says you and what army?"''']

        

    ep2_alondra_appreciate.quip_function = ep2_alondra_appreciate_quip_function
    ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce = conversation.Node(410)
    def ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce_quip_function():

        ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce.quip = universal.format_text_translate([['\n\n' + '''As ''', universal.state.player.name, ''' goes to leave, ''', person.heshe(), ''' glances over ''', person.hisher(), ''' shoulder at Alondra, and gives ''', person.hisher(), ''' bare cheeks a quick wiggle, throwing Alondra a wink as ''', person.heshe(), ''' does so. Alondra's blush deepens, then deepens even more when Ildri's hand comes around and gives ''', universal.state.player.name, ''' another, harder smack, making ''', universal.state.player.name, "'s", ''' right cheek bounce.'''],
['\n\n' + universal.state.player.name, ''' eeps cutely, and hops forward a few steps.'''],
['\n\n' + '''"Stop wasting time and go cover yourself," says Ildri sharply.''']])
        ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce.children = []
        ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce.playerComments = []

        ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce.children = ep2_ildri_sexy_idols_cover_ass.children
        conversation.say_node(ep2_ildri_sexy_idols_cover_ass.index)

    ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce.quip_function = ep2_ildri_sexy_idols_cover_ass_bounce_no_seduce_quip_function
    ep2_ildri_hate_sewing_dissapointment = conversation.Node(411)
    def ep2_ildri_hate_sewing_dissapointment_quip_function():

        
        
        ep2_ildri_hate_sewing_dissapointment.quip = universal.format_text_translate([['\n\n' + '''"Oh," says Alondra.'''],
['\n\n' + '''''', universal.format_line(['''''', universal.state.player.name, ''' feels a brief stab of regret. Was that dissapointment in Alondra's voice? Perhaps ''', person.heshe(), ''' said-No, of course not. No way ''', person.heshe(), ''' could be serious.''']) if 'attractedToAlondra' in textCommandsMusic.keywords() and 'lesbian_in_denial' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['''''', universal.format_line(['''''', universal.state.player.name, ''' feels a jolt. Was that disappointment in her voice? Perhaps later, ''', person.heshe(), ''' should have a little chat with Alondra...''']) if 'attractedToAlondra' in textCommandsMusic.keywords() else universal.format_line(['''''']), ''''''],
['\n\n' + '''"Anyway," says Ildri, giving ''', universal.state.player.name, ''' a warning glare and shaking her spatula at ''', universal.state.player.name, '''. "I don't care how little clothing other adventurers wear. You go and cover your ass, or I'll really give you something to show off."''']])
        ep2_ildri_hate_sewing_dissapointment.children = [ep2_ildri_sexy_idols_cover_ass, ep2_ildri_sexy_idols_immature, ep2_ildri_bare_rude]
        ep2_ildri_hate_sewing_dissapointment.playerComments = ['''"Yes ma'am."''','''"No. I don't want to, and you can't make me."''','''"Bite me."''']

        

    ep2_ildri_hate_sewing_dissapointment.quip_function = ep2_ildri_hate_sewing_dissapointment_quip_function
    ep2_ildri_sexy_idols_cover_ass = conversation.Node(412)
    def ep2_ildri_sexy_idols_cover_ass_quip_function():

        acceptableClothing = [clothing for item in universal.state.player.inventory if items.is_lower_clothing(clothing)]
        acceptableClothing = [clothing for item in acceptableClothing if not clothing.armorType == items.Underwear.armorType or not clothing.baring]
        
        
        
        ep2_ildri_sexy_idols_cover_ass.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' eyes the heavy looking spatula, then returns to ''', person.hisher(), ''' room, and begins searching for something to wear that Ildri would find acceptable.''']])
        ep2_ildri_sexy_idols_cover_ass.children = []
        ep2_ildri_sexy_idols_cover_ass.playerComments = []

        if acceptableClothing == []:
            ep2_ildri_sexy_idols_cover_ass.children = ep2_ildri_sexy_idols_cover_ass_no_clothing.children
            conversation.say_node(ep2_ildri_sexy_idols_cover_ass_no_clothing.index)
        elif True:
            ep2_ildri_sexy_idols_cover_ass.children = ep2_acceptable_clothing.children
            conversation.say_node(ep2_acceptable_clothing.index)

    ep2_ildri_sexy_idols_cover_ass.quip_function = ep2_ildri_sexy_idols_cover_ass_quip_function
    ep2_ildri_sexy_idols_cover_ass_no_clothing = conversation.Node(413)
    def ep2_ildri_sexy_idols_cover_ass_no_clothing_quip_function():

        
        
        ep2_ildri_sexy_idols_cover_ass_no_clothing.quip = universal.format_text_translate([['\n\n' + '''No clothing that covers ''', person.hisher(), ''' bottom at all. Well, that doesn't make any sense. Could have sworn ''', person.heshe(), ''' owned a pair of trousers at least. Did ''', person.heshe(), ''' sell them or something? Why did ''', person.heshe(), ''' do that?'''],
['\n\n' + '''Wait. When did ''', person.heshe(), ''' do that, and how did Ildri not notice ''', person.himher(), ''' wearing ass-baring clothing before?'''],
['\n\n' + '''Oh. Right. ''', person.HeShe(), ''' sold one pair of pants. Then ''', person.heshe(), ''' had to scrounge up some money to buy them back when Alondra warned ''', person.himher(), ''' that Ildri would spank ''', person.himher(), ''' so hard ''', person.heshe(), ''''d skip black and go right to blue. Then that pair of trousers got damaged yesterday when they got caught on an exposed nail.'''],
['\n\n' + universal.state.player.name, "'s", ''' takes one last look, and lights on three options. The first is the blanket on ''', person.hisher(), ''' bed. The second are the ragged remnants of ''', universal.state.player.name, "'s", ''' old trousers, currently hiding beneath ''', person.hisher(), ''' bed. The third is the small chest where Alondra keeps her spare clothing.''']])
        ep2_ildri_sexy_idols_cover_ass_no_clothing.children = [ep2_bedsheet, ep2_salvage_trousers, ep2_borrow_skirt]
        ep2_ildri_sexy_idols_cover_ass_no_clothing.playerComments = ['''Just wrap the blanket around yourself, and hope Ildri has mercy.''','''See if you can salvage the trousers''','''Borrow one of Alondra's skirts. It's an emergency after all. Surely she won't mind.''']

        

    ep2_ildri_sexy_idols_cover_ass_no_clothing.quip_function = ep2_ildri_sexy_idols_cover_ass_no_clothing_quip_function
    ep2_ildri_sexy_idols_immature = conversation.Node(414)
    def ep2_ildri_sexy_idols_immature_quip_function():

        
        
        ep2_ildri_sexy_idols_immature.quip = universal.format_text_translate([['\n\n' + '''Ildri's eyes narrow. "Since when did you turn five?"'''],
['\n\n' + universal.state.player.name, ''' crosses ''', person.hisher(), ''' arms over ''', person.hisher(), ''' chest and scowls at Ildri. "Since you started treating me like it."'''],
['\n\n' + '''"Please. If I were treating you like you were five, I'd have just carried you back to your room and personally picked out an outfit for you, instead of asking you to change yourself," says Ildri.'''],
['\n\n' + '''"Well, I like my outfit. I'm proud of my bottom, and I want to show it off," says ''', universal.state.player.name, ''', locking stares with Ildri. "I'm not going to change, and you won't make me."'''],
['\n\n' + '''Ildri nods. "Right then."'''],
['\n\n' + '''She steps forward and grabs ''', universal.state.player.name, ''' around the waist. With a heave and a grunt, she lifts ''', universal.state.player.name, ''' up into the air, and throws ''', person.himher(), ''' over her left shoulder.'''],
['\n\n' + '''"Hey!" cries ''', universal.state.player.name, ''', flailing uselessly in Ildri's grip. "What are you doing?"'''],
['\n\n' + '''There is a scrape of wood on stone as Ildri picks up her spatula. Then, she cracks it hard against ''', universal.state.player.name, "'s", ''' exposed left cheek. "I'm going to paddle you good, then put you in a proper outfit."'''],
['\n\n' + '''"No! Let go of me!" cries ''', universal.state.player.name, ''', kicking ''', person.hisher(), ''' legs, and pounding ''', person.hisher(), ''' fists against Ildri's back. "I'm an adult, I can where whatever I want!"'''],
['\n\n' + '''"Not in my guild you can't." Ildri storms out of the kitchen, her broad spatula smacking against ''', universal.state.player.name, "'s", ''' exposed bottom with every step.'''],
['\n\n' + '''By the time the two reach Ildri's room, ''', universal.state.player.name, "'s", ''' bottom is stinging fiercely, and ''', person.hisher(), ''' cries have as much pain as anger in them.'''],
['\n\n' + '''"You overbearing bi-oww!" wails ''', universal.state.player.name, '''. ''', person.HeShe(), ''' gives ''', person.hisher(), ''' feet a particularly kick, then starts flopping about on Ildri's shoulders.'''],
['\n\n' + '''Ildri dumps the ''', person.boygirl(), ''' on top of the bed. ''', universal.state.player.name, ''' rolls onto ''', person.hisher(), ''' hands and knees, and tries to crawl away, but Ildri grabs ''', person.hisher(), ''' hips and drags ''', person.himher(), ''' towards the edge of the bed. Ildri puts a firm hand on ''', person.hisher(), ''' back, and pins ''', person.himher(), ''' securely to the bed. Then, the spatula begins to rapidly rise and fall, peppering ''', universal.state.player.name, "'s", ''' ''', universal.state.player.underwear().name, '''-clad bottom with loud, sharp, stinging bows. ''', universal.state.player.name, ''' yowls beneath the beating, and ''', person.hisher(), ''' body flops about on the bed. But Ildri's grip is unbreakable, and her aim barely affected by ''', universal.state.player.name, "'s", ''' flailing. Ildri spanks ''', universal.state.player.name, ''' with steady, resolute smacks, neither speeding up nor slowing down in reaction to ''', universal.state.player.name, "'s", ''' carrying on. At one point during ''', person.hisher(), ''' flailing, ''', universal.state.player.name, "'s", ''' fingers close over one of Ildri's pillows. The young ''', person.manwoman(), ''' wraps ''', person.hisher(), ''' arms around the pillow and wails into it.'''],
['\n\n' + '''At one point, ''', universal.state.player.name, ''' realizes that Ildri has stopped spanking ''', person.himher(), '''.'''],
['\n\n' + '''"I know I've got it in here somewhere." Ildri's voice is muffled, as if a thin wall is between the cook and ''', universal.state.player.name, '''.'''],
['\n\n' + universal.state.player.name, ''' turns around, and looks in the direction of the voice. Ildri is half-buried in a large, ornate closet, ruffling through various sets of clothing.''']])
        ep2_ildri_sexy_idols_immature.children = []
        ep2_ildri_sexy_idols_immature.playerComments = []

        if universal.state.player.is_female():
            ep2_ildri_sexy_idols_immature.children = ep2_ildri_child_female.children
            conversation.say_node(ep2_ildri_child_female.index)
        elif True:
            ep2_ildri_sexy_idols_immature.children = ep2_ildri_child_male.children
            conversation.say_node(ep2_ildri_child_male.index)

    ep2_ildri_sexy_idols_immature.quip_function = ep2_ildri_sexy_idols_immature_quip_function
    ep2_ildri_child_female = conversation.Node(415)
    def ep2_ildri_child_female_quip_function():

        
        ep2_ildri_child_female.quip = universal.format_text_translate([['\n\n' + '''"Ah-hah!" cries Ildri, pulling out of the closet. Gripped in one hand is a bright pink dress, and in the other a pair of pink bows.'''],
['\n\n' + '''"What in La Madre's name are you doing?" asks ''', universal.state.player.name, ''' as Ildri walks over and lays the outfit on the bed next to the chastised Taironan.''']])
        ep2_ildri_child_female.children = []
        ep2_ildri_child_female.playerComments = []

        if universal.state.player.shirt().name != items.emptyUpperArmor.name:
            ep2_ildri_child_female.children = ep2_ildri_remove_shirt.children
            conversation.say_node(ep2_ildri_remove_shirt.index)
        elif True:
            ep2_ildri_child_female.children = ep2_ildri_put_on_dress.children
            conversation.say_node(ep2_ildri_put_on_dress.index)

    ep2_ildri_child_female.quip_function = ep2_ildri_child_female_quip_function
    ep2_ildri_remove_shirt = conversation.Node(416)
    def ep2_ildri_remove_shirt_quip_function():

        
        ep2_ildri_remove_shirt.quip = universal.format_text_translate([['\n\n' + '''Then Ildri pins ''', universal.state.player.name, ''' against the bed, and begins removing the adventurer's ''', universal.state.player.shirt().name, '''.'''],
['\n\n' + '''"Hey!" cries ''', universal.state.player.name, ''', struggling desperately. "What are you doing?"'''],
['\n\n' + '''"You'll barely fit into this thing as it is," says Ildri. "Let alone when wearing two layers. Ah, there we go!"'''],
['\n\n' + '''Ildri successfully pulls ''', universal.state.player.name, "'s", ''' ''', universal.state.player.shirt().name, ''' over ''', person.hisher(), ''' head, and tosses it onto the bed.''']])
        ep2_ildri_remove_shirt.children = []
        ep2_ildri_remove_shirt.playerComments = []

        if universal.state.player.is_female():
            ep2_ildri_remove_shirt.children = ep2_ildri_put_on_dress.children
            conversation.say_node(ep2_ildri_put_on_dress.index)
        elif True:
            ep2_ildri_remove_shirt.children = ep2_ildri_put_on_shorts.children
            conversation.say_node(ep2_ildri_put_on_shorts.index)

    ep2_ildri_remove_shirt.quip_function = ep2_ildri_remove_shirt_quip_function
    ep2_ildri_put_on_dress = conversation.Node(417)
    def ep2_ildri_put_on_dress_quip_function():

        
        ep2_ildri_put_on_dress.quip = universal.format_text_translate([['\n\n' + '''"Stop struggling," says Ildri, giving ''', universal.state.player.name, "'s", ''' flaming bottom a hard smack. "Or I'll start paddling you all over again."'''],
['\n\n' + universal.state.player.name, ''' stops struggling, ''', person.hisher(), ''' face burning fiercely as Ildri pushes the dress over ''', person.hisher(), ''' head, and tugs it down to ''', person.hisher(), ''' knees.''']])
        ep2_ildri_put_on_dress.children = []
        ep2_ildri_put_on_dress.playerComments = []

        if universal.state.player.long_hair():
            ep2_ildri_put_on_dress.children = ep2_ildri_put_in_bows.children
            conversation.say_node(ep2_ildri_put_in_bows.index)
        elif True:
            ep2_ildri_put_on_dress.children = ep2_ildri_female_done.children
            conversation.say_node(ep2_ildri_female_done.index)

    ep2_ildri_put_on_dress.quip_function = ep2_ildri_put_on_dress_quip_function
    ep2_ildri_put_in_bows = conversation.Node(418)
    def ep2_ildri_put_in_bows_quip_function():

        ep2_ildri_put_in_bows.quip = universal.format_text_translate([['\n\n' + '''Next, Ildri grabs the two bows, and with swift, efficient motions braids ''', universal.state.player.name, "'s", ''' hair into a pair of pigtails, tying them off at the end with the two bows.''']])
        ep2_ildri_put_in_bows.children = []
        ep2_ildri_put_in_bows.playerComments = []

        ep2_ildri_put_in_bows.children = ep2_ildri_female_done.children
        conversation.say_node(ep2_ildri_female_done.index)

    ep2_ildri_put_in_bows.quip_function = ep2_ildri_put_in_bows_quip_function
    ep2_ildri_female_done = conversation.Node(419)
    def ep2_ildri_female_done_quip_function():

        universal.state.player.take_item(itemspotionwars.pinkDress)
        universal.state.player.equip(itemspotionwars.pinkDress)
        
        
        ep2_ildri_female_done.quip = universal.format_text_translate([['\n\n' + '''"There," says Ildri, getting up off of ''', universal.state.player.name, ''', and backing up. She walks over to her vanity, and grabs a small mirror, holding it up in front of ''', universal.state.player.name, ''' so that ''', person.heshe(), ''' can see the end result. "Much more decent."'''],
['\n\n' + universal.state.player.name, ''' stares at the reflection as Ildri gradually angles the mirror so that ''', universal.state.player.name, ''' can take in ''', person.hisher(), ''' full body. ''', universal.format_line(['''''', person.HisHer(), ''' hair has been pulled back into two very childish pigtails, tied off with garish pink bows.''']) if universal.state.player.long_hair() else universal.format_line(['''''']), ''' ''', person.HeShe(), ''' is clad in a knee-length, bright pink dress. ''', universal.format_line(['''''', person.HeShe(), ''' could almost be mistaken for a child.''']) if universal.state.player.height == 'small' and universal.state.player.bodyType == 'thin' else universal.format_line(['''''']), ''''''],
['\n\n' + '''"You must be kidding me," moans ''', universal.state.player.name, ''', reaching towards the bows.'''],
['\n\n' + '''Ildri reaches forward and slaps ''', universal.state.player.name, "'s", ''' hand. "You want to act like a child? Fine, I'll dress you like a child."'''],
['\n\n' + '''"But when can I change out of it?" whines ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Since this is your first time, I'll only force you to wear it during breakfast," says Ildri. "But you act like a child again, and you can expect the same, except the paddling will be longer, and you'll have to wear the dress for the entire day. Understand?"'''],
['\n\n' + universal.state.player.name, ''' nods glumly. "Yes ma'am."'''],
['\n\n' + '''"Good, now let's get you some breakfast," says Ildri.'''],
['\n\n' + '''When the two return to the kitchen, Alondra's eyes widen. She glances at Ildri. "You weren't kidding, were you?"'''],
['\n\n' + '''"I don't kid when it comes to discipline," says Ildri. "Adventurers are an unruly lot. They'd tear the place apart if they didn't understand just whose in charge." She gives ''', universal.state.player.name, ''' a hard swat on the back of ''', person.hisher(), ''' skirt. "Now go have breakfast. There's some food on the far counter."'''],
['\n\n' + '''"Yes ma'am," mutters ''', universal.state.player.name, ''' sulkily, walking across the kitchen.'''],
['\n\n' + '''"And don't get food on that skirt," says Ildri sternly. "Or you'll have to wash it out."'''],
['\n\n' + universal.state.player.name, ''' spins around and quickly sticks ''', person.hisher(), ''' tongue at Ildri.'''],
['\n\n' + '''"What was that?" says Ildri in a low, warning voice.'''],
['\n\n' + '''"Nothing, nothing," says ''', universal.state.player.name, ''', scurrying over to the food. "Just want to eat."'''],
['\n\n' + '''Ildri grunts, and turns her attention back to Alondra's baking.''']])
        ep2_ildri_female_done.children = []
        ep2_ildri_female_done.playerComments = []

        ep2_ildri_female_done.children = ep2_other_adventurers_clothing.children
        conversation.say_node(ep2_other_adventurers_clothing.index)

    ep2_ildri_female_done.quip_function = ep2_ildri_female_done_quip_function
    ep2_ildri_child_male = conversation.Node(420)
    def ep2_ildri_child_male_quip_function():

        
        ep2_ildri_child_male.quip = universal.format_text_translate([['\n\n' + '''"Ah-hah!" cries Ildri, pulling out of the closet. Gripped in one hand is a pair of pale blue shorts, a white short-sleeved shirt, and matching blue vest.'''],
['\n\n' + '''"What in La Madre's name are you doing?" asks ''', universal.state.player.name, ''' as Ildri walks over and lays the outfit on the bed next to the chastised Taironan.''']])
        ep2_ildri_child_male.children = []
        ep2_ildri_child_male.playerComments = []

        if universal.state.player.shirt().name != items.emptyUpperArmor.name:
            ep2_ildri_child_male.children = ep2_ildri_remove_shirt.children
            conversation.say_node(ep2_ildri_remove_shirt.index)
        elif True:
            ep2_ildri_child_male.children = ep2_ildri_put_on_shorts.children
            conversation.say_node(ep2_ildri_put_on_shorts.index)

    ep2_ildri_child_male.quip_function = ep2_ildri_child_male_quip_function
    ep2_ildri_put_on_shorts = conversation.Node(421)
    def ep2_ildri_put_on_shorts_quip_function():

        ep2_ildri_put_on_shorts.quip = universal.format_text_translate([['\n\n' + '''"Stop struggling," says Ildri, giving ''', universal.state.player.name, "'s", ''' flaming bottom a hard smack. "Or I'll start paddling you all over again."'''],
['\n\n' + universal.state.player.name, ''' stops struggling, ''', person.hisher(), ''' face burning fiercely as Ildri pushes the shirt over ''', person.hisher(), ''' head, pushes the shorts up ''', person.hisher(), ''' legs, tucks the shirt into the shorts, then makes ''', person.himher(), ''' put on the vest on.''']])
        ep2_ildri_put_on_shorts.children = []
        ep2_ildri_put_on_shorts.playerComments = []

        ep2_ildri_put_on_shorts.children = ep2_ildri_male_done.children
        conversation.say_node(ep2_ildri_male_done.index)

    ep2_ildri_put_on_shorts.quip_function = ep2_ildri_put_on_shorts_quip_function
    ep2_ildri_male_done = conversation.Node(422)
    def ep2_ildri_male_done_quip_function():

        
        ep2_ildri_male_done.quip = universal.format_text_translate([['\n\n' + '''"There," says Ildri, finishing the last button, and backing up. She walks over to her vanity, and grabs a small mirror, holding it up in front of ''', universal.state.player.name, ''' so that ''', person.heshe(), ''' can see the end result. "Much more decent."'''],
['\n\n' + universal.state.player.name, ''' stares at the reflection as Ildri gradually angles the mirror so that ''', universal.state.player.name, ''' can take in ''', person.hisher(), ''' full body. ''', person.HeShe(), ''' is clad in a white shirt, blue vest, and matching blue shorts. ''', universal.format_line(['''''', person.HeShe(), ''' could almost be mistaken for a child.''']) if universal.state.player.height == 'small' and universal.state.player.bodyType == 'thin' else universal.format_line(['''''']), ''''''],
['\n\n' + '''"You must be kidding me," moans ''', universal.state.player.name, ''', reaching towards the buttons of the vest.'''],
['\n\n' + '''Ildri slaps ''', universal.state.player.name, "'s", ''' hand. "No."'''],
['\n\n' + '''"But when can I change out of it?" whines ''', universal.state.player.name, '''.'''],
['\n\n' + '''"Since this is your first time, I'll only force you to wear it during breakfast," says Ildri. "But you act like a child again, and you can expect the same, except the paddling will be longer, and you'll have to wear the shorts and vest for the entire day. Understand?"'''],
['\n\n' + universal.state.player.name, ''' nods glumly. "Yes ma'am."'''],
['\n\n' + '''"Good, now let's get you some breakfast," says Ildri.'''],
['\n\n' + '''When the two return to the kitchen, Alondra's eyes widen. She glances at Ildri. "You weren't kidding, were you?"'''],
['\n\n' + '''"I don't kid when it comes to discipline," says Ildri. "Adventurers are an unruly lot. They'd tear the place apart if they didn't understand just whose in charge." She gives ''', universal.state.player.name, ''' a hard swat on the back of ''', person.hisher(), ''' shorts. "Now go have breakfast. There's some food on the far counter."'''],
['\n\n' + '''"Yes ma'am," mutters ''', universal.state.player.name, ''' sulkily, walking across the kitchen.'''],
['\n\n' + '''"And don't get food on that vest," says Ildri sternly. "Or you'll have to wash it out yourself."'''],
['\n\n' + universal.state.player.name, ''' spins around and quickly sticks ''', person.hisher(), ''' tongue at Ildri.'''],
['\n\n' + '''"What was that?" says Ildri in a low, warning voice.'''],
['\n\n' + '''"Nothing, nothing," says ''', universal.state.player.name, ''', scurrying over to the food. "Just want to eat."'''],
['\n\n' + '''Ildri grunts, and turns her attention back to Alondra's baking.''']])
        ep2_ildri_male_done.children = []
        ep2_ildri_male_done.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_ildri_male_done.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_ildri_male_done.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_ildri_male_done.quip_function = ep2_ildri_male_done_quip_function
    ep2_other_adventurers_clothing = conversation.Node(423)
    def ep2_other_adventurers_clothing_quip_function():

        
        ep2_other_adventurers_clothing.quip = universal.format_text_translate([['''''']])
        ep2_other_adventurers_clothing.children = []
        ep2_other_adventurers_clothing.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_other_adventurers_clothing.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_other_adventurers_clothing.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_other_adventurers_clothing.quip_function = ep2_other_adventurers_clothing_quip_function
    ep2_ildri_hate_sewing = conversation.Node(424)
    def ep2_ildri_hate_sewing_quip_function():

        
        
        ep2_ildri_hate_sewing.quip = universal.format_text_translate([['\n\n' + '''"Actually, that is kind of a fair point," says Alondra, thoughtfully tapping her chin. "I'll bet adventurers go through clothing faster than a baby sauropod goes through scales."'''],
['\n\n' + '''Ildri throws a brief scowl at Alondra, before turning her attention back to ''', universal.state.player.name, '''. "You planning on fighting today?"'''],
['\n\n' + '''"Well, no," says ''', universal.state.player.name, '''. "But you never know when someone will ambush you."'''],
['\n\n' + '''Ildri rolls her eyes. "Please. Avaricum hasn't gotten that bad yet. Now, go put on some cursed pants, before I give you a good smacking."''']])
        ep2_ildri_hate_sewing.children = [ep2_ildri_sexy_idols_cover_ass, ep2_ildri_sexy_idols_immature, ep2_ildri_bare_rude]
        ep2_ildri_hate_sewing.playerComments = ['''"Yes ma'am."''','''"No. I don't want to, and you can't make me."''','''"Bite me."''']

        

    ep2_ildri_hate_sewing.quip_function = ep2_ildri_hate_sewing_quip_function
    ep2_ildri_bare_rude = conversation.Node(425)
    def ep2_ildri_bare_rude_quip_function():

        
        ep2_ildri_bare_rude.quip = universal.format_text_translate([['\n\n' + '''Ildri's eyes narrow. "Excuse me?"'''],
['\n\n' + '''"You heard me," says ''', universal.state.player.name, ''', crossing ''', person.hisher(), ''' arms over ''', person.hisher(), ''' chest, and scowling at Ildri.'''],
['\n\n' + '''"Look, you little brat, I don't have time to trade barbs with you," says Ildri, shaking her spoon at ''', universal.state.player.name, '''. "Now, you go cover your bottom, before I give it a solid thrashing."'''],
['\n\n' + universal.state.player.name, ''' tries to brush past Ildri. "Sorry, lady but I'm not your ''', person.sondaughter(), '''. You can't tell me how to dress."'''],
['\n\n' + '''"Oh-ho, yes I can. So long as you live under my roof, you follow my rules." Ildri cracks her spatula against ''', universal.state.player.name, "'s", ''' exposed bottom, making ''', universal.state.player.name, ''' yelp and jump. "Now go get changed."''']])
        ep2_ildri_bare_rude.children = [ep2_ildri_sexy_idols_cover_ass, ep2_ildri_bite_me]
        ep2_ildri_bare_rude.playerComments = ['''"Fine."''','''"Ah, go get buried."''']

        

    ep2_ildri_bare_rude.quip_function = ep2_ildri_bare_rude_quip_function
    ep2_ildri_bite_me = conversation.Node(426)
    def ep2_ildri_bite_me_quip_function():

        
        
        ep2_ildri_bite_me.quip = universal.format_text_translate([['\n\n' + '''Ildri takes a slow, deep breath. Then, she grabs ''', universal.state.player.name, "'s", ''' shoulders, bends ''', person.hisher(), ''' over, and wraps her burly left arm around ''', universal.state.player.name, "'s", ''' waist.'''],
['\n\n' + '''"Hey! Let go of me!" cries ''', universal.state.player.name, ''', pounding ''', person.hisher(), ''' fist against Ildri's calf.'''],
['\n\n' + '''"I'll teach you to mouth off to me," says Ildri, cracking her hard, callused hand against ''', universal.state.player.name, "'s", ''' exposed bum cheeks.'''],
['\n\n' + universal.state.player.name, ''' wiggles in Ildri's grip, ''', person.hisher(), ''' feet scrambling against the ground. "Let go of me you overbearing harlot!"'''],
['\n\n' + '''Smack! Smack! Smack!'''],
['\n\n' + universal.state.player.name, ''' begins to curse viciously as a hot sting rapidly builds in ''', person.hisher(), ''' vulnerable cheeks. "I said, let go of me!"'''],
['\n\n' + '''Smack! Smack! Smack!'''],
['\n\n' + universal.state.player.name, ''' grimaces as ''', person.hisher(), ''' bottom ripples beneath the cook's blows. ''', person.HeShe(), ''' rams ''', person.hisher(), ''' foot against the ground, and slaps Ildri's thigh. "Let go, curse you!"'''],
['\n\n' + '''Smack! Smack! Smack!'''],
['\n\n' + '''"Stop this, I hate you!" cries ''', universal.state.player.name, '''. ''', person.HeShe(), ''' jerks ''', person.hisher(), ''' hips back and forth in a vain effort to protect ''', person.hisher(), ''' exposed, burning cheeks.'''],
['\n\n' + '''Smack! Smack! Smack!'''],
['\n\n' + universal.state.player.name, "'s", ''' cries of rage begin to be interlaced with cries of pain. ''', person.HeShe(), ''' starts trying to reach back to shield ''', person.hisher(), ''' cheeks, but one arm can't get past Ildri's body, and Ildir pins the other between her arm and ''', universal.state.player.name, "'s", ''' side.'''],
['\n\n' + '''Smack! Smack! Smack!'''],
['\n\n' + '''"Owwww," moans ''', universal.state.player.name, ''', twisting ''', person.hisher(), ''' feet and clenching ''', person.hisher(), ''' bottom.'''],
['\n\n' + '''Ildri relaxes her grip, and lets ''', universal.state.player.name, ''' wiggle away from her. ''', universal.state.player.name, ''' starts to dance away, rubbing ''', person.hisher(), ''' bottom and moaning. However, ''', person.heshe(), ''' has only taken a few steps, before Ildri grabs ''', person.himher(), ''' again, and flings ''', person.himher(), ''' across her shoulder like a sack of grain.'''],
['\n\n' + '''"Hey," cries ''', universal.state.player.name, '''. "What are you doing now?"'''],
['\n\n' + '''"We're going to get you some actual clothing." Ildri gives ''', universal.state.player.name, "'s", ''' right cheek a heavy slap.'''],
['\n\n' + '''"Urrrgh!" cries ''', universal.state.player.name, ''', kicking ''', person.hisher(), ''' feet. "Madre, you horrible, oversized-owwww!"'''],
['\n\n' + '''Ildri lands four hard slaps to ''', universal.state.player.name, "'s", ''' stinging cheeks. "If you know what's good for you, you will not finish that sentence."'''],
['\n\n' + universal.state.player.name, ''' grumbles, but keeps silent.''']])
        ep2_ildri_bite_me.children = []
        ep2_ildri_bite_me.playerComments = []

        if 'boarding_with_Adrian' in textCommandsMusic.keywords():
            ep2_ildri_bite_me.children = ep2_ildri_bite_me_check_room.children
            conversation.say_node(ep2_ildri_bite_me_check_room.index)
        elif True:
            ep2_ildri_bite_me.children = ep2_ildri_carried_to_tailors.children
            conversation.say_node(ep2_ildri_carried_to_tailors.index)

    ep2_ildri_bite_me.quip_function = ep2_ildri_bite_me_quip_function
    ep2_ildri_bite_me_check_room = conversation.Node(427)
    def ep2_ildri_bite_me_check_room_quip_function():

        acceptableClothing = [clothing for item in universal.state.player.inventory if items.is_lower_clothing(clothing)]
        acceptableClothing = [clothing for item in acceptableClothing if not clothing.armorType == items.Underwear.armorType or not clothing.baring]
        
        
        
        ep2_ildri_bite_me_check_room.quip = universal.format_text_translate([['\n\n' + '''Ildri carries ''', universal.state.player.name, ''' back to ''', person.hisher(), ''' room. She pops open the chest at the end of ''', universal.state.player.name, "'s", ''' bed, and starts looking for some actual clothing for ''', person.himher(), ''' to wear.''']])
        ep2_ildri_bite_me_check_room.children = []
        ep2_ildri_bite_me_check_room.playerComments = []

        if acceptableClothing == []:
            ep2_ildri_bite_me_check_room.children = ep2_ildri_bite_me_no_clothing.children
            conversation.say_node(ep2_ildri_bite_me_no_clothing.index)
        elif True:
            ep2_ildri_bite_me_check_room.children = ep2_ildri_bite_me_clothing.children
            conversation.say_node(ep2_ildri_bite_me_clothing.index)

    ep2_ildri_bite_me_check_room.quip_function = ep2_ildri_bite_me_check_room_quip_function
    ep2_ildri_bite_me_no_clothing = conversation.Node(428)
    def ep2_ildri_bite_me_no_clothing_quip_function():

        ep2_ildri_bite_me_no_clothing.quip = universal.format_text_translate([['\n\n' + '''Ildri makes a disgusted noise. "Don't you have anything that will actually cover you? I could have sworn you at least had a pair of trousers."'''],
['\n\n' + universal.state.player.name, ''' doesn't say anything.'''],
['\n\n' + '''Ildri gives the ''', person.boygirl(), ''''s bottom a hard smack. "Don't you dare make me turn you over my knee."'''],
['\n\n' + universal.state.player.name, ''' grumbles under ''', person.hisher(), ''' breath for a second before answering. "I did. Then I sold them. Then I bought them back when Alondra told me what a tyrannical-"'''],
['\n\n' + '''Ildri starts to remove her belt.'''],
['\n\n' + '''"I mean, when she told me about your 'covered bottom' policy," says ''', universal.state.player.name, ''' a touch hastily. ''', person.HeShe(), ''' feels a bit of shame at how quickly ''', person.heshe(), ''' folded, but that belt looks thick. "Only, it got ripped at the end of the day yesterday. Got caught on an exposed nail."'''],
['\n\n' + '''Ildri rebuckles her belt, then starts to carry ''', universal.state.player.name, ''' out of the room. "Well, then we'll just have to go the tailors and get you some new clothing."'''],
['\n\n' + '''"So you gonna let me down, or what?" asks ''', universal.state.player.name, ''' sharply as they walk through the hallway.'''],
['\n\n' + '''"Nope."'''],
['\n\n' + '''"What? Come on! It's not my fault I don't have anything to wear," cries ''', universal.state.player.name, '''.'''],
['\n\n' + '''"For one, yes it is. If you couldn't afford a backup outfit, you should have told me. I would have happily helped," says Ildri. "And two, whether or not you're responsible, it doesn't change how you mouthed off to me. You're going to learn respect if it kills me."'''],
['\n\n' + universal.state.player.name, ''' starts muttering and cursing. ''', person.HisHer(), ''' grumbles are cut short by a hard smack.'''],
['\n\n' + '''"And I don't want to listen to your grumbling," says Ildri sharply.''']])
        ep2_ildri_bite_me_no_clothing.children = []
        ep2_ildri_bite_me_no_clothing.playerComments = []

        ep2_ildri_bite_me_no_clothing.children = ep2_ildri_carried_to_tailors.children
        conversation.say_node(ep2_ildri_carried_to_tailors.index)

    ep2_ildri_bite_me_no_clothing.quip_function = ep2_ildri_bite_me_no_clothing_quip_function
    ep2_ildri_bite_me_clothing = conversation.Node(429)
    def ep2_ildri_bite_me_clothing_quip_function():

        acceptableClothing = [clothing for item in universal.state.player.inventory if items.is_lower_clothing(clothing)]
        acceptableClothing = [clothing for item in acceptableClothing if not clothing.armorType == items.Underwear.armorType or not clothing.baring]
        chosenOutfit = acceptableClothing[0]
        universal.state.player.equip(chosenOutfit)
        
        
        
        ep2_ildri_bite_me_clothing.quip = universal.format_text_translate([['\n\n' + '''Ildri pulls the ''', universal.state.player.lower_clothing().name, ''' out of the chest, and dumps ''', universal.state.player.name, ''' on the bed. She holds ''', universal.format_line(['''them''']) if chosenOutfit.armorType == items.Pants.armorType or chosenOutfit.armorType == items.Shorts.armorType else universal.format_line(['''it''']), ''' out to ''', universal.state.player.name, '''. "Put these on young ''', person.manlady(), '''."''']])
        ep2_ildri_bite_me_clothing.children = [ep2_ildri_put_on_trousers, ep2_ildri_refuse_to_put_on_trousers]
        ep2_ildri_bite_me_clothing.playerComments = ['''"Yes ma'am."''','''"No. I don't want to, and you can't make me."''']

        

    ep2_ildri_bite_me_clothing.quip_function = ep2_ildri_bite_me_clothing_quip_function
    ep2_ildri_put_on_trousers = conversation.Node(430)
    def ep2_ildri_put_on_trousers_quip_function():

        
        ep2_ildri_put_on_trousers.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' takes ''', universal.state.player.lower_clothing().name, ''' and glumly pulls them on, hissing a little as the clothing rubs against ''', person.hisher(), ''' tender bottom.'''],
['\n\n' + '''"There," says Ildri, smiling. "Was that so hard?"'''],
['\n\n' + '''"Yes," says ''', universal.state.player.name, ''', pouting and rubbing ''', person.hisher(), ''' bum.'''],
['\n\n' + '''"Oh stop whining. Now let's go get you something to eat. You'll feel better when you've got some food in you," says Ildri, helping ''', universal.state.player.name, ''' stand, and ruffling ''', person.hisher(), ''' hair.'''],
['\n\n' + universal.state.player.name, ''' follows Ildri back to the kitchen. The cook points out the tray of food at the far end of the counter, and ''', universal.state.player.name, ''' dives in without further ado.''']])
        ep2_ildri_put_on_trousers.children = []
        ep2_ildri_put_on_trousers.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_ildri_put_on_trousers.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_ildri_put_on_trousers.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_ildri_put_on_trousers.quip_function = ep2_ildri_put_on_trousers_quip_function
    ep2_ildri_refuse_to_put_on_trousers = conversation.Node(431)
    def ep2_ildri_refuse_to_put_on_trousers_quip_function():

        
        ep2_ildri_refuse_to_put_on_trousers.quip = universal.format_text_translate([['\n\n' + '''Ildri sighs in disgust and massages her eyes. "Stop. Just, just stop. All I'm asking, is that you put on ''', universal.format_line(['''some''']) if universal.state.player.lower_clothing().armorType == items.Pants.armorType or universal.state.player.lower_clothing().armorType == items.Shorts.armorType else universal.format_line(['''a''']), ''' ''', universal.state.player.lower_clothing().name, '''. Why do you have to make it so difficult?"'''],
['\n\n' + '''"Because what I wear is none of your business," says ''', universal.state.player.name, ''' angrily. "You're not my mother. You're just my landlady"'''],
['\n\n' + '''"Could have fooled me," grumbles Ildri, unbuckling her belt.'''],
['\n\n' + '''"Hey, wait-" ''', universal.state.player.name, ''' starts to crawl away, but Ildri grabs ''', person.himher(), ''' and rolls ''', person.himher(), ''' onto ''', person.hisher(), ''' stomach. She finishes removing her belt, then yanks ''', universal.state.player.name, "'s", ''' ''', universal.state.player.underwear().name, ''' down to ''', person.hisher(), ''' knees.'''],
['\n\n' + '''"Let go of me," cries ''', universal.state.player.name, ''', kicking wildly. ''', person.HeShe(), ''' tries to push ''', person.himselfherself(), ''' off the bed, but a firm push from Ildri drives ''', person.himher(), ''' back into the bed.'''],
['\n\n' + '''"Stop kicking," snaps Ildri. "Unless you want me to belt your feet."'''],
['\n\n' + universal.state.player.name, ''' glares at Ildri, and pulls ''', person.hisher(), ''' feet tight against ''', person.hisher(), ''' exposed cheeks.'''],
['\n\n' + '''"Fine." Ildri points her finger at ''', universal.state.player.name, "'s", ''' ankles. A glowing gold cord shoots from Ildri's finger and wraps itself around ''', universal.state.player.name, "'s", ''' ankles. Ildri sweeps her arm up and over, in a pulling motion. On cue, the spectral rope tightens, and starts to pull ''', universal.state.player.name, "'s", ''' legs away from ''', person.hisher(), ''' bottom. ''', universal.state.player.name, ''' fights back, but ''', person.heshe(), ''' might as well have been in a tug of war with a sauropod, for all the good it did ''', person.himher(), '''. In seconds, ''', universal.state.player.name, "'s", ''' feet are flat against the bed. Another cord shoots from Ildri's finger, wrapping itself around ''', universal.state.player.name, "'s", ''' ankles, and the underside of the bed, securely pinning ''', person.hisher(), ''' legs against the feather-filled mattress.'''],
['\n\n' + universal.state.player.name, ''' pulls against the spectral cords, then scowls into the bed when ''', person.hisher(), ''' feet don't move an inch.'''],
['\n\n' + '''"Shall I tie your hands down too?" asks Ildri.'''],
['\n\n' + universal.state.player.name, ''' doesn't answer.'''],
['\n\n' + '''Ildri picks up her belt, and doubles it over. ''', universal.state.player.name, ''' glances over ''', person.hisher(), ''' shoulder, to see Ildri calmly raising the belt. ''', person.HeShe(), ''' quickly looks away, and stares straight ahead at the wall. With a sharp snap, Ildri brings the belt down across ''', universal.state.player.name, "'s", ''' bottom. ''', person.HisHer(), ''' cheeks jiggle beneath the blow, and ''', person.heshe(), ''' winces at the harsh sting. Ildri cracks the belt across ''', universal.state.player.name, "'s", ''' ''', universal.state.player.bum_adj(), ''' bottom a second time, just above the first blow. ''', universal.state.player.name, "'s", ''' fingers dig into the bed, and ''', person.heshe(), ''' takes a long, slow breath.'''],
['\n\n' + '''"I don't know what's going through your silly little head," says Ildri, just before belting ''', universal.state.player.name, "'s", ''' swelled cheeks a third time, right below the first blow. "What did you think was going to happen?"'''],
['\n\n' + universal.state.player.name, ''' just glares at the wall.'''],
['\n\n' + '''"Did you think I was just bluffing?" Ildri snaps the belt twice across ''', universal.state.player.name, "'s", ''' vulnerable cheeks. ''', universal.state.player.name, ''' grunts a little, and rocks a bit. "That I don't take my own rules seriously?"'''],
['\n\n' + universal.state.player.name, ''' doesn't answer.'''],
['\n\n' + '''"Don't want to answer? Fine. We can do that." Ildri begins laying into ''', universal.state.player.name, "'s", ''' cheeks with hard, fast blows. ''', universal.state.player.name, ''' can't help but whimper a little, as the hard, scaly leather batters ''', person.hisher(), ''' burning bottom. But then, ''', person.heshe(), ''' locks ''', person.hisher(), ''' jaw, and digs ''', person.hisher(), ''' nails into ''', person.hisher(), ''' palms.'''],
['\n\n' + '''Still, the belt continues to rise and fall, each harsh blow building on the throbbing sting of the previous. ''', universal.state.player.name, ''' can't help but start to wiggle ''', person.hisher(), ''' hips. Small mewls of pain begin to slip past ''', person.hisher(), ''' locked jaw. Then, Ildri lands three quick blows to ''', universal.state.player.name, "'s", ''' sitspots, and the mewls turn into howls. ''', universal.state.player.name, ''' arcs ''', person.hisher(), ''' back, and pushes ''', person.hisher(), ''' chest into the air.'''],
['\n\n' + '''Ildri pushes ''', person.himher(), ''' back down, and lands another half a dozen hard blows, ''', universal.state.player.name, ''' yelping and bucking through each one.'''],
['\n\n' + '''"Now put on the cursed ''', universal.state.player.lower_clothing().name, '''," says Ildri, waving her hand at the spectral chords, dissolving them.'''],
['\n\n' + '''For a moment, ''', universal.state.player.name, ''' considers continuing ''', person.hisher(), ''' defiance. But then, ''', person.heshe(), ''' rolls onto ''', person.hisher(), ''' bottom, the raw, welted flesh screaming as it scrapes against the bed. ''', person.HeShe(), ''' eyes the scaled leather belt, then nods glumly. ''', person.HeShe(), ''' grabs the ''', universal.state.player.lower_clothing().name, ''' and pulls \itthem{universal.state.player.lower_clothing()} them, wincing as \itthey{universal.state.player.lower_clothing()} scrapes against ''', person.hisher(), ''' sore bottom.'''],
['\n\n' + '''Ildri nods in satisfaction. "Good. Now go have some breakfast."'''],
['\n\n' + universal.state.player.name, ''' leads the way back to the kitchen, rubbing ''', person.hisher(), ''' bottom and silently fuming.'''],
['\n\n' + '''Once they reach the kitchen, ''', universal.state.player.name, ''' digs into the breakfast tray laid out on the far counter. Alondra flashes ''', person.himher(), ''' a comforting, slightly uneasy smile.''']])
        ep2_ildri_refuse_to_put_on_trousers.children = [ep2_alondra_focus_on_food, ep2_alondra_return_the_smile]
        ep2_ildri_refuse_to_put_on_trousers.playerComments = ['''Focus on the food''','''Return the smile''']

        

    ep2_ildri_refuse_to_put_on_trousers.quip_function = ep2_ildri_refuse_to_put_on_trousers_quip_function
    ep2_alondra_focus_on_food = conversation.Node(432)
    def ep2_alondra_focus_on_food_quip_function():

        
        ep2_alondra_focus_on_food.quip = universal.format_text_translate([['\n\n' + '''However, ''', universal.state.player.name, ''' is too focused on ''', person.hisher(), ''' breakfast (and certain vulgar thoughts regarding Ildri) to return the smile. ''', universal.format_line(['''''', person.HeShe(), ''' does however notice that Alondra looks rather hurt, which cools ''', person.hisher(), ''' anger somewhat, and leaves ''', person.himher(), ''' feeling a little bit ashamed.''']) if universal.state.player.is_female() else universal.format_line(['''''']), '''''']])
        ep2_alondra_focus_on_food.children = []
        ep2_alondra_focus_on_food.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_focus_on_food.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_focus_on_food.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_focus_on_food.quip_function = ep2_alondra_focus_on_food_quip_function
    ep2_alondra_return_the_smile = conversation.Node(433)
    def ep2_alondra_return_the_smile_quip_function():

        
        ep2_alondra_return_the_smile.quip = universal.format_text_translate([['\n\n' + '''A little bit startled, ''', universal.state.player.name, ''' returns the smile with one of ''', person.hisher(), ''' own. ''', universal.format_line(['''Alondra's smile widens, before turning her attention back to her cooking. The whole exchange leaves ''', universal.state.player.name, ''' feeling pleasantly warm.''']) if universal.state.player.is_female() else universal.format_line(['''''']), '''''']])
        ep2_alondra_return_the_smile.children = []
        ep2_alondra_return_the_smile.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_alondra_return_the_smile.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_alondra_return_the_smile.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_alondra_return_the_smile.quip_function = ep2_alondra_return_the_smile_quip_function
    ep2_no_pants_punishment = conversation.Node(434)
    def ep2_no_pants_punishment_quip_function():

        ep2_no_pants_punishment.quip = universal.format_text_translate([['''''']])
        ep2_no_pants_punishment.children = []
        ep2_no_pants_punishment.playerComments = []

        

    ep2_no_pants_punishment.quip_function = ep2_no_pants_punishment_quip_function
    ep2_ildri_carried_to_tailors = conversation.Node(435)
    def ep2_ildri_carried_to_tailors_quip_function():

        ep2_ildri_carried_to_tailors.quip = universal.format_text_translate([['\n\n' + '''Placeholder. We'll see how Jeffrey does, and if we can split some of that into carried to tailors.''']])
        ep2_ildri_carried_to_tailors.children = []
        ep2_ildri_carried_to_tailors.playerComments = []

        

    ep2_ildri_carried_to_tailors.quip_function = ep2_ildri_carried_to_tailors_quip_function
    ep2_acceptable_clothing = conversation.Node(436)
    def ep2_acceptable_clothing_quip_function():

        acceptableClothing = [clothing for item in universal.state.player.inventory if items.is_lower_clothing(clothing)]
        acceptableClothing = [clothing for item in acceptableClothing if not clothing.armorType == items.Underwear.armorType or not clothing.baring]
        acceptableOutfit = acceptableClothing[0]
        universal.state.player.equip(acceptableOutfit)
        
        
        
        ep2_acceptable_clothing.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' throws on ''', person.hisher(), ''' ''', universal.state.player.lower_clothing().name, ''', and returns to the kitchen.'''],
['\n\n' + '''Ildri glances at ''', universal.state.player.name, ''', and nods in satisfaction. "Much better. Now why don't you get something to eat."'''],
['\n\n' + '''''', universal.format_line(['''As ''', universal.state.player.name, ''' makes ''', person.hisher(), ''' way to the pile of breakfast, ''', person.heshe(), ''' glances at Alondra. The woman is looking at ''', universal.state.player.name, ''' with a faint dissapointment, like a young child whose just discovered ''', person.heshe(), ''' needs to wait longer than ''', person.heshe(), ''' thought for the Spring Festival. Alondra notices ''', universal.state.player.name, ''' looking, and blushes and looks away.''']) if universal.state.player.is_female() else universal.format_line(['''''']), '''''']])
        ep2_acceptable_clothing.children = []
        ep2_acceptable_clothing.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_acceptable_clothing.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_acceptable_clothing.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_acceptable_clothing.quip_function = ep2_acceptable_clothing_quip_function
    ep2_talk_to_Ildri_introvert = conversation.Node(437)
    def ep2_talk_to_Ildri_introvert_quip_function():

        
        ep2_talk_to_Ildri_introvert.quip = universal.format_text_translate([['\n\n' + '''Ildri smiles at ''', universal.state.player.name, ''' as ''', person.heshe(), ''' enters the kitchen.''']])
        ep2_talk_to_Ildri_introvert.children = []
        ep2_talk_to_Ildri_introvert.playerComments = []

        if universal.state.player.is_pantsless() and universal.state.player.underwear().baring:
            ep2_talk_to_Ildri_introvert.children = ep2_ildri_indecent.children
            conversation.say_node(ep2_ildri_indecent.index)
        elif True:
            ep2_talk_to_Ildri_introvert.children = ep2_introvert_kitchen_pants.children
            conversation.say_node(ep2_introvert_kitchen_pants.index)

    ep2_talk_to_Ildri_introvert.quip_function = ep2_talk_to_Ildri_introvert_quip_function
    ep2_introvert_kitchen_pants = conversation.Node(438)
    def ep2_introvert_kitchen_pants_quip_function():

        
        ep2_introvert_kitchen_pants.quip = universal.format_text_translate([['\n\n' + universal.state.player.name, ''' finds Alondra already hard at work pounding a pile of dough into something fit for baking, while Ildri splits her attention between her own pile of dough, and Alondra.'''],
['\n\n' + universal.state.player.name, ''' spies the first round of breakfast sitting on a different counter, and makes a beeline for it. "Thanks Ildri."'''],
['\n\n' + '''"Part of my job," says Ildri. "Also, good morning ''', universal.state.player.name, '''."'''],
['\n\n' + '''"Morning," says ''', universal.state.player.name, ''' around a mouthful of food.''']])
        ep2_introvert_kitchen_pants.children = []
        ep2_introvert_kitchen_pants.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_introvert_kitchen_pants.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_introvert_kitchen_pants.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_introvert_kitchen_pants.quip_function = ep2_introvert_kitchen_pants_quip_function
    ep2_ildri_greeting = conversation.Node(439)
    def ep2_ildri_greeting_quip_function():

        
        ep2_ildri_greeting.quip = universal.format_text_translate([['\n\n' + '''"Morning," says ''', universal.state.player.name, ''' around a mouthful of food.''']])
        ep2_ildri_greeting.children = []
        ep2_ildri_greeting.playerComments = []

        if 'teaching_Anne' in textCommandsMusic.keywords():
            ep2_ildri_greeting.children = ep2_talk_about_teaching.children
            conversation.say_node(ep2_talk_about_teaching.index)
        elif True:
            ep2_ildri_greeting.children = ep2_unplanned_day.children
            conversation.say_node(ep2_unplanned_day.index)

    ep2_ildri_greeting.quip_function = ep2_ildri_greeting_quip_function
    ep2_marias_wake_up = conversation.Node(440)
    def ep2_marias_wake_up_quip_function():

        
        ep2_marias_wake_up.quip = universal.format_text_translate([['''''']])
        ep2_marias_wake_up.children = []
        ep2_marias_wake_up.playerComments = []

        if 'extrovert' in textCommandsMusic.keywords():
            ep2_marias_wake_up.children = ep2_maria_wake_up_extrovert.children
            conversation.say_node(ep2_maria_wake_up_extrovert.index)
        elif True:
            ep2_marias_wake_up.children = ep2_maria_wake_up_introvert.children
            conversation.say_node(ep2_maria_wake_up_introvert.index)

    ep2_marias_wake_up.quip_function = ep2_marias_wake_up_quip_function
    ep2_maria_wake_up_extrovert = conversation.Node(441)
    def ep2_maria_wake_up_extrovert_quip_function():

        universal.state.player.takes_damage(1)
        
        
        
        ep2_maria_wake_up_extrovert.quip = universal.format_text_translate([['\n\n' + '''"Up and at 'em." Maria is gently shaking ''', universal.state.player.name, '''.'''],
['\n\n' + universal.state.player.name, ''' groans, and rolls away from ''', person.hisher(), ''' roommate. ''', person.HeShe(), ''' yanks ''', person.hisher(), ''' blanket over ''', person.hisher(), ''' head to block the morning sunlight wafting in through the window. "G'way."'''],
['\n\n' + '''"Now come on, you promised you'd volunteer at Sofia's clinic with me, remember?" says Maria. "You know, in exchange for footing last month's rent?"'''],
['\n\n' + '''"Not m'fault," mumbles ''', universal.state.player.name, '''. "No job."'''],
['\n\n' + '''"Doesn't stop you from going out with Carrie at least twice a week," says Maria sardonically, ripping ''', universal.state.player.name, "'s", ''' blanket off. "Where'd you get the money for that?"'''],
['\n\n' + '''"Hey!" cries ''', universal.state.player.name, ''', sitting up and reaching for the blanket. ''', person.HeShe(), ''' groans, and falls back onto ''', person.hisher(), ''' back, clutching ''', person.hisher(), ''' head.'''],
['\n\n' + '''Maria sighs. "How much did you drink last night?"'''],
['\n\n' + '''"Leave m'alone."'''],
['\n\n' + '''"Well?"'''],
['\n\n' + '''"Not a lot." Suddenly, ''', universal.state.player.name, "'s", ''' stomach heaves. ''', person.HeShe(), ''' lunges for a nearby bucket, and proceeds to empty the contents of ''', person.hisher(), ''' stomach. When ''', person.heshe(), ''' finishes, ''', person.heshe(), ''' feels a surge of power, and ''', person.hisher(), ''' headache, and nausea disappear. ''', person.HeShe(), ''' sighs in relief, then tenses. Crap. ''', person.himher(), ''' silly. Must act sick.'''],
['\n\n' + '''"Your health just triggered didn't it?" says Maria, a hint of anger creeping into her voice.''']])
        ep2_maria_wake_up_extrovert.children = [ep2_maria_extrovert_admit_health, ep2_maria_extrovert_deny_health]
        ep2_maria_wake_up_extrovert.playerComments = ['''"I guess."''','''"No."''']

        

    ep2_maria_wake_up_extrovert.quip_function = ep2_maria_wake_up_extrovert_quip_function
    ep2_maria_extrovert_admit_health = conversation.Node(442)
    def ep2_maria_extrovert_admit_health_quip_function():

        
        
        ep2_maria_extrovert_admit_health.quip = universal.format_text_translate([['\n\n' + '''"And what would Nana do if she caught you with a health-trigger hangover?" asks Maria.'''],
['\n\n' + '''"Give me a high-five and congratulate me for enjoying my life?" says ''', universal.state.player.name, ''', smiling innocently.'''],
['\n\n' + '''Maria gives ''', person.himher(), ''' a very Nanaesque "Stop the stegashit" look.''']])
        ep2_maria_extrovert_admit_health.children = [ep2_maria_extrovert_admit_compliant, ep2_maria_extrovert_admit_petulant, ep2_maria_extrovert_admit_resistant]
        ep2_maria_extrovert_admit_health.playerComments = ['''"She'd spank me."''','''"Not like it's any of your business."''','''"Fuck off."''']

        

    ep2_maria_extrovert_admit_health.quip_function = ep2_maria_extrovert_admit_health_quip_function
    ep2_maria_extrovert_admit_compliant = conversation.Node(443)
    def ep2_maria_extrovert_admit_compliant_quip_function():

        ep2_maria_extrovert_admit_compliant.quip = universal.format_text_translate([['\n\n' + '''"And do you know why she'd spank you?" asks Maria.'''],
['\n\n' + universal.state.player.name, ''' picks up the bucket of vomit, grabs a nearby rag, and carries them outside into the tiny courtyard behind their small apartment. Maria follows after ''', person.himher(), ''', patiently waiting for a response. ''', universal.state.player.name, ''' grabs an old rusty shovel, and begins digging a small hole. "Because healing's hard on your body."'''],
['\n\n' + '''"And what happens if your health triggers too much?"'''],
['\n\n' + '''"You get the General's Gift." ''', universal.state.player.name, ''' carefully pours the vomit into the small hole. %&&&''']])
        ep2_maria_extrovert_admit_compliant.children = []
        ep2_maria_extrovert_admit_compliant.playerComments = []

        

    ep2_maria_extrovert_admit_compliant.quip_function = ep2_maria_extrovert_admit_compliant_quip_function
    ep2_maria_extrovert_admit_petulant = conversation.Node(444)
    def ep2_maria_extrovert_admit_petulant_quip_function():

        ep2_maria_extrovert_admit_petulant.quip = universal.format_text_translate([['''''']])
        ep2_maria_extrovert_admit_petulant.children = []
        ep2_maria_extrovert_admit_petulant.playerComments = []

        

    ep2_maria_extrovert_admit_petulant.quip_function = ep2_maria_extrovert_admit_petulant_quip_function
    ep2_maria_extrovert_admit_petulant = conversation.Node(445)
    def ep2_maria_extrovert_admit_petulant_quip_function():

        ep2_maria_extrovert_admit_petulant.quip = universal.format_text_translate([['''''']])
        ep2_maria_extrovert_admit_petulant.children = []
        ep2_maria_extrovert_admit_petulant.playerComments = []

        

    ep2_maria_extrovert_admit_petulant.quip_function = ep2_maria_extrovert_admit_petulant_quip_function
    ep2_maria_extrovert_deny_health = conversation.Node(446)
    def ep2_maria_extrovert_deny_health_quip_function():

        ep2_maria_extrovert_deny_health.quip = universal.format_text_translate([['\n\n' + '''Maria slaps the seat of ''', universal.state.player.name, "'s", ''' ''', universal.state.player.pajama_bottom().name, '''. "Don't lie to me young ''', person.manlady(), '''. I saw your body jerk, then relax, then I heard you sigh, then watched you tense. In other words, your health triggered, you felt much better, and then realized that if I knew your hangover was so bad it triggered your health, I'd tan your hide."''']])
        ep2_maria_extrovert_deny_health.children = []
        ep2_maria_extrovert_deny_health.playerComments = []

        

    ep2_maria_extrovert_deny_health.quip_function = ep2_maria_extrovert_deny_health_quip_function
    ep2_maria_wake_up_extrovert_response_denial = conversation.Node(447)
    def ep2_maria_wake_up_extrovert_response_denial_quip_function():

        
        ep2_maria_wake_up_extrovert_response_denial.quip = universal.format_text_translate([['''''']])
        ep2_maria_wake_up_extrovert_response_denial.children = [ep2_carrie_favor, ep2_carrie_chores]
        ep2_maria_wake_up_extrovert_response_denial.playerComments = ['''"She hasn't said yet. Just says I owe her a favor."''','''"Help her with her chores."''']

        

    ep2_maria_wake_up_extrovert_response_denial.quip_function = ep2_maria_wake_up_extrovert_response_denial_quip_function
    ep2_maria_wake_up_extrovert_response = conversation.Node(448)
    def ep2_maria_wake_up_extrovert_response_quip_function():

        
        
        ep2_maria_wake_up_extrovert_response.quip = universal.format_text_translate([['''''']])
        ep2_maria_wake_up_extrovert_response.children = [ep2_carrie_sex_for_booze, ep2_carrie_favor, ep2_carrie_chores]
        ep2_maria_wake_up_extrovert_response.playerComments = ['''Grin suggestively.''','''"She hasn't said yet. Just says I how her a favor."''','''"Help her with her chores."''']

        

    ep2_maria_wake_up_extrovert_response.quip_function = ep2_maria_wake_up_extrovert_response_quip_function
    ep2_carrie_sex_for_booze = conversation.Node(449)
    def ep2_carrie_sex_for_booze_quip_function():

        
        
        ep2_carrie_sex_for_booze.quip = universal.format_text_translate([['\n\n' + '''Maria rolls her eyes. "Mother, you are such a whore."'''],
['\n\n' + '''"Yup." ''', universal.state.player.name, ''' closes ''', person.hisher(), ''' eyes smugly. "Total booze whore. 'Specially when my 'client's' got an ass like that. To say nothing of the boobs. Or the face. Or the legs. Or well, that whole body. Nice voice too. Fun conversationalist-"''']])
        ep2_carrie_sex_for_booze.children = []
        ep2_carrie_sex_for_booze.playerComments = []

        if universal.state.player.is_female():
            ep2_carrie_sex_for_booze.children = ep2_carrie_sex_for_booze_lesbian.children
            conversation.say_node(ep2_carrie_sex_for_booze_lesbian.index)
        elif True:
            ep2_carrie_sex_for_booze.children = ep2_carrie_sex_for_booze.children
            conversation.say_node(ep2_carrie_sex_for_booze.index)

    ep2_carrie_sex_for_booze.quip_function = ep2_carrie_sex_for_booze_quip_function
    ep2_carrie_sex_for_booze_lesbian = conversation.Node(450)
    def ep2_carrie_sex_for_booze_lesbian_quip_function():

        ep2_carrie_sex_for_booze_lesbian.quip = universal.format_text_translate([['\n\n' + '''"I get the picture," says Maria sardonically. "Seriously though, don't make a big deal about it."'''],
['\n\n' + '''"Curses," says ''', universal.state.player.name, '''. "And here I was looking forward to telling everyone at the clinic about that awesome sex I had with a Sister-in-training of the Matirian Church. I'm sure that'll go over great."'''],
['\n\n' + '''"Not just at the clinic," says Maria sharply. "Avoid talking about it with other Taironans, including Ildri's new kitchen girl. The Tierra Iglesias has grown very anti, erm, like-with-like in the past few years. The fact that you're boning a member of the Matirian Church is just gravy on the steak."'''],
['\n\n' + universal.state.player.name, ''' rolls onto ''', person.hisher(), ''' side, and gives Maria a baffled look. "Since when?"'''],
['\n\n' + '''"Well, maybe it's not happening in Chengue, but around here? It started before I arrived," says Maria. "It's only gotten worse since then."'''],
['\n\n' + universal.state.player.name, ''' smirks. "Is that why you became a Matirian?"'''],
['\n\n' + '''"Don't even joke about that," says Maria sharply.'''],
['\n\n' + '''"Fine, whatever," grumbles ''', universal.state.player.name, ''', yanking ''', person.hisher(), ''' curling up into a ball and closing ''', person.hisher(), ''' eyes. Maybe ''', person.heshe(), ''' shouldn't have stayed out quite so late last night.'''],
['\n\n' + '''"Up," says Maria.'''],
['\n\n' + universal.state.player.name, ''' doesn't move.'''],
['\n\n' + '''"Now, young ''', person.manlady(), '''," says Maria sternly.'''],
['\n\n' + '''"But I'm sleepy," mutters ''', universal.state.player.name, '''.'''],
['\n\n' + '''"How terrible. Fortunately, I have just the thing." There's a faint rustling, and then the sharp sound of wood on flesh.'''],
['\n\n' + universal.state.player.name, "'s", ''' head snaps off the pillow, and ''', person.heshe(), ''' rolls onto ''', person.hisher(), ''' (away from Maria) and looks up at the other woman. Maria is standing above ''', person.himher(), ''', slapping ''', universal.state.player.name, "'s", ''' spoon against her palm.''']])
        ep2_carrie_sex_for_booze_lesbian.children = []
        ep2_carrie_sex_for_booze_lesbian.playerComments = []

        

    ep2_carrie_sex_for_booze_lesbian.quip_function = ep2_carrie_sex_for_booze_lesbian_quip_function
    ep2_carrie_sex_for_booze = conversation.Node(451)
    def ep2_carrie_sex_for_booze_quip_function():

        ep2_carrie_sex_for_booze.quip = universal.format_text_translate([['\n\n' + '''"I get the picture," says Maria sardonically.''']])
        ep2_carrie_sex_for_booze.children = []
        ep2_carrie_sex_for_booze.playerComments = []

        

    ep2_carrie_sex_for_booze.quip_function = ep2_carrie_sex_for_booze_quip_function
    ep2_carrie_favor = conversation.Node(452)
    def ep2_carrie_favor_quip_function():

        ep2_carrie_favor.quip = universal.format_text_translate([['''''']])
        ep2_carrie_favor.children = []
        ep2_carrie_favor.playerComments = []

        

    ep2_carrie_favor.quip_function = ep2_carrie_favor_quip_function
    ep2_carrie_chores = conversation.Node(453)
    def ep2_carrie_chores_quip_function():

        ep2_carrie_chores.quip = universal.format_text_translate([['''''']])
        ep2_carrie_chores.children = []
        ep2_carrie_chores.playerComments = []

        

    ep2_carrie_chores.quip_function = ep2_carrie_chores_quip_function
    ep2_maria_wake_up_extrovert = conversation.Node(454)
    def ep2_maria_wake_up_extrovert_quip_function():

        ep2_maria_wake_up_extrovert.quip = universal.format_text_translate([['''''']])
        ep2_maria_wake_up_extrovert.children = []
        ep2_maria_wake_up_extrovert.playerComments = []

        

    ep2_maria_wake_up_extrovert.quip_function = ep2_maria_wake_up_extrovert_quip_function
def end_scene_1_episode_2(loading=False):
    pass


scene_1_episode_2 = episode.Scene("scene_1_episode_2", start_scene_1_episode_2, end_scene_1_episode_2)
def init_episode_2():
    build_chars()
    build_rooms()
episode2 = episode.Episode(2, "Back Alleys", scenes=[scene_1_episode_2], titleTheme=textCommandsMusic.LUCILLA, init=init_episode_2)