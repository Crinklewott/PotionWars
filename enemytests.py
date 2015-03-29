import episode1
import person
import pwenemies
import unittest


class TestEnemyMethods(unittest.TestCase):

    def setUp(self):
        self.warrior = pwenemies.VengadorWarrior(person.FEMALE)
        self.slinger = pwenemies.VengadorSpellslinger(person.FEMALE)
        self.scout = pwenemies.VengadorSpellslinger(person.FEMALE)
        self.necia = episode1.Necia(None, None, printedName="Vengador's Companion")
        self.edita = episode1.Edita(None, None, printedName="Young Vengador")

    def test_warrior_spanking(self):
        enemy = self.warrior
        for position in enemy.spankingFunctions:
            intro, duringRound, failure, reversal = enemy.spankingFunctions[position]
            print(intro(enemy, self.slinger))
            print('---------------------')
            print(duringRound(enemy, self.slinger))
            print('---------------------')
            print(failure(enemy, self.slinger))
            print('---------------------')
            print(reversal(enemy, self.slinger))

    def test_slinger_spanking(self):
        enemy = self.slinger
        for position in enemy.spankingFunctions:
            intro, duringRound, failure, reversal = enemy.spankingFunctions[position]
            print(intro(enemy, self.slinger))
            print('---------------------')
            print(duringRound(enemy, self.slinger))
            print('---------------------')
            print(failure(enemy, self.slinger))
            print('---------------------')
            print(reversal(enemy, self.slinger))

    def test_scout_spanking(self):
        enemy = self.scout
        for position in enemy.spankingFunctions:
            intro, duringRound, failure, reversal = enemy.spankingFunctions[position]
            print(intro(enemy, self.slinger))
            print('---------------------')
            print(duringRound(enemy, self.slinger))
            print('---------------------')
            print(failure(enemy, self.slinger))
            print('---------------------')
            print(reversal(enemy, self.slinger))

    def test_necia_spanking(self):
        enemy = self.necia
        for position in enemy.spankingFunctions:
            intro, duringRound, failure, reversal = enemy.spankingFunctions[position]
            print(intro(enemy, self.slinger))
            print('---------------------')
            print(duringRound(enemy, self.slinger))
            print('---------------------')
            print(failure(enemy, self.slinger))
            print('---------------------')
            print(reversal(enemy, self.slinger))
             
    def test_edita_spanking(self):
        enemy = self.edita
        for position in enemy.spankingFunctions:
            intro, duringRound, failure, reversal = enemy.spankingFunctions[position]
            print(intro(enemy, self.slinger))
            print('---------------------')
            print(duringRound(enemy, self.slinger))
            print('---------------------')
            print(failure(enemy, self.slinger))
            print('---------------------')
            print(reversal(enemy, self.slinger))

enemyTestSuite = unittest.TestLoader().loadTestsFromTestCase(TestEnemyMethods)

