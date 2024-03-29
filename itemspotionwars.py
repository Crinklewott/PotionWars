
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
import enchantments
import enchantmentspotionwars
import items
import spanking
import person
import universal
from universal import *


#-----------------------------------Upper Armor----------------------------
lamellarArmor = items.UpperArmor('lamellar armor', 'A sequence of thick rawhide leather plates tied together with thick strings. ' +  
'It is fairly flexible, but much thicker and heavier than clothing leather. However, because it does not contain much (if any) iron, it does not interfere with spellcasting.', attackDefense=6,
attackPenalty=1, price=400)

chainCuirass = items.UpperArmor('chain cuirass', 'A rigid shirt of interlocking links of metal. Though it provides better protection than the laminar armor, the fact that the majority ' +
'of the weight rests on your shoulders makes a chain cuirass much harder to move around in. Furthermore, the iron in the cuirass interferes with magical currents, making it harder to cast spells. On the plus side, the iron protects against spells that involve pure magic.', price=800, attackDefense=10, attackPenalty=4, castingPenalty=4, 
magicDefense=4)

plateArmor = items.UpperArmor('plate armor', 'A breastplate made of steel and chain. It provides much better protection than the chain cuirass, and surprisingly enough is ' + 
'even easier to move around in. This is because the weight of the armor is more evenly distributed about your body than a chain cuirass. However, it contains much more iron than the chain cuirass, making it significantly more difficult to cast spells in. Though on the flip side, it provides better protection from spells that rely on raw magical power.', price=2000, attackDefense=25, attackPenalty=3, castingPenalty=7, 
    magicDefense=7)

batteredLeatherBreastplate = items.UpperArmor('battered leather breastplate', 'An old, dented leather breastplate.', attackDefense=4, attackPenalty=1, price=150)

#------------------------------------Shirts---------------------------------------

tunic = items.Shirt('tunic', 'A fairly common, loose fitting tunic. A bit worn, but otherwise in good shape.', price=5) 

raggedTunic = items.Shirt('ragged tunic', 'A ragged, borderline useless tunic.', price=1, risque=1)

powderBlueTunic = items.Shirt('powder blue shirt', "A soft, powder blue dress spun from fine cotton without any trim.", price=25)
flowerPrintShirt = items.Shirt('yellow shirt', "A small yellow shirt made for preteen boys, and spun from fine cotton.", price=25)

vNeckTunic = items.Shirt('V-neck tunic', 'A cotton tunic with a deep v-shaped slit down the front, revealing a fair amount of the upper chest.', price=5, risque=2)

alondrasVNeckTunic = items.Shirt("Alondra's V-neck", 'A cotton tunic with a deep v-shaped slit down the front, revealing a fair amount of the upper chest. Belongs to Alondra.', price=0, risque=2)


blouse = items.Shirt('blouse', 'A plain, white, loose-fitting blouse.', price=5)

bra = items.Shirt('bra', format_line(['Recent research has shown that people who wear shirts are baby-eating, Mother-hating scum who are secretly planning to steal''',
    '''your husband's sword. Be a true Avaricumite. Wear nothing but a bra today (and pants. Or a teeny tiny skirt. Or just panties.)!''']), risque=4)

blueVest = items.Shirt('blue vest', 'A bright blue vest and white undershirt, cut in the style of outfits worn by young boys in the middle and upper classes.', price=10)

shirtRags = items.Shirt('shirt rags', 'A collection of rags that were once a shirt. Could be wrapped around the chest for something approximating clothing, or sold for a' +
    'few coins.', price=3)

#--------------------------------------Lower Armor--------------------------------

#--------------------------------------items.Pants-------------------------------------
trousers = items.Pants('trousers', 'Simple loose-fitting trousers. They are a bit ragged, but more or less in one piece.', tightness=items.LOOSE, price=5)

shorts = items.Shorts('shorts', 'A pair of knee-length cotton shorts.', tightness=items.LOOSE, price=5)

shortShorts = items.Shorts('short shorts', "A pair of skintight shorts that barely cover one's bottom.", tightness=items.TIGHT, price=5, risque=3)

