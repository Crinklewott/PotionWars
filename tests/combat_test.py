import combatAction
import itemspotionwars
import person
import positions
import pwenemies
import spells_PotionWars
import statusEffects
import unittest
import universal

class TestPerson(pwenemies.Enemy):

    def __init__(self, name):
        super(TestPerson, self).__init__(name, person.FEMALE, None, None)
        self.printedName = name

    def spank_text(self, top, bottom, position_name):
        return ' '.join([top.name, 'spanks', bottom.name, position_name + "!"])

    def round_text(self, top, bottom, position_name):
        return ' '.join([top.name, 'continues spanking', bottom.name, position_name + "!"])

    def reversal_text(self, top, bottom, position_name):
        return ' '.join([bottom.name, 'reverses', top.name, position_name + "!"])

    def otk_intro(self, top, bottom):
        return self.spank_text(top, bottom, 'otk')

    def otk_round(self, top, bottom):
        return self.round_text(top, bottom, 'otk')

    def otk_reversal(self, top, bottom):
        return self.reversal_text(top, bottom, 'otk')

    def standing_intro(self, top, bottom):
        return self.spank_text(top, bottom, 'standing')

    def standing_round(self, top, bottom):
        return self.round_text(top, bottom, 'standing')

    def standing_reversal(self, top, bottom):
        return self.reversal_text(top, bottom, 'standing')

    def on_the_ground_intro(self, top, bottom):
        return self.spank_text(top, bottom, 'on the ground')

    def on_the_ground_round(self, top, bottom):
        return self.round_text(top, bottom, 'on the ground')

    def on_the_ground_reversal(self, top, bottom):
        return self.reversal_text(top, bottom, 'on the ground')

class TestCombatActions(unittest.TestCase):
    """
    Note that the spanking text is tested under enemy tests. Basically it just grabs the text and prints it out to make sure that any typos or crashes are caught.

    The spanking tests here test to make sure the action works like it's supposed to.
    """

    def setUp(self):
        self.set_up_actors()
        self.set_up_actions()
        self.set_up_spells()

    def set_up_actors(self):
        self.attacker = TestPerson('attacker') 
        self.attacker.equip(itemspotionwars.familySword)
        self.attacker.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.defender = TestPerson('defender') 
        self.defender.equip(itemspotionwars.familySword)
        self.defender.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.guardian = TestPerson('guardian')
        self.guardian.set_all_stats(0, 0, 0, 0, 0, 0, 0)
        self.guardian.equip(itemspotionwars.familySword)

    def set_up_actions(self):
        self.attackAction = combatAction.AttackAction(self.attacker, [self.defender])
        self.grappleAction = combatAction.GrappleAction(self.attacker, [self.defender])
        self.breakGrappleAction = combatAction.BreakGrappleAction(self.attacker, [self.defender])
        self.defendAction = combatAction.DefendAction(self.guardian, [self.defender])
        self.defendActionSelf = combatAction.DefendAction(self.defender, [self.defender])
        self.throwActionAtGuardian = combatAction.ThrowAction(self.attacker, [self.defender, self.guardian])
        self.throwAction = combatAction.ThrowAction(self.attacker, [self.defender, self.defender])
        self.allies = [self.attacker]
        self.enemies = [self.defender, self.guardian]
        self.otk = combatAction.SpankAction(self.attacker, [self.defender], positions.overTheKnee)
        self.standing = combatAction.SpankAction(self.attacker, [self.defender], positions.standing)
        self.onTheGround = combatAction.SpankAction(self.attacker, [self.defender], positions.onTheGround)

    def set_up_spells(self):
        self.firebolt = spells_PotionWars.Firebolt(self.attacker, [self.defender])

    def set_attack_stats(self, attackerDex, defenderDex, defenderHealth):
        self.attacker.increase_stat(universal.DEXTERITY, attackerDex)
        self.defender.increase_stat(universal.DEXTERITY, defenderDex)
        self.defender.increase_stat(universal.CURRENT_HEALTH, defenderHealth)
        self.guardian.increase_stat(universal.DEXTERITY, defenderDex)
        self.guardian.increase_stat(universal.CURRENT_HEALTH, defenderHealth)

    def attack(self):
        return self.attackAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def defend(self):
        return self.defendAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def defend_self(self):
        return self.defendActionSelf.effect(allies=self.allies, enemies=self.enemies)[:2]

