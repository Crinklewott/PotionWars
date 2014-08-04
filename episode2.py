import universal
import textCommands
import person
import items
import pwenemies
import dungeonmode
import itemspotionwars
import episode2CharRooms




def init_episode_2_1():
    ep2_wakeup = Node( 321 )

    def ep2_wakeup_quip_function():
        ep2_wakeup.quip = format_text_no_space([[''''''],
])
        ep2_wakeup.quip = ""
        if "boarding_with_Adrian" in keywords:
            ep2_wakeup.children = ep2_guild_wake_up.children
            conversation.say_node(ep2_guild_wake_up)
            
        elif "boarding_with_Maria" in keywords:
            ep2_wakeup.children = ep2_marias_wake_up.children
            conversation.say_node(ep2_marias_wake_up)


    
    ep2_wakeup.quip_function = ep2_wakeup_quip_function
    ep2_guild_wake_up = Node( 322 )

    def ep2_guild_wake_up_quip_function():
        ep2_guild_wake_up.quip = format_text_no_space([[''''''],
])
        ep2_guild_wake_up.quip = ""
        if "extrovert" in keywords:
            ep2_guild_wake_up.children = ep2_guild_wake_up_extrovert.children
            conversation.say_node(ep2_guild_wake_up_extrovert)
            
        elif "introvert" in keywords:
            ep2_guild_wake_up.children = ep2_guild_wake_up_introvert.children
            conversation.say_node(ep2_guild_wake_up_introvert)


    
    ep2_guild_wake_up.quip_function = ep2_guild_wake_up_quip_function
    ep2_guild_wake_up_extrovert = Node( 323 )

    def ep2_guild_wake_up_extrovert_quip_function():
        ep2_guild_wake_up_extrovert.quip = format_text_no_space([[''''''],
['''An earsplitting shriek stabs into ''', universal.state.player.name, ''''s''', ''' ears like a white-hot needle. ''', person.HeShe(), ''' half jumps, half rolls out of bed, fumbling for ''', person.hisher(), ''' weapon.'''],
['''"Got you! Got you!"'''],
['''After an eternity, ''', universal.state.player.name, ''''s''', ''' fingers clumsily close over the hilt of ''', person.hisher(), ''' ''', universal.state.player.weapon(), '''. ''', person.HeShe(), ''' jumps to ''', person.hisher(), ''' feet, then promptly falls to ''', person.hisher(), ''' knees and throws up all over the floor.'''],
['''"No fair! Gotta count to ten!"'''],
['''"I counted to ten!"'''],
['''"You skipped seven!"'''],
['''"No I didn't!"'''],
['''"Yes you did!"'''],
['''''', universal.state.player.name, ''' groans, and rubs ''', person.hisher(), ''' throbbing forehead. A pair of children charge past the (thank La Madre!) closed door. ''', person.HisHer(), ''' headache spikes, and ''', person.heshe(), ''' groans. How in La Madre's name could such tiny feet (to say nothing of the voices!) make so much noise?'''],
['''Stupid Alondra, and her stupid siblings.'''],
['''Stupid Carrie, and her stupid "Let's party tonight!"'''],
['''For the past six days.'''],
['''Or was it seven?'''],
['''Whatever.'''],
['''''', universal.state.player.name, ''' stares numbly at the puddle of foul smelling bodily fluids spreading grotesquely across the floor in front of ''', person.himher(), '''. Wonder if Paloma could give ''', person.himher(), ''' something to for the headache. ''', person.HeShe(), ''' grimaces. Eh, maybe not. The day after the Vengador raid, Paloma had collapsed while cleaning her infirmary. Adrian and Ildri swiftly brought in a pair of Sisters, who diagnosed Paloma with a severe case of magic deficiency. The exact same kind of magic deficiency that makes the Wasting Wail so deadly. Apparently, ''', universal.state.player.name, ''' hadn't been the only person Paloma was fully healing multiple times during the raid, and the constant strain of repeatedly slinging such an exhausting spell had very nearly killed her. The Sisters spent over an hour working to get Paloma's magic back up to sustainable levels without shocking her system. She's spent the past month recovering.'''],
['''''', universal.state.player.name, ''' sighs and slowly stands. Better get this cleaned up. The last time ''', person.heshe(), ''' was less than prompt about cleaning up hangover induced vomit, ''', person.heshe(), ''' spent a solid fifteen minutes over Ildri's knee. Stupid Ildri and her stupid "My guild will be kept clean!" ''', universal.state.player.name, ''' grabs a small bucket of water ''', person.heshe(), ''' keeps next to the bed for just such emergencies, and a nearby rag, and began gingerly cleaning up ''', person.hisher(), ''' mess.'''],
['''Fifteen minutes later, ''', person.heshe(), ''' leaves ''', person.hisher(), ''' room, and staggers down the hallway, and towards the kitchen. While passing Adrian's office, ''', universal.state.player.name, ''' picks up the sharp thwack of a paddling. ''', person.HeShe(), ''' hesitates. If ''', person.heshe(), ''' listens carefully, ''', person.heshe(), ''' can just make out voices. Sounds like Paloma and Adrian.'''],
['''"But it was an emergency!" wails Paloma.'''],
['''"Please. An emergency is when someone is dying. The only person who almost died was you." A series of bangs burst from the office, and Paloma wails.'''],
['''''', universal.state.player.name, ''' winces in sympathy.  Clearly, she's finally well enough to get her fanny tanned.'''],
['''''', universal.state.player.name, ''' shrugs, and moves on. ''', person.HeShe(), ''' enters the kitchen, wincing at the bright sunlight from the windows.'''],
['''Ildri and Alondra are standing at the counter, kneading several piles of dough. Ildri glances over her shoulder at ''', universal.state.player.name, '''. She wipes her hands on her apron, then turns and puts them on her hips. "Well, well. Look whose finally up."'''],
['''\child{"I didn't wake you, did I?"}{ep2 guild wake}'''],
['''\child{"Go stick your ugly face in someone else's business, you stupid old busybody."}{ep2 guild snap}'''],
['''\child{"Ugh."}{ep2 guild grunt}'''],
])
    
    ep2_guild_wake_up_extrovert.quip_function = ep2_guild_wake_up_extrovert_quip_function
    ep2_guild_wake = Node( 324 )

    def ep2_guild_wake_quip_function():
        ep2_guild_wake.quip = format_text_no_space([['''"Oh, you'd know if you'd woken me, trust me," says Ildri. She glances over her shoulder at Alondra, who is starting to move her dough onto a baking pan. She spins around and gives the girl a sharp swat. "You call that done? You put that in the oven, and half the loaf will be burned, the other hardly cooked!"'''],
['''Alondra yelps, and hops up on her toes. She quickly pulls the bread off the sheet, and plops it back on the counter. "Sorry, sorry. I just, you're so fast-"'''],
['''"Of course I'm fast," says Ildri. "I've been doing this since before you were born. Now, do it right. I'd rather one good loaf from you than half a dozen bad."'''],
['''"Erm, breakfast?" asks ''', universal.state.player.name, '''.'''],
['''Ildri jerks her head towards a small platter on the far end of the counter. "Some biscuits over there, a few small pieces of fruit, left over from the winter stores. Also a pitcher of water, sanitized by Paloma before her meeting with Adrian."'''],
['''\child{Blanch}{ep2 guild beer}'''],
['''\child{"Good. Thought of beer makes me want to hurl."}{ep2 guild water}'''],
])
    
    ep2_guild_wake.quip_function = ep2_guild_wake_quip_function
    ep2_guild_beer = Node( 325 )

    def ep2_guild_beer_quip_function():
        ep2_guild_beer.quip = format_text_no_space([['''Ildri shakes her finger at the Taironan. "Don't give me that face young ''', person.manlady(), '''. Drinking watered down beer is acceptable when you don't have potable water, but this is perfectly clean."'''],
['''''', universal.state.player.name, ''' grimaces, but doesn't try to argue. Instead, ''', person.heshe(), ''' makes ''', person.hisher(), ''' way towards the far end of the counter. ''', person.HeShe(), ''' snatches up half a dozen of the biscuits, and grabs a few slices of dried apples. ''', person.HeShe(), ''' opens a small container of conserves, and slathers some on the biscuits. Then, ''', person.heshe(), ''' wolfs the food down, glancing sideways at the pitcher of water. ''', person.HeShe(), ''' glances about, and ''', person.hisher(), ''' eyes light on the small box (kept chilled with a charm maintained by Airell) containing the beer. ''', person.HeShe(), ''' looks between the pitcher of water, and the container, then glances at Ildri, whose back is towards the icebox. The buxom cook is currently explaining the finer details of dough kneading to Alondra, who listens with a slightly bewildered look on her face.'''],
['''\child{Grab some beer! Ildri won't notice.}{ep2 guild beer}'''],
['''\child{Just drink the water. It'll probably make you feel better anyway.}{ep2 guild water}'''],
])
    
    ep2_guild_beer.quip_function = ep2_guild_beer_quip_function
    ep2_guild_take_beer = Node( 326 )

    def ep2_guild_take_beer_quip_function():
        ep2_guild_take_beer.quip = format_text_no_space([])
        ep2_guild_take_beer.quip = ""
        if universal.state.player.stealth() +  random.randint(4)  >= 8:
            ep2_guild_take_beer.children = ep2_guild_take_beer_success.children
            conversation.say_node(ep2_guild_take_beer_success)
            
        elif universal.state.player.stealth() +  random.randint(4)  < 8:
            ep2_guild_take_beer.children = ep2_guild_take_beer_failure.children
            conversation.say_node(ep2_guild_take_beer_failure)


    
    ep2_guild_take_beer.quip_function = ep2_guild_take_beer_quip_function
    ep2_guild_take_beer_success = Node( 327 )

    def ep2_guild_take_beer_success_quip_function():
        ep2_guild_take_beer_success.quip = format_text_no_space([['''''', universal.state.player.name, ''' slowly sidles to the far end of the counter, closest to the icebox. ''', person.HeShe(), ''' pretends to pour some water in ''', person.hisher(), ''' glass and take a drink, watching Ildri and Alondra over the top of the glass. Alondra begins hesitantly kneading the dough. Ildri watches the girl for a moment, then gives her a light swat, and starts speaking animatedly, while slowly kneading the dough.'''],
['''Seeing ''', person.hisher(), ''' chance, ''', universal.state.player.name, ''' turns, and slinks over to the box. ''', person.HeShe(), ''' slowly opens the door a crack, sneaks ''', person.hisher(), ''' hand in and pulls out a pitcher of beer. ''', person.HeShe(), ''' quickly pours half a glass, and slips the pitcher back in the icebox. ''', person.HeShe(), ''' silently closes the door and slips back over to ''', person.hisher(), ''' breakfast. ''', person.HeShe(), ''' takes a swig of the cold alcohol and sighs in satisfaction. Success!'''],
['''''', universal.state.player.name, ''' finishes ''', person.hisher(), ''' breakfast, sighing as the delicious food fills ''', person.hisher(), ''' empty belly. ''', person.HisHer(), ''' headache has already faded to manageable levels. Perhaps it's time to see if Adrian has a job for ''', person.himher(), '''? It's been a month, and ''', person.heshe(), ''' has had nothing to do except help get the guild back together (which hardly counts)! There'd better be something today, or ''', universal.state.player.name, ''' just might just go crazy.'''],
])
    
    ep2_guild_take_beer_success.quip_function = ep2_guild_take_beer_success_quip_function
    ep2_guild_take_beer_failure = Node( 328 )

    def ep2_guild_take_beer_failure_quip_function():
        ep2_guild_take_beer_failure.quip = format_text_no_space([['''''', universal.state.player.name, ''' watches Ildri and Alondra for a moment. The two seem pretty absorbed in the intricacies of dough kneading. ''', person.HeShe(), ''' turns, and hastens over to the icebox, quickly yanking it open, and going for the beer pitcher.'''],
['''In the middle of pulling the pitcher free, someone taps ''', person.himher(), ''' on the shoulder.'''],
['''''', universal.state.player.name, ''' swallows uneasily, and glances over ''', person.hisher(), ''' shoulder. Ildri ''']])
        if ildri.towers_over(universal.state.player):
            ep2_guild_take_beer_failure.quip = format_text_no_space([[ep2_guild_take_beer_failure.quip,'''towers over''']])
        else:
            ep2_guild_take_beer_failure.quip = format_text_no_space([[ep2_guild_take_beer_failure.quip,'''stands behind''']])
        ep2_guild_take_beer_failure.quip = format_text_no_space([[ep2_guild_take_beer_failure.quip,''' ''', person.himher(), ''' with her arms crossed and an annoyed look on her face.'''],
['''\child{Maybe if you smile innocently enough, she won't notice your arm sticking out of the icebox!}{ep2 innocent smile}'''],
['''\child{"Umm...Ildri. Hi. Nice weather we're having, huh?"}{ep2 greet ildri}'''],
['''\child{"So I'm drinking beer. I'm an adult, I can drink whatever I want. Now leave me alone!"}{ep2 beer bratty}'''],
])
    
    ep2_guild_take_beer_failure.quip_function = ep2_guild_take_beer_failure_quip_function
    ep2_innocent_smile = Node( 329 )

    def ep2_innocent_smile_quip_function():
        ep2_innocent_smile.quip = format_text_no_space([['''''', universal.state.player.name, ''' puts on ''', person.hisher(), ''' best smile of pure innocence.'''],
['''Ildri raises an eyebrow.'''],
['''''', universal.state.player.name, ''''s''', ''' smile falters a little.'''],
['''"You might want to remove your hand, and close the door," says Ildri. "You're letting all the cold air out."'''],
['''''', universal.state.player.name, ''''s''', ''' anxiously bites down on ''', person.hisher(), ''' lower lip, as ''', person.heshe(), ''' slowly removes ''', person.hisher(), ''' hand. So much for that brilliant plan.'''],
['''''']])
        if ildri.taller_than(universal.state.player):
            ep2_innocent_smile.quip = format_text_no_space([[ep2_innocent_smile.quip,'''As Ildri continues to glare down at ''', universal.state.player.name, ''', ''', universal.state.player.name, ''' becomes acutely aware of just how tall the guild mistress is. Very tall. Tremendously tall. The kind of tall that goes with lots of strength. The kind of strength that interferes with sitting for several days.''']])
        else:
            ep2_innocent_smile.quip = format_text_no_space([[ep2_innocent_smile.quip,'''Despite their comparable heights, Ildri seems to tower over ''', universal.state.player.name, ''', as if the woman had grown six inches in the past six seconds. Kind of like Nana. How do they do that?''']])
        ep2_innocent_smile.quip = format_text_no_space([[ep2_innocent_smile.quip,''''''],
['''\continue{Ildri scolding continue}{ep2 ildri scolding}'''],
])
    
    ep2_innocent_smile.quip_function = ep2_innocent_smile_quip_function
    ep2_greet_ildri = Node( 330 )

    def ep2_greet_ildri_quip_function():
        ep2_greet_ildri.quip = format_text_no_space([[''''''],
['''"It's rained three out of the past five days," says Ildri, tapping the fingers of her right hand against her left bicep.'''],
['''"Erm, yes. Yes it has," says ''', universal.state.player.name, '''. "Don't you just love the rain?"'''],
['''"All the rain ruined my garden."'''],
['''"Oh. I'm sorry."'''],
['''"Mostly because Alondra forgot to put a tarp over it."'''],
['''"Yes. I, uh, heard the spanking." ''', universal.state.player.name, ''' slowly pulls ''', person.hisher(), ''' numb arm out of the ice box, and pushes the box closed.'''],
['''"Sounded like it hurt didn't it?" asks Ildri, watching as ''', universal.state.player.name, ''' pulls ''', person.hisher(), ''' arm free, and tries to shake sensation back into it.'''],
['''"Um, yeah. Went on for a while too," says ''', universal.state.player.name, '''.'''],
['''"Well, I do love my garden. You know what else I love?" asks Ildri.'''],
['''"I dunno. What?"'''],
['''Ildri leans in close to ''', universal.state.player.name, ''', who shrinks back against the icebox. "When bratty little party animals do what I tell them."'''],
['''"Oh." ''', universal.state.player.name, ''' laughs uneasily, ''', person.hisher(), ''' bottom frantically clenching and unclenching. "That's, um, yeah. That makes sense. I mean, who doesn't love that?"'''],
['''\continue{Ildri scolding continue}{ep2 ildri scolding}'''],
])
    
    ep2_greet_ildri.quip_function = ep2_greet_ildri_quip_function
    ep2_ildri_scolding = Node( 331 )

    def ep2_ildri_scolding_quip_function():
        ep2_ildri_scolding.quip = format_text_no_space([[''''''],
])
    
    ep2_ildri_scolding.quip_function = ep2_ildri_scolding_quip_function
    ep2_beer_bratty = Node( 332 )

    def ep2_beer_bratty_quip_function():
        ep2_beer_bratty.quip = format_text_no_space([['''''', universal.state.player.name, ''' has barely finished the sentence, before ''', person.heshe(), ''' finds ''', person.himselfherself(), ''' tucked under Ildri's arm, ''']])
        if ildri.towers_over(universal.state.player):
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''''', person.hisher(), ''' feet dangling in mid-air as Ildri hoists ''', person.himher(), ''' completely off the ground.''']])
        else:
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''''', person.hisher(), ''' feet scrambling against the floor.''']])
        ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,''' The woman's large, hard hand starts smashing into ''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.muscle_adj(), ''' bottom. ''', universal.state.player.name, ''' squeals and kicks as hot pain blooms in ''', person.hisher(), ''' ''', universal.state.player.clad_bottom(pajama=True), ''' cheeks.'''],
['''"Not when it's my beer you can't," says Ildri, her punishing hand making ''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.bum_adj(), ''' bottom ''']])
        if universal.state.player.is_soft():
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''ripple''']])
        elif universal.state.player.is_fit():
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''jiggle''']])
        else:
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''jump''']])
        ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''. "You've spent almost every night of the past month drinking like a fish, and I'll be cursed if I let you drink during the day too!"'''],