holeyTrousers = items.Pants('holey trousers', 'A pair of ragged, borderline unwearable trousers. There is a massive hole in the left knee, the right leg stops in a frayed mess just pass the knee, and the waist is held up with a threadbare rope.', tightness=items.LOOSE)

flowerPrintTrousers = items.Pants('yellow trousers', "A small pair of dark yellow pants made for preteen boys, and spun from fine cotton.", price=25, tightness=items.LOOSE)
powderBlueTrousers = items.Pants('powder blue trousers', "A pair of soft, powder blue trousers spun from fine cotton without any trim.", price=25, tightness=items.LOOSE)
blueShorts = items.Shorts('blue shorts', 'A pair of blue shorts cut in a style similar to what young boys wear in the middle and upper classes.', price=10, tightness=items.LOOSE)

cutoffShorts = items.Shorts('cut off shorts', "A pair of cut-off leather shorts that barely cover one's bottom.", price=0, risque=4, tightness=items.TIGHT)

#---------------------------------------items.Skirts------------------------------------
combatSkirt = items.Skirt('combat skirt', 'A skirt that extends down to just shy of the knees. There is the faintest hint of magic. Not much, but enough that the skirt likely provides some limited combat protection.', price=5, attackDefense=2, tightness=items.LOOSE)

plainSkirt = items.Skirt('skirt', 'A simple cotton skirt that extends down to just past the knees.', 
        price=5, tightness=items.LOOSE)

miniSkirt = items.Skirt('miniskirt', 'A tight leather skirt that extends about halfway down the thigh.', 
        price=5, risque=2, tightness=items.TIGHT)

pencilSkirt = items.Skirt('pencil skirt', 'A narrow, black skirt that extends just past the knees. The skirt has a slit in back to minimize movement restriction.',
        price=5, risque=1, tightness=items.TIGHT)

alondrasSkirt = items.Skirt("Alondra's Skirt", "A plain wool skirt belonging to Alondra", price=0, risque=0, tightness=items.LOOSE)

skirtRags = items.Skirt('skirt rags', 'The remnants of a skirt. Can be wrapped around the waist for something approximating clothing, or sold for a few coins.',
        price=3, risque=3, tightness=items.LOOSE)


#------------------------------------items.Underwear-------------------------------------
modestUnderwear = items.Underwear("underwear", universal.format_line(['A plain, modest pair of underwear that', 'covers the entire bottom.']), price=3)

silkPanties = items.Underwear('silk panties', universal.format_line(["A very well-made and comfortable pair of",
    "black silk panties that leave the lower-half of one's bottom exposed."]), price=50, baring=True, risque=5)

underShorts = items.Underwear('undershorts', universal.format_line(['A pair of shorts that extend about a quarter',
    'of the way down the thigh. Such shorts are often worn underneath skirts to better protect', 
    'a woman\'s modesty. Particularly useful if she tends to engage in acrobatics (combat related',
    'or otherwise).']), price=3)

thong = items.Thong('thong', ' '.join(['An undergarment that covers the genitalia, but leaves the',
    'bottom bare (except for a narrow strip of cloth that runs between the cheeks).']), price=3, risque=5)

carriesGString = items.Thong("Carrie's G-String", ' '.join(["A teeny tiny little pair of purple panties, consisting of a teeny tiny little string in the back. The front is barely more than that. Why",
    "anyone would even bother wearing underwear this tiny is a mystery for the ages."]), risque=6)

lacyUnderwear = items.Underwear('lacy underwear', 'A pair of white, flowery, lacy underwear that leaves the lower-half of the bottom bare.', baring=True, price=3, risque=4)

boyShorts = items.Underwear('boyshorts', 'A pair of dark red boyshorts that completely cover the bottom.', price=3)

speedThong = items.Thong('loincloth of speed', ' '.join(["A brown loincloth that leaves the majority of the wearer's cheeks exposed. It is lightly imbued with magic. The magic provides the wearer with improved fine motor",
    '''control over their legs, improving the wearer's ability to move speedily. Provides a +1 bonus to speed.''']), price=50, 
    enchantments=[enchantments.StatEnchantment(1, universal.SPEED, 1)], risque=5)

