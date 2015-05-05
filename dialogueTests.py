import unittest
import episode
import episode1
import episode2
import episode2CharRooms
import conversation
import person
import universal
import pygame

def debug_mode():
    pass

class DummyEpisode():

    def next_scene(self):
        pass

class TestNodes(unittest.TestCase):
    """
    Executes a conversation on each node currently constructed. This is just to make sure that there aren't any typos or crashes in the text. It does not check to make sure the text is correct.
    That needs to be handled by good old fashioned proofreading.
    """

    def setUp(self):
        episode2.init_scene_1_episode_2()
        #Used so that the litanies don't crash if they refer to the player.
        dummy = person.PlayerCharacter("Juliana", 0)
        dummy.bodyType = person.BODY_TYPES[0]
        dummy.musculature = person.MUSCULATURE[0]
        dummy.hairLength = person.HAIR_LENGTH[0]
        dummy.height = person.HEIGHTS[0]
        dummy.currentEpisode = 0 
        universal.state.player = dummy
        conversation.globalModeIn = debug_mode
        universal.commandView = pygame.Rect(0, 0, 0, 0)
        universal.screen = pygame.Surface((0, 0))
        pygame.init()
        pygame.display.set_mode((0, 0))
        def next_scene():
            pass
        episode.allEpisodes[0] = DummyEpisode()

    def test_dialogue(self):
        for nodeName, node in conversation.allNodeNames.iteritems():
            print("Testing " + nodeName)
            node.quip_function()

dialogueSuite = unittest.TestLoader().loadTestsFromTestCase(TestNodes)




