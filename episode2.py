import universal
import textCommandsMusic
import person
import items
import pwenemies
import dungeonmode
import itemspotionwars
import random
import conversation
import episode
import townmode
import episode2CharRooms




def init_episode_2_scene_1():
    episode2.currentSceneIndex = 0 if episode2.currentSceneIndex != 0 else episode2.currentSceneIndex
    episode2CharRooms.build_chars()
    episode2CharRooms.build_rooms()
    ep2_wakeup = conversation.Node( 327 )

    def ep2_wakeup_quip_function():
        ep2_wakeup.quip = universal.format_text_no_space([[''''''],
['''''']])
        if True:
            ep2_wakeup.quip = universal.format_text_no_space([[ep2_wakeup.quip,'''Testing''']])
''']])

    
    ep2_wakeup.quip_function = ep2_wakeup_quip_function


def start_scene_1_episode_2(loading=False):
    universal.state.set_init_scene(init_episode_2_scene_1)
    asdfasd
    universal.state.player.litany = 327
    conversation.converse_with(universal.state.player, townmode.town_mode)




episode2Scene1 = episode.Scene('episode_2 Scene 1', start_scene_1_episode_2, end_scene_1_episode_2)
episode2Scene1.init_scene = init_episode_2_scene_1


def init_episode_2():
    if universal.state.location == universal.state.get_room("offStage"):
        episode2Scene1.init_scene()
        episode2.start_episode()


episode2 = episode.Episode(2, "Back Alleys", scenes=[episode2Scene1], init=init_episode_2, titleTheme=textCommandsMusic.CARLITA)