['''"Well, maybe I-oww!-wouldn't-yeouch!-drink so much if-oww oww oww!-Adrian would give me a cursed-oww!- job," cries ''', universal.state.player.name, '''.'''],
['''"He'll give you a job when he gets one that matches your skill," says Ildri, her hand never slowing. "He warned you that it'd be one a month at best."'''],
['''"But I'm so bo-owww!" wails ''', universal.state.player.name, '''.'''],
['''"Bored? Well we can't have that," says Ildri. "I have a dozen and one things you can do."'''],
['''"That's not-oww!" ''']])
        if ildri.taller_than(universal.state.player) or ildri.height == universal.state.player.height:
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''''', universal.state.player.name, ''' kicks ''', person.hisher(), ''' dangling feet.''']])
        else:
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''''', universal.state.player.name, ''' stomps ''', person.hisher(), ''' foot against the ground.''']])
        ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,''' "I don't want to fix some ugly, smelly kitchen! I want to adventure!"'''],
['''Alondra gasps.'''],
['''"Ugly?" growls Ildri. She cracks her hand against ''', universal.state.player.name, ''''s''', ''' right sitspot with stunning force. "Smelly? Ohhh, you're getting it now young ''', person.manlady(), '''. Alondra, fetch me my spanking stool. Then, go to Adrian and borrow his razor strop. I have a brat who needs a lesson in manners."'''],
['''"No!" wails ''', universal.state.player.name, '''. ''', person.HeShe(), ''' pounds ''', person.hisher(), ''' fist against Ildri's calf. "Let me go, let me go!"'''],
['''Alondra hurries over, a small footstool gripped in both hands.'''],
['''''', universal.state.player.name, ''' glares at Alondra.'''],
['''"Oh don't give me that look," says Alondra, setting the stool down next to Ildri. "You'd do the same if our positions were reversed. Madre's love, you have done the same."'''],
['''Ildri puts her foot on the stool, swings ''', universal.state.player.name, ''' around, lifts the Taironan a few more inches, and drapes ''', person.himher(), ''' across her lap. ''', universal.state.player.name, ''''s''', ''' arms and legs dangle uselessly, ''', person.hisher(), ''' hands and feet ''']])
        if universal.state.player.is_average_or_shorter():
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''hanging well above the floor.''']])
        else:
            ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,'''a scant few inches above the floor.''']])
        ep2_beer_bratty.quip = format_text_no_space([[ep2_beer_bratty.quip,''''''],
['''Ildri ''', person.lowerslifts(universal.state.player.pajama_bottom()), 's', ''' ''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.pajama_bottom().name, ''', revealing ''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.bum_adj(), ''', ''', universal.state.player.muscle_adj(), ''' bottom. ''', universal.state.player.name, ''' kicks ''', person.hisher(), ''' legs, wailing as ''', person.hisher(), ''' bare lower body is exposed to Ildri.'''],
['''"Oh, stop whining," says Ildri, slapping ''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.muscle_adj(), ''' cheeks with swift, stinging slaps. "It's not like I've never seen it before. Remember that time you threw up and left it to dry all night?"'''],
['''''', universal.state.player.name, ''' whimpers, and clutches Ildri's leg, as ''', person.heshe(), ''' sways on the large woman's thigh.'''],
['''"Don't worry, I won't let you fall," says Ildri, her hand spreading a buzzing sting across ''', universal.state.player.name, ''''s''', ''' upthrust bottom. "Can't spank you if you fall off, now can I? Ahh. Alondra. Thank you, dear."'''],
['''''', universal.state.player.name, ''' glances up, sucking in a breath as ''', person.heshe(), ''' watches Alondra hand Ildri the leather strop. "Aww, come on! That's for sharpening razors, not hitting people!"'''],
['''"Actually, they're used to straighten a blade, not sharpen it," says Ildri. She snaps the strop across ''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.bum_adj(), ''' bottom. ''', universal.state.player.name, ''' throws ''', person.hisher(), ''' head back and howls at the sharp sting. ''', person.HeShe(), ''' starts to frantically kick ''', person.hisher(), ''' feet, and thrash ''', person.hisher(), ''' body across Ildri's thigh.'''],
['''"Hold still," snaps Ildri, tightening her grip on ''', universal.state.player.name, ''''s''', ''' back, and applying the strop with great prejudice. "Or I'll hold you up by your ankles, and strap you upside down."'''],
['''''', universal.state.player.name, ''' tries to still ''', person.hisher(), ''' kicking feet, but ''', person.heshe(), ''' still can't help but flail a little as the leather snaps repeatedly across ''', person.hisher(), ''' bare, vulnerable bottom.'''],
['''After a few minutes, and many horribly painful strokes, Ildri sets the strop on the counter, lifts ''', universal.state.player.name, ''' off her thigh, and sets ''', person.himher(), ''' back on the ground.'''],
['''''', universal.state.player.name, ''''s''', ''' hands immediately fly back to ''', person.hisher(), ''' bottom, giving it a fierce rub before ''', person.lowerlift(universal.state.player.lower_clothing()), '''ing ''', person.hisher(), ''' ''', universal.state.player.pajama_bottom().name, ''' back over ''', person.hisher(), ''' throbbing bottom.'''],
['''"Now, finish your breakfast," says Ildri curtly. "Alondra, let's get back to the bread."'''],
['''''', universal.state.player.name, ''' pouts, but does as directed, one hand rubbing ''', person.hisher(), ''' aching bottom, while the other shovels food into ''', person.hisher(), ''' mouth.'''],
['''Stupid Ildri and her stupid water.'''],
['''Ah, well. Perhaps it's time to see if Adrian has a job for ''', person.himher(), '''? It's been a month, and ''', person.heshe(), ''' has had nothing to do except help get the guild back together (which hardly counts)! There'd better be something today, or ''', universal.state.player.name, ''' just might just go crazy.'''],
[''''''])
    universal.state.player.marks.append('''''', universal.state.player.name, ''''s''', ''' ''', universal.state.player.bum_adj(), ''' ''', universal.state.player.muscle_adj(), ''' bottom is marred by several long, broad marks in the shape of a razor strop. ''', person.HeShe(), ''' gives one of the marks a tender rub, and makes ''', person.himselfherself(), ''' a silent promise never to raid Ildri's beer without her permission again.'''
    format_text_no_space([ep2_beer_bratty.quip, [''''''],
])
    
    ep2_beer_bratty.quip_function = ep2_beer_bratty_quip_function
    ep2_guild_water = Node( 333 )

    def ep2_guild_water_quip_function():
        ep2_guild_water.quip = format_text_no_space([[''''''],
])
    
    ep2_guild_water.quip_function = ep2_guild_water_quip_function
    ep2_guild_snap = Node( 334 )

    def ep2_guild_snap_quip_function():
        ep2_guild_snap.quip = format_text_no_space([[''''''],
])
    
    ep2_guild_snap.quip_function = ep2_guild_snap_quip_function
    ep2_guild_grunt = Node( 335 )

    def ep2_guild_grunt_quip_function():
        ep2_guild_grunt.quip = format_text_no_space([[''''''],
])
    
    ep2_guild_grunt.quip_function = ep2_guild_grunt_quip_function
    ep2_guild_wake_up_introvert = Node( 336 )

    def ep2_guild_wake_up_introvert_quip_function():
        ep2_guild_wake_up_introvert.quip = format_text_no_space([[''''''],
])
    
    ep2_guild_wake_up_introvert.quip_function = ep2_guild_wake_up_introvert_quip_function
    ep2_marias_wake_up = Node( 337 )

    def ep2_marias_wake_up_quip_function():
        ep2_marias_wake_up.quip = format_text_no_space([[''''''],
])
    
    ep2_marias_wake_up.quip_function = ep2_marias_wake_up_quip_function


def start_scene_1_episode_2(loading=False):
    guild = universal.state.get_room("Adventurer's Guild")
    deidre = universalstate.get_character("Deidre.person")
    textCommands.enterLeft(deidre, guild)
    universal.state.player.litany = conversation.allNodes[321]