chainmailBikini = items.Thong('chainmail bikini', "A two piece set of chainmail. The top piece covers a woman's breasts, but nothing else. The bottom is a chainmail thong. Though it looks as useless as useless can be, the armor is in fact infused with tremendously powerful magic that allows it to provide protection that's almost as good as a chain cuirass. Furthermore, thanks to the leather backing, the fact that the chain is very very finely woven, and a touch of magic, the armor is just as comfortable as thong lingerie (which admittedly isn't THAT comfortable, unless you like wedgies), just a little bit heavier. Furthermore, because the iron in the armor covers only a small part of one's body, the armor has a negligible impact on magic.", price=5000, attackDefense=16, risque=6, maxEnchantment=2) 

chainmailThong = items.Thong('chainmail thong', "A chainmail thong. Though it looks as useless as useless can be, the armor is in fact infused with tremendously powerful magic that allows it to provide protection that's just as good as a chain cuirass. Furthermore, thanks to the leather backing, the fact that the chain is very very finely woven, and a touch of magic, the armor is just as comfortable as thong lingerie (which admittedly isn't THAT comfortable, unless you like wedgies), just a little bit heavier. Furthermore, because the iron in the armor covers only a small part of your body, the armor only has a much smaller penalty to magic than a chain (or plate) cuirass.", price=5000, attackDefense=16, risque=6, maxEnchantment=2)


#--------------------------Full Armor---------------------------------------
fullPlate = items.FullArmor('full plate', "A full suit of plate mail, that completely covers your body. It provides excellent protection, and is surprisingly light. However, it takes up both the upper and lower armor slots. Furthermore, because it covers your body from head to toe, casting magic out of it is all but impossible.", price=1000, 
        attackDefense=36, attackPenalty=4, castingPenalty=10, magicDefense=10)

#------------------------Dresses---------------------------------------
wornDress = items.Dress('worn dress', "An old, ragged wool dress.", tightness=items.LOOSE)
blueDress = items.Dress('blue dress', "A soft blue cotton dress without any trim. This type of dress is worn by Younger Sisters of the Healer Persuasion in the Mother's Church.", tightness=items.LOOSE)

powderBlueDress = items.Dress('powder blue dress', "A soft, powder blue dress spun from fine cotton without any trim.", price=50, tightness=items.LOOSE)
flowerPrintDress = items.Dress('flower print dress', "A small, flower print yellow dress made for preteen girls, and spun from fine cotton.", price=50, tightness=items.LOOSE)

blackDress = items.Dress('black dress', "A long, slinky black dress that extends from the bottom of your neck to your ankles, but hugs your form in all the right places. A " +
"slit runs up the side of the dress to allow for front-saddle riding.", price=20, risque=2, tightness=items.TIGHT)

sunDress = items.Dress('sun dress', 'A low-cut cotton dress that extends to about two-thirds down the thigh.', price=20, risque=3, tightness=items.LOOSE)

deidresDress = items.Dress("Deidre's dress", "A black dress with red trim made from high quality cotton. The dress is floor-length on Deidre, and is cut to balance professionalism with showing off Deidre's average bust, shapely hips and long legs. Though an elegant dress, it can interfere with combat and other highly physical activities.", 
        attackDefense=4, attackPenalty=1, tightness=items.LOOSE)

pinkDress = items.Dress('pink dress', 'A modest pink dress cut in a style similar to what young children of the middle and upper classes tend to wear.', price=20, tightness=items.LOOSE)

carriesDress = items.Dress("Carrie's dress", "A low-cut, tight, rich purple dress that extends to about halfway down Carrie's thighs. Comes with black cotton tights.", price=0, tightness=items.TIGHT)

alondrasDress = items.Dress("Alondra's dress", "A plain wool dress that Alondra made for herself. Has a slight V-neck that shows off a bit of her plushy breasts, and the skirt hugs her hips just enough to show off her wide hips and round bottom, but not so tightly as to interfere with movement.", price=0) 


#------------------------Robes----------------------------------------
wornRobe = items.Robe('worn robe', "An old, ragged wool robe.")
robe = items.Robe("robe", "A warm, bulky outfit often worn by men who wish they were women, but don't have the guts to wear a dress.")
#---------------------Weapons---------------------------------------------
#------------------------------Knives------------------------------------
familyDagger = items.Knife('family dagger', "Engraved on the hilt is a green, serpentine dragon. Though the weapon itself is nothing special, the intricate hilt design would fetch it a very nice price, assuming one didn't mind selling a family heirloom.", price=100)