#--------------------Defend----------------------------------

    def test_defend(self):
        self.set_attack_stats(10, 8, 30)
        resultString, _ = self.defend()
        self.assertEqual(len(self.defender.guardians), 1)
        self.assertEqual(self.defender.guardians[0], self.guardian)
        self.assertEqual(resultString, 'guardian defends defender!')
        self.assertEqual(8, self.defender.dexterity())
        self.assertEqual(0, self.defender.strength())
        self.assertEqual(0, self.defender.willpower())
        self.assertEqual(0, self.defender.talent())
        self.assertEqual(8, self.guardian.dexterity())
        self.assertEqual(0, self.guardian.strength())
        self.assertEqual(0, self.guardian.willpower())
        self.assertEqual(0, self.guardian.talent())

    def test_defend_self(self):
        self.set_attack_stats(10, 8, 30)
        resultString, _ = self.defend_self()
        self.assertEqual(len(self.defender.guardians), 0)
        self.assertEqual(resultString, 'defender defends herself!')
        self.assertEqual(len(self.defender.guardians), 0)
        self.assertEqual(10, self.defender.dexterity())
        self.assertEqual(2, self.defender.strength())
        self.assertEqual(2, self.defender.willpower())
        self.assertEqual(2, self.defender.talent())

#--------------------Attack----------------------------------

    def test_damage_attacker_slightly_higher_warfare(self):
        self.set_attack_stats(10, 8, 30)
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 28)
        self.assertEqual(resultString, 'attacker hits defender for 28 damage!')

    def test_attack_guardian(self):
        self.set_attack_stats(10, 8, 30)
        self.defend()
        resultString, damageInflicted = self.attack()
        damageInflicted = damageInflicted[0]
        self.assertEqual(damageInflicted, 28)
        self.assertEqual(resultString, 'guardian defends defender from attacker!\nattacker hits guardian for 28 damage!')

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

