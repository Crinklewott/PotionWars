import combatTests
import unittest

pwSuite = unittest.TestSuite([combatTests.combatSuite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(pwSuite)
