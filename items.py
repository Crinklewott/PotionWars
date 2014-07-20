
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

class NakedError(Exception):
    pass

class Enchantment(universal.RPGObject):
    def __init__(self, cost=0, stat=None, bonus=0):
        self.cost = cost
        self.stat = stat
        self.bonus = bonus

    def display(self):
        return ''.join(['+', str(self.bonus), ' ', universal.stat_name(self.stat)])

class MaxEnchantmentError(Exception):
    pass

class Item(universal.RPGObject):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, 
            enchantments=None, maxEnchantment=0):
        self.name = name
        self.description = description
        self.price = price
        self.attackPenalty = attackPenalty
        self.attackDefense = attackDefense
        self.castingPenalty = castingPenalty
        self.magicDefense = magicDefense
        self.enchantments = [] if enchantments is None else enchantments
        self.maxEnchantment = maxEnchantment
        universal.state.add_item(self)


    def enchantment_level(self):
        return sum([enchantment.cost for enchantment in self.enchantments])

    def add_enchantment(self, enchantment):
        if self.enchantment_level() + max(1, 2 * enchantment.cost // 3) <= self.maxEnchantment:
            enchantment.cost = max(1, 2 * enchantment.cost // 3)
            enchantment.bonus = max(1, 2 * enchantment.bonus // 3)
            self.enchantments.append(enchantment)
        else:
            raise MaxEnchantmentError()
    def remove_enchantment(self, enchantment):
        self.enchantments.remove(enchantment)

    def _save(self):
        raise NotImplementedError()

    def is_equippable(self):
        return False

    def __eq__(self, item):
        return self.name == item.name 
    def __ne__(self, item):
        return self.name != item.name

    def apply_bonuses(self, person):
        for enchantment in self.enchantments: 
            person.increase_secondary_stat(enchantment.stat, enchantment.bonus)

    def remove_bonuses(self, person):
        for enchantment in self.enchantments: 
            person.decrease_stat(enchantment.stat, enchantment.bonus)

    def print_enchantments(self):
        if self.enchantments:
            return '\n'.join(['\t' + enchantment.display() for enchantment in self.enchantments])
        else:
            return 'None'

    @abc.abstractmethod
    def display(self):
        return '\n'.join([self.name, self.description, 'Price: ' + str(self.price), ''.join(['Enchantment Level: ', str(self.enchantment_level()), '/', 
            str(self.maxEnchantment)]), 'Enchantments:', self.print_enchantments()])
    def get_price(self):
        return self.price

    @staticmethod
    def _load(dataList):
        raise NotImplementedError()

class Armor(Item):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=6, risque=0):
        #print(' '.join([name, 'price:', str(price), 'attackDefense:', str(attackDefense)]))
        super(Armor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment)
        self.armorType = 'armor'
        self.risque = 0

    def is_equippable(self):
        return True
     
    def display(self):
        displayString = super(Armor, self).display()    
        return '\n'.join([displayString, 'attack defense: ' + str(self.attackDefense), 
            'attack penalty: ' + str(self.attackPenalty), 'casting penalty: ' + str(self.castingPenalty), 'casting defense: ' + str(self.magicDefense)])

class UpperArmor(Armor):
    armorType = 'chest armor'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=6, risque=0):
        super(UpperArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque)
        self.armorType = 'chest armor'

    def equip(self, char):
        char.unequip(char.shirt())
        char._set_shirt(self)

    def unequip(self, char, couldBeNaked=True):
        """
        couldBeNaked is here only for reasons of consistency with the other types of equipment. It doesn't influence the execution of unequip at all.
        """
        char._set_shirt(emptyUpperArmor)
        char.take_item(self)

class Shirt(UpperArmor):
    armorType = 'shirt'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0):
        super(Shirt, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque)
        self.armorType = Shirt.armorType

class FullArmor(Armor):
    armorType = 'full armor'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, enchantments=None, maxEnchantment=12, risque=0):
        super(FullArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque)
        self.armorType = 'full armor'

    def unequip(self, char, couldBeNaked=True):
        if couldBeNaked and char.underwear() == emptyUnderwear:
            raise NakedError()
        else:
            char._set_lower_clothing(emptyLowerArmor)
            char._set_shirt(emptyUpperArmor)
            char.take_item(self)

    def equip(self, char):
        char.unequip(char.lower_clothing(), False)
        char.unequip(char.shirt())
        char._set_shirt(self)
        char._set_lower_clothing(self)

class Dress(FullArmor):
    armorType = 'dress'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, enchantments=None, maxEnchantment=18, risque=0):
        super(Dress, self).__init__(name, description, attackDefense, attackPenalty, castingPenalty, magicDefense, price, enchantments, maxEnchantment, risque)
        self.armorType = 'dress'
    pass

class Robe(Dress):
    armorType = 'dress'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, enchantments=None, maxEnchantment=18, risque=0):
        super(Robe, self).__init__(name, description, attackDefense, attackPenalty, castingPenalty, magicDefense, price, enchantments, maxEnchantment, risque)
        self.armorType = 'robe'

