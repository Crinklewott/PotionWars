PotionWars
==========

The source code, and associated images for the text-based role playing game Pandemonium Cycle: The Potion Wars. Be warned this game has erotic content, and is very NSFW. The development blog can be 
found at spankingrpgs.com. There you can read monthly blog posts by me about the game's development, and download a binary for either Ubuntu or Windows 7.

Thank you for downloading the source-code for Pandemonium Cycle: The Potion Wars. I hope you enjoy it!

-------------------------Looking at the code-------------

The bulk of the source code is the result of about six months of crazy coding by a single individual (me). As such, it's more than a little bit messy. PotionWars.py is the main driver, episode1.py contains
the text of the first episode, and sp_rpg_engine.py contains the read-eval-print loop. Those are probably the best files to look at if you want to start tinkinger with the source code I've tried to make 
the filenames and
dependencies as clear as possible. The only major lack of clarity are the Magic classes. Those are defined in the person.py file, because magic and people depend on 
each other, so I couldn't really split them into two modules without a circular dependency, or some clever code that I didn't think of.

Note: Unless you're an experienced programmer with Python experience, it is NOT recommended that you try to use my engine to write your own game, using episode1.py as a model. This code is not geared
towards being an engine for casual programmers to write games. It's written by me, for me for the explicit purpose of writing my game. If you're more interested in writing a game than in tinkering with
source code, I highly recommend using a fully fleshed out RPG game creator, like RPG-Maker. Furthermore, do not
try to write the text directly in the source code using episode1.py as a model.

Currently (June 13 2014), I am developing a python
script (in parallel with writing the second episode) that will allow me to convert a (miniscule) fraction of LaTeX with some custom environments into python code of the
type seen in episode1.py. LaTeX is MUCH better for writing lots of text than Python, so this script will make it MUCH easier to use my code to write rpgs. Therefore, I 
would recommend that you wait until I've developed and published that script before trying to write your own game. Instead, sit back, relax, and plan out your game. Or,
begin learning some basic LaTeX if you don't know it already.

Also, as a little warning. You'll see at the top of my files "from universal import *" DO NOT DO THIS IN YOUR PYTHON CODE! EVER! I did it because I was stupid and
inexperienced, and going through and changing it would take way too long and result in way too many crashes due to Python's rather lazy approach to checking if code is
well-formed (doesn't check until it tries to execute it). This command has a lot of problems, including: making the code harder to follow, and most importantly: ANYTHING
YOU IMPORT USING THAT COMMAND DOES NOT GET UDATED IF YOU MODIFY THE VARIABLE FROM THE ORIGINAL FILE. For example, suppose we have two modules:

/*

Module 1:               Module 2:
x = 5                   from Module 1 import *
def f():                def g():
    global x                f()
    x += 1                  print(x)

Here, if we invoke g(), the terminal will print out "5" not "6." The reason is that when Python executes the from NAME import * command, it COPIES the objects being referenced by the variables 
into the other module. Therefore, any modifications to the variable in Module 1 will not show up in Module 2. I ... spent many hours trying to figure out why my code
was breaking so badly, before I learned about this "feature."


---------------Running the code--------------

If you would like to run my game directly using the Python source, you need two things:

1. Python 2.7 - 32 bit
2. Pygame-19.1- win32-py2.7.msi

Note: The version number and the bit type ARE VERY IMPORTANT. Python 3 and Python 2 are not compatible, and my game is written in Python 2, because when I started 
writing it, Pygame hadn't developed a stable version for Python 3. Furthermore, the bit type (32 vs. 64) for Python and Pygame MUST agree, and Pygame is only available for
32-bit (note that 32-bit programs work fine on 64-bit machines).

Once you have those two installed, you should be able to just right click on PotionWars.py and run it using IDLE.

Unfortunately, you won't be able to play with music, because the license I signed for it forbids me from releasing it unless I encrypt it (which would be useless, because
I will need to decrypt it in order to use it, and to decrypt I'll need to have the key in the source code), or bundle it with the application (which is what I'm doing). Sorry about that.


------------------------------------------------Game-----------------------------------------------------------------

The game's interface is (hopefully!) pretty self-explanatory. There are only a few things I would like to point out. For more details see the included manual (manual/potionwars.pdf). Note: The manual is currently a bit out of date with respect to combat. I'll update it when I get some time.

The game screen is split into two parts. The top two-thirds is the game world. This is where you will see text describing your character's actions, your location, and
your interactions with other characters.

The bottom third is the command window. This will display the list of available commands. A command of the form (C)ommand indicates that pressing the "C" key will
trigger Command. So, while in town, you will see the command (G)o. Pressing "G" allows you to travel to a different location. Some commands may have the () in the
middle: Co(M)mand. This is likely because there is another command that already uses the first letter of that word. In this case, you need to press "M" to trigger Command, 
not "C."

When in the dungeon mode, you move the player using the arrow keys. The up key moves forward, the down key moves back, and the left and right keys turn you
ninety degrees. The walls are split into squares. Some of the squares will have a second square inside them. These are doors, which you can go through by pressing "up,",
just like you were walking forward. You may also see colored squares. These indicate special events. The different colors mean different things, which I'll let you figure out
on your own. 

There are two styles of combat: armslength and grapple. When fighting at armslength, spears get bonuses, and daggers get penalties. Grappling gives daggers bonuses and
spears penalties. Swords suffer neither bonuses nor penalties, regardless of the fighting style. The primary benefit of grappling is that it forces most multi-target
spells to only target the grappler. This can be a good way of shutting down enemies who target more than one of your characters (though this won't come up in the first
episode, because your character is fighting alone). It's also useful for mitigating the danger from spear wielders.

Furthermore, iron disrupts magical energy. As a result, some spells will receive penalties when cast by or on a character wearing metal armor. The exceptions to this
rule are spells that don't rely on raw magical energy for their effect (such as firebolt. Flames still heat the iron and burn the recipient, regardless of whether they
were created by magic or not), or if it's a buff/healing spell that the caster casts on themselves (since the magical energy never has to travel through the iron
armor). Most buff, healing, status, and spectral spells will be affected. What this means is that iron armor protects a character from hostile spells, but 
also makes it harder for their allies to help them.

If you choose to (Q)uick Save, the game will be automatically saved in the file "quick.sav."

If you have any comments or criticims about the story or writing, please either comment on my blog at spankingrpgs.com, or send an e-mail to 
sprpgs+PWStory@gmail.com.

Any bug reports, post on my blog, or send me an e-mail at sprpgs+PWBugs@gmail.com

Any comments or criticisms on the gameplay, post on my blog, or send me an e-mail at sprpgs+PWGameplay@gmail.com

Any other general questions or concerns, post on my blog, or send me an e-mail at sprgs@gmail.com

When sending criticisms please try to make them constructive. Saying "This game sucks sweaty donkey balls" tells me absolutely nothing except that you don't like it.
Saying something like "The gameplay is really out of whack. The spell Spectral Breakage makes every other combat command redundant." is much more helpful.

