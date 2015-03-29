import itemspotionwars
import person
import unittest
import universal
import combatAction

class TestAttackAction(unittest.TestCase):

    def setUp(self):
        self.attacker = person.Person('attacker', person.FEMALE, None, None) 
        self.attacker.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.defender = person.Person('defender', person.FEMALE, None, None) 
        self.defender.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.action = combatAction.AttackAction(self.attacker, [self.defender])
        self.allies = [self.attacker]
        self.enemies = [self.defender]

    def set_attack_stats(self, attackerDex, defenderDex, defenderHealth):
        self.attacker.increase_stat(universal.DEXTERITY, attackerDex)
        self.defender.increase_stat(universal.DEXTERITY, defenderDex)
        self.defender.increase_stat(universal.CURRENT_HEALTH, defenderHealth)

    def attack(self):
        return self.action.effect(allies=self.allies, enemies=self.enemies)[:2]

    def test_damage_attacker_slightly_higher_warfare(self):
        self.set_attack_stats(10, 8, 30)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 28)
        self.assertEqual(resultString, 'attacker hits defender for 28 damage!')


    def test_damage_attacker_equal_warfare(self):
        self.set_attack_stats(10, 10, 30)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 20)
        self.assertEqual(resultString, 'attacker hits defender for 20 damage!')

    def test_damage_attacker_equal_much_higher_warfare(self):
        self.set_attack_stats(30, 10, 130)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 125)
        self.assertEqual(resultString, 'attacker hits defender for 125 damage!')

    def test_damage_attacker_slightly_lower_warfare(self):
        self.set_attack_stats(8, 10, 30)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 10)
        self.assertEqual(resultString, 'attacker hits defender for 10 damage!')

    def test_damage_attacker_much_much_lower_warfare(self):
        self.set_attack_stats(15, 30, 30)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 1)
        self.assertEqual(resultString, 'attacker hits defender for 1 damage!')

    def test_damage_attacker_much_lower_warfare(self):
        self.set_attack_stats(22, 30, 30)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 11)
        self.assertEqual(resultString, 'attacker hits defender for 11 damage!')

    def test_damage_spear(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familySpear)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 28)
        self.assertEqual(resultString, 'attacker hits defender for 28 damage!')

    def test_damage_sword(self):
        #self.set_attack_stats(10, 10, 30)
        self.attacker.set_all_stats(2, 2, 2, 2, 2, 2, 2)
        self.defender.set_all_stats(strength=1, dexterity=2, willpower=0, talent=0, health=12, mana=0, alertness=1)
        self.attacker.equip(itemspotionwars.familySword)
        self.defender.equip(itemspotionwars.familySpear)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 7)
        self.assertEqual(resultString, 'attacker hits defender for 7 damage!')

    def test_damage_knife(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familyDagger)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 12)
        self.assertEqual(resultString, 'attacker hits defender for 12 damage!')

    def test_damage_grapple_spear(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familySpear)
        self.attacker.grapple(self.defender)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 12)

    def test_damage_grapple_sword(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familySword)
        self.attacker.grapple(self.defender)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 20)

    def test_damage_grapple_dagger(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familyDagger)
        self.attacker.grapple(self.defender)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 28)
        self.assertEqual(resultString, 'attacker hits defender for 28 damage!')


combatSuite = unittest.TestLoader().loadTestsFromTestCase(TestAttackAction)