class LowerArmor(Armor):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=6, risque=0,
            baring=False):
        super(LowerArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque)
        self.baring = False
    #def down_up

    def unequip(self, char, couldBeNaked=True):
        if couldBeNaked and char.underwear() == emptyUnderwear:
            raise NakedError()
        else:
            char._set_lower_clothing(emptyLowerArmor)
            char.take_item(self)

    def equip(self, char):
        char.unequip(char.lower_clothing(), False)
        char._set_lower_clothing(self)
   

class Pants(LowerArmor):
    armorType = 'pants'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0,
            baring=False):
        super(Pants, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque, baring)
        self.armorType = 'pants'

class Shorts(Pants):
    armorType = 'shorts'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0,
            baring=False):
        super(Shorts, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque, baring)
        self.armorType = Shorts.armorType

class Skirt(LowerArmor):
    armorType = 'skirt'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0,
            baring=False):
        super(Skirt, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque,
                baring)
        self.armorType = 'skirt'

class Underwear(Armor):
    armorType = 'underwear'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, baring=False, armorType='underwear',
            enchantments=None, maxEnchantment=9, risque=0):
        super(Underwear, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque)
        self.baring = baring
        self.armorType = armorType

    def equip(self, char):
        char.unequip(char.underwear(), False)
        char._set_underwear(self)

    def unequip(self, char, couldBeNaked=True):
        """
        If couldBeNaked is True, then the player is trying to unequip this armor. If couldBeNaked is False, then this armor is being unequipped as part of equipping
        a different piece of equipment.
        """
        if couldBeNaked and char.lower_clothing() == emptyLowerArmor:
            raise NakedError()
        else:
            char._set_underwear(emptyUnderwear)
            char.take_item(self)


class Thong(Underwear):
    armorType = 'thong'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, armorType='thong', enchantments=None, maxEnchantment=9,
            risque=3):
        super(Thong, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, True, armorType, enchantments, maxEnchantment,
                risque) 

class Weapon(Item):
    weaponType = 'weapon'   
    def __init__(self, name, description, price=0, minDamage=0, maxDamage=0, grappleAttempt=0, grappleAttemptDefense=0, grappleBonus=0, armslengthBonus=0, genericBonus=0,
            enchantments=None, maxEnchantment=4):
        super(Weapon, self).__init__(name, description, price, enchantments=enchantments, maxEnchantment=maxEnchantment)
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
            'Damage:  ' + str(self.minDamage + self.genericBonus) + ' - ' + str(self.maxDamage + self.genericBonus), 
            'grapple attempt: ' + str(self.grappleAttempt + self.genericBonus), 
            'grapple attempt defense: ' + str(self.grappleAttemptDefense + self.genericBonus), 
            'grapple bonus: ' + str(self.grappleBonus + self.genericBonus), 
            'armslength bonus: ' + str(self.armslengthBonus + self.genericBonus)])

    def unequip(self, char, couldBeNaked=True):
        """
        couldBeNaked is here only for reasons of consistency with the other types of equipment. It has no impact on the execution of this method.
        """
        char._set_weapon(emptyWeapon)
        char.take_item(self)

    def equip(self, char):
        char.unequip(char.weapon())
        char._set_weapon(self)

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
            enchantments=None, maxEnchantment=4):
        super(Knife, self).__init__(name, description, price, minDamage, maxDamage, grappleAttempt, grappleAttemptDefense, grappleBonus, armslengthBonus, genericBonus,
                enchantments, maxEnchantment)
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
            armslengthBonus=0, genericBonus=0, enchantments=None, maxEnchantment=4):
        super(Sword, self).__init__(name, description, price, minDamage, maxDamage, 
                grappleAttempt, grappleAttemptDefense, grappleBonus,
                armslengthBonus, genericBonus, enchantments=enchantments, maxEnchantment=maxEnchantment)
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
            armslengthBonus=2, genericBonus=0, enchantments=None, maxEnchantment=4):
        super(Spear, self).__init__(name, description, price, minDamage, maxDamage, 
                grappleAttempt, grappleAttemptDefense, grappleBonus,
                armslengthBonus, genericBonus, enchantments=enchantments, maxEnchantment=maxEnchantment)
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

emptyItem = Item('empty', 'empty', maxEnchantment=0)
emptyWeapon = Weapon('bare hands', "I'll crush you with my bare hands! Or my magic. Whatever.", 0, 1, 1, -3, 2, -2, 0, maxEnchantment=0)
emptyUpperArmor = UpperArmor('shirtless', "Going for the sexy shirtless barbarian look eh? Remember, the key is to be flexing ALL THE TIME. Unless you're a woman, in which case the key is to have a two-dimensional waist and boobs so big they'd force you to walk on your hands and knees if you were a real-life person constrained by real-life physics. Fortunately, you are not.", maxEnchantment=0, risque=3) 
emptyLowerArmor = LowerArmor('pantsless', "Real Men(TM) know that balls of steel are the only defense a man needs. Real Women(TM) know that running around pantsless is the best way to sell magazines. And books. And video games. And, well, anything really.", maxEnchantment=0, baring=True, risque=3)
emptyUnderwear = Underwear('bare bottom', "Your tush. A truly glorious specimen. Go ahead and give it a slap. You know you want to.", baring=True, armorType='bare',
        maxEnchantment=0, risque=999)

emptyEquipment = [emptyItem, emptyWeapon, emptyUpperArmor, emptyLowerArmor, emptyUnderwear]

