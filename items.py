
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
from __future__ import division
import universal
from universal import *
import abc
import random

allItems = {}

LOOSE = 'loose'
TIGHT = 'tight'

class NakedError(Exception):
    pass



class Enchantment(universal.RPGObject):
    def __init__(self, cost=0, stat=None, bonus=0):
        self.cost = cost
        self.stat = stat
        self.bonus = bonus

    def apply_enchantment(self):
        raise NotImplementedError()

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Enchantment Data:", data])

    def save(self):
        saveData = []
        Enchantment.add_data(str(self.cost), saveData)
        Enchantment.add_data(str(self.stat), saveData)
        Enchantment.add_data(str(self.bonus), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(enchantmentData, enchantment):
        _, cost, stat, bonus = enchantmentData.split("Enchantment Data:")
        enchantment.cost = int(cost.strip())
        enchantment.stat = int(stat.strip()) 
        enchantment.bonus = int(bonus.strip())


    def display(self):
        raise NotImplementedError()

class AttackEnchantment(Enchantment):
    """
    Grants a +1 damage bonus to weapons, and a +1 defense bonus to clothing.
    """
    def __init__(self):
        super(AttackEnchantment, self).__init__(cost=1, bonus=1)

    def apply_enchantment(self):
        return self.bonus

    def display(self):
        return ''.join(['+', str(self.bonus), ' damage'])

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

    def __eq__(self, item):
        return self.name == item.name
    
    def __neq__(self, item):
        return self.name != item.name

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Item Data:", data])

    def save(self):
        saveData = []
        Item.add_data(self.name, saveData)
        Item.add_data(self.description, saveData)
        Item.add_data(str(self.attackPenalty), saveData)
        Item.add_data(str(self.attackDefense), saveData)
        Item.add_data(str(self.castingPenalty), saveData)
        Item.add_data(str(self.magicDefense), saveData)
        Item.add_data('\n'.join(enchantment.save() for enchantment in self.enchantments), saveData)
        Item.add_data(str(self.maxEnchantment), saveData) 
        return '\n'.join(saveData)

    @staticmethod
    def load(itemData, item):
        rest = []
        try:
            _, name, description, attackPenalty, attackDefense, castingPenalty, magicDefense, enchantments, maxEnchantment, rest = itemData.split("Item Data:")
        except ValueError:
            _, name, description, attackPenalty, attackDefense, castingPenalty, magicDefense, enchantments, maxEnchantment = itemData.split("Item Data:")
        item.name = name.strip()
        item.description = description.replace('\n', ' ').strip()
        item.attackPenalty = int(attackPenalty.strip())
        item.attackDefense = int(attackDefense.strip())
        item.castingPenalty = int(castingPenalty.strip())
        item.magicDefense = int(magicDefense.strip())
        if enchantments.strip():
            enchantments = enchantments.split("Enchantment:")
            item.enchantments = [Enchantment() for enchantment in enchantments]
            for enchantment, enchantmentData in zip(item.enchantments, enchantments):
                Enchantment.load(enchantmentData, enchantment)
        #&&& Need to handle the loading of subclasses.
        if rest:
            if "Armor Only:" in rest:
                Armor.load(rest, item)
            elif "Weapon Only:" in rest:
                Weapon.load(rest, item)



    def enchantment_level(self):
        return sum([enchantment.cost for enchantment in self.enchantments])

    def add_enchantment(self, enchantment):
        if self.enchantment_level() + max(1, 2 * enchantment.cost // 3) <= self.maxEnchantment:
            enchantment.cost = enchantment.cost #max(1, 2 * enchantment.cost // 3)
            enchantment.bonus = enchantment.bonus #max(1, 2 * enchantment.bonus // 3)
            self.enchantments.append(enchantment)
        else:
            raise MaxEnchantmentError()
    def remove_enchantment(self, enchantment):
        self.enchantments.remove(enchantment)

    def defense_bonus(self):
        return 0

    def _save(self):
        raise NotImplementedError()

    def is_equippable(self):
        return False

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

allGems = {}
class Gem(Item):
    """
    Special gems used to imbue weapons and clothing with enchantments.
    """
    def __init__(self, name, description, enchantmentType):
        """
        name - name of the Gem
        description - Gem's description in text
        enchantmentType - The Enchantment class associated with this gem. This should be the 
        enchantment that the gem imbues the desired weapon or clothing with. 
        """
        super(Gem, self).__init__(name, description)
        self.enchantmentType = enchantmentType
        self.cost = enchantmentType().cost
        self.bonus = enchantmentType().bonus

    '''
    def save(self):
        saveData = []
        Gem.add_data(str(self.name), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Gem Data:", data])

    @staticmethod
    def load(saveData, gem):
        """
        Because enchantment gems can't be changed by the player, and we always start with a copy of the object, whose state is then updated to match the state in the savefile, nothing fancy needs to happen when loading gems.
        """
        pass
    '''


class Armor(Item):
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=6, risque=0):
        super(Armor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment)
        self.armorType = 'armor'
        self.risque = risque

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Armor Data:", data])

    def save(self):
        saveData = [super(Armor, self).save(), "Item Data:", "Armor Only:"]
        Armor.add_data(str(self.risque), saveData)
        return '\n'.join(saveData)

    def defense_bonus(self):
        enchantmentBonus = 0
        for enchantment in self.enchantments:
            try:
                enchantmentEffect = enchantment.apply_enchantment()
            except NotImplementedError:
                continue
            else:
                if enchantmentEffect:
                    enchantmentBonus += enchantmentEffect
        return enchantmentBonus

    def liftlower(self):
        return "lower"

    def updown(self):
        return "up"

    def restore_liftlower(self):
        return "lift"

    def lowerlift(self):
        return "lift"

    def restore_lowerlift(self):
        return "lower"


    def liftslowers(self):
        return self.liftlower() + "s"

    def lowerslifts(self):
        return self.lowerlift() + "s"

    def waistband_hem(self):
        return "waistband"

    def hem_waistband(self):
        return self.waistband_hem()

    @staticmethod
    def load(armorData, armor):
        rest = ""
        try:
            _, risque, rest = armorData.split("Armor Data:")
        except ValueError:
            _, risque = armorData.split("Armor Data:")
        #armor.risque = int(risque.strip())
        if rest and "Lower Only:" in rest:
            LowerArmor.load(rest, armor)

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
        self.armorType = UpperArmor.armorType

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
        self.baring = False

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
    tightness = 'loose'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, enchantments=None, maxEnchantment=18, risque=0, tightness=None):
        super(Dress, self).__init__(name, description, attackDefense, attackPenalty, castingPenalty, magicDefense, price, enchantments, maxEnchantment, risque)
        self.armorType = 'dress'
        if tightness:
            self.tightness = tightness
        else:
            self.tightness = Dress.tightness

    def waistband_hem(self):
        return "hem"

    def liftlower(self):
        return "lift"

    def updown(self):
        return "down"

    def restore_liftlower(self):
        return "lower"

