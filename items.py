
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
import abc
import random

allItems = {}
class Item(universal.RPGObject):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, 
            statBonuses=None):
        self.name = name
        self.description = description
        self.price = price
        self.attackPenalty = attackPenalty
        self.attackDefense = attackDefense
        self.castingPenalty = castingPenalty
        self.magicDefense = magicDefense
        if statBonuses is None:
            import person
            statBonuses = [0 for i in range(universal.NUM_STATS)]
        self.statBonuses = statBonuses
        universal.state.add_item(self)

    def _save(self):
        raise NotImplementedError()

    def is_equippable(self):
        return False

    def __eq__(self, item):
        print(self)
        print(item)
        return self.name == item.name 
    def __ne__(self, item):
        return self.name != item.name

    def apply_bonuses(self, person):
        for stat in range(len(self.statBonuses)): 
            person.increase_stat(stat, self.statBonuses[stat])

    def remove_bonuses(self, person):
        for stat in range(len(self.statBonuses)): 
            person.decrease_stat(stat, self.statBonuses[stat])


    @abc.abstractmethod
    def display(self):
        return '\n'.join([self.name, self.description, 'Price: ' + str(self.price)])

    def get_price(self):
        return self.price

    @staticmethod
    def _load(dataList):
        raise NotImplementedError()

class Armor(Item):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, statBonuses=None):
        #print(' '.join([name, 'price:', str(price), 'attackDefense:', str(attackDefense)]))
        super(Armor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.armorType = 'armor'

    def is_equippable(self):
        return True
    
    def display(self):
        displayString = super(Armor, self).display()    
        return '\n'.join([displayString, 'attack defense: ' + str(self.attackDefense), 
            'attack penalty: ' + str(self.attackPenalty), 'casting penalty: ' + str(self.castingPenalty), 'casting defense: ' + str(self.magicDefense)])

class UpperArmor(Armor):
    armorType = 'chest armor'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, statBonuses=None):
        super(UpperArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.armorType = 'chest armor'

class FullArmor(Armor):
    armorType = 'full armor'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, statBonuses=None):
        super(FullArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.armorType = 'full armor'

class Dress(FullArmor):
    armorType = 'dress'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, statBonuses=None):
        super(Dress, self).__init__(name, description, attackDefense, attackPenalty, castingPenalty, magicDefense, price, statBonuses)
        self.armorType = 'dress'
    pass

class Robe(Dress):
    armorType = 'dress'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, statBonuses=None):
        super(Robe, self).__init__(name, description, attackDefense, attackPenalty, castingPenalty, magicDefense, price, statBonuses)
        self.armorType = 'robe'

class LowerArmor(Armor):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, statBonuses=None):
        super(LowerArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
    #def down_up

class Pants(LowerArmor):
    armorType = 'pants'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, statBonuses=None):
        super(Pants, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.armorType = 'pants'

class Shorts(Pants):
    armorType = 'shorts'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, statBonuses=None):
        super(Shorts, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.armorType = Shorts.armorType

class Skirt(LowerArmor):
    armorType = 'skirt'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, statBonuses=None):
        super(Skirt, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.armorType = 'skirt'

class Underwear(Armor):
    armorType = 'underwear'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, baring=False, armorType='underwear',
            statBonuses=None):
        super(Underwear, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, statBonuses)
        self.baring = baring
        self.armorType = armorType

class Thong(Underwear):
    armorType = 'thong'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, armorType='thong', statBonuses=None):
        super(Thong, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, True, armorType, statBonuses) 

class Weapon(Item):
    weaponType = 'weapon'   
    def __init__(self, name, description, price=0, minDamage=0, maxDamage=0, grappleAttempt=0, grappleAttemptDefense=0, grappleBonus=0, armslengthBonus=0, genericBonus=0,
            statBonuses=None):
        super(Weapon, self).__init__(name, description, price, statBonuses=statBonuses)
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.grappleAttempt = grappleAttempt
        self.grappleAttemptDefense = grappleAttemptDefense
        self.grappleBonus = grappleBonus
        self.armslengthBonus = armslengthBonus
        self.genericBonus = genericBonus
        self.weaponType = Weapon.weaponType

    def is_equippable(self):
        return True

    def display(self):
        displayString = super(Weapon, self).display()
        return '\n'.join([displayString, 
            'Damage:  ' + str(self.minDamage + self.genericBonus) + ' -> ' + str(self.maxDamage + self.genericBonus), 
            'grapple attempt: ' + str(self.grappleAttempt + self.genericBonus), 
            'grapple attempt defense: ' + str(self.grappleAttemptDefense + self.genericBonus), 
            'grapple bonus: ' + str(self.grappleBonus + self.genericBonus), 
            'armslength bonus: ' + str(self.armslengthBonus + self.genericBonus)])
            

    def grapple_bonus(self):
        return self.grappleBonus + self.genericBonus

    def attack_bonus(self, grappling):
        return (self.grappleBonus if grappling else self.armslengthBonus) + self.genericBonus

    def parry_bonus(self, grappling):
        """
            For now, this function returns the same thing as attack_bonus. They are split both to enhance readability, and because we may decide to modify this in the 
            future.
        """
        return self.attack_bonus(grappling)

    def damage(self, grappling):
        if self.minDamage == self.maxDamage:
            return self.minDamage + (self.grappleBonus if grappling else self.armslengthBonus) + self.genericBonus
        else:
            return random.randrange(self.minDamage, self.maxDamage) + (self.grappleBonus if grappling else self.armslengthBonus) + self.genericBonus


