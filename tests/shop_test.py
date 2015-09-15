import itemspotionwars
import person
import pygame
import pygame.locals
import shopmode
import unittest
import universal

class TestPerson(person.Person):

    def __init__(self, name):
        person.Person.__init__(self, name, person.FEMALE, None, None)

class MockKeyEvent(object):

    def __init__(self, key):
        self.key = key

class TestShopMode(unittest.TestCase):

    def setUp(self):
        pygame.init()
        universal.state.party.members = []
        self.set_up_party()
        self.set_up_items()
        universal.state.testing = True
        
    def set_up_party(self):
        universal.state.party.add_member(TestPerson("Jane"))
        universal.state.party.add_member(TestPerson("Jill"))
        universal.state.party.add_member(TestPerson("Janice"))

    def set_up_items(self):
        enchantmentGem = itemspotionwars.attackGem
        jane = universal.state.get_character("Jane.person")
        jane.take_item(enchantmentGem)
        jane.take_item(itemspotionwars.familySpear)
        jane.equip(jane.get_item(1))
        jill = universal.state.get_character("Jill.person")
        jill.take_item(itemspotionwars.familySword)
        jill.equip(jill.get_item(0))
        janice = universal.state.get_character("Janice.person")
        janice.take_item(itemspotionwars.familyDagger)
        janice.equip(janice.get_item(0))

    def test_select_gem(self):
        shopmode.select_gem()
        jane = universal.state.get_character("Jane.person")
        gemList = [(jane, jane.get_item(0))]
        self.assertEqual(shopmode.gemList, gemList)

    def test_select_gem_interpreter(self):
        selectGem = MockKeyEvent(pygame.locals.K_1)
        jane = universal.state.get_character("Jane.person")
        shopmode.select_gem_interpreter(selectGem, True)
        chosenPerson, chosenGem = shopmode.chosenPersonGem
        self.assertEqual(itemspotionwars.attackGem, chosenGem)
        self.assertEqual(chosenPerson, jane)

    def test_select_equipment(self):
        shopmode.select_equipment()
        jane = universal.state.get_character("Jane.person")
        jill = universal.state.get_character("Jill.person")
        janice = universal.state.get_character("Janice.person")
        equipmentList = [(jane.name, jane.weapon()), (jill.name, jill.weapon()), 
                (janice.name, janice.weapon())]
        self.assertEqual([(person.name, equipment) for (person, equipment) in 
            shopmode.equipmentList], equipmentList)

    def test_select_equipment_interpreter(self):
        selectSpear = MockKeyEvent(pygame.locals.K_1)
        jane = universal.state.get_character("Jane.person")
        shopmode.select_equipment_interpreter(selectSpear, True)
        self.assertEqual(shopmode.chosenEquipment, jane.weapon())

    def test_enchant_equipment(self):
        universal.state.enchantmentFreebies = 0
        jane = universal.state.get_character("Jane")
        shopmode.chosenPersonGem = (jane, jane.get_item(0))
        shopmode.chosenEquipment = jane.weapon()
        self.assertEqual(shopmode.chosenPersonGem[1].enchantmentType, 
                itemspotionwars.attackGem.enchantmentType)
        self.assertEqual(shopmode.chosenEquipment.name, itemspotionwars.familySpear.name)
        shopmode.enchant_equipment()
        for person in universal.state.party:
            self.assertEqual((person.name, 10), (person.name, person.coins))
        weapon = universal.state.get_character("Jane.person").weapon()
        self.assertEqual(weapon.print_enchantments(), "\t+1 damage")
        self.assertEqual(weapon.damage_bonus(), 1)
        #Make sure we're not modifying a version of the item that should stay unaffected.
        self.assertEqual(itemspotionwars.familySpear.damage_bonus(), 0)
        self.assertEqual(itemspotionwars.familySpear.print_enchantments(), 'None')
        self.assertEqual(jane.inventory, [])


shopmodeSuite = unittest.TestLoader().loadTestsFromTestCase(TestShopMode)
        




