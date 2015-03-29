import enemytests
import unittest

pwSuite = unittest.TestSuite([enemytests.enemyTestSuite])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(pwSuite)