class Knife(Weapon):
    """
    Knives are exceptionally dangerous in close quarters, but all but useless if a 
    combatant is forced to keep their distance.
    """
    weaponType = 'knife'
    def __init__(self, name, description, price=0, minDamage=1, maxDamage=5, grappleAttempt=2, grappleAttemptDefense=-2, grappleBonus=2, armslengthBonus=-2, genericBonus=0,
            statBonuses=None):
        super(Knife, self).__init__(name, description, price, minDamage, maxDamage, grappleAttempt, grappleAttemptDefense, grappleBonus, armslengthBonus, genericBonus,
                statBonuses)
        self.weaponType = 'knife'

class Sword(Weapon):
    """
    Swords do 1-5 damage, and don't have any grapple-related bonuses or penalties. 
    Swords are versatile (though expensive) weapons that are typically used by 
    combatants who prefer flexibility. They are also used as a status symbol by the 
    nobility.
    """
    weaponType = 'sword'
    def __init__(self, name, description, price=0, minDamage=1, maxDamage=5, 
            grappleAttempt=0, grappleAttemptDefense=0, grappleBonus=0, 
            armslengthBonus=0, genericBonus=0, statBonuses=None):
        super(Sword, self).__init__(name, description, price, minDamage, maxDamage, 
                grappleAttempt, grappleAttemptDefense, grappleBonus,
                armslengthBonus, genericBonus, statBonuses=statBonuses)
        self.weaponType = 'sword'

class Spear(Weapon):        
    """
    Spears are almost as cheap as daggers, and do more damage than swords. They 
    also make it more difficult for an enemy to grapple you, and are very dangerous 
    at 
    armslength. However, it is very difficult to grapple when using 
    one, and it provides a serious penalty
    when you are grappled. Since the grappleDefenseBonus is only 2, a spearwielder 
    can be very vulnerable against a skilled grappler. 
    """
    weaponType = 'spear'
    def __init__(self, name, description, price=0, minDamage=1, maxDamage=5, 
            grappleAttempt=-1, grappleAttemptDefense=2, grappleBonus=-2,
            armslengthBonus=2, genericBonus=0, statBonuses=None):
        super(Spear, self).__init__(name, description, price, minDamage, maxDamage, 
                grappleAttempt, grappleAttemptDefense, grappleBonus,
                armslengthBonus, genericBonus, statBonuses=statBonuses)
        self.weaponType = 'spear'

def liftlower(armor):
    if armor.armorType == Dress.armorType or armor.armorType == Skirt.armorType or armor.armorType == Robe.armorType:
        return 'lift'
    elif armor.armorType == Pants.armorType or armor.armorType == Underwear.armorType or armor.armorType == Shorts.armorType:
        return 'lower'

def restore_liftlower(armor):
    if armor.armorType == Dress.armorType or armor.armorType == Skirt.armorType:
        return 'lower'
    elif armor.armorType == Pants.armorType or armor.armorType == Underwear.armorType:
        return 'lift'

def lowerlift(armor):
    if armor.armorType == Dress.armorType:
        return 'lift'
    elif armor.armorType == Pants.armorType or armor.armorType == Underwear.armorType or armor.armorType == Skirt.armorType or armor.armorType == Shorts.armorType:
        return 'lower'
def restore_lowerlift(armor):
    if armor.armorType == Dress.armorType:
        return 'lower'
    elif armor.armorType == Pants.armorType or armor.armorType == Underwear.armorType or armor.armorType == Skirt.armorType or armor.armorType == Shorts.armorType:
        return 'lift'

def itthem(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Shorts.armorType:
        return "them"
    else:
        return "it"

def isare(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Shorts.armorType:
        return "are"
    else:
        return "is"

def waistbandhem(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Skirt.armorType or armor.armorType == Underwear.armorType or armor.armorType == Shorts.armorType:
        return 'waistband'
    else:
        return 'hem'

def hemwaistband(armor):    
    if armor.armorType == Pants.armorType or armor.armorType == Underwear.armorType or armor.armorType == Shorts.armorType:
        return 'waistband'
    else:
        return 'hem'
    


def bottom_without_lower_clothing(person):
    if person.underwear().name == emptyUnderwear.name:
        return 'bare bottom'
    else:
        return person.underwear().name + "-clad bottom"

emptyItem = Item('empty', 'empty')
emptyWeapon = Weapon('bare hands', "I'll crush you with my bare hands! Or my magic. Whatever.", 0, 1, 1, -3, 2, -2, 0)
emptyUpperArmor = UpperArmor('shirtless', "Going for the sexy shirtless barbarian look eh? Remember, the key is to be flexing ALL THE TIME. Unless you're a woman, in which case the key is to have a two-dimensional waist and boobs so big they'd force you to walk on your hands and knees if you were a real-life person constrained by real-life physics. Fortunately, you are not.") 
emptyLowerArmor = LowerArmor('pantsless', "Real Men(TM) know that balls of steel are the only defense a man needs. Real Women(TM) know that running around pantsless is the best way to sell magazines. And books. And video games. And, well, anything really.")
emptyUnderwear = Underwear('bare bottom', "Your tush. A round, firm, glorious specimen. Go ahead and give it a slap. You know you want to.", baring=True, armorType='bare')