class Robe(Dress):
    armorType = 'dress'
    def __init__(self, name, description, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, price=0, enchantments=None, maxEnchantment=18, risque=0):
        super(Robe, self).__init__(name, description, attackDefense, attackPenalty, castingPenalty, magicDefense, price, enchantments, maxEnchantment, risque)
        self.armorType = 'robe'

class LowerArmor(Armor):
    armorType = "Lower Armor"
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=6, risque=0,
            baring=False):
        super(LowerArmor, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque)
        self.baring = baring

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Lower Data:", data])

    def save(self):
        saveData = [super(LowerArmor, self).save(), "Armor Data:", "Lower Only:", "Lower Data:"]
        LowerArmor.add_data(str(self.baring), saveData)
        return '\n'.join(saveData)


    @staticmethod
    def load(armorData, armor):
        _, lowerOnly, baring = armorData.split("Lower Data:")
        armor.baring = baring.strip() == "True"
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
    tightness = 'loose'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0,
            baring=False, tightness=None):
        super(Pants, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque, baring)
        self.armorType = 'pants'
        tightness = tightness if tightness else Pants.tightness

class Shorts(Pants):
    armorType = 'shorts'
    tightness = 'tight'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0,
            baring=False, tightness=None):
        super(Shorts, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque, baring)
        self.armorType = Shorts.armorType
        self.tightness = tightness if tightness else Shorts.tightness

