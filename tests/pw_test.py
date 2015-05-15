import sys
import unittest
import tests.enemy_test
import tests.combat_test
import tests.dialogue_test

pwSuite = unittest.TestSuite([tests.combat_test.combatSuite, tests.enemy_test.enemyTestSuite, 
    tests.dialogue_test.dialogueSuite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(pwSuite)
