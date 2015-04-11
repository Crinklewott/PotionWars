import unittest
import enemytests
import combatTests
import dialogueTests

pwSuite = unittest.TestSuite([combatTests.combatSuite, enemytests.enemyTestSuite, dialogueTests.dialogueSuite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(pwSuite)
