import universal

ENCHANTMENT_TYPES = {}
class Enchantment(universal.RPGObject):

    enchantmentType = "Enchantment"


    def __init__(self, cost=0):
        self.cost = cost

    @staticmethod
    def add_data(data, saveData):
        saveData.extend(["Enchantment Data:", data])

    def save(self):
        saveData = []
        Enchantment.add_data("Enchantment", saveData)
        Enchantment.add_data(str(self.cost), saveData)
        return '\n'.join(saveData)

    @staticmethod
    def load(enchantmentData, enchantment):
        data = [loadData for loadData in  enchantmentData.split("Enchantment Data") if 
                loadData.strip()]
        enchantmentType = data[0]
        assert enchantmentType in ENCHANTMENT_TYPES
        if enchantmentType != self.enchantmentType:
            ENCHANTMENT_TYPES[enchantmentType].load(data[2:], enchantment)
        enchantment.cost = int(data[1].strip())

    def display(self):
        raise NotImplementedError()

    def display_for_weapon(self):
        return self.display()

    def display_for_armor(self):
        return self.display()

ENCHANTMENT_TYPES[Enchantment.enchantmentType] = Enchantment

class StatEnchantment(Enchantment):
    """
    Applies a stat bonus to the affected stat upon equipping an item with this enchantment.
    """
    enchantmentType = "StatEnchantment"
    def __init__(self, cost, stat, bonus):
        super(StatEnchantment, self).__init__(cost)
        self.stat = stat
        self.bonus = bonus

    def apply_stat_bonus(self, target):
        if target:
            target.increase_stat(self.stat, self.bonus)

    def remove_stat_bonus(self, target):
        if target:
            target.decrease_stat(self.stat, self.bonus)


    def display(self):
        return ' '.join(["Improves the stat: ", universal.primary_stat_name(stat), "by ", 
            int(self.bonus), "points."])

    def display_for_weapon(self):
        return self.display_for_equipment()

    def display_for_armor(self):
        return self.display_for_equipment()

    def display_for_equipment(self):
        return ''.join(["+", str(self.bonus), " ", universal.primary_stat_name(self.stat)])


ENCHANTMENT_TYPES[StatEnchantment.enchantmentType] = StatEnchantment

class MaxEnchantmentError(Exception):
    pass
