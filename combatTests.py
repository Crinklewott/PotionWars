import itemspotionwars
import person
import unittest
import universal
import combatAction

class TestAttackAction(unittest.TestCase):

    def setUp(self):
        self.attacker = person.Person('attacker', person.FEMALE, None, None) 
        self.attacker.equip(itemspotionwars.familySword)
        self.attacker.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.defender = person.Person('defender', person.FEMALE, None, None) 
        self.defender.equip(itemspotionwars.familySword)
        self.defender.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.attackAction = combatAction.AttackAction(self.attacker, [self.defender])
        self.grappleAction = combatAction.GrappleAction(self.attacker, [self.defender])
        self.breakGrappleAction = combatAction.BreakGrappleAction(self.attacker, [self.defender])
        self.throwAction = combatAction.ThrowAction(self.attacker, [self.defender, self.defender])
        self.allies = [self.attacker]
        self.enemies = [self.defender]

    def set_attack_stats(self, attackerDex, defenderDex, defenderHealth):
        self.attacker.increase_stat(universal.DEXTERITY, attackerDex)
        self.defender.increase_stat(universal.DEXTERITY, defenderDex)
        self.defender.increase_stat(universal.CURRENT_HEALTH, defenderHealth)

    def attack(self):
        return self.attackAction.effect(allies=self.allies, enemies=self.enemies)[:2]

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

    def test_damage_attacker_much_higher_warfare(self):
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
        self.assertEqual(damageInflicted, 6)
        self.assertEqual(resultString, 'attacker hits defender for 6 damage!')

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
        self.attacker.grapple(self.defender, 1)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 12)

    def test_damage_grapple_sword(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familySword)
        self.attacker.grapple(self.defender, 1)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 20)

    def test_damage_grapple_dagger(self):
        self.set_attack_stats(10, 10, 30)
        self.attacker.equip(itemspotionwars.familyDagger)
        self.attacker.grapple(self.defender, 1)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 28)
        self.assertEqual(resultString, 'attacker hits defender for 28 damage!')

    def set_grapple_stats(self, attackerDex, defenderDex, defenderHealth):
        self.attacker.increase_stat(universal.STRENGTH, attackerDex)
        self.defender.increase_stat(universal.STRENGTH, defenderDex)
        self.defender.increase_stat(universal.CURRENT_HEALTH, defenderHealth)

    def grapple(self):
        return self.grappleAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def break_grapple(self):
        return self.breakGrappleAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def throw(self):
        return self.throwAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def test_grapple_equal_grapples(self):
        self.set_grapple_stats(10, 10, 40)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 0)
        self.assertEqual(resultString, 'attacker cannot grapple defender!')

    def test_grapple_slightly_higher_grapple(self):
        self.set_grapple_stats(14, 10, 40)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 8)
        self.assertEqual(resultString, 'attacker grapples defender!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertTrue(success)
        self.assertEqual(resultString, 'attacker breaks the grapple with defender!')
        self.grapple()
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 28)
        self.assertEqual(resultString, 'attacker throws defender for 28 damage!')

    def test_grapple_much_higher_grapple(self):
        self.set_grapple_stats(40, 10, 100)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 60)
        self.assertEqual(resultString, 'attacker grapples defender!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertTrue(success)
        self.assertEqual(resultString, "attacker breaks the grapple with defender!")
        self.grapple()
        self.assertEqual(self.attacker.grappleDuration, self.defender.grappleDuration)
        self.assertEqual(self.attacker.grappleDuration, 60)
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 0)
        self.assertEqual(resultString, 'attacker cannot yet throw defender!')
        self.attacker.reduce_grapple_duration(20)
        self.defender.reduce_grapple_duration(20)
        self.assertEqual(self.attacker.grapple_duration(), self.defender.grapple_duration())
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 80)
        self.assertEqual(resultString, 'attacker throws defender for 80 damage!')
        

    def test_grapple_slightly_lower_grapple(self):
        self.set_grapple_stats(10, 14, 30)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 0)
        self.assertEqual(resultString, 'attacker cannot grapple defender!')

    def test_grapple_much_lower_grapple(self):
        self.set_grapple_stats(10, 40, 30)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 0)
        self.assertEqual(resultString, 'attacker cannot grapple defender!')
        self.attacker.grapplingPartner = self.defender
        self.defender.grapplingPartner = self.attacker
        self.attacker.grappleDuration = self.defender.grappleDuration = 50
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertFalse(success)
        self.assertEqual(resultString, "attacker loosens defender's hold on her!")
        self.assertEqual(self.attacker.grappleDuration, self.defender.grappleDuration)
        self.assertEqual(self.attacker.grappleDuration, 30)
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 0)
        self.assertEqual(resultString, 'attacker cannot yet throw defender!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertFalse(success)
        self.assertEqual(resultString, "attacker loosens defender's hold on her!")
        self.assertEqual(self.attacker.grappleDuration, self.defender.grappleDuration)
        self.assertEqual(self.attacker.grappleDuration, 10)
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 20)
        self.assertEqual(resultString, 'attacker throws defender for 20 damage!')




combatSuite = unittest.TestLoader().loadTestsFromTestCase(TestAttackAction)