neciasDagger = items.Knife("Necia's dagger", "A very high quality dagger used by a Vengador.", genericBonus=1, 
        price=75) 

knuckleDagger = items.Knife('knuckle dagger', ' '.join(["A dagger whose handle doubles as brass knuckles (made from wood). The knuckles allow the user to either stab an enemy, or punch them with the knuckles. However, the restrictive knuckles",
    "limit the number of combat grips. The knuckle dagger does more damage than the family dagger, and gets a higher bonus to damage when grappling, but is harder to grapple with."]), minDamage=2, maxDamage=6, grappleAttempt=-1, grappleAttemptDefense=-3, 
    grappleBonus=2, price=50)

stiletto = items.Knife('stiletto', ' '.join(["When not affixed to a woman's heel, these long, thin daggers have been making life pleasant for assassins for decades. Long, thin, feather light, and very fast, a stiletto is a grappler's dream. However, they aren't",
    "particular heavy, and aren't as useful against heavily armored enemies."]), minDamage=3, maxDamage=4, grappleAttempt=2, grappleAttemptDefense=2, grappleBonus=2, price=50)

mariasDagger = items.Knife("Maria's dagger", "A beautifully made war dagger with a wicked edge. The weapon seems to gleem faintly, a sign of the magic that was imbued into the steel at its time of forging.", genericBonus=4)

batteredDagger = items.Knife('battered dagger', "A dull, heavily knicked war dagger.", genericBonus=-1)
    
dagger = items.Knife('dagger', "A large, wicked looking dagger.", price=10)


#-------------------------Swords------------------------------------------
longSword = items.Sword('longsword', "A standard, double-edged sword. Often used as a sign of status by knights and other warriors of noble birth.", price=100)

familySword = items.Sword('family sword', "Engraved on the hilt is a green, serpentine dragon. Though the weapon itself is nothing special, the intricate hilt design would fetch it a very nice price, assuming one didn't mind selling a family heirloom.", price=150)

twoHandedSword = items.Sword('two handed sword', ' '.join(["Heavier and longer than a longsword. Its increased length means that it is more dangerous at arms length. Its heavy pommel and large crossguard also make it dangerous",
    "in a grapple (though not as dangerous as any dagger)."]), 
    minDamage=1, maxDamage=6, grappleAttempt=0, grappleAttemptDefense=1, grappleBonus=0, armslengthBonus=1, price=125)

#sideSword = items.Sword('side sword', ' '.join(["Halfway between a heavier longsword, and a thinner, faster rapier, the side sword is fast and light, making the weapon quite reliable. It is still heavy enough to possess some oomph to it, however, making it", 
#    "more useful against an armored opponent than a rapier. Its great speed makes it useful for holding off dagger-wielding brigands, while its accuracy makes it very reliable."]), minDamage=2, maxDamage=5, grappleAttempt=1, grappleAttemptDefense=1, price=75)

rapier  = items.Sword('rapier', ' '.join(["Long, thin and blinding fast, rapiers are considered a civilian's weapon, and are most effective against enemies in little to no armor. Their nimbleness and length provides quite a bit of defense against grapplers, and their", 
    "precision makes them very reliable. However, they are specialized for thrusting against unarmored opponents, so they are less than effective against armor. Their length also makes it awkward to initiate a grapple with."]), minDamage=3, maxDamage=4, 
    grappleAttempt=-1, grappleAttemptDefense=2, price=125)


#-----------------------------Spears-------------------------------------
warspear = items.Spear('warspear', "A heavy wooden pole with a thick metal spike on one end, and an iron band on the other for balance. Very dangerous when you can keep your opponents at arms length.", price=50, genericBonus=0)

familySpear = items.Spear('family spear', "Engraved on the spear shaft is a green, serpentine dragon. Though the weapon itself is nothing special, the intricate design would fetch it a very nice price, assuming one didn't mind selling a family heirloom.", price=100)

staff = items.Spear('staff', "A heavy wooden staff. Staff-wielders are specially trained in defensive combat. Therefore, although not as dangerous as a spear, a staff provides better protection against being grappled, and has a smaller penalty while grappled. A favorite weapon of spellslingers.", price=30, minDamage=1, maxDamage=1, 
        grappleAttempt=-3, grappleAttemptDefense=3, grappleBonus=-1,
        armslengthBonus=2)