class Skirt(LowerArmor):
    armorType = 'skirt'
    tightness = 'loose'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, enchantments=None, maxEnchantment=9, risque=0,
            baring=False, tightness=None):
        super(Skirt, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, enchantments, maxEnchantment, risque,
                baring)
        self.armorType = 'skirt'
        self.tightness = tightness if tightness else Skirt.tightness

    def waistband_hem(self):
        return "waistband"


    def hem_waistband(self):
        return "hem"

    def liftlower(self):
        return "lift"

    def updown(self):
        return "down"

    def restore_liftlower(self):
        return "lower"

    def lowerlift(self):
        return "lower"

    def downup(self):
        return "up"

    def restore_lowerlift(self):
        return "lift"


class Underwear(Armor):
    armorType = 'underwear'
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, baring=False, armorType='underwear',
            enchantments=None, maxEnchantment=9, risque=3):
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
    def __init__(self, name, description, price=0, attackDefense=0, attackPenalty=0, castingPenalty=0, magicDefense=0, armorType='underwear', enchantments=None, maxEnchantment=9,
            risque=5):
        super(Thong, self).__init__(name, description, price, attackDefense, attackPenalty, castingPenalty, magicDefense, True, armorType, enchantments, maxEnchantment,
                risque) 
        self.armorType = armorType

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

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Weapon Data:", data])

    def save(self):
        saveData = [super(Weapon, self).save(), "Item Data:", 'Weapon Only:']
        Weapon.add_data(str(self.minDamage), saveData)
        Weapon.add_data(str(self.maxDamage), saveData)
        Weapon.add_data(str(self.grappleAttempt), saveData)
        Weapon.add_data(str(self.grappleAttemptDefense), saveData)
        Weapon.add_data(str(self.grappleBonus), saveData)
        Weapon.add_data(str(self.armslengthBonus), saveData)
        Weapon.add_data(str(self.genericBonus), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(weaponData, weapon):
        _, minDamage, maxDamage, grappleAttempt, grappleAttemptDefense, grappleBonus, armslengthBonus, genericBonus = weaponData.split("Weapon Data:")
        weapon.minDamage = int(minDamage.strip())
        weapon.maxDamage = int(maxDamage.strip())
        weapon.grappleAttempt = int(grappleAttempt.strip())
        weapon.grappleAttemptDefense = int(grappleAttemptDefense.strip())
        weapon.grappleBonus = int(grappleBonus.strip())
        weapon.armslengthBonus = int(armslengthBonus.strip())
        weapon.genericBonus = int(genericBonus.strip())

    def is_equippable(self):
        return True

    def display(self):
        displayString = super(Weapon, self).display()
        return '\n'.join([displayString, 
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

    def armslength_bonus(self):
        return self.armslengthBonus + self.genericBonus

    def attack_bonus(self, grappling):
        return (self.grappleBonus if grappling else self.armslengthBonus) + self.genericBonus

    def parry_bonus(self, grappling):
        """
            For now, this function returns the same thing as attack_bonus. They are split both to enhance readability, and because we may decide to modify this in the 
            future.
        """
        return self.attack_bonus(grappling)

    def damage_multiplier(self, grappling):
        return ((self.grappleBonus if grappling else self.armslengthBonus) + self.genericBonus) / 10

    def damage_bonus(self):
        enchantmentBonus = 0
        for enchantment in self.enchantments:
            try:
                enchantmentEffect = enchantment.apply_enchantment()
            except NotImplementedError:
                continue
            else:
                if enchantmentEffect:
                    enchantmentBonus += enchantmentEffect
        return enchantmentBonus




PENALTY = -2
BONUS = 2
class Knife(Weapon):
    """
    Knives are exceptionally dangerous in close quarters, but all but useless if a 
    combatant is forced to keep their distance.
    """
    weaponType = 'knife'
    def __init__(self, name, description, price=0, minDamage=1, maxDamage=5, grappleAttempt=BONUS, grappleAttemptDefense=PENALTY, grappleBonus=BONUS, armslengthBonus=PENALTY, genericBonus=0,
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
            grappleAttempt=PENALTY, grappleAttemptDefense=BONUS, grappleBonus=PENALTY,
            armslengthBonus=BONUS, genericBonus=0, enchantments=None, maxEnchantment=4):
        super(Spear, self).__init__(name, description, price, minDamage, maxDamage, 
                grappleAttempt, grappleAttemptDefense, grappleBonus,
                armslengthBonus, genericBonus, enchantments=enchantments, maxEnchantment=maxEnchantment)
        self.weaponType = 'spear'


#----------------------------------------------------Pajamas---------------------------------------

class Pajamas(Item):
    armorType = 'pajamas'
    def __init__(self, name, description, price, risque=0):
        super(Pajamas, self).__init__(name, description, price)
        self.armorType = Pajamas.armorType
        self.risque = risque

    def is_equippable(self):
        return True

class FullPajamas(Pajamas):
    armorType = 'full pajamas'
    def __init__(self, name, description, price):
        super(FullPajamas, self).__init__(name, description, price)
        self.armorType = FullPajamas.armorType

    def unequip(self, char, couldBeNaked=True):
        if couldBeNaked:
            raise NakedError()
        else:
            char._set_pajama_bottom(emptyLowerArmor)
            char._set_pajama_top(emptyUpperArmor)
            char.take_item(self)

    def equip(self, char):
        char.unequip(char.pajama_bottom(), False)
        char.unequip(char.pajama_top())
        char._set_pajama_top(self)
        char._set_pajama_bottom(self)

class PajamaTop(Pajamas):
    armorType = 'pajama top'
    def __init__(self, name, description, price):
        super(PajamaTop, self).__init__(name, description, price)
        self.armorType = PajamaTop.armorType

    def equip(self, char):
        char.unequip(char.pajama_top())
        char._set_pajama_top(self)

    def unequip(self, char, couldBeNaked=True):
        """
        couldBeNaked is here only for reasons of consistency with the other types of equipment. It doesn't influence the execution of unequip at all.
        """
        char._set_pajama_top(emptyPajamaTop)
        char.take_item(self)


class DropSeatPajamas(FullPajamas):
    armorType = 'dropseat pajamas'
    
    def __init__(self, name, description, price):
        super(DropSeatPajamas, self).__init__(name, description, price)
        self.armorType = DropSeatPajamas.armorType

    def waistband_hem(self):
        return "drop seat"

    def liftlower(self):
        return "lower"

class PajamaBottom(Pajamas):
    armorType = 'pajama bottom'
    def __init__(self, name, description, price):
        super(PajamaBottom, self).__init__(name, description, price)
        self.armorType = PajamaBottom.armorType

    def unequip(self, char, couldBeNaked=True):
        if couldBeNaked:
            raise NakedError()
        else:
            char._set_pajama_bottom(emptyPajamaBottom)
            char.take_item(self)

    def equip(self, char):
        char.unequip(char.pajama_bottom(), False)
        char._set_pajama_bottom(self)

    def waistband_hem(self):
        return "hem"

    def liftlower(self):
        return "lift"
    
class PajamaPants(PajamaBottom):
    armorType = 'pajama pants'
    def __init__(self, name, description, price):
        super(PajamaPants, self).__init__(name, description, price)
        self.armorType = PajamaPants.armorType

    def liftlower(self):
        return "lower"

    def waistband_hem(self):
        return "waistband"

def liftlower(armor):
    return armor.liftlower()

def liftslowers(armor):
    return liftlower(armor) + "s"


def restore_liftlower(armor):
    return armor.restore_liftlower()

def restore_liftslowers(armor):
    return restore_liftlower(armor) + "s"

def lowerlift(armor):
    return armor.lowerlift()

def lowerslifts(armor):
    return lowerlift(armor) + "s"

def restore_lowerlift(armor):
    return armor.restore_lowerlift()

def restore_lowerslifts(armor):
    return restore_lowerlift(armor) + "s"

def itthem(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Shorts.armorType:
        return "them"
    else:
        return "it"

def itthey(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Shorts.armorType:
        return "they"
    else:
        return "it"

def isare(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Shorts.armorType:
        return "are"
    else:
        return "is"

def waistbandhem(armor):
    if armor.armorType == Pants.armorType or armor.armorType == Skirt.armorType or armor.armorType == Underwear.armorType or armor.armorType == Shorts.armorType or armor.armorType == Thong.armorType:
        return 'waistband'
    else:
        return 'hem'

def hemwaistband(armor):    
    if armor.armorType == Pants.armorType or armor.armorType == Underwear.armorType or armor.armorType == Thong.armorType or armor.armorType == Shorts.armorType:
        return 'waistband'
    else:
        return 'hem'
    


def bottom_without_lower_clothing(person):
    if person.underwear().name == emptyUnderwear.name:
        return 'bare bottom'
    else:
        return person.underwear().name + "-clad bottom"

emptyItem = Item('empty', 'empty', maxEnchantment=0)
emptyWeapon = Weapon('bare hands', "I'll crush you with my bare hands! Or my magic. Whatever.", 0, 0, 0, PENALTY, PENALTY, PENALTY, PENALTY, maxEnchantment=0)
emptyUpperArmor = UpperArmor('shirtless', "Going for the sexy shirtless barbarian look eh? Remember, the key is to be flexing ALL THE TIME. Unless you're a woman, in which case the key is to have a two-dimensional waist and boobs so big they'd force you to walk on your hands and knees if you were a real-life person constrained by real-life physics. Fortunately, you are not.", maxEnchantment=0, risque=3) 
emptyLowerArmor = LowerArmor('pantsless', "Real Men(TM) know that balls of steel are the only defense a man needs. Real Women(TM) know that running around pantsless is the best way to sell magazines. And books. And video games. And, well, anything really.", maxEnchantment=0, baring=True, risque=3)
assert emptyLowerArmor.baring
emptyUnderwear = Underwear('bare bottom', "Your tush. A truly glorious specimen. Go ahead and give it a slap. You know you want to.", baring=True, armorType='bare',
        maxEnchantment=0, risque=999)

emptyPajamaTop = PajamaTop('Topless', 'Who needs to sleep with a top on?', 0)

emptyPajamaBottom = PajamaBottom('Bottomless', 'Who needs to sleep with a bottom on?', 0)

emptyEquipment = [emptyItem, emptyWeapon, emptyUpperArmor, emptyLowerArmor, emptyUnderwear, emptyPajamaTop, emptyPajamaBottom]

#The purpose of the following functions is to simplify the latex translation for when trying to get the equipment of arbitrary characters.
def weapon(personName):
    return universal.state.get_character(personName).weapon()

def underwear(personName):
    return universal.state.get_character(personName).underwear()

def underwear_name(personName):
    return universal.state.get_character(personName).underwear().name

def lower_clothing(personName):
    return universal.state.get_character(personName).lower_clothing()

def upper_clothing(personName):
    return universal.state.get_character(personName).upper_clothing()

def pajama_top(personName):
    return universal.state.get_character(personName).pajama_top()

def pajama_bottom(personName):
    return universal.state.get_character(personName).pajama_bottom()

def weapon_name(personName):
    return universal.state.get_character(personName).weapon().name

def lower_clothing_name(personName):
    return universal.state.get_character(personName).lower_clothing().name

def upper_clothing_name(personName):
    return universal.state.get_character(personName).upper_clothing().name

def pajama_top_name(personName):
    return universal.state.get_character(personName).pajama_top().name

def pajama_bottom_name(personName):
    return universal.state.get_character(personName).pajama_bottom().name

def clad_bottom(personName):
    return universal.state.get_character(personName).clad_bottom()

def clad_pajama_bottom(personName):
    return universal.state.get_character(personName).clad_bottom(pajama=True)

def is_lower_clothing(item):
    try:
        return (item.armorType == Pants.armorType or item.armorType == Skirt.armorType or item.armorType == Shorts.armorType or item.armorType == Dress.armorType or 
            item.armorType == LowerArmor.armorType or item.armorType == FullArmor.armorType or item.armorType == Underwear.armorType)
    except AttributeError:
        return False

def waistband_hem(lowerClothing):
    return lowerClothing.waistband_hem()

def dropseat_based_msg(person, dropseatMsg, loweredMsg, liftedMsg):
    return universal.msg_selector(person.pajama_bottoms().armorType == DropSeatPajamas.armorType, {True:dropseatMsg, False:pjliftedlowered_based_msg(person, liftedMsg, loweredMsg)})

def liftedlowered_based_msg(person, liftedMsg, loweredMsg):
    return universal.msg_selector(person.lower_clothing().liftlower() == "lift", {True:liftedMsg, False:loweredMsg})

def loweredlifted_based_msg(person, loweredMsg, liftedMsg):
    return universal.msg_selector(person.lower_clothing().lowerlift() == "lower", {True:loweredMsg, False:liftedMsg})

def pjliftedlowered_based_msg(person, liftedMsg, loweredMsg):
    return universal.msg_selector(person.pajama_bottoms().liftlower() == "lift", {True:liftedMsg, False:loweredMsg})

def pjloweredlifted_based_msg(person, loweredMsg, liftedMsg):
    return universal.msg_selector(person.pajama_bottoms().lowerlift() == "lower", {True:loweredMsg, False:liftedMsg})

def pajama_type_msg(person, dropSeatMsg, pantsMsg, dressMsg):
    if person.pajama_bottoms().armorType == DropSeatPajamas.armorType:
        return dropSeatMsg
    elif person.pajama_bottoms().armorType == PajamaPants.armorType:
        return pantsMsg
    else:
        return dressMsg

def is_tight(clothing):
    try:
        return clothing.tightness == 'tight'
    except AttributeError:
        return False

def tight_msg(clothing, tightMsg, looseMsg):
    return universal.msg_selector(clothing.tightness == TIGHT, {True:tightMsg, False:looseMsg})

def is_loose(clothing):
    try:
        return clothing.tightness == 'loose'
    except AttributeError:
        return False

def loose_msg(person, looseMsg, tightMsg):
    return universal.msg_selector(person.lower_clothing().tightness == LOOSE, {True:looseMsg, False:tightMsg})

def wearing_trousers(person, wearingTrousers, notWearingTrousers='', noLowerClothing=''):
    if person.lower_clothing() == emptyLowerArmor:
        return noLowerClothing
    return universal.msg_selector(person.wearing_pants_or_shorts() or person.lower_clothing().armorType == Skirt.armorType, {True:wearingTrousers, False:notWearingTrousers})

def wearing_shirt(person, wearingShirt, notWearingShirt='', noLowerClothing=''):
    if person.shirt() == emptyUpperArmor:
        return noLowerClothing
    return universal.msg_selector(person.shirt() != emptyUpperArmor, {True:wearingShirt, False:notWearingShirt})

def wearing_underwear(person, wearingUnderwear, notWearingUnderwear=''):
    return universal.msg_selector(person.underwear() != emptyUnderwear, {True:wearingUnderwear, False:notWearingUnderwear})

def wearing_dress(person, wearingDress, notWearingDress='', noOuterClothing=''):
    if person.shirt() == emptyUpperArmor and person.lower_clothing() == emptyLowerArmor:
        return noOuterClothing
    else:
        return universal.msg_selector(person.lower_clothing().armorType == Skirt.armorType or person.lower_clothing().armorType == Dress.armorType, {True:wearingDress, False:notWearingDress})

def baring_underwear(underwear, baringMsg, notBaringMsg, notWearingUnderwearMsg=''):
    return notWearingUnderwearMsg if underwear == emptyUnderwear else universal.msg_selector(underwear.baring, {True:baringMsg, False:notBaringMsg})

def shirt_name(character):
    return character.shirt().name

def is_empty_item(item):
    return (item.name == emptyUnderwear.name or  item.name == emptyLowerArmor.name or 
            item.name == emptyUpperArmor.name or item.name == emptyWeapon.name)

def is_pajamas(item):
    try:
        return 'pajama' in item.armorType
    except AttributeError:
        return False

