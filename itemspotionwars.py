
"""
Copyright 2014 Andrew Russell

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
from universal import *
import items
import spanking
import person


#-----------------------------------Upper Armor----------------------------
leatherCuirass = items.UpperArmor('leather cuirass', 'A leather breastplate. Often worn by foot soldiers, when they can afford any armor at all. The leather is very hard ' +  
'and rigid, and makes it slightly harder to breathe. However, because it does not contain much (if any) iron, it does not interfere with spellcasting.', attackDefense=2,
attackPenalty=1, price=70)

chainCuirass = items.UpperArmor('chain cuirass', 'A rigid shirt of interlocking links of metal. Though it provides better protection than the leather cuirass, the fact that the majority ' +
'of the weight rests on your shoulders makes a chain cuirass much harder to move around in. Furthermore, the iron in the cuirass interferes with magical currents, making it harder to cast spells. On the plus side, the iron protects against spells that involve pure magic.', price=120, attackDefense=4, attackPenalty=4, castingPenalty=4, 
magicDefense=4)

plateCuirass = items.UpperArmor('plate cuirass', 'A breastplate made of steel and chain. It provides much better protection than the chain cuirass, and surprisingly enough is ' + 
'even easier to move around in. This is because the weight of the armor is more evenly distributed about your body than a chain cuirass. However, it contains much more iron than the chain cuirass, making it significantly more difficult to cast spells in. Though on the flip side, it provides better protection from spells that rely on raw magical power.', price=220, attackDefense=9, attackPenalty=3, castingPenalty=7, 
    magicDefense=7)

batteredLeatherBreastplate = items.UpperArmor('battered leather breastplate', 'An old, dented leather breastplate.', attackDefense=2, attackPenalty=1, price=40)

#------------------------------------Shirts---------------------------------------

tunic = items.UpperArmor('tunic', 'A fairly common, loose fitting tunic. A bit worn, but otherwise in good shape.', price=5) 

qualityTunic = items.UpperArmor('quality tunic', 'A heavy tunic made from high quality leathers. The tunic also has the smallest hint of magic about it, providing ' +
'a little bit of protection from enemy blows.', attackDefense=1, price=10)

vNeckTunic = items.UpperArmor('V-neck tunic', 'A cotton tunic with a deep v-shaped slit down the front, revealing a fair amount of the upper chest.', price=5)

qualityVNeckTunic = items.UpperArmor('quality V-neck tunic', 'A high quality v-neck tunic. There\'s even a little bit of magic woven into it, providing a bit of protection.', price=10, attackDefense=1)

#--------------------------------------Lower Armor--------------------------------

#--------------------------------------items.Pants-------------------------------------
trousers = items.Pants('trousers', 'Simple loose-fitting trousers. They are a bit ragged, but more or less in one piece.', price=5)

shorts = items.Pants('shorts', 'A pair of knee-length cotton shorts.', price=5)

shortShorts = items.Pants('short shorts', "A pair of skintight shorts that barely cover one's bottom.", price=10)

holeyTrousers = items.Pants('holey Trousers', 'A pair of ragged, borderline unwearable trousers. There is a massive hole in the left knee, the right leg stops in a frayed mess just pass the knee, and the waist is held up with a threadbare rope.')

#---------------------------------------items.Skirts------------------------------------
combatSkirt = items.Skirt('combat skirt', 'A skirt that extends down to just shy of the knees. There is the faintest hint of magic. Not much, but enough that the skirt likely provides some limited combat protection, despite being made of cloth.', price=5, attackDefense=1)

plainSkirt = items.Skirt('skirt', 'A simple cotton skirt that extends down to just past the knees.', 
        price=5)

miniSkirt = items.Skirt('miniskirt', 'A tight leather skirt that extends about halfway down the thigh.', 
        price=5)

#------------------------------------items.Underwear-------------------------------------
modestUnderwear = items.Underwear("underwear", universal.format_line(['A plain, modest pair of underwear that', 'covers the entire bottom.']), price=3)

silkPanties = items.Underwear('silk panties', universal.format_line(['A very well-made and comfortable pair of',
    'black silk panties that leave the lower-half of a woman\'s bottom exposed.']), price=50, baring=True)

underShorts = items.Underwear('undershorts', universal.format_line(['A pair of shorts that extend about a quarter',
    'of the way down the thigh. Such shorts are often worn underneath skirts to better protect', 
    'a woman\'s modesty. Particularly useful if she tends to engage in acrobatics (combat related',
    'or otherwise).']), price=3)

thong = items.Thong('thong', ' '.join(['An undergarment that covers the genitalia, but leaves the',
    'bottom bare (except for a narrow strip of cloth that runs between the cheeks). If you\'re',
    'female, comes with a matching brassiere.']), price=3)

lacyUnderwear = items.Underwear('lacy underwear', 'A pair of white, flowery, lacy underwear that leaves the lower-half of the bottom bare.', baring=True, price=3)

boyShorts = items.Underwear('boyshorts', 'A pair of dark red boyshorts that completely cover the bottom.', price=3)

stealthThongBonus = [0 for i in range(universal.NUM_STATS)]
stealthThongBonus[universal.STEALTH] = 1
Thong = items.Thong('thong of stealth', ' '.join(['A V-string, dark red thong that is lightly imbued with magic. The magic provides the wearer with improved fine motor''',
    '''control over their legs, improving the wearer's ability to move stealthily. Provides a +1 bonus to Stealth.''']), price=200, 
    statBonuses=stealthThongBonus)

chainmailBikini = items.Thong('chainmail bikini', "A two piece set of chainmail. The top piece covers a woman's breasts, but nothing else. The bottom is a chainmail thong. Though it looks as useless as useless can be, the armor is in fact infused with tremendously powerful magic that allows it to provide protection that's almost as good as a chain cuirass. Furthermore, thanks to the leather backing, the fact that the chain is very very finely woven, and a touch of magic, the armor is just as comfortable as thong lingerie (which admittedly isn't THAT comfortable, unless you like wedgies), just a little bit heavier. Furthermore, because the iron in the armor covers only a small part of one's body, the armor has a negligible impact on magic.",price=5000, attackDefense=8) 

chainmailThong = items.Thong('chainmail thong', "A chainmail thong. Though it looks as useless as useless can be, the armor is in fact infused with tremendously powerful magic that allows it to provide protection that's just as good as a chain cuirass. Furthermore, thanks to the leather backing, the fact that the chain is very very finely woven, and a touch of magic, the armor is just as comfortable as thong lingerie (which admittedly isn't THAT comfortable, unless you like wedgies), just a little bit heavier. Furthermore, because the iron in the armor covers only a small part of your body, the armor only has a much smaller penalty to magic than a chain (or plate) cuirass.", price=5000, attackDefense=4)


#--------------------------Full Armor---------------------------------------
fullPlate = items.FullArmor('full plate', "A full suit of plate mail, that completely covers your body. It provides excellent protection, and is surprisingly light. However, it takes up both the upper and lower armor slots. Furthermore, because it covers your body from head to toe, casting magic out of it is all but impossible.", price=1000, 
        attackDefense=18, attackPenalty=4, castingPenalty=10, magicDefense=10)

#------------------------Dresses---------------------------------------
wornDress = items.Dress('worn dress', "An old, ragged wool dress.")
blueDress = items.Dress('blue dress', "A soft blue cotton dress without any trim. This type of dress is worn by Younger Sisters of the Healer Persuasion in the Mother's Church.")

blackDress = items.Dress('black dress', "A long, slinky black dress that extends from the bottom of your neck to your ankles, but hugs your form in all the right places. A " +
"slit runs up the side of the dress to allow for front-saddle riding.", price=20)

sunDress = items.Dress('sun dress', 'A low-cut cotton dress  that extends to just above the knees.', price=20)

deidresDress = items.Dress("Deidre's dress", "A black dress with red trim made from high quality cotton. The dress is floor-length on Deidre, and is cut to balance professionalism with showing off Deidre's average bust, shapely hips and long legs. Though an elegant dress, it can interfere with combat and other highly physical activities.", 
        attackDefense=2, attackPenalty=1)


#------------------------Robes----------------------------------------
wornRobe = items.Robe('worn robe', "An old, ragged wool robe.")
#---------------------Weapons---------------------------------------------
#------------------------------Knives------------------------------------
familyDagger = items.Knife('family dagger', "A war dagger, typically carried by fledgling warriors. Engraved on the hilt is a green, serpentine dragon. Though the weapon itself is nothing special, the intricate hilt design would fetch it a very nice price, assuming one didn't mind selling a family heirloom.", price=100)

qualityDagger = items.Knife('quality dagger', "A war dagger very similar to the Family Dagger. However this version is larger and better balanced.", genericBonus=1, price=50) 

mariasDagger = items.Knife("Maria's dagger", "A beautifully made war dagger with a wicked edge. The weapon seems to gleem faintly, a sign of the magic that was imbued into the steel at its time of forging.", genericBonus=4)

batteredDagger = items.Knife('battered dagger', "A dull, heavily knicked war dagger.", genericBonus=-1)
    
dagger = items.Knife('dagger', "A large, wicked looking dagger.", price=10)


#-------------------------Swords------------------------------------------
longsword = items.Sword('longsword', "A standard, one-handed, double-edged sword. Often used as a sign of status by knights and other warriors of noble birth.", price=100)

#-----------------------------Spears-------------------------------------
warspear = items.Spear('warspear', "A heavy wooden pole with a thick metal spike on one end, and an iron band on the other for balance. Very dangerous when you can keep your opponents at arms length.", price=50)

staff = items.Spear('staff', "A heavy wooden staff. Staff-wielders are specially trained in defensive combat. Therefore, although not as dangerous as a spear, a staff provides better protection against being grappled, and has a smaller penalty while grappled. A favorite weapon of spellslingers.", price=20, minDamage=1, maxDamage=1, 
        grappleAttempt=-3, grappleAttemptDefense=4, grappleBonus=-1,
        armslengthBonus=1)

#-----------------------------------Implements---------------------------------
woodenSpoon = spanking.CombatImplement('wooden spoon', 'A large spoon made from wood. (Good for smacking naughty bottoms, too!)', severity=1)
leatherBelt = spanking.CombatImplement('leather belt', 'A wide, worn leather belt. Popular for both holding up pants and welting naughty bottoms.', severity=3)

#--------------------------------Generic Items--------------------------------
whiteRibbon = items.Item('White Ribbon', 'A simple, yet elegant white silk ribbon.')