wingedSpear = items.Spear('winged spear', ' '.join(["A spear just shy of six feet (1.82 meters). There is a heavy metal cap on the other that serves both as counter-balance and for bludgeoning."]),
        minDamage=2, maxDamage=6, grappleAttemptDefense=2, grappleAttempt=-1, price=75)

#halberd = items.Spear('halberd', ' '.join(["An eight foot (2.43) polearm with a heavy axehead on one end, and a spike on the other. Although a little bit slower and more unwieldy than a spear or a short spear, a halberd can do very serious damage to an enemy, even",
#    "one who is heavily armored. Their length and heaviness however make them borderline useless in a grapple. On the other hand, their length, and heavy axehead makes it quite difficult to grapple someone with a halberd."]), minDamage=1, maxDamage=10, 
#    grappleAttemptDefense=3, grappleAttempt=-4, grappleBonus=-3, price=150)

#-----------------------------------Implements---------------------------------
woodenSpoon = spanking.CombatImplement('wooden spoon', 'A large spoon made from wood. (Good for smacking naughty bottoms, too!)', severity=1)
leatherBelt = spanking.CombatImplement('leather belt', 'A wide, worn leather belt. Popular for both holding up pants and welting naughty bottoms.', severity=3)

def has_belt(person, beltMsg, noBeltMsg):
    return universal.msg_selector(leatherBelt in person.inventory(), {True:beltMsg, False:noBeltMsg})

#--------------------------------Generic Items--------------------------------
whiteRibbon = items.Item('White Ribbon', 'A simple, yet elegant white silk ribbon.')


#----------------------------------Pajamas-----------------------------------------
oldShirt = items.PajamaTop('old shirt', 'An old, but comfortable t-shirt, just perfect for sleeping in.', 0)
comfyShorts = items.PajamaPants('comfy shorts', 'A pair of soft, comfy short shorts just perfect for sleeping in.', 0)


largeShirt = items.FullPajamas('large shirt', 'A comfortable shirt that reaches about halfway down your thighs. Great for sleeping in.', 3)

alondrasChemise = items.FullPajamas("Alondra's Chemise", "A thin cotton worn by Alondra as nightwear. The chemise is quite low cut, showing off Alondra's large, firm breasts. It also just barely covers her wide hips and round, bouncy, protruding bottom.", 0)

dropSeatPJs = items.DropSeatPajamas('drop seat pajamas', 
    format_line(['A one-piece, full body set of comfy pajamas. Great for cooler nights. Comes with a dropseat to make midnight bathroom rooms as painless as possible.']),
    6)

pinkPajamaPants = items.PajamaPants('pink pajama pants', 
    'A pair of delightfully soft, bright pink pajama pants. Just tight enough to show off your ass, not tight enough to be uncomfortable.', 3)

pinkPajamaShirt = items.PajamaTop('pink pajama shirt', 'A delightfully soft, bright pink pajama shirt. Goes great with the pink pajama pants', 3)


bluePajamaPants = items.PajamaPants('blue pajama pants', 
    'A pair of delightfully soft, dark blue pajama pants. Just tight enough to show off your ass, not tight enough to be uncomfortable.', 3)

bluePajamaShirt = items.PajamaTop('blue pajama shirt', 'A delightfully soft, dark blue pajama shirt. Goes great with the blue pajama pants', 3)


#----------------------------------Gems-----------------------------------------

attackGem = items.Gem(
    'Attack Gem', 
    'Weapons enchanted with this gem gain a +1 bonus to damage. Clothing enchanted with the gem ' + 
    'gain a +1 bonus to defense.', 
    enchantmentspotionwars.AttackEnchantment)

poorWeaknessGem = items.Gem(
        'Poor Weakness Gem', 
        'Weapons enchanted with this gem have a ' +
        '2% chance to inflict weakness for three rounds on every attack. Clothing enchanted with' +
        'the gem ' +
        'provides the wearer with immunity from one casting of Weakness per battle.', 
        enchantmentspotionwars.poor_weakness_ennchantment)
