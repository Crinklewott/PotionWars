import unittest
import enemy_test
import combat_test
import dialogue_test

pwSuite = unittest.TestSuite([combat_test.combatSuite, enemy_test.enemyTestSuite, 
    dialogue_test.dialogueSuite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(pwSuite)