#--------------------Grapple----------------------------------
    def set_grapple_stats(self, attackerStr, defenderStr, defenderHealth):
        self.attacker.increase_stat(universal.STRENGTH, attackerStr)
        self.defender.increase_stat(universal.STRENGTH, defenderStr)
        self.defender.increase_stat(universal.CURRENT_HEALTH, defenderHealth)
        self.guardian.increase_stat(universal.STRENGTH, defenderStr)
        self.guardian.increase_stat(universal.CURRENT_HEALTH, defenderHealth)

    def set_equal_grapple_stats(self):
        self.set_grapple_stats(10, 10, 40)

    def set_slightly_greater_grapple_stats(self):
        self.set_grapple_stats(14, 10, 40)

    def set_slightly_lower_grapple_stats(self):
        self.set_grapple_stats(10, 14, 40)

    def set_much_greater_grapple_stats(self):
        self.set_grapple_stats(40, 10, 40)

    def set_much_lower_grapple_stats(self):
        self.set_grapple_stats(10, 40, 40)

    def grapple(self):
        return self.grappleAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def break_grapple(self):
        return self.breakGrappleAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def throw(self):
        return self.throwAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def throw_at_guardian(self):
        return self.throwActionAtGuardian.effect(allies=self.allies, enemies=self.enemies)[:2]

    def test_grapple_equal_grapples(self):
        self.set_grapple_stats(10, 10, 40)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 20)
        self.assertEqual(resultString, 'attacker grapples defender!')


    def grapple(self):
        return self.grappleAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def break_grapple(self):
        return self.breakGrappleAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def throw(self):
        return self.throwAction.effect(allies=self.allies, enemies=self.enemies)[:2]

    def throw_at_guardian(self):
        return self.throwActionAtGuardian.effect(allies=self.allies, enemies=self.enemies)[:2]

    def test_grapple_equal_grapples(self):
        self.set_grapple_stats(10, 10, 40)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 20)
        self.assertEqual(resultString, 'attacker grapples defender!')

    def test_grapple_guardian(self):
        self.set_grapple_stats(14, 10, 40)
        self.defend()
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 45)
        self.assertEqual(resultString, 'guardian defends defender from attacker!\nattacker grapples guardian!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertFalse(success)
        self.assertEqual(resultString, "attacker loosens guardian's hold on her!")
        self.grappleAction.defenders = [self.defender]
        self.break_grapple()
        self.break_grapple()
        resultString, success = self.break_grapple()
        sucess = success[0]
        self.assertTrue(success)
        self.assertEqual(resultString, "attacker breaks the grapple with guardian!")

    def test_grapple_slightly_higher_grapple(self):
        self.set_grapple_stats(14, 10, 40)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 45)
        self.assertEqual(resultString, 'attacker grapples defender!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertFalse(success)
        self.assertEqual(resultString, "attacker loosens defender's hold on her!")
        self.break_grapple()
        self.break_grapple()
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 28)
        self.assertEqual(resultString, 'attacker throws defender for 28 damage!')

    def test_grapple_much_higher_grapple(self):
        self.set_grapple_stats(40, 10, 100)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 175)
        self.assertEqual(resultString, 'attacker grapples defender!')
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 0)
        self.assertEqual(resultString, 'attacker cannot yet throw defender!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertFalse(success)
        self.assertEqual(self.attacker.grapple_duration(), 135)
        self.assertEqual(self.defender.grapple_duration(), self.attacker.grapple_duration())
        self.assertEqual(resultString, "attacker loosens defender's hold on her!")
        self.assertEqual(self.attacker.grapple_duration(), self.defender.grapple_duration())
        self.break_grapple()
        self.break_grapple()
        self.break_grapple()
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(resultString, 'attacker throws defender for 80 damage!')
        self.assertEqual(damage, 80)
        
    def test_grapple_slightly_lower_grapple(self):
        self.set_grapple_stats(10, 14, 30)
        resultString, grappleDuration = self.grapple()
        grappleDuration = grappleDuration[0]
        self.assertEqual(grappleDuration, 7)
        self.assertEqual(resultString, 'attacker grapples defender!')

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
        self.assertEqual(self.attacker.grappleDuration, 40)
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 0)
        self.assertEqual(resultString, 'attacker cannot yet throw defender!')
        resultString, success = self.break_grapple()
        success = success[0]
        self.assertFalse(success)
        self.assertEqual(resultString, "attacker loosens defender's hold on her!")
        self.assertEqual(self.attacker.grappleDuration, self.defender.grappleDuration)
        self.assertEqual(self.attacker.grappleDuration, 30)
        self.attacker.grappleDuration = 8
        self.defender.grappleDuration = 8
        resultString, damage = self.throw()
        damage = damage[0]
        self.assertEqual(damage, 20)
        self.assertEqual(resultString, 'attacker throws defender for 20 damage!')

    #-------------------------Spanking----------------------------

    def test_spanking_otk(self):
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 0
        while effect <= 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.attacker.terminate_spanking()
            except AttributeError:
                pass
            resultString, effect, _ = self.otk.effect(allies=self.allies, enemies=self.enemies) 
            effect = effect[0]
        self.assertTrue(self.defender.is_inflicted_with(statusEffects.Humiliated.name))
        self.assertEqual(effect, 2)
        self.assertEqual(resultString, "attacker spanks defender otk!")

    def test_spanking_attacker_spanked(self):
        """
        Tests to make sure the attacker doesn't do anything if she tries to spank an opponent, but she herself gets spanked first
        """
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 0
        defender_spanks = combatAction.SpankAction(self.defender, [self.attacker], positions.overTheKnee)
        while effect <= 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.defender.terminate_spanking()
            except AttributeError:
                pass
            _, effect, _ = defender_spanks.effect(allies=self.enemies, enemies=self.allies)
            effect = effect[0]
        resultString, effect, _ = self.otk.effect(allies=self.allies, enemies=self.enemies) 
        self.assertIsNone(effect[0])
        self.assertEqual(resultString, '')

    def test_spanking_defender_not_in_opponents(self):
        self.set_equal_grapple_stats()
        self.grapple()
        resultString, effect, _ = self.otk.effect(allies=self.allies, enemies=[enemy for enemy in self.enemies if self.defender != enemy])
        self.assertIsNone(effect[0])
        self.assertEqual(resultString, "attacker defends herself!")

    def test_spanking_attacker_defender_not_grappling(self):
        self.set_equal_grapple_stats()
        self.set_attack_stats(10, 10, 40)
        resultString, effect, _ = self.otk.effect(allies=self.allies, enemies=self.enemies)
        self.assertEqual(effect[0], 30)
        self.assertEqual(resultString, "attacker hits defender for 30 damage!")

    def test_spanking_attacker_defender_not_grappling_attacker_higher_grapple(self):
        self.set_slightly_greater_grapple_stats()
        resultString, effect, _ = self.otk.effect(allies=self.allies, enemies=self.enemies)
        self.assertEqual(effect[0], 45)
        self.assertEqual(resultString, "attacker grapples defender!")

    def test_spanking_reverse_otk(self):
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 1
        while effect > 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.attacker.terminate_spanking()
            except AttributeError:
                pass
            resultString, effect, _ = self.otk.effect(allies=self.allies, enemies=self.enemies) 
            effect = effect[0]
        self.assertTrue(self.attacker.is_inflicted_with(statusEffects.Humiliated.name))
        self.assertEqual(effect, -2)
        self.assertEqual(resultString, "defender reverses attacker otk!")

    def test_spanking_standing(self):
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 0
        while effect <= 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.attacker.terminate_spanking()
            except AttributeError:
                pass
            resultString, effect, _ = self.standing.effect(allies=self.allies, enemies=self.enemies) 
            effect = effect[0]
        self.assertTrue(self.defender.is_inflicted_with(statusEffects.Humiliated.name))
        self.assertEqual(effect, 4)
        self.assertEqual(resultString, "attacker spanks defender standing!")

    def test_spanking_reverse_standing(self):
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 1
        while effect > 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.attacker.terminate_spanking()
            except AttributeError:
                pass
            resultString, effect, _ = self.standing.effect(allies=self.allies, enemies=self.enemies) 
            effect = effect[0]
        self.assertTrue(self.attacker.is_inflicted_with(statusEffects.Humiliated.name))
        self.assertEqual(effect, -2)
        self.assertEqual(resultString, "defender reverses attacker standing!")

    def test_spanking_reverse_on_the_ground(self):
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 1
        while effect > 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.attacker.terminate_spanking()
            except AttributeError:
                pass
            resultString, effect, _ = self.onTheGround.effect(allies=self.allies, enemies=self.enemies) 
            effect = effect[0]
        self.assertTrue(self.attacker.is_inflicted_with(statusEffects.Humiliated.name))
        self.assertEqual(effect, -2)
        self.assertEqual(resultString, "defender reverses attacker on the ground!")

    def test_spanking_on_the_ground(self):
        self.set_equal_grapple_stats()
        self.grapple()
        effect = 0
        while effect <= 0:
            self.attacker.clear_statuses()
            self.defender.clear_statuses()
            try:
                self.attacker.terminate_spanking()
            except AttributeError:
                pass
            resultString, effect, _ = self.onTheGround.effect(allies=self.allies, enemies=self.enemies) 
            effect = effect[0]
        self.assertTrue(self.defender.is_inflicted_with(statusEffects.Humiliated.name))
        self.assertEqual(effect, 6)
        self.assertEqual(resultString, "attacker spanks defender on the ground!")





    #--------------------------Spells------------------------------

    #--------------------------Firebolt------------------------------

    def test_firebolt_just_started_being_spanked(self):
        pass

    def test_firebolt(self):
        pass
        #result, effects, action = self.firebolt.effect(allies=self.allies, enemies=self.enemies)


combatSuite = unittest.TestLoader().loadTestsFromTestCase(TestCombatActions)
