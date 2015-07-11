import enchantments
import spells_PotionWars

class AttackEnchantment(enchantments.Enchantment):
    """
    Grants a +1 damage bonus to weapons, and a +1 defense bonus to clothing.
    """
    enchantmentType = "AttackEnchantment" 
    def __init__(self):
        super(AttackEnchantment, self).__init__(cost=1)
        self.bonus = 1

    def save(self):
        saveData = [super(AttackEnchantment, self).save()]
        AttackEnchantment.add_data(self.bonus, saveData)
        return '\n'.join(saveData)

    def load(enchantmentData, enchantment):
        enchantment.bonus = int(enchantmentData[0].strip())

    def damage_bonus(self):
        return self.bonus

    def display(self):
        return ("Provides a +1 bonus to damage if put on a weapon, and a +1 bonus to defense if " +
                "put on clothing.")

    def display_for_weapon(self):
        return ''.join(["+", str(self.bonus), " damage"])

    def display_for_armor(self):
        return ''.join(["+", str(self.bonus), " defense"])


enchantments.ENCHANTMENT_TYPES[AttackEnchantment.enchantmentType] = AttackEnchantment


class WeaknessEnchantment(enchantments.Enchantment):
    """
    Grants a chance of inflicting Weakness with each attack to weapons, and some number of 
    immunities from weakness on clothing.
    """
    enchantmentType = "WeaknessEnchantment"
    def __init__(self, cost, percentChance, numImmunities, duration):
        super(WeaknessEnchantment, self).__init__(cost)
        self.percentChance = percentChance
        self.numImmunities = numImmunities

    def save(self):
        saveData = [super(AttackEnchantment, self).save()]
        WeaknessEnchantment.add_data(self.percentChance, saveData)
        WeaknessEnchantment.add_data(self.numImmunities, saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(enchantmentData, enchantment):
        self.percentChance = enchantmentData[0]
        self.numImmunities = enchantmentData[1]

    def apply_offensive_enchantment(self, target):
        if random.randint(0, 100) <= self.percentChance:
            target.inflict_status(statusEffects.Weaken(self.duration))
            return ' '.join([target.printedName, 'has been inflicted with Weakness!'])
        return ''

    def apply_defensive_enchantment(self, target):
        target.add_ignored_spell(spells_PotionWars.Weaken, self.numImmunities)

    def display(self):
        return ' '.join(["Has a", int(self.percentChance), "% chance of inflicting weakness",
            "on a target if put on a weapon. Renders the wearer immune to", 
            int(self.numImmunities), "castings of Weaken per combat if put on clothing."])

    def display_for_weapon(self):
        return ''.join([str(self.percentChance), "% chance to inflict weakness."])

    def display_for_armor(self):
        return ''.join(["immunity to ", str(self.numImmunities), " castings of Weakness."])


enchantments.ENCHANTMENT_TYPES[WeaknessEnchantment.enchantmentType] = WeaknessEnchantment

def poor_weakness_ennchantment():
    """
    Returns a WeaknessEnchantment object with the stats corresponding to a very poor weakness
    enchantment.
    """
    return WeaknessEnchantment(2, 2, 1, 2)
